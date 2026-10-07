from __future__ import annotations

import tools.hyp0006_data_tolerance_freeze as freeze


def geometry_row(
    *,
    pre_prev: int = 100,
    pre_next: int = 200,
    pre_release: int = 50,
    post_prev: int = 300,
    post_next: int = 400,
) -> dict[str, str]:
    return {
        "event_id": "BLS-CPI-TEST",
        "archive_release_date": "2020-01-01",
        "release_time_utc": "2020-01-01T13:30:00Z",
        "archive_zone_label": "ET",
        "schedule_crosscheck_status": "FROZEN_OFFICIAL_SCHEDULE",
        "same_time_bls_labels": "Consumer Price Index|Real Earnings",
        "required_tick_object_count": "5",
        "missing_tick_object_count": "0",
        "pre60_prev_gap_ms": str(pre_prev),
        "pre60_next_gap_ms": str(pre_next),
        "pre_release_last_gap_ms": str(pre_release),
        "post60_prev_gap_ms": str(post_prev),
        "post60_next_gap_ms": str(post_next),
        "quote_geometry_status": "COMPLETE_TIMESTAMP_GEOMETRY",
    }


def test_numeric_tolerances_are_frozen_before_reveal() -> None:
    assert freeze.BOUNDARY_MAX_ABS_GAP_MS == 30_000
    assert freeze.PRE_RELEASE_MAX_STALENESS_MS == 30_000


def test_nearest_anchor_tie_break_prefers_previous() -> None:
    assert freeze.nearest_side(10, 10) == ("PREVIOUS", 10)
    assert freeze.nearest_side(11, 10) == ("NEXT", 10)


def test_geometry_at_frozen_limits_is_eligible() -> None:
    result = freeze.evaluate_geometry_row(
        geometry_row(
            pre_prev=30_000,
            pre_next=40_000,
            pre_release=30_000,
            post_prev=35_000,
            post_next=30_000,
        )
    )
    assert result["eligible"] is True
    assert result["pre60_selected_side"] == "PREVIOUS"
    assert result["post60_selected_side"] == "NEXT"


def test_geometry_above_any_frozen_limit_is_excluded() -> None:
    result = freeze.evaluate_geometry_row(
        geometry_row(
            pre_prev=30_001,
            pre_next=40_000,
            pre_release=30_001,
            post_prev=30_001,
            post_next=40_000,
        )
    )
    assert result["eligible"] is False
    assert result["exclusion_reasons"] == [
        "PRE_60_ANCHOR_GAP_EXCEEDS_30000MS",
        "PRE_RELEASE_STALENESS_EXCEEDS_30000MS",
        "POST_60_ANCHOR_GAP_EXCEEDS_30000MS",
    ]


def test_incomplete_or_missing_source_geometry_is_excluded() -> None:
    row = geometry_row()
    row["quote_geometry_status"] = "INCOMPLETE"
    row["missing_tick_object_count"] = "1"
    result = freeze.evaluate_geometry_row(row)
    assert result["eligible"] is False
    assert "INCOMPLETE_TIMESTAMP_GEOMETRY" in result["exclusion_reasons"]
    assert "MISSING_TICK_OBJECT" in result["exclusion_reasons"]


def test_freeze_contract_contains_no_market_outcome_calculation() -> None:
    assert freeze.PRE_RELEASE_RULE == "LAST_QUOTE_STRICTLY_BEFORE_RELEASE"
    assert freeze.PRICE_PAIRING_RULE == "BID_AND_ASK_FROM_SAME_RAW_TICK_RECORD"
    assert freeze.DUPLICATE_TIMESTAMP_TIE_BREAK == "LAST_RAW_RECORD_AT_SELECTED_MILLISECOND"
