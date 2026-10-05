from __future__ import annotations

import hashlib
import lzma
import struct
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

import tools.hyp0006_dukascopy_browser_pilot as pilot
from tools import hyp0006_data_feasibility as feasibility
from tools import hyp0006_dukascopy_controlled_download as controlled


def inventory_row(hour_start: datetime, *, exists: bool = False) -> controlled.InventoryRow:
    return controlled.InventoryRow(
        hour_start=feasibility.iso_z(hour_start),
        source_url=feasibility.tick_source_url(pilot.CANONICAL_BASE, hour_start),
        local_path=(
            f"data/raw/dukascopy/hyp0006/EURUSD/{hour_start.year}/"
            f"{hour_start.month:02d}/{hour_start.day:02d}/{hour_start.hour:02d}h_ticks.bi5"
        ),
        exists=exists,
    )


def valid_bi5_bytes() -> bytes:
    record = struct.pack(">IIIff", 1_000, 110_010, 110_000, 1.0, 2.0)
    return lzma.compress(record)


def test_pilot_inventory_selects_first_50_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start = datetime(2010, 1, 1, tzinfo=UTC)
    rows = [inventory_row(start + timedelta(hours=index), exists=index < 3) for index in range(60)]
    monkeypatch.setattr(
        controlled,
        "build_inventory",
        lambda: (rows, controlled.AUTHORIZED_CALENDAR_SHA256, 217),
    )

    selected, calendar_sha256, event_count = pilot.pilot_inventory()

    assert len(selected) == 50
    assert selected[0].hour_start == rows[3].hour_start
    assert selected[-1].hour_start == rows[52].hour_start
    assert calendar_sha256 == controlled.AUTHORIZED_CALENDAR_SHA256
    assert event_count == 217


def test_run_pilot_retries_once_then_skips(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    sentinel = tmp_path / "consumed.json"
    monkeypatch.setattr(pilot, "CONSUMED_SENTINEL", sentinel)
    monkeypatch.setattr(pilot, "canonical_authorization_is_active", lambda: True)
    monkeypatch.setattr(feasibility, "git_head", lambda: "abc123")

    start = datetime(2010, 1, 1, tzinfo=UTC)
    rows = [inventory_row(start), inventory_row(start + timedelta(hours=1))]
    monkeypatch.setattr(
        pilot,
        "pilot_inventory",
        lambda: (rows, controlled.AUTHORIZED_CALENDAR_SHA256, 217),
    )
    monkeypatch.setattr(
        pilot,
        "find_new_valid_download",
        lambda **_kwargs: None,
    )

    opened: list[str] = []

    report = pilot.run_pilot(
        downloads_dir=downloads,
        wait_seconds=1,
        opener=lambda url: opened.append(url) or True,
    )

    assert len(opened) == 4
    assert report["objects_selected"] == 2
    assert report["objects_promoted"] == 0
    assert report["objects_skipped_after_two_attempts"] == 2
    assert all(row["attempts"] == 2 for row in report["rows"])
    assert all(row["status"] == "SKIPPED_AFTER_2_ATTEMPTS" for row in report["rows"])
    assert sentinel.is_file()


def test_consumed_sentinel_blocks_before_browser(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    sentinel = tmp_path / "consumed.json"
    sentinel.write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(pilot, "CONSUMED_SENTINEL", sentinel)
    monkeypatch.setattr(pilot, "canonical_authorization_is_active", lambda: True)

    def must_not_open(_url: str) -> bool:
        raise AssertionError("consumed pilot must block before browser open")

    with pytest.raises(pilot.BrowserPilotError, match="already been consumed"):
        pilot.run_pilot(
            downloads_dir=downloads,
            wait_seconds=1,
            opener=must_not_open,
        )


def test_promote_valid_download_preserves_bytes_and_validates(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    raw_root = tmp_path / "raw"
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    monkeypatch.setattr(feasibility, "RAW_DUKASCOPY_ROOT", raw_root)

    hour = datetime(2010, 1, 15, 13, tzinfo=UTC)
    item = inventory_row(hour)
    downloaded = downloads / "13h_ticks.bi5"
    payload = valid_bi5_bytes()
    downloaded.write_bytes(payload)

    sha256, record_count = pilot.promote_valid_download(downloaded, item)

    destination = controlled.local_tick_path(hour, raw_root)
    assert destination.read_bytes() == payload
    assert sha256 == hashlib.sha256(payload).hexdigest()
    assert record_count == 1
    assert downloaded.exists() is False
