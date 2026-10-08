#!/usr/bin/env python3
"""RF-032 technical HYP-0005 offline source-input repair (no market outcome)."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

TASK_ID = "ATS2-RF-032"
TASK_NAME = "HYP-0005 official-source offline-only intake architecture"

RF030_MAIN_COMMIT = "d1135bb2486009ebb358bf4b508c06303ab77f74"
FROZEN_HYP0006_RUNNER_BLOB = "6afb870c035bc5ae76f773784a5fa3db15d680fd"
REVEAL_JSON_SHA256 = "484575ceb2b6c12df651697d50559e70c7cba8a8f52fc4508d28943e8c5447e9"
REVEAL_TEXT_SHA256 = "2f547f6866f13367cb1cdc4f7c31dfec8a7ff12c9fc4e1391d9124b50ba3f213"
REVEAL_JSON = ROOT / "reports/local_ci/HYP0006_PROTO01_RESULT.json"
REVEAL_TEXT = ROOT / "reports/local_ci/HYP0006_PROTO01_RESULT_REPORT.txt"
REVEAL_REVIEW = ROOT / "research/reviews/HYP-0006-PROTOTYPE-01-RESULT-REVIEW.md"
NEW_HYPOTHESIS = ROOT / "research/hypotheses/HYP-0007.md"
STATE = ROOT / "03_СОСТОЯНИЕ_ПРОЕКТА.yaml"
SOURCE_INTAKE = ROOT / "research/reviews/HYP-0005-OFFLINE-SOURCE-INTAKE.md"
RF023_SOURCE_TOOL = ROOT / "tools/hyp0005_data_feasibility.py"
RF023_SNAPSHOT_ROOT = ROOT / "data/external/dukascopy/EURUSD/H1"

FROZEN_BLOBS = {
    "tools/hyp0006_proto01.py": FROZEN_HYP0006_RUNNER_BLOB,
    "research/reviews/HYP-0006-PROTOTYPE-01.md": ("9f7bcd8480f66a37ea273cc7e158a56758b79b12"),
    "research/hypotheses/HYP-0006.md": ("6b3f260ceacd98adf7a6aa44205404e68e4fd4ca"),
    "research/hypotheses/HYP-0005.md": ("ebbbc89187c911485c1568dc11f5f2f9e703718a"),
}


class TaskCheckError(RuntimeError):
    """Infrastructure/governance failure, never a market outcome."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TaskCheckError(message)


def sha256_file(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def git_output(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def check_exact_main_context() -> str:
    print("\n== RF-032 exact-main and clean-tree ==", flush=True)
    branch = git_output("branch", "--show-current")
    head = git_output("rev-parse", "HEAD")
    origin_main = git_output("rev-parse", "origin/main")
    require(branch == "main", f"expected main, got {branch}")
    require(head == origin_main, "main differs from origin/main")
    require(
        not git_output("status", "--porcelain=v1", "-uall"),
        "working tree not clean",
    )
    require(
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", RF030_MAIN_COMMIT, head],
            cwd=ROOT,
            check=False,
        ).returncode
        == 0,
        "RF-030 exact-main reveal commit not an ancestor",
    )
    print(f"[PASS] exact main: {head}, clean tree", flush=True)
    return head


def check_frozen_lineage() -> None:
    print("\n== Frozen HYP-0005/HYP-0006 lineage ==", flush=True)
    for relative, frozen_blob in FROZEN_BLOBS.items():
        require(
            git_output("rev-parse", f"HEAD:{relative}") == frozen_blob,
            f"frozen Git blob changed: {relative}",
        )
        require(
            git_output("hash-object", "--", relative) == frozen_blob,
            f"frozen worktree content changed: {relative}",
        )
    print("[PASS] untouched frozen runner and HYP-0005/0006 lineage", flush=True)


def check_saved_result_identity(result: dict[str, Any]) -> None:
    """Check already-revealed facts; DO NOT compute any new market outcomes."""
    required = {
        "git_commit": RF030_MAIN_COMMIT,
        "hypothesis_id": "HYP-0006",
        "prototype_id": "PROTO-01",
        "evidence_classification": "DEVELOPMENT_EXPLORATORY_ONLY",
        "information_boundary": "DEVELOPMENT_REVEALED_EXPLORATORY_ONLY",
        "candidate_event_count": 217,
        "eligible_event_count": 216,
        "ineligible_event_count": 1,
        "ineligible_event_ids": ["BLS-CPI-20030815"],
        "median_pre_abs_60m_return": 0.0005589654536042321,
        "median_post_abs_60m_return": 0.0012930417305135888,
        "primary_inequality_pass": True,
        "prototype_decision": "ADVANCE_TO_ECONOMIC_SCREEN",
        "next_action": "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
        "same_time_bls_flagged_event_count": 216,
        "outcome_metrics_computed": True,
        "primary_claim_evaluated": True,
    }
    for key, value in required.items():
        require(result.get(key) == value, f"frozen HYP-0006 result drift: {key}")
    rows = result.get("event_observations")
    require(
        isinstance(rows, list) and len(rows) == 216,
        "216 saved event records required",
    )
    require(
        all(isinstance(row, dict) and isinstance(row.get("event_id"), str) for row in rows),
        "saved HYP-0006 event identities malformed",
    )
    require(len({row["event_id"] for row in rows}) == 216, "duplicate saved event IDs")
    require(
        all(bool(row.get("same_time_bls_labels")) for row in rows),
        "all 216 original BLS overlap flags must remain visible",
    )


def check_preserved_reveal_artifacts() -> None:
    print("\n== Preserved RF-030 reveal (hash-only; NO RE-RUN) ==", flush=True)
    require(REVEAL_JSON.is_file(), "HYP-0006 saved reveal JSON missing")
    require(REVEAL_TEXT.is_file(), "HYP-0006 saved reveal report missing")
    require(
        sha256_file(REVEAL_JSON) == REVEAL_JSON_SHA256,
        "saved HYP-0006 reveal JSON SHA-256 differs",
    )
    require(
        sha256_file(REVEAL_TEXT) == REVEAL_TEXT_SHA256,
        "saved HYP-0006 reveal text SHA-256 differs",
    )
    result = json.loads(REVEAL_JSON.read_text(encoding="utf-8"))
    require(isinstance(result, dict), "saved reveal is not a JSON object")
    check_saved_result_identity(result)
    print("[PASS] exact archived JSON/text SHA-256; 216 original records", flush=True)
    print("HYP-0006 result: DEVELOPMENT_REVEALED_EXPLORATORY_ONLY", flush=True)


def check_new_confirmatory_hypothesis() -> None:
    print("\n== HYP-0007 hypothesis-formation-only gate ==", flush=True)
    for path, markers in {
        NEW_HYPOTHESIS: (
            "Hypothesis ID: `HYP-0007`",
            "Parent Idea ID: `IDEA-0005`",
            "NO_CONFIRMATORY_OUTCOME_COMPUTED",
            "INDEPENDENT_DATA_FEASIBILITY",
            "1/8",
            "8/8",
            "median(post_abs_60m_return) > median(pre_abs_60m_return)",
        ),
        REVEAL_REVIEW: (
            "ATS2-RF-031",
            RF030_MAIN_COMMIT,
            REVEAL_JSON_SHA256,
            "EXPLORATORY_PROTOTYPE",
            "216",
        ),
        STATE: (
            'last_completed_task_id: "ATS2-RF-031"',
            'next_task_id: "ATS2-RF-032"',
            'strategy_5_confirmatory_hypothesis_id: "HYP-0007"',
            'strategy_5_confirmatory_source_status: "INDEPENDENCE_NOT_YET_CERTIFIED"',
            "strategy_5_confirmatory_outcome_computed: false",
        ),
    }.items():
        require(path.is_file(), f"missing source-of-truth artifact: {path}")
        raw = path.read_text(encoding="utf-8")
        for marker in markers:
            require(marker in raw, f"missing canonical marker {marker}: {path}")
    print("[PASS] one new material HYP, 8-gate plan and independent source unselected")
    print("HYP-0007 outcome: NO_CONFIRMATORY_OUTCOME_COMPUTED", flush=True)


def check_rf023_offline_source_architecture() -> None:
    print("\n== RF-032 offline RF-023 source architecture ==", flush=True)
    require(RF023_SOURCE_TOOL.is_file(), "frozen RF-023 source tool missing")
    require(SOURCE_INTAKE.is_file(), "RF-032 intake instructions missing")
    source_code = RF023_SOURCE_TOOL.read_text(encoding="utf-8")
    intake = SOURCE_INTAKE.read_text(encoding="utf-8")
    for marker in (
        "SOURCE_INPUT_REQUIRED_LOCAL_SNAPSHOT",
        "SOURCE_INPUT_REQUIRED_PARTIAL_PAIR",
        "SOURCE_INPUT_REQUIRED_EMPTY_OBJECT",
        "LOCAL_FROZEN_COPY",
        "source.jetta_raw_path",
        "source.raw_path",
        "download_source_pair_resilient",
    ):
        require(marker in source_code, f"RF-023 offline source guard missing: {marker}")
    for forbidden in (
        "source.download_jetta_source_once",
        "source.download_legacy_source_once",
        "source.fetch_bytes(",
        "time.sleep(",
    ):
        require(
            forbidden not in source_code,
            f"RF-023 network path remains: {forbidden}",
        )
    for marker in (
        "ATS2-RF-032",
        "SOURCE_INPUT_REQUIRED_2026_09",
        "2026/09/BID_candles_hour_1.json",
        "2026/09/ASK_candles_hour_1.json",
        "https://jetta.dukascopy.com/v1/candles/hour/EUR-USD/",
        "NO_CONFIRMATORY_OUTCOME_COMPUTED",
    ):
        require(marker in intake, f"RF-032 intake contract marker absent: {marker}")
    state = STATE.read_text(encoding="utf-8")
    for marker in (
        'strategy_4_confirmatory_source_availability_status: "SOURCE_INPUT_REQUIRED_2026_09"',
        'strategy_4_confirmatory_source_execution_mode: "OFFLINE_ONLY_NO_HTTP_NO_RETRY"',
        "strategy_4_confirmatory_source_manual_intake_authorized: false",
        "strategy_4_confirmatory_source_network_retry_authorized: false",
        'next_task_id: "ATS2-RF-032"',
    ):
        require(marker in state, f"RF-032 state marker absent: {marker}")
    print("[PASS] RF-023 source runtime is offline-only; no HTTP/retry", flush=True)


def record_local_rf023_file_inventory() -> None:
    """Nonblocking metadata audit; intentionally no price decode, no source network."""
    print("\n== RF-032 frozen HYP-0005 file-only inventory ==", flush=True)
    missing_months: list[str] = []
    for year, month in ((2003, 5), (2003, 6), (2003, 7), (2003, 8), (2026, 9)):
        directory = RF023_SNAPSHOT_ROOT / str(year) / f"{month:02d}"
        complete_formats: list[str] = []
        for extension in ("json", "bi5"):
            pair_complete = True
            for side in ("BID", "ASK"):
                path = directory / f"{side}_candles_hour_1.{extension}"
                if not path.is_file():
                    pair_complete = False
                    continue
                size = path.stat().st_size
                checksum = sha256_file(path) if size else "EMPTY"
                print(
                    f"{year}-{month:02d} {extension} {side}: bytes={size} sha256={checksum}",
                    flush=True,
                )
                if size == 0:
                    pair_complete = False
            if pair_complete:
                complete_formats.append(extension)
        if not complete_formats:
            missing_months.append(f"{year}-{month:02d}")
        print(
            f"[INFO] {year}-{month:02d} complete local file pairs: "
            f"{','.join(complete_formats) if complete_formats else 'NONE'}",
            flush=True,
        )
    if missing_months:
        print(
            "[INFO] SOURCE_INPUT_REQUIRED: "
            + ",".join(missing_months)
            + "; OFFLINE ARCHITECTURE PASS DOES NOT MEAN RESEARCH PASS",
            flush=True,
        )
    else:
        print(
            "[INFO] ALL_LOCAL_FILE_PAIRS_PRESENT; "
            "official provenance/decoded coherence still unverified",
            flush=True,
        )
    print("HYP-0005 outcome: NO_CONFIRMATORY_OUTCOME_COMPUTED", flush=True)


def run_full_ci() -> None:
    print("\n== RF-032 full ATS Local CI (no market runner) ==", flush=True)
    completed = subprocess.run(
        [sys.executable, "tools/verify_repo.py"],
        cwd=ROOT,
        check=False,
    )
    require(completed.returncode == 0, "full Local CI failed")
    print("[PASS] full ATS Local CI", flush=True)


def main() -> int:
    print("ATS CURRENT TASK CHECK", flush=True)
    print(f"Task: {TASK_ID} — {TASK_NAME}", flush=True)
    print(
        "RF-032: OFFLINE source/intake only; NO HTTP, protected price decode or reveal.",
        flush=True,
    )
    try:
        commit = check_exact_main_context()
        check_frozen_lineage()
        check_preserved_reveal_artifacts()
        check_new_confirmatory_hypothesis()
        check_rf023_offline_source_architecture()
        record_local_rf023_file_inventory()
        run_full_ci()
        require(check_exact_main_context() == commit, "main changed during full CI")
    except (
        TaskCheckError,
        FileNotFoundError,
        OSError,
        ValueError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
    ) as exc:
        print(
            f"[FAIL] RF-032 governance/source-architecture blocker: {exc}",
            flush=True,
        )
        print("HYP-0007 outcome: NO_CONFIRMATORY_OUTCOME_COMPUTED", flush=True)
        print("ATS CURRENT TASK CHECK: FAIL", flush=True)
        return 1
    print("HYP-0007 outcome: NO_CONFIRMATORY_OUTCOME_COMPUTED", flush=True)
    print("ATS CURRENT TASK CHECK: PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
