#!/usr/bin/env python3
"""RF-038: audit preserved HYP-0005 first reveal, NEVER compute a new outcome."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

TASK_ID = "ATS2-RF-038"
TASK_NAME = "HYP-0005 saved confirmatory result review, hash-only"

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


RF034_MAIN_COMMIT = "14531698c87fd3a0d87e1ec54c6713f11b7cbb60"
RF024_REVIEW = ROOT / "research/reviews/HYP-0005-DATA-FEASIBILITY.md"
RF024_MANIFEST = ROOT / "data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001.yaml"
RF024_SCHEMA = ROOT / "data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF.schema.json"
RF024_RF023_JSON_SHA256 = "d2eadd9a64da74ae79e2a0008426147953f24beb8c23f66557a721a7b8a65381"
RF024_RF023_TEXT_SHA256 = "fe9f26d15a99294cff17d2f94f3f58dcd41bbb22ffde60bdaf815aedb93d4618"
RF024_CSV_SHA256 = "b1091c4975665b2b0cd4f58627a10aceaab7aeff5076431abb6abc74c0a054c1"
RF024_SOURCE_BUNDLE_SHA256 = "65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2"

RF035_PROTO_RECORD = ROOT / "research/reviews/HYP-0005-PROTOTYPE-01.md"
RF035_RUNNER = ROOT / "tools/hyp0005_proto01.py"
RF035_RUNNER_TEST = ROOT / "tests/test_hyp0005_proto01.py"
RF035_RUNNER_BLOB = "814193997768605fe60607d66dfd755a9323f339"
RF035_RESULT_JSON = ROOT / "reports/local_ci/HYP0005_PROTO01_RESULT.json"
RF035_RESULT_TEXT = ROOT / "reports/local_ci/HYP0005_PROTO01_RESULT_REPORT.txt"
RF035_MAIN_COMMIT = "9da36dba228d4fa55c3068a01cabc7f215aa7e02"
RF036_GATE_DOC = ROOT / "research/reviews/HYP-0005-PROTOTYPE-01-REVEAL-GATE.md"
RF036_CONSUMED_SENTINEL = ROOT / "reports/local_ci/HYP0005_PROTO01_FIRST_REVEAL_CONSUMED.json"
RF035_OWNER_REPORT_SHA256 = "d7833785bee462c7b122479de22eae041329f42e24d38a1e7481ae4286aeff1b"
RF024_FROZEN_MAIN = "dd014ef6a1014edcfaa26f7d735478aee0cc94ef"
RF036_MAIN_COMMIT = "1facc2604e701cc05b34118e8c3295070bfd9eaa"
RF037_GATE_TOOL = ROOT / "tools/hyp0005_first_reveal_gate.py"
RF037_GATE_TEST = ROOT / "tests/test_hyp0005_first_reveal_gate.py"
RF037_RESULT_RECEIPT = ROOT / "reports/local_ci/HYP0005_PROTO01_FIRST_REVEAL_RECEIPT.json"
RF037_ONE_SHOT_AUTHORIZATION = "OWNER_AUTHORIZED_HYP0005_FIRST_REVEAL_ONCE_2026_10_12"
RF037_MAIN_COMMIT = "4388ac8aac732f7bd745a4466f8a9b524d543167"
RF038_RESULT_REVIEW = ROOT / "research/reviews/HYP-0005-PROTOTYPE-01-RESULT-REVIEW.md"
RF038_OWNER_REPORT_SHA256 = "f5fff726d8243d0434364d6bfcff60d4f1614bbe459de4d7494c40b229a46369"
RF038_RESULT_JSON_SHA256 = "cba7f07eebef52b649d2a2b6a7edb1dc0b808c04080fe1ae0d71e6eab25f19dc"
RF038_RESULT_TEXT_SHA256 = "57daab4a0ae2834d338f77785d52ecd3383c026d5df1196648f0b19a86813af9"
RF038_CONSUMED_SHA256 = "726ffc650a43982b49da998cd2d5ac6a5f33f816bbb0a39434998335296cf359"
RF038_RECEIPT_SHA256 = "3a0f29606781c6fadabc3a141439752a60aa8e744760405a584ec005400ab6c1"

FROZEN_BLOBS = {
    "tools/hyp0006_proto01.py": FROZEN_HYP0006_RUNNER_BLOB,
    "research/reviews/HYP-0006-PROTOTYPE-01.md": ("9f7bcd8480f66a37ea273cc7e158a56758b79b12"),
    "research/hypotheses/HYP-0006.md": ("6b3f260ceacd98adf7a6aa44205404e68e4fd4ca"),
    "research/hypotheses/HYP-0005.md": ("ebbbc89187c911485c1568dc11f5f2f9e703718a"),
    "tools/hyp0004_proto01.py": ("cbc9a46bf5e5296615f51c0ea564153968bc2a55"),
    "tools/hyp0005_proto01.py": RF035_RUNNER_BLOB,
    "research/reviews/HYP-0005-DATA-FEASIBILITY.md": ("adc77feb7473d15b1b185ef8e1a7cd9b1c066c92"),
    "data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001.yaml": (
        "03dccee9c7f21fff77ade9347b9730b79d6c62c7"
    ),
    "data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF.schema.json": (
        "a806fc993776904eabd6a1276d781e08b0112ebf"
    ),
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
    print("\n== RF-038 exact-main and clean-tree ==", flush=True)
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
    require(
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", RF035_MAIN_COMMIT, head],
            cwd=ROOT,
            check=False,
        ).returncode
        == 0,
        "RF-035 frozen runner exact-main commit not an ancestor",
    )
    require(
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", RF036_MAIN_COMMIT, head],
            cwd=ROOT,
            check=False,
        ).returncode
        == 0,
        "RF-036 first-reveal preparation not an ancestor",
    )
    require(
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", RF037_MAIN_COMMIT, head],
            cwd=ROOT,
            check=False,
        ).returncode
        == 0,
        "RF-037 first reveal exact-main commit is not an ancestor",
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
            'last_completed_task_id: "ATS2-RF-037"',
            'next_task_id: "ATS2-RF-038"',
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
        'next_task_id: "ATS2-RF-038"',
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
            "official provider authenticity remains owner-attested; "
            "decoded coherence is recorded in frozen RF-023 result",
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


def check_rf024_preparation_identity() -> None:
    """Verify already-created RF-023 bytes and geometry without recomputation."""
    print("\n== RF-024 exact preserved RF-023 preparation identity ==", flush=True)
    require(
        sha256_file(RF034_RESULT_JSON) == RF024_RF023_JSON_SHA256,
        "RF-023 preserved preparation JSON SHA-256 drift",
    )
    require(
        sha256_file(RF034_RESULT_TEXT) == RF024_RF023_TEXT_SHA256,
        "RF-023 preserved preparation text SHA-256 drift",
    )
    require(
        sha256_file(RF034_DERIVED_CSV) == RF024_CSV_SHA256,
        "RF-023 derived CSV SHA-256 drift",
    )
    require(not RF034_DERIVED_PART.exists(), "RF-023 orphaned derived .part exists")
    check_rf023_preparation_result(RF034_MAIN_COMMIT)
    result = json.loads(RF034_RESULT_JSON.read_text(encoding="utf-8"))
    require(
        result.get("preparation_decision") == "READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE",
        "RF-024 cannot freeze non-ready data feasibility geometry",
    )
    require(
        result.get("source_bundle_sha256") == RF024_SOURCE_BUNDLE_SHA256,
        "RF-023 source bundle SHA-256 drift",
    )
    require(result.get("derived_row_count") == 2010, "RF-023 prepared row count drift")
    expected = {
        "eligible_exact_next_hour_count": 1991,
        "eligible_rows_by_bucket": {
            "CORE_ACTIVE": 838,
            "OFF_HOURS": 837,
            "TRANSITION": 316,
        },
        "eligible_rows_by_segment": {
            "LEFT_UNSEEN": 1542,
            "RIGHT_UNSEEN": 449,
        },
        "expected_market_hours_by_segment": {
            "LEFT_UNSEEN": 1560,
            "RIGHT_UNSEEN": 453,
        },
        "total_rows_by_segment": {
            "LEFT_UNSEEN": 1557,
            "RIGHT_UNSEEN": 453,
        },
        "missing_market_hours_by_segment": {
            "LEFT_UNSEEN": 3,
            "RIGHT_UNSEEN": 0,
        },
        "ineligible_closed_market_next_hour_count": 16,
        "ineligible_missing_expected_next_hour_count": 3,
        "ineligible_segment_end_count": 0,
    }
    geometry = result.get("geometry")
    require(isinstance(geometry, dict), "RF-023 geometry missing")
    for key, value in expected.items():
        require(geometry.get(key) == value, f"RF-023 frozen geometry drift: {key}")
    source_rows = result.get("source_files")
    require(isinstance(source_rows, list), "source metadata missing")
    sorted_rows = sorted(
        source_rows,
        key=lambda item: (item["symbol"], item["month"], item["side"]),
    )
    bundle_payload = [
        {
            "symbol": item["symbol"],
            "month": item["month"],
            "side": item["side"],
            "sha256": item["sha256"],
        }
        for item in sorted_rows
    ]
    digest = hashlib.sha256(
        json.dumps(bundle_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    require(digest == RF024_SOURCE_BUNDLE_SHA256, "reconstructed source bundle SHA-256 drift")
    print("[PASS] RF-023 result, 2010 rows and 1991 eligible pairs preserved", flush=True)


def check_rf024_manifest_and_review() -> None:
    """Validate only tracked metadata/schema; never parse source quote rows."""
    print("\n== RF-024 conditional manifest and row schema ==", flush=True)
    for path in (RF024_REVIEW, RF024_MANIFEST, RF024_SCHEMA):
        require(path.is_file(), f"missing RF-024 tracked freeze artifact: {path}")
    sys.path.insert(0, str(ROOT / "src"))
    from ats.schemas.dataset_manifest import load_dataset_manifest

    manifest = load_dataset_manifest(RF024_MANIFEST)
    require(
        manifest.dataset_id == "DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001",
        "RF-024 manifest dataset identity mismatch",
    )
    require(manifest.dataset_version == "1.0.0", "RF-024 manifest version drift")
    require(manifest.integrity.digest == RF024_CSV_SHA256, "RF-024 CSV digest drift")
    require(
        RF024_SOURCE_BUNDLE_SHA256 in manifest.source.snapshot_reference,
        "RF-024 source bundle identity absent",
    )
    require(
        RF024_RF023_JSON_SHA256 in manifest.source.snapshot_reference,
        "RF-024 RF-023 result identity absent",
    )
    require(
        "USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER"
        in manifest.source.source_reference,
        "RF-024 provider provenance overstated",
    )
    require(
        manifest.storage.location == "data/derived/HYP-0005-CONF-01-EURUSD-H1.csv",
        "RF-024 manifest storage path mismatch",
    )
    require(
        manifest.storage.schema_reference
        == "data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF.schema.json",
        "RF-024 manifest schema reference mismatch",
    )
    require(
        manifest.time_semantics.event_time_field == "event_time"
        and manifest.time_semantics.availability_time_field == "availability_time"
        and manifest.time_semantics.availability_mode == "EXPLICIT_FIELD",
        "RF-024 boundary availability semantics drift",
    )
    require(
        manifest.quality_policy.missing == "ALLOW_DECLARED_GAPS",
        "RF-024 missing market hour handling drift",
    )
    require(
        manifest.ordering.keys == ("event_time",)
        and manifest.ordering.tie_break_keys == ("sequence",),
        "RF-024 deterministic row ordering drift",
    )
    require(
        len(manifest.known_limitations) >= 5,
        "RF-024 conditional limitations must remain explicit",
    )
    schema = json.loads(RF024_SCHEMA.read_text(encoding="utf-8"))
    require(isinstance(schema, dict), "RF-024 schema must be a JSON object")
    columns = set(RF034_EXPECTED_CSV_FIELDS)
    require(
        set(schema.get("required", [])) == columns,
        "RF-024 row schema required columns drift",
    )
    properties = schema.get("properties")
    require(
        isinstance(properties, dict) and set(properties) == columns,
        "RF-024 row schema unexpected columns",
    )
    require(schema.get("additionalProperties") is False, "RF-024 row schema not closed")
    review = RF024_REVIEW.read_text(encoding="utf-8")
    for marker in (
        "Review decision: `CONDITIONAL`",
        "STAGED_PENDING_EXACT_MAIN_PASS",
        RF024_RF023_JSON_SHA256,
        RF024_SOURCE_BUNDLE_SHA256,
        RF024_CSV_SHA256,
        "NO_CONFIRMATORY_OUTCOME_COMPUTED",
    ):
        require(marker in review, f"RF-024 review marker missing: {marker}")
    print("[PASS] staged review/manifest/schema match immutable local dataset", flush=True)
    print("Data Feasibility: CONDITIONAL / H1_OPEN_PROXY_AT_EVENT_TIME", flush=True)
    print("HYP-0005 outcome: NO_CONFIRMATORY_OUTCOME_COMPUTED", flush=True)


def check_rf035_pre_reveal_runner_freeze(*, require_absence: bool = True) -> None:
    """Freeze code and identity only. Never call the protected result function."""
    print("\n== RF-035 first-reveal runner/protocol frozen identity ==", flush=True)
    for path in (RF035_PROTO_RECORD, RF035_RUNNER, RF035_RUNNER_TEST):
        require(path.is_file(), f"RF-035 required source file missing: {path}")
    if require_absence:
        for path in (RF035_RESULT_JSON, RF035_RESULT_TEXT):
            require(not path.exists(), f"unexpected HYP-0005 confirmatory first reveal: {path}")
    record = RF035_PROTO_RECORD.read_text(encoding="utf-8")
    for marker in (
        "ATS2-RF-035",
        RF035_RUNNER_BLOB,
        RF024_FROZEN_MAIN,
        RF024_CSV_SHA256,
        RF024_SOURCE_BUNDLE_SHA256,
        "median(abs_next_1h_return | CORE_ACTIVE)",
        "median(relative_spread | CORE_ACTIVE)",
        "CONFIRMATORY_STRUCTURAL_PASS",
        "CONFIRMATORY_STRUCTURAL_FAIL",
        "STAGED_PENDING_EXACT_MAIN_PASS",
        "NO_CONFIRMATORY_OUTCOME_COMPUTED",
    ):
        require(marker in record, f"RF-035 pre-reveal protocol marker missing: {marker}")
    source_code = RF035_RUNNER.read_text(encoding="utf-8")
    for marker in (
        "def run_first_reveal_once(*, authorized: bool = False)",
        "OWNER first-reveal authorization required",
        "run_first_reveal_once",
        "FROZEN_PARENT_RUNNER_BLOB",
        "FROZEN_PREP_RUNNER_BLOB",
        "EXPECTED_GEOMETRY",
        "frozen_geometry",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "CONFIRMATORY_STRUCTURAL_PASS",
        "CONFIRMATORY_STRUCTURAL_FAIL",
        "return 2",
    ):
        require(marker in source_code, f"RF-035 runner source marker missing: {marker}")
    tests = RF035_RUNNER_TEST.read_text(encoding="utf-8")
    for marker in (
        "test_default_cli_and_unapproved_reveal_are_blocked",
        "test_synthetic_geometry_is_frozen_before_outcome_computation",
        "test_exact_parent_formulas_and_two_independent_primary_booleans",
    ):
        require(marker in tests, f"RF-035 synthetic contract test missing: {marker}")
    state = STATE.read_text(encoding="utf-8")
    for marker in (
        'next_task_id: "ATS2-RF-038"',
        "strategy_4_confirmatory_dataset_freeze_completed: true",
        "strategy_4_confirmatory_first_reveal_authorized: true",
        "strategy_4_confirmatory_outcome_computed: true",
        f'strategy_4_confirmatory_pre_reveal_runner_git_blob: "{RF035_RUNNER_BLOB}"',
    ):
        require(marker in state, f"RF-035 research information boundary drift: {marker}")
    print("[PASS] unchanged RF-035 runner and decision contract", flush=True)
    if require_absence:
        print("HYP-0005 outcome: NO_CONFIRMATORY_OUTCOME_COMPUTED", flush=True)


def check_rf036_gate_preparation(*, require_absence: bool = True) -> None:
    """Metadata-only: no protected price reads and absolutely no reveal invocation."""
    print("\n== RF-036 preparation-only first-reveal authorization boundary ==", flush=True)
    require(RF036_GATE_DOC.is_file(), "RF-036 reveal gate protocol missing")
    protocol = RF036_GATE_DOC.read_text(encoding="utf-8")
    for marker in (
        "ATS2-RF-036",
        "4.1/5",
        "STAGED_PREPARATION_ONLY_REVEAL_NOT_AUTHORIZED",
        RF035_MAIN_COMMIT,
        RF035_RUNNER_BLOB,
        RF035_OWNER_REPORT_SHA256,
        RF024_CSV_SHA256,
        RF024_SOURCE_BUNDLE_SHA256,
        "median(abs_next_1h_return | CORE_ACTIVE)",
        "median(relative_spread | CORE_ACTIVE)",
        "CONFIRMATORY_STRUCTURAL_PASS",
        "CONFIRMATORY_STRUCTURAL_FAIL",
        "NOT_AUTHORIZED / NOT_EXECUTED",
        "HYP0005_PROTO01_FIRST_REVEAL_CONSUMED.json",
    ):
        require(marker in protocol, f"RF-036 reveal protocol missing marker: {marker}")
    if require_absence:
        for path in (RF035_RESULT_JSON, RF035_RESULT_TEXT, RF036_CONSUMED_SENTINEL):
            require(
                not path.exists(), f"RF-036 preparation prohibited; reveal output exists: {path}"
            )
    state = STATE.read_text(encoding="utf-8")
    for marker in (
        'last_completed_task_id: "ATS2-RF-037"',
        'next_task_id: "ATS2-RF-038"',
        'strategy_4_confirmatory_pre_reveal_status: "RF035_EXACT_MAIN_PASS_FROZEN"',
        "strategy_4_confirmatory_research_plan_current_major_step: 5",
        'strategy_4_confirmatory_reveal_gate_preparation: "RF036_EXACT_MAIN_PASS_CLOSED"',
        "strategy_4_confirmatory_first_reveal_authorized: true",
        "strategy_4_confirmatory_reveal_gate_execution_enabled: false",
        "strategy_4_confirmatory_first_reveal_consumed: true",
        "strategy_4_confirmatory_outcome_computed: true",
    ):
        require(marker in state, f"RF-036 canonical information boundary drift: {marker}")
    print("[PASS] preserved RF-036 technical protocol", flush=True)
    if require_absence:
        print("HYP-0005 outcome: NO_CONFIRMATORY_OUTCOME_COMPUTED", flush=True)


def check_rf037_one_shot_authorization() -> None:
    """Check OWNER authority and immutable source identities without price metrics."""
    print("\n== RF-037 OWNER one-shot authorization and output protection ==", flush=True)
    require(RF037_GATE_TOOL.is_file(), "RF-037 gate implementation missing")
    require(RF037_GATE_TEST.is_file(), "RF-037 synthetic gate tests missing")
    state = STATE.read_text(encoding="utf-8")
    for marker in (
        'last_completed_task_id: "ATS2-RF-036"',
        'next_task_id: "ATS2-RF-037"',
        'strategy_4_confirmatory_reveal_gate_preparation: "RF036_EXACT_MAIN_PASS_CLOSED"',
        "strategy_4_confirmatory_research_plan_current_major_step: 4",
        'rf036_verified_commit: "1facc2604e701cc05b34118e8c3295070bfd9eaa"',
        "strategy_4_confirmatory_first_reveal_authorized: true",
        "strategy_4_confirmatory_reveal_gate_execution_enabled: true",
        "strategy_4_confirmatory_first_reveal_consumed: false",
        "strategy_4_confirmatory_outcome_computed: false",
        f'strategy_4_confirmatory_first_reveal_authorization_record: "{RF037_ONE_SHOT_AUTHORIZATION}"',
        f'strategy_4_confirmatory_pre_reveal_runner_git_blob: "{RF035_RUNNER_BLOB}"',
    ):
        require(marker in state, f"RF-037 authorization drift: {marker}")
    source = RF037_GATE_TOOL.read_text(encoding="utf-8")
    tests = RF037_GATE_TEST.read_text(encoding="utf-8")
    for marker in (
        RF037_ONE_SHOT_AUTHORIZATION,
        RF035_RUNNER_BLOB,
        "CONSUMED_BEFORE_OUTCOME",
        'path.open("x", encoding="utf-8")',
        "os.fsync(stream.fileno())",
        "run_first_reveal_once(authorized=True)",
        "def execute_or_verify_once(",
        "FIRST_REVEAL_COMPLETED_ONCE",
        "No automatic retry",
    ):
        require(marker.lower() in source.lower(), f"RF-037 code marker missing: {marker}")
    for marker in (
        "test_rf037_synthetic_first_reveal_consumes_once_before_result",
        "test_rf037_consumed_failure_cannot_be_retried",
        "test_rf037_saved_result_sha_drift_is_blocked",
        "test_rf037_unauthorized_first_reveal_is_blocked",
    ):
        require(marker in tests, f"RF-037 test marker missing: {marker}")
    ignore_lines = RF033_GITIGNORE.read_text(encoding="utf-8").splitlines()
    for path in (
        RF035_RESULT_JSON,
        RF035_RESULT_TEXT,
        RF036_CONSUMED_SENTINEL,
        RF037_RESULT_RECEIPT,
    ):
        relative = path.relative_to(ROOT).as_posix()
        require(relative in ignore_lines, f"missing narrow .gitignore rule: {relative}")
        require(
            git_output("check-ignore", "--", relative) == relative,
            f"first reveal output is tracked: {relative}",
        )
    print("[PASS] approved once, frozen runner, local receipt paths ignored", flush=True)


def check_rf038_saved_reveal_archive() -> None:
    """Read the preserved result and receipt only. NEVER execute the market runner."""
    print(
        "\
== RF-038 saved HYP-0005 first reveal (HASH ONLY / NO RERUN) ==",
        flush=True,
    )
    required_files = (
        (RF035_RESULT_JSON, RF038_RESULT_JSON_SHA256),
        (RF035_RESULT_TEXT, RF038_RESULT_TEXT_SHA256),
        (RF036_CONSUMED_SENTINEL, RF038_CONSUMED_SHA256),
        (RF037_RESULT_RECEIPT, RF038_RECEIPT_SHA256),
    )
    for path, digest in required_files:
        require(path.is_file(), f"original reveal artifact missing: {path}")
        require(sha256_file(path) == digest, f"original reveal SHA-256 drift: {path}")

    consumed = json.loads(RF036_CONSUMED_SENTINEL.read_text(encoding="utf-8"))
    receipt = json.loads(RF037_RESULT_RECEIPT.read_text(encoding="utf-8"))
    saved = json.loads(RF035_RESULT_JSON.read_text(encoding="utf-8"))
    require(
        all(isinstance(item, dict) for item in (consumed, receipt, saved)),
        "original reveal archive must contain three JSON objects",
    )
    require(
        consumed.get("state") == "CONSUMED_BEFORE_OUTCOME",
        "original OWNER authorization consumption missing",
    )
    require(
        receipt.get("status") == "FIRST_REVEAL_COMPLETED_ONCE",
        "original one-shot completion receipt missing",
    )
    require(
        consumed.get("authorization") == RF037_ONE_SHOT_AUTHORIZATION,
        "original consumed authorization drift",
    )
    require(
        receipt.get("authorization") == RF037_ONE_SHOT_AUTHORIZATION,
        "original receipt authorization drift",
    )
    for item in (consumed, receipt):
        require(item.get("git_commit") == RF037_MAIN_COMMIT, "saved exact-main drift")
        require(item.get("runner_git_blob") == RF035_RUNNER_BLOB, "saved runner drift")
        require(
            item.get("dataset_csv_sha256") == RF024_CSV_SHA256,
            "saved dataset drift",
        )
    require(
        receipt.get("result_json_sha256") == RF038_RESULT_JSON_SHA256,
        "original receipt JSON hash mismatch",
    )
    require(
        receipt.get("report_text_sha256") == RF038_RESULT_TEXT_SHA256,
        "original receipt text hash mismatch",
    )
    require(
        receipt.get("source_bundle_sha256") == RF024_SOURCE_BUNDLE_SHA256,
        "original receipt source bundle drift",
    )
    for key, value in {
        "schema_version": "hyp0005-confirmatory-proto01-result-1",
        "hypothesis_id": "HYP-0005",
        "parent_idea_id": "IDEA-0004",
        "prototype_id": "PROTO-01",
        "evidence_class": "CONFIRMATORY_STRUCTURAL_NOT_INDEPENDENT_EXAM",
        "decision": "CONFIRMATORY_STRUCTURAL_PASS",
        "decision_reason": "BOTH_PRIMARY_INEQUALITIES_MET",
        "next_action": "REVIEW_CONFIRMATORY_STRUCTURAL_EVIDENCE_NO_DIRECT_R4",
        "outcome_metrics_computed": True,
        "primary_claim_evaluated": True,
    }.items():
        require(saved.get(key) == value, f"frozen saved result metadata drift: {key}")
    require(
        saved.get("run_context", {}).get("git_commit") == RF037_MAIN_COMMIT,
        "result exact main context drift",
    )
    require(
        saved.get("geometry", {}).get("eligible_exact_next_hour_count") == 1991,
        "saved original result eligible count drift",
    )
    require(
        saved.get("primary") == {
            "movement_inequality_pass": True,
            "spread_inequality_pass": True,
            "both_primary_inequalities_pass": True,
        },
        "saved original primary flags drift",
    )
    require(
        receipt.get("decision") == saved.get("decision"),
        "receipt original result decision drift",
    )
    require(
        receipt.get("both_primary_inequalities_pass") is True,
        "receipt original primary decision drift",
    )

    require(RF038_RESULT_REVIEW.is_file(), "RF-038 tracked review missing")
    review = RF038_RESULT_REVIEW.read_text(encoding="utf-8")
    for marker in (
        "ATS2-RF-038",
        RF037_MAIN_COMMIT,
        RF038_OWNER_REPORT_SHA256,
        RF038_RESULT_JSON_SHA256,
        RF038_RESULT_TEXT_SHA256,
        RF038_CONSUMED_SHA256,
        RF038_RECEIPT_SHA256,
        "CONFIRMATORY_STRUCTURAL_PASS",
        "NO_DIRECT_R4",
        "STAGED_PENDING_EXACT_MAIN_PASS",
        "CONSUMED",
    ):
        require(marker in review, f"RF-038 tracked result review incomplete: {marker}")
    state = STATE.read_text(encoding="utf-8")
    for marker in (
        'last_completed_task_id: "ATS2-RF-037"',
        'next_task_id: "ATS2-RF-038"',
        'rf037_verified_commit: "4388ac8aac732f7bd745a4466f8a9b524d543167"',
        "strategy_4_confirmatory_first_reveal_consumed: true",
        "strategy_4_confirmatory_outcome_computed: true",
        "strategy_4_confirmatory_primary_claim_evaluated: true",
        "strategy_4_confirmatory_research_plan_current_major_step: 5",
        'strategy_4_confirmatory_decision: "CONFIRMATORY_STRUCTURAL_PASS"',
        "strategy_4_confirmatory_reveal_gate_execution_enabled: false",
        "strategy_5_hyp0005_protected_segments_consumed: true",
    ):
        require(marker in state, f"RF-038 current-state evidence drift: {marker}")
    print("[PASS] four exact original artifacts and receipt SHA-256 preserved", flush=True)
    print("HYP-0005 original decision: CONFIRMATORY_STRUCTURAL_PASS", flush=True)
    print("HYP-0005 market outcome recomputed: NO", flush=True)


def run_full_ci() -> None:
    print("\n== RF-038 full ATS Local CI (saved-archive checks only) ==", flush=True)
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
    print("RF-038: original first reveal is CONSUMED; HASH ONLY, NO RERUN", flush=True)
    try:
        commit = check_exact_main_context()
        check_frozen_lineage()
        check_preserved_reveal_artifacts()
        check_new_confirmatory_hypothesis()
        check_rf023_offline_source_architecture()
        record_local_rf023_file_inventory()
        check_local_source_intake_identity()
        check_rf034_frozen_source_hashes()
        check_rf024_preparation_identity()
        check_rf024_manifest_and_review()
        check_rf035_pre_reveal_runner_freeze(require_absence=False)
        check_rf036_gate_preparation(require_absence=False)
        check_rf038_saved_reveal_archive()
        run_full_ci()
        require(check_exact_main_context() == commit, "main changed during full CI")
        check_frozen_lineage()
        check_rf034_frozen_source_hashes()
        check_rf024_preparation_identity()
        check_rf024_manifest_and_review()
        check_rf038_saved_reveal_archive()
        require(
            check_exact_main_context() == commit, "main changed during RF-038 archive review"
        )
    except (
        TaskCheckError,
        FileNotFoundError,
        OSError,
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"[FAIL] RF-038 preserved first-reveal evidence blocker: {exc}", flush=True)
        print("RF-038 may NOT rerun or reinterpret the original market experiment.", flush=True)
        print("ATS CURRENT TASK CHECK: FAIL", flush=True)
        return 1
    print("HYP-0005: CONFIRMATORY_STRUCTURAL_PASS / REVIEWED_NO_DIRECT_R4", flush=True)
    print("FIRST_REVEAL: CONSUMED / PRESERVED_SHA256 / NO_RERUN", flush=True)
    print("ATS CURRENT TASK CHECK: PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
