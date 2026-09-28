#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-022"
TASK_NAME = "HYP-0005 confirmatory hypothesis formation"
HYPOTHESIS = Path("research/hypotheses/HYP-0005.md")
PARENT_IDEA = Path("research/ideas/IDEA-0004.md")
DEVELOPMENT_HYPOTHESIS = Path("research/hypotheses/HYP-0004.md")
DEVELOPMENT_RESULT = Path("reports/research/HYP-0004-PROTOTYPE-01-result.json")
EXPECTED_DEVELOPMENT_RESULT_SHA256 = (
    "1c9b2cb1a1628599e935ee61fd8c9b152d7bd3447969b065c920c8d13e3e5230"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def check_hypothesis_formation() -> bool:
    print("\n== RF-022 HYP-0005 confirmatory hypothesis formation ==", flush=True)

    required = (HYPOTHESIS, PARENT_IDEA, DEVELOPMENT_HYPOTHESIS, DEVELOPMENT_RESULT)
    missing = [str(path) for path in required if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing RF-022 artifact: {path}", flush=True)
        return False

    actual_result_sha = sha256_file(ROOT / DEVELOPMENT_RESULT)
    if actual_result_sha != EXPECTED_DEVELOPMENT_RESULT_SHA256:
        print("[FAIL] HYP-0004 canonical development result changed", flush=True)
        return False

    future_artifacts = []
    for base in (
        ROOT / "research/reviews",
        ROOT / "data/manifests",
        ROOT / "reports/research",
    ):
        future_artifacts.extend(
            path for path in base.glob("*HYP*0005*") if path.is_file()
        )
    if future_artifacts:
        for path in sorted(future_artifacts):
            print(
                f"[FAIL] RF-022 must not create confirmatory data/review/result artifact: "
                f"{path.relative_to(ROOT)}",
                flush=True,
            )
        return False

    text = (ROOT / HYPOTHESIS).read_text(encoding="utf-8")
    required_markers = (
        "Hypothesis ID: `HYP-0005`",
        "Parent Idea ID: `IDEA-0004`",
        "Development predecessor: `HYP-0004`",
        "Status: `READY_FOR_DATA_FEASIBILITY`",
        "`CORE_ACTIVE`: UTC hours `07` through `16` inclusive",
        "`TRANSITION`: UTC hours `17` through `20` inclusive",
        "`OFF_HOURS`: UTC hours `21`, `22`, `23`, and `00` through `06` inclusive",
        "median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)",
        "median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)",
        "No minimum effect-size threshold is added after the HYP-0004 reveal.",
        "Confirmatory datasets inspected by RF-022: `0`",
        "Confirmatory outcomes inspected by RF-022: `0`",
        "Exact provider, coverage dates, row count and source hashes are intentionally unknown",
        "If a genuinely unseen confirmatory block cannot be established",
        "ATS2-RF-023 — HYP-0005 confirmatory Data Feasibility",
        "Direct R4 entry remains blocked",
    )
    for marker in required_markers:
        if marker not in text:
            print(f"[FAIL] HYP-0005 formation marker missing: {marker}", flush=True)
            return False

    forbidden_markers = (
        "Decision: `ADVANCE_TO_ECONOMIC_SCREEN`",
        "Decision: `REJECT`",
        "confirmatory dataset SHA-256:",
        "confirmatory result SHA-256:",
    )
    for marker in forbidden_markers:
        if marker in text:
            print(
                f"[FAIL] RF-022 contains premature confirmatory outcome/data marker: {marker}",
                flush=True,
            )
            return False

    print(
        "[PASS] RF-022 registered HYP-0005 without selecting or revealing confirmatory data",
        flush=True,
    )
    return True


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    print(f"Commit: {git_output('rev-parse', 'HEAD')}")

    emit_progress(45)
    hypothesis = check_hypothesis_formation()

    emit_progress(65)
    governance = run(
        "RF-022 HYP-0005 formation governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-022 HYP-0005 formation",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((hypothesis, governance, full_ci))
    if passed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
