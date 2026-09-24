#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from ats.schemas.dataset_manifest import load_dataset_manifest

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-009"
TASK_NAME = "HYP-0003 development data freeze"
RF008_RESULT = Path("reports/research/HYP-0003-DEVELOPMENT-DATA-PREP-result.json")
MANIFEST_PATH = Path("data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001.yaml")
SCHEMA_PATH = Path("data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV.schema.json")
PREPARED_PATH = Path("data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv")
DATA_FEASIBILITY_PATH = Path("research/reviews/HYP-0003-DATA-FEASIBILITY.md")
EXPECTED_RF008_COMMIT = "63e1bc9c7e1ba2e001ecdd9918244d83db0e58c3"
EXPECTED_SOURCE_SHA256 = "9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a"
EXPECTED_PREPARED_SHA256 = "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2"
EXPECTED_DATASET_ID = "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001"
EXPECTED_DATASET_VERSION = "1.0.0"
EXPECTED_SCHEMA_FIELDS = (
    "event_time",
    "availability_time",
    "currency",
    "source_symbol",
    "source_orientation",
    "sequence",
    "bid_open",
    "bid_high",
    "bid_low",
    "bid_close",
    "ask_open",
    "ask_high",
    "ask_low",
    "ask_close",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def check_freeze_artifacts() -> bool:
    print("\n== RF-009 HYP-0003 development data freeze artifacts ==", flush=True)
    required = (RF008_RESULT, MANIFEST_PATH, SCHEMA_PATH, DATA_FEASIBILITY_PATH, PREPARED_PATH)
    missing = [str(path) for path in required if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"[FAIL] missing required artifact: {path}", flush=True)
        return False
    print("[PASS] RF-009 HYP-0003 development data freeze artifacts", flush=True)
    return True


def check_canonical_freeze() -> bool:
    print("\n== RF-009 canonical RF-008 result / manifest / schema / bytes ==", flush=True)
    try:
        result = json.loads((ROOT / RF008_RESULT).read_text(encoding="utf-8"))
        schema = json.loads((ROOT / SCHEMA_PATH).read_text(encoding="utf-8"))
        manifest = load_dataset_manifest(ROOT / MANIFEST_PATH)
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"[FAIL] cannot load RF-009 freeze artifacts: {exc}", flush=True)
        return False

    checks = {
        "task_id": "ATS2-RF-008",
        "hypothesis_id": "HYP-0003",
        "preparation_commit": EXPECTED_RF008_COMMIT,
        "launcher_status": "PASS",
        "preparation_decision": "READY_FOR_DEVELOPMENT_DATA_FREEZE",
        "development_dataset_id": EXPECTED_DATASET_ID,
        "development_dataset_version": EXPECTED_DATASET_VERSION,
        "source_objects_expected": 3906,
        "source_objects_acquired": 3906,
        "source_objects_missing": 0,
        "source_bundle_sha256": EXPECTED_SOURCE_SHA256,
        "prepared_csv_sha256": EXPECTED_PREPARED_SHA256,
        "prepared_rows": 1014509,
        "eligible_monthly_ranking_points_ge6": 207,
        "eligible_longest_12_12_geometry_points": 184,
        "protected_tail_source_objects_requested": 0,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    }
    for key, expected in checks.items():
        actual = result.get(key)
        if actual != expected:
            print(
                f"[FAIL] canonical RF-008 result mismatch for {key}: "
                f"{actual!r} != {expected!r}",
                flush=True,
            )
            return False

    if (
        manifest.dataset_id != EXPECTED_DATASET_ID
        or manifest.dataset_version != EXPECTED_DATASET_VERSION
    ):
        print("[FAIL] Dataset Manifest identity mismatch", flush=True)
        return False
    if manifest.storage.location != PREPARED_PATH.as_posix():
        print("[FAIL] Dataset Manifest storage path mismatch", flush=True)
        return False
    if manifest.integrity.digest != EXPECTED_PREPARED_SHA256:
        print("[FAIL] Dataset Manifest prepared-data digest mismatch", flush=True)
        return False
    if manifest.source.snapshot_reference != f"source-bundle-sha256:{EXPECTED_SOURCE_SHA256}":
        print("[FAIL] Dataset Manifest source snapshot mismatch", flush=True)
        return False

    if tuple(schema.get("required", ())) != EXPECTED_SCHEMA_FIELDS:
        print("[FAIL] development schema required fields mismatch", flush=True)
        return False
    if schema.get("additionalProperties") is not False:
        print("[FAIL] development schema must reject additional properties", flush=True)
        return False

    actual_prepared_sha = sha256_file(ROOT / PREPARED_PATH)
    if actual_prepared_sha != EXPECTED_PREPARED_SHA256:
        print(f"[FAIL] prepared CSV SHA256 mismatch: {actual_prepared_sha}", flush=True)
        return False

    feasibility = (ROOT / DATA_FEASIBILITY_PATH).read_text(encoding="utf-8")
    for marker in (
        "RF-009 development data freeze update",
        "FREEZE_DEVELOPMENT_DATASET",
        EXPECTED_SOURCE_SHA256,
        EXPECTED_PREPARED_SHA256,
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    ):
        if marker not in feasibility:
            print(f"[FAIL] Data Feasibility freeze marker missing: {marker}", flush=True)
            return False

    print("[PASS] RF-009 canonical freeze matches RF-008 OWNER PASS evidence", flush=True)
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

    emit_progress(60)
    canonical = artifacts and check_canonical_freeze()

    emit_progress(75)
    governance = run(
        "RF-009 HYP-0003 freeze governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(85)
    full_ci = run(
        "full ATS Local CI for RF-009 development data freeze",
        [sys.executable, "tools/verify_repo.py"],
    )

    passed = all((artifacts, canonical, governance, full_ci))
    if passed:
        emit_progress(100)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
