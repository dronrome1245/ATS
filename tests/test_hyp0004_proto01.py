"""Synthetic contract tests for frozen HYP-0004 PROTO-01 logic."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from tools.hyp0004_proto01 import (
    abs_next_1h_return,
    bucket_metrics,
    calendar_year_diagnostics,
    eligible_observations,
    midpoint,
    primary_summary,
    prototype_decision,
    relative_spread,
)


def observation(
    bucket: str,
    year: int,
    absolute_return: float,
    spread: float,
) -> dict[str, object]:
    return {
        "event_time": datetime(year, 1, 2, 12, tzinfo=UTC),
        "year": year,
        "utc_bucket": bucket,
        "abs_next_1h_return": absolute_return,
        "relative_spread": spread,
    }


def test_midpoint_spread_and_absolute_return_contract() -> None:
    assert midpoint(1.1000, 1.1002) == pytest.approx(1.1001)
    assert relative_spread(1.1000, 1.1002) == pytest.approx(0.0002 / 1.1001)

    value = abs_next_1h_return(1.1000, 1.1002, 1.1010, 1.1012)
    assert value == pytest.approx(abs(1.1011 / 1.1001 - 1.0))


def test_bucket_metrics_use_median_primary_statistics() -> None:
    observations = [
        observation("CORE_ACTIVE", 2020, 0.003, 0.00010),
        observation("CORE_ACTIVE", 2020, 0.001, 0.00020),
        observation("OFF_HOURS", 2020, 0.001, 0.00030),
        observation("OFF_HOURS", 2020, 0.0005, 0.00040),
        observation("TRANSITION", 2020, 0.002, 0.00025),
    ]

    metrics = bucket_metrics(observations)

    assert metrics["CORE_ACTIVE"]["observation_count"] == 2
    assert metrics["CORE_ACTIVE"]["mean_abs_next_1h_return"] == pytest.approx(0.002)
    assert metrics["CORE_ACTIVE"]["median_abs_next_1h_return"] == pytest.approx(0.002)
    assert metrics["CORE_ACTIVE"]["median_relative_spread"] == pytest.approx(0.00015)
    assert metrics["OFF_HOURS"]["median_abs_next_1h_return"] == pytest.approx(0.00075)


def test_primary_decision_requires_both_inequalities() -> None:
    passing = {
        "CORE_ACTIVE": {
            "observation_count": 10,
            "median_abs_next_1h_return": 0.002,
            "median_relative_spread": 0.0002,
        },
        "OFF_HOURS": {
            "observation_count": 10,
            "median_abs_next_1h_return": 0.001,
            "median_relative_spread": 0.0003,
        },
        "TRANSITION": {
            "observation_count": 10,
            "median_abs_next_1h_return": 999.0,
            "median_relative_spread": 999.0,
        },
    }

    assert primary_summary(passing) == {
        "movement_inequality_pass": True,
        "spread_inequality_pass": True,
        "both_primary_inequalities_pass": True,
    }
    assert prototype_decision(passing) == (
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "BOTH_PRIMARY_INEQUALITIES_MET",
        "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
    )

    movement_fail = {
        **passing,
        "CORE_ACTIVE": {
            **passing["CORE_ACTIVE"],
            "median_abs_next_1h_return": 0.001,
        },
    }
    assert prototype_decision(movement_fail) == (
        "REJECT",
        "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED",
        "STOP_HYP0004",
    )

    spread_fail = {
        **passing,
        "CORE_ACTIVE": {
            **passing["CORE_ACTIVE"],
            "median_relative_spread": 0.0004,
        },
    }
    assert prototype_decision(spread_fail) == (
        "REJECT",
        "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED",
        "STOP_HYP0004",
    )


def test_primary_decision_parks_when_primary_bucket_is_empty() -> None:
    metrics = {
        "CORE_ACTIVE": {
            "observation_count": 0,
            "median_abs_next_1h_return": None,
            "median_relative_spread": None,
        },
        "OFF_HOURS": {
            "observation_count": 10,
            "median_abs_next_1h_return": 0.001,
            "median_relative_spread": 0.0003,
        },
        "TRANSITION": {
            "observation_count": 0,
            "median_abs_next_1h_return": None,
            "median_relative_spread": None,
        },
    }

    assert prototype_decision(metrics) == (
        "PARK",
        "PRIMARY_BUCKET_HAS_ZERO_OBSERVATIONS",
        "PARK",
    )


def test_calendar_year_diagnostics_are_reporting_only() -> None:
    observations = [
        observation("CORE_ACTIVE", 2019, 0.001, 0.0002),
        observation("CORE_ACTIVE", 2020, 0.003, 0.0001),
        observation("CORE_ACTIVE", 2020, 0.005, 0.0003),
        observation("OFF_HOURS", 2020, 0.001, 0.0004),
    ]

    result = calendar_year_diagnostics(observations)

    assert result["CORE_ACTIVE"]["max_calendar_year_observation_share"] == pytest.approx(2 / 3)
    assert result["CORE_ACTIVE"]["years"]["2020"]["observation_count"] == 2
    assert result["CORE_ACTIVE"]["years"]["2020"][
        "median_abs_next_1h_return"
    ] == pytest.approx(0.004)
    assert result["CORE_ACTIVE"]["years"]["2020"]["median_relative_spread"] == pytest.approx(
        0.0002
    )


def test_exact_next_hour_geometry_does_not_bridge_closed_or_missing_hours() -> None:
    friday = datetime(2021, 8, 6, 20, tzinfo=UTC)
    sunday = datetime(2021, 8, 8, 21, tzinfo=UTC)
    monday_06 = datetime(2021, 8, 9, 6, tzinfo=UTC)
    monday_08 = datetime(2021, 8, 9, 8, tzinfo=UTC)

    rows = {
        friday: {
            "event_time": friday,
            "utc_bucket": "TRANSITION",
            "bid_open": 1.1000,
            "ask_open": 1.1002,
        },
        sunday: {
            "event_time": sunday,
            "utc_bucket": "OFF_HOURS",
            "bid_open": 1.1000,
            "ask_open": 1.1002,
        },
        monday_06: {
            "event_time": monday_06,
            "utc_bucket": "OFF_HOURS",
            "bid_open": 1.1000,
            "ask_open": 1.1002,
        },
        monday_08: {
            "event_time": monday_08,
            "utc_bucket": "CORE_ACTIVE",
            "bid_open": 1.1010,
            "ask_open": 1.1012,
        },
    }

    observations, geometry = eligible_observations(rows)

    assert observations == []
    assert geometry["ineligible_closed_market_next_hour_count"] == 1
    assert geometry["ineligible_missing_expected_next_hour_count"] == 2
    assert geometry["ineligible_dataset_end_count"] == 1


def test_adjacent_exact_hour_rows_form_one_observation_per_start_boundary() -> None:
    start = datetime(2021, 8, 9, 7, tzinfo=UTC)
    next_time = start + timedelta(hours=1)
    rows = {
        start: {
            "event_time": start,
            "utc_bucket": "CORE_ACTIVE",
            "bid_open": 1.1000,
            "ask_open": 1.1002,
        },
        next_time: {
            "event_time": next_time,
            "utc_bucket": "CORE_ACTIVE",
            "bid_open": 1.1010,
            "ask_open": 1.1012,
        },
    }

    observations, geometry = eligible_observations(rows)

    assert len(observations) == 1
    assert observations[0]["event_time"] == start
    assert geometry["eligible_count"] == 1
    assert geometry["ineligible_dataset_end_count"] == 1
