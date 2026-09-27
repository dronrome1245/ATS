from __future__ import annotations

import csv
from datetime import UTC, datetime

import pytest

import tools.hyp0004_development_data as prep


def synthetic_row(timestamp: datetime, bucket: str | None = None) -> dict[str, object]:
    return {
        "event_time": timestamp,
        "event_time_text": prep.iso_z(timestamp),
        "availability_time_text": prep.iso_z(timestamp.replace(tzinfo=UTC) + prep.timedelta(hours=1)),
        "parent_sequence": 1,
        "source_symbol": "EURUSD",
        "bid_open_text": "1.1000",
        "ask_open_text": "1.1002",
        "utc_bucket": bucket or prep.bucket_for_hour(timestamp.hour),
    }


def write_parent_csv(path, rows: list[dict[str, str]]) -> None:
    fieldnames = (
        "event_time",
        "availability_time",
        "currency",
        "source_symbol",
        "source_orientation",
        "sequence",
        "bid_open",
        "ask_open",
    )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def test_bucket_mapping_is_frozen() -> None:
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


def test_parse_utc_hour_rejects_non_hour_boundary() -> None:
    with pytest.raises(prep.DevelopmentDataPrepError, match="exact hourly boundary"):
        prep.parse_utc_hour("2021-08-02T07:30:00Z")


def test_geometry_summary_counts_exact_next_hour_without_outcomes() -> None:
    rows = [
        synthetic_row(datetime(2021, 8, 2, 6, tzinfo=UTC)),
        synthetic_row(datetime(2021, 8, 2, 7, tzinfo=UTC)),
        synthetic_row(datetime(2021, 8, 2, 8, tzinfo=UTC)),
    ]

    result = prep.geometry_summary(rows)

    assert result["eligible_exact_next_hour_count"] == 2
    assert result["eligible_rows_by_bucket"] == {
        "CORE_ACTIVE": 1,
        "OFF_HOURS": 1,
        "TRANSITION": 0,
    }
    assert result["ineligible_dataset_end_count"] == 1
    assert "abs_next_1h_return" not in result
    assert "relative_spread" not in result


def test_geometry_summary_distinguishes_closed_and_missing_hours() -> None:
    friday = datetime(2021, 8, 6, 20, tzinfo=UTC)
    sunday = datetime(2021, 8, 8, 21, tzinfo=UTC)
    closed_rows = [synthetic_row(friday), synthetic_row(sunday)]

    closed = prep.geometry_summary(closed_rows)

    assert closed["ineligible_closed_market_next_hour_count"] == 1
    assert closed["ineligible_dataset_end_count"] == 1

    monday_06 = datetime(2021, 8, 9, 6, tzinfo=UTC)
    monday_08 = datetime(2021, 8, 9, 8, tzinfo=UTC)
    missing = prep.geometry_summary([synthetic_row(monday_06), synthetic_row(monday_08)])

    assert missing["ineligible_missing_expected_next_hour_count"] == 1
    assert missing["ineligible_dataset_end_count"] == 1


def test_preparation_decision_requires_primary_bucket_geometry() -> None:
    ready = {
        "eligible_rows_by_bucket": {
            "CORE_ACTIVE": 10,
            "TRANSITION": 3,
            "OFF_HOURS": 8,
        }
    }
    insufficient = {
        "eligible_rows_by_bucket": {
            "CORE_ACTIVE": 10,
            "TRANSITION": 3,
            "OFF_HOURS": 0,
        }
    }

    assert prep.preparation_decision(ready) == "READY_FOR_DEVELOPMENT_DATA_FREEZE"
    assert prep.preparation_decision(insufficient) == "INSUFFICIENT_DEVELOPMENT_DATA"


def test_load_eurusd_rows_verifies_parent_identity_and_filters(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    parent = tmp_path / "parent.csv"
    write_parent_csv(
        parent,
        [
            {
                "event_time": "2021-08-02T07:00:00Z",
                "availability_time": "2021-08-02T08:00:00Z",
                "currency": "EUR",
                "source_symbol": "EURUSD",
                "source_orientation": "DIRECT",
                "sequence": "10",
                "bid_open": "1.1000",
                "ask_open": "1.1002",
            },
            {
                "event_time": "2021-08-02T07:00:00Z",
                "availability_time": "2021-08-02T08:00:00Z",
                "currency": "GBP",
                "source_symbol": "GBPUSD",
                "source_orientation": "DIRECT",
                "sequence": "11",
                "bid_open": "1.3900",
                "ask_open": "1.3902",
            },
        ],
    )
    monkeypatch.setattr(prep, "EXPECTED_PARENT_SHA256", prep.sha256_file(parent))

    rows = prep.load_eurusd_rows(parent)

    assert len(rows) == 1
    assert rows[0]["source_symbol"] == "EURUSD"
    assert rows[0]["parent_sequence"] == 10
    assert rows[0]["utc_bucket"] == "CORE_ACTIVE"


def test_load_eurusd_rows_rejects_boundary_crossing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    parent = tmp_path / "parent.csv"
    write_parent_csv(
        parent,
        [
            {
                "event_time": "2021-08-02T07:00:00Z",
                "availability_time": "2021-08-02T08:00:00Z",
                "currency": "EUR",
                "source_symbol": "EURUSD",
                "source_orientation": "DIRECT",
                "sequence": "10",
                "bid_open": "1.1002",
                "ask_open": "1.1000",
            }
        ],
    )
    monkeypatch.setattr(prep, "EXPECTED_PARENT_SHA256", prep.sha256_file(parent))

    with pytest.raises(prep.DevelopmentDataPrepError, match="ask_open < bid_open"):
        prep.load_eurusd_rows(parent)


def test_derived_csv_contains_no_hypothesis_outcome_columns(tmp_path) -> None:
    rows = [
        synthetic_row(datetime(2021, 8, 2, 7, tzinfo=UTC)),
        synthetic_row(datetime(2021, 8, 2, 8, tzinfo=UTC)),
    ]
    destination = tmp_path / "derived.csv"

    first_hash = prep.write_derived_csv(rows, destination)
    first_bytes = destination.read_bytes()
    second_hash = prep.write_derived_csv(rows, destination)

    assert first_hash == second_hash
    assert first_bytes == destination.read_bytes()
    header = destination.read_text(encoding="utf-8").splitlines()[0]
    assert "abs_next_1h_return" not in header
    assert "relative_spread" not in header
    assert "utc_bucket" in header
