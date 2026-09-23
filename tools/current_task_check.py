#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-002"
TASK_NAME = "Strategy #3 idea sourcing"
REQUIRED_ARTIFACTS = (
    Path("governance/program/STRATEGY_3_SOURCING_REBASELINE.md"),
    Path("governance/program/STRATEGY_3_IDEA_SOURCING.md"),
)


def check_required_artifacts() -> bool:
    print("\n== RF-002 Strategy #3 idea sourcing artifacts ==")
    missing = [str(path) for path in REQUIRED_ARTIFACTS if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing required artifact: {path}")
        return False
    print("[PASS] RF-002 Strategy #3 idea sourcing artifacts")
    return True


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==")
    print("$ " + " ".join(command))
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    return passed


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

    results = [
        check_required_artifacts(),
        run(
            "RF-002 Strategy #3 idea sourcing governance validation",
            [sys.executable, "tools/validate_repo.py"],
        ),
        run("full ATS Local CI", [sys.executable, "tools/verify_repo.py"]),
    ]
    overall = all(results)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if overall else 'FAIL'}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
