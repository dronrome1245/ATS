from __future__ import annotations

from datetime import UTC, datetime

import tools.hyp0005_data_feasibility as prep


def test_direct_script_import_mode_resolves_sibling_tool() -> None:
    import subprocess
    import sys

    code = "import os; os.chdir('tools'); import hyp0005_data_feasibility; print('IMPORT_OK')"
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=prep.ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert completed.stdout.strip() == "IMPORT_OK"


def synthetic_row(timestamp: datetime, segment: str) -> dict[str, object]:
    return {
        "event_time": timestamp,
        "event_time_text": prep.iso_z(timestamp),
        "availability_time_text": prep.iso_z(timestamp),
        "source_bar_completion_time_text": prep.iso_z(
            timestamp.replace(tzinfo=UTC) + prep.timedelta(hours=1)
        ),
        "confirmatory_segment": segment,
        "source_symbol": "EURUSD",
        "bid_open": 1.1000,
        "ask_open": 1.1002,
        "utc_bucket": prep.bucket_for_hour(timestamp.hour),
    }


def test_frozen_segments_do_not_overlap_consumed_project_interval() -> None:
    prep.assert_frozen_boundaries()

    assert prep.LEFT_END == prep.CONSUMED_START
    assert prep.RIGHT_START == prep.CONSUMED_END
    assert prep.segment_for_time(prep.LEFT_END) is None
    assert prep.segment_for_time(prep.RIGHT_START) == "RIGHT_UNSEEN"


def test_source_months_are_exactly_predeclared() -> None:
    assert [(value.year, value.month) for value in prep.source_months()] == [
        (2003, 5),
        (2003, 6),
        (2003, 7),
        (2003, 8),
        (2026, 9),
    ]


def test_bucket_mapping_is_inherited_without_change() -> None:
    assert [prep.bucket_for_hour(hour) for hour in range(24)] == [
        "OFF_HOURS",
        "OFF_HOURS",
        "OFF_HOURS",
        "OFF_HOURS",
        "OFF_HOURS",
        "OFF_HOURS",
        "OFF_HOURS",
        "CORE_ACTIVE",
        "CORE_ACTIVE",
        "CORE_ACTIVE",
        "CORE_ACTIVE",
        "CORE_ACTIVE",
        "CORE_ACTIVE",
        "CORE_ACTIVE",
        "CORE_ACTIVE",
        "CORE_ACTIVE",
        "CORE_ACTIVE",
        "TRANSITION",
        "TRANSITION",
        "TRANSITION",
        "TRANSITION",
        "OFF_HOURS",
        "OFF_HOURS",
        "OFF_HOURS",
    ]


def test_geometry_counts_each_segment_without_bridging_gap() -> None:
    rows = []
    for segment, start in (
        ("LEFT_UNSEEN", datetime(2003, 5, 5, 6, tzinfo=UTC)),
        ("RIGHT_UNSEEN", datetime(2026, 9, 1, 6, tzinfo=UTC)),
    ):
        rows.extend(
            [
                synthetic_row(start, segment),
                synthetic_row(start.replace(hour=7), segment),
                synthetic_row(start.replace(hour=8), segment),
            ]
        )

    result = prep.geometry_summary(rows)

    assert result["eligible_exact_next_hour_count"] == 4
    assert result["eligible_rows_by_segment"] == {
        "LEFT_UNSEEN": 2,
        "RIGHT_UNSEEN": 2,
    }
    assert result["eligible_rows_by_bucket"]["CORE_ACTIVE"] == 2
    assert result["eligible_rows_by_bucket"]["OFF_HOURS"] == 2
    assert result["ineligible_missing_expected_next_hour_count"] == 2


def test_preparation_decision_requires_both_segments_and_primary_buckets() -> None:
    ready = {
        "eligible_rows_by_bucket": {
            "CORE_ACTIVE": 10,
            "TRANSITION": 4,
            "OFF_HOURS": 8,
        },
        "eligible_rows_by_segment": {
            "LEFT_UNSEEN": 11,
            "RIGHT_UNSEEN": 11,
        },
    }
    insufficient = {
        "eligible_rows_by_bucket": {
            "CORE_ACTIVE": 10,
            "TRANSITION": 4,
            "OFF_HOURS": 8,
        },
        "eligible_rows_by_segment": {
            "LEFT_UNSEEN": 22,
            "RIGHT_UNSEEN": 0,
        },
    }

    assert prep.preparation_decision(ready) == "READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE"
    assert prep.preparation_decision(insufficient) == "INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY"


def test_derived_csv_contains_no_hypothesis_outcome_columns(tmp_path) -> None:
    rows = [
        synthetic_row(datetime(2003, 5, 5, 6, tzinfo=UTC), "LEFT_UNSEEN"),
        synthetic_row(datetime(2003, 5, 5, 7, tzinfo=UTC), "LEFT_UNSEEN"),
    ]
    destination = tmp_path / "confirmatory.csv"

    first_hash = prep.write_derived_csv(rows, destination)
    first_bytes = destination.read_bytes()
    second_hash = prep.write_derived_csv(rows, destination)

    assert first_hash == second_hash
    assert first_bytes == destination.read_bytes()
    header = destination.read_text(encoding="utf-8").splitlines()[0]
    assert "abs_next_1h_return" not in header
    assert "relative_spread" not in header
    assert "utc_bucket" in header
    assert "confirmatory_segment" in header
