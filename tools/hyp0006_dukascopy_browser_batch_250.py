#!/usr/bin/env python3
"""Bounded 250-object browser-assisted Dukascopy BI5 intake for RF-027.

This tool performs source acquisition/integrity work only. It does not compute
HYP-0006 returns, the primary inequality, or P&L.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from tools import hyp0006_data_feasibility as feasibility
from tools import hyp0006_dukascopy_browser_pilot as browser
from tools import hyp0006_dukascopy_controlled_download as controlled

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-027"
SUBSTAGE = "DUKASCOPY_BROWSER_BATCH_250"
INFORMATION_BOUNDARY = "NO_HYPOTHESIS_OUTCOME_COMPUTED"
SOURCE_IDENTITY = "DUKASCOPY_HOURLY_TICK_BI5"
CANONICAL_BASE = controlled.CANONICAL_BASE

BATCH_OBJECT_COUNT = 250
MAX_ATTEMPTS_PER_OBJECT = 2
DEFAULT_WAIT_SECONDS = 45

STATE_PATH = ROOT / "03_СОСТОЯНИЕ_ПРОЕКТА.yaml"
ACTIVE_AUTHORIZATION_MARKER = (
    'strategy_5_dukascopy_browser_batch_250_status: '
    '"OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05"'
)

REPORT_JSON = ROOT / "reports" / "local_ci" / "HYP0006_DUKASCOPY_BROWSER_BATCH_250.json"
REPORT_TEXT = ROOT / "reports" / "local_ci" / "HYP0006_DUKASCOPY_BROWSER_BATCH_250_REPORT.txt"
BATCH_MANIFEST_CSV = (
    ROOT / "reports" / "local_ci" / "HYP0006_DUKASCOPY_BROWSER_BATCH_250_MANIFEST.csv"
)
CONSUMED_SENTINEL = (
    ROOT / "reports" / "local_ci" / "HYP0006_DUKASCOPY_BROWSER_BATCH_250_CONSUMED.json"
)


class BrowserBatchError(RuntimeError):
    """Raised when the bounded 250-object browser batch cannot proceed."""


@dataclass(frozen=True)
class BatchRow:
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


def batch_inventory() -> tuple[list[controlled.InventoryRow], str, int]:
    inventory, calendar_sha256, event_count = controlled.build_inventory()
    missing = [item for item in inventory if not item.exists]
    selected = missing[:BATCH_OBJECT_COUNT]
    if not selected:
        raise BrowserBatchError("no missing Dukascopy objects remain for the batch")
    return selected, calendar_sha256, event_count


def run_batch(
    *,
    downloads_dir: Path,
    wait_seconds: int,
    opener: Callable[[str], bool] = browser.open_browser_tab,
) -> dict[str, object]:
    if not canonical_authorization_is_active():
        raise BrowserBatchError("bounded browser batch 250 is not active in canonical state")
    if CONSUMED_SENTINEL.exists():
        raise BrowserBatchError("browser batch 250 authorization has already been consumed")
    if not downloads_dir.is_dir():
        raise BrowserBatchError(f"Downloads directory does not exist: {downloads_dir}")

    selected, calendar_sha256, event_count = batch_inventory()

    CONSUMED_SENTINEL.parent.mkdir(parents=True, exist_ok=True)
    CONSUMED_SENTINEL.write_text(
        json.dumps(
            {
                "task_id": TASK_ID,
                "substage": SUBSTAGE,
                "git_commit": feasibility.git_head(),
                "consumed_at": now_utc(),
                "authorized_object_limit": BATCH_OBJECT_COUNT,
                "max_attempts_per_object": MAX_ATTEMPTS_PER_OBJECT,
                "information_boundary": INFORMATION_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    rows: list[BatchRow] = []
    for ordinal, item in enumerate(selected, start=1):
        hour_start = controlled.parse_utc(item.hour_start)
        final_status = "SKIPPED_AFTER_2_ATTEMPTS"
        failure: str | None = None
        sha256: str | None = None
        record_count: int | None = None
        attempts = 0

        for attempt in range(1, MAX_ATTEMPTS_PER_OBJECT + 1):
            attempts = attempt
            before = browser.current_download_snapshot(downloads_dir, hour_start)
            opened = opener(item.source_url)
            if not opened:
                failure = f"browser_open_returned_false_attempt_{attempt}"
                continue

            found = browser.find_new_valid_download(
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
                sha256, record_count = browser.promote_valid_download(downloaded_path, item)
            except (
                browser.BrowserPilotError,
                OSError,
                feasibility.PreparationError,
            ) as exc:
                failure = f"integrity_or_promotion_failure_attempt_{attempt}: {exc}"
                continue

            final_status = "DOWNLOADED_VALIDATED_PROMOTED"
            failure = None
            break

        rows.append(
            BatchRow(
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
        "schema_version": "hyp0006-dukascopy-browser-batch-250-1",
        "task_id": TASK_ID,
        "substage": SUBSTAGE,
        "git_commit": feasibility.git_head(),
        "source_identity": SOURCE_IDENTITY,
        "canonical_base": CANONICAL_BASE,
        "calendar_sha256": calendar_sha256,
        "event_count": event_count,
        "batch_object_limit": BATCH_OBJECT_COUNT,
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
        "HYP-0006 Dukascopy browser batch 250",
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
    selected, _calendar_sha256, _event_count = batch_inventory()
    BATCH_MANIFEST_CSV.parent.mkdir(parents=True, exist_ok=True)
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
    BATCH_MANIFEST_CSV.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Downloads directory: {downloads_dir}")
    print(f"Batch manifest: {BATCH_MANIFEST_CSV}")
    print(f"Objects: {len(selected)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Bounded browser-assisted intake of the first 250 currently missing "
            "frozen RF-027 Dukascopy BI5 objects."
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
        "--owner-authorized-250",
        action="store_true",
        help="Required with --execute-browser for this one bounded 250-object batch.",
    )
    args = parser.parse_args()

    try:
        if not args.execute_browser:
            write_manifest(args.downloads_dir)
            print("DRY_RUN_READY_BROWSER_BATCH_250")
            print(f"Information boundary: {INFORMATION_BOUNDARY}")
            return 0
        if not args.owner_authorized_250:
            raise BrowserBatchError("execute mode requires --owner-authorized-250")
        if args.wait_seconds <= 0:
            raise BrowserBatchError("--wait-seconds must be positive")

        report = run_batch(
            downloads_dir=args.downloads_dir,
            wait_seconds=args.wait_seconds,
        )
        write_reports(report)
        print(REPORT_TEXT.read_text(encoding="utf-8"), end="")
        return 0
    except (BrowserBatchError, OSError, feasibility.PreparationError) as exc:
        print(f"RF-027 browser batch 250 blocked: {exc}")
        return 24


if __name__ == "__main__":
    raise SystemExit(main())
