#!/usr/bin/env python3
"""Emit the reproducible ATS M2 research-environment fingerprint."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version

PACKAGES = (
    "numpy",
    "pydantic",
    "PyYAML",
    "pytest",
    "ruff",
)


def package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "NOT_INSTALLED"


def uv_version() -> str:
    try:
        completed = subprocess.run(
            ["uv", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "UNAVAILABLE"
    return completed.stdout.strip()


def main() -> int:
    fingerprint = {
        "implementation": platform.python_implementation(),
        "packages": {name: package_version(name) for name in PACKAGES},
        "platform": platform.platform(),
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "uv": uv_version(),
    }
    print(json.dumps(fingerprint, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
