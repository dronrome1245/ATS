"""Tests for the PROTO-01 EUR/USD market-session calendar."""

from datetime import UTC, datetime

from tools.proto01_eurusd import is_fx_market_hour, us_dst_active_utc


def test_us_dst_boundaries_2024() -> None:
    assert not us_dst_active_utc(datetime(2024, 3, 10, 6, 59, tzinfo=UTC))
    assert us_dst_active_utc(datetime(2024, 3, 10, 7, 0, tzinfo=UTC))
    assert us_dst_active_utc(datetime(2024, 11, 3, 5, 59, tzinfo=UTC))
    assert not us_dst_active_utc(datetime(2024, 11, 3, 6, 0, tzinfo=UTC))


def test_summer_fx_weekend_boundaries() -> None:
    assert is_fx_market_hour(datetime(2024, 7, 5, 20, 0, tzinfo=UTC))
    assert not is_fx_market_hour(datetime(2024, 7, 5, 21, 0, tzinfo=UTC))
    assert not is_fx_market_hour(datetime(2024, 7, 7, 20, 0, tzinfo=UTC))
    assert is_fx_market_hour(datetime(2024, 7, 7, 21, 0, tzinfo=UTC))


def test_winter_fx_weekend_boundaries() -> None:
    assert is_fx_market_hour(datetime(2024, 1, 12, 21, 0, tzinfo=UTC))
    assert not is_fx_market_hour(datetime(2024, 1, 12, 22, 0, tzinfo=UTC))
    assert not is_fx_market_hour(datetime(2024, 1, 14, 21, 0, tzinfo=UTC))
    assert is_fx_market_hour(datetime(2024, 1, 14, 22, 0, tzinfo=UTC))
