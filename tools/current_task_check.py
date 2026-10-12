#!/usr/bin/env python3
"""RF-034 frozen offline HYP-0005 RF-023 Data Feasibility preparation gate."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

TASK_ID = "ATS2-RF-034"
TASK_NAME = "HYP-0005 RF-023 frozen offline data feasibility preparation"

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
RF033_INTAKE_EVIDENCE = ROOT / "research/reviews/HYP-0005-LOCAL-SOURCE-INTAKE-EVIDENCE.md"
RF033_GITIGNORE = ROOT / ".gitignore"
RF033_PROVENANCE_RELATIVE = "reports/local_ci/HYP0005_2026_09_SOURCE_INTAKE_PROVENANCE.json"
RF033_EXPECTED_LOCAL_FILES = {
    "data/external/dukascopy/EURUSD/H1/2026/09/BID_candles_hour_1.json": (
        12724,
        "4da5797f7abba1e015f137474a0116dcd35056ddbf5633200e65a40e5a259943",
    ),
    "data/external/dukascopy/EURUSD/H1/2026/09/ASK_candles_hour_1.json": (
        12745,
        "1672abce57189bf8519bdf7a806dcbd1e8152bc0d6f4ce06c9bb244289f10530",
    ),
    RF033_PROVENANCE_RELATIVE: (
        1321,
        "9f79cea766237a73992275d500217c1d91c3a8f5a4e2182cb1402e2a0d6fc410",
    ),
}


RF034_PREPARATION_PROTOCOL = ROOT / "research/reviews/HYP-0005-RF023-OFFLINE-PREPARATION-GATE.md"
RF034_PREP_TOOL = ROOT / "tools/hyp0005_data_feasibility.py"
RF034_RESULT_JSON = ROOT / "reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP.json"
RF034_RESULT_TEXT = ROOT / "reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP_REPORT.txt"
RF034_DERIVED_CSV = ROOT / "data/derived/HYP-0005-CONF-01-EURUSD-H1.csv"
RF034_DERIVED_PART = RF034_DERIVED_CSV.with_suffix(".csv.part")
RF034_ALLOWED_DECISIONS = (
    "READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE",
    "INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY",
)
RF034_SOURCE_HASHES = {
    "2003/05/BID_candles_hour_1.json": (
        12324,
        "16f689edd5643b906de2cdc6b6069ed62489241892506f5624c4104ccfef1293",
    ),
    "2003/05/ASK_candles_hour_1.json": (
        12311,
        "ac766b0ebe86ddb7fd818617dea5efefae71150a6b295f051608bac0487e02a5",
    ),
    "2003/06/BID_candles_hour_1.json": (
        13040,
        "58d4dd1d34a74edfa66bfd22bf52cbc7000921a67559f5a91d2d97b3a2a5e7bc",
    ),
    "2003/06/ASK_candles_hour_1.json": (
        13016,
        "a4252590d4bc432e2d7d151771f0c8de72b94b3fde671a1333f1f724a2eee72b",
    ),
    "2003/07/BID_candles_hour_1.json": (
        14023,
        "69b14b1f6bcdf18fa43664529f75a740c2575079e2b769033f47277deef7c653",
    ),
    "2003/07/ASK_candles_hour_1.json": (
        14009,
        "2f18e66d24d9b9325c45e10944eb11a54a9a7557e2a8c3504c97f90e37781dee",
    ),
    "2003/08/BID_candles_hour_1.json": (
        12763,
        "71c0ba7c4871e2431198acf84233d93d88375e63b63434617c825e595b602d7f",
    ),
    "2003/08/ASK_candles_hour_1.json": (
        12740,
        "96ab42f94d729de73a3fd2aa296e01645a01f5fd70a3679b3bf520166b380da7",
    ),
    "2026/09/BID_candles_hour_1.json": (
        12724,
        "4da5797f7abba1e015f137474a0116dcd35056ddbf5633200e65a40e5a259943",
    ),
    "2026/09/ASK_candles_hour_1.json": (
        12745,
        "1672abce57189bf8519bdf7a806dcbd1e8152bc0d6f4ce06c9bb244289f10530",
    ),
}
RF034_EXPECTED_CSV_FIELDS = (
    "event_time",
    "availability_time",
    "source_bar_completion_time",
    "sequence",
    "confirmatory_segment",
    "source_symbol",
    "bid_open",
    "ask_open",
    "utc_bucket",
)

FROZEN_BLOBS = {
    "tools/hyp0006_proto01.py": FROZEN_HYP0006_RUNNER_BLOB,
    "research/reviews/HYP-0006-PROTOTYPE-01.md": ("9f7bcd8480f66a37ea273cc7e158a56758b79b12"),
    "research/hypotheses/HYP-0006.md": ("6b3f260ceacd98adf7a6aa44205404e68e4fd4ca"),
    "research/hypotheses/HYP-0005.md": ("ebbbc89187c911485c1568dc11f5f2f9e703718a"),
    "tools/hyp0005_data_feasibility.py": ("b8d72d858d5c2691de7dec9a709f6e4d7ccb2808"),
    "research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md": (
        "c15b2b67700dd46fc592f1208731ce6b42f6905c"
    ),
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
    print("\n== RF-034 exact-main and clean-tree ==", flush=True)
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
            'last_completed_task_id: "ATS2-RF-033"',
            'next_task_id: "ATS2-RF-034"',
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
    print("\n== RF-034 frozen offline RF-023 source architecture ==", flush=True)
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
        'strategy_4_confirmatory_source_availability_status: "LOCAL_2026_09_PAIR_RECEIVED_USER_ATTESTED"',
        'strategy_4_confirmatory_source_execution_mode: "OFFLINE_ONLY_NO_HTTP_NO_RETRY"',
        "strategy_4_confirmatory_source_manual_intake_authorized: true",
        "strategy_4_confirmatory_source_network_retry_authorized: false",
        'next_task_id: "ATS2-RF-034"',
    ):
        require(marker in state, f"RF-032 state marker absent: {marker}")
    print("[PASS] RF-023 source runtime is offline-only; no HTTP/retry", flush=True)


def record_local_rf023_file_inventory() -> None:
    """Nonblocking metadata audit; intentionally no price decode, no source network."""
    print("\n== RF-034 frozen HYP-0005 file-only inventory ==", flush=True)
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


def check_local_source_intake_identity() -> None:
    """Hash-only source-intake gate; never decode prices or calculate outcomes."""
    print("\n== RF-034 local September BID/ASK/provenance SHA-256 ==", flush=True)
    require(RF033_INTAKE_EVIDENCE.is_file(), "missing tracked intake evidence")
    evidence = RF033_INTAKE_EVIDENCE.read_text(encoding="utf-8")
    require(
        "USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER" in evidence,
        "intake provenance class must remain owner-attested",
    )
    require(RF033_GITIGNORE.is_file(), "missing canonical .gitignore")
    ignore_lines = RF033_GITIGNORE.read_text(encoding="utf-8").splitlines()
    require(
        RF033_PROVENANCE_RELATIVE in ignore_lines,
        "narrow local provenance .gitignore path absent",
    )
    require(
        git_output("check-ignore", "--", RF033_PROVENANCE_RELATIVE) == RF033_PROVENANCE_RELATIVE,
        "provenance file not ignored by canonical Git rules",
    )
    expected_files = RF033_EXPECTED_LOCAL_FILES
    for relative_path, (expected_size, expected_sha256) in expected_files.items():
        path = ROOT / relative_path
        require(path.is_file(), f"missing protected local source file: {relative_path}")
        require(
            path.stat().st_size == expected_size,
            f"local source byte-size drift: {relative_path}",
        )
        require(
            sha256_file(path) == expected_sha256,
            f"local source SHA-256 drift: {relative_path}",
        )
        require(
            relative_path in evidence and expected_sha256 in evidence,
            f"tracked local source evidence does not match hash: {relative_path}",
        )
        print(f"[PASS] {relative_path}: bytes={expected_size} sha256={expected_sha256}")
    print("[PASS] source-intake hashes and Git ignore", flush=True)
    print("HYP-0005 outcome: NO_CONFIRMATORY_OUTCOME_COMPUTED", flush=True)


def check_rf034_frozen_source_hashes() -> None:
    """Verify fixed official-URL user-attested snapshots, never decode quotes."""
    print("\n== RF-034 ten frozen offline H1 BID/ASK source SHA-256 ==", flush=True)
    require(
        RF034_PREPARATION_PROTOCOL.is_file(),
        "RF-034 offline preparation protocol missing",
    )
    for relative, (expected_size, expected_sha256) in RF034_SOURCE_HASHES.items():
        path = RF023_SNAPSHOT_ROOT / relative
        require(path.is_file(), f"missing frozen RF-023 source file: {relative}")
        require(
            path.stat().st_size == expected_size,
            f"frozen RF-023 source size mismatch: {relative}",
        )
        require(
            sha256_file(path) == expected_sha256,
            f"frozen RF-023 source SHA-256 mismatch: {relative}",
        )
    print("[PASS] ten exact local source objects present and hash-matched", flush=True)


def check_rf034_output_absence() -> None:
    print("\n== RF-034 one-shot output absence gate ==", flush=True)
    for path in (
        RF034_RESULT_JSON,
        RF034_RESULT_TEXT,
        RF034_DERIVED_CSV,
        RF034_DERIVED_PART,
    ):
        require(not path.exists(), f"RF-023 output already exists; no rerun: {path}")
    print("[PASS] no previous RF-023 result or partial derived CSV", flush=True)


def run_rf023_offline_once() -> None:
    """Execute the already-frozen geometry-only script exactly once, no retries."""
    print("\n== RF-034 authorized one-shot offline RF-023 execution ==", flush=True)
    require(RF034_PREP_TOOL.is_file(), "frozen RF-023 runner missing")
    check_rf034_output_absence()
    completed = subprocess.run(
        [sys.executable, "tools/hyp0005_data_feasibility.py"],
        cwd=ROOT,
        check=False,
    )
    require(
        completed.returncode == 0,
        "RF-023 offline preparation failed; retain evidence, STOP, no retry",
    )
    print("[PASS] frozen RF-023 geometry-only runner completed once", flush=True)


def check_rf023_preparation_result(commit: str) -> None:
    """Check stored data-feasibility evidence without recomputing market metrics."""
    print("\n== RF-034 RF-023 preserved preparation result ==", flush=True)
    for path in (RF034_RESULT_JSON, RF034_RESULT_TEXT, RF034_DERIVED_CSV):
        require(path.is_file(), f"RF-023 expected output missing: {path}")
    result_text = RF034_RESULT_JSON.read_text(encoding="utf-8")
    require(
        "relative_spread" not in result_text and "abs_next_1h_return" not in result_text,
        "forbidden HYP-0005 outcome field in preparation report",
    )
    result = json.loads(result_text)
    require(isinstance(result, dict), "RF-023 result must be a JSON object")
    expected = {
        "schema_version": "hyp0005-data-feasibility-prep-1",
        "task_id": "ATS2-RF-023",
        "hypothesis_id": "HYP-0005",
        "git_commit": commit,
        "confirmatory_dataset_id": "DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001",
        "confirmatory_dataset_version": "1.0.0",
        "source_provider": "DUKASCOPY",
        "source_symbol": "EURUSD",
        "source_orientation": "DIRECT",
        "source_month_count": 5,
        "source_object_count": 10,
        "boundary_availability_mode": "H1_OPEN_PROXY_AT_EVENT_TIME",
        "exact_tick_boundary_time_known": False,
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_CONFIRMATORY_OUTCOME_COMPUTED",
        "derived_csv_relative_path": "data/derived/HYP-0005-CONF-01-EURUSD-H1.csv",
        "consumed_project_interval_start": "2003-08-03T21:00:00Z",
        "consumed_project_interval_end_exclusive": "2026-09-01T00:00:00Z",
    }
    for key, value in expected.items():
        require(result.get(key) == value, f"RF-023 frozen identity drift: {key}")
    expected_segments = [
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
    require(result.get("segments") == expected_segments, "RF-023 frozen segments drift")
    sources = result.get("source_files")
    require(isinstance(sources, list) and len(sources) == 10, "expected ten source records")
    prefix = "data/external/dukascopy/EURUSD/H1/"
    recorded: dict[str, str] = {}
    for item in sources:
        require(isinstance(item, dict), "malformed RF-023 source record")
        relative = item.get("relative_path")
        require(isinstance(relative, str), "RF-023 source path must be a string")
        require(relative not in recorded, f"duplicate RF-023 source path: {relative}")
        require(item.get("source_format") == "JETTA_JSON", "unexpected source format")
        require(item.get("source_url") == "LOCAL_FROZEN_COPY", "network source detected")
        recorded[relative] = item.get("sha256")
    expected_paths = {
        prefix + relative: digest for relative, (_, digest) in RF034_SOURCE_HASHES.items()
    }
    require(recorded == expected_paths, "RF-023 source identity/hash mismatch")
    csv_digest = result.get("derived_csv_sha256")
    require(
        isinstance(csv_digest, str) and len(csv_digest) == 64,
        "RF-023 derived CSV SHA-256 malformed",
    )
    require(
        sha256_file(RF034_DERIVED_CSV) == csv_digest,
        "RF-023 derived CSV SHA-256 mismatch",
    )
    require(
        isinstance(result.get("derived_row_count"), int) and result["derived_row_count"] > 0,
        "RF-023 empty/noninteger derived row count",
    )
    with RF034_DERIVED_CSV.open("r", encoding="utf-8") as handle:
        columns = tuple(handle.readline().strip().split(","))
    require(columns == RF034_EXPECTED_CSV_FIELDS, "RF-023 derived CSV schema drift")
    geometry = result.get("geometry")
    require(isinstance(geometry, dict), "RF-023 geometry missing")
    for key in (
        "eligible_rows_by_segment",
        "eligible_rows_by_bucket",
        "expected_market_hours_by_segment",
        "missing_market_hours_by_segment",
    ):
        counts = geometry.get(key)
        require(isinstance(counts, dict), f"RF-023 {key} missing")
        require(
            all(type(value) is int and value >= 0 for value in counts.values()),
            f"RF-023 {key} contains invalid count",
        )
    decision = result.get("preparation_decision")
    require(decision in RF034_ALLOWED_DECISIONS, "unknown RF-023 preparation decision")
    report_text = RF034_RESULT_TEXT.read_text(encoding="utf-8")
    for marker in (
        f"Decision: {decision}",
        "Outcome metrics computed: False",
        "Primary claim evaluated: False",
        "Information boundary: NO_CONFIRMATORY_OUTCOME_COMPUTED",
    ):
        require(marker in report_text, f"RF-023 report missing marker: {marker}")
    print(f"[PASS] RF-023 preparation decision: {decision}", flush=True)
    print(f"[PASS] derived SHA-256: {csv_digest}", flush=True)
    print("HYP-0005 outcome: NO_CONFIRMATORY_OUTCOME_COMPUTED", flush=True)


def run_full_ci() -> None:
    print("\n== RF-034 full ATS Local CI (no market runner) ==", flush=True)
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
        "RF-034: frozen offline source/geometry preparation only; no market outcome.",
        flush=True,
    )
    try:
        commit = check_exact_main_context()
        check_frozen_lineage()
        check_preserved_reveal_artifacts()
        check_new_confirmatory_hypothesis()
        check_rf023_offline_source_architecture()
        record_local_rf023_file_inventory()
        check_local_source_intake_identity()
        check_rf034_frozen_source_hashes()
        check_rf034_output_absence()
        run_full_ci()
        require(check_exact_main_context() == commit, "main changed during full CI")
        run_rf023_offline_once()
        check_rf023_preparation_result(commit)
        check_rf034_frozen_source_hashes()
        require(check_exact_main_context() == commit, "main changed during RF-023 preparation")
    except (
        TaskCheckError,
        FileNotFoundError,
        OSError,
        ValueError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
    ) as exc:
        print(
            f"[FAIL] RF-034 offline preparation/source blocker: {exc}",
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
