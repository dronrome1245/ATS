#!/usr/bin/env python3
"""Run the verification package for the currently closing ATS task."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-011"
TASK_NAME = "HYP-0003 PROTO-01 reveal"
RUNNER = Path("tools/hyp0003_proto01.py")
PROTO = Path("research/reviews/HYP-0003-PROTOTYPE-01.md")
DATA = Path("data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv")
RESULT = Path("reports/local_ci/HYP0003_PROTO01_RESULT.json")
EXPECTED_RUNNER_GIT_BLOB = "d65746f39476ba3fee8cf59acfd0b2f82af9c663"
EXPECTED_DATASET_SHA256 = "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2"
EXPECTED_SOURCE_BUNDLE_SHA256 = "9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a"
FORMATION_MONTHS = [1, 3, 6, 9, 12]
HOLDING_MONTHS = [1, 3, 6, 9, 12]
VALID_DECISIONS = {
    "ADVANCE_TO_ECONOMIC_SCREEN": "CREATE_NEW_CONFIRMATORY_HYPOTHESIS_BEFORE_R4",
    "REJECT": "STOP_HYP0003",
    "PARK": "PARK",
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


def check_frozen_inputs() -> bool:
    print("\n== RF-011 frozen reveal inputs ==", flush=True)
    for path in (RUNNER, PROTO, DATA):
        if not (ROOT / path).is_file():
            print(f"[FAIL] missing frozen input: {path}", flush=True)
            return False
    runner_blob = git_output("hash-object", str(RUNNER))
    if runner_blob != EXPECTED_RUNNER_GIT_BLOB:
        print(
            f"[FAIL] frozen runner blob mismatch: {runner_blob} != {EXPECTED_RUNNER_GIT_BLOB}",
            flush=True,
        )
        return False
    if sha256_file(ROOT / DATA) != EXPECTED_DATASET_SHA256:
        print("[FAIL] frozen development CSV SHA256 mismatch", flush=True)
        return False
    proto_text = (ROOT / PROTO).read_text(encoding="utf-8")
    for marker in ("FROZEN_PRE_REVEAL", "PENDING_RF011_REVEAL", "25 / 25"):
        if marker not in proto_text:
            print(f"[FAIL] frozen prototype marker missing: {marker}", flush=True)
            return False
    print("[PASS] exact RF-010 frozen runner/protocol/data identity", flush=True)
    return True


def validate_result(payload: dict[str, Any], commit: str) -> bool:
    checks = {
        "schema_version": "hyp0003-proto01-result-1",
        "hypothesis_id": "HYP-0003",
        "prototype_sequence": "PROTO-01",
        "evidence_class": "EXPLORATORY_PROTOTYPE",
        "economic_label": "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
    }
    for key, expected in checks.items():
        if payload.get(key) != expected:
            print(f"[FAIL] result mismatch for {key}: {payload.get(key)!r}", flush=True)
            return False

    grid = payload.get("grid")
    if not isinstance(grid, dict):
        print("[FAIL] result grid missing", flush=True)
        return False
    if grid.get("formation_months") != FORMATION_MONTHS:
        print("[FAIL] formation grid mismatch", flush=True)
        return False
    if grid.get("holding_months") != HOLDING_MONTHS:
        print("[FAIL] holding grid mismatch", flush=True)
        return False
    if grid.get("declared_cell_count") != 25:
        print("[FAIL] declared cell count mismatch", flush=True)
        return False

    cells = payload.get("cells")
    expected_pairs = [(f, h) for f in FORMATION_MONTHS for h in HOLDING_MONTHS]
    if not isinstance(cells, list) or len(cells) != 25:
        print("[FAIL] result must retain exactly 25 cells", flush=True)
        return False
    actual_pairs = [
        (cell.get("formation_months"), cell.get("holding_months"))
        for cell in cells
        if isinstance(cell, dict)
    ]
    if actual_pairs != expected_pairs:
        print("[FAIL] result cell grid/order mismatch", flush=True)
        return False

    dataset = payload.get("dataset")
    if not isinstance(dataset, dict):
        print("[FAIL] result dataset identity missing", flush=True)
        return False
    if dataset.get("prepared_csv_sha256") != EXPECTED_DATASET_SHA256:
        print("[FAIL] result dataset SHA256 mismatch", flush=True)
        return False
    if dataset.get("source_bundle_sha256") != EXPECTED_SOURCE_BUNDLE_SHA256:
        print("[FAIL] result source bundle SHA256 mismatch", flush=True)
        return False

    run_context = payload.get("run_context")
    if not isinstance(run_context, dict) or run_context.get("git_commit") != commit:
        print("[FAIL] result does not belong to exact current commit", flush=True)
        return False

    decision = payload.get("decision")
    if decision not in VALID_DECISIONS:
        print(f"[FAIL] invalid prototype decision: {decision!r}", flush=True)
        return False
    if payload.get("next_action") != VALID_DECISIONS[decision]:
        print("[FAIL] result next_action inconsistent with frozen decision", flush=True)
        return False

    breadth = payload.get("breadth")
    if not isinstance(breadth, dict):
        print("[FAIL] breadth summary missing", flush=True)
        return False

    print(f"[PASS] RF-011 reveal result contract ({decision})", flush=True)
    print(f"Result SHA-256: {sha256_file(ROOT / RESULT)}", flush=True)
    return True


def reveal_once(commit: str) -> bool:
    print("\n== RF-011 one-time HYP-0003 PROTO-01 reveal ==", flush=True)
    if (ROOT / RESULT).is_file():
        print("Existing local result found; validating without recomputation.", flush=True)
    else:
        if not run("exact frozen HYP-0003 PROTO-01 runner", [sys.executable, str(RUNNER)]):
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
        "RF-011 HYP-0003 reveal governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(75)
    full_ci = run(
        "full ATS Local CI before RF-011 reveal",
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
