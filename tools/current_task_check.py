#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-016"
TASK_NAME = "HYP-0004 Data Feasibility"
REVIEW = Path("research/reviews/HYP-0004-DATA-FEASIBILITY.md")
PREPARATION = Path("research/reviews/HYP-0004-DEVELOPMENT-DATA-PREP.md")


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def check_review() -> bool:
    print("\n== RF-016 HYP-0004 Data Feasibility artifact ==", flush=True)
    path = ROOT / REVIEW
    if not path.is_file():
        print(f"[FAIL] missing Data Feasibility review: {REVIEW}", flush=True)
        return False

    text = path.read_text(encoding="utf-8")
    markers = (
        "ATS2-RF-016",
        "Hypothesis ID: `HYP-0004`",
        "Review status: `CONDITIONAL`",
        "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001",
        "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2",
        "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001",
        "ask_open >= bid_open",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "Prototype authorization:",
        "`NOT_YET_AUTHORIZED`",
        "ATS2-RF-017 — HYP-0004 development data preparation",
    )
    for marker in markers:
        if marker not in text:
            print(f"[FAIL] HYP-0004 Data Feasibility marker missing: {marker}", flush=True)
            return False

    if (ROOT / PREPARATION).exists():
        print("[FAIL] RF-016 must not create the RF-017 preparation artifact", flush=True)
        return False

    print(
        "[PASS] RF-016 recorded CONDITIONAL feasibility without HYP-0004 outcome computation",
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
    review = check_review()

    emit_progress(65)
    governance = run(
        "RF-016 HYP-0004 Data Feasibility governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-016 HYP-0004 Data Feasibility",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((review, governance, full_ci))
    if passed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
