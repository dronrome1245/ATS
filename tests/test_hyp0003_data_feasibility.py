from __future__ import annotations

from datetime import UTC, datetime

import pytest

import tools.hyp0003_data_feasibility as feasibility
from tools.hyp0003_data_feasibility import (
    month_from_number,
    month_number,
    normalized_bid_ask,
    previous_month,
    source_url,
)


def test_month_index_round_trip_and_previous_month() -> None:
    month = datetime(2021, 1, 1, tzinfo=UTC)
    assert month_from_number(month_number(month)) == month
    assert previous_month(month) == datetime(2020, 12, 1, tzinfo=UTC)


def test_source_url_uses_zero_based_dukascopy_month() -> None:
    month = datetime(2021, 8, 1, tzinfo=UTC)
    assert source_url(
        "https://datafeed.dukascopy.com/datafeed",
        "EURUSD",
        month,
        "BID",
    ).endswith("/EURUSD/2021/07/BID_candles_hour_1.bi5")


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
        datetime(1997, 11, 1, tzinfo=UTC),
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
