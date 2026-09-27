#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-018"
TASK_NAME = "HYP-0004 development data freeze"
CANONICAL_RESULT = Path("reports/research/HYP-0004-DEVELOPMENT-DATA-PREP-result.json")
MANIFEST = Path("data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001.yaml")
SCHEMA = Path("data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV.schema.json")
DATA_FEASIBILITY = Path("research/reviews/HYP-0004-DATA-FEASIBILITY.md")
PROTOTYPE = Path("research/reviews/HYP-0004-PROTOTYPE-01.md")
EXPECTED_RESULT_SHA256 = "4902235ce2e01ef12a325b327ef43027c95fd709ed7c4239ab08897a6575f6ea"


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_freeze_artifacts() -> bool:
    print("\n== RF-018 HYP-0004 development data freeze artifacts ==", flush=True)
    required = (CANONICAL_RESULT, MANIFEST, SCHEMA, DATA_FEASIBILITY)
    missing = [str(path) for path in required if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing required freeze artifact: {path}", flush=True)
        return False

    if (ROOT / PROTOTYPE).exists():
        print("[FAIL] RF-018 must not create the RF-019 prototype artifact", flush=True)
        return False

    result_path = ROOT / CANONICAL_RESULT
    actual_result_sha256 = sha256_file(result_path)
    if actual_result_sha256 != EXPECTED_RESULT_SHA256:
        print(
            f"[FAIL] canonical RF-017 result SHA-256 mismatch: "
            f"{actual_result_sha256} != {EXPECTED_RESULT_SHA256}",
            flush=True,
        )
        return False

    try:
        payload = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot load canonical RF-017 result: {exc}", flush=True)
        return False

    checks = {
        "task_id": "ATS2-RF-017",
        "hypothesis_id": "HYP-0004",
        "git_commit": "ae9767a71b3860e55d345afb34b2f9c18b5dd063",
        "preparation_decision": "READY_FOR_DEVELOPMENT_DATA_FREEZE",
        "development_dataset_id": "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001",
        "development_dataset_version": "1.0.0",
        "derived_row_count": 112900,
        "derived_csv_sha256": ("3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6"),
        "eligible_exact_next_hour_count": 111938,
        "ineligible_closed_market_next_hour_count": 940,
        "ineligible_missing_expected_next_hour_count": 21,
        "ineligible_dataset_end_count": 1,
        "boundary_open_crossing_count": 0,
        "duplicate_event_time_count": 0,
        "out_of_order_event_time_count": 0,
        "malformed_boundary_row_count": 0,
        "boundary_availability_mode": "H1_OPEN_PROXY_AT_EVENT_TIME",
        "exact_tick_boundary_time_known": False,
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    }
    for key, expected in checks.items():
        actual = payload.get(key)
        if actual != expected:
            print(
                f"[FAIL] canonical result mismatch for {key}: {actual!r} != {expected!r}",
                flush=True,
            )
            return False

    if payload.get("eligible_rows_by_bucket") != {
        "CORE_ACTIVE": 47012,
        "OFF_HOURS": 46737,
        "TRANSITION": 18189,
    }:
        print("[FAIL] frozen eligible bucket counts changed", flush=True)
        return False

    denominator = (
        payload["eligible_exact_next_hour_count"]
        + payload["ineligible_closed_market_next_hour_count"]
        + payload["ineligible_missing_expected_next_hour_count"]
        + payload["ineligible_dataset_end_count"]
    )
    if denominator != payload["derived_row_count"]:
        print("[FAIL] exact-next-hour denominator does not reconcile", flush=True)
        return False

    manifest = (ROOT / MANIFEST).read_text(encoding="utf-8")
    for marker in (
        "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001",
        "3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6",
        "112,900",
        "111,938",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    ):
        if marker not in manifest:
            print(f"[FAIL] frozen manifest marker missing: {marker}", flush=True)
            return False

    review = (ROOT / DATA_FEASIBILITY).read_text(encoding="utf-8")
    for marker in (
        "RF-018 development data freeze update",
        "FREEZE_DEVELOPMENT_DATASET",
        "111938 + 940 + 21 + 1 = 112900",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "ATS2-RF-019 — HYP-0004 PROTO-01 freeze",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    ):
        if marker not in review:
            print(f"[FAIL] Data Feasibility freeze marker missing: {marker}", flush=True)
            return False

    print(
        "[PASS] RF-018 froze the exact HYP-0004 development dataset without outcome computation",
        flush=True,
    )
    return True


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    print(f"Commit: {commit}")

    emit_progress(45)
    artifacts = check_freeze_artifacts()

    emit_progress(65)
    governance = run(
        "RF-018 HYP-0004 development data freeze governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(80)
    full_ci = run(
        "full ATS Local CI for RF-018 HYP-0004 development data freeze",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((artifacts, governance, full_ci))
    if passed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
