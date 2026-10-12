"""RF-037 synthetic-only one-shot reveal gate tests; no real quote data is opened."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import hyp0005_first_reveal_gate as gate

SYNTHETIC_COMMIT = "SYNTHETIC_MAIN_FOR_GATING_ONLY"


def _fixture_result(commit: str, *, passes: bool) -> dict:
    """Synthetic decision directions; neither is evidence about HYP-0005."""
    core_movement = 0.003 if passes else 0.001
    core_spread = 0.0001 if passes else 0.0003
    movement = core_movement > 0.002
    spread = core_spread <= 0.0002
    both = movement and spread
    decision = (
        "CONFIRMATORY_STRUCTURAL_PASS" if both else "CONFIRMATORY_STRUCTURAL_FAIL"
    )
    reason = (
        "BOTH_PRIMARY_INEQUALITIES_MET"
        if both
        else "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED"
    )
    action = (
        "REVIEW_CONFIRMATORY_STRUCTURAL_EVIDENCE_NO_DIRECT_R4"
        if both
        else "RETAIN_NEGATIVE_CONFIRMATORY_EVIDENCE_NO_RETUNING"
    )
    return {
        "schema_version": "hyp0005-confirmatory-proto01-result-1",
        "hypothesis_id": "HYP-0005",
        "parent_idea_id": "IDEA-0004",
        "prototype_id": "PROTO-01",
        "evidence_class": "CONFIRMATORY_STRUCTURAL_NOT_INDEPENDENT_EXAM",
        "measurement_label": "H1_OPEN_PROXY_STRUCTURAL_NO_TRADING_PNL",
        "outcome_metrics_computed": True,
        "primary_claim_evaluated": True,
        "geometry": gate.EXPECTED_GEOMETRY,
        "dataset": {
            "dataset_id": gate.DATASET_ID,
            "dataset_version": "1.0.0",
            "derived_csv_sha256": gate.CSV_SHA256,
            "source_bundle_sha256": gate.SOURCE_SHA256,
            "boundary_availability_mode": "H1_OPEN_PROXY_AT_EVENT_TIME",
            "exact_tick_boundary_time_known": False,
            "confirmatory_preparation_sha256": gate.PREP_SHA256,
        },
        "run_context": {"git_commit": commit, "completed_at": "SYNTHETIC_TIMESTAMP"},
        "primary": {
            "movement_inequality_pass": movement,
            "spread_inequality_pass": spread,
            "both_primary_inequalities_pass": both,
        },
        "bucket_metrics": {
            "CORE_ACTIVE": {
                "observation_count": 838,
                "mean_abs_next_1h_return": 0.003,
                "median_abs_next_1h_return": core_movement,
                "median_relative_spread": core_spread,
            },
            "OFF_HOURS": {
                "observation_count": 837,
                "mean_abs_next_1h_return": 0.002,
                "median_abs_next_1h_return": 0.002,
                "median_relative_spread": 0.0002,
            },
            "TRANSITION": {
                "observation_count": 316,
                "mean_abs_next_1h_return": 0.0025,
                "median_abs_next_1h_return": 0.0025,
                "median_relative_spread": 0.00015,
            },
        },
        "calendar_year_diagnostics": {"SYNTHETIC_ONLY": True},
        "decision": decision,
        "decision_reason": reason,
        "next_action": action,
        "limitations": ["SYNTHETIC_ONLY_NOT_HYPOTHESIS_EVIDENCE"],
    }


def _fixture_report(result: dict) -> str:
    return "\n".join(
        (
            "HYP-0005 CONFIRMATORY STRUCTURAL PROTO-01 REVEAL",
            "No directional trading strategy, economic proof, or independent examination",
            f"Git commit: {result['run_context']['git_commit']}",
            f"Decision: {result['decision']}",
            f"Reason: {result['decision_reason']}",
            f"Next action: {result['next_action']}",
            f"Both predeclared inequalities pass: "
            f"{result['primary']['both_primary_inequalities_pass']}",
        )
    ) + "\n"


def _setup(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    passes: bool = True,
) -> tuple[dict, list[str]]:
    monkeypatch.setattr(gate, "RESULT_JSON", tmp_path / "result.json")
    monkeypatch.setattr(gate, "RESULT_TEXT", tmp_path / "result.txt")
    monkeypatch.setattr(gate, "CONSUMED", tmp_path / "consumed.json")
    monkeypatch.setattr(gate, "RECEIPT", tmp_path / "receipt.json")
    monkeypatch.setattr(gate, "_check_exact_main", lambda commit: None)
    monkeypatch.setattr(gate, "_verify_frozen_input_hashes", lambda: None)
    result = _fixture_result(SYNTHETIC_COMMIT, passes=passes)
    calls: list[str] = []

    def invoke() -> dict:
        assert gate.CONSUMED.is_file()
        assert not gate.RECEIPT.exists()
        calls.append("SYNTHETIC_CALL")
        gate.RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        gate.RESULT_TEXT.write_text(_fixture_report(result), encoding="utf-8")
        return result

    monkeypatch.setattr(gate, "_invoke_frozen_runner", invoke)
    return result, calls


@pytest.mark.parametrize("passes", [True, False])
def test_rf037_synthetic_first_reveal_consumes_once_before_result(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, passes: bool
) -> None:
    _result, calls = _setup(tmp_path, monkeypatch, passes=passes)
    receipt = gate.execute_or_verify_once(
        expected_commit=SYNTHETIC_COMMIT, authorized=True
    )
    assert calls == ["SYNTHETIC_CALL"]
    assert receipt["status"] == "FIRST_REVEAL_COMPLETED_ONCE"
    assert receipt["authorization"] == gate.AUTHORIZATION
    assert receipt["decision"] == (
        "CONFIRMATORY_STRUCTURAL_PASS" if passes else "CONFIRMATORY_STRUCTURAL_FAIL"
    )
    assert gate.CONSUMED.is_file()
    assert gate.RECEIPT.is_file()
    original_json = gate.RESULT_JSON.read_bytes()
    original_text = gate.RESULT_TEXT.read_bytes()
    monkeypatch.setattr(
        gate,
        "_invoke_frozen_runner",
        lambda: pytest.fail("a saved first reveal must NEVER invoke market runner"),
    )
    repeated = gate.execute_or_verify_once(
        expected_commit=SYNTHETIC_COMMIT, authorized=True
    )
    assert repeated == receipt
    assert gate.RESULT_JSON.read_bytes() == original_json
    assert gate.RESULT_TEXT.read_bytes() == original_text


def test_rf037_unauthorized_first_reveal_is_blocked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _setup(tmp_path, monkeypatch)
    with pytest.raises(
        gate.FirstRevealGateError, match="OWNER first reveal authorization"
    ):
        gate.execute_or_verify_once(expected_commit=SYNTHETIC_COMMIT)
    assert not gate.CONSUMED.exists()
    assert not gate.RESULT_JSON.exists()


@pytest.mark.parametrize("artifact", ["RESULT_JSON", "RESULT_TEXT", "RECEIPT"])
def test_rf037_orphaned_artifacts_block_before_synthetic_reveal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, artifact: str
) -> None:
    _result, calls = _setup(tmp_path, monkeypatch)
    getattr(gate, artifact).write_bytes(b"preexisting synthetic invalid artifact")
    with pytest.raises(gate.FirstRevealGateError, match="artifact already present"):
        gate.execute_or_verify_once(expected_commit=SYNTHETIC_COMMIT, authorized=True)
    assert calls == []
    assert not gate.CONSUMED.exists()


def test_rf037_consumed_failure_cannot_be_retried(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _result, calls = _setup(tmp_path, monkeypatch)

    def synthetic_failure() -> dict:
        assert gate.CONSUMED.is_file()
        calls.append("SYNTHETIC_FAILURE")
        raise RuntimeError("synthetic failure AFTER consumed marker")

    monkeypatch.setattr(gate, "_invoke_frozen_runner", synthetic_failure)
    with pytest.raises(gate.FirstRevealGateError, match="authorization CONSUMED"):
        gate.execute_or_verify_once(expected_commit=SYNTHETIC_COMMIT, authorized=True)
    assert calls == ["SYNTHETIC_FAILURE"]
    assert gate.CONSUMED.is_file()
    assert not gate.RECEIPT.exists()
    with pytest.raises(
        gate.FirstRevealGateError, match="consumed marker/receipt incomplete"
    ):
        gate.execute_or_verify_once(expected_commit=SYNTHETIC_COMMIT, authorized=True)
    assert calls == ["SYNTHETIC_FAILURE"]


def test_rf037_saved_result_sha_drift_is_blocked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _setup(tmp_path, monkeypatch)
    gate.execute_or_verify_once(expected_commit=SYNTHETIC_COMMIT, authorized=True)
    gate.RESULT_TEXT.write_bytes(gate.RESULT_TEXT.read_bytes() + b"synthetic-tamper")
    with pytest.raises(gate.FirstRevealGateError, match="report SHA-256 mismatch"):
        gate.execute_or_verify_once(expected_commit=SYNTHETIC_COMMIT, authorized=True)


def test_rf037_direct_cli_is_disabled() -> None:
    assert gate.main() == 2
