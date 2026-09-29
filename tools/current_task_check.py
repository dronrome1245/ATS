#!/usr/bin/env python3
"""Run the verification package for ATS2-RF-026 on exact main."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-026"
TASK_NAME = "HYP-0006 Data Feasibility"

HYPOTHESIS = Path("research/hypotheses/HYP-0006.md")
REVIEW = Path("research/reviews/HYP-0006-DATA-FEASIBILITY.md")
STATE = Path("03_СОСТОЯНИЕ_ПРОЕКТА.yaml")
BACKLOG = Path("governance/backlog/PROGRAM_BACKLOG_V2.md")
HANDOFF = Path("AI_HANDOFF.md")
NEXT_STEP = Path("02_СЛЕДУЮЩИЙ_ШАГ.md")
STATUS = Path("01_СТАТУС_ПРОЕКТА.md")

FROZEN_BLOBS = {
    "research/hypotheses/HYP-0005.md": "ebbbc89187c911485c1568dc11f5f2f9e703718a",
    "research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md": (
        "c15b2b67700dd46fc592f1208731ce6b42f6905c"
    ),
    "tools/hyp0005_data_feasibility.py": "310b23213876304ade674ef36ba17ce6d457353f",
    "tests/test_hyp0005_data_feasibility.py": "12697882da682eab699bf5b7debd7c358e56aca9",
    "research/hypotheses/HYP-0006.md": "6b3f260ceacd98adf7a6aa44205404e68e4fd4ca",
}

PROHIBITED_RF026_PATHS = (
    Path("research/reviews/HYP-0006-DATA-FEASIBILITY-PREP.md"),
    Path("data/manifests/DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001.yaml"),
    Path("data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv"),
    Path("tools/hyp0006_data_feasibility.py"),
    Path("tests/test_hyp0006_data_feasibility.py"),
    Path("reports/research/HYP-0006-DATA-FEASIBILITY-PREP-result.json"),
)


def git_output(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def require_markers(path: Path, markers: tuple[str, ...]) -> bool:
    full_path = ROOT / path
    if not full_path.is_file():
        print(f"[FAIL] missing RF-026 artifact: {path}", flush=True)
        return False
    content = full_path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in content:
            print(f"[FAIL] RF-026 marker missing in {path}: {marker}", flush=True)
            return False
    return True


def check_frozen_lineage() -> bool:
    print("\n== RF-026 frozen HYP-0005/HYP-0006 lineage ==", flush=True)
    passed = True
    for relative, expected_blob in FROZEN_BLOBS.items():
        path = ROOT / relative
        if not path.is_file():
            print(f"[FAIL] frozen artifact missing: {relative}", flush=True)
            passed = False
            continue
        actual_blob = git_output("rev-parse", f"HEAD:{relative}")
        if actual_blob != expected_blob:
            print(
                f"[FAIL] frozen artifact changed: {relative} ({actual_blob} != {expected_blob})",
                flush=True,
            )
            passed = False
        else:
            print(f"[PASS] unchanged: {relative}", flush=True)
    return passed


def check_no_premature_rf027_artifacts() -> bool:
    print("\n== HYP-0006 RF-026 information boundary ==", flush=True)
    found = [str(path) for path in PROHIBITED_RF026_PATHS if (ROOT / path).exists()]
    if found:
        for relative in found:
            print(
                f"[FAIL] RF-026 must not pre-create RF-027/outcome artifact: {relative}",
                flush=True,
            )
        return False
    print("[PASS] no RF-027 dataset/runner/result artifact exists", flush=True)
    return True


def check_rf026_contract() -> bool:
    print("\n== RF-026 conditional Data Feasibility contract ==", flush=True)

    review_ok = require_markers(
        REVIEW,
        (
            "Task: `ATS2-RF-026`",
            "Hypothesis ID: `HYP-0006`",
            "Review status: `CONDITIONAL`",
            "U.S. Bureau of Labor Statistics",
            "Dukascopy historical EUR/USD tick data",
            "2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z",
            "DEVELOPMENT / EXPLORATORY ONLY",
            "FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            "Prototype authorization:",
            "`NOT_YET_AUTHORIZED`",
            "ATS2-RF-027 — HYP-0006 Data Feasibility preparation",
        ),
    )
    state_ok = require_markers(
        STATE,
        (
            'last_completed_task_id: "ATS2-RF-025"',
            'next_task_id: "ATS2-RF-026"',
            'current_task: "ATS2-RF-026"',
            'next_task: "ATS2-RF-027"',
            'rf025_verified_commit: "9b0a6c8898a7ebf9b03167a871ad02af96ca2807"',
            'strategy_5_data_feasibility_decision: "CONDITIONAL"',
            'strategy_5_development_start: "2003-08-03T21:00:00Z"',
            'strategy_5_development_end_exclusive: "2021-09-01T00:00:00Z"',
            "strategy_5_prototype_authorized: false",
            "strategy_5_outcome_computed: false",
            'strategy_5_information_boundary: "NO_HYPOTHESIS_OUTCOME_COMPUTED"',
            'strategy_4_information_boundary: "NO_CONFIRMATORY_OUTCOME_COMPUTED"',
        ),
    )
    backlog_ok = require_markers(
        BACKLOG,
        (
            "`ATS2-RF-025`",
            "DONE / PASS",
            "`ATS2-RF-026`",
            "`ATS2-RF-027`",
            "Data Feasibility preparation",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        ),
    )
    docs_ok = all(
        (
            require_markers(
                HANDOFF,
                (
                    "ATS2-RF-026",
                    "HYP-0006-DATA-FEASIBILITY.md",
                    "CONDITIONAL",
                    "NO_HYPOTHESIS_OUTCOME_COMPUTED",
                    "NO_CONFIRMATORY_OUTCOME_COMPUTED",
                ),
            ),
            require_markers(
                NEXT_STEP,
                (
                    "ATS2-RF-026",
                    "ATS2-RF-027",
                    "NO_HYPOTHESIS_OUTCOME_COMPUTED",
                    "agent/rf026-hyp0006-data-feasibility",
                ),
            ),
            require_markers(
                STATUS,
                (
                    "ATS2-RF-026",
                    "CONDITIONAL",
                    "NO_HYPOTHESIS_OUTCOME_COMPUTED",
                    "NO_CONFIRMATORY_OUTCOME_COMPUTED",
                ),
            ),
        )
    )

    return all(
        (
            review_ok,
            state_ok,
            backlog_ok,
            docs_ok,
            check_frozen_lineage(),
            check_no_premature_rf027_artifacts(),
        )
    )


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    branch = git_output("branch", "--show-current")
    commit = git_output("rev-parse", "HEAD")
    print(f"Branch: {branch or '<detached>'}")
    print(f"Commit: {commit}")

    emit_progress(40)
    staged = check_rf026_contract()

    emit_progress(60)
    governance = run(
        "RF-026 repository governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-026",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((staged, governance, full_ci))
    if passed:
        emit_progress(100)

    print("\nHYP-0005 outcome computed by RF-026: NO", flush=True)
    print("HYP-0006 outcome computed by RF-026: NO", flush=True)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
