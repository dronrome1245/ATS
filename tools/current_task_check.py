#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-015"
TASK_NAME = "HYP-0004 formation"
HYPOTHESIS = Path("research/hypotheses/HYP-0004.md")
DATA_FEASIBILITY = Path("research/reviews/HYP-0004-DATA_FEASIBILITY.md")


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def check_hypothesis() -> bool:
    print("\n== RF-015 HYP-0004 formation artifact ==", flush=True)
    path = ROOT / HYPOTHESIS
    if not path.is_file():
        print(f"[FAIL] missing Hypothesis artifact: {HYPOTHESIS}", flush=True)
        return False

    text = path.read_text(encoding="utf-8")
    markers = (
        "HYP-0004",
        "IDEA-0004",
        "READY_FOR_DATA_FEASIBILITY",
        "CORE_ACTIVE",
        "TRANSITION",
        "OFF_HOURS",
        "EURUSD",
        "median(abs_next_1h_return | CORE_ACTIVE) > "
        "median(abs_next_1h_return | OFF_HOURS)",
        "median(relative_spread | CORE_ACTIVE) <= "
        "median(relative_spread | OFF_HOURS)",
        "DATA_FEASIBILITY",
        "No HYP-0004 outcome may be computed",
    )
    for marker in markers:
        if marker not in text:
            print(f"[FAIL] HYP-0004 marker missing: {marker}", flush=True)
            return False

    if (ROOT / DATA_FEASIBILITY).exists():
        print("[FAIL] RF-015 must not create the HYP-0004 Data Feasibility review", flush=True)
        return False

    print(
        "[PASS] RF-015 registered a bounded HYP-0004 before outcome inspection",
        flush=True,
    )
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

    emit_progress(45)
    hypothesis = check_hypothesis()

    emit_progress(65)
    governance = run(
        "RF-015 HYP-0004 formation governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-015 HYP-0004 formation",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((hypothesis, governance, full_ci))
    if passed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
