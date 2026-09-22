#!/usr/bin/env python3
"""Prepare HYP-0002 development thresholds and unseen confirmatory data."""

from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from proto01_eurusd import DERIVED_PATH as DEVELOPMENT_PATH
from proto01_eurusd import (
    ProtoDataError,
    bundle_hash,
    decode_month,
    download_month,
    is_fx_market_hour,
    iso_z,
    load_manifest,
    next_month,
    parse_time,
    raw_path,
    read_rows,
    sha256_file,
    valid_window,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIRM_START = datetime(2026, 1, 1, tzinfo=UTC)
CONFIRM_END = datetime(2026, 9, 1, tzinfo=UTC)
CONFIRM_PATH = ROOT / "data/derived/HYP-0002-CONFIRM-01-EURUSD-H1.csv"
REPORT_JSON = ROOT / "reports/local_ci/HYP0002_DATA_FEASIBILITY.json"
REPORT_TEXT = ROOT / "reports/local_ci/HYP0002_DATA_FEASIBILITY_REPORT.txt"
EXPECTED_DEVELOPMENT_SHA256 = (
    "aeda05d90994259a22e25d882398218aead968941fe0b1c73eb34894841291c0"
)


class FeasibilityPrepError(RuntimeError):
    """Raised when HYP-0002 data-feasibility preparation cannot be frozen."""


def git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def linear_quantile(values: list[float], quantile: float) -> float:
    if not values:
        raise FeasibilityPrepError("cannot calculate quantile from an empty sample")
    if not 0.0 <= quantile <= 1.0:
        raise FeasibilityPrepError("quantile must be between 0 and 1")
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def development_thresholds() -> tuple[int, float, float]:
    manifest = load_manifest()
    expected = manifest.get("integrity", {}).get("digest")
    actual = sha256_file(DEVELOPMENT_PATH)
    if expected != EXPECTED_DEVELOPMENT_SHA256 or actual != EXPECTED_DEVELOPMENT_SHA256:
        raise FeasibilityPrepError("development dataset SHA-256 does not match canonical identity")

    rows = read_rows()
    returns: list[float] = []
    for index in range(24, len(rows) - 25):
        if not valid_window(rows, index):
            continue
        current_mid = (rows[index]["bid_close"] + rows[index]["ask_close"]) / 2.0
        prior_mid = (rows[index - 24]["bid_close"] + rows[index - 24]["ask_close"]) / 2.0
        returns.append(current_mid / prior_mid - 1.0)

    if not returns:
        raise FeasibilityPrepError("no eligible development threshold observations")
    return len(returns), linear_quantile(returns, 0.10), linear_quantile(returns, 0.90)


def confirm_months() -> list[datetime]:
    values: list[datetime] = []
    current = CONFIRM_START
    while current < CONFIRM_END:
        values.append(current)
        current = next_month(current)
    return values


def build_confirmatory_rows() -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    bid: dict[datetime, tuple[float, float, float, float]] = {}
    ask: dict[datetime, tuple[float, float, float, float]] = {}
    source_files: list[dict[str, str]] = []

    for month in confirm_months():
        for side, target in (("BID", bid), ("ASK", ask)):
            path, headers = download_month(month, side)
            decoded = decode_month(path, month)
            duplicates = set(target).intersection(decoded)
            if duplicates:
                raise FeasibilityPrepError(
                    f"duplicate timestamp across source files: {min(duplicates)}"
                )
            target.update(decoded)
            source_files.append(
                {
                    "month": month.strftime("%Y-%m"),
                    "side": side,
                    "sha256": sha256_file(path),
                    "relative_path": str(raw_path(month, side).relative_to(ROOT)).replace(
                        "\\", "/"
                    ),
                    "source_url": headers["source_url"],
                    "last_modified": headers["last_modified"],
                    "etag": headers["etag"],
                }
            )

    bid_times = {
        value
        for value in bid
        if CONFIRM_START <= value < CONFIRM_END and is_fx_market_hour(value)
    }
    ask_times = {
        value
        for value in ask
        if CONFIRM_START <= value < CONFIRM_END and is_fx_market_hour(value)
    }
    if bid_times != ask_times:
        raise FeasibilityPrepError(
            "confirmatory BID/ASK timestamps do not match exactly; "
            f"missing ASK={len(bid_times - ask_times)}, "
            f"missing BID={len(ask_times - bid_times)}"
        )

    timestamps = sorted(bid_times)
    if not timestamps:
        raise FeasibilityPrepError("no aligned confirmatory bars")

    rows: list[dict[str, Any]] = []
    for sequence, timestamp in enumerate(timestamps):
        bid_open, bid_high, bid_low, bid_close = bid[timestamp]
        ask_open, ask_high, ask_low, ask_close = ask[timestamp]
        if ask_open < bid_open:
            raise FeasibilityPrepError(f"ASK open below BID open at {timestamp}")
        rows.append(
            {
                "event_time": iso_z(timestamp),
                "availability_time": iso_z(timestamp + timedelta(hours=1)),
                "sequence": sequence,
                "bid_open": bid_open,
                "bid_high": bid_high,
                "bid_low": bid_low,
                "bid_close": bid_close,
                "ask_open": ask_open,
                "ask_high": ask_high,
                "ask_low": ask_low,
                "ask_close": ask_close,
            }
        )
    return rows, source_files


def write_confirmatory_csv(rows: list[dict[str, Any]]) -> None:
    CONFIRM_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIRM_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            formatted = dict(row)
            for key in (
                "bid_open",
                "bid_high",
                "bid_low",
                "bid_close",
                "ask_open",
                "ask_high",
                "ask_low",
                "ask_close",
            ):
                formatted[key] = f"{row[key]:.5f}"
            writer.writerow(formatted)


def confirmatory_stats(rows: list[dict[str, Any]]) -> dict[str, Any]:
    timestamps = [parse_time(str(row["event_time"])) for row in rows]
    gaps = [
        int((current - previous).total_seconds() // 3600)
        for previous, current in zip(timestamps, timestamps[1:])
        if current - previous != timedelta(hours=1)
    ]
    eligible = sum(valid_window(rows, index) for index in range(24, len(rows) - 25))
    calendar_hours = int((CONFIRM_END - CONFIRM_START).total_seconds() // 3600)
    expected_market_hours = sum(
        is_fx_market_hour(CONFIRM_START + timedelta(hours=offset))
        for offset in range(calendar_hours)
    )
    return {
        "aligned_rows": len(rows),
        "coverage_start": iso_z(timestamps[0]),
        "coverage_end": iso_z(timestamps[-1]),
        "gap_count": len(gaps),
        "max_gap_hours": max(gaps, default=1),
        "eligible_24_before_24_after": eligible,
        "expected_market_hours": expected_market_hours,
        "missing_market_hours": expected_market_hours - len(rows),
    }


def write_reports(
    threshold_count: int,
    q10_dev: float,
    q90_dev: float,
    rows: list[dict[str, Any]],
    source_files: list[dict[str, str]],
) -> None:
    stats = confirmatory_stats(rows)
    payload = {
        "schema_version": "hyp0002-data-feasibility-prep-1",
        "hypothesis_id": "HYP-0002",
        "git_commit": git_head(),
        "development": {
            "dataset_id": "DATA-DUKASCOPY-EURUSDH1-PROTO01-001",
            "dataset_version": "1.0.0",
            "dataset_sha256": sha256_file(DEVELOPMENT_PATH),
            "eligible_threshold_observations": threshold_count,
            "q10_dev": q10_dev,
            "q90_dev": q90_dev,
        },
        "confirmatory": {
            "period_start": iso_z(CONFIRM_START),
            "period_end_exclusive": iso_z(CONFIRM_END),
            **stats,
            "prepared_csv_sha256": sha256_file(CONFIRM_PATH),
            "source_bundle_sha256": bundle_hash(source_files),
            "source_file_count": len(source_files),
            "source_files": source_files,
        },
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "ATS HYP-0002 DATA FEASIBILITY PREPARATION",
        "=========================================",
        f"Git commit: {payload['git_commit']}",
        "Hypothesis: HYP-0002",
        f"Development SHA256: {payload['development']['dataset_sha256']}",
        f"Threshold observations: {threshold_count}",
        f"Q10_DEV: {q10_dev:.12f}",
        f"Q90_DEV: {q90_dev:.12f}",
        "Confirmatory period: 2026-01-01T00:00:00Z to 2026-09-01T00:00:00Z",
        f"Confirmatory aligned rows: {stats['aligned_rows']}",
        f"Confirmatory coverage first: {stats['coverage_start']}",
        f"Confirmatory coverage last: {stats['coverage_end']}",
        f"Missing tradable hours: {stats['missing_market_hours']}",
        f"Detected gaps: {stats['gap_count']}",
        f"Maximum gap hours: {stats['max_gap_hours']}",
        f"Eligible 24-before/24-after: {stats['eligible_24_before_24_after']}",
        f"Confirmatory CSV SHA256: {payload['confirmatory']['prepared_csv_sha256']}",
        f"Confirmatory source bundle SHA256: {payload['confirmatory']['source_bundle_sha256']}",
        f"Confirmatory source files: {len(source_files)}",
        "Information boundary: NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "",
        "NEXT STEP",
        "---------",
        "Send CURRENT_TASK_REPORT.txt to ChatGPT.",
        "Do not run a HYP-0002 outcome calculation before the Data Feasibility review is committed.",
    ]
    REPORT_TEXT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def prepare() -> int:
    threshold_count, q10_dev, q90_dev = development_thresholds()
    rows, source_files = build_confirmatory_rows()
    write_confirmatory_csv(rows)
    write_reports(threshold_count, q10_dev, q90_dev, rows, source_files)
    return 0


def main() -> int:
    try:
        return prepare()
    except (FeasibilityPrepError, ProtoDataError, OSError, ValueError) as exc:
        print(f"HYP-0002 DATA FEASIBILITY PREP BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
