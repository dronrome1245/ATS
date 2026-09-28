#!/usr/bin/env python3
"""Prepare HYP-0005 confirmatory data feasibility without computing the hypothesis outcome."""

from __future__ import annotations

import csv
import importlib
import json
import math
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
try:
    source = importlib.import_module("tools.hyp0003_development_data")
except ModuleNotFoundError as exc:
    if exc.name != "tools":
        raise
    source = importlib.import_module("hyp0003_development_data")

TASK_ID = "ATS2-RF-023"
HYPOTHESIS_ID = "HYP-0005"
DATASET_ID = "DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001"
DATASET_VERSION = "1.0.0"
SOURCE_SYMBOL = "EURUSD"
SOURCE_ORIENTATION = "DIRECT"

LEFT_START = datetime(2003, 5, 4, 21, tzinfo=UTC)
LEFT_END = datetime(2003, 8, 3, 21, tzinfo=UTC)
RIGHT_START = datetime(2026, 9, 1, 0, tzinfo=UTC)
RIGHT_END = datetime(2026, 9, 26, 0, tzinfo=UTC)

SEGMENTS = (
    ("LEFT_UNSEEN", LEFT_START, LEFT_END),
    ("RIGHT_UNSEEN", RIGHT_START, RIGHT_END),
)
CONSUMED_START = LEFT_END
CONSUMED_END = RIGHT_START

DERIVED_PATH = ROOT / "data/derived/HYP-0005-CONF-01-EURUSD-H1.csv"
REPORT_JSON = ROOT / "reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP.json"
REPORT_TEXT = ROOT / "reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP_REPORT.txt"

DOWNLOAD_BATCH_BACKOFF_SECONDS = (5.0, 15.0, 30.0)
BUCKETS = ("CORE_ACTIVE", "TRANSITION", "OFF_HOURS")
FIELDNAMES = (
    "event_time",
    "availability_time",
    "source_bar_completion_time",
    "sequence",
    "confirmatory_segment",
    "source_symbol",
    "bid_open",
    "ask_open",
    "utc_bucket",
)


class ConfirmatoryDataPrepError(RuntimeError):
    """Raised when RF-023 cannot honestly prepare the HYP-0005 data boundary."""


def git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def bucket_for_hour(hour: int) -> str:
    if 7 <= hour <= 16:
        return "CORE_ACTIVE"
    if 17 <= hour <= 20:
        return "TRANSITION"
    return "OFF_HOURS"


def source_months() -> list[datetime]:
    months: list[datetime] = []
    seen: set[tuple[int, int]] = set()
    for _, start, end in SEGMENTS:
        current = datetime(start.year, start.month, 1, tzinfo=UTC)
        while current < end:
            key = (current.year, current.month)
            if key not in seen:
                seen.add(key)
                months.append(current)
            current = source.next_month(current)
    return months


def segment_for_time(value: datetime) -> str | None:
    for name, start, end in SEGMENTS:
        if start <= value < end:
            return name
    return None


def assert_frozen_boundaries() -> None:
    if LEFT_END != CONSUMED_START or RIGHT_START != CONSUMED_END:
        raise ConfirmatoryDataPrepError("unseen/consumed boundary mismatch")
    if not LEFT_END <= RIGHT_START:
        raise ConfirmatoryDataPrepError("confirmatory segments overlap consumed history")
    for name, start, end in SEGMENTS:
        if start >= end:
            raise ConfirmatoryDataPrepError(f"invalid segment interval: {name}")
        if start < CONSUMED_END and end > CONSUMED_START:
            if not (end <= CONSUMED_START or start >= CONSUMED_END):
                raise ConfirmatoryDataPrepError(f"segment overlaps consumed interval: {name}")


def _download_pair_from_format(
    month: datetime,
    source_format: str,
) -> dict[str, tuple[Path, dict[str, str]]] | None:
    if source_format == source.SOURCE_FORMAT_JETTA_JSON:
        downloader = source.download_jetta_source_once
    elif source_format == source.SOURCE_FORMAT_BI5:
        downloader = source.download_legacy_source_once
    else:
        raise ConfirmatoryDataPrepError(f"unknown source format: {source_format}")

    result: dict[str, tuple[Path, dict[str, str]]] = {}
    missing: list[str] = []
    for side in ("BID", "ASK"):
        downloaded = downloader(SOURCE_SYMBOL, month, side)
        if downloaded is None:
            missing.append(side)
        else:
            result[side] = downloaded

    if not missing:
        return result
    if len(missing) == 2:
        return None
    raise ConfirmatoryDataPrepError(
        f"one-sided {source_format} source absence for {month:%Y-%m}: missing {missing[0]}"
    )


def download_source_pair_once(
    month: datetime,
) -> dict[str, tuple[Path, dict[str, str]]]:
    errors: list[str] = []
    for source_format in (
        source.SOURCE_FORMAT_JETTA_JSON,
        source.SOURCE_FORMAT_BI5,
    ):
        try:
            pair = _download_pair_from_format(month, source_format)
        except source.DevelopmentDataPrepError as exc:
            errors.append(f"{source_format}: {exc}")
            continue
        if pair is not None:
            return pair

    if errors:
        raise ConfirmatoryDataPrepError(
            f"coherent source pair unavailable for {month:%Y-%m}: " + " | ".join(errors)
        )
    raise ConfirmatoryDataPrepError(f"source pair absent for {month:%Y-%m}")


def download_source_pair_resilient(
    month: datetime,
) -> dict[str, tuple[Path, dict[str, str]]]:
    attempts = len(DOWNLOAD_BATCH_BACKOFF_SECONDS) + 1
    last_error: Exception | None = None
    for batch in range(attempts):
        try:
            return download_source_pair_once(month)
        except (ConfirmatoryDataPrepError, source.DevelopmentDataPrepError) as exc:
            last_error = exc
            if batch == attempts - 1:
                break
            delay = DOWNLOAD_BATCH_BACKOFF_SECONDS[batch]
            print(
                f"[network] EURUSD {month:%Y-%m} coherent BID/ASK pair failed; "
                f"retrying in {delay:.0f}s",
                flush=True,
            )
            time.sleep(delay)
    raise ConfirmatoryDataPrepError(
        f"cannot acquire EURUSD {month:%Y-%m} after {attempts} batches: {last_error}"
    )


def _validate_open_pair(
    timestamp: datetime,
    bid_open: float,
    ask_open: float,
) -> None:
    if not all(math.isfinite(value) and value > 0 for value in (bid_open, ask_open)):
        raise ConfirmatoryDataPrepError(f"invalid open quote at {timestamp.isoformat()}")
    if ask_open < bid_open:
        raise ConfirmatoryDataPrepError(f"ASK open below BID open at {timestamp.isoformat()}")


def acquire_rows() -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    assert_frozen_boundaries()
    rows: list[dict[str, Any]] = []
    source_files: list[dict[str, str]] = []

    for month in source_months():
        downloaded_pair = download_source_pair_resilient(month)
        formats = {headers["source_format"] for _, headers in downloaded_pair.values()}
        if len(formats) != 1:
            raise ConfirmatoryDataPrepError(
                f"mixed source formats for EURUSD {month:%Y-%m}: {sorted(formats)}"
            )
        source_format = next(iter(formats))
        decoded: dict[str, dict[datetime, tuple[float, float, float, float]]] = {}
        for side in ("BID", "ASK"):
            path, headers = downloaded_pair[side]
            decoded[side] = source.decode_source_object(
                path,
                month,
                SOURCE_SYMBOL,
                source_format,
            )
            source_files.append(
                {
                    "symbol": SOURCE_SYMBOL,
                    "month": month.strftime("%Y-%m"),
                    "side": side,
                    "source_format": source_format,
                    "sha256": source.sha256_file(path),
                    "relative_path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "source_url": headers.get("source_url", ""),
                    "last_modified": headers.get("last_modified", ""),
                    "etag": headers.get("etag", ""),
                }
            )

        bid_times = {
            timestamp for timestamp in decoded["BID"] if segment_for_time(timestamp) is not None
        }
        ask_times = {
            timestamp for timestamp in decoded["ASK"] if segment_for_time(timestamp) is not None
        }
        if bid_times != ask_times:
            raise ConfirmatoryDataPrepError(
                f"BID/ASK timestamp mismatch in frozen segments for {month:%Y-%m}: "
                f"missing ASK={len(bid_times - ask_times)}, "
                f"missing BID={len(ask_times - bid_times)}"
            )

        for timestamp in sorted(bid_times):
            segment = segment_for_time(timestamp)
            if segment is None:
                continue
            if not source.is_fx_market_hour(timestamp):
                raise ConfirmatoryDataPrepError(
                    f"closed-market source row inside frozen segment: {timestamp.isoformat()}"
                )
            bid_open = decoded["BID"][timestamp][0]
            ask_open = decoded["ASK"][timestamp][0]
            _validate_open_pair(timestamp, bid_open, ask_open)
            rows.append(
                {
                    "event_time": timestamp,
                    "event_time_text": iso_z(timestamp),
                    "availability_time_text": iso_z(timestamp),
                    "source_bar_completion_time_text": iso_z(timestamp + timedelta(hours=1)),
                    "confirmatory_segment": segment,
                    "source_symbol": SOURCE_SYMBOL,
                    "bid_open": bid_open,
                    "ask_open": ask_open,
                    "utc_bucket": bucket_for_hour(timestamp.hour),
                }
            )

    rows.sort(key=lambda item: item["event_time"])
    if not rows:
        raise ConfirmatoryDataPrepError("no confirmatory rows acquired")
    event_keys = {(row["confirmatory_segment"], row["event_time"]) for row in rows}
    if len(event_keys) != len(rows):
        raise ConfirmatoryDataPrepError("duplicate confirmatory event_time")
    return rows, source_files


def expected_market_count(start: datetime, end: datetime) -> int:
    count = 0
    current = start
    while current < end:
        if source.is_fx_market_hour(current):
            count += 1
        current += timedelta(hours=1)
    return count


def geometry_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    event_times = {(str(row["confirmatory_segment"]), row["event_time"]) for row in rows}
    total_by_bucket = Counter({bucket: 0 for bucket in BUCKETS})
    eligible_by_bucket = Counter({bucket: 0 for bucket in BUCKETS})
    total_by_segment = Counter({name: 0 for name, _, _ in SEGMENTS})
    eligible_by_segment = Counter({name: 0 for name, _, _ in SEGMENTS})
    expected_by_segment: dict[str, int] = {}
    eligible = 0
    closed_next = 0
    missing_next = 0
    segment_end_next = 0

    bounds = {name: (start, end) for name, start, end in SEGMENTS}
    for name, start, end in SEGMENTS:
        expected_by_segment[name] = expected_market_count(start, end)

    for row in rows:
        segment = str(row["confirmatory_segment"])
        event_time = row["event_time"]
        bucket = str(row["utc_bucket"])
        total_by_bucket[bucket] += 1
        total_by_segment[segment] += 1

        _, segment_end = bounds[segment]
        next_time = event_time + timedelta(hours=1)
        if next_time >= segment_end:
            segment_end_next += 1
            continue
        if not source.is_fx_market_hour(next_time):
            closed_next += 1
            continue
        if (segment, next_time) not in event_times:
            missing_next += 1
            continue

        eligible += 1
        eligible_by_bucket[bucket] += 1
        eligible_by_segment[segment] += 1

    missing_market_by_segment = {
        name: expected_by_segment[name] - total_by_segment[name] for name, _, _ in SEGMENTS
    }
    if any(value < 0 for value in missing_market_by_segment.values()):
        raise ConfirmatoryDataPrepError("source rows exceed frozen expected market-hour geometry")

    return {
        "eligible_exact_next_hour_count": eligible,
        "ineligible_closed_market_next_hour_count": closed_next,
        "ineligible_missing_expected_next_hour_count": missing_next,
        "ineligible_segment_end_count": segment_end_next,
        "total_rows_by_bucket": dict(sorted(total_by_bucket.items())),
        "eligible_rows_by_bucket": dict(sorted(eligible_by_bucket.items())),
        "total_rows_by_segment": dict(sorted(total_by_segment.items())),
        "eligible_rows_by_segment": dict(sorted(eligible_by_segment.items())),
        "expected_market_hours_by_segment": dict(sorted(expected_by_segment.items())),
        "missing_market_hours_by_segment": dict(sorted(missing_market_by_segment.items())),
    }


def write_derived_csv(rows: list[dict[str, Any]], destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        for sequence, row in enumerate(rows):
            writer.writerow(
                {
                    "event_time": row["event_time_text"],
                    "availability_time": row["availability_time_text"],
                    "source_bar_completion_time": row["source_bar_completion_time_text"],
                    "sequence": sequence,
                    "confirmatory_segment": row["confirmatory_segment"],
                    "source_symbol": row["source_symbol"],
                    "bid_open": f"{float(row['bid_open']):.5f}",
                    "ask_open": f"{float(row['ask_open']):.5f}",
                    "utc_bucket": row["utc_bucket"],
                }
            )
    temporary.replace(destination)
    return source.sha256_file(destination)


def preparation_decision(geometry: dict[str, Any]) -> str:
    eligible_by_bucket = geometry["eligible_rows_by_bucket"]
    eligible_by_segment = geometry["eligible_rows_by_segment"]
    if (
        eligible_by_bucket["CORE_ACTIVE"] > 0
        and eligible_by_bucket["OFF_HOURS"] > 0
        and all(eligible_by_segment[name] > 0 for name, _, _ in SEGMENTS)
    ):
        return "READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE"
    return "INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY"


def build_result(
    rows: list[dict[str, Any]],
    source_files: list[dict[str, str]],
    geometry: dict[str, Any],
    derived_sha256: str,
    commit: str,
) -> dict[str, Any]:
    return {
        "schema_version": "hyp0005-data-feasibility-prep-1",
        "task_id": TASK_ID,
        "hypothesis_id": HYPOTHESIS_ID,
        "git_commit": commit,
        "confirmatory_dataset_id": DATASET_ID,
        "confirmatory_dataset_version": DATASET_VERSION,
        "source_provider": "DUKASCOPY",
        "source_symbol": SOURCE_SYMBOL,
        "source_orientation": SOURCE_ORIENTATION,
        "source_month_count": len(source_months()),
        "source_object_count": len(source_files),
        "source_bundle_sha256": source.source_bundle_hash(source_files),
        "source_files": source_files,
        "derived_csv_relative_path": str(DERIVED_PATH.relative_to(ROOT)).replace("\\", "/"),
        "derived_csv_sha256": derived_sha256,
        "derived_row_count": len(rows),
        "segments": [
            {
                "segment_id": name,
                "start": iso_z(start),
                "end_exclusive": iso_z(end),
            }
            for name, start, end in SEGMENTS
        ],
        "consumed_project_interval_start": iso_z(CONSUMED_START),
        "consumed_project_interval_end_exclusive": iso_z(CONSUMED_END),
        "boundary_availability_mode": "H1_OPEN_PROXY_AT_EVENT_TIME",
        "exact_tick_boundary_time_known": False,
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_CONFIRMATORY_OUTCOME_COMPUTED",
        "geometry": geometry,
        "preparation_decision": preparation_decision(geometry),
    }


def write_reports(result: dict[str, Any]) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    geometry = result["geometry"]
    lines = [
        "HYP-0005 CONFIRMATORY DATA FEASIBILITY PREPARATION",
        "=================================================",
        f"Task: {result['task_id']}",
        f"Commit: {result['git_commit']}",
        f"Decision: {result['preparation_decision']}",
        f"Dataset: {result['confirmatory_dataset_id']}@{result['confirmatory_dataset_version']}",
        f"Source months: {result['source_month_count']}",
        f"Source objects: {result['source_object_count']}",
        f"Source bundle SHA-256: {result['source_bundle_sha256']}",
        f"Derived rows: {result['derived_row_count']}",
        f"Derived CSV SHA-256: {result['derived_csv_sha256']}",
        f"Eligible exact-next-hour: {geometry['eligible_exact_next_hour_count']}",
        f"Eligible by bucket: {json.dumps(geometry['eligible_rows_by_bucket'], sort_keys=True)}",
        f"Eligible by segment: {json.dumps(geometry['eligible_rows_by_segment'], sort_keys=True)}",
        (
            "Missing market hours by segment: "
            f"{json.dumps(geometry['missing_market_hours_by_segment'], sort_keys=True)}"
        ),
        f"Boundary availability mode: {result['boundary_availability_mode']}",
        f"Exact tick boundary time known: {result['exact_tick_boundary_time_known']}",
        f"Outcome metrics computed: {result['outcome_metrics_computed']}",
        f"Primary claim evaluated: {result['primary_claim_evaluated']}",
        f"Information boundary: {result['information_boundary']}",
        "",
        "NEXT STEP",
        "---------",
        "Send CURRENT_TASK_REPORT.txt and HYP0005_DATA_FEASIBILITY_PREP.json to ChatGPT.",
        "Do not calculate HYP-0005 spread/return medians or primary inequalities yet.",
    ]
    REPORT_TEXT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)


def main() -> int:
    print("ATS HYP-0005 CONFIRMATORY DATA FEASIBILITY PREPARATION", flush=True)
    try:
        commit = git_head()
        rows, source_files = acquire_rows()
        geometry = geometry_summary(rows)
        derived_sha256 = write_derived_csv(rows, DERIVED_PATH)
        result = build_result(rows, source_files, geometry, derived_sha256, commit)
        write_reports(result)
    except (
        ConfirmatoryDataPrepError,
        source.DevelopmentDataPrepError,
        OSError,
        subprocess.CalledProcessError,
        ValueError,
    ) as exc:
        print(f"[FAIL] RF-023 preparation: {exc}", flush=True)
        return 1

    print(
        f"[PASS] RF-023 preparation: {result['preparation_decision']}",
        flush=True,
    )
    print(f"Derived rows: {result['derived_row_count']}", flush=True)
    print(f"Derived SHA-256: {result['derived_csv_sha256']}", flush=True)
    print(f"Information boundary: {result['information_boundary']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
