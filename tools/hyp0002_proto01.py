#!/usr/bin/env python3
"""Run frozen HYP-0002 PROTO-01 on the confirmatory EUR/USD H1 dataset."""

from __future__ import annotations

import csv
import json
import statistics
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from proto01_eurusd import parse_time, sha256_file

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/derived/HYP-0002-CONFIRM-01-EURUSD-H1.csv"
MANIFEST_PATH = ROOT / "data/manifests/DATA-DUKASCOPY-EURUSDH1-HYP0002-001.yaml"
RESULT_PATH = ROOT / "reports/local_ci/HYP0002_PROTO01_RESULT.json"
RESULT_REPORT_PATH = ROOT / "reports/local_ci/HYP0002_PROTO01_RESULT_REPORT.txt"
EXPECTED_DATASET_ID = "DATA-DUKASCOPY-EURUSDH1-HYP0002-001"
EXPECTED_DATASET_VERSION = "1.0.0"
EXPECTED_DATASET_SHA256 = "d62a7103478da2a79a0992310005bcd0afc8dc0010088dccd2ed0e54e2ec112f"
Q10_DEV = -0.005141454111
Q90_DEV = 0.005394148971
HORIZON_HOURS = 24


class Proto02Error(RuntimeError):
    """Raised when the frozen HYP-0002 PROTO-01 contract cannot be executed."""


def git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def load_manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open(encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle)
    if not isinstance(manifest, dict):
        raise Proto02Error("confirmatory Dataset Manifest is not a mapping")
    if manifest.get("dataset_id") != EXPECTED_DATASET_ID:
        raise Proto02Error("confirmatory Dataset ID mismatch")
    if manifest.get("dataset_version") != EXPECTED_DATASET_VERSION:
        raise Proto02Error("confirmatory Dataset version mismatch")
    digest = manifest.get("integrity", {}).get("digest")
    if digest != EXPECTED_DATASET_SHA256:
        raise Proto02Error("confirmatory manifest SHA-256 mismatch")
    if sha256_file(DATA_PATH) != EXPECTED_DATASET_SHA256:
        raise Proto02Error("confirmatory prepared CSV SHA-256 mismatch")
    return manifest


def read_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            parsed: dict[str, Any] = {
                "event_time": parse_time(row["event_time"]),
                "availability_time": parse_time(row["availability_time"]),
                "sequence": int(row["sequence"]),
            }
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
                parsed[key] = float(row[key])
            rows.append(parsed)
    return rows


def valid_window(rows: list[dict[str, Any]], index: int) -> bool:
    window = rows[index - HORIZON_HOURS : index + HORIZON_HOURS + 2]
    return len(window) == 50 and all(
        current["event_time"] - previous["event_time"] == timedelta(hours=1)
        for previous, current in zip(window, window[1:])
    )


def prior_return(rows: list[dict[str, Any]], index: int) -> float:
    current_mid = (rows[index]["bid_close"] + rows[index]["ask_close"]) / 2.0
    prior = rows[index - HORIZON_HOURS]
    prior_mid = (prior["bid_close"] + prior["ask_close"]) / 2.0
    return current_mid / prior_mid - 1.0


def up_signed_return(entry: dict[str, Any], exit_bar: dict[str, Any]) -> float:
    return exit_bar["bid_open"] / entry["ask_open"] - 1.0


def down_signed_return(entry: dict[str, Any], exit_bar: dict[str, Any]) -> float:
    return entry["bid_open"] / exit_bar["ask_open"] - 1.0


def overlap_share(indices: list[int]) -> tuple[int, float]:
    overlaps = 0
    previous_exit: int | None = None
    for index in indices:
        entry = index + 1
        exit_index = entry + HORIZON_HOURS
        if previous_exit is not None and entry <= previous_exit:
            overlaps += 1
        previous_exit = max(previous_exit or exit_index, exit_index)
    return overlaps, overlaps / len(indices) if indices else 0.0


def side_metrics(
    values: list[float],
    baseline: list[float],
    indices: list[int],
) -> dict[str, int | float]:
    if not values:
        return {
            "event_count": 0,
            "mean_signed_return": 0.0,
            "median_signed_return": 0.0,
            "positive_share": 0.0,
            "unconditional_mean_return": statistics.fmean(baseline),
            "mean_minus_baseline": 0.0,
            "overlapping_event_windows": 0,
            "overlapping_event_share": 0.0,
        }
    mean_return = statistics.fmean(values)
    baseline_mean = statistics.fmean(baseline)
    overlaps, share = overlap_share(indices)
    return {
        "event_count": len(values),
        "mean_signed_return": mean_return,
        "median_signed_return": statistics.median(values),
        "positive_share": sum(value > 0 for value in values) / len(values),
        "unconditional_mean_return": baseline_mean,
        "mean_minus_baseline": mean_return - baseline_mean,
        "overlapping_event_windows": overlaps,
        "overlapping_event_share": share,
    }


def prototype_decision(
    high: dict[str, int | float],
    low: dict[str, int | float],
) -> tuple[str, str]:
    if int(high["event_count"]) == 0 or int(low["event_count"]) == 0:
        return "PARK", "ONE_OR_BOTH_TAILS_HAVE_ZERO_EVENTS"
    passed = (
        float(high["mean_signed_return"]) > 0.0
        and float(high["mean_minus_baseline"]) > 0.0
        and float(low["mean_signed_return"]) > 0.0
        and float(low["mean_minus_baseline"]) > 0.0
    )
    if passed:
        return "ADVANCE_TO_ECONOMIC_SCREEN", "ALL_FOUR_PRIMARY_INEQUALITIES_MET"
    return "REJECT", "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED"


def evaluate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    eligible: list[int] = []
    up_baseline: list[float] = []
    down_baseline: list[float] = []
    high_values: list[float] = []
    low_values: list[float] = []
    high_indices: list[int] = []
    low_indices: list[int] = []

    for index in range(HORIZON_HOURS, len(rows) - HORIZON_HOURS - 1):
        if not valid_window(rows, index):
            continue
        entry = rows[index + 1]
        exit_bar = rows[index + 1 + HORIZON_HOURS]
        up_value = up_signed_return(entry, exit_bar)
        down_value = down_signed_return(entry, exit_bar)
        up_baseline.append(up_value)
        down_baseline.append(down_value)
        eligible.append(index)

        feature = prior_return(rows, index)
        if feature >= Q90_DEV:
            high_values.append(down_value)
            high_indices.append(index)
        if feature <= Q10_DEV:
            low_values.append(up_value)
            low_indices.append(index)

    if not eligible:
        raise Proto02Error("no eligible confirmatory observations")

    high = side_metrics(high_values, down_baseline, high_indices)
    low = side_metrics(low_values, up_baseline, low_indices)
    decision, reason = prototype_decision(high, low)
    return {
        "schema_version": "hyp0002-proto01-result-1",
        "hypothesis_id": "HYP-0002",
        "prototype_sequence": "PROTO-01",
        "evidence_class": "EXPLORATORY_PROTOTYPE",
        "economic_label": "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
        "frozen_thresholds": {
            "q10_dev": Q10_DEV,
            "q90_dev": Q90_DEV,
        },
        "metrics": {
            "aligned_bars": len(rows),
            "eligible_observations": len(eligible),
            "high_tail_down": high,
            "low_tail_up": low,
        },
        "decision": decision,
        "decision_reason": reason,
    }


def run_result() -> int:
    manifest = load_manifest()
    result = evaluate(read_rows())
    result["dataset"] = {
        "dataset_id": manifest["dataset_id"],
        "dataset_version": manifest["dataset_version"],
        "prepared_csv_sha256": EXPECTED_DATASET_SHA256,
    }
    result["run_context"] = {
        "git_commit": git_head(),
        "completed_at": datetime.now(UTC).isoformat(),
    }
    result["limitations"] = [
        "Commission is not modeled.",
        "Financing/rollover is not modeled.",
        "1H quote opens are not guaranteed live fills.",
        "Overlapping forward windows create dependent observations.",
        "This is exploratory prototype evidence, not validation evidence.",
    ]

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    high = result["metrics"]["high_tail_down"]
    low = result["metrics"]["low_tail_up"]
    lines = [
        "ATS HYP-0002 PROTO-01 RESULT",
        "=============================",
        f"Git commit: {result['run_context']['git_commit']}",
        f"High-tail DOWN events: {high['event_count']}",
        f"High-tail DOWN mean: {high['mean_signed_return']:.12f}",
        f"High-tail DOWN excess: {high['mean_minus_baseline']:.12f}",
        f"Low-tail UP events: {low['event_count']}",
        f"Low-tail UP mean: {low['mean_signed_return']:.12f}",
        f"Low-tail UP excess: {low['mean_minus_baseline']:.12f}",
        f"Decision: {result['decision']}",
        f"Reason: {result['decision_reason']}",
        "Economic label: QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
    ]
    RESULT_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


def main() -> int:
    try:
        return run_result()
    except (Proto02Error, OSError, ValueError, KeyError) as exc:
        print(f"HYP-0002 PROTO-01 BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
