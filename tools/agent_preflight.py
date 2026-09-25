#!/usr/bin/env python3
"""Run OWNER-quality verification on an agent branch before merge to main."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENT_BRANCH_PREFIX = "agent/"


def git_output(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def ref_exists(ref: str) -> bool:
    completed = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", ref],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return completed.returncode == 0


def run_current_task_import_smoke() -> int:
    smoke_code = (
        "import runpy; "
        "runpy.run_path('tools/current_task_check.py', "
        "run_name='agent_preflight_import_smoke')"
    )
    command = [sys.executable, "-c", smoke_code]
    print("\n== current task checker import smoke ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(
        f"[{'PASS' if passed else 'FAIL'}] current task checker import smoke",
        flush=True,
    )
    return completed.returncode


def run_full_gate() -> int:
    command = [sys.executable, "tools/verify_repo.py"]
    print("\n== full ATS Local CI on agent branch ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(
        f"[{'PASS' if passed else 'FAIL'}] full ATS Local CI on agent branch",
        flush=True,
    )
    return completed.returncode


def main() -> int:
    try:
        branch = git_output("branch", "--show-current")
        commit = git_output("rev-parse", "HEAD")
        status = git_output("status", "--porcelain")
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"[FAIL] git metadata unavailable: {exc}", file=sys.stderr)
        return 2

    print("ATS AGENT PREFLIGHT")
    print(f"Branch: {branch or '<detached>'}")
    print(f"Commit: {commit}")

    if not branch.startswith(AGENT_BRANCH_PREFIX):
        print(
            "[FAIL] preflight must run on an agent/* branch before merge to main",
            flush=True,
        )
        return 1

    if status:
        print("[FAIL] agent preflight requires a clean working tree", flush=True)
        print(status, flush=True)
        return 1

    base = "origin/main" if ref_exists("origin/main") else "main"
    if not ref_exists(base):
        print("[FAIL] neither origin/main nor main is available", flush=True)
        return 1

    try:
        merge_base = git_output("merge-base", base, "HEAD")
        changed_text = git_output("diff", "--name-only", f"{base}...HEAD")
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"[FAIL] cannot compare agent branch with {base}: {exc}", flush=True)
        return 1

    changed = [line for line in changed_text.splitlines() if line]
    print(f"Base: {base}")
    print(f"Merge base: {merge_base}")
    print(f"Changed files: {len(changed)}")
    for path in changed:
        print(f"  - {path}")

    if not changed:
        print("[FAIL] agent branch has no changes relative to main", flush=True)
        return 1

    import_smoke = run_current_task_import_smoke()
    if import_smoke != 0:
        return import_smoke

    return run_full_gate()


if __name__ == "__main__":
    raise SystemExit(main())
