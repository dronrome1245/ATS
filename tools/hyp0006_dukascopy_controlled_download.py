#!/usr/bin/env python3
"""Controlled Dukascopy preload for RF-027 without computing HYP-0006 outcomes."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tools import hyp0006_data_feasibility as feasibility

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-027"
SUBSTAGE = "DUKASCOPY_CONTROLLED_PRELOAD"
INFORMATION_BOUNDARY = "NO_HYPOTHESIS_OUTCOME_COMPUTED"
SOURCE_POLICY = "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF"
CANONICAL_BASE = "https://datafeed.dukascopy.com/datafeed"

AUTHORIZED_CALENDAR_SHA256 = (
    "646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9"
)
AUTHORIZED_EVENT_COUNT = 217
AUTHORIZED_REQUIRED_OBJECT_COUNT = 1085

REPORT_JSON = (\n    ROOT / "reports" / "local_ci" / "HYP0006_DUKASCOPY_CONTROLLED_DOWNLOAD.json"\n)
REPORT_TEXT = (\n    ROOT / "reports" / "local_ci" / "HYP0006_DUKASCOPY_CONTROLLED_DOWNLOAD_REPORT.txt"\n)
INVENTORY_CSV = (
    ROOT / "reports" / "local_ci" / "HYP0006_DUKASCOPY_CONTROLLED_DOWNLOAD_INVENTORY.csv"
)


class ControlledDownloadError(RuntimeError):
    """Raised when the controlled preload contract cannot be executed."""


@dataclass(frozen=True)
class InventoryRow:
    hour_start: str
    source_url: str
    local_path: str
    exists: bool


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ControlledDownloadError(f"release timestamp lacks timezone: {value}")
    return parsed.astimezone(UTC)


def local_tick_path(hour_start: datetime, raw_root: Path) -> Path:
    return (
        raw_root
        / str(hour_start.year)
        / f"{hour_start.month:02d}"
        / f"{hour_start.day:02d}"
        / f"{hour_start.hour:02d}h_ticks.bi5"
    )


def relative_display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def build_inventory(
    calendar_path: Path = feasibility.BLS_CALENDAR_CSV,
    raw_root: Path = feasibility.RAW_DUKASCOPY_ROOT,
    *,
    expected_calendar_sha256: str | None = AUTHORIZED_CALENDAR_SHA256,
    expected_event_count: int | None = AUTHORIZED_EVENT_COUNT,
    expected_object_count: int | None = AUTHORIZED_REQUIRED_OBJECT_COUNT,
) -> tuple[list[InventoryRow], str, int]:
    if not calendar_path.is_file():
        raise ControlledDownloadError(f"missing frozen BLS calendar: {calendar_path}")

    calendar_sha256 = feasibility.sha256_file(calendar_path)
    if expected_calendar_sha256 is not None and calendar_sha256 != expected_calendar_sha256:
        raise ControlledDownloadError(
            "BLS calendar SHA-256 does not match the OWNER-authorized RF-027 inventory"
        )

    with calendar_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != feasibility.BLS_CALENDAR_FIELDS:
            raise ControlledDownloadError("unexpected BLS calendar header")
        rows = [dict(row) for row in reader]

    if expected_event_count is not None and len(rows) != expected_event_count:
        raise ControlledDownloadError(
            f"BLS calendar event count mismatch: {len(rows)} != {expected_event_count}"
        )

    required_hours: set[datetime] = set()
    for row in rows:
        release_time = parse_utc(row["release_time_utc"])
        for hour_start in feasibility.required_tick_hours(release_time):
            if feasibility.inside_hyp0005_protected(hour_start):
                raise ControlledDownloadError(
                    f"inventory enters HYP-0005 protected data: {feasibility.iso_z(hour_start)}"
                )
            required_hours.add(hour_start)

    ordered_hours = sorted(required_hours)
    if expected_object_count is not None and len(ordered_hours) != expected_object_count:
        raise ControlledDownloadError(
            f"required object count mismatch: {len(ordered_hours)} != {expected_object_count}"
        )

    inventory: list[InventoryRow] = []
    for hour_start in ordered_hours:
        local_path = local_tick_path(hour_start, raw_root)
        inventory.append(
            InventoryRow(
                hour_start=feasibility.iso_z(hour_start),
                source_url=feasibility.tick_source_url(CANONICAL_BASE, hour_start),
                local_path=relative_display(local_path),
                exists=local_path.is_file(),
            )
        )
    return inventory, calendar_sha256, len(rows)


def write_inventory_csv(inventory: list[InventoryRow], path: Path = INVENTORY_CSV) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("hour_start", "source_url", "local_path", "status"),
            lineterminator="\n",
        )
        writer.writeheader()
        for item in inventory:
            writer.writerow(
                {
                    "hour_start": item.hour_start,
                    "source_url": item.source_url,
                    "local_path": item.local_path,
                    "status": "EXISTS" if item.exists else "MISSING",
                }
            )
    temporary.replace(path)


def resolve_local_path(item: InventoryRow, raw_root: Path) -> Path:
    hour_start = parse_utc(item.hour_start)
    return local_tick_path(hour_start, raw_root)


def controlled_download(
    inventory: list[InventoryRow],
    raw_root: Path = feasibility.RAW_DUKASCOPY_ROOT,
) -> dict[str, Any]:
    downloaded_count = 0
    semantic_missing_count = 0
    network_requests = 0
    failed_hour: str | None = None
    failed_url: str | None = None
    failure: str | None = None
    status = "COMPLETE"

    for item in inventory:
        destination = resolve_local_path(item, raw_root)
        if destination.is_file():
            continue

        network_requests += 1
        hour_start = parse_utc(item.hour_start)
        try:
            body, _headers = feasibility.fetch_bytes(item.source_url)
        except FileNotFoundError:
            semantic_missing_count += 1
            continue
        except feasibility.PreparationError as exc:
            status = "SOURCE_BLOCKED"
            failed_hour = item.hour_start
            failed_url = item.source_url
            failure = f"{SOURCE_POLICY}: {exc}"
            break

        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(destination.suffix + ".part")
        try:
            temporary.write_bytes(body)
            feasibility.decode_tick_object(temporary, hour_start, item.source_url)
            temporary.replace(destination)
        except (OSError, feasibility.PreparationError) as exc:
            temporary.unlink(missing_ok=True)
            status = "SOURCE_OR_LOCAL_INTEGRITY_BLOCKED"
            failed_hour = item.hour_start
            failed_url = item.source_url
            failure = str(exc)
            break
        downloaded_count += 1

    return {
        "status": status,
        "network_requests": network_requests,
        "downloaded_count": downloaded_count,
        "semantic_missing_count": semantic_missing_count,
        "failed_hour": failed_hour,
        "failed_url": failed_url,
        "failure": failure,
    }


def write_reports(report: dict[str, Any]) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(\n        json.dumps(report, indent=2, sort_keys=True) + "\n",\n        encoding="utf-8",\n    )

    lines = [
        "HYP-0006 Dukascopy controlled preload",
        f"Task: {report['task_id']}",
        f"Substage: {report['substage']}",
        f"Status: {report['status']}",
        f"Calendar SHA-256: {report['calendar_sha256']}",
        f"CPI events: {report['event_count']}",
        f"Required unique objects: {report['required_object_count']}",
        f"Existing before run: {report['existing_before']}",
        f"Missing before run: {report['missing_before']}",
        f"Existing after run: {report.get('existing_after', '')}",
        f"Missing after run: {report.get('missing_after', '')}",
        f"Network requests: {report['network_requests']}",
        f"Downloaded: {report['downloaded_count']}",
        f"Semantic missing objects: {report['semantic_missing_count']}",
        f"Failed hour: {report['failed_hour'] or ''}",
        f"Failed URL: {report['failed_url'] or ''}",
        f"Failure: {report['failure'] or ''}",
        "Hypothesis outcome computed: NO",
        f"Information boundary: {INFORMATION_BOUNDARY}",
    ]
    REPORT_TEXT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(*, execute: bool, owner_authorized: bool) -> tuple[int, dict[str, Any]]:
    inventory, calendar_sha256, event_count = build_inventory()
    write_inventory_csv(inventory)

    existing_before = sum(item.exists for item in inventory)
    missing_before = len(inventory) - existing_before
    result: dict[str, Any] = {
        "schema_version": "hyp0006-dukascopy-controlled-preload-1",
        "task_id": TASK_ID,
        "substage": SUBSTAGE,
        "git_commit": feasibility.git_head(),
        "source_policy": SOURCE_POLICY,
        "canonical_base": CANONICAL_BASE,
        "calendar_sha256": calendar_sha256,
        "event_count": event_count,
        "required_object_count": len(inventory),
        "existing_before": existing_before,
        "missing_before": missing_before,
        "network_requests": 0,
        "downloaded_count": 0,
        "semantic_missing_count": 0,
        "failed_hour": None,
        "failed_url": None,
        "failure": None,
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": INFORMATION_BOUNDARY,
    }

    if not execute:
        result["status"] = "DRY_RUN_READY"
        result["existing_after"] = existing_before
        result["missing_after"] = missing_before
        write_reports(result)
        return 0, result

    if not owner_authorized:
        result["status"] = "OWNER_AUTHORIZATION_REQUIRED"
        result["failure"] = "execute mode requires --owner-authorized"
        result["existing_after"] = existing_before
        result["missing_after"] = missing_before
        write_reports(result)
        return 23, result

    result.update(controlled_download(inventory))
    existing_after = sum(
        resolve_local_path(item, feasibility.RAW_DUKASCOPY_ROOT).is_file() for item in inventory
    )
    result["existing_after"] = existing_after
    result["missing_after"] = len(inventory) - existing_after
    write_reports(result)
    return (0 if result["status"] == "COMPLETE" else 24), result


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory or preload the OWNER-authorized RF-027 Dukascopy BI5 objects. "
            "Default mode is offline inventory only."
        )
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Perform canonical Dukascopy downloads instead of offline inventory only.",
    )
    parser.add_argument(
        "--owner-authorized",
        action="store_true",
        help="Required together with --execute after explicit OWNER authorization.",
    )
    args = parser.parse_args()

    try:
        return_code, report = run(
            execute=args.execute,
            owner_authorized=args.owner_authorized,
        )
    except ControlledDownloadError as exc:
        print(f"RF-027 controlled preload blocked: {exc}", file=sys.stderr)
        return 22

    print(f"RF-027 controlled preload status: {report['status']}")
    print(f"Network requests: {report['network_requests']}")
    print(f"Downloaded: {report['downloaded_count']}")
    print(f"Information boundary: {INFORMATION_BOUNDARY}")
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
