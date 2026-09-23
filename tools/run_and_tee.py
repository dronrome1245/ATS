#!/usr/bin/env python3
"""Run a Python script while streaming output to console and a task report."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRESS_PREFIX = "@@PROGRESS "


def render_progress(percent: int) -> None:
    bounded = max(0, min(100, percent))
    width = 20
    filled = round(width * bounded / 100)
    bar = "#" * filled + "-" * (width - filled)
    print(f"\rProgress: [{bar}] {bounded:3d}%", end="", flush=True)


def main() -> int:
    if len(sys.argv) < 3:
        print(
            "usage: run_and_tee.py REPORT_PATH SCRIPT [SCRIPT_ARG ...]",
            file=sys.stderr,
        )
        return 2

    report_path = ROOT / sys.argv[1]
    script_path = sys.argv[2]
    command = [sys.executable, script_path, *sys.argv[3:]]
    environment = dict(os.environ)
    environment["PYTHONUNBUFFERED"] = "1"

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("a", encoding="utf-8") as report:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        assert process.stdout is not None
        last_progress: int | None = None
        for line in process.stdout:
            report.write(line)
            report.flush()
            if line.startswith(PROGRESS_PREFIX):
                try:
                    last_progress = int(line[len(PROGRESS_PREFIX) :].strip())
                except ValueError:
                    continue
                render_progress(last_progress)
        return_code = process.wait()
        if last_progress is not None:
            print()
        return return_code


if __name__ == "__main__":
    raise SystemExit(main())
