#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-012"
TASK_NAME = "Strategy #3 early-rejection closeout"
RESULT = Path("reports/research/HYP-0003-PROTOTYPE-01-result.json")
PROTO = Path("research/reviews/HYP-0003-PROTOTYPE-01.md")
CLOSEOUT = Path("governance/program/STRATEGY_3_CLOSEOUT.md")
EXPECTED_RESULT_SHA256 = "a1feee3d6495afdcc46f81ce0ee8e137896a77a3bd52de8baf6cbf53da1a7620"
EXPECTED_REVEAL_COMMIT = "f974b9bb60a6cc295cb8aaba4a263499c14769c0"


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


def load_result() -> dict[str, Any] | None:
    if not (ROOT / RESULT).is_file():
        print(f"[FAIL] canonical result missing: {RESULT}", flush=True)
        return None
    actual_sha = sha256_file(ROOT / RESULT)
    if actual_sha != EXPECTED_RESULT_SHA256:
        print(
            f"[FAIL] canonical result SHA256 mismatch: {actual_sha} != {EXPECTED_RESULT_SHA256}",
            flush=True,
        )
        return None
    try:
        payload = json.loads((ROOT / RESULT).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot load canonical result: {exc}", flush=True)
        return None
    if not isinstance(payload, dict):
        print("[FAIL] canonical result top level must be a mapping", flush=True)
        return None
    return payload


def check_closeout() -> bool:
    print("\n== RF-012 HYP-0003 terminal result / closeout ==", flush=True)
    payload = load_result()
    if payload is None:
        return False

    expected = {
        "schema_version": "hyp0003-proto01-result-1",
        "hypothesis_id": "HYP-0003",
        "prototype_sequence": "PROTO-01",
        "evidence_class": "EXPLORATORY_PROTOTYPE",
        "economic_label": "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
        "decision": "REJECT",
        "decision_reason": "ONE_OR_MORE_BROAD_REGION_CRITERIA_FAILED",
        "next_action": "STOP_HYP0003",
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            print(f"[FAIL] result mismatch for {key}: {payload.get(key)!r}", flush=True)
            return False

    run_context = payload.get("run_context")
    if not isinstance(run_context, dict) or run_context.get("git_commit") != EXPECTED_REVEAL_COMMIT:
        print("[FAIL] canonical result reveal commit mismatch", flush=True)
        return False

    cells = payload.get("cells")
    if not isinstance(cells, list) or len(cells) != 25:
        print("[FAIL] canonical result must retain all 25 cells", flush=True)
        return False

    breadth = payload.get("breadth")
    if not isinstance(breadth, dict):
        print("[FAIL] breadth summary missing", flush=True)
        return False
    breadth_checks = {
        "all_cells_observed": True,
        "median_cell_mean": -0.0013404354655954772,
        "median_positive": False,
        "positive_cell_count_pass": False,
        "positive_mean_cell_count": 8,
        "positive_formation_period_count": 4,
        "positive_holding_period_count": 4,
    }
    for key, value in breadth_checks.items():
        if breadth.get(key) != value:
            print(f"[FAIL] breadth mismatch for {key}: {breadth.get(key)!r}", flush=True)
            return False

    for path, markers in (
        (
            PROTO,
            (
                "COMPLETED / REJECT",
                "DEVELOPMENT_REVEALED_PROTOTYPE_REJECTED",
                EXPECTED_RESULT_SHA256,
                "STOP_HYP0003",
            ),
        ),
        (
            CLOSEOUT,
            (
                "REJECTED_AT_R3",
                EXPECTED_RESULT_SHA256,
                "NEGATIVE_EVIDENCE_PRESERVED_WITHOUT_RESCUE",
                "ATS2-RF-013 — Strategy #4 idea sourcing",
            ),
        ),
    ):
        text = (ROOT / path).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                print(f"[FAIL] {path} missing marker: {marker}", flush=True)
                return False

    print("[PASS] RF-012 canonical negative result and closeout", flush=True)
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
    closeout = check_closeout()

    emit_progress(65)
    governance = run(
        "RF-012 Strategy #3 closeout governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-012 Strategy #3 closeout",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((closeout, governance, full_ci))
    if passed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
