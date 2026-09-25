#!/usr/bin/env python3
"""Run frozen HYP-0003 PROTO-01 on the development currency H1 dataset."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv"
MANIFEST_PATH = ROOT / "data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001.yaml"
RESULT_PATH = ROOT / "reports/local_ci/HYP0003_PROTO01_RESULT.json"
RESULT_REPORT_PATH = ROOT / "reports/local_ci/HYP0003_PROTO01_RESULT_REPORT.txt"

EXPECTED_DATASET_ID = "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001"
EXPECTED_DATASET_VERSION = "1.0.0"
EXPECTED_DATASET_SHA256 = "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2"
EXPECTED_SOURCE_BUNDLE_SHA256 = "9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a"
EXPECTED_ROWS = 1_014_509

DATA_START = datetime(2003, 8, 3, 21, tzinfo=UTC)
DATA_END = datetime(2021, 9, 1, tzinfo=UTC)
FIRST_SOURCE_MONTH = datetime(2003, 8, 1, tzinfo=UTC)
LAST_SOURCE_MONTH = datetime(2021, 8, 1, tzinfo=UTC)

FORMATION_MONTHS = (1, 3, 6, 9, 12)
HOLDING_MONTHS = (1, 3, 6, 9, 12)
CURRENCIES = ("AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NOK", "NZD", "SEK")
MINIMUM_CURRENCIES = 6

Bar = tuple[float, float, float, float]
Observation = dict[str, Any]


class Proto03Error(RuntimeError):
    """Raised when the frozen HYP-0003 PROTO-01 contract cannot execute."""


def parse_time(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def next_month(value: datetime) -> datetime:
    if value.month == 12:
        return datetime(value.year + 1, 1, 1, tzinfo=UTC)
    return datetime(value.year, value.month + 1, 1, tzinfo=UTC)


def shift_month_start(value: datetime, months: int) -> datetime:
    index = value.year * 12 + value.month - 1 + months
    year, month_index = divmod(index, 12)
    return datetime(year, month_index + 1, 1, tzinfo=UTC)


def nth_weekday_of_month(year: int, month: int, weekday: int, occurrence: int) -> int:
    first = datetime(year, month, 1, tzinfo=UTC)
    offset = (weekday - first.weekday()) % 7
    return 1 + offset + 7 * (occurrence - 1)


def us_dst_active_utc(value: datetime) -> bool:
    march_sunday = nth_weekday_of_month(value.year, 3, 6, 2)
    november_sunday = nth_weekday_of_month(value.year, 11, 6, 1)
    start = datetime(value.year, 3, march_sunday, 7, tzinfo=UTC)
    end = datetime(value.year, 11, november_sunday, 6, tzinfo=UTC)
    return start <= value < end


def is_fx_market_hour(value: datetime) -> bool:
    weekday = value.weekday()
    if weekday < 4:
        return True
    boundary_hour = 21 if us_dst_active_utc(value) else 22
    if weekday == 4:
        return value.hour < boundary_hour
    if weekday == 5:
        return False
    return value.hour >= boundary_hour


def monthly_cutoff(month: datetime) -> datetime:
    candidate = next_month(month) - timedelta(hours=1)
    while candidate >= month:
        if is_fx_market_hour(candidate):
            return candidate
        candidate -= timedelta(hours=1)
    raise Proto03Error(f"no expected FX market hour in {month:%Y-%m}")


def first_market_hour_at_or_after(value: datetime) -> datetime:
    candidate = value
    while not is_fx_market_hour(candidate):
        candidate += timedelta(hours=1)
    return candidate


def development_months() -> list[datetime]:
    values: list[datetime] = []
    current = FIRST_SOURCE_MONTH
    while current <= LAST_SOURCE_MONTH:
        values.append(current)
        current = next_month(current)
    return values


def basket_size(eligible_currency_count: int) -> int:
    if eligible_currency_count < MINIMUM_CURRENCIES:
        raise ValueError("basket size requires at least six currencies")
    return max(1, math.ceil(eligible_currency_count / 6))


def select_baskets(formation_returns: dict[str, float]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if len(formation_returns) < MINIMUM_CURRENCIES:
        raise ValueError("basket selection requires at least six currencies")
    size = basket_size(len(formation_returns))
    losers = tuple(
        currency
        for currency, _value in sorted(
            formation_returns.items(),
            key=lambda item: (item[1], item[0]),
        )[:size]
    )
    winners = tuple(
        currency
        for currency, _value in sorted(
            formation_returns.items(),
            key=lambda item: (-item[1], item[0]),
        )[:size]
    )
    return winners, losers


def winner_long_return(entry: Bar, exit_bar: Bar) -> float:
    bid_open, _bid_close, ask_open, _ask_close = entry
    exit_bid_open, _exit_bid_close, _exit_ask_open, _exit_ask_close = exit_bar
    return exit_bid_open / ask_open - 1.0


def loser_short_return(entry: Bar, exit_bar: Bar) -> float:
    bid_open, _bid_close, _ask_open, _ask_close = entry
    _exit_bid_open, _exit_bid_close, exit_ask_open, _exit_ask_close = exit_bar
    return bid_open / exit_ask_open - 1.0


def mid_close(bar: Bar) -> float:
    _bid_open, bid_close, _ask_open, ask_close = bar
    return (bid_close + ask_close) / 2.0


def side_turnover(previous: tuple[str, ...], current: tuple[str, ...]) -> float:
    previous_weight = 1.0 / len(previous)
    current_weight = 1.0 / len(current)
    retained = sum(
        min(previous_weight, current_weight)
        for currency in set(previous).intersection(current)
    )
    return 1.0 - retained


def observation_turnover(previous: Observation, current: Observation) -> float:
    return 0.5 * (
        side_turnover(previous["winners"], current["winners"])
        + side_turnover(previous["losers"], current["losers"])
    )


def load_manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open(encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle)
    if not isinstance(manifest, dict):
        raise Proto03Error("development Dataset Manifest is not a mapping")
    if manifest.get("dataset_id") != EXPECTED_DATASET_ID:
        raise Proto03Error("development Dataset ID mismatch")
    if manifest.get("dataset_version") != EXPECTED_DATASET_VERSION:
        raise Proto03Error("development Dataset version mismatch")
    if manifest.get("integrity", {}).get("digest") != EXPECTED_DATASET_SHA256:
        raise Proto03Error("development manifest prepared CSV SHA-256 mismatch")
    snapshot = manifest.get("source", {}).get("snapshot_reference")
    if snapshot != f"source-bundle-sha256:{EXPECTED_SOURCE_BUNDLE_SHA256}":
        raise Proto03Error("development source-bundle identity mismatch")
    if sha256_file(DATA_PATH) != EXPECTED_DATASET_SHA256:
        raise Proto03Error("development prepared CSV SHA-256 mismatch")
    return manifest


def relevant_timestamps() -> set[datetime]:
    targets: set[datetime] = set()
    for month in development_months():
        ranking_anchor = next_month(month)
        if ranking_anchor >= DATA_END:
            continue
        current_cutoff = monthly_cutoff(month)
        targets.add(current_cutoff)
        targets.add(first_market_hour_at_or_after(current_cutoff + timedelta(hours=1)))
        for formation in FORMATION_MONTHS:
            formation_month = shift_month_start(month, -formation)
            if formation_month >= FIRST_SOURCE_MONTH:
                targets.add(monthly_cutoff(formation_month))
        for holding in HOLDING_MONTHS:
            exit_anchor = shift_month_start(ranking_anchor, holding)
            if exit_anchor < DATA_END:
                targets.add(first_market_hour_at_or_after(exit_anchor))
    return targets


def read_relevant_bars() -> dict[str, dict[datetime, Bar]]:
    targets = relevant_timestamps()
    bars: dict[str, dict[datetime, Bar]] = {currency: {} for currency in CURRENCIES}
    rows = 0
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows += 1
            timestamp = parse_time(row["event_time"])
            if timestamp >= DATA_END:
                raise Proto03Error("protected-tail row present in frozen development CSV")
            currency = row["currency"]
            if currency not in bars:
                raise Proto03Error(f"unexpected currency in development CSV: {currency}")
            if timestamp not in targets:
                continue
            if timestamp in bars[currency]:
                raise Proto03Error(f"duplicate relevant timestamp for {currency}: {iso_z(timestamp)}")
            bars[currency][timestamp] = (
                float(row["bid_open"]),
                float(row["bid_close"]),
                float(row["ask_open"]),
                float(row["ask_close"]),
            )
    if rows != EXPECTED_ROWS:
        raise Proto03Error(f"development row count mismatch: {rows} != {EXPECTED_ROWS}")
    return bars


def cell_observations(
    bars: dict[str, dict[datetime, Bar]],
    formation: int,
    holding: int,
) -> list[Observation]:
    observations: list[Observation] = []
    for month in development_months():
        ranking_anchor = next_month(month)
        if ranking_anchor >= DATA_END:
            continue
        formation_month = shift_month_start(month, -formation)
        if formation_month < FIRST_SOURCE_MONTH:
            continue
        exit_anchor = shift_month_start(ranking_anchor, holding)
        if exit_anchor >= DATA_END:
            continue

        current_cutoff = monthly_cutoff(month)
        start_cutoff = monthly_cutoff(formation_month)
        formation_returns: dict[str, float] = {}
        for currency in CURRENCIES:
            current_bar = bars[currency].get(current_cutoff)
            start_bar = bars[currency].get(start_cutoff)
            if current_bar is None or start_bar is None:
                continue
            formation_returns[currency] = mid_close(current_bar) / mid_close(start_bar) - 1.0

        if len(formation_returns) < MINIMUM_CURRENCIES:
            continue

        winners, losers = select_baskets(formation_returns)
        entry_time = first_market_hour_at_or_after(current_cutoff + timedelta(hours=1))
        exit_time = first_market_hour_at_or_after(exit_anchor)
        if exit_time >= DATA_END:
            continue

        selected = winners + losers
        if any(
            bars[currency].get(entry_time) is None or bars[currency].get(exit_time) is None
            for currency in selected
        ):
            continue

        winner_values = [
            winner_long_return(bars[currency][entry_time], bars[currency][exit_time])
            for currency in winners
        ]
        loser_values = [
            loser_short_return(bars[currency][entry_time], bars[currency][exit_time])
            for currency in losers
        ]
        observations.append(
            {
                "ranking_anchor": ranking_anchor,
                "entry_time": entry_time,
                "exit_time": exit_time,
                "eligible_currency_count": len(formation_returns),
                "basket_size": len(winners),
                "winners": winners,
                "losers": losers,
                "portfolio_return": statistics.fmean(winner_values)
                + statistics.fmean(loser_values),
            }
        )
    return observations


def overlap_metrics(observations: list[Observation]) -> tuple[int, float]:
    overlaps = 0
    running_exit: datetime | None = None
    for observation in observations:
        entry_time = observation["entry_time"]
        exit_time = observation["exit_time"]
        if running_exit is not None and entry_time < running_exit:
            overlaps += 1
        if running_exit is None or exit_time > running_exit:
            running_exit = exit_time
    return overlaps, overlaps / len(observations) if observations else 0.0


def cell_metrics(
    observations: list[Observation],
    formation: int,
    holding: int,
) -> dict[str, Any]:
    if not observations:
        return {
            "formation_months": formation,
            "holding_months": holding,
            "observation_count": 0,
            "mean_return": None,
            "median_return": None,
            "positive_share": None,
            "overlapping_windows": 0,
            "overlapping_share": None,
            "mean_membership_turnover": None,
            "min_eligible_currency_count": None,
            "max_eligible_currency_count": None,
        }

    values = [float(item["portfolio_return"]) for item in observations]
    overlaps, overlap_share = overlap_metrics(observations)
    turnovers = [
        observation_turnover(previous, current)
        for previous, current in zip(observations, observations[1:])
    ]
    eligible_counts = [int(item["eligible_currency_count"]) for item in observations]
    return {
        "formation_months": formation,
        "holding_months": holding,
        "observation_count": len(observations),
        "mean_return": statistics.fmean(values),
        "median_return": statistics.median(values),
        "positive_share": sum(value > 0.0 for value in values) / len(values),
        "overlapping_windows": overlaps,
        "overlapping_share": overlap_share,
        "mean_membership_turnover": statistics.fmean(turnovers) if turnovers else 0.0,
        "min_eligible_currency_count": min(eligible_counts),
        "max_eligible_currency_count": max(eligible_counts),
    }


def breadth_summary(cells: list[dict[str, Any]]) -> dict[str, Any]:
    if len(cells) != 25:
        raise ValueError("breadth summary requires all 25 declared cells")
    if any(int(cell["observation_count"]) == 0 for cell in cells):
        return {
            "all_cells_observed": False,
            "median_cell_mean": None,
            "positive_mean_cell_count": None,
            "positive_formation_period_count": None,
            "positive_holding_period_count": None,
            "median_positive": False,
            "positive_cell_count_pass": False,
            "formation_span_pass": False,
            "holding_span_pass": False,
        }

    positive = [cell for cell in cells if float(cell["mean_return"]) > 0.0]
    median_mean = statistics.median(float(cell["mean_return"]) for cell in cells)
    formation_span = len({int(cell["formation_months"]) for cell in positive})
    holding_span = len({int(cell["holding_months"]) for cell in positive})
    return {
        "all_cells_observed": True,
        "median_cell_mean": median_mean,
        "positive_mean_cell_count": len(positive),
        "positive_formation_period_count": formation_span,
        "positive_holding_period_count": holding_span,
        "median_positive": median_mean > 0.0,
        "positive_cell_count_pass": len(positive) >= 13,
        "formation_span_pass": formation_span >= 3,
        "holding_span_pass": holding_span >= 3,
    }


def prototype_decision(cells: list[dict[str, Any]]) -> tuple[str, str, str]:
    breadth = breadth_summary(cells)
    if not breadth["all_cells_observed"]:
        return "PARK", "ONE_OR_MORE_DECLARED_CELLS_HAVE_ZERO_OBSERVATIONS", "PARK"
    passed = (
        breadth["median_positive"]
        and breadth["positive_cell_count_pass"]
        and breadth["formation_span_pass"]
        and breadth["holding_span_pass"]
    )
    if passed:
        return (
            "ADVANCE_TO_ECONOMIC_SCREEN",
            "ALL_BROAD_REGION_CRITERIA_MET",
            "CREATE_NEW_CONFIRMATORY_HYPOTHESIS_BEFORE_R4",
        )
    return "REJECT", "ONE_OR_MORE_BROAD_REGION_CRITERIA_FAILED", "STOP_HYP0003"


def evaluate(bars: dict[str, dict[datetime, Bar]]) -> dict[str, Any]:
    cells: list[dict[str, Any]] = []
    for formation in FORMATION_MONTHS:
        for holding in HOLDING_MONTHS:
            observations = cell_observations(bars, formation, holding)
            cells.append(cell_metrics(observations, formation, holding))

    breadth = breadth_summary(cells)
    decision, reason, next_action = prototype_decision(cells)
    return {
        "schema_version": "hyp0003-proto01-result-1",
        "hypothesis_id": "HYP-0003",
        "prototype_sequence": "PROTO-01",
        "evidence_class": "EXPLORATORY_PROTOTYPE",
        "economic_label": "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
        "grid": {
            "formation_months": list(FORMATION_MONTHS),
            "holding_months": list(HOLDING_MONTHS),
            "declared_cell_count": 25,
        },
        "cells": cells,
        "breadth": breadth,
        "decision": decision,
        "decision_reason": reason,
        "next_action": next_action,
    }


def run_result() -> int:
    manifest = load_manifest()
    result = evaluate(read_relevant_bars())
    result["dataset"] = {
        "dataset_id": manifest["dataset_id"],
        "dataset_version": manifest["dataset_version"],
        "prepared_csv_sha256": EXPECTED_DATASET_SHA256,
        "source_bundle_sha256": EXPECTED_SOURCE_BUNDLE_SHA256,
    }
    result["run_context"] = {
        "git_commit": git_head(),
        "completed_at": datetime.now(UTC).isoformat(),
    }
    result["limitations"] = [
        "Commission is not modeled.",
        "Financing/rollover is not modeled and is material for multi-month holds.",
        "H1 quote opens are not guaranteed live fills.",
        "Overlapping monthly holding windows create dependent observations.",
        "Development data are exploratory and are not validation or independent evidence.",
        "A positive broad region requires a new fixed confirmatory Hypothesis before R4.",
    ]

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    breadth = result["breadth"]
    lines = [
        "ATS HYP-0003 PROTO-01 RESULT",
        "=============================",
        f"Git commit: {result['run_context']['git_commit']}",
        f"Declared cells: {result['grid']['declared_cell_count']}",
        f"All cells observed: {breadth['all_cells_observed']}",
        f"Median cell mean: {breadth['median_cell_mean']}",
        f"Positive mean cells: {breadth['positive_mean_cell_count']}",
        f"Positive formation span: {breadth['positive_formation_period_count']}",
        f"Positive holding span: {breadth['positive_holding_period_count']}",
        f"Decision: {result['decision']}",
        f"Reason: {result['decision_reason']}",
        f"Next action: {result['next_action']}",
        "Economic label: QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
    ]
    RESULT_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


def main() -> int:
    try:
        return run_result()
    except (Proto03Error, OSError, ValueError, KeyError, ZeroDivisionError) as exc:
        print(f"HYP-0003 PROTO-01 BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
