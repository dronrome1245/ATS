from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

import tools.hyp0006_dukascopy_browser_batch_250 as batch
from tools import hyp0006_data_feasibility as feasibility
from tools import hyp0006_dukascopy_controlled_download as controlled


def inventory_row(hour_start: datetime, *, exists: bool = False) -> controlled.InventoryRow:
    return controlled.InventoryRow(
        hour_start=feasibility.iso_z(hour_start),
        source_url=feasibility.tick_source_url(batch.CANONICAL_BASE, hour_start),
        local_path=(
            f"data/raw/dukascopy/hyp0006/EURUSD/{hour_start.year}/"
            f"{hour_start.month:02d}/{hour_start.day:02d}/{hour_start.hour:02d}h_ticks.bi5"
        ),
        exists=exists,
    )


def test_batch_inventory_selects_first_250_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start = datetime(2010, 1, 1, tzinfo=UTC)
    rows = [
        inventory_row(start + timedelta(hours=index), exists=index < 7)
        for index in range(270)
    ]
    monkeypatch.setattr(
        controlled,
        "build_inventory",
        lambda: (rows, controlled.AUTHORIZED_CALENDAR_SHA256, 217),
    )

    selected, calendar_sha256, event_count = batch.batch_inventory()

    assert len(selected) == 250
    assert selected[0].hour_start == rows[7].hour_start
    assert selected[-1].hour_start == rows[256].hour_start
    assert calendar_sha256 == controlled.AUTHORIZED_CALENDAR_SHA256
    assert event_count == 217


def test_run_batch_retries_once_then_skips(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    sentinel = tmp_path / "consumed.json"
    monkeypatch.setattr(batch, "CONSUMED_SENTINEL", sentinel)
    monkeypatch.setattr(batch, "canonical_authorization_is_active", lambda: True)
    monkeypatch.setattr(feasibility, "git_head", lambda: "abc123")

    start = datetime(2010, 1, 1, tzinfo=UTC)
    rows = [inventory_row(start), inventory_row(start + timedelta(hours=1))]
    monkeypatch.setattr(
        batch,
        "batch_inventory",
        lambda: (rows, controlled.AUTHORIZED_CALENDAR_SHA256, 217),
    )
    monkeypatch.setattr(
        batch.browser,
        "find_new_valid_download",
        lambda **_kwargs: None,
    )

    opened: list[str] = []

    report = batch.run_batch(
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
    monkeypatch.setattr(batch, "CONSUMED_SENTINEL", sentinel)
    monkeypatch.setattr(batch, "canonical_authorization_is_active", lambda: True)

    def must_not_open(_url: str) -> bool:
        raise AssertionError("consumed batch must block before browser open")

    with pytest.raises(batch.BrowserBatchError, match="already been consumed"):
        batch.run_batch(
            downloads_dir=downloads,
            wait_seconds=1,
            opener=must_not_open,
        )
