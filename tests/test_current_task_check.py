"""Synthetic RF-030 gate tests; no market data or reveal execution."""

from __future__ import annotations

import hashlib
import statistics
from pathlib import Path

import pytest

from tools import current_task_check as check


def test_reveal_artifact_guard_blocks_partial_pair(tmp_path: Path) -> None:
    result = tmp_path / "result.json"
    report = tmp_path / "report.txt"
    assert check.reveal_artifact_state(result, report) == "ABSENT"
    result.write_text("{}\n", encoding="utf-8")
    with pytest.raises(check.TaskCheckError, match="partial reveal artifacts"):
        check.reveal_artifact_state(result, report)
    report.write_text("preserved\n", encoding="utf-8")
    assert check.reveal_artifact_state(result, report) == "EXISTING_PAIR"


def test_full_bi5_hash_gate_checks_every_identity(tmp_path: Path) -> None:
    identities = []
    for index, payload in enumerate((b"first", b"second")):
        relative = f"data/raw/dukascopy/hyp0006/EURUSD/2020/01/01/0{index}h_ticks.bi5"
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        identities.append(
            {
                "relative_path": relative,
                "hour_start": f"2020-01-01T0{index}:00:00Z",
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    check.verify_all_bi5_objects(identities, root=tmp_path, expected_count=2)
    (tmp_path / identities[1]["relative_path"]).write_bytes(b"changed")
    with pytest.raises(check.TaskCheckError, match="SHA-256 mismatch"):
        check.verify_all_bi5_objects(identities, root=tmp_path, expected_count=2)


def synthetic_reveal(*, advance: bool = True) -> tuple[dict, dict, dict, str]:
    event_ids = [f"SYNTHETIC-{index:03d}" for index in range(216)]
    events = [
        {
            "event_id": event_id,
            "release_time_utc": "2020-01-01T13:30:00Z",
            "same_time_bls_labels": [],
        }
        for event_id in event_ids
    ]
    observations = [
        {
            **event,
            "pre_abs_60m_return": index / 1_000_000,
            "post_abs_60m_return": (index + 1 if advance else index - 1) / 1_000_000,
            "pre_release_relative_spread": 1 / 100_000,
            "first_post_release_relative_spread": 2 / 100_000,
        }
        for index, event in enumerate(events, start=1)
    ]
    pre = [item["pre_abs_60m_return"] for item in observations]
    post = [item["post_abs_60m_return"] for item in observations]
    exact_commit = "a" * 40
    result = {
        "schema_version": "hyp0006-proto01-reveal-1",
        "hypothesis_id": "HYP-0006",
        "prototype_id": "PROTO-01",
        "git_commit": exact_commit,
        "rf028_git_commit": check.RF028_COMMIT,
        "rf028_json_sha256": check.RF028_JSON_SHA256,
        "dataset_id": "DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001",
        "dataset_version": "1.0.0",
        "source_bundle_sha256": check.FROZEN_SOURCE_SHA256,
        "geometry_csv_sha256": check.FROZEN_GEOMETRY_SHA256,
        "evidence_classification": "DEVELOPMENT_EXPLORATORY_ONLY",
        "candidate_event_count": 217,
        "eligible_event_count": 216,
        "ineligible_event_count": 1,
        "ineligible_event_ids": [check.FROZEN_INELIGIBLE_ID],
        "event_observations": observations,
        "median_pre_abs_60m_return": statistics.median(pre),
        "median_post_abs_60m_return": statistics.median(post),
        "primary_inequality_pass": advance,
        "prototype_decision": "ADVANCE_TO_ECONOMIC_SCREEN" if advance else "REJECT",
        "next_action": (
            "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4" if advance else "STOP_HYP0006"
        ),
        "median_pre_release_relative_spread": 1 / 100_000,
        "median_first_post_release_relative_spread": 2 / 100_000,
        "same_time_bls_flagged_event_count": 0,
        "calendar_year_diagnostics": [
            {
                "year": 2020,
                "count": 216,
                "share_of_eligible": 1.0,
                "median_pre_abs_return": statistics.median(pre),
                "median_post_abs_return": statistics.median(post),
            }
        ],
        "max_calendar_year_event_share": 1.0,
        "outcome_metrics_computed": True,
        "primary_claim_evaluated": True,
        "information_boundary": "DEVELOPMENT_REVEALED_EXPLORATORY_ONLY",
    }
    return result, {"events": events}, {"eligible_event_ids": event_ids}, exact_commit


def test_reveal_payload_enforces_216_observations_and_decision_rule() -> None:
    result, rf027, rf028, exact_commit = synthetic_reveal()
    check.validate_reveal_payload(result, rf027, rf028, exact_commit)
    result["prototype_decision"] = "REJECT"
    with pytest.raises(check.TaskCheckError, match="prototype decision drift"):
        check.validate_reveal_payload(result, rf027, rf028, exact_commit)

    rejected, rf027, rf028, exact_commit = synthetic_reveal(advance=False)
    check.validate_reveal_payload(rejected, rf027, rf028, exact_commit)
    assert rejected["prototype_decision"] == "REJECT"
    assert rejected["next_action"] == "STOP_HYP0006"
