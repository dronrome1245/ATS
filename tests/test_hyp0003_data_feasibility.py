from __future__ import annotations

import struct
from datetime import UTC, datetime

import pytest

import tools.hyp0003_data_feasibility as feasibility
from tools.hyp0003_data_feasibility import (
    history_start_datetime,
    normalized_bid_ask,
    parse_history_start,
    parse_instruments_jsonp,
    source_url,
)


def test_source_url_uses_zero_based_dukascopy_month() -> None:
    month = datetime(2021, 8, 1, tzinfo=UTC)
    assert source_url(
        "https://datafeed.dukascopy.com/datafeed",
        "EURUSD",
        month,
        "BID",
    ).endswith("/EURUSD/2021/07/BID_candles_hour_1.bi5")


def test_parse_history_start_h1_metadata() -> None:
    name = b"AUDUSD"
    payload = b"".join(
        (
            struct.pack(">H", len(name)),
            name,
            struct.pack(">Q", 2),
            struct.pack(">Q", 60_000),
            struct.pack(">Q", 1_100_000_000_000),
            struct.pack(">Q", 3_600_000),
            struct.pack(">Q", 1_200_000_000_000),
        )
    )

    history = parse_history_start(payload)

    assert history["AUDUSD"][3_600_000] == 1_200_000_000_000
    assert history_start_datetime(history, "AUDUSD") == datetime.fromtimestamp(
        1_200_000_000,
        tz=UTC,
    )


def test_parse_instruments_jsonp_h1_fallback() -> None:
    payload = (
        b'jsonp({"instruments":{"1":{"historical_filename":"AUDUSD",'
        b'"history_start_60min":1200000000000}}})'
    )

    history = parse_instruments_jsonp(payload)

    assert history["AUDUSD"][3_600_000] == 1_200_000_000_000


def test_load_history_metadata_falls_back_to_instruments_jsonp(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    fallback = tmp_path / "instruments.jsonp"
    fallback.write_bytes(
        b'jsonp({"instruments":{"1":{"historical_filename":"AUDUSD",'
        b'"history_start_60min":1200000000000}}})'
    )
    calls: list[str] = []

    def fake_cached_or_fetch_any(
        _urls: tuple[str, ...],
        _destination,
        label: str,
    ):
        calls.append(label)
        if "HistoryStart" in label:
            raise feasibility.ProbeError("metadata timeout")
        return fallback, {"source_url": "INSTRUMENTS_FALLBACK"}

    monkeypatch.setattr(
        feasibility,
        "cached_or_fetch_any",
        fake_cached_or_fetch_any,
    )

    history, source_url, digest = feasibility.load_history_metadata()

    assert source_url == "INSTRUMENTS_FALLBACK"
    assert history["AUDUSD"][3_600_000] == 1_200_000_000_000
    assert len(digest) == 64
    assert calls == [
        "Dukascopy HistoryStart.bi5",
        "Dukascopy instruments metadata",
    ]


def test_fetch_bytes_sets_freeserv_referer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, str | None] = {}

    class FakeResponse:
        headers = {"Last-Modified": "test", "ETag": "test"}

        def __enter__(self) -> "FakeResponse":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def read(self) -> bytes:
            return b'jsonp({"instruments":{}})'

    def fake_urlopen(
        request: feasibility.urllib.request.Request,
        **_kwargs: object,
    ) -> FakeResponse:
        captured["referer"] = request.get_header("Referer")
        return FakeResponse()

    monkeypatch.setattr(feasibility.urllib.request, "urlopen", fake_urlopen)

    body, _headers = feasibility.fetch_bytes(feasibility.INSTRUMENTS_URL)

    assert body.startswith(b"jsonp(")
    assert captured["referer"] == feasibility.FREESERV_REFERER


def test_fetch_bytes_normalizes_direct_oserror(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_urlopen(*_args: object, **_kwargs: object) -> object:
        raise ConnectionResetError(10054, "connection reset")

    monkeypatch.setattr(feasibility.urllib.request, "urlopen", fail_urlopen)

    with pytest.raises(feasibility.ProbeError, match="network error while probing"):
        feasibility.fetch_bytes("https://example.invalid/test")


def test_probe_side_resilient_retries_transient_network_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, datetime, str]] = []

    def fake_probe_side(
        symbol: str,
        month: datetime,
        side: str,
    ) -> feasibility.ProbeObject | None:
        calls.append((symbol, month, side))
        if len(calls) < 3:
            raise feasibility.ProbeError("transient network failure")
        return None

    monkeypatch.setattr(feasibility, "probe_side", fake_probe_side)
    monkeypatch.setattr(feasibility.time, "sleep", lambda _delay: None)

    result = feasibility.probe_side_resilient(
        "AUDUSD",
        datetime(2021, 8, 1, tzinfo=UTC),
        "BID",
    )

    assert result is None
    assert len(calls) == 3


def test_normalized_bid_ask_preserves_executable_order() -> None:
    direct_bid, direct_ask = normalized_bid_ask(1.1, 1.2, "DIRECT")
    assert (direct_bid, direct_ask) == (1.1, 1.2)

    inverse_bid, inverse_ask = normalized_bid_ask(1.1, 1.2, "INVERSE")
    assert inverse_bid == pytest.approx(1.0 / 1.2)
    assert inverse_ask == pytest.approx(1.0 / 1.1)
    assert inverse_ask >= inverse_bid

    with pytest.raises(ValueError):
        normalized_bid_ask(1.2, 1.1, "DIRECT")
