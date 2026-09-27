#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-020"
TASK_NAME = "HYP-0004 PROTO-01 reveal"
PROTO = Path("research/reviews/HYP-0004-PROTOTYPE-01.md")
RUNNER = Path("tools/hyp0004_proto01.py")
DATA = Path("data/derived/HYP-0004-DEV-01-EURUSD-H1.csv")
MANIFEST = Path("data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001.yaml")
RESULT = Path("reports/local_ci/HYP0004_PROTO01_RESULT.json")
CANONICAL_RESULT = Path("reports/research/HYP-0004-PROTOTYPE-01-result.json")

EXPECTED_RUNNER_GIT_BLOB = "cbc9a46bf5e5296615f51c0ea564153968bc2a55"
EXPECTED_DATASET_ID = "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001"
EXPECTED_DATASET_VERSION = "1.0.0"
EXPECTED_DATASET_SHA256 = "3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6"
EXPECTED_ELIGIBLE = 111_938
EXPECTED_ELIGIBLE_BY_BUCKET = {
    "CORE_ACTIVE": 47_012,
    "OFF_HOURS": 46_737,
    "TRANSITION": 18_189,
}
EXPECTED_CLOSED_NEXT = 940
EXPECTED_MISSING_NEXT = 21
EXPECTED_DATASET_END = 1
BUCKETS = ("CORE_ACTIVE", "TRANSITION", "OFF_HOURS")


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


def check_frozen_inputs() -> bool:
    print("\n== RF-020 frozen reveal inputs ==", flush=True)
    for path in (PROTO, RUNNER, DATA, MANIFEST):
        if not (ROOT / path).is_file():
            print(f"[FAIL] missing frozen input: {path}", flush=True)
            return False

    if (ROOT / CANONICAL_RESULT).exists():
        print("[FAIL] canonical HYP-0004 result exists before RF-020 reveal", flush=True)
        return False

    runner_blob = git_output("rev-parse", f"HEAD:{RUNNER.as_posix()}")
    if runner_blob != EXPECTED_RUNNER_GIT_BLOB:
        print(
            f"[FAIL] frozen runner blob mismatch: {runner_blob} != {EXPECTED_RUNNER_GIT_BLOB}",
            flush=True,
        )
        return False

    actual_dataset_sha256 = sha256_file(ROOT / DATA)
    if actual_dataset_sha256 != EXPECTED_DATASET_SHA256:
        print(
            f"[FAIL] frozen development CSV SHA-256 mismatch: "
            f"{actual_dataset_sha256} != {EXPECTED_DATASET_SHA256}",
            flush=True,
        )
        return False

    prototype = (ROOT / PROTO).read_text(encoding="utf-8")
    for marker in (
        "FROZEN / NOT_REVEALED",
        EXPECTED_RUNNER_GIT_BLOB,
        "BOTH_PRIMARY_INEQUALITIES_MET",
        "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED",
        "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "ATS2-RF-020 — HYP-0004 PROTO-01 reveal",
    ):
        if marker not in prototype:
            print(f"[FAIL] frozen prototype marker missing: {marker}", flush=True)
            return False

    print("[PASS] exact RF-019 frozen runner/protocol/data identity", flush=True)
    return True


def finite_nonnegative(value: object, label: str) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        print(f"[FAIL] {label} must be numeric", flush=True)
        return False
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        print(f"[FAIL] {label} must be finite and non-negative", flush=True)
        return False
    return True


def validate_result(payload: dict[str, Any], commit: str) -> bool:
    checks = {
        "schema_version": "hyp0004-proto01-result-1",
        "hypothesis_id": "HYP-0004",
        "prototype_sequence": "PROTO-01",
        "evidence_class": "EXPLORATORY_PROTOTYPE",
        "measurement_label": "STRUCTURAL_H1_OPEN_PROXY_NO_TRADING_PNL",
    }
    for key, expected in checks.items():
        actual = payload.get(key)
        if actual != expected:
            print(f"[FAIL] result mismatch for {key}: {actual!r} != {expected!r}", flush=True)
            return False

    dataset = payload.get("dataset")
    if not isinstance(dataset, dict):
        print("[FAIL] result dataset identity missing", flush=True)
        return False
    dataset_checks = {
        "dataset_id": EXPECTED_DATASET_ID,
        "dataset_version": EXPECTED_DATASET_VERSION,
        "prepared_csv_sha256": EXPECTED_DATASET_SHA256,
        "boundary_availability_mode": "H1_OPEN_PROXY_AT_EVENT_TIME",
        "exact_tick_boundary_time_known": False,
        "eligible_exact_next_hour_count": EXPECTED_ELIGIBLE,
    }
    for key, expected in dataset_checks.items():
        actual = dataset.get(key)
        if actual != expected:
            print(
                f"[FAIL] result dataset mismatch for {key}: {actual!r} != {expected!r}",
                flush=True,
            )
            return False

    geometry = payload.get("geometry")
    if not isinstance(geometry, dict):
        print("[FAIL] result geometry missing", flush=True)
        return False
    geometry_checks = {
        "eligible_count": EXPECTED_ELIGIBLE,
        "eligible_by_bucket": EXPECTED_ELIGIBLE_BY_BUCKET,
        "ineligible_closed_market_next_hour_count": EXPECTED_CLOSED_NEXT,
        "ineligible_missing_expected_next_hour_count": EXPECTED_MISSING_NEXT,
        "ineligible_dataset_end_count": EXPECTED_DATASET_END,
    }
    for key, expected in geometry_checks.items():
        actual = geometry.get(key)
        if actual != expected:
            print(
                f"[FAIL] result geometry mismatch for {key}: {actual!r} != {expected!r}",
                flush=True,
            )
            return False

    metrics = payload.get("bucket_metrics")
    if not isinstance(metrics, dict) or set(metrics) != set(BUCKETS):
        print("[FAIL] result bucket metrics do not match frozen buckets", flush=True)
        return False
    for bucket in BUCKETS:
        item = metrics.get(bucket)
        if not isinstance(item, dict):
            print(f"[FAIL] bucket metric payload missing for {bucket}", flush=True)
            return False
        if item.get("observation_count") != EXPECTED_ELIGIBLE_BY_BUCKET[bucket]:
            print(f"[FAIL] observation count mismatch for {bucket}", flush=True)
            return False
        for field in (
            "mean_abs_next_1h_return",
            "median_abs_next_1h_return",
            "median_relative_spread",
        ):
            if not finite_nonnegative(item.get(field), f"{bucket}.{field}"):
                return False

    diagnostics = payload.get("calendar_year_diagnostics")
    if not isinstance(diagnostics, dict) or set(diagnostics) != set(BUCKETS):
        print("[FAIL] calendar-year diagnostics do not match frozen buckets", flush=True)
        return False
    for bucket in BUCKETS:
        item = diagnostics.get(bucket)
        if not isinstance(item, dict):
            print(f"[FAIL] calendar-year diagnostics missing for {bucket}", flush=True)
            return False
        years = item.get("years")
        if not isinstance(years, dict) or not years:
            print(f"[FAIL] calendar-year rows missing for {bucket}", flush=True)
            return False
        count_sum = 0
        shares: list[float] = []
        for year, year_item in years.items():
            if not isinstance(year_item, dict):
                print(f"[FAIL] invalid calendar-year payload for {bucket}/{year}", flush=True)
                return False
            count = year_item.get("observation_count")
            share = year_item.get("observation_share")
            if not isinstance(count, int) or count <= 0:
                print(f"[FAIL] invalid observation count for {bucket}/{year}", flush=True)
                return False
            if not finite_nonnegative(share, f"{bucket}/{year}.observation_share"):
                return False
            share_value = float(share)
            if share_value > 1.0:
                print(f"[FAIL] observation share exceeds one for {bucket}/{year}", flush=True)
                return False
            for field in ("median_abs_next_1h_return", "median_relative_spread"):
                if not finite_nonnegative(year_item.get(field), f"{bucket}/{year}.{field}"):
                    return False
            count_sum += count
            shares.append(share_value)

        if count_sum != EXPECTED_ELIGIBLE_BY_BUCKET[bucket]:
            print(f"[FAIL] calendar-year count sum mismatch for {bucket}", flush=True)
            return False
        if not math.isclose(sum(shares), 1.0, rel_tol=0.0, abs_tol=1e-12):
            print(f"[FAIL] calendar-year observation shares do not sum to one for {bucket}", flush=True)
            return False
        max_share = item.get("max_calendar_year_observation_share")
        if not finite_nonnegative(max_share, f"{bucket}.max_calendar_year_observation_share"):
            return False
        if not math.isclose(float(max_share), max(shares), rel_tol=0.0, abs_tol=1e-15):
            print(f"[FAIL] maximum calendar-year share mismatch for {bucket}", flush=True)
            return False

    core = metrics["CORE_ACTIVE"]
    off = metrics["OFF_HOURS"]
    expected_movement = float(core["median_abs_next_1h_return"]) > float(
        off["median_abs_next_1h_return"]
    )
    expected_spread = float(core["median_relative_spread"]) <= float(
        off["median_relative_spread"]
    )
    expected_both = expected_movement and expected_spread

    primary = payload.get("primary")
    expected_primary = {
        "movement_inequality_pass": expected_movement,
        "spread_inequality_pass": expected_spread,
        "both_primary_inequalities_pass": expected_both,
    }
    if primary != expected_primary:
        print(
            f"[FAIL] primary Boolean summary mismatch: {primary!r} != {expected_primary!r}",
            flush=True,
        )
        return False

    if expected_both:
        expected_route = (
            "ADVANCE_TO_ECONOMIC_SCREEN",
            "BOTH_PRIMARY_INEQUALITIES_MET",
            "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
        )
    else:
        expected_route = (
            "REJECT",
            "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED",
            "STOP_HYP0004",
        )
    actual_route = (
        payload.get("decision"),
        payload.get("decision_reason"),
        payload.get("next_action"),
    )
    if actual_route != expected_route:
        print(f"[FAIL] frozen decision route mismatch: {actual_route!r}", flush=True)
        return False

    run_context = payload.get("run_context")
    if not isinstance(run_context, dict) or run_context.get("git_commit") != commit:
        print("[FAIL] result does not belong to the exact current reveal commit", flush=True)
        return False

    limitations = payload.get("limitations")
    if not isinstance(limitations, list) or not any(
        "Exact tick-level boundary time is unknown." == str(item) for item in limitations
    ):
        print("[FAIL] frozen timing limitation missing from result", flush=True)
        return False

    print(f"[PASS] RF-020 reveal result contract ({payload['decision']})", flush=True)
    print(
        "CORE_ACTIVE median abs next-1h return: "
        f"{core['median_abs_next_1h_return']}",
        flush=True,
    )
    print(
        "OFF_HOURS median abs next-1h return: "
        f"{off['median_abs_next_1h_return']}",
        flush=True,
    )
    print(f"Movement inequality pass: {expected_movement}", flush=True)
    print(
        f"CORE_ACTIVE median relative spread: {core['median_relative_spread']}",
        flush=True,
    )
    print(
        f"OFF_HOURS median relative spread: {off['median_relative_spread']}",
        flush=True,
    )
    print(f"Spread inequality pass: {expected_spread}", flush=True)
    print(f"Both primary inequalities pass: {expected_both}", flush=True)
    print(f"Next action: {payload['next_action']}", flush=True)
    print(f"Result SHA-256: {sha256_file(ROOT / RESULT)}", flush=True)
    return True


def reveal_once(commit: str) -> bool:
    print("\n== RF-020 one-time HYP-0004 PROTO-01 reveal ==", flush=True)
    if (ROOT / RESULT).is_file():
        print("Existing local result found; validating without recomputation.", flush=True)
    else:
        if not run("exact frozen HYP-0004 PROTO-01 runner", [sys.executable, str(RUNNER)]):
            return False

    try:
        payload = json.loads((ROOT / RESULT).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot load reveal result: {exc}", flush=True)
        return False
    if not isinstance(payload, dict):
        print("[FAIL] reveal result top level must be a mapping", flush=True)
        return False
    return validate_result(payload, commit)


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    commit = git_output("rev-parse", "HEAD")
    print(f"Commit: {commit}")

    emit_progress(45)
    frozen = check_frozen_inputs()

    emit_progress(60)
    governance = run(
        "RF-020 HYP-0004 reveal governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(75)
    full_ci = run(
        "full ATS Local CI before RF-020 HYP-0004 reveal",
        [sys.executable, "tools/verify_repo.py"],
    )

    if not all((frozen, governance, full_ci)):
        print("\nATS CURRENT TASK CHECK: FAIL", flush=True)
        return 1

    emit_progress(90)
    revealed = reveal_once(commit)

    if revealed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if revealed else 'FAIL'}", flush=True)
    return 0 if revealed else 1


if __name__ == "__main__":
    raise SystemExit(main())
