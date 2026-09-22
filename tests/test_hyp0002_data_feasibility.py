"""Regression tests for HYP-0002 data-feasibility preparation."""

from __future__ import annotations

import importlib
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Callable

TOOLS = Path(__file__).resolve().parents[1] / "tools"


def load_confirmatory_stats() -> Callable[[list[dict[str, Any]]], dict[str, Any]]:
    sys.path.insert(0, str(TOOLS))
    try:
        module = importlib.import_module("hyp0002_data_feasibility")
    finally:
        sys.path.pop(0)
    return module.confirmatory_stats


def test_confirmatory_stats_accepts_serialized_event_times() -> None:
    confirmatory_stats = load_confirmatory_stats()
    start = datetime(2026, 1, 5, tzinfo=UTC)
    rows = [
        {
            "event_time": (start + timedelta(hours=index)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        for index in range(60)
    ]

    result = confirmatory_stats(rows)

    assert result["aligned_rows"] == 60
    assert result["gap_count"] == 0
    assert result["eligible_24_before_24_after"] == 11
    assert result["coverage_start"] == "2026-01-05T00:00:00Z"
    assert result["coverage_end"] == "2026-01-07T11:00:00Z"
