#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-010"
TASK_NAME = "HYP-0003 PROTO-01 freeze"
PROTO = Path("research/reviews/HYP-0003-PROTOTYPE-01.md")
RUNNER = Path("tools/hyp0003_proto01.py")
TESTS = Path("tests/test_hyp0003_proto01.py")
DATA = Path("data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv")
EXPECTED_DATASET_SHA256 = "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def check_proto_freeze() -> bool:
    print("\n== RF-010 HYP-0003 PROTO-01 frozen artifacts ==", flush=True)
    required = (PROTO, RUNNER, TESTS, DATA)
    missing = [str(path) for path in required if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing required artifact: {path}", flush=True)
        return False

    proto_text = (ROOT / PROTO).read_text(encoding="utf-8")
    runner_text = (ROOT / RUNNER).read_text(encoding="utf-8")
    required_proto_markers = (
        "FROZEN_PRE_REVEAL",
        "25 / 25",
        "basket_size = max(1, ceil(eligible_currency_count / 6))",
        "PENDING_RF011_REVEAL",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "RF-011",
    )
    for marker in required_proto_markers:
        if marker not in proto_text:
            print(f"[FAIL] prototype freeze marker missing: {marker}", flush=True)
            return False

    for marker in (
        "FORMATION_MONTHS = (1, 3, 6, 9, 12)",
        "HOLDING_MONTHS = (1, 3, 6, 9, 12)",
        "select_baskets",
        "winner_long_return",
        "loser_short_return",
        "breadth_summary",
        "prototype_decision",
        "CREATE_NEW_CONFIRMATORY_HYPOTHESIS_BEFORE_R4",
    ):
        if marker not in runner_text:
            print(f"[FAIL] frozen runner marker missing: {marker}", flush=True)
            return False

    actual_sha = sha256_file(ROOT / DATA)
    if actual_sha != EXPECTED_DATASET_SHA256:
        print(f"[FAIL] frozen development CSV SHA256 mismatch: {actual_sha}", flush=True)
        return False

    print("[PASS] RF-010 frozen protocol/runner/tests and dataset identity", flush=True)
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
    artifacts = check_proto_freeze()

    emit_progress(65)
    governance = run(
        "RF-010 HYP-0003 PROTO-01 freeze governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-010 PROTO-01 freeze",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((artifacts, governance, full_ci))
    if passed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
