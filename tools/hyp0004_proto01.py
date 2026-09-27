#!/usr/bin/env python3
"""Run frozen HYP-0004 PROTO-01 on the frozen EUR/USD H1 development dataset."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/derived/HYP-0004-DEV-01-EURUSD-H1.csv"
MANIFEST_PATH = ROOT / "data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001.yaml"
RESULT_PATH = ROOT / "reports/local_ci/HYP0004_PROTO01_RESULT.json"
RESULT_REPORT_PATH = ROOT / "reports/local_ci/HYP0004_PROTO01_RESULT_REPORT.txt"

EXPECTED_DATASET_ID = "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001"
EXPECTED_DATASET_VERSION = "1.0.0"
EXPECTED_DATASET_SHA256 = "3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6"
EXPECTED_ROWS = 112_900
EXPECTED_ELIGIBLE = 111_938
EXPECTED_ELIGIBLE_BY_BUCKET = {
    "CORE_ACTIVE": 47_012,
    "OFF_HOURS": 46_737,
    "TRANSITION": 18_189,
}
EXPECTED_CLOSED_NEXT = 940
EXPECTED_MISSING_NEXT = 21
EXPECTED_DATASET_END = 1
BOUNDARY_AVAILABILITY_MODE = "H1_OPEN_PROXY_AT_EVENT_TIME"
BUCKETS = ("CORE_ACTIVE", "TRANSITION", "OFF_HOURS")
PRIMARY_BUCKETS = ("CORE_ACTIVE", "OFF_HOURS")

Row = dict[str, Any]
Observation = dict[str, Any]


class Proto04Error(RuntimeError):
    """Raised when the frozen HYP-0004 PROTO-01 contract cannot execute."""


def parse_time(value: str) -> datetime:
    parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    return parsed


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


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


def midpoint(bid: float, ask: float) -> float:
    if not all(math.isfinite(value) and value > 0.0 for value in (bid, ask)):
        raise ValueError("midpoint requires finite positive BID/ASK")
    if ask < bid:
        raise ValueError("midpoint requires ASK >= BID")
    return (bid + ask) / 2.0


def relative_spread(bid: float, ask: float) -> float:
    mid = midpoint(bid, ask)
    return (ask - bid) / mid


def abs_next_1h_return(
    bid: float,
    ask: float,
    next_bid: float,
    next_ask: float,
) -> float:
    current_mid = midpoint(bid, ask)
    next_mid = midpoint(next_bid, next_ask)
    return abs(next_mid / current_mid - 1.0)


def load_manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open(encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle)
    if not isinstance(manifest, dict):
        raise Proto04Error("development Dataset Manifest is not a mapping")
    if manifest.get("dataset_id") != EXPECTED_DATASET_ID:
        raise Proto04Error("development Dataset ID mismatch")
    if manifest.get("dataset_version") != EXPECTED_DATASET_VERSION:
        raise Proto04Error("development Dataset version mismatch")
    if manifest.get("integrity", {}).get("digest") != EXPECTED_DATASET_SHA256:
        raise Proto04Error("development manifest prepared CSV SHA-256 mismatch")
    if sha256_file(DATA_PATH) != EXPECTED_DATASET_SHA256:
        raise Proto04Error("development prepared CSV SHA-256 mismatch")
    lineage_steps = manifest.get("transformation_lineage", {}).get("steps", [])
    if not any(BOUNDARY_AVAILABILITY_MODE in str(item) for item in lineage_steps):
        raise Proto04Error("boundary availability mode missing from manifest lineage")
    return manifest


def _parse_positive_float(value: str, field: str, line_no: int) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise Proto04Error(f"invalid {field} at line {line_no}: {value!r}") from exc
    if not math.isfinite(parsed) or parsed <= 0.0:
        raise Proto04Error(f"non-positive/non-finite {field} at line {line_no}")
    return parsed


def read_rows() -> dict[datetime, Row]:
    rows: dict[datetime, Row] = {}
    previous_time: datetime | None = None
    previous_parent_sequence: int | None = None

    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for index, raw in enumerate(reader):
            line_no = index + 2
            event_time = parse_time(raw["event_time"])
            availability_time = parse_time(raw["availability_time"])
            parent_availability = parse_time(raw["parent_row_availability_time"])

            if availability_time != event_time:
                raise Proto04Error(f"derived availability_time mismatch at line {line_no}")
            if parent_availability != event_time + timedelta(hours=1):
                raise Proto04Error(f"parent_row_availability_time mismatch at line {line_no}")
            if raw["source_symbol"] != "EURUSD":
                raise Proto04Error(f"unexpected source_symbol at line {line_no}")
            if raw["utc_bucket"] != bucket_for_hour(event_time.hour):
                raise Proto04Error(f"UTC bucket mismatch at line {line_no}")
            if not is_fx_market_hour(event_time):
                raise Proto04Error(f"closed-market row present at {iso_z(event_time)}")
            if event_time in rows:
                raise Proto04Error(f"duplicate event_time at {iso_z(event_time)}")
            if previous_time is not None and event_time <= previous_time:
                raise Proto04Error(f"out-of-order event_time at {iso_z(event_time)}")

            try:
                sequence = int(raw["sequence"])
                parent_sequence = int(raw["parent_sequence"])
            except (TypeError, ValueError) as exc:
                raise Proto04Error(f"invalid sequence at line {line_no}") from exc
            if sequence != index:
                raise Proto04Error(f"derived sequence mismatch at line {line_no}")
            if previous_parent_sequence is not None and parent_sequence <= previous_parent_sequence:
                raise Proto04Error(f"parent sequence is not increasing at line {line_no}")

            bid = _parse_positive_float(raw["bid_open"], "bid_open", line_no)
            ask = _parse_positive_float(raw["ask_open"], "ask_open", line_no)
            if ask < bid:
                raise Proto04Error(f"ask_open < bid_open at line {line_no}")

            rows[event_time] = {
                "event_time": event_time,
                "utc_bucket": raw["utc_bucket"],
                "bid_open": bid,
                "ask_open": ask,
            }
            previous_time = event_time
            previous_parent_sequence = parent_sequence

    if len(rows) != EXPECTED_ROWS:
        raise Proto04Error(f"development row count mismatch: {len(rows)} != {EXPECTED_ROWS}")
    return rows


def eligible_observations(rows: dict[datetime, Row]) -> tuple[list[Observation], dict[str, Any]]:
    if not rows:
        raise ValueError("rows must not be empty")

    last_event = max(rows)
    observations: list[Observation] = []
    closed_next = 0
    missing_next = 0
    dataset_end = 0
    eligible_by_bucket = Counter({bucket: 0 for bucket in BUCKETS})

    for event_time in sorted(rows):
        current = rows[event_time]
        next_time = event_time + timedelta(hours=1)
        if next_time > last_event:
            dataset_end += 1
            continue
        if not is_fx_market_hour(next_time):
            closed_next += 1
            continue
        next_row = rows.get(next_time)
        if next_row is None:
            missing_next += 1
            continue

        bucket = str(current["utc_bucket"])
        eligible_by_bucket[bucket] += 1
        observations.append(
            {
                "event_time": event_time,
                "year": event_time.year,
                "utc_bucket": bucket,
                "abs_next_1h_return": abs_next_1h_return(
                    float(current["bid_open"]),
                    float(current["ask_open"]),
                    float(next_row["bid_open"]),
                    float(next_row["ask_open"]),
                ),
                "relative_spread": relative_spread(
                    float(current["bid_open"]),
                    float(current["ask_open"]),
                ),
            }
        )

    geometry = {
        "eligible_count": len(observations),
        "eligible_by_bucket": dict(sorted(eligible_by_bucket.items())),
        "ineligible_closed_market_next_hour_count": closed_next,
        "ineligible_missing_expected_next_hour_count": missing_next,
        "ineligible_dataset_end_count": dataset_end,
    }
    return observations, geometry


def verify_frozen_geometry(geometry: dict[str, Any]) -> None:
    checks = {
        "eligible_count": EXPECTED_ELIGIBLE,
        "eligible_by_bucket": EXPECTED_ELIGIBLE_BY_BUCKET,
        "ineligible_closed_market_next_hour_count": EXPECTED_CLOSED_NEXT,
        "ineligible_missing_expected_next_hour_count": EXPECTED_MISSING_NEXT,
        "ineligible_dataset_end_count": EXPECTED_DATASET_END,
    }
    for key, expected in checks.items():
        actual = geometry.get(key)
        if actual != expected:
            raise Proto04Error(f"frozen geometry mismatch for {key}: {actual!r} != {expected!r}")


def bucket_metrics(observations: list[Observation]) -> dict[str, Any]:
    grouped: dict[str, list[Observation]] = {bucket: [] for bucket in BUCKETS}
    for observation in observations:
        grouped[str(observation["utc_bucket"])].append(observation)

    result: dict[str, Any] = {}
    for bucket in BUCKETS:
        values = grouped[bucket]
        if not values:
            result[bucket] = {
                "observation_count": 0,
                "mean_abs_next_1h_return": None,
                "median_abs_next_1h_return": None,
                "median_relative_spread": None,
            }
            continue
        absolute_returns = [float(item["abs_next_1h_return"]) for item in values]
        spreads = [float(item["relative_spread"]) for item in values]
        result[bucket] = {
            "observation_count": len(values),
            "mean_abs_next_1h_return": statistics.fmean(absolute_returns),
            "median_abs_next_1h_return": statistics.median(absolute_returns),
            "median_relative_spread": statistics.median(spreads),
        }
    return result


def calendar_year_diagnostics(observations: list[Observation]) -> dict[str, Any]:
    grouped: dict[str, dict[int, list[Observation]]] = {
        bucket: defaultdict(list) for bucket in BUCKETS
    }
    for observation in observations:
        grouped[str(observation["utc_bucket"])][int(observation["year"])].append(observation)

    result: dict[str, Any] = {}
    for bucket in BUCKETS:
        years: dict[str, Any] = {}
        total = sum(len(values) for values in grouped[bucket].values())
        for year, values in sorted(grouped[bucket].items()):
            absolute_returns = [float(item["abs_next_1h_return"]) for item in values]
            spreads = [float(item["relative_spread"]) for item in values]
            years[str(year)] = {
                "observation_count": len(values),
                "observation_share": len(values) / total if total else None,
                "median_abs_next_1h_return": statistics.median(absolute_returns),
                "median_relative_spread": statistics.median(spreads),
            }
        max_share = max(
            (float(item["observation_share"]) for item in years.values()),
            default=0.0,
        )
        result[bucket] = {
            "max_calendar_year_observation_share": max_share,
            "years": years,
        }
    return result


def primary_summary(metrics: dict[str, Any]) -> dict[str, Any]:
    core = metrics["CORE_ACTIVE"]
    off = metrics["OFF_HOURS"]
    if not core["observation_count"] or not off["observation_count"]:
        return {
            "movement_inequality_pass": False,
            "spread_inequality_pass": False,
            "both_primary_inequalities_pass": False,
        }

    movement_pass = float(core["median_abs_next_1h_return"]) > float(
        off["median_abs_next_1h_return"]
    )
    spread_pass = float(core["median_relative_spread"]) <= float(off["median_relative_spread"])
    return {
        "movement_inequality_pass": movement_pass,
        "spread_inequality_pass": spread_pass,
        "both_primary_inequalities_pass": movement_pass and spread_pass,
    }


def prototype_decision(metrics: dict[str, Any]) -> tuple[str, str, str]:
    core_count = int(metrics["CORE_ACTIVE"]["observation_count"])
    off_count = int(metrics["OFF_HOURS"]["observation_count"])
    if core_count == 0 or off_count == 0:
        return "PARK", "PRIMARY_BUCKET_HAS_ZERO_OBSERVATIONS", "PARK"

    primary = primary_summary(metrics)
    if primary["both_primary_inequalities_pass"]:
        return (
            "ADVANCE_TO_ECONOMIC_SCREEN",
            "BOTH_PRIMARY_INEQUALITIES_MET",
            "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
        )
    return "REJECT", "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED", "STOP_HYP0004"


def evaluate(observations: list[Observation]) -> dict[str, Any]:
    metrics = bucket_metrics(observations)
    primary = primary_summary(metrics)
    decision, reason, next_action = prototype_decision(metrics)
    return {
        "schema_version": "hyp0004-proto01-result-1",
        "hypothesis_id": "HYP-0004",
        "prototype_sequence": "PROTO-01",
        "evidence_class": "EXPLORATORY_PROTOTYPE",
        "measurement_label": "STRUCTURAL_H1_OPEN_PROXY_NO_TRADING_PNL",
        "bucket_metrics": metrics,
        "calendar_year_diagnostics": calendar_year_diagnostics(observations),
        "primary": primary,
        "decision": decision,
        "decision_reason": reason,
        "next_action": next_action,
    }


def run_result() -> int:
    manifest = load_manifest()
    observations, geometry = eligible_observations(read_rows())
    verify_frozen_geometry(geometry)
    result = evaluate(observations)
    result["dataset"] = {
        "dataset_id": manifest["dataset_id"],
        "dataset_version": manifest["dataset_version"],
        "prepared_csv_sha256": EXPECTED_DATASET_SHA256,
        "boundary_availability_mode": BOUNDARY_AVAILABILITY_MODE,
        "exact_tick_boundary_time_known": False,
        "eligible_exact_next_hour_count": EXPECTED_ELIGIBLE,
    }
    result["geometry"] = geometry
    result["run_context"] = {
        "git_commit": git_head(),
        "completed_at": datetime.now(UTC).isoformat(),
    }
    result["limitations"] = [
        "H1_OPEN_PROXY_AT_EVENT_TIME is a development approximation.",
        "Exact tick-level boundary time is unknown.",
        "The result is a structural distribution test, not a directional trading rule.",
        "Commission, financing and live-fill slippage are not modeled.",
        "Development data are exploratory and are not validation or independent evidence.",
        "A positive result requires a separate fixed confirmatory or trading Hypothesis before R4.",
    ]

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    core = result["bucket_metrics"]["CORE_ACTIVE"]
    off = result["bucket_metrics"]["OFF_HOURS"]
    primary = result["primary"]
    lines = [
        "ATS HYP-0004 PROTO-01 RESULT",
        "=============================",
        f"Git commit: {result['run_context']['git_commit']}",
        f"Eligible observations: {geometry['eligible_count']}",
        f"CORE_ACTIVE median abs next-1h return: {core['median_abs_next_1h_return']}",
        f"OFF_HOURS median abs next-1h return: {off['median_abs_next_1h_return']}",
        f"Movement inequality pass: {primary['movement_inequality_pass']}",
        f"CORE_ACTIVE median relative spread: {core['median_relative_spread']}",
        f"OFF_HOURS median relative spread: {off['median_relative_spread']}",
        f"Spread inequality pass: {primary['spread_inequality_pass']}",
        f"Both primary inequalities pass: {primary['both_primary_inequalities_pass']}",
        f"Decision: {result['decision']}",
        f"Reason: {result['decision_reason']}",
        f"Next action: {result['next_action']}",
        "Measurement label: STRUCTURAL_H1_OPEN_PROXY_NO_TRADING_PNL",
    ]
    RESULT_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


def main() -> int:
    try:
        return run_result()
    except (
        Proto04Error,
        OSError,
        ValueError,
        KeyError,
        ZeroDivisionError,
    ) as exc:
        print(f"HYP-0004 PROTO-01 BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
