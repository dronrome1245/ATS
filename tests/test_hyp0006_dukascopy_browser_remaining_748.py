from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

import tools.hyp0006_dukascopy_browser_remaining_748 as remaining
from tools import hyp0006_data_feasibility as feasibility
from tools import hyp0006_dukascopy_controlled_download as controlled


def inventory_row(hour_start: datetime, *, exists: bool = False) -> controlled.InventoryRow:
    return controlled.InventoryRow(
        hour_start=feasibility.iso_z(hour_start),
        source_url=feasibility.tick_source_url(remaining.CANONICAL_BASE, hour_start),
        local_path=(
            f"data/raw/dukascopy/hyp0006/EURUSD/{hour_start.year}/"
            f"{hour_start.month:02d}/{hour_start.day:02d}/{hour_start.hour:02d}h_ticks.bi5"
        ),
        exists=exists,
    )


def test_remaining_inventory_selects_exact_748_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start = datetime(2010, 1, 1, tzinfo=UTC)
    rows = [inventory_row(start + timedelta(hours=index), exists=index < 7) for index in range(755)]
    monkeypatch.setattr(
        controlled,
        "build_inventory",
        lambda: (rows, controlled.AUTHORIZED_CALENDAR_SHA256, 217),
    )

    selected, calendar_sha256, event_count = remaining.remaining_inventory()

    assert len(selected) == 748
    assert selected[0].hour_start == rows[7].hour_start
    assert selected[-1].hour_start == rows[-1].hour_start
    assert calendar_sha256 == controlled.AUTHORIZED_CALENDAR_SHA256
    assert event_count == 217


@pytest.mark.parametrize("missing_count", [747, 749])
def test_remaining_inventory_blocks_on_count_drift(
    monkeypatch: pytest.MonkeyPatch,
    missing_count: int,
) -> None:
    start = datetime(2010, 1, 1, tzinfo=UTC)
    rows = [inventory_row(start + timedelta(hours=index)) for index in range(missing_count)]
    monkeypatch.setattr(
        controlled,
        "build_inventory",
        lambda: (rows, controlled.AUTHORIZED_CALENDAR_SHA256, 217),
    )

    with pytest.raises(remaining.BrowserRemainingError, match="inventory drift"):
        remaining.remaining_inventory()


def test_run_remaining_retries_once_then_skips(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    sentinel = tmp_path / "consumed.json"
    monkeypatch.setattr(remaining, "CONSUMED_SENTINEL", sentinel)
    monkeypatch.setattr(remaining, "canonical_authorization_is_active", lambda: True)
    monkeypatch.setattr(feasibility, "git_head", lambda: "abc123")

    start = datetime(2010, 1, 1, tzinfo=UTC)
    rows = [inventory_row(start), inventory_row(start + timedelta(hours=1))]
    monkeypatch.setattr(
        remaining,
        "remaining_inventory",
        lambda: (rows, controlled.AUTHORIZED_CALENDAR_SHA256, 217),
    )
    monkeypatch.setattr(
        remaining.browser,
        "find_new_valid_download",
        lambda **_kwargs: None,
    )

    opened: list[str] = []

    report = remaining.run_remaining(
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
    monkeypatch.setattr(remaining, "CONSUMED_SENTINEL", sentinel)
    monkeypatch.setattr(remaining, "canonical_authorization_is_active", lambda: True)

    def must_not_open(_url: str) -> bool:
        raise AssertionError("consumed batch must block before browser open")

    with pytest.raises(remaining.BrowserRemainingError, match="already been consumed"):
        remaining.run_remaining(
            downloads_dir=downloads,
            wait_seconds=1,
            opener=must_not_open,
        )
