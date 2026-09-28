#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-023"
TASK_NAME = "HYP-0005 confirmatory Data Feasibility preparation"

HYPOTHESIS = Path("research/hypotheses/HYP-0005.md")
PREP_PROTOCOL = Path("research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md")
PREP_TOOL = Path("tools/hyp0005_data_feasibility.py")
PREP_TEST = Path("tests/test_hyp0005_data_feasibility.py")
LOCAL_RESULT = Path("reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP.json")
DERIVED_DATA = Path("data/derived/HYP-0005-CONF-01-EURUSD-H1.csv")
FUTURE_REVIEW = Path("research/reviews/HYP-0005-DATA-FEASIBILITY.md")
FUTURE_MANIFEST = Path("data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001.yaml")

EXPECTED_DATASET_ID = "DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001"
EXPECTED_DATASET_VERSION = "1.0.0"
EXPECTED_SEGMENTS = [
    {
        "segment_id": "LEFT_UNSEEN",
        "start": "2003-05-04T21:00:00Z",
        "end_exclusive": "2003-08-03T21:00:00Z",
    },
    {
        "segment_id": "RIGHT_UNSEEN",
        "start": "2026-09-01T00:00:00Z",
        "end_exclusive": "2026-09-26T00:00:00Z",
    },
]
VALID_DECISIONS = {
    "READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE",
    "INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


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


def check_staged_contract() -> bool:
    print("\n== RF-023 staged confirmatory Data Feasibility contract ==", flush=True)

    for path in (HYPOTHESIS, PREP_PROTOCOL, PREP_TOOL, PREP_TEST):
        if not (ROOT / path).is_file():
            print(f"[FAIL] missing RF-023 artifact: {path}", flush=True)
            return False

    for path in (FUTURE_REVIEW, FUTURE_MANIFEST):
        if (ROOT / path).exists():
            print(f"[FAIL] RF-023 must not pre-create RF-024 freeze artifact: {path}", flush=True)
            return False

    protocol = (ROOT / PREP_PROTOCOL).read_text(encoding="utf-8")
    markers = (
        "PREPARATION_PROTOCOL_FROZEN",
        "2003-05-04T21:00:00Z <= event_time < 2003-08-03T21:00:00Z",
        "2026-09-01T00:00:00Z <= event_time < 2026-09-26T00:00:00Z",
        "2003-08-03T21:00:00Z <= event_time < 2026-09-01T00:00:00Z",
        "DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "NO_CONFIRMATORY_OUTCOME_COMPUTED",
        "READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE",
        "INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY",
        "ATS2-RF-024 — HYP-0005 confirmatory Data Feasibility freeze",
    )
    for marker in markers:
        if marker not in protocol:
            print(f"[FAIL] RF-023 protocol marker missing: {marker}", flush=True)
            return False

    print("[PASS] RF-023 staged contract preserves the confirmatory information boundary", flush=True)
    return True


def _valid_nonnegative_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def validate_local_result(payload: dict[str, Any], commit: str) -> bool:
    fixed = {
        "schema_version": "hyp0005-data-feasibility-prep-1",
        "task_id": TASK_ID,
        "hypothesis_id": "HYP-0005",
        "git_commit": commit,
        "confirmatory_dataset_id": EXPECTED_DATASET_ID,
        "confirmatory_dataset_version": EXPECTED_DATASET_VERSION,
        "source_provider": "DUKASCOPY",
        "source_symbol": "EURUSD",
        "source_orientation": "DIRECT",
        "source_month_count": 5,
        "source_object_count": 10,
        "segments": EXPECTED_SEGMENTS,
        "consumed_project_interval_start": "2003-08-03T21:00:00Z",
        "consumed_project_interval_end_exclusive": "2026-09-01T00:00:00Z",
        "boundary_availability_mode": "H1_OPEN_PROXY_AT_EVENT_TIME",
        "exact_tick_boundary_time_known": False,
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_CONFIRMATORY_OUTCOME_COMPUTED",
    }
    for key, expected in fixed.items():
        if payload.get(key) != expected:
            print(
                f"[FAIL] RF-023 local result mismatch for {key}: "
                f"{payload.get(key)!r} != {expected!r}",
                flush=True,
            )
            return False

    decision = payload.get("preparation_decision")
    if decision not in VALID_DECISIONS:
        print(f"[FAIL] invalid RF-023 preparation decision: {decision!r}", flush=True)
        return False

    for key in ("source_bundle_sha256", "derived_csv_sha256"):
        value = payload.get(key)
        if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
            print(f"[FAIL] invalid/missing {key}", flush=True)
            return False

    if not _valid_nonnegative_int(payload.get("derived_row_count")):
        print("[FAIL] invalid derived_row_count", flush=True)
        return False
    if payload["derived_row_count"] <= 0:
        print("[FAIL] RF-023 produced zero confirmatory rows", flush=True)
        return False

    source_files = payload.get("source_files")
    if not isinstance(source_files, list) or len(source_files) != 10:
        print("[FAIL] RF-023 source file inventory must contain exactly 10 objects", flush=True)
        return False
    identities: set[tuple[str, str]] = set()
    for item in source_files:
        if not isinstance(item, dict):
            print("[FAIL] invalid source-file inventory entry", flush=True)
            return False
        side = item.get("side")
        month = item.get("month")
        digest = item.get("sha256")
        relative_path = item.get("relative_path")
        if side not in {"BID", "ASK"} or not isinstance(month, str):
            print("[FAIL] invalid source-file side/month identity", flush=True)
            return False
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            print("[FAIL] invalid source-file SHA-256", flush=True)
            return False
        if not isinstance(relative_path, str):
            print("[FAIL] invalid source-file relative path", flush=True)
            return False
        source_path = ROOT / relative_path
        if not source_path.is_file() or sha256_file(source_path) != digest:
            print(f"[FAIL] local frozen source object mismatch: {relative_path}", flush=True)
            return False
        identities.add((month, side))
    if len(identities) != 10:
        print("[FAIL] duplicate source month/side identities", flush=True)
        return False

    geometry = payload.get("geometry")
    if not isinstance(geometry, dict):
        print("[FAIL] RF-023 geometry missing", flush=True)
        return False
    for key in (
        "eligible_exact_next_hour_count",
        "ineligible_closed_market_next_hour_count",
        "ineligible_missing_expected_next_hour_count",
        "ineligible_segment_end_count",
    ):
        if not _valid_nonnegative_int(geometry.get(key)):
            print(f"[FAIL] invalid geometry field: {key}", flush=True)
            return False

    eligible_by_bucket = geometry.get("eligible_rows_by_bucket")
    eligible_by_segment = geometry.get("eligible_rows_by_segment")
    if not isinstance(eligible_by_bucket, dict) or set(eligible_by_bucket) != {
        "CORE_ACTIVE",
        "TRANSITION",
        "OFF_HOURS",
    }:
        print("[FAIL] eligible bucket geometry mismatch", flush=True)
        return False
    if not isinstance(eligible_by_segment, dict) or set(eligible_by_segment) != {
        "LEFT_UNSEEN",
        "RIGHT_UNSEEN",
    }:
        print("[FAIL] eligible segment geometry mismatch", flush=True)
        return False
    if any(not _valid_nonnegative_int(value) for value in eligible_by_bucket.values()):
        print("[FAIL] invalid eligible bucket counts", flush=True)
        return False
    if any(not _valid_nonnegative_int(value) for value in eligible_by_segment.values()):
        print("[FAIL] invalid eligible segment counts", flush=True)
        return False

    if decision == "READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE":
        if eligible_by_bucket["CORE_ACTIVE"] <= 0 or eligible_by_bucket["OFF_HOURS"] <= 0:
            print("[FAIL] ready decision lacks primary-bucket geometry", flush=True)
            return False
        if any(eligible_by_segment[name] <= 0 for name in ("LEFT_UNSEEN", "RIGHT_UNSEEN")):
            print("[FAIL] ready decision lacks both unseen segments", flush=True)
            return False

    if not (ROOT / DERIVED_DATA).is_file():
        print("[FAIL] RF-023 derived CSV missing", flush=True)
        return False
    if sha256_file(ROOT / DERIVED_DATA) != payload["derived_csv_sha256"]:
        print("[FAIL] RF-023 derived CSV SHA-256 mismatch", flush=True)
        return False

    with (ROOT / DERIVED_DATA).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
    if "abs_next_1h_return" in header or "relative_spread" in header:
        print("[FAIL] derived CSV contains prohibited HYP-0005 outcome columns", flush=True)
        return False
    for required in ("confirmatory_segment", "utc_bucket", "bid_open", "ask_open"):
        if required not in header:
            print(f"[FAIL] derived CSV missing required field: {required}", flush=True)
            return False

    return True


def prepare_or_validate(commit: str) -> bool:
    print("\n== RF-023 exact confirmatory data preparation ==", flush=True)

    existing: dict[str, Any] | None = None
    if (ROOT / LOCAL_RESULT).is_file():
        try:
            loaded = json.loads((ROOT / LOCAL_RESULT).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            loaded = None
        if isinstance(loaded, dict) and loaded.get("git_commit") == commit:
            existing = loaded

    if existing is not None:
        print("Existing exact-commit local preparation result found; validating without acquisition.")
        payload = existing
    else:
        if not run(
            "RF-023 HYP-0005 source acquisition and confirmatory preparation",
            [sys.executable, str(PREP_TOOL)],
        ):
            return False
        try:
            payload = json.loads((ROOT / LOCAL_RESULT).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[FAIL] cannot load RF-023 local preparation result: {exc}", flush=True)
            return False

    if not isinstance(payload, dict) or not validate_local_result(payload, commit):
        return False

    result_sha = sha256_file(ROOT / LOCAL_RESULT)
    print(f"[PASS] RF-023 local preparation result ({payload['preparation_decision']})", flush=True)
    print(f"Local result SHA-256: {result_sha}", flush=True)
    print(f"Source bundle SHA-256: {payload['source_bundle_sha256']}", flush=True)
    print(f"Derived CSV SHA-256: {payload['derived_csv_sha256']}", flush=True)
    print(f"Derived rows: {payload['derived_row_count']}", flush=True)
    print(f"Information boundary: {payload['information_boundary']}", flush=True)
    return True


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    commit = git_output("rev-parse", "HEAD")
    print(f"Commit: {commit}")

    emit_progress(40)
    staged = check_staged_contract()

    emit_progress(55)
    governance = run(
        "RF-023 HYP-0005 preparation governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(70)
    full_ci = run(
        "full ATS Local CI before RF-023 source acquisition",
        [sys.executable, "tools/verify_repo.py"],
    )

    if not all((staged, governance, full_ci)):
        print("\nATS CURRENT TASK CHECK: FAIL", flush=True)
        return 1

    emit_progress(85)
    prepared = prepare_or_validate(commit)

    if prepared:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if prepared else 'FAIL'}", flush=True)
    return 0 if prepared else 1


if __name__ == "__main__":
    raise SystemExit(main())
