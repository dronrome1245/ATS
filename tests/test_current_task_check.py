"""Synthetic RF-032 offline intake checks; no market execution or network."""

from __future__ import annotations

import hashlib
import inspect
from pathlib import Path

import pytest

from tools import current_task_check as check


def archived_synthetic_result() -> dict:
    """A synthetic schema fixture; NEVER from HYP-0006 raw market quotes."""
    return {
        "git_commit": check.RF030_MAIN_COMMIT,
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
        "event_observations": [
            {
                "event_id": f"SYNTHETIC-{i:03d}",
                "same_time_bls_labels": ["Simultaneous diagnostic"],
            }
            for i in range(216)
        ],
    }


def test_saved_reveal_identity_rejects_drift() -> None:
    value = archived_synthetic_result()
    check.check_saved_result_identity(value)
    value["primary_inequality_pass"] = False
    with pytest.raises(check.TaskCheckError, match="primary_inequality_pass"):
        check.check_saved_result_identity(value)
    value = archived_synthetic_result()
    value["event_observations"].pop()
    with pytest.raises(check.TaskCheckError, match="216 saved event"):
        check.check_saved_result_identity(value)
    value = archived_synthetic_result()
    value["event_observations"][0]["same_time_bls_labels"] = []
    with pytest.raises(check.TaskCheckError, match="BLS overlap flags"):
        check.check_saved_result_identity(value)


def test_hash_only_archive_function_preserves_exact_bytes(tmp_path: Path) -> None:
    archive = tmp_path / "archive.json"
    raw = b'{"synthetic":"fixture"}\n'
    archive.write_bytes(raw)
    assert check.sha256_file(archive) == hashlib.sha256(raw).hexdigest()
    archive.write_bytes(raw + b" ")
    assert check.sha256_file(archive) != hashlib.sha256(raw).hexdigest()


def test_rf032_checker_never_executes_market_runner() -> None:
    source = inspect.getsource(check)
    assert 'TASK_ID = "ATS2-RF-032"' in source
    assert "--execute-first-reveal" not in source
    assert "prepare_first_reveal(" not in source
    assert "verify_repo.py" in source
    assert "NO_CONFIRMATORY_OUTCOME_COMPUTED" in source


def test_rf032_source_contract_is_offline_only() -> None:
    check.check_rf023_offline_source_architecture()


def test_rf032_file_inventory_is_metadata_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(check, "RF023_SNAPSHOT_ROOT", tmp_path)
    path = tmp_path / "2003" / "05"
    path.mkdir(parents=True)
    (path / "BID_candles_hour_1.json").write_bytes(b"synthetic")
    (path / "ASK_candles_hour_1.json").write_bytes(b"synthetic")
    check.record_local_rf023_file_inventory()
    printed = capsys.readouterr().out
    assert "2003-05 complete local file pairs: json" in printed
    assert "2026-09 complete local file pairs: NONE" in printed
    assert "SOURCE_INPUT_REQUIRED" in printed
    assert "NO_CONFIRMATORY_OUTCOME_COMPUTED" in printed
