#!/usr/bin/env python3
"""Run the verification package for ATS2-RF-028."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-028"
TASK_NAME = "HYP-0006 pre-reveal data/tolerance freeze"

FREEZE_REVIEW = Path("research/reviews/HYP-0006-DATA-TOLERANCE-FREEZE.md")
FREEZE_TOOL = Path("tools/hyp0006_data_tolerance_freeze.py")
FREEZE_TEST = Path("tests/test_hyp0006_data_tolerance_freeze.py")
STATE = Path("03_СОСТОЯНИЕ_ПРОЕКТА.yaml")
BACKLOG = Path("governance/backlog/PROGRAM_BACKLOG_V2.md")
HANDOFF = Path("AI_HANDOFF.md")
NEXT_STEP = Path("02_СЛЕДУЮЩИЙ_ШАГ.md")
STATUS = Path("01_СТАТУС_ПРОЕКТА.md")

RF027_RESULT = Path("reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP.json")
GEOMETRY_CSV = Path("data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv")
LOCAL_RESULT = Path("reports/local_ci/HYP0006_DATA_TOLERANCE_FREEZE.json")

RF027_COMMIT = "bbbdbd301b610dfc61316c9ff82015fb0e039a47"
EXPECTED_SOURCE_BUNDLE_SHA256 = "5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425"
EXPECTED_GEOMETRY_SHA256 = "e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034"
EXPECTED_BLS_MANIFEST_SHA256 = "3837c463b36914c2276e9985a8a70a8ead13ca0e4b16901a22cb4fd2dece6ee4"
EXPECTED_BLS_BUNDLE_SHA256 = "5306799d4c4196941d701e661df2fa4255682783b966e7bcfd69f702a1ead341"
EXPECTED_BLS_CALENDAR_SHA256 = "646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9"
EXPECTED_EVENT_COUNT = 217
BOUNDARY_MAX_ABS_GAP_MS = 30_000
PRE_RELEASE_MAX_STALENESS_MS = 30_000

FROZEN_BLOBS = {
    "research/hypotheses/HYP-0005.md": "ebbbc89187c911485c1568dc11f5f2f9e703718a",
    "research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md": (
        "c15b2b67700dd46fc592f1208731ce6b42f6905c"
    ),
    "tools/hyp0005_data_feasibility.py": "310b23213876304ade674ef36ba17ce6d457353f",
    "tests/test_hyp0005_data_feasibility.py": "12697882da682eab699bf5b7debd7c358e56aca9",
    "research/hypotheses/HYP-0006.md": "6b3f260ceacd98adf7a6aa44205404e68e4fd4ca",
    "research/reviews/HYP-0006-DATA-FEASIBILITY.md": "ae58099a05daec4be385c18177c74f1f22d1eb30",
}


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def git_output(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_markers(path: Path, markers: tuple[str, ...]) -> bool:
    full_path = ROOT / path
    if not full_path.is_file():
        print(f"[FAIL] missing RF-028 artifact: {path}", flush=True)
        return False
    content = full_path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in content:
            print(f"[FAIL] RF-028 marker missing in {path}: {marker}", flush=True)
            return False
    return True


def check_frozen_lineage() -> bool:
    print("\n== RF-028 frozen HYP-0005/HYP-0006 lineage ==", flush=True)
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


def check_rf028_contract() -> bool:
    print("\n== RF-028 pre-reveal freeze contract ==", flush=True)
    checks = (
        require_markers(
            FREEZE_REVIEW,
            (
                "ATS2-RF-028",
                "15/22",
                "bbbdbd301b610dfc61316c9ff82015fb0e039a47",
                "READY_FOR_DATA_FEASIBILITY_FREEZE",
                "DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001@1.0.0",
                "5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425",
                "e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034",
                "NEAREST_TO_T_MINUS_60M_WITHIN_30000MS_TIE_PREVIOUS",
                "LAST_QUOTE_STRICTLY_BEFORE_RELEASE_MAX_STALENESS_30000MS",
                "NEAREST_TO_T_PLUS_60M_WITHIN_30000MS_TIE_PREVIOUS",
                "LAST_RAW_RECORD_AT_SELECTED_MILLISECOND",
                "BID_AND_ASK_FROM_SAME_RAW_TICK_RECORD",
                "EXCLUDE_EVENT_IF_ANY_REQUIRED_ANCHOR_FAILS_FROZEN_GAP_RULE",
                "FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION",
                "FREEZE_DATA_AND_TOLERANCES",
                "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            ),
        ),
        require_markers(
            FREEZE_TOOL,
            (
                'TASK_ID = "ATS2-RF-028"',
                'RF027_COMMIT = "bbbdbd301b610dfc61316c9ff82015fb0e039a47"',
                "BOUNDARY_MAX_ABS_GAP_MS = 30_000",
                "PRE_RELEASE_MAX_STALENESS_MS = 30_000",
                'BOUNDARY_TIE_BREAK = "PREVIOUS_ON_EQUAL_GAP"',
                'DUPLICATE_TIMESTAMP_TIE_BREAK = "LAST_RAW_RECORD_AT_SELECTED_MILLISECOND"',
                'PRE_RELEASE_RULE = "LAST_QUOTE_STRICTLY_BEFORE_RELEASE"',
                'PRICE_PAIRING_RULE = "BID_AND_ASK_FROM_SAME_RAW_TICK_RECORD"',
                "FREEZE_DATA_AND_TOLERANCES",
                '"outcome_metrics_computed": False',
                '"primary_claim_evaluated": False',
                "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            ),
        ),
        require_markers(
            FREEZE_TEST,
            (
                "test_numeric_tolerances_are_frozen_before_reveal",
                "test_nearest_anchor_tie_break_prefers_previous",
                "test_geometry_at_frozen_limits_is_eligible",
                "test_geometry_above_any_frozen_limit_is_excluded",
                "test_incomplete_or_missing_source_geometry_is_excluded",
                "test_freeze_contract_contains_no_market_outcome_calculation",
            ),
        ),
        require_markers(
            STATE,
            (
                'last_completed_task_id: "ATS2-RF-027"',
                'next_task_id: "ATS2-RF-028"',
                'current_task: "ATS2-RF-028"',
                'current_ready_task: "ATS2-RF-028"',
                'strategy_5_data_feasibility_prep_status: "RF027_EXACT_MAIN_PASS"',
                'strategy_5_data_feasibility_prep_decision: "READY_FOR_DATA_FEASIBILITY_FREEZE"',
                'rf027_verified_commit: "bbbdbd301b610dfc61316c9ff82015fb0e039a47"',
                'strategy_5_data_tolerance_freeze_status: "RF028_STAGED_PRE_REVEAL"',
                "strategy_5_anchor_boundary_max_abs_gap_ms: 30000",
                "strategy_5_pre_release_max_staleness_ms: 30000",
                'strategy_5_information_boundary: "NO_HYPOTHESIS_OUTCOME_COMPUTED"',
            ),
        ),
        require_markers(
            BACKLOG,
            (
                "ATS2-RF-027",
                "DONE / PASS",
                "ATS2-RF-028",
                "READY",
                "bbbdbd301b610dfc61316c9ff82015fb0e039a47",
                "READY_FOR_DATA_FEASIBILITY_FREEZE",
                "30,000 ms",
                "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            ),
        ),
        require_markers(
            HANDOFF,
            (
                "ATS2-RF-028",
                "15/22",
                "bbbdbd301b610dfc61316c9ff82015fb0e039a47",
                "READY_FOR_DATA_FEASIBILITY_FREEZE",
                "30,000 ms",
                "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            ),
        ),
        require_markers(
            NEXT_STEP,
            (
                "15/22",
                "ATS2-RF-028",
                "tools/hyp0006_data_tolerance_freeze.py",
                "30,000 ms",
                "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            ),
        ),
        require_markers(
            STATUS,
            (
                "15/22",
                "ATS2-RF-028",
                "READY_FOR_DATA_FEASIBILITY_FREEZE",
                "1085 / 1085",
                "217 / 217",
                "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            ),
        ),
    )
    return all(checks)


def validate_result(payload: dict[str, Any], commit: str) -> bool:
    checks: dict[str, Any] = {
        "schema_version": "hyp0006-data-tolerance-freeze-1",
        "task_id": TASK_ID,
        "hypothesis_id": "HYP-0006",
        "git_commit": commit,
        "rf027_git_commit": RF027_COMMIT,
        "dataset_id": "DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001",
        "dataset_version": "1.0.0",
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
        "boundary_tie_break": "PREVIOUS_ON_EQUAL_GAP",
        "pre_release_rule": "LAST_QUOTE_STRICTLY_BEFORE_RELEASE",
        "duplicate_timestamp_tie_break": "LAST_RAW_RECORD_AT_SELECTED_MILLISECOND",
        "price_pairing_rule": "BID_AND_ASK_FROM_SAME_RAW_TICK_RECORD",
        "same_time_event_policy": "FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION",
        "missing_data_policy": "EXCLUDE_EVENT_IF_ANY_REQUIRED_ANCHOR_FAILS_FROZEN_GAP_RULE",
        "freeze_decision": "FREEZE_DATA_AND_TOLERANCES",
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    }
    passed = True
    for key, expected in checks.items():
        actual = payload.get(key)
        if actual != expected:
            print(
                f"[FAIL] RF-028 result mismatch for {key}: {actual!r} != {expected!r}",
                flush=True,
            )
            passed = False

    eligible = payload.get("eligible_event_count")
    ineligible = payload.get("ineligible_event_count")
    if not isinstance(eligible, int) or eligible <= 0:
        print("[FAIL] RF-028 eligible_event_count must be positive", flush=True)
        passed = False
    if not isinstance(ineligible, int) or ineligible < 0:
        print("[FAIL] RF-028 ineligible_event_count invalid", flush=True)
        passed = False
    if isinstance(eligible, int) and isinstance(ineligible, int):
        if eligible + ineligible != EXPECTED_EVENT_COUNT:
            print("[FAIL] RF-028 event denominator does not reconcile to 217", flush=True)
            passed = False

    eligible_ids = payload.get("eligible_event_ids")
    ineligible_events = payload.get("ineligible_events")
    if not isinstance(eligible_ids, list) or len(eligible_ids) != eligible:
        print("[FAIL] RF-028 eligible_event_ids length mismatch", flush=True)
        passed = False
        eligible_ids = []
    if not isinstance(ineligible_events, list) or len(ineligible_events) != ineligible:
        print("[FAIL] RF-028 ineligible_events length mismatch", flush=True)
        passed = False
        ineligible_events = []

    if len(set(eligible_ids)) != len(eligible_ids):
        print("[FAIL] RF-028 duplicate eligible event IDs", flush=True)
        passed = False

    ineligible_ids = [
        item.get("event_id")
        for item in ineligible_events
        if isinstance(item, dict) and isinstance(item.get("event_id"), str)
    ]
    if len(ineligible_ids) != len(ineligible_events):
        print("[FAIL] RF-028 malformed ineligible event identity", flush=True)
        passed = False
    if len(set(ineligible_ids)) != len(ineligible_ids):
        print("[FAIL] RF-028 duplicate ineligible event IDs", flush=True)
        passed = False
    if set(eligible_ids) & set(ineligible_ids):
        print("[FAIL] RF-028 eligible/ineligible event overlap", flush=True)
        passed = False
    if len(set(eligible_ids) | set(ineligible_ids)) != EXPECTED_EVENT_COUNT:
        print("[FAIL] RF-028 frozen event-ID denominator does not equal 217", flush=True)
        passed = False

    geometry_evaluations = payload.get("geometry_evaluations")
    if (
        not isinstance(geometry_evaluations, list)
        or len(geometry_evaluations) != EXPECTED_EVENT_COUNT
    ):
        print("[FAIL] RF-028 geometry_evaluations length mismatch", flush=True)
        passed = False
    else:
        evaluation_ids = [
            item.get("event_id")
            for item in geometry_evaluations
            if isinstance(item, dict) and isinstance(item.get("event_id"), str)
        ]
        if (
            len(evaluation_ids) != EXPECTED_EVENT_COUNT
            or len(set(evaluation_ids)) != EXPECTED_EVENT_COUNT
        ):
            print("[FAIL] RF-028 geometry evaluation identities invalid", flush=True)
            passed = False
        elif set(evaluation_ids) != (set(eligible_ids) | set(ineligible_ids)):
            print("[FAIL] RF-028 geometry evaluations do not match frozen denominator", flush=True)
            passed = False

    for forbidden in (
        "pre_abs_60m_return",
        "post_abs_60m_return",
        "primary_inequality",
        "trading_pnl",
    ):
        if forbidden in payload:
            print(f"[FAIL] prohibited outcome key in RF-028 result: {forbidden}", flush=True)
            passed = False

    if not (ROOT / RF027_RESULT).is_file():
        print("[FAIL] exact RF-027 local result missing", flush=True)
        passed = False
    if not (ROOT / GEOMETRY_CSV).is_file():
        print("[FAIL] exact RF-027 geometry CSV missing", flush=True)
        passed = False
    elif sha256_file(ROOT / GEOMETRY_CSV) != EXPECTED_GEOMETRY_SHA256:
        print("[FAIL] exact RF-027 geometry CSV hash changed", flush=True)
        passed = False

    if passed:
        print(
            f"[PASS] RF-028 froze {eligible}/{EXPECTED_EVENT_COUNT} eligible events "
            "without HYP-0006 outcome computation",
            flush=True,
        )
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
            "RF-028 HYP-0006 pre-reveal data/tolerance freeze",
            [sys.executable, str(FREEZE_TOOL)],
        ):
            return False
        try:
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[FAIL] cannot load RF-028 result: {exc}", flush=True)
            return False
        if not isinstance(loaded, dict):
            print("[FAIL] RF-028 result is not a JSON object", flush=True)
            return False
        existing = loaded
    else:
        print("\nExisting exact-commit RF-028 local result found; validating.", flush=True)

    return validate_result(existing, commit)


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    branch = git_output("branch", "--show-current")
    commit = git_output("rev-parse", "HEAD")
    print(f"Branch: {branch or '<detached>'}")
    print(f"Commit: {commit}")

    emit_progress(30)
    contract = check_rf028_contract()

    emit_progress(45)
    lineage = check_frozen_lineage()

    emit_progress(60)
    governance = run(
        "RF-028 repository governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(75)
    full_ci = run(
        "full ATS Local CI before RF-028 freeze execution",
        [sys.executable, "tools/verify_repo.py"],
    )

    if not all((contract, lineage, governance, full_ci)):
        print("\nHYP-0006 outcome computed by RF-028: NO", flush=True)
        print("\nATS CURRENT TASK CHECK: FAIL", flush=True)
        return 1

    emit_progress(85)
    frozen = prepare_or_validate(commit)
    if frozen:
        emit_progress(100)

    print("\nHYP-0006 outcome computed by RF-028: NO", flush=True)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if frozen else 'FAIL'}", flush=True)
    return 0 if frozen else 1


if __name__ == "__main__":
    raise SystemExit(main())
