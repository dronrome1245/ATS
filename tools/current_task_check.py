#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-007"
TASK_NAME = "HYP-0003 Data Feasibility freeze"
RESULT_PATH = Path("reports/research/HYP-0003-DATA-FEASIBILITY-PREP-result.json")
REQUIRED_ARTIFACTS = (
    Path("research/reviews/HYP-0003-DATA-FEASIBILITY.md"),
    Path("research/reviews/HYP-0003-DATA-FEASIBILITY-PREP.md"),
    RESULT_PATH,
    Path("tools/hyp0003_data_feasibility.py"),
    Path("tests/test_hyp0003_data_feasibility.py"),
)

EXPECTED_RESULT = {
    "task_id": "ATS2-RF-006",
    "hypothesis_id": "HYP-0003",
    "preparation_commit": "acf197d5774116c7d9a8b742eab77c6ee3447214",
    "launcher_status": "PASS",
    "source_probe_status": "PASS",
    "preparation_decision": "READY_FOR_FREEZE_REVIEW",
    "retained_currency_count": 9,
    "minimum_required_currency_count": 6,
    "common_possible_development_start": "2003-08-03T21:00:00Z",
    "development_end_exclusive": "2021-09-01T00:00:00Z",
    "history_metadata_sha256": ("215ad432126018f4f871a1e10bc3f315524b84ae29d83fc3fd3adc188107417d"),
    "probe_bundle_sha256": ("a88add123fd42e83396ba17de13cf65fedf18d8e0a5e1eca476ed6338c91b45e"),
    "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
}
EXPECTED_CURRENCIES = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NOK", "NZD", "SEK"]


def check_required_artifacts() -> bool:
    print("\n== RF-007 HYP-0003 Data Feasibility freeze artifacts ==", flush=True)
    missing = [str(path) for path in REQUIRED_ARTIFACTS if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing required artifact: {path}")
        return False
    print("[PASS] RF-007 HYP-0003 Data Feasibility freeze artifacts", flush=True)
    return True


def check_canonical_preparation_result() -> bool:
    print("\n== RF-007 canonical RF-006 preparation result ==", flush=True)
    try:
        payload = json.loads((ROOT / RESULT_PATH).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot load canonical preparation result: {exc}", flush=True)
        return False

    for key, expected in EXPECTED_RESULT.items():
        actual = payload.get(key)
        if actual != expected:
            print(
                f"[FAIL] canonical preparation result mismatch for {key}: "
                f"{actual!r} != {expected!r}",
                flush=True,
            )
            return False

    if payload.get("retained_source_currencies") != EXPECTED_CURRENCIES:
        print("[FAIL] canonical retained currency order/set mismatch", flush=True)
        return False

    symbol_results = payload.get("symbol_results")
    if not isinstance(symbol_results, list) or len(symbol_results) != 9:
        print("[FAIL] canonical symbol result count must be 9", flush=True)
        return False
    if any(item.get("status") != "SOURCE_AVAILABLE" for item in symbol_results):
        print("[FAIL] every frozen source symbol must be SOURCE_AVAILABLE", flush=True)
        return False

    print("[PASS] RF-007 canonical RF-006 preparation result", flush=True)
    return True


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


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
    artifacts = check_required_artifacts()

    emit_progress(55)
    canonical_result = check_canonical_preparation_result()

    emit_progress(65)
    governance = run(
        "RF-007 HYP-0003 freeze governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(75)
    full_ci = run(
        "full ATS Local CI for RF-007 freeze",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((artifacts, canonical_result, governance, full_ci))
    if passed:
        emit_progress(100)
    print(
        f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}",
        flush=True,
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
