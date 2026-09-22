#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-M6-006"
TASK_NAME = "HYP-0002 PROTO-01 freeze"
REQUIRED_ARTIFACTS = (
    Path("research/reviews/HYP-0002-PROTOTYPE-01.md"),
    Path("tools/hyp0002_proto01.py"),
    Path("tests/test_hyp0002_proto01.py"),
)


def check_required_artifacts() -> bool:
    print("\n== M6-006 HYP-0002 PROTO-01 freeze artifacts ==")
    missing = [str(path) for path in REQUIRED_ARTIFACTS if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing required artifact: {path}")
        return False
    print("[PASS] M6-006 HYP-0002 PROTO-01 freeze artifacts")
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
            "M6-006 HYP-0002 PROTO-01 freeze governance validation",
            [sys.executable, "tools/validate_repo.py"],
        ),
        run("full ATS Local CI", [sys.executable, "tools/verify_repo.py"]),
    ]
    overall = all(results)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if overall else 'FAIL'}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
