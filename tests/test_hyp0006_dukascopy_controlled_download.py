from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path

import pytest

import tools.hyp0006_data_feasibility as feasibility
import tools.hyp0006_dukascopy_controlled_download as downloader


def write_calendar(path: Path, release_time: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=feasibility.BLS_CALENDAR_FIELDS,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerow(
            {
                "event_id": "BLS-CPI-TEST",
                "release_date_local": "2010-01-15",
                "release_time_local": "08:30",
                "release_time_utc": release_time,
                "timezone_semantics": "BLS_ANNUAL_SCHEDULE_US_EASTERN",
                "schedule_label": "Consumer Price Index",
                "same_time_bls_labels": "",
                "source_year": "2010",
                "source_url": "https://www.bls.gov/schedule/2010/home.htm",
                "source_snapshot_relative_path": "data/raw/bls/hyp0006/schedules/2010.html",
                "source_snapshot_sha256": "0" * 64,
            }
        )


def test_inventory_uses_frozen_required_hours_and_canonical_base(tmp_path: Path) -> None:
    calendar = tmp_path / "calendar.csv"
    raw_root = tmp_path / "raw"
    write_calendar(calendar, "2010-01-15T13:30:00Z")

    inventory, _sha256, event_count = downloader.build_inventory(
        calendar,
        raw_root,
        expected_calendar_sha256=None,
        expected_event_count=1,
        expected_object_count=5,
    )

    assert event_count == 1
    assert [item.hour_start for item in inventory] == [
        "2010-01-15T11:00:00Z",
        "2010-01-15T12:00:00Z",
        "2010-01-15T13:00:00Z",
        "2010-01-15T14:00:00Z",
        "2010-01-15T15:00:00Z",
    ]
    assert all(
        item.source_url.startswith(downloader.CANONICAL_BASE + "/EURUSD/")
        for item in inventory
    )


def test_controlled_download_stops_after_first_external_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    hours = (
        datetime(2010, 1, 15, 13, tzinfo=UTC),
        datetime(2010, 1, 15, 14, tzinfo=UTC),
    )
    inventory = [
        downloader.InventoryRow(
            hour_start=feasibility.iso_z(hour),
            source_url=feasibility.tick_source_url(downloader.CANONICAL_BASE, hour),
            local_path=str(downloader.local_tick_path(hour, tmp_path)),
            exists=False,
        )
        for hour in hours
    ]
    calls: list[str] = []

    def fail_first(url: str, timeout: int = 45) -> tuple[bytes, dict[str, str]]:
        del timeout
        calls.append(url)
        raise feasibility.PreparationError(f"HTTP 503 while fetching {url}")

    monkeypatch.setattr(feasibility, "fetch_bytes", fail_first)

    result = downloader.controlled_download(inventory, tmp_path)

    assert result["status"] == "SOURCE_BLOCKED"
    assert result["network_requests"] == 1
    assert result["downloaded_count"] == 0
    assert result["failed_hour"] == "2010-01-15T13:00:00Z"
    assert calls == [inventory[0].source_url]


def test_controlled_download_does_not_overwrite_existing_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    hour = datetime(2010, 1, 15, 13, tzinfo=UTC)
    destination = downloader.local_tick_path(hour, tmp_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(b"already-present")

    inventory = [
        downloader.InventoryRow(
            hour_start=feasibility.iso_z(hour),
            source_url=feasibility.tick_source_url(downloader.CANONICAL_BASE, hour),
            local_path=str(destination),
            exists=True,
        )
    ]

    def must_not_fetch(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("existing object must never trigger a network request")

    monkeypatch.setattr(feasibility, "fetch_bytes", must_not_fetch)

    result = downloader.controlled_download(inventory, tmp_path)

    assert result["status"] == "COMPLETE"
    assert result["network_requests"] == 0
    assert result["downloaded_count"] == 0
    assert destination.read_bytes() == b"already-present"


def test_execute_requires_explicit_owner_authorization(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    inventory = [
        downloader.InventoryRow(
            hour_start="2010-01-15T13:00:00Z",
            source_url=(\n                "https://datafeed.dukascopy.com/datafeed/EURUSD/2010/00/15/13h_ticks.bi5"\n            ),
            local_path="data/raw/example.bi5",
            exists=False,
        )
    ]

    monkeypatch.setattr(
        downloader,
        "build_inventory",
        lambda: (inventory, downloader.AUTHORIZED_CALENDAR_SHA256, 217),
    )
    monkeypatch.setattr(downloader, "write_inventory_csv", lambda _inventory: None)
    monkeypatch.setattr(downloader, "write_reports", lambda _report: None)

    return_code, report = downloader.run(execute=True, owner_authorized=False)

    assert return_code == 23
    assert report["status"] == "OWNER_AUTHORIZATION_REQUIRED"
    assert report["network_requests"] == 0


def test_dry_run_never_starts_controlled_download(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    inventory = [
        downloader.InventoryRow(
            hour_start="2010-01-15T13:00:00Z",
            source_url="https://datafeed.dukascopy.com/datafeed/EURUSD/2010/00/15/13h_ticks.bi5",
            local_path="data/raw/example.bi5",
            exists=False,
        )
    ]

    monkeypatch.setattr(
        downloader,
        "build_inventory",
        lambda: (inventory, downloader.AUTHORIZED_CALENDAR_SHA256, 217),
    )
    monkeypatch.setattr(downloader, "write_inventory_csv", lambda _inventory: None)
    monkeypatch.setattr(downloader, "write_reports", lambda _report: None)

    def must_not_download(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("dry-run must not execute downloads")

    monkeypatch.setattr(downloader, "controlled_download", must_not_download)

    return_code, report = downloader.run(execute=False, owner_authorized=False)

    assert return_code == 0
    assert report["status"] == "DRY_RUN_READY"
    assert report["network_requests"] == 0
