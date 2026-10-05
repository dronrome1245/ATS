#!/usr/bin/env python3
"""Bounded browser-assisted Dukascopy BI5 intake pilot for RF-027.

This tool does not compute HYP-0006 returns, the primary inequality, or P&L.
It opens canonical Dukascopy URLs in the local default browser one at a time,
waits for a valid BI5 file to appear in the chosen Downloads directory, retries
each object at most once, validates raw BI5 integrity, and promotes only valid
bytes into the canonical frozen local raw path.
"""

from __future__ import annotations

import argparse
import json
import shutil
import time
import webbrowser
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from tools import hyp0006_data_feasibility as feasibility
from tools import hyp0006_dukascopy_controlled_download as controlled

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-027"
SUBSTAGE = "DUKASCOPY_BROWSER_PILOT_50"
INFORMATION_BOUNDARY = "NO_HYPOTHESIS_OUTCOME_COMPUTED"
SOURCE_IDENTITY = "DUKASCOPY_HOURLY_TICK_BI5"
CANONICAL_BASE = controlled.CANONICAL_BASE

PILOT_OBJECT_COUNT = 50
MAX_ATTEMPTS_PER_OBJECT = 2
DEFAULT_WAIT_SECONDS = 45
POLL_SECONDS = 0.5

STATE_PATH = ROOT / "03_СОСТОЯНИЕ_ПРОЕКТА.yaml"
ACTIVE_AUTHORIZATION_MARKER = (
    'strategy_5_dukascopy_browser_pilot_status: "OWNER_AUTHORIZED_BROWSER_PILOT_50_2026_10_05"'
)

REPORT_JSON = ROOT / "reports" / "local_ci" / "HYP0006_DUKASCOPY_BROWSER_PILOT_50.json"
REPORT_TEXT = ROOT / "reports" / "local_ci" / "HYP0006_DUKASCOPY_BROWSER_PILOT_50_REPORT.txt"
PILOT_MANIFEST_CSV = (
    ROOT / "reports" / "local_ci" / "HYP0006_DUKASCOPY_BROWSER_PILOT_50_MANIFEST.csv"
)
CONSUMED_SENTINEL = (
    ROOT / "reports" / "local_ci" / "HYP0006_DUKASCOPY_BROWSER_PILOT_50_CONSUMED.json"
)


class BrowserPilotError(RuntimeError):
    """Raised when the bounded browser pilot contract cannot proceed."""


@dataclass(frozen=True)
class PilotRow:
    ordinal: int
    hour_start: str
    source_url: str
    canonical_local_path: str
    status: str
    attempts: int
    sha256: str | None
    record_count: int | None
    failure: str | None


def now_utc() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def canonical_authorization_is_active(state_path: Path = STATE_PATH) -> bool:
    if not state_path.is_file():
        return False
    return ACTIVE_AUTHORIZATION_MARKER in state_path.read_text(encoding="utf-8")


def pilot_inventory() -> tuple[list[controlled.InventoryRow], str, int]:
    inventory, calendar_sha256, event_count = controlled.build_inventory()
    missing = [item for item in inventory if not item.exists]
    selected = missing[:PILOT_OBJECT_COUNT]
    if not selected:
        raise BrowserPilotError("no missing Dukascopy objects remain for the pilot")
    return selected, calendar_sha256, event_count


def candidate_prefix(hour_start: datetime) -> str:
    return f"{hour_start.hour:02d}h_ticks"


def current_download_snapshot(
    downloads_dir: Path,
    hour_start: datetime,
) -> dict[Path, tuple[int, int]]:
    prefix = candidate_prefix(hour_start)
    snapshot: dict[Path, tuple[int, int]] = {}
    for path in downloads_dir.glob(f"{prefix}*.bi5"):
        try:
            stat = path.stat()
        except OSError:
            continue
        if path.is_file():
            snapshot[path] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def find_new_valid_download(
    *,
    downloads_dir: Path,
    item: controlled.InventoryRow,
    before: dict[Path, tuple[int, int]],
    wait_seconds: int,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> tuple[Path, feasibility.TickObject] | None:
    hour_start = controlled.parse_utc(item.hour_start)
    deadline = time.monotonic() + wait_seconds
    seen_sizes: dict[Path, tuple[int, int]] = {}

    while time.monotonic() < deadline:
        current = current_download_snapshot(downloads_dir, hour_start)
        candidates = [
            path
            for path, fingerprint in current.items()
            if path not in before or before[path] != fingerprint
        ]
        for path in sorted(candidates, key=lambda p: current[p][1]):
            size = current[path][0]
            previous_size, stable_polls = seen_sizes.get(path, (-1, 0))
            stable_polls = stable_polls + 1 if size == previous_size and size > 0 else 0
            seen_sizes[path] = (size, stable_polls)
            if stable_polls < 1:
                continue
            try:
                metadata, _times = feasibility.decode_tick_object(
                    path,
                    hour_start,
                    item.source_url,
                )
            except (OSError, feasibility.PreparationError):
                continue
            return path, metadata
        sleep_fn(POLL_SECONDS)
    return None


def promote_valid_download(
    downloaded_path: Path,
    item: controlled.InventoryRow,
) -> tuple[str, int]:
    hour_start = controlled.parse_utc(item.hour_start)
    destination = controlled.local_tick_path(hour_start, feasibility.RAW_DUKASCOPY_ROOT)
    if destination.exists():
        raise BrowserPilotError(f"refusing to overwrite existing object: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".browser-pilot.part")
    source_sha256 = feasibility.sha256_file(downloaded_path)
    try:
        shutil.copyfile(downloaded_path, temporary)
        metadata, _times = feasibility.decode_tick_object(
            temporary,
            hour_start,
            item.source_url,
        )
        if metadata.sha256 != source_sha256:
            raise BrowserPilotError("byte-preservation SHA-256 mismatch during promotion")
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)

    downloaded_path.unlink(missing_ok=True)
    return source_sha256, metadata.record_count


def open_browser_tab(url: str) -> bool:
    return bool(webbrowser.open_new_tab(url))


def run_pilot(
    *,
    downloads_dir: Path,
    wait_seconds: int,
    opener: Callable[[str], bool] = open_browser_tab,
) -> dict[str, object]:
    if not canonical_authorization_is_active():
        raise BrowserPilotError("bounded browser pilot is not active in canonical state")
    if CONSUMED_SENTINEL.exists():
        raise BrowserPilotError("browser pilot authorization has already been consumed")
    if not downloads_dir.is_dir():
        raise BrowserPilotError(f"Downloads directory does not exist: {downloads_dir}")

    selected, calendar_sha256, event_count = pilot_inventory()

    CONSUMED_SENTINEL.parent.mkdir(parents=True, exist_ok=True)
    CONSUMED_SENTINEL.write_text(
        json.dumps(
            {
                "task_id": TASK_ID,
                "substage": SUBSTAGE,
                "git_commit": feasibility.git_head(),
                "consumed_at": now_utc(),
                "authorized_object_limit": PILOT_OBJECT_COUNT,
                "max_attempts_per_object": MAX_ATTEMPTS_PER_OBJECT,
                "information_boundary": INFORMATION_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    rows: list[PilotRow] = []
    for ordinal, item in enumerate(selected, start=1):
        hour_start = controlled.parse_utc(item.hour_start)
        final_status = "SKIPPED_AFTER_2_ATTEMPTS"
        failure: str | None = None
        sha256: str | None = None
        record_count: int | None = None
        attempts = 0

        for attempt in range(1, MAX_ATTEMPTS_PER_OBJECT + 1):
            attempts = attempt
            before = current_download_snapshot(downloads_dir, hour_start)
            opened = opener(item.source_url)
            if not opened:
                failure = f"browser_open_returned_false_attempt_{attempt}"
                continue

            found = find_new_valid_download(
                downloads_dir=downloads_dir,
                item=item,
                before=before,
                wait_seconds=wait_seconds,
            )
            if found is None:
                failure = f"no_valid_bi5_download_within_{wait_seconds}s_attempt_{attempt}"
                continue

            downloaded_path, _metadata = found
            try:
                sha256, record_count = promote_valid_download(downloaded_path, item)
            except (BrowserPilotError, OSError, feasibility.PreparationError) as exc:
                failure = f"integrity_or_promotion_failure_attempt_{attempt}: {exc}"
                continue

            final_status = "DOWNLOADED_VALIDATED_PROMOTED"
            failure = None
            break

        rows.append(
            PilotRow(
                ordinal=ordinal,
                hour_start=item.hour_start,
                source_url=item.source_url,
                canonical_local_path=item.local_path,
                status=final_status,
                attempts=attempts,
                sha256=sha256,
                record_count=record_count,
                failure=failure,
            )
        )

    successful = sum(row.status == "DOWNLOADED_VALIDATED_PROMOTED" for row in rows)
    skipped = len(rows) - successful
    return {
        "schema_version": "hyp0006-dukascopy-browser-pilot-50-1",
        "task_id": TASK_ID,
        "substage": SUBSTAGE,
        "git_commit": feasibility.git_head(),
        "source_identity": SOURCE_IDENTITY,
        "canonical_base": CANONICAL_BASE,
        "calendar_sha256": calendar_sha256,
        "event_count": event_count,
        "pilot_object_limit": PILOT_OBJECT_COUNT,
        "max_attempts_per_object": MAX_ATTEMPTS_PER_OBJECT,
        "objects_selected": len(rows),
        "objects_promoted": successful,
        "objects_skipped_after_two_attempts": skipped,
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": INFORMATION_BOUNDARY,
        "rows": [asdict(row) for row in rows],
    }


def write_reports(report: dict[str, object]) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "HYP-0006 Dukascopy browser pilot 50",
        f"Task: {report['task_id']}",
        f"Substage: {report['substage']}",
        f"Git commit: {report['git_commit']}",
        f"Objects selected: {report['objects_selected']}",
        f"Objects promoted: {report['objects_promoted']}",
        (
            "Objects skipped after two attempts: "
            f"{report['objects_skipped_after_two_attempts']}"
        ),
        f"Max attempts/object: {report['max_attempts_per_object']}",
        "Hypothesis outcome computed: NO",
        f"Information boundary: {report['information_boundary']}",
    ]
    REPORT_TEXT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(downloads_dir: Path) -> None:
    selected, _calendar_sha256, _event_count = pilot_inventory()
    PILOT_MANIFEST_CSV.parent.mkdir(parents=True, exist_ok=True)
    lines = ["ordinal,hour_start,source_url,canonical_local_path"]
    for ordinal, item in enumerate(selected, start=1):
        lines.append(
            ",".join(
                (
                    str(ordinal),
                    item.hour_start,
                    item.source_url,
                    item.local_path,
                )
            )
        )
    PILOT_MANIFEST_CSV.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Downloads directory: {downloads_dir}")
    print(f"Pilot manifest: {PILOT_MANIFEST_CSV}")
    print(f"Objects: {len(selected)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Bounded browser-assisted intake of the first 50 missing frozen RF-027 "
            "Dukascopy BI5 objects."
        )
    )
    parser.add_argument(
        "--downloads-dir",
        type=Path,
        default=Path.home() / "Downloads",
        help="Browser download directory to monitor.",
    )
    parser.add_argument(
        "--wait-seconds",
        type=int,
        default=DEFAULT_WAIT_SECONDS,
        help="Maximum wait for a valid BI5 download after each browser-open attempt.",
    )
    parser.add_argument(
        "--execute-browser",
        action="store_true",
        help="Open canonical Dukascopy URLs in the local default browser.",
    )
    parser.add_argument(
        "--owner-authorized-50",
        action="store_true",
        help="Required with --execute-browser for the bounded 50-object OWNER-authorized pilot.",
    )
    args = parser.parse_args()

    try:
        if not args.execute_browser:
            write_manifest(args.downloads_dir)
            print("DRY_RUN_READY_BROWSER_PILOT_50")
            print(f"Information boundary: {INFORMATION_BOUNDARY}")
            return 0
        if not args.owner_authorized_50:
            raise BrowserPilotError("execute mode requires --owner-authorized-50")
        if args.wait_seconds <= 0:
            raise BrowserPilotError("--wait-seconds must be positive")

        report = run_pilot(
            downloads_dir=args.downloads_dir,
            wait_seconds=args.wait_seconds,
        )
        write_reports(report)
        print(REPORT_TEXT.read_text(encoding="utf-8"), end="")
        return 0
    except (BrowserPilotError, OSError, feasibility.PreparationError) as exc:
        print(f"RF-027 browser pilot blocked: {exc}")
        return 24


if __name__ == "__main__":
    raise SystemExit(main())
