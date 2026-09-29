from __future__ import annotations

import csv
import lzma
import struct
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

import tools.hyp0006_data_feasibility as feasibility


def source_object(year: int) -> feasibility.SourceObject:
    return feasibility.SourceObject(
        category="BLS_SCHEDULE_SNAPSHOT",
        identity=str(year),
        relative_path=f"data/raw/bls/hyp0006/schedules/{year}.html",
        source_url=f"https://www.bls.gov/schedule/{year}/home.htm",
        sha256=f"{year:064x}"[-64:],
    )


def test_live_bls_network_access_is_prohibited(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = False

    def should_not_call(*_args: object, **_kwargs: object) -> object:
        nonlocal called
        called = True
        raise AssertionError("urlopen must not be called for BLS")

    monkeypatch.setattr(feasibility.urllib.request, "urlopen", should_not_call)

    with pytest.raises(feasibility.PreparationError, match="live BLS network access is disabled"):
        feasibility.fetch_bytes("https://www.bls.gov/schedule/2003/home.htm")

    assert called is False


def test_snapshot_manifest_requires_exact_2003_2021_contract(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    manifest = tmp_path / "manifest.csv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("year", "source_url", "snapshot_relative_path"))
        for year in range(2003, 2022):
            writer.writerow(
                (
                    year,
                    f"https://www.bls.gov/schedule/{year}/home.htm",
                    f"data/raw/bls/hyp0006/schedules/{year}.html",
                )
            )

    monkeypatch.setattr(feasibility, "BLS_SNAPSHOT_MANIFEST", manifest)
    rows = feasibility.load_bls_snapshot_manifest()

    assert len(rows) == 19
    assert rows[0]["year"] == "2003"
    assert rows[-1]["year"] == "2021"


def test_missing_snapshot_bundle_is_owner_input_not_hypothesis_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    rows = [
        {
            "year": "2003",
            "source_url": "https://www.bls.gov/schedule/2003/home.htm",
            "snapshot_relative_path": "data/raw/bls/hyp0006/schedules/2003.html",
        }
    ]
    monkeypatch.setattr(feasibility, "ROOT", tmp_path)

    with pytest.raises(
        feasibility.OwnerInputRequiredError,
        match="OWNER_INPUT_REQUIRED_BLS_SCHEDULE_SNAPSHOTS",
    ):
        feasibility.load_bls_schedule_snapshots(rows)


def test_legacy_schedule_text_parses_cpi_and_same_time_release() -> None:
    payload = b"""
    <html><body><pre>
    Consumer Price Index, July 2003                 Aug. 15, 2003    8:30 am
    Real Earnings, July 2003                        Aug. 15           8:30 am
    Consumer Price Index, December 2003             Jan. 15, 2004    8:30 am
    Real Earnings, December 2003                    Jan. 15           8:30 am
    </pre></body></html>
    """
    entries = feasibility.schedule_entries(payload, 2003)

    cpi_rows = [
        item
        for item in entries
        if "consumer price index" in str(item["label"]).lower()
    ]
    assert [(item["date"], item["clock"]) for item in cpi_rows] == [
        (date(2003, 8, 15), "08:30"),
        (date(2004, 1, 15), "08:30"),
    ]
    assert feasibility.same_time_schedule_labels(
        entries,
        date(2003, 8, 15),
        "08:30",
    ) == ("Real Earnings, July 2003",)


def test_et_conversion_uses_pre_and_post_2007_dst_rules() -> None:
    assert feasibility.eastern_local_to_utc(
        datetime(2006, 3, 20, 8, 30),
        "ET",
    ) == datetime(2006, 3, 20, 13, 30, tzinfo=UTC)
    assert feasibility.eastern_local_to_utc(
        datetime(2006, 4, 3, 8, 30),
        "ET",
    ) == datetime(2006, 4, 3, 12, 30, tzinfo=UTC)
    assert feasibility.eastern_local_to_utc(
        datetime(2007, 3, 12, 8, 30),
        "ET",
    ) == datetime(2007, 3, 12, 12, 30, tzinfo=UTC)


def test_schedule_candidates_preserve_frozen_development_interval() -> None:
    schedule_by_year = {
        2003: [
            {
                "date": date(2003, 7, 16),
                "clock": "08:30",
                "label": "Consumer Price Index, June 2003",
            },
            {
                "date": date(2003, 8, 15),
                "clock": "08:30",
                "label": "Consumer Price Index, July 2003",
            },
        ],
        2021: [
            {
                "date": date(2021, 8, 11),
                "clock": "08:30",
                "label": "Consumer Price Index for July 2021",
            },
            {
                "date": date(2021, 9, 14),
                "clock": "08:30",
                "label": "Consumer Price Index for August 2021",
            },
        ],
    }
    source_by_year = {
        2003: source_object(2003),
        2021: source_object(2021),
    }

    candidates = feasibility.cpi_schedule_candidates(schedule_by_year, source_by_year)

    assert [item["date"] for item in candidates] == [
        date(2003, 8, 15),
        date(2021, 8, 11),
    ]
    assert candidates[0]["source_snapshot_relative_path"].endswith("2003.html")
    assert candidates[1]["source_snapshot_relative_path"].endswith("2021.html")


def test_bls_calendar_csv_contains_only_event_identity_and_provenance(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    calendar = tmp_path / "calendar.csv"
    monkeypatch.setattr(feasibility, "BLS_CALENDAR_CSV", calendar)

    schedule_by_year = {
        2003: [
            {
                "date": date(2003, 8, 15),
                "clock": "08:30",
                "label": "Consumer Price Index, July 2003",
            },
            {
                "date": date(2003, 8, 15),
                "clock": "08:30",
                "label": "Real Earnings, July 2003",
            },
        ]
    }
    candidates = feasibility.cpi_schedule_candidates(
        schedule_by_year,
        {2003: source_object(2003)},
    )

    digest = feasibility.write_bls_calendar_csv(candidates, schedule_by_year)

    assert len(digest) == 64
    header = calendar.read_text(encoding="utf-8").splitlines()[0].split(",")
    assert tuple(header) == feasibility.BLS_CALENDAR_FIELDS
    lowered = {field.lower() for field in header}
    assert "bid" not in lowered
    assert "ask" not in lowered
    assert "return" not in lowered
    assert "pnl" not in lowered


def test_tick_source_url_uses_zero_based_month_and_hour_bucket() -> None:
    hour = datetime(2021, 8, 11, 12, tzinfo=UTC)
    url = feasibility.tick_source_url(
        "https://datafeed.dukascopy.com/datafeed",
        hour,
    )
    assert url.endswith("/EURUSD/2021/07/11/12h_ticks.bi5")


def test_decode_tick_object_validates_coherent_bid_ask(
    tmp_path: Path,
) -> None:
    raw = b"".join(
        (
            struct.pack(">IIIff", 1000, 120005, 120000, 1.0, 1.0),
            struct.pack(">IIIff", 2000, 120006, 120001, 2.0, 2.0),
        )
    )
    path = tmp_path / "12h_ticks.bi5"
    path.write_bytes(lzma.compress(raw))
    hour = datetime(2021, 8, 11, 12, tzinfo=UTC)

    metadata, times = feasibility.decode_tick_object(path, hour, "TEST")

    assert metadata.record_count == 2
    assert metadata.duplicate_timestamp_count == 0
    assert times == [
        hour + timedelta(seconds=1),
        hour + timedelta(seconds=2),
    ]


def test_decode_tick_object_rejects_crossed_quote(
    tmp_path: Path,
) -> None:
    raw = struct.pack(">IIIff", 1000, 119999, 120000, 1.0, 1.0)
    path = tmp_path / "12h_ticks.bi5"
    path.write_bytes(lzma.compress(raw))

    with pytest.raises(feasibility.PreparationError, match="ASK below BID"):
        feasibility.decode_tick_object(
            path,
            datetime(2021, 8, 11, 12, tzinfo=UTC),
            "TEST",
        )


def test_required_tick_hours_are_bounded_and_exclude_hyp0005() -> None:
    release = datetime(2003, 8, 15, 12, 30, tzinfo=UTC)
    hours = feasibility.required_tick_hours(release)

    assert len(hours) == 5
    assert hours[0] == datetime(2003, 8, 15, 10, tzinfo=UTC)
    assert hours[-1] == datetime(2003, 8, 15, 14, tzinfo=UTC)
    assert not any(feasibility.inside_hyp0005_protected(hour) for hour in hours)


def test_event_geometry_uses_timestamps_only_and_requires_strict_pre_release() -> None:
    release = datetime(2021, 8, 11, 12, 30, tzinfo=UTC)
    times = [
        release - timedelta(minutes=60, milliseconds=500),
        release - timedelta(minutes=60) + timedelta(milliseconds=300),
        release - timedelta(milliseconds=200),
        release,
        release + timedelta(minutes=60, milliseconds=700),
        release + timedelta(minutes=60) - timedelta(milliseconds=400),
    ]

    geometry = feasibility.event_geometry(times, release)

    assert geometry["pre60_prev_gap_ms"] == 500
    assert geometry["pre60_next_gap_ms"] == 300
    assert geometry["pre_release_last_gap_ms"] == 200
    assert geometry["post60_prev_gap_ms"] == 400
    assert geometry["post60_next_gap_ms"] == 700
    assert geometry["quote_geometry_status"] == "COMPLETE_TIMESTAMP_GEOMETRY"


def test_geometry_output_schema_contains_no_price_or_outcome_fields() -> None:
    lowered = {field.lower() for field in feasibility.GEOMETRY_FIELDS}

    assert "bid" not in lowered
    assert "ask" not in lowered
    assert "pre_abs_60m_return" not in lowered
    assert "post_abs_60m_return" not in lowered
    assert "return" not in lowered
    assert "pnl" not in lowered


def test_preparation_decision_is_non_market_geometry_gate() -> None:
    assert (
        feasibility.preparation_decision(
            candidate_event_count=10,
            complete_geometry_count=8,
        )
        == "READY_FOR_DATA_FEASIBILITY_FREEZE"
    )
    assert (
        feasibility.preparation_decision(
            candidate_event_count=10,
            complete_geometry_count=0,
        )
        == "INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY"
    )
