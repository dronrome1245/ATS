#!/usr/bin/env python3
"""Prepare HYP-0004 EUR/USD development data without computing hypothesis outcomes."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-017"
HYPOTHESIS_ID = "HYP-0004"
PARENT_DATASET_ID = "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001"
PARENT_PATH = ROOT / "data" / "derived" / "HYP-0003-DEV-01-G10EXUSD-H1.csv"
EXPECTED_PARENT_SHA256 = "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2"
EXPECTED_PARENT_SOURCE_BUNDLE_SHA256 = (
    "9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a"
)
DEVELOPMENT_DATASET_ID = "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001"
DEVELOPMENT_DATASET_VERSION = "1.0.0"
DERIVED_PATH = ROOT / "data" / "derived" / "HYP-0004-DEV-01-EURUSD-H1.csv"
REPORT_JSON = ROOT / "reports" / "local_ci" / "HYP0004_DEVELOPMENT_DATA.json"
REPORT_TEXT = ROOT / "reports" / "local_ci" / "HYP0004_DEVELOPMENT_DATA_REPORT.txt"
INFORMATION_BOUNDARY = "NO_HYPOTHESIS_OUTCOME_COMPUTED"

PARENT_REQUIRED_FIELDS = (
    "event_time",
    "availability_time",
    "currency",
    "source_symbol",
    "source_orientation",
    "sequence",
    "bid_open",
    "ask_open",
)
DERIVED_FIELDNAMES = (
    "event_time",
    "availability_time",
    "sequence",
    "parent_sequence",
    "source_symbol",
    "bid_open",
    "ask_open",
    "utc_bucket",
)
BUCKETS = ("CORE_ACTIVE", "TRANSITION", "OFF_HOURS")
VALID_PREPARATION_DECISIONS = {
    "READY_FOR_DEVELOPMENT_DATA_FREEZE",
    "INSUFFICIENT_DEVELOPMENT_DATA",
}


class DevelopmentDataPrepError(RuntimeError):
    """Raised when RF-017 cannot honestly prepare the frozen development data."""


def git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_utc_hour(value: str) -> datetime:
    if not value.endswith("Z"):
        raise DevelopmentDataPrepError(f"timestamp must use UTC Z suffix: {value!r}")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise DevelopmentDataPrepError(f"invalid RFC3339 timestamp: {value!r}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise DevelopmentDataPrepError(f"timestamp is not UTC: {value!r}")
    parsed = parsed.astimezone(UTC)
    if any((parsed.minute, parsed.second, parsed.microsecond)):
        raise DevelopmentDataPrepError(f"timestamp is not an exact hourly boundary: {value!r}")
    return parsed


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def bucket_for_hour(hour: int) -> str:
    if not 0 <= hour <= 23:
        raise ValueError(f"invalid UTC hour: {hour}")
    if 7 <= hour <= 16:
        return "CORE_ACTIVE"
    if 17 <= hour <= 20:
        return "TRANSITION"
    return "OFF_HOURS"


def nth_weekday_of_month(year: int, month: int, weekday: int, occurrence: int) -> int:
    first = datetime(year, month, 1, tzinfo=UTC)
    offset = (weekday - first.weekday()) % 7
    return 1 + offset + 7 * (occurrence - 1)


def us_dst_active_utc(value: datetime) -> bool:
    march_sunday = nth_weekday_of_month(value.year, 3, 6, 2)
    november_sunday = nth_weekday_of_month(value.year, 11, 6, 1)
    start = datetime(value.year, 3, march_sunday, 7, tzinfo=UTC)
    end = datetime(value.year, 11, november_sunday, 6, tzinfo=UTC)
    return start <= value < end


def is_fx_market_hour(value: datetime) -> bool:
    weekday = value.weekday()
    if weekday < 4:
        return True
    boundary_hour = 21 if us_dst_active_utc(value) else 22
    if weekday == 4:
        return value.hour < boundary_hour
    if weekday == 5:
        return False
    return value.hour >= boundary_hour


def _positive_finite(value: str, field: str, line_no: int) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise DevelopmentDataPrepError(
            f"invalid {field} at parent CSV line {line_no}: {value!r}"
        ) from exc
    if not math.isfinite(parsed) or parsed <= 0:
        raise DevelopmentDataPrepError(
            f"non-positive/non-finite {field} at parent CSV line {line_no}: {value!r}"
        )
    return parsed


def load_eurusd_rows(parent_path: Path) -> list[dict[str, Any]]:
    if not parent_path.is_file():
        raise DevelopmentDataPrepError(f"frozen parent dataset is missing: {parent_path}")

    actual_sha256 = sha256_file(parent_path)
    if actual_sha256 != EXPECTED_PARENT_SHA256:
        raise DevelopmentDataPrepError(
            "frozen parent dataset SHA-256 mismatch: "
            f"{actual_sha256} != {EXPECTED_PARENT_SHA256}"
        )

    rows: list[dict[str, Any]] = []
    previous_event: datetime | None = None
    previous_parent_sequence: int | None = None

    with parent_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = tuple(reader.fieldnames or ())
        missing = [field for field in PARENT_REQUIRED_FIELDS if field not in fields]
        if missing:
            raise DevelopmentDataPrepError(
                "parent dataset missing required fields: " + ", ".join(missing)
            )

        for line_no, row in enumerate(reader, start=2):
            if row["currency"] != "EUR":
                continue
            if row["source_symbol"] != "EURUSD" or row["source_orientation"] != "DIRECT":
                raise DevelopmentDataPrepError(
                    f"unexpected EUR source identity at parent CSV line {line_no}"
                )

            event_time = parse_utc_hour(row["event_time"])
            availability_time = parse_utc_hour(row["availability_time"])
            if availability_time != event_time + timedelta(hours=1):
                raise DevelopmentDataPrepError(
                    f"availability_time mismatch at parent CSV line {line_no}"
                )
            if not is_fx_market_hour(event_time):
                raise DevelopmentDataPrepError(
                    f"unexpected closed-market EUR/USD row at {row['event_time']}"
                )

            try:
                parent_sequence = int(row["sequence"])
            except ValueError as exc:
                raise DevelopmentDataPrepError(
                    f"invalid parent sequence at parent CSV line {line_no}"
                ) from exc
            if parent_sequence < 0:
                raise DevelopmentDataPrepError(
                    f"negative parent sequence at parent CSV line {line_no}"
                )
            if previous_parent_sequence is not None and parent_sequence <= previous_parent_sequence:
                raise DevelopmentDataPrepError(
                    f"non-increasing parent sequence at parent CSV line {line_no}"
                )

            bid_open = _positive_finite(row["bid_open"], "bid_open", line_no)
            ask_open = _positive_finite(row["ask_open"], "ask_open", line_no)
            if ask_open < bid_open:
                raise DevelopmentDataPrepError(
                    f"ask_open < bid_open at parent CSV line {line_no}"
                )

            if previous_event is not None:
                if event_time == previous_event:
                    raise DevelopmentDataPrepError(
                        f"duplicate EUR/USD event_time at {row['event_time']}"
                    )
                if event_time < previous_event:
                    raise DevelopmentDataPrepError(
                        f"out-of-order EUR/USD event_time at {row['event_time']}"
                    )

            rows.append(
                {
                    "event_time": event_time,
                    "event_time_text": iso_z(event_time),
                    "availability_time_text": iso_z(availability_time),
                    "parent_sequence": parent_sequence,
                    "source_symbol": "EURUSD",
                    "bid_open_text": row["bid_open"],
                    "ask_open_text": row["ask_open"],
                    "utc_bucket": bucket_for_hour(event_time.hour),
                }
            )
            previous_event = event_time
            previous_parent_sequence = parent_sequence

    if not rows:
        raise DevelopmentDataPrepError("frozen parent dataset contains no EUR/USD rows")
    return rows


def geometry_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    event_times = {row["event_time"] for row in rows}
    if len(event_times) != len(rows):
        raise DevelopmentDataPrepError("duplicate event_time survived EUR/USD validation")

    last_event = rows[-1]["event_time"]
    total_by_bucket = Counter({bucket: 0 for bucket in BUCKETS})
    eligible_by_bucket = Counter({bucket: 0 for bucket in BUCKETS})
    total_by_year: Counter[int] = Counter()
    eligible_by_year: Counter[int] = Counter()

    eligible = 0
    closed_market_next = 0
    missing_expected_next = 0
    dataset_end_next = 0

    for row in rows:
        event_time = row["event_time"]
        bucket = row["utc_bucket"]
        total_by_bucket[bucket] += 1
        total_by_year[event_time.year] += 1

        next_time = event_time + timedelta(hours=1)
        if next_time > last_event:
            dataset_end_next += 1
            continue
        if not is_fx_market_hour(next_time):
            closed_market_next += 1
            continue
        if next_time not in event_times:
            missing_expected_next += 1
            continue

        eligible += 1
        eligible_by_bucket[bucket] += 1
        eligible_by_year[event_time.year] += 1

    return {
        "eligible_exact_next_hour_count": eligible,
        "ineligible_closed_market_next_hour_count": closed_market_next,
        "ineligible_missing_expected_next_hour_count": missing_expected_next,
        "ineligible_dataset_end_count": dataset_end_next,
        "total_rows_by_bucket": dict(sorted(total_by_bucket.items())),
        "eligible_rows_by_bucket": dict(sorted(eligible_by_bucket.items())),
        "total_rows_by_year": {
            str(year): count for year, count in sorted(total_by_year.items())
        },
        "eligible_rows_by_year": {
            str(year): count for year, count in sorted(eligible_by_year.items())
        },
    }


def write_derived_csv(rows: list[dict[str, Any]], destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=DERIVED_FIELDNAMES,
            lineterminator="\n",
        )
        writer.writeheader()
        for sequence, row in enumerate(rows):
            writer.writerow(
                {
                    "event_time": row["event_time_text"],
                    "availability_time": row["availability_time_text"],
                    "sequence": sequence,
                    "parent_sequence": row["parent_sequence"],
                    "source_symbol": row["source_symbol"],
                    "bid_open": row["bid_open_text"],
                    "ask_open": row["ask_open_text"],
                    "utc_bucket": row["utc_bucket"],
                }
            )
    temporary.replace(destination)
    return sha256_file(destination)


def preparation_decision(geometry: dict[str, Any]) -> str:
    eligible_by_bucket = geometry["eligible_rows_by_bucket"]
    if eligible_by_bucket["CORE_ACTIVE"] and eligible_by_bucket["OFF_HOURS"]:
        return "READY_FOR_DEVELOPMENT_DATA_FREEZE"
    return "INSUFFICIENT_DEVELOPMENT_DATA"


def build_result(
    rows: list[dict[str, Any]],
    geometry: dict[str, Any],
    derived_sha256: str,
    commit: str,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "task_id": TASK_ID,
        "hypothesis_id": HYPOTHESIS_ID,
        "git_commit": commit,
        "parent_dataset_id": PARENT_DATASET_ID,
        "parent_dataset_sha256": EXPECTED_PARENT_SHA256,
        "parent_source_bundle_sha256": EXPECTED_PARENT_SOURCE_BUNDLE_SHA256,
        "development_dataset_id": DEVELOPMENT_DATASET_ID,
        "development_dataset_version": DEVELOPMENT_DATASET_VERSION,
        "derived_csv_sha256": derived_sha256,
        "derived_row_count": len(rows),
        "first_event_time": rows[0]["event_time_text"],
        "last_event_time": rows[-1]["event_time_text"],
        "duplicate_event_time_count": 0,
        "out_of_order_event_time_count": 0,
        "malformed_boundary_row_count": 0,
        "boundary_open_crossing_count": 0,
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": INFORMATION_BOUNDARY,
    }
    result.update(geometry)
    result["preparation_decision"] = preparation_decision(geometry)
    return result


def write_reports(result: dict[str, Any]) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "HYP-0004 DEVELOPMENT DATA PREPARATION",
        "====================================",
        f"Task: {result['task_id']}",
        f"Commit: {result['git_commit']}",
        f"Decision: {result['preparation_decision']}",
        f"Parent dataset: {result['parent_dataset_id']}",
        f"Parent SHA-256: {result['parent_dataset_sha256']}",
        f"Derived dataset: {result['development_dataset_id']}",
        f"Derived rows: {result['derived_row_count']}",
        f"Derived SHA-256: {result['derived_csv_sha256']}",
        f"First event: {result['first_event_time']}",
        f"Last event: {result['last_event_time']}",
        f"Exact-next-hour eligible: {result['eligible_exact_next_hour_count']}",
        (
            "Ineligible closed-market next hour: "
            f"{result['ineligible_closed_market_next_hour_count']}"
        ),
        (
            "Ineligible missing expected next hour: "
            f"{result['ineligible_missing_expected_next_hour_count']}"
        ),
        f"Ineligible dataset end: {result['ineligible_dataset_end_count']}",
        f"Eligible by bucket: {json.dumps(result['eligible_rows_by_bucket'], sort_keys=True)}",
        f"Outcome metrics computed: {result['outcome_metrics_computed']}",
        f"Primary claim evaluated: {result['primary_claim_evaluated']}",
        f"Information boundary: {result['information_boundary']}",
    ]
    REPORT_TEXT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    print("ATS HYP-0004 DEVELOPMENT DATA PREPARATION", flush=True)
    try:
        commit = git_head()
        rows = load_eurusd_rows(PARENT_PATH)
        geometry = geometry_summary(rows)
        derived_sha256 = write_derived_csv(rows, DERIVED_PATH)
        result = build_result(rows, geometry, derived_sha256, commit)
        write_reports(result)
    except (OSError, subprocess.CalledProcessError, DevelopmentDataPrepError) as exc:
        print(f"[FAIL] RF-017 preparation: {exc}", flush=True)
        return 1

    print(
        f"[PASS] RF-017 preparation: {result['preparation_decision']}",
        flush=True,
    )
    print(f"Derived rows: {result['derived_row_count']}", flush=True)
    print(f"Derived SHA-256: {result['derived_csv_sha256']}", flush=True)
    print(f"Information boundary: {result['information_boundary']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
