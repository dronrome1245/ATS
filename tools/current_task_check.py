#!/usr/bin/env python3
"""Run ATS2-RF-027 exact-main checks and HYP-0006 data-feasibility preparation."""

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
TASK_ID = "ATS2-RF-027"
TASK_NAME = "HYP-0006 Data Feasibility preparation"

PROTOCOL = Path("research/reviews/HYP-0006-DATA-FEASIBILITY-PREP.md")
TOOL = Path("tools/hyp0006_data_feasibility.py")
TEST = Path("tests/test_hyp0006_data_feasibility.py")
CONTROLLED_DOWNLOAD_TOOL = Path("tools/hyp0006_dukascopy_controlled_download.py")
CONTROLLED_DOWNLOAD_TEST = Path("tests/test_hyp0006_dukascopy_controlled_download.py")
BROWSER_PILOT_TOOL = Path("tools/hyp0006_dukascopy_browser_pilot.py")
BROWSER_PILOT_TEST = Path("tests/test_hyp0006_dukascopy_browser_pilot.py")
BROWSER_BATCH_250_TOOL = Path("tools/hyp0006_dukascopy_browser_batch_250.py")
BROWSER_BATCH_250_TEST = Path("tests/test_hyp0006_dukascopy_browser_batch_250.py")
BROWSER_REMAINING_748_TOOL = Path("tools/hyp0006_dukascopy_browser_remaining_748.py")
BROWSER_REMAINING_748_TEST = Path("tests/test_hyp0006_dukascopy_browser_remaining_748.py")
STATE = Path("03_СОСТОЯНИЕ_ПРОЕКТА.yaml")
BACKLOG = Path("governance/backlog/PROGRAM_BACKLOG_V2.md")
HANDOFF = Path("AI_HANDOFF.md")
NEXT_STEP = Path("02_СЛЕДУЮЩИЙ_ШАГ.md")
STATUS = Path("01_СТАТУС_ПРОЕКТА.md")
SOURCE_RECOVERY = Path("research/reviews/HYP-0006-DUKASCOPY-SOURCE-RECOVERY.md")

LOCAL_RESULT = Path("reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP.json")
BLS_SNAPSHOT_MANIFEST = Path("data/reference/HYP-0006-BLS-SCHEDULE-SNAPSHOT-MANIFEST.csv")
BLS_CALENDAR_CSV = Path("data/derived/HYP-0006-BLS-CPI-CALENDAR-2003-2021.csv")
GEOMETRY_CSV = Path("data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv")

FROZEN_BLOBS = {
    "research/hypotheses/HYP-0005.md": "ebbbc89187c911485c1568dc11f5f2f9e703718a",
    "research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md": (
        "c15b2b67700dd46fc592f1208731ce6b42f6905c"
    ),
    "tools/hyp0005_data_feasibility.py": "310b23213876304ade674ef36ba17ce6d457353f",
    "tests/test_hyp0005_data_feasibility.py": "12697882da682eab699bf5b7debd7c358e56aca9",
    "research/hypotheses/HYP-0006.md": "6b3f260ceacd98adf7a6aa44205404e68e4fd4ca",
    "research/reviews/HYP-0006-DATA-FEASIBILITY.md": ("ae58099a05daec4be385c18177c74f1f22d1eb30"),
}

ALLOWED_DECISIONS = {
    "READY_FOR_DATA_FEASIBILITY_FREEZE",
    "UNRESOLVED_OFFICIAL_EVENT_TIMES",
    "INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_BLS_CALENDAR_HEADER = (
    "event_id",
    "release_date_local",
    "release_time_local",
    "release_time_utc",
    "timezone_semantics",
    "schedule_label",
    "same_time_bls_labels",
    "source_year",
    "source_url",
    "source_snapshot_relative_path",
    "source_snapshot_sha256",
)
EXPECTED_GEOMETRY_HEADER = (
    "event_id",
    "archive_release_date",
    "release_time_utc",
    "archive_zone_label",
    "schedule_crosscheck_status",
    "same_time_bls_labels",
    "required_tick_object_count",
    "missing_tick_object_count",
    "pre60_prev_gap_ms",
    "pre60_next_gap_ms",
    "pre_release_last_gap_ms",
    "post60_prev_gap_ms",
    "post60_next_gap_ms",
    "quote_geometry_status",
)
PROHIBITED_OUTCOME_FIELDS = {
    "bid",
    "ask",
    "mid",
    "midpoint",
    "pre_abs_60m_return",
    "post_abs_60m_return",
    "return",
    "pnl",
    "profit",
}


def git_output(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


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


def require_markers(path: Path, markers: tuple[str, ...]) -> bool:
    full_path = ROOT / path
    if not full_path.is_file():
        print(f"[FAIL] missing RF-027 artifact: {path}", flush=True)
        return False
    content = full_path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in content:
            print(f"[FAIL] RF-027 marker missing in {path}: {marker}", flush=True)
            return False
    return True


def check_frozen_lineage() -> bool:
    print("\n== RF-027 frozen HYP-0005/HYP-0006 lineage ==", flush=True)
    passed = True
    for relative, expected_blob in FROZEN_BLOBS.items():
        path = ROOT / relative
        if not path.is_file():
            print(f"[FAIL] frozen artifact missing: {relative}", flush=True)
            passed = False
            continue
        actual_blob = git_output("rev-parse", f"HEAD:{relative}")
        if actual_blob != expected_blob:
            print(
                f"[FAIL] frozen artifact changed: {relative} ({actual_blob} != {expected_blob})",
                flush=True,
            )
            passed = False
        else:
            print(f"[PASS] unchanged: {relative}", flush=True)
    return passed


def check_rf027_contract() -> bool:
    print("\n== RF-027 frozen preparation contract ==", flush=True)

    protocol_ok = require_markers(
        PROTOCOL,
        (
            "ATS2-RF-027",
            "PREPARATION_PROTOCOL_FROZEN_OFFLINE_BLS_SNAPSHOTS",
            "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF",
            "OWNER-authorized controlled Dukascopy preload",
            "1085",
            "AUTHORIZED_ONCE_BY_OWNER_2026_10_05",
            "SOURCE_BLOCKED_AUTHORIZATION_CONSUMED",
            "OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
            "OWNER_AUTHORIZED_BROWSER_PILOT_50_2026_10_05",
            "SKIPPED_AFTER_2_ATTEMPTS",
            "tools/hyp0006_dukascopy_browser_pilot.py",
            "OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05",
            "tools/hyp0006_dukascopy_browser_batch_250.py",
            "PASS_250_OF_250_AUTHORIZATION_CONSUMED",
            "OWNER_AUTHORIZED_REMAINING_748_2026_10_05",
            "tools/hyp0006_dukascopy_browser_remaining_748.py",
            "PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED",
            "0131dd82d286814adaa76ff6e2524e0d000ca13c",
            "a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4",
            "391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7",
            "6810",
            "CONFIRMED_ZERO_NETWORK_COMPLETE",
            "1085 / 1085",
            "ATS_TASK_CHECK.bat",
            "ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112",
            "2011-11-16T11:00:00Z",
            "no_valid_bi5_download_within_45s_attempt_2",
            "FULL_JSON_MANIFEST_REVIEW_PASS",
            "438bc59aa6f2cc81a762914f111017f75a2e46b2",
            "FULL_JSON_MANIFEST_REVIEW_PASS",
            "36e1301d551a69990ca707e7bf33da1ce07e5e88b1e7dc23a379a66b814e6b2c",
            "9aa6d7646c809f7a8fb2caaf421f13553ec30ba26dee5d8d991464e1e6cad2e1",
            "BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS",
            "BLS_ANNUAL_SCHEDULE_US_EASTERN",
            "DUKASCOPY_HOURLY_TICK_BI5",
            "FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION",
            "READY_FOR_DATA_FEASIBILITY_FREEZE",
            "UNRESOLVED_OFFICIAL_EVENT_TIMES",
            "INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
            "ATS2-RF-028",
        ),
    )
    tool_ok = require_markers(
        TOOL,
        (
            'TASK_ID = "ATS2-RF-027"',
            'HYPOTHESIS_ID = "HYP-0006"',
            "BLS_SNAPSHOT_MANIFEST",
            "BLS_CALENDAR_CSV",
            "OwnerInputRequiredError",
            "load_bls_snapshot_manifest",
            "load_bls_schedule_snapshots",
            "bls_snapshot_bundle_hash",
            "write_bls_calendar_csv",
            "live BLS network access is disabled",
            "cpi_schedule_candidates",
            'SOURCE_SYMBOL = "EURUSD"',
            "EXTERNAL_SOURCE_FAILURE_POLICY",
            "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF",
            "HYP0005_LEFT_START",
            "HYP0005_RIGHT_START",
            "required_tick_hours",
            "DUKASCOPY_NORMAL_RUNTIME_NETWORK_MODE",
            "require_local_dukascopy_snapshot",
            "load_local_tick_hour",
            "decode_tick_object",
            "event_geometry",
            "BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS",
            "BLS_ANNUAL_SCHEDULE_US_EASTERN",
            "outcome_metrics_computed",
            "primary_claim_evaluated",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        ),
    )
    test_ok = require_markers(
        TEST,
        (
            "test_live_bls_network_access_is_prohibited",
            "test_external_source_failure_hands_off_after_first_attempt",
            "test_normal_rf027_dukascopy_runtime_is_offline_only",
            "test_snapshot_manifest_requires_exact_2003_2021_contract",
            "test_missing_snapshot_bundle_is_owner_input_not_hypothesis_failure",
            "test_legacy_schedule_text_parses_cpi_and_same_time_release",
            "test_et_conversion_uses_pre_and_post_2007_dst_rules",
            "test_schedule_candidates_preserve_frozen_development_interval",
            "test_bls_calendar_csv_contains_only_event_identity_and_provenance",
            "test_decode_tick_object_validates_coherent_bid_ask",
            "test_required_tick_hours_are_bounded_and_exclude_hyp0005",
            "test_event_geometry_uses_timestamps_only_and_requires_strict_pre_release",
            "test_geometry_output_schema_contains_no_price_or_outcome_fields",
            "test_preparation_decision_is_non_market_geometry_gate",
        ),
    )
    controlled_tool_ok = require_markers(
        CONTROLLED_DOWNLOAD_TOOL,
        (
            'TASK_ID = "ATS2-RF-027"',
            'SUBSTAGE = "DUKASCOPY_CONTROLLED_PRELOAD"',
            'SOURCE_POLICY = "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF"',
            'CANONICAL_BASE = "https://datafeed.dukascopy.com/datafeed"',
            "AUTHORIZED_EVENT_COUNT = 217",
            "AUTHORIZED_REQUIRED_OBJECT_COUNT = 1085",
            "AUTHORIZED_CALENDAR_SHA256",
            "OWNER_AUTHORIZATION_REQUIRED",
            "OWNER_AUTHORIZATION_CONSUMED",
            "ACTIVE_AUTHORIZATION_MARKER",
            "canonical_authorization_is_active",
            "DRY_RUN_READY",
            "SOURCE_BLOCKED",
            '"outcome_metrics_computed": False',
            '"primary_claim_evaluated": False',
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        ),
    )
    controlled_test_ok = require_markers(
        CONTROLLED_DOWNLOAD_TEST,
        (
            "test_inventory_uses_frozen_required_hours_and_canonical_base",
            "test_controlled_download_stops_after_first_external_failure",
            "test_controlled_download_does_not_overwrite_existing_file",
            "test_execute_requires_explicit_owner_authorization",
            "test_execute_rejects_consumed_canonical_authorization",
            "test_dry_run_never_starts_controlled_download",
        ),
    )
    browser_pilot_tool_ok = require_markers(
        BROWSER_PILOT_TOOL,
        (
            'TASK_ID = "ATS2-RF-027"',
            'SUBSTAGE = "DUKASCOPY_BROWSER_PILOT_50"',
            'SOURCE_IDENTITY = "DUKASCOPY_HOURLY_TICK_BI5"',
            "PILOT_OBJECT_COUNT = 50",
            "MAX_ATTEMPTS_PER_OBJECT = 2",
            "OWNER_AUTHORIZED_BROWSER_PILOT_50_2026_10_05",
            "SKIPPED_AFTER_2_ATTEMPTS",
            "CONSUMED_SENTINEL",
            "canonical_authorization_is_active",
            "promote_valid_download",
            '"outcome_metrics_computed": False',
            '"primary_claim_evaluated": False',
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        ),
    )
    browser_pilot_test_ok = require_markers(
        BROWSER_PILOT_TEST,
        (
            "test_pilot_inventory_selects_first_50_missing",
            "test_run_pilot_retries_once_then_skips",
            "test_consumed_sentinel_blocks_before_browser",
            "test_promote_valid_download_preserves_bytes_and_validates",
        ),
    )
    browser_batch_250_tool_ok = require_markers(
        BROWSER_BATCH_250_TOOL,
        (
            'TASK_ID = "ATS2-RF-027"',
            'SUBSTAGE = "DUKASCOPY_BROWSER_BATCH_250"',
            'SOURCE_IDENTITY = "DUKASCOPY_HOURLY_TICK_BI5"',
            "BATCH_OBJECT_COUNT = 250",
            "MAX_ATTEMPTS_PER_OBJECT = 2",
            "OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05",
            "SKIPPED_AFTER_2_ATTEMPTS",
            "CONSUMED_SENTINEL",
            "canonical_authorization_is_active",
            "run_batch",
            '"outcome_metrics_computed": False',
            '"primary_claim_evaluated": False',
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        ),
    )
    browser_batch_250_test_ok = require_markers(
        BROWSER_BATCH_250_TEST,
        (
            "test_batch_inventory_selects_first_250_missing",
            "test_run_batch_retries_once_then_skips",
            "test_consumed_sentinel_blocks_before_browser",
        ),
    )
    browser_remaining_748_tool_ok = require_markers(
        BROWSER_REMAINING_748_TOOL,
        (
            'TASK_ID = "ATS2-RF-027"',
            'SUBSTAGE = "DUKASCOPY_BROWSER_REMAINING_748"',
            'SOURCE_IDENTITY = "DUKASCOPY_HOURLY_TICK_BI5"',
            "REMAINING_OBJECT_COUNT = 748",
            "MAX_ATTEMPTS_PER_OBJECT = 2",
            "OWNER_AUTHORIZED_REMAINING_748_2026_10_05",
            "inventory drift",
            "SKIPPED_AFTER_2_ATTEMPTS",
            "CONSUMED_SENTINEL",
            "canonical_authorization_is_active",
            "run_remaining",
            '"outcome_metrics_computed": False',
            '"primary_claim_evaluated": False',
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        ),
    )
    browser_remaining_748_test_ok = require_markers(
        BROWSER_REMAINING_748_TEST,
        (
            "test_remaining_inventory_selects_exact_748_missing",
            "test_remaining_inventory_blocks_on_count_drift",
            "test_run_remaining_retries_once_then_skips",
            "test_consumed_sentinel_blocks_before_browser",
        ),
    )
    state_ok = require_markers(
        STATE,
        (
            'last_completed_task_id: "ATS2-RF-026"',
            'next_task_id: "ATS2-RF-027"',
            'current_task: "ATS2-RF-027"',
            'next_task: "ATS2-RF-028"',
            'rf026_verified_commit: "5e0ff9e4481e5dc28c14a73adcf32433715973a3"',
            'strategy_5_data_feasibility_prep_status: "RF027_SOURCE_BUNDLE_COMPLETE_READY_FOR_EXACT_MAIN_PREPARATION"',
            'strategy_5_data_feasibility_prep_decision: "PENDING_EXACT_MAIN_PREPARATION_NO_OUTCOME"',
            'strategy_5_bls_runtime_network_mode: "PROHIBITED"',
            'strategy_5_bls_snapshot_years: "2003..2021"',
            "strategy_5_bls_snapshot_canonical_count: 19",
            'rf027_offline_architecture_merged_commit: "79a01623c3fef4deb3757e4d2940b8cd16b9bff3"',
            'rf027_latest_exact_main_blocker: "DUKASCOPY_HTTP_503_2004_03_17T13_00_00Z"',
            'strategy_5_bls_snapshot_intake_status: "CANONICAL_19_READY_LOCAL"',
            "strategy_5_bls_calendar_observed_event_count: 217",
            'strategy_5_bls_calendar_observed_sha256: "646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9"',
            'strategy_5_dukascopy_failed_hour: "2004-03-17T13:00:00Z"',
            "strategy_5_dukascopy_http_status: 503",
            'strategy_5_external_source_failure_policy: "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF"',
            'strategy_5_dukascopy_retry_rule: "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF_REQUIRES_OWNER_AUTHORIZATION"',
            'rf027_first_failure_policy_merged_commit: "367976fa7510d0fe8c3662d5b33a9889fc824c94"',
            "strategy_5_dukascopy_inventory_required_object_count: 1085",
            "strategy_5_dukascopy_inventory_existing_object_count: 37",
            "strategy_5_dukascopy_inventory_missing_object_count: 1048",
            "strategy_5_dukascopy_controlled_downloader_status: "
            '"SOURCE_BLOCKED_AFTER_AUTHORIZED_EXECUTE"',
            'strategy_5_dukascopy_controlled_downloader_branch: "MERGED_TO_MAIN"',
            "strategy_5_dukascopy_controlled_execution_status: "
            '"SOURCE_BLOCKED_AUTHORIZATION_CONSUMED"',
            "strategy_5_dukascopy_controlled_execution_authorization_count: 1",
            'strategy_5_dukascopy_controlled_execution_authorization_record: "AUTHORIZED_ONCE_BY_OWNER_2026_10_05"',
            'strategy_5_dukascopy_controlled_execution_commit: "f3151d8915b61d1a08e79cf27133764201475e65"',
            "strategy_5_dukascopy_controlled_execution_network_requests: 1",
            "strategy_5_dukascopy_controlled_execution_downloaded_count: 0",
            "strategy_5_dukascopy_controlled_execution_existing_after: 37",
            "strategy_5_dukascopy_controlled_execution_missing_after: 1048",
            'strategy_5_dukascopy_normal_runtime_network_mode: "PROHIBITED"',
            'strategy_5_dukascopy_snapshot_bundle_status: "COMPLETE_1085_OF_1085_ZERO_NETWORK_CONFIRMED"',
            'strategy_5_dukascopy_manual_browser_probe_status: "PASS_3_OF_3_VALID_BI5"',
            'strategy_5_dukascopy_browser_pilot_status: "PASS_50_OF_50_AUTHORIZATION_CONSUMED"',
            "strategy_5_dukascopy_browser_pilot_object_limit: 50",
            "strategy_5_dukascopy_browser_pilot_max_attempts_per_object: 2",
            'strategy_5_dukascopy_browser_pilot_source_mode: "CANONICAL_BROWSER_ASSISTED_DUKASCOPY_BI5"',
            'strategy_5_dukascopy_browser_pilot_execution_status: "COMPLETE_50_OF_50"',
            'strategy_5_dukascopy_browser_pilot_fallback_policy: "NO_ALTERNATE_HOSTNAME_MIRROR_PROXY_OR_PROVIDER"',
            "strategy_5_dukascopy_browser_pilot_outcome_computed: false",
            'strategy_5_dukascopy_browser_pilot_execution_commit: "c7a10c8bcd84ca4754db92af4c63f39c02101543"',
            "strategy_5_dukascopy_browser_pilot_selected_count: 50",
            "strategy_5_dukascopy_browser_pilot_promoted_count: 50",
            "strategy_5_dukascopy_browser_pilot_skipped_count: 0",
            "strategy_5_dukascopy_browser_pilot_expected_existing_after: 87",
            "strategy_5_dukascopy_browser_pilot_expected_missing_after: 998",
            'strategy_5_dukascopy_next_external_batch_status: "OWNER_AUTHORIZATION_REQUIRED"',
            'strategy_5_dukascopy_post_pilot_inventory_status: "CONFIRMED_ZERO_NETWORK"',
            "strategy_5_dukascopy_post_pilot_inventory_required_object_count: 1085",
            "strategy_5_dukascopy_post_pilot_inventory_existing_object_count: 87",
            "strategy_5_dukascopy_post_pilot_inventory_missing_object_count: 998",
            "strategy_5_dukascopy_post_pilot_inventory_network_requests: 0",
            "strategy_5_dukascopy_post_pilot_inventory_downloaded_count: 0",
            "strategy_5_dukascopy_post_pilot_inventory_semantic_missing_count: 0",
            "strategy_5_dukascopy_post_pilot_inventory_outcome_computed: false",
            'strategy_5_dukascopy_browser_batch_250_status: "PASS_250_OF_250_AUTHORIZATION_CONSUMED"',
            "strategy_5_dukascopy_browser_batch_250_object_limit: 250",
            "strategy_5_dukascopy_browser_batch_250_max_attempts_per_object: 2",
            'strategy_5_dukascopy_browser_batch_250_source_mode: "CANONICAL_BROWSER_ASSISTED_DUKASCOPY_BI5"',
            'strategy_5_dukascopy_browser_batch_250_execution_status: "COMPLETE_250_OF_250"',
            'strategy_5_dukascopy_browser_batch_250_fallback_policy: "NO_ALTERNATE_HOSTNAME_MIRROR_PROXY_OR_PROVIDER"',
            "strategy_5_dukascopy_browser_batch_250_outcome_computed: false",
            'strategy_5_dukascopy_browser_batch_250_execution_commit: "438bc59aa6f2cc81a762914f111017f75a2e46b2"',
            "strategy_5_dukascopy_browser_batch_250_selected_count: 250",
            "strategy_5_dukascopy_browser_batch_250_promoted_count: 250",
            "strategy_5_dukascopy_browser_batch_250_skipped_count: 0",
            "strategy_5_dukascopy_browser_batch_250_expected_existing_after: 337",
            "strategy_5_dukascopy_browser_batch_250_expected_missing_after: 748",
            'strategy_5_dukascopy_browser_batch_250_evidence_status: "FULL_JSON_MANIFEST_REVIEW_PASS"',
            "strategy_5_dukascopy_browser_batch_250_attempts_1_count: 250",
            "strategy_5_dukascopy_browser_batch_250_attempts_2_count: 0",
            "strategy_5_dukascopy_browser_batch_250_record_count_min: 341",
            "strategy_5_dukascopy_browser_batch_250_record_count_max: 8535",
            'strategy_5_dukascopy_browser_batch_250_json_sha256: "36e1301d551a69990ca707e7bf33da1ce07e5e88b1e7dc23a379a66b814e6b2c"',
            'strategy_5_dukascopy_browser_batch_250_manifest_sha256: "9aa6d7646c809f7a8fb2caaf421f13553ec30ba26dee5d8d991464e1e6cad2e1"',
            'strategy_5_dukascopy_post_batch_250_inventory_status: "CONFIRMED_ZERO_NETWORK"',
            "strategy_5_dukascopy_post_batch_250_inventory_required_object_count: 1085",
            "strategy_5_dukascopy_post_batch_250_inventory_existing_object_count: 337",
            "strategy_5_dukascopy_post_batch_250_inventory_missing_object_count: 748",
            "strategy_5_dukascopy_post_batch_250_inventory_network_requests: 0",
            "strategy_5_dukascopy_post_batch_250_inventory_downloaded_count: 0",
            "strategy_5_dukascopy_post_batch_250_inventory_semantic_missing_count: 0",
            "strategy_5_dukascopy_post_batch_250_inventory_outcome_computed: false",
            'strategy_5_dukascopy_browser_remaining_748_status: "PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED"',
            'strategy_5_dukascopy_browser_remaining_748_authorization_record: "OWNER_AUTHORIZED_REMAINING_748_2026_10_05"',
            "strategy_5_dukascopy_browser_remaining_748_object_count: 748",
            "strategy_5_dukascopy_browser_remaining_748_max_attempts_per_object: 2",
            'strategy_5_dukascopy_browser_remaining_748_source_mode: "CANONICAL_BROWSER_ASSISTED_DUKASCOPY_BI5"',
            'strategy_5_dukascopy_browser_remaining_748_execution_status: "COMPLETE_747_PROMOTED_1_SKIPPED"',
            'strategy_5_dukascopy_browser_remaining_748_execution_commit: "0131dd82d286814adaa76ff6e2524e0d000ca13c"',
            'strategy_5_dukascopy_browser_remaining_748_inventory_rule: "REQUIRE_EXACTLY_748_CURRENT_MISSING"',
            'strategy_5_dukascopy_browser_remaining_748_manifest_status: "MANIFEST_REVIEW_PASS_748_OF_748"',
            'strategy_5_dukascopy_browser_remaining_748_manifest_sha256: "a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4"',
            "strategy_5_dukascopy_browser_remaining_748_selected_count: 748",
            "strategy_5_dukascopy_browser_remaining_748_promoted_count: 747",
            "strategy_5_dukascopy_browser_remaining_748_skipped_count: 1",
            "strategy_5_dukascopy_browser_remaining_748_expected_existing_after: 1084",
            "strategy_5_dukascopy_browser_remaining_748_expected_missing_after: 1",
            'strategy_5_dukascopy_browser_remaining_748_evidence_status: "FULL_JSON_MANIFEST_REVIEW_PASS"',
            'strategy_5_dukascopy_browser_remaining_748_evidence_review_commit: "b4802ea909ff7c2436f43f817bf0160dbb67cffc"',
            "strategy_5_dukascopy_browser_remaining_748_attempts_1_count: 746",
            "strategy_5_dukascopy_browser_remaining_748_attempts_2_count: 2",
            "strategy_5_dukascopy_browser_remaining_748_record_count_min: 419",
            "strategy_5_dukascopy_browser_remaining_748_record_count_max: 31693",
            "strategy_5_dukascopy_browser_remaining_748_promoted_sha256_count: 747",
            "strategy_5_dukascopy_browser_remaining_748_promoted_sha256_unique_count: 747",
            "strategy_5_dukascopy_browser_remaining_748_promoted_sha256_duplicate_count: 0",
            'strategy_5_dukascopy_browser_remaining_748_json_sha256: "ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112"',
            "strategy_5_dukascopy_browser_remaining_748_skipped_ordinal: 159",
            'strategy_5_dukascopy_browser_remaining_748_skipped_hour: "2011-11-16T11:00:00Z"',
            'strategy_5_dukascopy_browser_remaining_748_skipped_source_url: "https://datafeed.dukascopy.com/datafeed/EURUSD/2011/10/16/11h_ticks.bi5"',
            'strategy_5_dukascopy_browser_remaining_748_skipped_local_path: "data/raw/dukascopy/hyp0006/EURUSD/2011/11/16/11h_ticks.bi5"',
            'strategy_5_dukascopy_browser_remaining_748_skipped_failure: "no_valid_bi5_download_within_45s_attempt_2"',
            'strategy_5_dukascopy_browser_remaining_748_skipped_file_status: "ABSENT"',
            'strategy_5_dukascopy_browser_remaining_748_consumed_sentinel_status: "VALIDATED_PASS"',
            'strategy_5_dukascopy_final_manual_intake_status: "PASS_OWNER_SUPPLIED_VALIDATED"',
            'strategy_5_dukascopy_final_manual_intake_hour: "2011-11-16T11:00:00Z"',
            'strategy_5_dukascopy_final_manual_intake_source_url: "https://datafeed.dukascopy.com/datafeed/EURUSD/2011/10/16/11h_ticks.bi5"',
            'strategy_5_dukascopy_final_manual_intake_local_path: "data/raw/dukascopy/hyp0006/EURUSD/2011/11/16/11h_ticks.bi5"',
            'strategy_5_dukascopy_final_manual_intake_sha256: "391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7"',
            "strategy_5_dukascopy_final_manual_intake_record_count: 6810",
            'strategy_5_dukascopy_final_manual_intake_decoder_status: "PASS"',
            "strategy_5_dukascopy_final_manual_intake_destination_existed_before: false",
            'strategy_5_dukascopy_final_manual_intake_byte_preserving_copy_status: "PASS"',
            'strategy_5_dukascopy_post_manual_intake_inventory_status: "CONFIRMED_ZERO_NETWORK_COMPLETE"',
            "strategy_5_dukascopy_post_manual_intake_inventory_required_object_count: 1085",
            "strategy_5_dukascopy_post_manual_intake_inventory_existing_object_count: 1085",
            "strategy_5_dukascopy_post_manual_intake_inventory_missing_object_count: 0",
            "strategy_5_dukascopy_post_manual_intake_inventory_network_requests: 0",
            "strategy_5_dukascopy_post_manual_intake_inventory_downloaded_count: 0",
            "strategy_5_dukascopy_post_manual_intake_inventory_semantic_missing_count: 0",
            "strategy_5_dukascopy_post_manual_intake_inventory_outcome_computed: false",
            'strategy_5_dukascopy_browser_remaining_748_fallback_policy: "NO_ALTERNATE_HOSTNAME_MIRROR_PROXY_OR_PROVIDER"',
            "strategy_5_dukascopy_browser_remaining_748_outcome_computed: false",
            "strategy_5_dukascopy_controlled_execution_authorized_command:",
            'rf027_controlled_downloader_merged_commit: "a638e49108e05e9618208ca577c6ebd0c74aa4e1"',
            "rf027_controlled_downloader_dry_run_commit: "
            '"a638e49108e05e9618208ca577c6ebd0c74aa4e1"',
            'rf027_controlled_downloader_dry_run_status: "DRY_RUN_READY"',
            "rf027_controlled_downloader_dry_run_event_count: 217",
            "rf027_controlled_downloader_dry_run_required_object_count: 1085",
            "rf027_controlled_downloader_dry_run_existing_object_count: 37",
            "rf027_controlled_downloader_dry_run_missing_object_count: 1048",
            "rf027_controlled_downloader_dry_run_network_requests: 0",
            'strategy_5_geometry_output_status: "NOT_CREATED_READY_FOR_RF027_PREPARATION"',
            "strategy_5_required_protected_hyp0005_source_requests: 0",
            "strategy_5_outcome_computed: false",
            'strategy_5_information_boundary: "NO_HYPOTHESIS_OUTCOME_COMPUTED"',
            'strategy_4_information_boundary: "NO_CONFIRMATORY_OUTCOME_COMPUTED"',
        ),
    )
    backlog_ok = require_markers(
        BACKLOG,
        (
            "ATS2-RF-026",
            "DONE / PASS",
            "ATS2-RF-027",
            "SOURCE-BLOCKED",
            "ATS2-RF-028",
            "FROZEN_LOCAL_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
            "OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
            "SOURCE_BLOCKED_AUTHORIZATION_CONSUMED",
            "1085",
            "PASS_250_OF_250_AUTHORIZATION_CONSUMED",
            "337",
            "748",
            "FULL_JSON_MANIFEST_REVIEW_PASS",
            "36e1301d551a69990ca707e7bf33da1ce07e5e88b1e7dc23a379a66b814e6b2c",
            "9aa6d7646c809f7a8fb2caaf421f13553ec30ba26dee5d8d991464e1e6cad2e1",
            "CONFIRMED_ZERO_NETWORK",
            "OWNER_AUTHORIZED_REMAINING_748_2026_10_05",
            "PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED",
            "0131dd82d286814adaa76ff6e2524e0d000ca13c",
            "a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4",
            "391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7",
            "6810",
            "CONFIRMED_ZERO_NETWORK_COMPLETE",
            "1085 / 1085",
            "ATS_TASK_CHECK.bat",
            "ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112",
            "2011-11-16T11:00:00Z",
            "no_valid_bi5_download_within_45s_attempt_2",
            "FULL_JSON_MANIFEST_REVIEW_PASS",
            "tools/hyp0006_dukascopy_browser_remaining_748.py",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        ),
    )
    docs_ok = all(
        (
            require_markers(
                HANDOFF,
                (
                    "ATS2-RF-027",
                    "f3151d8915b61d1a08e79cf27133764201475e65",
                    "SOURCE_BLOCKED_AUTHORIZATION_CONSUMED",
                    "OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
                    "FROZEN_LOCAL_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
                    "OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05",
                    "PASS_250_OF_250_AUTHORIZATION_CONSUMED",
                    "438bc59aa6f2cc81a762914f111017f75a2e46b2",
                    "tools/hyp0006_dukascopy_browser_batch_250.py",
                    "OWNER_AUTHORIZED_REMAINING_748_2026_10_05",
                    "PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED",
                    "0131dd82d286814adaa76ff6e2524e0d000ca13c",
                    "a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4",
                    "391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7",
                    "6810",
                    "CONFIRMED_ZERO_NETWORK_COMPLETE",
                    "1085 / 1085",
                    "ATS_TASK_CHECK.bat",
                    "ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112",
                    "2011-11-16T11:00:00Z",
                    "no_valid_bi5_download_within_45s_attempt_2",
                    "FULL_JSON_MANIFEST_REVIEW_PASS",
                    "tools/hyp0006_dukascopy_browser_remaining_748.py",
                    "NO_HYPOTHESIS_OUTCOME_COMPUTED",
                    "NO_CONFIRMATORY_OUTCOME_COMPUTED",
                ),
            ),
            require_markers(
                NEXT_STEP,
                (
                    "ATS2-RF-027",
                    "ATS2-RF-028",
                    "f3151d8915b61d1a08e79cf27133764201475e65",
                    "SOURCE_BLOCKED_AUTHORIZATION_CONSUMED",
                    "OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
                    "FROZEN_LOCAL_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
                    "OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05",
                    "PASS_250_OF_250_AUTHORIZATION_CONSUMED",
                    "438bc59aa6f2cc81a762914f111017f75a2e46b2",
                    "tools/hyp0006_dukascopy_browser_batch_250.py",
                    "OWNER_AUTHORIZED_REMAINING_748_2026_10_05",
                    "PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED",
                    "0131dd82d286814adaa76ff6e2524e0d000ca13c",
                    "a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4",
                    "391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7",
                    "6810",
                    "CONFIRMED_ZERO_NETWORK_COMPLETE",
                    "1085 / 1085",
                    "ATS_TASK_CHECK.bat",
                    "ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112",
                    "2011-11-16T11:00:00Z",
                    "no_valid_bi5_download_within_45s_attempt_2",
                    "FULL_JSON_MANIFEST_REVIEW_PASS",
                    "tools/hyp0006_dukascopy_browser_remaining_748.py",
                    "NO_HYPOTHESIS_OUTCOME_COMPUTED",
                ),
            ),
            require_markers(
                STATUS,
                (
                    "ATS2-RF-027",
                    "TECHNICAL_SOURCE_ACCESS_FAILURE",
                    "f3151d8915b61d1a08e79cf27133764201475e65",
                    "SOURCE_BLOCKED_AUTHORIZATION_CONSUMED",
                    "OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
                    "FROZEN_LOCAL_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
                    "OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05",
                    "PASS_250_OF_250_AUTHORIZATION_CONSUMED",
                    "438bc59aa6f2cc81a762914f111017f75a2e46b2",
                    "tools/hyp0006_dukascopy_browser_batch_250.py",
                    "OWNER_AUTHORIZED_REMAINING_748_2026_10_05",
                    "PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED",
                    "0131dd82d286814adaa76ff6e2524e0d000ca13c",
                    "a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4",
                    "391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7",
                    "6810",
                    "CONFIRMED_ZERO_NETWORK_COMPLETE",
                    "1085 / 1085",
                    "ATS_TASK_CHECK.bat",
                    "ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112",
                    "2011-11-16T11:00:00Z",
                    "no_valid_bi5_download_within_45s_attempt_2",
                    "FULL_JSON_MANIFEST_REVIEW_PASS",
                    "tools/hyp0006_dukascopy_browser_remaining_748.py",
                    "NO_HYPOTHESIS_OUTCOME_COMPUTED",
                    "NO_CONFIRMATORY_OUTCOME_COMPUTED",
                ),
            ),
        )
    )
    source_recovery_ok = require_markers(
        SOURCE_RECOVERY,
        (
            "SOURCE_BLOCKED_NO_OUTCOME",
            "f3151d8915b61d1a08e79cf27133764201475e65",
            "2004-03-17T13:00:00Z",
            "FROZEN_LOCAL_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
            "OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
            "DUKASCOPY_HOURLY_TICK_BI5",
            "OWNER_AUTHORIZED_BROWSER_PILOT_50_2026_10_05",
            "SKIPPED_AFTER_2_ATTEMPTS",
            "tools/hyp0006_dukascopy_browser_pilot.py",
            "PASS_50_OF_50_AUTHORIZATION_CONSUMED",
            "c7a10c8bcd84ca4754db92af4c63f39c02101543",
            "87",
            "998",
            "CONFIRMED_ZERO_NETWORK",
            "OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05",
            "tools/hyp0006_dukascopy_browser_batch_250.py",
            "PASS_250_OF_250_AUTHORIZATION_CONSUMED",
            "438bc59aa6f2cc81a762914f111017f75a2e46b2",
            "337",
            "748",
            "FULL_JSON_MANIFEST_REVIEW_PASS",
            "36e1301d551a69990ca707e7bf33da1ce07e5e88b1e7dc23a379a66b814e6b2c",
            "9aa6d7646c809f7a8fb2caaf421f13553ec30ba26dee5d8d991464e1e6cad2e1",
            "CONFIRMED_ZERO_NETWORK",
            "OWNER_AUTHORIZED_REMAINING_748_2026_10_05",
            "PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED",
            "0131dd82d286814adaa76ff6e2524e0d000ca13c",
            "a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4",
            "391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7",
            "6810",
            "CONFIRMED_ZERO_NETWORK_COMPLETE",
            "1085 / 1085",
            "ATS_TASK_CHECK.bat",
            "ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112",
            "2011-11-16T11:00:00Z",
            "no_valid_bi5_download_within_45s_attempt_2",
            "FULL_JSON_MANIFEST_REVIEW_PASS",
            "tools/hyp0006_dukascopy_browser_remaining_748.py",
            "REQUIRE_EXACTLY_748_CURRENT_MISSING",
            "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        ),
    )

    return all(
        (
            protocol_ok,
            tool_ok,
            test_ok,
            controlled_tool_ok,
            controlled_test_ok,
            browser_pilot_tool_ok,
            browser_pilot_test_ok,
            browser_batch_250_tool_ok,
            browser_batch_250_test_ok,
            browser_remaining_748_tool_ok,
            browser_remaining_748_test_ok,
            state_ok,
            backlog_ok,
            docs_ok,
            source_recovery_ok,
            check_frozen_lineage(),
        )
    )


def validate_bls_calendar(payload: dict[str, Any]) -> bool:
    path = ROOT / BLS_CALENDAR_CSV
    if not path.is_file():
        print("[FAIL] RF-027 BLS calendar CSV missing", flush=True)
        return False

    expected_digest = payload.get("bls_calendar_csv_sha256")
    if not isinstance(expected_digest, str) or not SHA256_RE.fullmatch(expected_digest):
        print("[FAIL] invalid RF-027 BLS calendar SHA-256 field", flush=True)
        return False
    if sha256_file(path) != expected_digest:
        print("[FAIL] RF-027 BLS calendar SHA-256 mismatch", flush=True)
        return False

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = tuple(next(reader, []))

    if header != EXPECTED_BLS_CALENDAR_HEADER:
        print(f"[FAIL] RF-027 BLS calendar header mismatch: {header}", flush=True)
        return False

    lowered = {name.lower() for name in header}
    for field in PROHIBITED_OUTCOME_FIELDS:
        if field in lowered:
            print(f"[FAIL] prohibited field in RF-027 BLS calendar: {field}", flush=True)
            return False

    print("[PASS] RF-027 frozen BLS calendar identity and outcome-free schema", flush=True)
    return True


def validate_geometry_csv(payload: dict[str, Any]) -> bool:
    path = ROOT / GEOMETRY_CSV
    if not path.is_file():
        print("[FAIL] RF-027 geometry CSV missing", flush=True)
        return False

    expected_digest = payload.get("geometry_csv_sha256")
    if not isinstance(expected_digest, str) or not SHA256_RE.fullmatch(expected_digest):
        print("[FAIL] invalid RF-027 geometry CSV SHA-256 field", flush=True)
        return False
    if sha256_file(path) != expected_digest:
        print("[FAIL] RF-027 geometry CSV SHA-256 mismatch", flush=True)
        return False

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = tuple(next(reader, []))

    if header != EXPECTED_GEOMETRY_HEADER:
        print(f"[FAIL] RF-027 geometry header mismatch: {header}", flush=True)
        return False

    lowered = {name.lower() for name in header}
    for field in PROHIBITED_OUTCOME_FIELDS:
        if field in lowered:
            print(f"[FAIL] prohibited field in RF-027 geometry CSV: {field}", flush=True)
            return False

    print("[PASS] RF-027 geometry CSV identity and outcome-free schema", flush=True)
    return True


def validate_local_result(payload: dict[str, Any], commit: str) -> bool:
    print("\n== RF-027 machine preparation result ==", flush=True)
    passed = True

    exact_pairs: tuple[tuple[str, Any], ...] = (
        ("task_id", TASK_ID),
        ("hypothesis_id", "HYP-0006"),
        ("git_commit", commit),
        ("evidence_classification", "DEVELOPMENT_EXPLORATORY_ONLY"),
        (
            "event_inventory_source",
            "BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS",
        ),
        ("event_time_source", "BLS_ANNUAL_SCHEDULE_US_EASTERN"),
        ("quote_source", "DUKASCOPY_HOURLY_TICK_BI5"),
        ("bls_snapshot_count", 19),
        ("protected_hyp0005_source_requests", 0),
        ("outcome_metrics_computed", False),
        ("primary_claim_evaluated", False),
        ("information_boundary", "NO_HYPOTHESIS_OUTCOME_COMPUTED"),
    )
    for key, expected in exact_pairs:
        if payload.get(key) != expected:
            print(
                f"[FAIL] RF-027 result field {key}: {payload.get(key)!r} != {expected!r}",
                flush=True,
            )
            passed = False

    decision = payload.get("preparation_decision")
    if decision not in ALLOWED_DECISIONS:
        print(f"[FAIL] invalid RF-027 preparation decision: {decision}", flush=True)
        passed = False

    count_keys = (
        "candidate_event_count",
        "resolved_event_time_count",
        "same_time_bls_cluster_count",
        "requested_tick_object_count",
        "acquired_tick_object_count",
        "missing_tick_object_count",
        "complete_timestamp_geometry_event_count",
    )
    for key in count_keys:
        value = payload.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            print(f"[FAIL] invalid non-negative count {key}: {value!r}", flush=True)
            passed = False

    candidate_count = payload.get("candidate_event_count")
    resolved_count = payload.get("resolved_event_time_count")
    if (
        isinstance(candidate_count, int)
        and isinstance(resolved_count, int)
        and candidate_count != resolved_count
    ):
        print("[FAIL] RF-027 event denominator does not reconcile", flush=True)
        passed = False

    manifest_path = str(BLS_SNAPSHOT_MANIFEST).replace("\\", "/")
    if payload.get("bls_snapshot_manifest_relative_path") != manifest_path:
        print("[FAIL] unexpected RF-027 BLS snapshot manifest path", flush=True)
        passed = False
    manifest_digest = payload.get("bls_snapshot_manifest_sha256")
    if not isinstance(manifest_digest, str) or not SHA256_RE.fullmatch(manifest_digest):
        print("[FAIL] invalid RF-027 BLS manifest SHA-256", flush=True)
        passed = False
    elif sha256_file(ROOT / BLS_SNAPSHOT_MANIFEST) != manifest_digest:
        print("[FAIL] RF-027 BLS manifest SHA-256 mismatch", flush=True)
        passed = False

    for key in (
        "bls_snapshot_bundle_sha256",
        "bls_calendar_csv_sha256",
        "source_bundle_sha256",
        "geometry_csv_sha256",
    ):
        value = payload.get(key)
        if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
            print(f"[FAIL] invalid RF-027 SHA-256 field {key}: {value!r}", flush=True)
            passed = False

    expected_calendar_path = str(BLS_CALENDAR_CSV).replace("\\", "/")
    if payload.get("bls_calendar_csv_relative_path") != expected_calendar_path:
        print("[FAIL] unexpected RF-027 BLS calendar path", flush=True)
        passed = False

    expected_geometry_path = str(GEOMETRY_CSV).replace("\\", "/")
    if payload.get("geometry_csv_relative_path") != expected_geometry_path:
        print("[FAIL] unexpected RF-027 geometry CSV path", flush=True)
        passed = False

    for forbidden in (
        "pre_abs_60m_return",
        "post_abs_60m_return",
        "primary_inequality",
        "trading_pnl",
    ):
        if forbidden in payload:
            print(f"[FAIL] prohibited outcome key in RF-027 result: {forbidden}", flush=True)
            passed = False

    if not validate_bls_calendar(payload):
        passed = False
    if not validate_geometry_csv(payload):
        passed = False

    if passed:
        print(f"[PASS] RF-027 preparation result: {decision}", flush=True)
    return passed


def prepare_or_validate(commit: str) -> bool:
    existing: dict[str, Any] | None = None
    result_path = ROOT / LOCAL_RESULT
    if result_path.is_file():
        try:
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            loaded = None
        if isinstance(loaded, dict) and loaded.get("git_commit") == commit:
            existing = loaded

    if existing is None:
        if not run(
            "RF-027 HYP-0006 official-event and tick geometry preparation",
            [sys.executable, str(TOOL)],
        ):
            return False
        try:
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[FAIL] cannot load RF-027 result: {exc}", flush=True)
            return False
        if not isinstance(loaded, dict):
            print("[FAIL] RF-027 result is not a JSON object", flush=True)
            return False
        existing = loaded
    else:
        print(
            "\nExisting exact-commit RF-027 local preparation result found; validating.",
            flush=True,
        )

    return validate_local_result(existing, commit)


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    branch = git_output("branch", "--show-current")
    commit = git_output("rev-parse", "HEAD")
    print(f"Branch: {branch or '<detached>'}")
    print(f"Commit: {commit}")

    emit_progress(35)
    staged = check_rf027_contract()

    emit_progress(50)
    governance = run(
        "RF-027 repository governance validation",
        [sys.executable, "tools/validate_repo.py"],
    )

    emit_progress(65)
    full_ci = run(
        "full ATS Local CI before RF-027 source preparation",
        [sys.executable, "tools/verify_repo.py"],
    )

    if not all((staged, governance, full_ci)):
        print("\nHYP-0005 outcome computed by RF-027: NO", flush=True)
        print("HYP-0006 outcome computed by RF-027: NO", flush=True)
        print("\nATS CURRENT TASK CHECK: FAIL", flush=True)
        return 1

    emit_progress(80)
    prepared = prepare_or_validate(commit)

    if prepared:
        emit_progress(100)

    print("\nHYP-0005 outcome computed by RF-027: NO", flush=True)
    print("HYP-0006 outcome computed by RF-027: NO", flush=True)
    print(f"\nATS CURRENT TASK CHECK: {'PASS' if prepared else 'FAIL'}", flush=True)
    return 0 if prepared else 1


if __name__ == "__main__":
    raise SystemExit(main())
