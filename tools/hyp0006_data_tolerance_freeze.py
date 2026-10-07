#!/usr/bin/env python3
"""RF-028 pre-reveal HYP-0006 data/tolerance freeze.

This tool consumes only RF-027 identity/timestamp geometry. It does not read
quote prices and does not calculate HYP-0006 returns, the primary inequality,
directional returns, or P&L.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-028"
HYPOTHESIS_ID = "HYP-0006"
RF027_COMMIT = "bbbdbd301b610dfc61316c9ff82015fb0e039a47"

RF027_RESULT = ROOT / "reports" / "local_ci" / "HYP0006_DATA_FEASIBILITY_PREP.json"
GEOMETRY_CSV = ROOT / "data" / "derived" / "HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv"
REPORT_JSON = ROOT / "reports" / "local_ci" / "HYP0006_DATA_TOLERANCE_FREEZE.json"
REPORT_TEXT = ROOT / "reports" / "local_ci" / "HYP0006_DATA_TOLERANCE_FREEZE_REPORT.txt"

DATASET_ID = "DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001"
DATASET_VERSION = "1.0.0"

EXPECTED_BLS_MANIFEST_SHA256 = "3837c463b36914c2276e9985a8a70a8ead13ca0e4b16901a22cb4fd2dece6ee4"
EXPECTED_BLS_BUNDLE_SHA256 = "5306799d4c4196941d701e661df2fa4255682783b966e7bcfd69f702a1ead341"
EXPECTED_BLS_CALENDAR_SHA256 = "646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9"
EXPECTED_SOURCE_BUNDLE_SHA256 = "5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425"
EXPECTED_GEOMETRY_SHA256 = "e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034"
EXPECTED_EVENT_COUNT = 217
EXPECTED_TICK_OBJECT_COUNT = 1085
EXPECTED_BLS_SNAPSHOT_COUNT = 19

# Frozen before RF-028 exact-main execution and before any HYP-0006 outcome reveal.
BOUNDARY_MAX_ABS_GAP_MS = 30_000
PRE_RELEASE_MAX_STALENESS_MS = 30_000
BOUNDARY_TIE_BREAK = "PREVIOUS_ON_EQUAL_GAP"
DUPLICATE_TIMESTAMP_TIE_BREAK = "LAST_RAW_RECORD_AT_SELECTED_MILLISECOND"
PRE_RELEASE_RULE = "LAST_QUOTE_STRICTLY_BEFORE_RELEASE"
SAME_TIME_EVENT_POLICY = "FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION"
MISSING_DATA_POLICY = "EXCLUDE_EVENT_IF_ANY_REQUIRED_ANCHOR_FAILS_FROZEN_GAP_RULE"
PRICE_PAIRING_RULE = "BID_AND_ASK_FROM_SAME_RAW_TICK_RECORD"

GEOMETRY_HEADER = (
    "event_id",
    "archive_release_date",
    "release_time_utc",
    "archive_zone_label",
    "schedule_crosscheck_status",
    "same_time_bls_labels",
    "required_tick_object_count",
    "missing_tick_object_count",
    "pre60_prev_gap_ms",
    "pre60_next_gap_ms",
    "pre_release_last_gap_ms",
    "post60_prev_gap_ms",
    "post60_next_gap_ms",
    "quote_geometry_status",
)

PROHIBITED_OUTCOME_TOKENS = (
    "bid",
    "ask",
    "mid",
    "price",
    "return",
    "inequality",
    "pnl",
    "profit",
)


class FreezeError(RuntimeError):
    """Raised when the RF-028 pre-reveal freeze cannot be reproduced."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _require_equal(payload: dict[str, Any], key: str, expected: Any) -> None:
    actual = payload.get(key)
    if actual != expected:
        raise FreezeError(f"RF-027 identity mismatch for {key}: {actual!r} != {expected!r}")


def load_rf027_result() -> dict[str, Any]:
    if not RF027_RESULT.is_file():
        raise FreezeError(f"missing exact-main RF-027 result: {RF027_RESULT}")

    try:
        payload = json.loads(RF027_RESULT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FreezeError(f"cannot read RF-027 result: {exc}") from exc
    if not isinstance(payload, dict):
        raise FreezeError("RF-027 result is not a JSON object")

    checks = {
        "schema_version": "hyp0006-data-feasibility-prep-2",
        "task_id": "ATS2-RF-027",
        "hypothesis_id": HYPOTHESIS_ID,
        "git_commit": RF027_COMMIT,
        "evidence_classification": "DEVELOPMENT_EXPLORATORY_ONLY",
        "event_inventory_source": "BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS",
        "event_time_source": "BLS_ANNUAL_SCHEDULE_US_EASTERN",
        "quote_source": "DUKASCOPY_HOURLY_TICK_BI5",
        "bls_snapshot_manifest_sha256": EXPECTED_BLS_MANIFEST_SHA256,
        "bls_snapshot_count": EXPECTED_BLS_SNAPSHOT_COUNT,
        "bls_snapshot_bundle_sha256": EXPECTED_BLS_BUNDLE_SHA256,
        "bls_calendar_csv_sha256": EXPECTED_BLS_CALENDAR_SHA256,
        "candidate_event_count": EXPECTED_EVENT_COUNT,
        "resolved_event_time_count": EXPECTED_EVENT_COUNT,
        "complete_timestamp_geometry_event_count": EXPECTED_EVENT_COUNT,
        "requested_tick_object_count": EXPECTED_TICK_OBJECT_COUNT,
        "acquired_tick_object_count": EXPECTED_TICK_OBJECT_COUNT,
        "missing_tick_object_count": 0,
        "protected_hyp0005_source_requests": 0,
        "source_bundle_sha256": EXPECTED_SOURCE_BUNDLE_SHA256,
        "geometry_csv_sha256": EXPECTED_GEOMETRY_SHA256,
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "preparation_decision": "READY_FOR_DATA_FEASIBILITY_FREEZE",
    }
    for key, expected in checks.items():
        _require_equal(payload, key, expected)

    if len(payload.get("events", [])) != EXPECTED_EVENT_COUNT:
        raise FreezeError("RF-027 event array length mismatch")
    if len(payload.get("tick_objects", [])) != EXPECTED_TICK_OBJECT_COUNT:
        raise FreezeError("RF-027 tick-object array length mismatch")
    if len(payload.get("source_objects", [])) != EXPECTED_BLS_SNAPSHOT_COUNT:
        raise FreezeError("RF-027 source-object array length mismatch")

    return payload


def load_geometry_rows() -> list[dict[str, str]]:
    if not GEOMETRY_CSV.is_file():
        raise FreezeError(f"missing RF-027 geometry CSV: {GEOMETRY_CSV}")
    actual_hash = sha256_file(GEOMETRY_CSV)
    if actual_hash != EXPECTED_GEOMETRY_SHA256:
        raise FreezeError(
            f"geometry CSV SHA-256 mismatch: {actual_hash} != {EXPECTED_GEOMETRY_SHA256}"
        )

    with GEOMETRY_CSV.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != GEOMETRY_HEADER:
            raise FreezeError("geometry CSV header changed")
        rows = [dict(row) for row in reader]

    if len(rows) != EXPECTED_EVENT_COUNT:
        raise FreezeError(f"geometry event count changed: {len(rows)} != {EXPECTED_EVENT_COUNT}")
    if len({row["event_id"] for row in rows}) != len(rows):
        raise FreezeError("duplicate event_id in geometry CSV")

    for field in GEOMETRY_HEADER:
        lowered = field.lower()
        if any(token in lowered for token in PROHIBITED_OUTCOME_TOKENS):
            raise FreezeError(f"prohibited outcome/price field in geometry input: {field}")

    return rows


def parse_gap(row: dict[str, str], field: str) -> int:
    raw = row.get(field, "")
    if raw == "":
        raise FreezeError(f"missing geometry gap {field} for {row.get('event_id')}")
    try:
        value = int(raw)
    except ValueError as exc:
        raise FreezeError(f"invalid geometry gap {field}: {raw!r}") from exc
    if value < 0:
        raise FreezeError(f"negative geometry gap {field}: {value}")
    return value


def nearest_side(previous_gap_ms: int, next_gap_ms: int) -> tuple[str, int]:
    if previous_gap_ms <= next_gap_ms:
        return "PREVIOUS", previous_gap_ms
    return "NEXT", next_gap_ms


def evaluate_geometry_row(row: dict[str, str]) -> dict[str, Any]:
    event_id = row["event_id"]
    reasons: list[str] = []

    if row.get("quote_geometry_status") != "COMPLETE_TIMESTAMP_GEOMETRY":
        reasons.append("INCOMPLETE_TIMESTAMP_GEOMETRY")
    if row.get("missing_tick_object_count") != "0":
        reasons.append("MISSING_TICK_OBJECT")

    pre60_side, pre60_gap = nearest_side(
        parse_gap(row, "pre60_prev_gap_ms"),
        parse_gap(row, "pre60_next_gap_ms"),
    )
    post60_side, post60_gap = nearest_side(
        parse_gap(row, "post60_prev_gap_ms"),
        parse_gap(row, "post60_next_gap_ms"),
    )
    pre_release_gap = parse_gap(row, "pre_release_last_gap_ms")

    if pre60_gap > BOUNDARY_MAX_ABS_GAP_MS:
        reasons.append("PRE_60_ANCHOR_GAP_EXCEEDS_30000MS")
    if pre_release_gap > PRE_RELEASE_MAX_STALENESS_MS:
        reasons.append("PRE_RELEASE_STALENESS_EXCEEDS_30000MS")
    if post60_gap > BOUNDARY_MAX_ABS_GAP_MS:
        reasons.append("POST_60_ANCHOR_GAP_EXCEEDS_30000MS")

    return {
        "event_id": event_id,
        "eligible": not reasons,
        "exclusion_reasons": reasons,
        "pre60_selected_side": pre60_side,
        "pre60_selected_gap_ms": pre60_gap,
        "pre_release_last_gap_ms": pre_release_gap,
        "post60_selected_side": post60_side,
        "post60_selected_gap_ms": post60_gap,
    }


def prepare() -> dict[str, Any]:
    load_rf027_result()
    rows = load_geometry_rows()
    evaluations = [evaluate_geometry_row(row) for row in rows]

    eligible = [item for item in evaluations if item["eligible"]]
    ineligible = [item for item in evaluations if not item["eligible"]]
    reason_counts: Counter[str] = Counter()
    for item in ineligible:
        reason_counts.update(item["exclusion_reasons"])

    decision = (
        "FREEZE_DATA_AND_TOLERANCES"
        if eligible
        else "INSUFFICIENT_ANCHOR_GEOMETRY_UNDER_FROZEN_TOLERANCES"
    )

    return {
        "schema_version": "hyp0006-data-tolerance-freeze-1",
        "task_id": TASK_ID,
        "hypothesis_id": HYPOTHESIS_ID,
        "git_commit": git_head(),
        "rf027_git_commit": RF027_COMMIT,
        "dataset_id": DATASET_ID,
        "dataset_version": DATASET_VERSION,
        "evidence_classification": "DEVELOPMENT_EXPLORATORY_ONLY",
        "development_start": "2003-08-03T21:00:00Z",
        "development_end_exclusive": "2021-09-01T00:00:00Z",
        "event_inventory_source": "BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS",
        "event_time_source": "BLS_ANNUAL_SCHEDULE_US_EASTERN",
        "quote_source": "DUKASCOPY_HOURLY_TICK_BI5",
        "bls_snapshot_manifest_sha256": EXPECTED_BLS_MANIFEST_SHA256,
        "bls_snapshot_bundle_sha256": EXPECTED_BLS_BUNDLE_SHA256,
        "bls_calendar_csv_sha256": EXPECTED_BLS_CALENDAR_SHA256,
        "source_bundle_sha256": EXPECTED_SOURCE_BUNDLE_SHA256,
        "geometry_csv_sha256": EXPECTED_GEOMETRY_SHA256,
        "candidate_event_count": EXPECTED_EVENT_COUNT,
        "boundary_max_abs_gap_ms": BOUNDARY_MAX_ABS_GAP_MS,
        "pre_release_max_staleness_ms": PRE_RELEASE_MAX_STALENESS_MS,
        "pre60_anchor_selection": "NEAREST_TO_T_MINUS_60M_WITHIN_FROZEN_GAP",
        "post60_anchor_selection": "NEAREST_TO_T_PLUS_60M_WITHIN_FROZEN_GAP",
        "boundary_tie_break": BOUNDARY_TIE_BREAK,
        "pre_release_rule": PRE_RELEASE_RULE,
        "duplicate_timestamp_tie_break": DUPLICATE_TIMESTAMP_TIE_BREAK,
        "price_pairing_rule": PRICE_PAIRING_RULE,
        "same_time_event_policy": SAME_TIME_EVENT_POLICY,
        "missing_data_policy": MISSING_DATA_POLICY,
        "eligible_event_count": len(eligible),
        "ineligible_event_count": len(ineligible),
        "eligible_event_ids": [item["event_id"] for item in eligible],
        "ineligible_events": [
            {
                "event_id": item["event_id"],
                "exclusion_reasons": item["exclusion_reasons"],
            }
            for item in ineligible
        ],
        "exclusion_reason_counts": dict(sorted(reason_counts.items())),
        "geometry_evaluations": evaluations,
        "freeze_decision": decision,
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    }


def write_reports(result: dict[str, Any]) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "HYP-0006 DATA/TOLERANCE FREEZE",
        "==============================",
        f"Task: {result['task_id']}",
        f"Commit: {result['git_commit']}",
        f"RF-027 commit: {result['rf027_git_commit']}",
        f"Decision: {result['freeze_decision']}",
        f"Dataset: {result['dataset_id']}@{result['dataset_version']}",
        f"Candidate CPI events: {result['candidate_event_count']}",
        f"Eligible events: {result['eligible_event_count']}",
        f"Ineligible events: {result['ineligible_event_count']}",
        f"Boundary max absolute gap ms: {result['boundary_max_abs_gap_ms']}",
        f"Pre-release max staleness ms: {result['pre_release_max_staleness_ms']}",
        f"Source bundle SHA-256: {result['source_bundle_sha256']}",
        f"Geometry CSV SHA-256: {result['geometry_csv_sha256']}",
        f"Outcome metrics computed: {result['outcome_metrics_computed']}",
        f"Primary claim evaluated: {result['primary_claim_evaluated']}",
        f"Information boundary: {result['information_boundary']}",
        "",
        "NEXT STEP",
        "---------",
        "Send CURRENT_TASK_REPORT.txt and HYP0006_DATA_TOLERANCE_FREEZE.json to ChatGPT.",
        "Do not calculate HYP-0006 pre/post returns or the primary inequality.",
    ]
    REPORT_TEXT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)


def main() -> int:
    print("ATS HYP-0006 DATA/TOLERANCE FREEZE", flush=True)
    try:
        result = prepare()
        write_reports(result)
    except (FreezeError, OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"[FAIL] RF-028 freeze: {exc}", flush=True)
        return 1

    if result["freeze_decision"] != "FREEZE_DATA_AND_TOLERANCES":
        print(f"[FAIL] RF-028 freeze: {result['freeze_decision']}", flush=True)
        return 1

    print("[PASS] RF-028 pre-reveal data/tolerance freeze", flush=True)
    print("Information boundary: NO_HYPOTHESIS_OUTCOME_COMPUTED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
