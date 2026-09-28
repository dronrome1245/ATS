#!/usr/bin/env python3
"""Run the verification package for ATS2-RF-025 on exact main."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-025"
TASK_NAME = "Parallel Strategy #5 Idea Intake + HYP-0006 formation"

IDEA = Path("research/ideas/IDEA-0005.md")
HYPOTHESIS = Path("research/hypotheses/HYP-0006.md")
STATE = Path("03_СОСТОЯНИЕ_ПРОЕКТА.yaml")
BACKLOG = Path("governance/backlog/PROGRAM_BACKLOG_V2.md")
HANDOFF = Path("AI_HANDOFF.md")
NEXT_STEP = Path("02_СЛЕДУЮЩИЙ_ШАГ.md")
STATUS = Path("01_СТАТУС_ПРОЕКТА.md")

HYP0005_FROZEN_BLOBS = {
    "research/hypotheses/HYP-0005.md": "ebbbc89187c911485c1568dc11f5f2f9e703718a",
    "research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md": (
        "c15b2b67700dd46fc592f1208731ce6b42f6905c"
    ),
    "tools/hyp0005_data_feasibility.py": "310b23213876304ade674ef36ba17ce6d457353f",
    "tests/test_hyp0005_data_feasibility.py": "12697882da682eab699bf5b7debd7c358e56aca9",
}

PROHIBITED_RF025_OUTPUT_PATTERNS = (
    "research/reviews/HYP-0006*",
    "reports/research/HYP-0006*",
    "data/manifests/*HYP0006*",
    "data/manifests/*HYP-0006*",
    "data/derived/*HYP0006*",
    "data/derived/*HYP-0006*",
    "tools/hyp0006*",
    "tests/test_hyp0006*",
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
        print(f"[FAIL] missing RF-025 artifact: {path}", flush=True)
        return False
    content = full_path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in content:
            print(f"[FAIL] RF-025 marker missing in {path}: {marker}", flush=True)
            return False
    return True


def check_hyp0005_immutability() -> bool:
    print("\n== HYP-0005 frozen-line immutability ==", flush=True)
    passed = True
    for relative, expected_blob in HYP0005_FROZEN_BLOBS.items():
        path = ROOT / relative
        if not path.is_file():
            print(f"[FAIL] frozen HYP-0005 artifact missing: {relative}", flush=True)
            passed = False
            continue
        actual_blob = git_output("rev-parse", f"HEAD:{relative}")
        if actual_blob != expected_blob:
            print(
                f"[FAIL] frozen HYP-0005 artifact changed: {relative} "
                f"({actual_blob} != {expected_blob})",
                flush=True,
            )
            passed = False
        else:
            print(f"[PASS] unchanged: {relative}", flush=True)
    return passed


def check_no_hyp0006_outcome_artifacts() -> bool:
    print("\n== HYP-0006 pre-result information boundary ==", flush=True)
    matches: list[str] = []
    for pattern in PROHIBITED_RF025_OUTPUT_PATTERNS:
        matches.extend(
            str(path.relative_to(ROOT))
            for path in ROOT.glob(pattern)
            if path.is_file()
        )
    if matches:
        for relative in sorted(set(matches)):
            print(
                f"[FAIL] RF-025 must not create downstream/outcome artifact: {relative}",
                flush=True,
            )
        return False
    print(
        "[PASS] no HYP-0006 Data Feasibility, runner, dataset or outcome artifact exists",
        flush=True,
    )
    return True


def check_rf025_contract() -> bool:
    print("\n== RF-025 staged lineage and hypothesis contract ==", flush=True)

    idea_ok = require_markers(
        IDEA,
        (
            "Idea ID: `IDEA-0005`",
            "Status: `SCREENING`",
            "S4-FAM-02 - Macroeconomic announcement response",
            "EVENT_CONDITIONAL_ABSOLUTE_RETURN_SHIFT",
            "Decision: `SCREEN`",
            "two new Material Research Attempts",
            "The frozen HYP-0005 unseen segments are unavailable",
            "research/hypotheses/HYP-0006.md",
        ),
    )
    hypothesis_ok = require_markers(
        HYPOTHESIS,
        (
            "Hypothesis ID: `HYP-0006`",
            "Parent Idea ID: `IDEA-0005`",
            "Status: `READY_FOR_DATA_FEASIBILITY`",
            "scheduled U.S. Consumer Price Index",
            "PREVIOUS_60_MINUTES",
            "NEXT_60_MINUTES",
            "median(post_abs_60m_return) > median(pre_abs_60m_return)",
            "No quote timestamp at or after `t` may serve as `PRE_RELEASE_ANCHOR`",
            "HYP-0005 frozen unseen segments used by HYP-0006 formation: `0`",
            "HYP-0006 market outcomes inspected before formation: `0`",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            "ATS2-RF-026 — HYP-0006 Data Feasibility",
        ),
    )
    state_ok = require_markers(
        STATE,
        (
            'next_task_id: "ATS2-RF-025"',
            'current_task: "ATS2-RF-025"',
            'next_task: "ATS2-RF-026"',
            'current_strategy_sequence: 5',
            'strategy_5_idea_id: "IDEA-0005"',
            'strategy_5_hypothesis_id: "HYP-0006"',
            'strategy_5_material_research_attempts_registered: 2',
            'strategy_5_hyp0005_protected_segments_consumed: false',
            'strategy_5_outcome_computed: false',
            'strategy_5_information_boundary: "NO_HYPOTHESIS_OUTCOME_COMPUTED"',
            'strategy_4_information_boundary: "NO_CONFIRMATORY_OUTCOME_COMPUTED"',
        ),
    )
    backlog_ok = require_markers(
        BACKLOG,
        (
            "`ATS2-RF-023`",
            "`ATS2-RF-024`",
            "`ATS2-RF-025`",
            "`ATS2-RF-026`",
            "two Material Research Attempts",
            "preserve all HYP-0005 frozen artifacts",
        ),
    )
    handoff_ok = require_markers(
        HANDOFF,
        (
            "ATS2-RF-025",
            "IDEA-0005",
            "HYP-0006",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            "NO_CONFIRMATORY_OUTCOME_COMPUTED",
            "RF-023 remains separately open",
        ),
    )
    next_ok = require_markers(
        NEXT_STEP,
        (
            "ATS2-RF-025",
            "ATS2-RF-026",
            ".\\ATS_AGENT_PREFLIGHT.bat",
            ".\\ATS_TASK_CHECK.bat",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            "NO_CONFIRMATORY_OUTCOME_COMPUTED",
        ),
    )
    status_ok = require_markers(
        STATUS,
        (
            "ATS2-RF-025",
            "IDEA-0005",
            "HYP-0006",
            "NEW_IDEA_FROM_RETAINED_RESEARCH_FAMILY",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            "NO_CONFIRMATORY_OUTCOME_COMPUTED",
        ),
    )

    return all(
        (
            idea_ok,
            hypothesis_ok,
            state_ok,
            backlog_ok,
            handoff_ok,
            next_ok,
            status_ok,
            check_hyp0005_immutability(),
            check_no_hyp0006_outcome_artifacts(),
        )
    )


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    commit = git_output("rev-parse", "HEAD")
    branch = git_output("branch", "--show-current")
    print(f"Branch: {branch or '<detached>'}")
    print(f"Commit: {commit}")

    emit_progress(40)
    staged = check_rf025_contract()

    emit_progress(60)
    governance = run(
        "RF-025 repository governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-025",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((staged, governance, full_ci))
    if passed:
        emit_progress(100)

    print("\nHYP-0005 outcome computed by RF-025: NO", flush=True)
    print("HYP-0006 outcome computed by RF-025: NO", flush=True)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
