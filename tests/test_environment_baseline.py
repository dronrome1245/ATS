from __future__ import annotations

import sys
from importlib.metadata import version

EXPECTED_PACKAGES = {
    "numpy": "2.5.3",
    "pydantic": "2.13.5",
    "PyYAML": "6.0.3",
    "pytest": "9.1.1",
    "ruff": "0.16.7",
}


def test_exact_python_patch() -> None:
    assert sys.version_info[:3] == (3, 13, 15)


def test_direct_environment_versions() -> None:
    installed = {name: version(name) for name in EXPECTED_PACKAGES}
    assert installed == EXPECTED_PACKAGES
