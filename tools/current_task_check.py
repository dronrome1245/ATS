#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-M6-007"
TASK_NAME = "HYP-0002 PROTO-01 reveal"
REQUIRED_ARTIFACTS = (
    Path("research/reviews/HYP-0002-PROTOTYPE-01.md"),
    Path("tools/hyp0002_proto01.py"),
    Path("tests/test_hyp0002_proto01.py"),
)


def check_required_artifacts() -> bool:
    print("\n== M6-007 HYP-0002 PROTO-01 frozen inputs ==")
    missing = [str(path) for path in REQUIRED_ARTIFACTS if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing required artifact: {path}")
        return False
    print("[PASS] M6-007 HYP-0002 PROTO-01 frozen inputs")
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

    pre_reveal = [
        check_required_artifacts(),
        run(
            "M6-007 HYP-0002 PROTO-01 reveal governance validation",
            [sys.executable, "tools/validate_repo.py"],
        ),
        run("full ATS Local CI before reveal", [sys.executable, "tools/verify_repo.py"]),
    ]
    if not all(pre_reveal):
        print("\nATS CURRENT TASK CHECK: FAIL")
        return 1

    revealed = run(
        "M6-007 HYP-0002 PROTO-01 frozen reveal",
        [sys.executable, "tools/hyp0002_proto01.py"],
    )
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if revealed else 'FAIL'}")
    return 0 if revealed else 1


if __name__ == "__main__":
    raise SystemExit(main())
