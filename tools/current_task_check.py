#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-019"
TASK_NAME = "HYP-0004 PROTO-01 freeze"
PROTO_ARTIFACT = Path("research/reviews/HYP-0004-PROTOTYPE-01.md")
RUNNER = Path("tools/hyp0004_proto01.py")
RUNNER_TEST = Path("tests/test_hyp0004_proto01.py")
DATA_FEASIBILITY = Path("research/reviews/HYP-0004-DATA-FEASIBILITY.md")
MANIFEST = Path("data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001.yaml")
EXPECTED_RUNNER_GIT_BLOB = "1bf672db5e27dab80ffc217b9ab8bc76de25b6f5"
FORBIDDEN_RESULTS = (
    Path("reports/local_ci/HYP0004_PROTO01_RESULT.json"),
    Path("reports/local_ci/HYP0004_PROTO01_RESULT_REPORT.txt"),
    Path("reports/research/HYP-0004-PROTOTYPE-01-result.json"),
)


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def git_output(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def check_frozen_protocol() -> bool:
    print("\n== RF-019 HYP-0004 PROTO-01 frozen protocol ==", flush=True)
    required = (PROTO_ARTIFACT, RUNNER, RUNNER_TEST, DATA_FEASIBILITY, MANIFEST)
    missing = [str(path) for path in required if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing required artifact: {path}", flush=True)
        return False

    present_results = [str(path) for path in FORBIDDEN_RESULTS if (ROOT / path).exists()]
    if present_results:
        for path in present_results:
            print(f"[FAIL] RF-019 must not reveal HYP-0004 outcome: {path}", flush=True)
        return False

    runner_blob = git_output("rev-parse", f"HEAD:{RUNNER.as_posix()}")
    if runner_blob != EXPECTED_RUNNER_GIT_BLOB:
        print(
            f"[FAIL] frozen runner git blob mismatch: {runner_blob} != {EXPECTED_RUNNER_GIT_BLOB}",
            flush=True,
        )
        return False

    prototype = (ROOT / PROTO_ARTIFACT).read_text(encoding="utf-8")
    required_markers = (
        "FROZEN / NOT_REVEALED",
        "median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)",
        "median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)",
        "BOTH_PRIMARY_INEQUALITIES_MET",
        "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED",
        "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "ATS2-RF-020 — HYP-0004 PROTO-01 reveal",
    )
    for marker in required_markers:
        if marker not in prototype:
            print(f"[FAIL] frozen prototype marker missing: {marker}", flush=True)
            return False

    runner = (ROOT / RUNNER).read_text(encoding="utf-8")
    runner_markers = (
        "EXPECTED_DATASET_SHA256",
        "EXPECTED_ELIGIBLE = 111_938",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "movement_inequality_pass",
        "spread_inequality_pass",
        "both_primary_inequalities_pass",
        "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
        "HYP0004_PROTO01_RESULT.json",
    )
    for marker in runner_markers:
        if marker not in runner:
            print(f"[FAIL] frozen runner marker missing: {marker}", flush=True)
            return False

    print(
        "[PASS] RF-019 froze HYP-0004 PROTO-01 without revealing development outcomes",
        flush=True,
    )
    return True


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    commit = git_output("rev-parse", "HEAD")
    print(f"Commit: {commit}")

    emit_progress(45)
    frozen = check_frozen_protocol()

    emit_progress(65)
    governance = run(
        "RF-019 HYP-0004 PROTO-01 freeze governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-019 HYP-0004 PROTO-01 freeze",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((frozen, governance, full_ci))
    if passed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
