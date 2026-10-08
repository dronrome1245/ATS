#!/usr/bin/env python3
"""RF-029: freeze HYP-0006 PROTO-01 without computing a market outcome."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-029"
TASK_NAME = "HYP-0006 PROTO-01 pre-reveal freeze"

FREEZE_RESULT = ROOT / "reports/local_ci/HYP0006_DATA_TOLERANCE_FREEZE.json"
GEOMETRY_CSV = ROOT / "data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv"
PROTOTYPE_REVIEW = ROOT / "research/reviews/HYP-0006-PROTOTYPE-01.md"
PROTOTYPE_RUNNER = ROOT / "tools/hyp0006_proto01.py"
PROTOTYPE_TEST = ROOT / "tests/test_hyp0006_proto01.py"

RF028_COMMIT = "e7f05a0d237c4d78a8a0edb93710619e6ad2ba00"
RF028_JSON_SHA256 = "1b575682b959070f4a0981b7cd13d70626f1e169d221d0c9fb2383fc679fd5fb"
FROZEN_GEOMETRY_SHA256 = "e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034"
FROZEN_SOURCE_SHA256 = "5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425"
FROZEN_RUNNER_GIT_BLOB = "a3ac99eeea0159050364da156194a4753c4f5966"

FROZEN_BLOBS = {
    "research/hypotheses/HYP-0005.md": "ebbbc89187c911485c1568dc11f5f2f9e703718a",
    "research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md": (
        "c15b2b67700dd46fc592f1208731ce6b42f6905c"
    ),
    "tools/hyp0005_data_feasibility.py": "310b23213876304ade674ef36ba17ce6d457353f",
    "tests/test_hyp0005_data_feasibility.py": "12697882da682eab699bf5b7debd7c358e56aca9",
    "research/hypotheses/HYP-0006.md": "6b3f260ceacd98adf7a6aa44205404e68e4fd4ca",
    "research/reviews/HYP-0006-DATA-FEASIBILITY.md": "ae58099a05daec4be385c18177c74f1f22d1eb30",
}


def git_output(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    done = subprocess.run(command, cwd=ROOT, check=False)
    passed = done.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def has_markers(path: Path, markers: tuple[str, ...]) -> bool:
    if not path.is_file():
        print(f"[FAIL] missing RF-029 artifact: {path}", flush=True)
        return False
    content = path.read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in content]
    for marker in missing:
        print(f"[FAIL] missing marker in {path}: {marker}", flush=True)
    return not missing


def check_frozen_lineage() -> bool:
    passed = True
    for relative, expected in FROZEN_BLOBS.items():
        actual = git_output("rev-parse", f"HEAD:{relative}")
        if actual != expected:
            print(f"[FAIL] protected lineage changed: {relative}", flush=True)
            passed = False
        else:
            print(f"[PASS] unchanged: {relative}", flush=True)
    return passed


def check_rf028_result() -> bool:
    print("\n== RF-028 frozen 216-event result identity ==", flush=True)
    if not FREEZE_RESULT.is_file() or sha256_file(FREEZE_RESULT) != RF028_JSON_SHA256:
        print("[FAIL] exact RF-028 JSON SHA-256 changed or missing", flush=True)
        return False
    if not GEOMETRY_CSV.is_file() or sha256_file(GEOMETRY_CSV) != FROZEN_GEOMETRY_SHA256:
        print("[FAIL] frozen RF-027 geometry SHA-256 changed or missing", flush=True)
        return False
    try:
        result: dict[str, Any] = json.loads(FREEZE_RESULT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] malformed RF-028 result: {exc}", flush=True)
        return False
    expected: dict[str, Any] = {
        "task_id": "ATS2-RF-028",
        "git_commit": RF028_COMMIT,
        "freeze_decision": "FREEZE_DATA_AND_TOLERANCES",
        "candidate_event_count": 217,
        "eligible_event_count": 216,
        "ineligible_event_count": 1,
        "boundary_max_abs_gap_ms": 30000,
        "pre_release_max_staleness_ms": 30000,
        "geometry_csv_sha256": FROZEN_GEOMETRY_SHA256,
        "source_bundle_sha256": FROZEN_SOURCE_SHA256,
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    }
    for key, value in expected.items():
        if result.get(key) != value:
            print(f"[FAIL] frozen RF-028 mismatch: {key}", flush=True)
            return False
    eligible = result.get("eligible_event_ids")
    excluded = result.get("ineligible_events")
    if not isinstance(eligible, list) or len(eligible) != 216 or len(set(eligible)) != 216:
        print("[FAIL] RF-028 eligible ID list changed", flush=True)
        return False
    if excluded != [
        {
            "event_id": "BLS-CPI-20030815",
            "exclusion_reasons": ["POST_60_ANCHOR_GAP_EXCEEDS_30000MS"],
        }
    ]:
        print("[FAIL] RF-028 excluded event changed", flush=True)
        return False
    print("[PASS] 216/217 exact RF-028 frozen denominator", flush=True)
    return True


def check_prototype_contract() -> bool:
    print("\n== RF-029 PROTO-01 pre-reveal contract ==", flush=True)
    passed = all(
        (
            has_markers(
                PROTOTYPE_REVIEW,
                (
                    "ATS2-RF-029",
                    "16/22",
                    "216 + 1 = 217",
                    RF028_JSON_SHA256,
                    FROZEN_RUNNER_GIT_BLOB,
                    "NO_HYPOTHESIS_OUTCOME_COMPUTED",
                    "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
                ),
            ),
            has_markers(
                PROTOTYPE_RUNNER,
                (
                    'HYPOTHESIS_ID = "HYP-0006"',
                    'PROTO_ID = "PROTO-01"',
                    "FROZEN_RF028_JSON_SHA256",
                    "FROZEN_ELIGIBLE_COUNT = 216",
                    "select_nearest",
                    "select_pre_release",
                    "LAST_RAW_RECORD",
                    "primary_decision",
                    "REVEAL_BLOCKED_PRE_FREEZE",
                    "--execute-first-reveal",
                ),
            ),
            has_markers(
                PROTOTYPE_TEST,
                (
                    "test_rf028_denominator_and_hash_are_precommitted",
                    "test_nearest_boundary_equal_gap_chooses_previous",
                    "test_duplicate_selected_timestamp_chooses_last_raw_bid_ask_pair",
                    "test_strict_pre_release_excludes_tick_at_release",
                    "test_import_is_pre_reveal_only_and_default_cli_is_blocked",
                ),
            ),
        )
    )
    actual_blob = git_output("rev-parse", "HEAD:tools/hyp0006_proto01.py")
    if actual_blob != FROZEN_RUNNER_GIT_BLOB:
        print("[FAIL] prototype runner Git blob mismatch", flush=True)
        passed = False
    if passed:
        print("[PASS] RF-029 runner and frozen decision contract", flush=True)
    return passed


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    print("Branch:", git_output("branch", "--show-current"))
    print("Commit:", git_output("rev-parse", "HEAD"))
    print("RF-029 is pre-reveal only. HYP-0006 outcome calculation prohibited.", flush=True)

    frozen = check_rf028_result()
    contract = check_prototype_contract()
    lineage = check_frozen_lineage()
    governance = run("repository governance", [sys.executable, "tools/validate_repo.py"])
    full_ci = run("full Local CI without market reveal", [sys.executable, "tools/verify_repo.py"])
    passed = all((frozen, contract, lineage, governance, full_ci))
    print("\nHYP-0006 outcome computed by RF-029: NO", flush=True)
    print("Information boundary: NO_HYPOTHESIS_OUTCOME_COMPUTED", flush=True)
    print(f"ATS CURRENT TASK CHECK: {'PASS' if passed else 'FAIL'}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
