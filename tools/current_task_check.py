#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-006"
TASK_NAME = "HYP-0003 Data Feasibility preparation"
REQUIRED_ARTIFACTS = (
    Path("research/reviews/HYP-0003-DATA-FEASIBILITY.md"),
    Path("research/reviews/HYP-0003-DATA-FEASIBILITY-PREP.md"),
    Path("tools/hyp0003_data_feasibility.py"),
    Path("tests/test_hyp0003_data_feasibility.py"),
)


def check_required_artifacts() -> bool:
    print("\n== RF-006 HYP-0003 Data Feasibility preparation artifacts ==")
    missing = [str(path) for path in REQUIRED_ARTIFACTS if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing required artifact: {path}")
        return False
    print("[PASS] RF-006 HYP-0003 Data Feasibility preparation artifacts")
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

    pre_probe = [
        check_required_artifacts(),
        run(
            "RF-006 HYP-0003 preparation governance validation",
            [sys.executable, "tools/validate_repo.py"],
        ),
        run("full ATS Local CI before source probe", [sys.executable, "tools/verify_repo.py"]),
    ]
    if not all(pre_probe):
        print("\nATS CURRENT TASK CHECK: FAIL")
        return 1

    probe = run(
        "RF-006 HYP-0003 source availability probe",
        [sys.executable, "tools/hyp0003_data_feasibility.py"],
    )
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if probe else 'FAIL'}")
    return 0 if probe else 1


if __name__ == "__main__":
    raise SystemExit(main())
