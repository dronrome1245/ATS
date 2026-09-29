from __future__ import annotations

import lzma
import struct
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

import tools.hyp0006_data_feasibility as feasibility


def test_parse_archive_index_extracts_release_dates() -> None:
    payload = b"""
    <html><body>
    <a href="/news.release/archives/cpi_08152003.htm">July 2003 CPI</a>
    <a href="/news.release/archives/cpi_08112021.htm">July 2021 CPI</a>
    <a href="/news.release/archives/cpi_09142021.pdf">PDF</a>
    </body></html>
    """
    records = feasibility.parse_archive_index(payload)

    assert records == [
        (
            date(2003, 8, 15),
            "https://www.bls.gov/news.release/archives/cpi_08152003.htm",
        ),
        (
            date(2021, 8, 11),
            "https://www.bls.gov/news.release/archives/cpi_08112021.htm",
        ),
    ]


def test_bls_request_headers_identify_research_owner() -> None:
    headers = feasibility.request_headers(feasibility.BLS_ARCHIVE_INDEX_URL)

    assert headers["User-Agent"] == (
        "ATS-Research/1.0 (+https://github.com/dronrome1245/ATS)"
    )
    assert headers["Referer"] == "https://www.bls.gov/"
    assert headers["Accept-Language"] == "en-US,en;q=0.9"


def test_bls_403_fails_fast_without_retry(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    calls = 0

    def denied(*_args: object, **_kwargs: object) -> object:
        nonlocal calls
        calls += 1
        raise feasibility.urllib.error.HTTPError(
            feasibility.BLS_ARCHIVE_INDEX_URL,
            403,
            "Forbidden",
            hdrs=None,
            fp=None,
        )

    monkeypatch.setattr(feasibility.urllib.request, "urlopen", denied)
    monkeypatch.setattr(feasibility.time, "sleep", lambda _delay: None)

    with pytest.raises(feasibility.SourceAccessDeniedError, match="BLS HTTP 403"):
        feasibility.cached_or_fetch_any(
            (feasibility.BLS_ARCHIVE_INDEX_URL,),
            tmp_path / "index.htm",
            "BLS CPI archive index",
            missing_ok=False,
        )

    assert calls == 1


def test_parse_archive_release_time_handles_historical_edt() -> None:
    payload = b"""
    <html><body>
    Transmission of material in this release is embargoed until
    8:30 A.M. (EDT), Friday, August 15, 2003
    </body></html>
    """
    parsed = feasibility.parse_archive_release_time(payload, date(2003, 8, 15))

    assert parsed is not None
    utc_time, zone, local_text = parsed
    assert utc_time == datetime(2003, 8, 15, 12, 30, tzinfo=UTC)
    assert zone == "EDT"
    assert local_text == "2003-08-15 08:30"


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


def test_schedule_entries_and_same_time_flags() -> None:
    payload = b"""
    <table>
      <tr><td>Aug. 15</td><td>8:30 am</td><td>Consumer Price Index, July 2003</td></tr>
      <tr><td>Aug. 15</td><td>8:30 am</td><td>Real Earnings, July 2003</td></tr>
      <tr><td>Aug. 19</td><td>10:00 am</td><td>State Employment</td></tr>
    </table>
    """
    entries = feasibility.schedule_entries(payload, 2003)
    status, labels = feasibility.schedule_crosscheck(
        entries,
        date(2003, 8, 15),
        "2003-08-15 08:30",
    )

    assert status == "MATCH"
    assert labels == ("Real Earnings, July 2003",)


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
            unresolved_event_time_count=0,
            schedule_mismatch_count=0,
            complete_geometry_count=8,
        )
        == "READY_FOR_DATA_FEASIBILITY_FREEZE"
    )
    assert (
        feasibility.preparation_decision(
            candidate_event_count=10,
            unresolved_event_time_count=1,
            schedule_mismatch_count=0,
            complete_geometry_count=8,
        )
        == "UNRESOLVED_OFFICIAL_EVENT_TIMES"
    )
