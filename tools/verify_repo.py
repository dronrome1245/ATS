#!/usr/bin/env python3
"""Run the canonical ATS local quality gate."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "reports" / "local_ci" / "LATEST.json"
LINT_PATHS = (
    "tools/validate_repo.py",
    "tools/validate_repo_core.py",
    "tools/environment_fingerprint.py",
    "tools/search_experiments.py",
    "tools/verify_repo.py",
    "tools/current_task_check.py",
    "tools/proto01_eurusd.py",
    "src",
    "tests",
)
FORMAT_PATHS = (
    "tools/environment_fingerprint.py",
    "tools/search_experiments.py",
    "tools/verify_repo.py",
    "tools/current_task_check.py",
    "tools/proto01_eurusd.py",
    "src",
    "tests",
)


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def git_output(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def run_step(name: str, command: list[str]) -> dict[str, Any]:
    print(f"\n== {name} ==")
    print("$ " + " ".join(command))
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    return {
        "name": name,
        "command": command,
        "return_code": completed.returncode,
        "status": "PASS" if passed else "FAIL",
    }


def environment_fingerprint() -> tuple[dict[str, Any], dict[str, Any] | None]:
    command = [sys.executable, "tools/environment_fingerprint.py"]
    print("\n== environment fingerprint ==")
    print("$ " + " ".join(command))
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.stderr:
        print(completed.stderr.rstrip(), file=sys.stderr)

    parsed: dict[str, Any] | None = None
    if completed.returncode == 0:
        try:
            parsed = json.loads(completed.stdout)
        except json.JSONDecodeError:
            completed = subprocess.CompletedProcess(
                completed.args,
                1,
                completed.stdout,
                "environment fingerprint did not emit valid JSON",
            )

    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] environment fingerprint")
    step = {
        "name": "environment fingerprint",
        "command": command,
        "return_code": completed.returncode,
        "status": "PASS" if passed else "FAIL",
    }
    return step, parsed


def write_report(report: dict[str, Any]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="ATS local CI gate")
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Run the fast development gate instead of the full completion gate.",
    )
    args = parser.parse_args()

    started_at = now_iso()
    mode = "FAST" if args.fast else "FULL"

    try:
        commit_sha = git_output("rev-parse", "HEAD")
        status_porcelain = git_output("status", "--porcelain")
        dirty = bool(status_porcelain)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Git metadata unavailable: {exc}", file=sys.stderr)
        return 2

    print(f"ATS Local CI Gate — {mode}")
    print(f"commit: {commit_sha}")
    print(f"working tree: {'DIRTY' if dirty else 'CLEAN'}")
    if dirty:
        print("working tree changes:")
        print(status_porcelain)

    steps: list[dict[str, Any]] = []
    fingerprint: dict[str, Any] | None = None

    if not args.fast and dirty:
        steps.append(
            {
                "name": "working tree clean",
                "command": ["git", "status", "--porcelain"],
                "return_code": 1,
                "status": "FAIL",
            }
        )
        overall = "FAIL"
        report = {
            "commit_sha": commit_sha,
            "completed_at": now_iso(),
            "environment_fingerprint": fingerprint,
            "mode": mode,
            "overall": overall,
            "started_at": started_at,
            "steps": steps,
            "working_tree_dirty": dirty,
            "working_tree_status": status_porcelain.splitlines(),
        }
        write_report(report)
        print("\n[FAIL] Full gate requires a clean working tree.")
        print(f"Report: {REPORT_PATH.relative_to(ROOT)}")
        print("ATS LOCAL CI: FAIL")
        return 1

    ruff = shutil.which("ruff")
    if ruff is None:
        print("Ruff executable is unavailable in the frozen environment.", file=sys.stderr)
        return 2

    steps.append(
        run_step(
            "repository validator",
            [sys.executable, "tools/validate_repo.py"],
        )
    )
    steps.append(
        run_step(
            "ruff lint",
            [ruff, "check", *LINT_PATHS],
        )
    )
    steps.append(
        run_step(
            "ruff format",
            [ruff, "format", "--check", *FORMAT_PATHS],
        )
    )

    if not args.fast:
        steps.append(
            run_step(
                "pytest",
                [sys.executable, "-m", "pytest"],
            )
        )
        fingerprint_step, fingerprint = environment_fingerprint()
        steps.append(fingerprint_step)

    overall = "PASS" if all(step["status"] == "PASS" for step in steps) else "FAIL"
    report = {
        "commit_sha": commit_sha,
        "completed_at": now_iso(),
        "environment_fingerprint": fingerprint,
        "mode": mode,
        "overall": overall,
        "started_at": started_at,
        "steps": steps,
        "working_tree_dirty": dirty,
    }
    write_report(report)

    print(f"\nReport: {REPORT_PATH.relative_to(ROOT)}")
    print(f"ATS LOCAL CI: {overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
