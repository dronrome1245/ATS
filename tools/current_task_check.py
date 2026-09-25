#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-014"
TASK_NAME = "Strategy #4 family selection and Idea intake"
SELECTION = Path("governance/program/STRATEGY_4_FAMILY_SELECTION.md")
IDEA = Path("research/ideas/IDEA-0004.md")


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def check_selection() -> bool:
    print("\n== RF-014 Strategy #4 family selection / Idea Intake ==", flush=True)
    selection_path = ROOT / SELECTION
    idea_path = ROOT / IDEA
    if not selection_path.is_file():
        print(f"[FAIL] missing family-selection artifact: {SELECTION}", flush=True)
        return False
    if not idea_path.is_file():
        print(f"[FAIL] missing Idea artifact: {IDEA}", flush=True)
        return False

    selection = selection_path.read_text(encoding="utf-8")
    selection_markers = (
        "ATS2-RF-014",
        "S4-FAM-03 — INTRADAY_TIME_SESSION_EFFECT",
        "`SELECT`",
        "research/ideas/IDEA-0004.md",
        "`SCREEN`",
        "ATS2-RF-015 — HYP-0004 formation",
        "does not claim that an intraday/session effect is profitable",
        "No claim is made that any unselected family is inferior",
    )
    for marker in selection_markers:
        if marker not in selection:
            print(f"[FAIL] family-selection marker missing: {marker}", flush=True)
            return False

    idea = idea_path.read_text(encoding="utf-8")
    idea_markers = (
        "Idea ID: `IDEA-0004`",
        "Status: `SCREENING`",
        "CLOCK_SESSION_CONDITIONAL_FX_DISTRIBUTION_SHIFT",
        "Decision: `SCREEN`",
        "research/hypotheses/HYP-0004.md",
        "No directional sign, session boundary, instrument, bucket width, threshold or target magnitude is fixed by this Idea.",
    )
    for marker in idea_markers:
        if marker not in idea:
            print(f"[FAIL] IDEA-0004 marker missing: {marker}", flush=True)
            return False

    if (ROOT / "research/hypotheses/HYP-0004.md").exists():
        print("[FAIL] RF-014 must not create HYP-0004", flush=True)
        return False

    print(
        "[PASS] RF-014 selected one family and screened IDEA-0004 without parameter fixation",
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
    selection = check_selection()

    emit_progress(65)
    governance = run(
        "RF-014 Strategy #4 family-selection governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-014 Strategy #4 family selection",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((selection, governance, full_ci))
    if passed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
