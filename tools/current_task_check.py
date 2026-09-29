#!/usr/bin/env python3
"""Run ATS2-RF-027 exact-main checks and HYP-0006 data-feasibility preparation."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-027"
TASK_NAME = "HYP-0006 Data Feasibility preparation"

PROTOCOL = Path("research/reviews/HYP-0006-DATA-FEASIBILITY-PREP.md")
TOOL = Path("tools/hyp0006_data_feasibility.py")
TEST = Path("tests/test_hyp0006_data_feasibility.py")
STATE = Path("03_СОСТОЯНИЕ_ПРОЕКТА.yaml")
BACKLOG = Path("governance/backlog/PROGRAM_BACKLOG_V2.md")
HANDOFF = Path("AI_HANDOFF.md")
NEXT_STEP = Path("02_СЛЕДУЮЩИЙ_ШАГ.md")
STATUS = Path("01_СТАТУС_ПРОЕКТА.md")

LOCAL_RESULT = Path("reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP.json")
GEOMETRY_CSV = Path("data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv")

FROZEN_BLOBS = {
    "research/hypotheses/HYP-0005.md": "ebbbc89187c911485c1568dc11f5f2f9e703718a",
    "research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md": (
        "c15b2b67700dd46fc592f1208731ce6b42f6905c"
    ),
    "tools/hyp0005_data_feasibility.py": "310b23213876304ade674ef36ba17ce6d457353f",
    "tests/test_hyp0005_data_feasibility.py": "12697882da682eab699bf5b7debd7c358e56aca9",
    "research/hypotheses/HYP-0006.md": "6b3f260ceacd98adf7a6aa44205404e68e4fd4ca",
    "research/reviews/HYP-0006-DATA-FEASIBILITY.md": ("ae58099a05daec4be385c18177c74f1f22d1eb30"),
}

ALLOWED_DECISIONS = {
    "READY_FOR_DATA_FEASIBILITY_FREEZE",
    "UNRESOLVED_OFFICIAL_EVENT_TIMES",
    "OFFICIAL_TIME_CROSSCHECK_MISMATCH",
    "INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_GEOMETRY_HEADER = (
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
PROHIBITED_OUTCOME_FIELDS = {
    "bid",
    "ask",
    "mid",
    "midpoint",
    "pre_abs_60m_return",
    "post_abs_60m_return",
    "return",
    "pnl",
    "profit",
}


def git_output(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
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


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def require_markers(path: Path, markers: tuple[str, ...]) -> bool:
    full_path = ROOT / path
    if not full_path.is_file():
        print(f"[FAIL] missing RF-027 artifact: {path}", flush=True)
        return False
    content = full_path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in content:
            print(f"[FAIL] RF-027 marker missing in {path}: {marker}", flush=True)
            return False
    return True


def check_frozen_lineage() -> bool:
    print("\n== RF-027 frozen HYP-0005/HYP-0006 lineage ==", flush=True)
    passed = True
    for relative, expected_blob in FROZEN_BLOBS.items():
        path = ROOT / relative
        if not path.is_file():
            print(f"[FAIL] frozen artifact missing: {relative}", flush=True)
            passed = False
            continue
        actual_blob = git_output("rev-parse", f"HEAD:{relative}")
        if actual_blob != expected_blob:
            print(
                f"[FAIL] frozen artifact changed: {relative} ({actual_blob} != {expected_blob})",
                flush=True,
            )
            passed = False
        else:
            print(f"[PASS] unchanged: {relative}", flush=True)
    return passed


def check_rf027_contract() -> bool:
    print("\n== RF-027 frozen preparation contract ==", flush=True)

    protocol_ok = require_markers(
        PROTOCOL,
        (
            "ATS2-RF-027",
            "PREPARATION_PROTOCOL_FROZEN",
            "https://www.bls.gov/bls/news-release/cpi.htm",
            "DUKASCOPY_HOURLY_TICK_BI5",
            "FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION",
            "READY_FOR_DATA_FEASIBILITY_FREEZE",
            "UNRESOLVED_OFFICIAL_EVENT_TIMES",
            "OFFICIAL_TIME_CROSSCHECK_MISMATCH",
            "INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            "ATS2-RF-028",
        ),
    )
    tool_ok = require_markers(
        TOOL,
        (
            'TASK_ID = "ATS2-RF-027"',
            'HYPOTHESIS_ID = "HYP-0006"',
            "https://www.bls.gov/bls/news-release/cpi.htm",
            'SOURCE_SYMBOL = "EURUSD"',
            "HYP0005_LEFT_START",
            "HYP0005_RIGHT_START",
            "required_tick_hours",
            "parse_archive_release_time",
            "decode_tick_object",
            "event_geometry",
            "outcome_metrics_computed",
            "primary_claim_evaluated",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        ),
    )
    test_ok = require_markers(
        TEST,
        (
            "test_parse_archive_index_extracts_release_dates",
            "test_parse_archive_release_time_handles_historical_edt",
            "test_et_conversion_uses_pre_and_post_2007_dst_rules",
            "test_schedule_entries_and_same_time_flags",
            "test_decode_tick_object_validates_coherent_bid_ask",
            "test_required_tick_hours_are_bounded_and_exclude_hyp0005",
            "test_event_geometry_uses_timestamps_only_and_requires_strict_pre_release",
            "test_geometry_output_schema_contains_no_price_or_outcome_fields",
            "test_preparation_decision_is_non_market_geometry_gate",
        ),
    )
    state_ok = require_markers(
        STATE,
        (
            'last_completed_task_id: "ATS2-RF-026"',
            'next_task_id: "ATS2-RF-027"',
            'current_task: "ATS2-RF-027"',
            'next_task: "ATS2-RF-028"',
            'rf026_verified_commit: "5e0ff9e4481e5dc28c14a73adcf32433715973a3"',
            'strategy_5_data_feasibility_prep_status: "RF027_PROTOCOL_FROZEN_PENDING_OWNER_PREPARATION"',
            'strategy_5_data_feasibility_prep_decision: "PENDING_OWNER_RUNTIME"',
            "strategy_5_required_protected_hyp0005_source_requests: 0",
            "strategy_5_outcome_computed: false",
            'strategy_5_information_boundary: "NO_HYPOTHESIS_OUTCOME_COMPUTED"',
            'strategy_4_information_boundary: "NO_CONFIRMATORY_OUTCOME_COMPUTED"',
        ),
    )
    backlog_ok = require_markers(
        BACKLOG,
        (
            "ATS2-RF-026",
            "DONE / PASS",
            "ATS2-RF-027",
            "ATS2-RF-028",
            "HYP-0006 Data Feasibility preparation",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        ),
    )
    docs_ok = all(
        (
            require_markers(
                HANDOFF,
                (
                    "ATS2-RF-027",
                    "HYP-0006-DATA-FEASIBILITY-PREP.md",
                    "NO_HYPOTHESIS_OUTCOME_COMPUTED",
                    "NO_CONFIRMATORY_OUTCOME_COMPUTED",
                ),
            ),
            require_markers(
                NEXT_STEP,
                (
                    "ATS2-RF-027",
                    "ATS2-RF-028",
                    "agent/rf027-hyp0006-data-feasibility-prep",
                    "NO_HYPOTHESIS_OUTCOME_COMPUTED",
                ),
            ),
            require_markers(
                STATUS,
                (
                    "ATS2-RF-027",
                    "NO_HYPOTHESIS_OUTCOME_COMPUTED",
                    "NO_CONFIRMATORY_OUTCOME_COMPUTED",
                ),
            ),
        )
    )

    return all(
        (
            protocol_ok,
            tool_ok,
            test_ok,
            state_ok,
            backlog_ok,
            docs_ok,
            check_frozen_lineage(),
        )
    )


def validate_geometry_csv(payload: dict[str, Any]) -> bool:
    path = ROOT / GEOMETRY_CSV
    if not path.is_file():
        print("[FAIL] RF-027 geometry CSV missing", flush=True)
        return False

    expected_digest = payload.get("geometry_csv_sha256")
    if not isinstance(expected_digest, str) or not SHA256_RE.fullmatch(expected_digest):
        print("[FAIL] invalid RF-027 geometry CSV SHA-256 field", flush=True)
        return False
    if sha256_file(path) != expected_digest:
        print("[FAIL] RF-027 geometry CSV SHA-256 mismatch", flush=True)
        return False

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = tuple(next(reader, []))

    if header != EXPECTED_GEOMETRY_HEADER:
        print(f"[FAIL] RF-027 geometry header mismatch: {header}", flush=True)
        return False

    lowered = {name.lower() for name in header}
    for field in PROHIBITED_OUTCOME_FIELDS:
        if field in lowered:
            print(f"[FAIL] prohibited field in RF-027 geometry CSV: {field}", flush=True)
            return False

    print("[PASS] RF-027 geometry CSV identity and outcome-free schema", flush=True)
    return True


def validate_local_result(payload: dict[str, Any], commit: str) -> bool:
    print("\n== RF-027 machine preparation result ==", flush=True)
    passed = True

    exact_pairs: tuple[tuple[str, Any], ...] = (
        ("task_id", TASK_ID),
        ("hypothesis_id", "HYP-0006"),
        ("git_commit", commit),
        ("evidence_classification", "DEVELOPMENT_EXPLORATORY_ONLY"),
        ("event_inventory_source", "BLS_CPI_ARCHIVE_INDEX"),
        ("quote_source", "DUKASCOPY_HOURLY_TICK_BI5"),
        ("protected_hyp0005_source_requests", 0),
        ("outcome_metrics_computed", False),
        ("primary_claim_evaluated", False),
        ("information_boundary", "NO_HYPOTHESIS_OUTCOME_COMPUTED"),
    )
    for key, expected in exact_pairs:
        if payload.get(key) != expected:
            print(
                f"[FAIL] RF-027 result field {key}: {payload.get(key)!r} != {expected!r}",
                flush=True,
            )
            passed = False

    decision = payload.get("preparation_decision")
    if decision not in ALLOWED_DECISIONS:
        print(f"[FAIL] invalid RF-027 preparation decision: {decision}", flush=True)
        passed = False

    count_keys = (
        "candidate_event_count",
        "resolved_event_time_count",
        "unresolved_event_time_count",
        "schedule_match_count",
        "schedule_mismatch_count",
        "same_time_bls_cluster_count",
        "requested_tick_object_count",
        "acquired_tick_object_count",
        "missing_tick_object_count",
        "complete_timestamp_geometry_event_count",
    )
    for key in count_keys:
        value = payload.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            print(f"[FAIL] invalid non-negative count {key}: {value!r}", flush=True)
            passed = False

    candidate_count = payload.get("candidate_event_count")
    resolved_count = payload.get("resolved_event_time_count")
    unresolved_count = payload.get("unresolved_event_time_count")
    if (
        isinstance(candidate_count, int)
        and isinstance(resolved_count, int)
        and isinstance(unresolved_count, int)
        and candidate_count != resolved_count + unresolved_count
    ):
        print("[FAIL] RF-027 event denominator does not reconcile", flush=True)
        passed = False

    source_digest = payload.get("source_bundle_sha256")
    if not isinstance(source_digest, str) or not SHA256_RE.fullmatch(source_digest):
        print("[FAIL] invalid RF-027 source bundle SHA-256", flush=True)
        passed = False

    expected_path = str(GEOMETRY_CSV).replace("\\", "/")
    if payload.get("geometry_csv_relative_path") != expected_path:
        print("[FAIL] unexpected RF-027 geometry CSV path", flush=True)
        passed = False

    for forbidden in (
        "pre_abs_60m_return",
        "post_abs_60m_return",
        "primary_inequality",
        "trading_pnl",
    ):
        if forbidden in payload:
            print(f"[FAIL] prohibited outcome key in RF-027 result: {forbidden}", flush=True)
            passed = False

    if not validate_geometry_csv(payload):
        passed = False

    if passed:
        print(f"[PASS] RF-027 preparation result: {decision}", flush=True)
    return passed


def prepare_or_validate(commit: str) -> bool:
    existing: dict[str, Any] | None = None
    result_path = ROOT / LOCAL_RESULT
    if result_path.is_file():
        try:
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            loaded = None
        if isinstance(loaded, dict) and loaded.get("git_commit") == commit:
            existing = loaded

    if existing is None:
        if not run(
            "RF-027 HYP-0006 official-event and tick geometry preparation",
            [sys.executable, str(TOOL)],
        ):
            return False
        try:
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[FAIL] cannot load RF-027 result: {exc}", flush=True)
            return False
        if not isinstance(loaded, dict):
            print("[FAIL] RF-027 result is not a JSON object", flush=True)
            return False
        existing = loaded
    else:
        print(
            "\nExisting exact-commit RF-027 local preparation result found; validating.",
            flush=True,
        )

    return validate_local_result(existing, commit)


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    branch = git_output("branch", "--show-current")
    commit = git_output("rev-parse", "HEAD")
    print(f"Branch: {branch or '<detached>'}")
    print(f"Commit: {commit}")

    emit_progress(35)
    staged = check_rf027_contract()

    emit_progress(50)
    governance = run(
        "RF-027 repository governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(65)
    full_ci = run(
        "full ATS Local CI before RF-027 source preparation",
        [sys.executable, "tools/verify_repo.py"],
    )

    if not all((staged, governance, full_ci)):
        print("\nHYP-0005 outcome computed by RF-027: NO", flush=True)
        print("HYP-0006 outcome computed by RF-027: NO", flush=True)
        print("\nATS CURRENT TASK CHECK: FAIL", flush=True)
        return 1

    emit_progress(80)
    prepared = prepare_or_validate(commit)

    if prepared:
        emit_progress(100)

    print("\nHYP-0005 outcome computed by RF-027: NO", flush=True)
    print("HYP-0006 outcome computed by RF-027: NO", flush=True)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if prepared else 'FAIL'}", flush=True)
    return 0 if prepared else 1


if __name__ == "__main__":
    raise SystemExit(main())
