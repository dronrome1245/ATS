#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-017"
TASK_NAME = "HYP-0004 development data preparation"
LOCAL_RESULT = Path("reports/local_ci/HYP0004_DEVELOPMENT_DATA.json")
REQUIRED_ARTIFACTS = (
    Path("research/reviews/HYP-0004-DATA-FEASIBILITY.md"),
    Path("research/reviews/HYP-0004-DEVELOPMENT-DATA-PREP.md"),
    Path("tools/hyp0004_development_data.py"),
    Path("tests/test_hyp0004_development_data.py"),
)
VALID_PREPARATION_DECISIONS = {
    "READY_FOR_DEVELOPMENT_DATA_FREEZE",
    "INSUFFICIENT_DEVELOPMENT_DATA",
}


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def check_required_artifacts() -> bool:
    print("\n== RF-017 HYP-0004 development data preparation artifacts ==", flush=True)
    missing = [str(path) for path in REQUIRED_ARTIFACTS if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing required artifact: {path}", flush=True)
        return False
    print("[PASS] RF-017 development data preparation artifacts", flush=True)
    return True


def check_local_preparation_result(commit: str) -> bool:
    print("\n== RF-017 local HYP-0004 development-data result ==", flush=True)
    try:
        payload = json.loads((ROOT / LOCAL_RESULT).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot load local preparation result: {exc}", flush=True)
        return False

    checks = {
        "task_id": TASK_ID,
        "hypothesis_id": "HYP-0004",
        "git_commit": commit,
        "parent_dataset_id": "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001",
        "parent_dataset_sha256": (
            "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2"
        ),
        "development_dataset_id": "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001",
        "development_dataset_version": "1.0.0",
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "duplicate_event_time_count": 0,
        "out_of_order_event_time_count": 0,
        "malformed_boundary_row_count": 0,
        "boundary_open_crossing_count": 0,
    }
    for key, expected in checks.items():
        actual = payload.get(key)
        if actual != expected:
            print(
                f"[FAIL] local preparation result mismatch for {key}: "
                f"{actual!r} != {expected!r}",
                flush=True,
            )
            return False

    decision = payload.get("preparation_decision")
    if decision not in VALID_PREPARATION_DECISIONS:
        print(f"[FAIL] invalid preparation decision: {decision!r}", flush=True)
        return False

    if not payload.get("derived_csv_sha256") or not payload.get("derived_row_count"):
        print("[FAIL] local result is missing derived dataset identity", flush=True)
        return False

    forbidden_keys = {
        "abs_next_1h_return",
        "relative_spread",
        "core_active_median_abs_return",
        "off_hours_median_abs_return",
        "core_active_median_relative_spread",
        "off_hours_median_relative_spread",
    }
    if forbidden_keys.intersection(payload):
        print("[FAIL] local preparation result contains HYP-0004 outcome metrics", flush=True)
        return False

    print(f"[PASS] RF-017 local preparation result ({decision})", flush=True)
    return True


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    print(f"Commit: {commit}")

    emit_progress(40)
    artifacts = check_required_artifacts()

    emit_progress(55)
    governance = run(
        "RF-017 HYP-0004 preparation governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(70)
    full_ci = run(
        "full ATS Local CI before RF-017 local data preparation",
        [sys.executable, "tools/verify_repo.py"],
    )

    if not all((artifacts, governance, full_ci)):
        print("\nATS CURRENT TASK CHECK: FAIL", flush=True)
        return 1

    emit_progress(80)
    prepared = run(
        "RF-017 HYP-0004 development-data preparation",
        [sys.executable, "tools/hyp0004_development_data.py"],
    )
    local_result = prepared and check_local_preparation_result(commit)

    if local_result:
        emit_progress(100)
    print(
        f"\nATS CURRENT TASK CHECK: {'PASS' if local_result else 'FAIL'}",
        flush=True,
    )
    return 0 if local_result else 1


if __name__ == "__main__":
    raise SystemExit(main())
