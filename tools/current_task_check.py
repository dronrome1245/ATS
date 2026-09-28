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
TASK_ID = "ATS2-RF-021"
TASK_NAME = "HYP-0004 PROTO-01 result canonicalization and routing"
PROTO = Path("research/reviews/HYP-0004-PROTOTYPE-01.md")
RUNNER = Path("tools/hyp0004_proto01.py")
RESULT = Path("reports/research/HYP-0004-PROTOTYPE-01-result.json")
NEXT_HYPOTHESIS = Path("research/hypotheses/HYP-0005.md")
GITATTRIBUTES = Path(".gitattributes")

EXPECTED_RUNNER_GIT_BLOB = "cbc9a46bf5e5296615f51c0ea564153968bc2a55"
EXPECTED_RESULT_SHA256 = "1c9b2cb1a1628599e935ee61fd8c9b152d7bd3447969b065c920c8d13e3e5230"
EXPECTED_REVEAL_COMMIT = "60371d16b71c1e7d1fb0ccd83c5104984e4b740a"
EXPECTED_DATASET_SHA256 = "3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6"
EXPECTED_ELIGIBLE_BY_BUCKET = {
    "CORE_ACTIVE": 47_012,
    "OFF_HOURS": 46_737,
    "TRANSITION": 18_189,
}
EXPECTED_PRIMARY_METRICS = {
    "CORE_ACTIVE": {
        "median_abs_next_1h_return": 0.0006982268977376305,
        "median_relative_spread": 4.018781312113313e-05,
    },
    "OFF_HOURS": {
        "median_abs_next_1h_return": 0.0003493061509638462,
        "median_relative_spread": 6.690913261869393e-05,
    },
}


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


def check_result_contract(payload: dict[str, Any]) -> bool:
    fixed_fields = {
        "schema_version": "hyp0004-proto01-result-1",
        "hypothesis_id": "HYP-0004",
        "prototype_sequence": "PROTO-01",
        "evidence_class": "EXPLORATORY_PROTOTYPE",
        "measurement_label": "STRUCTURAL_H1_OPEN_PROXY_NO_TRADING_PNL",
        "decision": "ADVANCE_TO_ECONOMIC_SCREEN",
        "decision_reason": "BOTH_PRIMARY_INEQUALITIES_MET",
        "next_action": "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
    }
    for key, expected in fixed_fields.items():
        if payload.get(key) != expected:
            print(f"[FAIL] canonical result mismatch for {key}", flush=True)
            return False

    run_context = payload.get("run_context")
    if not isinstance(run_context, dict) or run_context.get("git_commit") != EXPECTED_REVEAL_COMMIT:
        print("[FAIL] canonical result reveal commit mismatch", flush=True)
        return False

    dataset = payload.get("dataset")
    if not isinstance(dataset, dict):
        print("[FAIL] canonical result dataset identity missing", flush=True)
        return False
    dataset_checks = {
        "dataset_id": "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001",
        "dataset_version": "1.0.0",
        "prepared_csv_sha256": EXPECTED_DATASET_SHA256,
        "boundary_availability_mode": "H1_OPEN_PROXY_AT_EVENT_TIME",
        "exact_tick_boundary_time_known": False,
        "eligible_exact_next_hour_count": 111_938,
    }
    for key, expected in dataset_checks.items():
        if dataset.get(key) != expected:
            print(f"[FAIL] canonical result dataset mismatch for {key}", flush=True)
            return False

    geometry = payload.get("geometry")
    if not isinstance(geometry, dict):
        print("[FAIL] canonical result geometry missing", flush=True)
        return False
    if geometry.get("eligible_count") != 111_938:
        print("[FAIL] canonical eligible count mismatch", flush=True)
        return False
    if geometry.get("eligible_by_bucket") != EXPECTED_ELIGIBLE_BY_BUCKET:
        print("[FAIL] canonical eligible bucket geometry mismatch", flush=True)
        return False
    if (
        geometry.get("ineligible_closed_market_next_hour_count") != 940
        or geometry.get("ineligible_missing_expected_next_hour_count") != 21
        or geometry.get("ineligible_dataset_end_count") != 1
    ):
        print("[FAIL] canonical ineligible geometry mismatch", flush=True)
        return False

    metrics = payload.get("bucket_metrics")
    if not isinstance(metrics, dict):
        print("[FAIL] canonical bucket metrics missing", flush=True)
        return False
    for bucket, expected_fields in EXPECTED_PRIMARY_METRICS.items():
        item = metrics.get(bucket)
        if not isinstance(item, dict):
            print(f"[FAIL] canonical bucket metrics missing for {bucket}", flush=True)
            return False
        if item.get("observation_count") != EXPECTED_ELIGIBLE_BY_BUCKET[bucket]:
            print(f"[FAIL] canonical bucket count mismatch for {bucket}", flush=True)
            return False
        for field, expected in expected_fields.items():
            actual = item.get(field)
            if (
                isinstance(actual, bool)
                or not isinstance(actual, (int, float))
                or not math.isclose(float(actual), expected, rel_tol=0.0, abs_tol=0.0)
            ):
                print(f"[FAIL] canonical metric mismatch for {bucket}.{field}", flush=True)
                return False

    primary = payload.get("primary")
    if primary != {
        "both_primary_inequalities_pass": True,
        "movement_inequality_pass": True,
        "spread_inequality_pass": True,
    }:
        print("[FAIL] canonical primary Boolean summary mismatch", flush=True)
        return False

    limitations = payload.get("limitations")
    if not isinstance(limitations, list):
        print("[FAIL] canonical limitations missing", flush=True)
        return False
    required_limitations = (
        "H1_OPEN_PROXY_AT_EVENT_TIME is a development approximation.",
        "Exact tick-level boundary time is unknown.",
        "The result is a structural distribution test, not a directional trading rule.",
        "Development data are exploratory and are not validation or independent evidence.",
    )
    for marker in required_limitations:
        if marker not in limitations:
            print(f"[FAIL] canonical limitation missing: {marker}", flush=True)
            return False

    return True


def check_canonicalization_and_routing() -> bool:
    print("\n== RF-021 HYP-0004 result canonicalization and routing ==", flush=True)

    for path in (PROTO, RUNNER, RESULT, GITATTRIBUTES):
        if not (ROOT / path).is_file():
            print(f"[FAIL] missing RF-021 artifact: {path}", flush=True)
            return False

    if (ROOT / NEXT_HYPOTHESIS).exists():
        print("[FAIL] RF-021 must not create HYP-0005 before RF-022", flush=True)
        return False

    runner_blob = git_output("rev-parse", f"HEAD:{RUNNER.as_posix()}")
    if runner_blob != EXPECTED_RUNNER_GIT_BLOB:
        print("[FAIL] frozen HYP-0004 runner changed after reveal", flush=True)
        return False

    result_sha256 = sha256_file(ROOT / RESULT)
    if result_sha256 != EXPECTED_RESULT_SHA256:
        print(
            f"[FAIL] canonical result SHA-256 mismatch: "
            f"{result_sha256} != {EXPECTED_RESULT_SHA256}",
            flush=True,
        )
        return False

    attributes = (ROOT / GITATTRIBUTES).read_text(encoding="utf-8")
    if "reports/research/HYP-0004-PROTOTYPE-01-result.json -text" not in attributes:
        print("[FAIL] canonical result exact-byte Git attribute missing", flush=True)
        return False

    try:
        payload = json.loads((ROOT / RESULT).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot read canonical HYP-0004 result: {exc}", flush=True)
        return False
    if not isinstance(payload, dict) or not check_result_contract(payload):
        return False

    prototype = (ROOT / PROTO).read_text(encoding="utf-8")
    required_proto_markers = (
        "COMPLETED / DEVELOPMENT_PASS",
        EXPECTED_RESULT_SHA256,
        EXPECTED_REVEAL_COMMIT,
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "BOTH_PRIMARY_INEQUALITIES_MET",
        "HYP-0005 — EUR/USD Fixed-UTC Intraday Activity Contrast Confirmatory Replication",
        "DEVELOPMENT_REVEALED_STRUCTURAL_PASS_CONFIRMATION_REQUIRED",
        "ATS2-RF-022 — HYP-0005 confirmatory hypothesis formation",
    )
    for marker in required_proto_markers:
        if marker not in prototype:
            print(f"[FAIL] RF-021 prototype routing marker missing: {marker}", flush=True)
            return False

    print(
        "[PASS] RF-021 preserved the exact HYP-0004 result and selected confirmatory routing",
        flush=True,
    )
    print(f"Canonical result SHA-256: {result_sha256}", flush=True)
    return True


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    print(f"Commit: {git_output('rev-parse', 'HEAD')}")

    emit_progress(45)
    canonical = check_canonicalization_and_routing()

    emit_progress(65)
    governance = run(
        "RF-021 HYP-0004 result routing governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-021 HYP-0004 result canonicalization",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((canonical, governance, full_ci))
    if passed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
