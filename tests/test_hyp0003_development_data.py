from __future__ import annotations

import lzma
from datetime import UTC, datetime

import pytest

import tools.hyp0003_development_data as prep


def test_development_months_are_frozen_before_protected_tail() -> None:
    months = prep.development_months()

    assert len(months) == 217
    assert months[0] == datetime(2003, 8, 1, tzinfo=UTC)
    assert months[-1] == datetime(2021, 8, 1, tzinfo=UTC)
    assert all(month < prep.DATA_END for month in months)


def test_point_divisors_are_explicit_and_jpy_specific() -> None:
    assert prep.POINT_DIVISORS == {
        "AUDUSD": 100_000,
        "USDCAD": 100_000,
        "USDCHF": 100_000,
        "EURUSD": 100_000,
        "GBPUSD": 100_000,
        "USDJPY": 1_000,
        "USDNOK": 100_000,
        "NZDUSD": 100_000,
        "USDSEK": 100_000,
    }


def test_decode_month_uses_frozen_point_divisor(tmp_path) -> None:
    month = datetime(2021, 8, 1, tzinfo=UTC)
    path = tmp_path / "BID_candles_hour_1.bi5"
    raw = prep.RECORD.pack(
        3_600,
        110_123,
        110_150,
        110_000,
        110_200,
        1.0,
    )
    path.write_bytes(lzma.compress(raw))

    decoded = prep.decode_month(
        path,
        month,
        prep.POINT_DIVISORS["USDJPY"],
    )

    assert decoded[datetime(2021, 8, 1, 1, tzinfo=UTC)] == pytest.approx(
        (110.123, 110.2, 110.0, 110.15)
    )


def test_decode_month_rejects_out_of_order_records(tmp_path) -> None:
    month = datetime(2021, 8, 1, tzinfo=UTC)
    path = tmp_path / "BID_candles_hour_1.bi5"
    first = prep.RECORD.pack(
        7_200,
        123_000,
        123_100,
        122_900,
        123_200,
        1.0,
    )
    second = prep.RECORD.pack(
        3_600,
        123_000,
        123_100,
        122_900,
        123_200,
        1.0,
    )
    path.write_bytes(lzma.compress(first + second))

    with pytest.raises(
        prep.DevelopmentDataPrepError,
        match="out-of-order",
    ):
        prep.decode_month(path, month, 100_000)


def test_normalize_pair_ohlc_preserves_execution_order() -> None:
    bid = (110.0, 111.0, 109.0, 110.5)
    ask = (110.1, 111.1, 109.1, 110.6)

    direct_bid, direct_ask = prep.normalize_pair_ohlc(
        bid,
        ask,
        "DIRECT",
    )
    assert direct_bid == bid
    assert direct_ask == ask

    inverse_bid, inverse_ask = prep.normalize_pair_ohlc(
        bid,
        ask,
        "INVERSE",
    )
    assert inverse_bid == pytest.approx((1.0 / 110.1, 1.0 / 109.1, 1.0 / 111.1, 1.0 / 110.6))
    assert inverse_ask == pytest.approx((1.0 / 110.0, 1.0 / 109.0, 1.0 / 111.0, 1.0 / 110.5))
    assert all(inverse_ask[index] >= inverse_bid[index] for index in range(4))


def test_source_bundle_hash_is_order_independent() -> None:
    first = {
        "symbol": "EURUSD",
        "month": "2021-08",
        "side": "BID",
        "sha256": "a" * 64,
        "source_url": "ignored",
    }
    second = {
        "symbol": "USDJPY",
        "month": "2021-08",
        "side": "ASK",
        "sha256": "b" * 64,
        "source_url": "ignored-too",
    }

    digest = prep.source_bundle_hash([first, second])

    assert digest == prep.source_bundle_hash([second, first])
    changed = dict(second)
    changed["sha256"] = "c" * 64
    assert digest != prep.source_bundle_hash([first, changed])


def test_monthly_cutoff_uses_last_expected_fx_market_hour() -> None:
    july = datetime(2021, 7, 1, tzinfo=UTC)

    assert prep.monthly_cutoff(july) == datetime(
        2021,
        7,
        30,
        20,
        tzinfo=UTC,
    )


def test_longest_12_12_geometry_respects_boundaries() -> None:
    assert not prep.supports_longest_12_12_geometry(datetime(2003, 7, 1, tzinfo=UTC))
    assert prep.supports_longest_12_12_geometry(datetime(2004, 8, 1, tzinfo=UTC))
    assert prep.supports_longest_12_12_geometry(datetime(2020, 7, 1, tzinfo=UTC))
    assert not prep.supports_longest_12_12_geometry(datetime(2020, 8, 1, tzinfo=UTC))


def test_download_source_rejects_protected_tail_before_network() -> None:
    with pytest.raises(
        prep.DevelopmentDataPrepError,
        match="protected-tail",
    ):
        prep.download_source_once(
            "EURUSD",
            datetime(2021, 9, 1, tzinfo=UTC),
            "BID",
        )


def test_download_source_resilient_retries_transient_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, datetime, str]] = []

    def fake_download_source_once(
        symbol: str,
        month: datetime,
        side: str,
    ):
        calls.append((symbol, month, side))
        if len(calls) < 3:
            raise prep.DevelopmentDataPrepError("transient")
        return None

    monkeypatch.setattr(
        prep,
        "download_source_once",
        fake_download_source_once,
    )
    monkeypatch.setattr(
        prep.time,
        "sleep",
        lambda _delay: None,
    )

    result = prep.download_source_resilient(
        "EURUSD",
        datetime(2021, 8, 1, tzinfo=UTC),
        "BID",
    )

    assert result is None
    assert len(calls) == 3
