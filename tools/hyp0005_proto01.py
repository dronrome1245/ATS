#!/usr/bin/env python3
"""Frozen-intent HYP-0005 confirmatory structural runner; default CLI is blocked."""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
import math
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/derived/HYP-0005-CONF-01-EURUSD-H1.csv"
MANIFEST_PATH = ROOT / "data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001.yaml"
PREPARATION_JSON = ROOT / "reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP.json"
RESULT_JSON = ROOT / "reports/local_ci/HYP0005_PROTO01_RESULT.json"
RESULT_TEXT = ROOT / "reports/local_ci/HYP0005_PROTO01_RESULT_REPORT.txt"

HYPOTHESIS_ID = "HYP-0005"
PARENT_IDEA_ID = "IDEA-0004"
DATASET_ID = "DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001"
DATASET_VERSION = "1.0.0"
CSV_SHA256 = "b1091c4975665b2b0cd4f58627a10aceaab7aeff5076431abb6abc74c0a054c1"
PREPARATION_SHA256 = "d2eadd9a64da74ae79e2a0008426147953f24beb8c23f66557a721a7b8a65381"
SOURCE_BUNDLE_SHA256 = "65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2"
RF024_MAIN_COMMIT = "dd014ef6a1014edcfaa26f7d735478aee0cc94ef"
FROZEN_PARENT_RUNNER_BLOB = "cbc9a46bf5e5296615f51c0ea564153968bc2a55"
FROZEN_PREP_RUNNER_BLOB = "b8d72d858d5c2691de7dec9a709f6e4d7ccb2808"
FROZEN_HYPOTHESIS_BLOB = "ebbbc89187c911485c1568dc11f5f2f9e703718a"
TIMING_MODE = "H1_OPEN_PROXY_AT_EVENT_TIME"
BUCKETS = ("CORE_ACTIVE", "TRANSITION", "OFF_HOURS")
SEGMENTS = (
    ("LEFT_UNSEEN", datetime(2003, 5, 4, 21, tzinfo=UTC), datetime(2003, 8, 3, 21, tzinfo=UTC)),
    ("RIGHT_UNSEEN", datetime(2026, 9, 1, tzinfo=UTC), datetime(2026, 9, 26, tzinfo=UTC)),
)
CSV_FIELDS = (
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
EXPECTED_GEOMETRY = {
    "eligible_exact_next_hour_count": 1991,
    "eligible_rows_by_bucket": {"CORE_ACTIVE": 838, "OFF_HOURS": 837, "TRANSITION": 316},
    "eligible_rows_by_segment": {"LEFT_UNSEEN": 1542, "RIGHT_UNSEEN": 449},
    "expected_market_hours_by_segment": {"LEFT_UNSEEN": 1560, "RIGHT_UNSEEN": 453},
    "missing_market_hours_by_segment": {"LEFT_UNSEEN": 3, "RIGHT_UNSEEN": 0},
    "total_rows_by_bucket": {"CORE_ACTIVE": 839, "OFF_HOURS": 837, "TRANSITION": 334},
    "total_rows_by_segment": {"LEFT_UNSEEN": 1557, "RIGHT_UNSEEN": 453},
    "ineligible_closed_market_next_hour_count": 16,
    "ineligible_missing_expected_next_hour_count": 3,
    "ineligible_segment_end_count": 0,
}
EXPECTED_ROWS = 2010

Row = dict[str, Any]
Observation = dict[str, Any]


class ConfirmatoryProtoError(RuntimeError):
    """Source, frozen-rule or structural-result execution blocker."""


def _load_frozen_dependencies() -> tuple[Any, Any]:
    try:
        baseline = importlib.import_module("tools.hyp0004_proto01")
        preparation = importlib.import_module("tools.hyp0005_data_feasibility")
    except ModuleNotFoundError as exc:
        if exc.name != "tools":
            raise
        baseline = importlib.import_module("hyp0004_proto01")
        preparation = importlib.import_module("hyp0005_data_feasibility")
    return baseline, preparation


def _require(value: bool, message: str) -> None:
    if not value:
        raise ConfirmatoryProtoError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()


def verify_frozen_files() -> dict[str, Any]:
    """No price-value parsing: reject any identity/manifest drift before reveal."""
    for relative, expected in {
        "tools/hyp0004_proto01.py": FROZEN_PARENT_RUNNER_BLOB,
        "tools/hyp0005_data_feasibility.py": FROZEN_PREP_RUNNER_BLOB,
        "research/hypotheses/HYP-0005.md": FROZEN_HYPOTHESIS_BLOB,
    }.items():
        _require(_git("rev-parse", f"HEAD:{relative}") == expected, f"frozen blob drift: {relative}")
        _require(_git("hash-object", "--", relative) == expected, f"worktree drift: {relative}")
    _require(sha256_file(DATA_PATH) == CSV_SHA256, "confirmatory CSV SHA-256 mismatch")
    _require(
        sha256_file(PREPARATION_JSON) == PREPARATION_SHA256,
        "RF-023 preparation JSON SHA-256 mismatch",
    )
    with MANIFEST_PATH.open(encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle)
    _require(isinstance(manifest, dict), "manifest must be mapping")
    _require(manifest.get("dataset_id") == DATASET_ID, "dataset identity drift")
    _require(manifest.get("dataset_version") == DATASET_VERSION, "dataset version drift")
    _require(manifest.get("integrity", {}).get("digest") == CSV_SHA256, "manifest SHA drift")
    _require(
        SOURCE_BUNDLE_SHA256 in manifest.get("source", {}).get("snapshot_reference", ""),
        "source bundle SHA missing from manifest",
    )
    _require(
        manifest.get("storage", {}).get("location") == str(DATA_PATH.relative_to(ROOT)).replace("\\", "/"),
        "manifest CSV location drift",
    )
    _require(manifest.get("time_semantics", {}).get("availability_mode") == "EXPLICIT_FIELD", "availability mode drift")
    _require(
        any(TIMING_MODE in str(step) for step in manifest.get("transformation_lineage", {}).get("steps", [])),
        "H1 bar-open boundary proxy not declared",
    )
    prep_result = json.loads(PREPARATION_JSON.read_text(encoding="utf-8"))
    _require(prep_result.get("git_commit") == "14531698c87fd3a0d87e1ec54c6713f11b7cbb60", "preparation commit drift")
    _require(prep_result.get("derived_csv_sha256") == CSV_SHA256, "prepared CSV digest drift")
    _require(prep_result.get("source_bundle_sha256") == SOURCE_BUNDLE_SHA256, "source bundle identity drift")
    _require(prep_result.get("geometry") == EXPECTED_GEOMETRY, "frozen RF-023 geometry drift")
    _require(prep_result.get("derived_row_count") == EXPECTED_ROWS, "prepared row count drift")
    _require(
        prep_result.get("outcome_metrics_computed") is False
        and prep_result.get("primary_claim_evaluated") is False,
        "preparation data exposed an outcome",
    )
    return manifest


def _time(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except (TypeError, ValueError) as exc:
        raise ConfirmatoryProtoError(f"invalid UTC hour timestamp: {value!r}") from exc


def _price(value: str, name: str) -> float:
    try:
        price = float(value)
    except (TypeError, ValueError) as exc:
        raise ConfirmatoryProtoError(f"invalid {name}") from exc
    _require(math.isfinite(price) and price > 0.0, f"nonpositive/nonfinite {name}")
    return price


def read_frozen_rows() -> dict[tuple[str, datetime], Row]:
    """Read the hash-verified frozen CSV only during separately authorized reveal."""
    _, prep = _load_frozen_dependencies()
    rows: dict[tuple[str, datetime], Row] = {}
    previous: datetime | None = None
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require(tuple(reader.fieldnames or ()) == CSV_FIELDS, "unexpected confirmatory CSV schema")
        for sequence, raw in enumerate(reader):
            event_time = _time(raw["event_time"])
            segment = raw["confirmatory_segment"]
            _require(prep.segment_for_time(event_time) == segment, "frozen segment drift")
            _require(event_time.minute == 0 and event_time.second == 0, "nonhourly event")
            _require(prep.source.is_fx_market_hour(event_time), "closed-market source row")
            _require(raw["source_symbol"] == "EURUSD", "unexpected source symbol")
            _require(raw["utc_bucket"] == prep.bucket_for_hour(event_time.hour), "UTC bucket drift")
            _require(_time(raw["availability_time"]) == event_time, "boundary availability drift")
            _require(
                _time(raw["source_bar_completion_time"]) == event_time + timedelta(hours=1),
                "source bar completion time drift",
            )
            _require(raw["sequence"] == str(sequence), "row sequence drift")
            _require(previous is None or event_time > previous, "duplicate/out-of-order timestamp")
            bid = _price(raw["bid_open"], "bid_open")
            ask = _price(raw["ask_open"], "ask_open")
            _require(ask >= bid, "crossed quote")
            key = (segment, event_time)
            _require(key not in rows, "duplicate segment/event row")
            rows[key] = {
                "event_time": event_time,
                "confirmatory_segment": segment,
                "utc_bucket": raw["utc_bucket"],
                "bid_open": bid,
                "ask_open": ask,
            }
            previous = event_time
    _require(len(rows) == EXPECTED_ROWS, "frozen confirmatory row count mismatch")
    return rows


def frozen_eligible_keys(rows: dict[tuple[str, datetime], Row]) -> list[tuple[str, datetime]]:
    """Exact same-segment +1h only; no closure, missing or cross-segment bridge."""
    _, prep = _load_frozen_dependencies()
    bounds = {segment: end for segment, _, end in SEGMENTS}
    eligible: list[tuple[str, datetime]] = []
    for segment, start in sorted(rows, key=lambda item: item[1]):
        next_hour = start + timedelta(hours=1)
        if next_hour >= bounds[segment] or not prep.source.is_fx_market_hour(next_hour):
            continue
        if (segment, next_hour) in rows:
            eligible.append((segment, start))
    return eligible


def frozen_geometry(rows: dict[tuple[str, datetime], Row]) -> list[tuple[str, datetime]]:
    """Verify all eligibility counts BEFORE any midpoint/spread/return evaluation."""
    _, prep = _load_frozen_dependencies()
    geometry = prep.geometry_summary(list(rows.values()))
    _require(geometry == EXPECTED_GEOMETRY, "confirmatory geometry drift")
    keys = frozen_eligible_keys(rows)
    _require(len(keys) == EXPECTED_GEOMETRY["eligible_exact_next_hour_count"], "eligible count drift")
    return keys


def observations_from_keys(
    rows: dict[tuple[str, datetime], Row], keys: list[tuple[str, datetime]]
) -> list[Observation]:
    """Inherited HYP-0004 equations evaluated ONLY after geometry passes."""
    baseline, _ = _load_frozen_dependencies()
    observations: list[Observation] = []
    for segment, start in keys:
        current = rows[(segment, start)]
        nxt = rows[(segment, start + timedelta(hours=1))]
        bid = float(current["bid_open"])
        ask = float(current["ask_open"])
        observations.append(
            {
                "event_time": start,
                "year": start.year,
                "utc_bucket": current["utc_bucket"],
                "confirmatory_segment": segment,
                "abs_next_1h_return": baseline.abs_next_1h_return(
                    bid, ask, float(nxt["bid_open"]), float(nxt["ask_open"])
                ),
                "relative_spread": baseline.relative_spread(bid, ask),
            }
        )
    return observations


def evaluate_synthetic_or_revealed(observations: list[Observation]) -> dict[str, Any]:
    """Primary rules are fixed; no favorable period, bucket or threshold selection."""
    baseline, _ = _load_frozen_dependencies()
    metrics = baseline.bucket_metrics(observations)
    _require(metrics["CORE_ACTIVE"]["observation_count"] > 0, "zero CORE_ACTIVE observations")
    _require(metrics["OFF_HOURS"]["observation_count"] > 0, "zero OFF_HOURS observations")
    primary = baseline.primary_summary(metrics)
    _require(isinstance(primary["both_primary_inequalities_pass"], bool), "primary malformed")
    passed = primary["both_primary_inequalities_pass"]
    return {
        "bucket_metrics": metrics,
        "calendar_year_diagnostics": baseline.calendar_year_diagnostics(observations),
        "primary": primary,
        "decision": "CONFIRMATORY_STRUCTURAL_PASS" if passed else "CONFIRMATORY_STRUCTURAL_FAIL",
        "decision_reason": (
            "BOTH_PRIMARY_INEQUALITIES_MET"
            if passed
            else "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED"
        ),
        "next_action": (
            "REVIEW_CONFIRMATORY_STRUCTURAL_EVIDENCE_NO_DIRECT_R4"
            if passed
            else "RETAIN_NEGATIVE_CONFIRMATORY_EVIDENCE_NO_RETUNING"
        ),
    }


def run_first_reveal_once() -> dict[str, Any]:
    """Only a future exact-main, explicitly authorized reveal gate may call this."""
    _require(not RESULT_JSON.exists() and not RESULT_TEXT.exists(), "first reveal already exists")
    manifest = verify_frozen_files()
    rows = read_frozen_rows()
    keys = frozen_geometry(rows)
    observations = observations_from_keys(rows, keys)
    result = evaluate_synthetic_or_revealed(observations)
    result.update(
        {
            "schema_version": "hyp0005-confirmatory-proto01-result-1",
            "hypothesis_id": HYPOTHESIS_ID,
            "parent_idea_id": PARENT_IDEA_ID,
            "prototype_id": "PROTO-01",
            "evidence_class": "CONFIRMATORY_STRUCTURAL_NOT_INDEPENDENT_EXAM",
            "measurement_label": "H1_OPEN_PROXY_STRUCTURAL_NO_TRADING_PNL",
            "outcome_metrics_computed": True,
            "primary_claim_evaluated": True,
            "dataset": {
                "dataset_id": DATASET_ID,
                "dataset_version": DATASET_VERSION,
                "derived_csv_sha256": CSV_SHA256,
                "source_bundle_sha256": SOURCE_BUNDLE_SHA256,
                "boundary_availability_mode": TIMING_MODE,
                "exact_tick_boundary_time_known": False,
                "confirmatory_preparation_sha256": PREPARATION_SHA256,
            },
            "geometry": EXPECTED_GEOMETRY,
            "run_context": {"git_commit": _git("rev-parse", "HEAD")},
            "limitations": list(manifest.get("known_limitations", [])),
        }
    )
    RESULT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with RESULT_JSON.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    summary = [
        "HYP-0005 CONFIRMATORY STRUCTURAL PROTO-01 REVEAL",
        "No directional trading strategy, economic proof, or independent examination",
        f"Git commit: {result['run_context']['git_commit']}",
        f"Dataset: {DATASET_ID}@{DATASET_VERSION}",
        f"Eligible exact-next-hour: {len(observations)}",
        f"Decision: {result['decision']}",
        f"Reason: {result['decision_reason']}",
        f"Next action: {result['next_action']}",
        f"Core median absolute next-hour return: {result['bucket_metrics']['CORE_ACTIVE']['median_abs_next_1h_return']}",
        f"Off-hours median absolute next-hour return: {result['bucket_metrics']['OFF_HOURS']['median_abs_next_1h_return']}",
        f"Core median relative spread: {result['bucket_metrics']['CORE_ACTIVE']['median_relative_spread']}",
        f"Off-hours median relative spread: {result['bucket_metrics']['OFF_HOURS']['median_relative_spread']}",
        f"Both predeclared inequalities pass: {result['primary']['both_primary_inequalities_pass']}",
    ]
    with RESULT_TEXT.open("x", encoding="utf-8") as handle:
        handle.write("\n".join(summary) + "\n")
    return result


def main() -> int:
    """Direct invocation blocked: RF-035 freezes code; RF-036 owns first reveal."""
    print(
        "HYP-0005 REVEAL BLOCKED: requires separate exact-main first-reveal authorization"
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
