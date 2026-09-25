#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-013"
TASK_NAME = "Strategy #4 idea sourcing"
SOURCING = Path("governance/program/STRATEGY_4_IDEA_SOURCING.md")


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def check_sourcing() -> bool:
    print("\n== RF-013 Strategy #4 sourcing artifact ==", flush=True)
    path = ROOT / SOURCING
    if not path.is_file():
        print(f"[FAIL] missing sourcing artifact: {SOURCING}", flush=True)
        return False

    text = path.read_text(encoding="utf-8")
    markers = (
        "ATS2-RF-013",
        "SOURCING_SHORTLIST_READY",
        "S4-FAM-01 - Currency carry / interest-rate differential",
        "S4-FAM-02 - Macroeconomic announcement response",
        "S4-FAM-03 - Intraday time/session effect",
        "S4-FAM-04 - Currency value / PPP / real-exchange-rate deviation",
        "S4-FAM-05 - Customer/order-flow prediction",
        "Families reviewed: `5`",
        "Immediate shortlist for RF-014 family selection: `4`",
        "No family is ranked.",
        "No family is selected.",
        "No strategy parameter is selected.",
        "ATS2-RF-014 - Strategy #4 family selection and Idea intake",
    )
    for marker in markers:
        if marker not in text:
            print(f"[FAIL] sourcing marker missing: {marker}", flush=True)
            return False

    if (ROOT / "research/ideas/IDEA-0004.md").exists():
        print("[FAIL] RF-013 must not create IDEA-0004", flush=True)
        return False

    print("[PASS] RF-013 bounded shortlist retained without winner selection", flush=True)
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
    sourcing = check_sourcing()

    emit_progress(65)
    governance = run(
        "RF-013 Strategy #4 sourcing governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-013 Strategy #4 sourcing",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((sourcing, governance, full_ci))
    if passed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
