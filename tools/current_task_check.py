#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-004"
TASK_NAME = "HYP-0003 formation"
REQUIRED_ARTIFACTS = (
    Path("research/ideas/IDEA-0003.md"),
    Path("research/hypotheses/HYP-0003.md"),
)


def check_required_artifacts() -> bool:
    print("\n== RF-004 HYP-0003 formation artifacts ==")
    missing = [str(path) for path in REQUIRED_ARTIFACTS if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing required artifact: {path}")
        return False
    print("[PASS] RF-004 HYP-0003 formation artifacts")
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
            "RF-004 HYP-0003 formation governance validation",
            [sys.executable, "tools/validate_repo.py"],
        ),
        run("full ATS Local CI", [sys.executable, "tools/verify_repo.py"]),
    ]
    overall = all(results)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if overall else 'FAIL'}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
