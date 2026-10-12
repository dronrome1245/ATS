"""Synthetic exact-main RF-037 gate tests; no protected price rows are opened."""

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


def test_rf037_current_task_requires_gate_and_never_invokes_runner_directly() -> None:
    source = inspect.getsource(check)
    main_source = inspect.getsource(check.main)
    assert 'TASK_ID = "ATS2-RF-037"' in source
    assert "--execute-first-reveal" not in source
    assert "def run_rf023_offline_once" not in source
    assert "check_rf034_output_absence()" not in main_source
    assert "check_rf024_preparation_identity()" in main_source
    assert "check_rf024_manifest_and_review()" in main_source
    assert "check_rf035_pre_reveal_runner_freeze(require_absence=False)" in main_source
    assert "check_rf036_gate_preparation(require_absence=False)" in main_source
    assert "check_rf037_one_shot_authorization()" in main_source
    assert "receipt = reveal_gate.execute_or_verify_once(expected_commit=commit, authorized=True)" in main_source
    assert "run_first_reveal_once(" not in main_source


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


def test_rf033_local_intake_hash_and_narrow_ignore_gate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Use only synthetic bytes, never decode/read HYP-0005 market quote content."""
    local_path = "test_only_source.json"
    data = b"synthetic-file-no-quotes"
    source_file = tmp_path / local_path
    source_file.write_bytes(data)
    checksum = hashlib.sha256(data).hexdigest()
    provenance = "reports/local_ci/HYP0005_2026_09_SOURCE_INTAKE_PROVENANCE.json"
    ignore = tmp_path / ".gitignore"
    ignore.write_text(provenance + "\n", encoding="utf-8")
    evidence = tmp_path / "evidence.md"
    evidence.write_text(
        "USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER\n" + local_path + " " + checksum,
        encoding="utf-8",
    )
    monkeypatch.setattr(check, "ROOT", tmp_path)
    monkeypatch.setattr(check, "RF033_GITIGNORE", ignore)
    monkeypatch.setattr(check, "RF033_INTAKE_EVIDENCE", evidence)
    monkeypatch.setattr(check, "RF033_EXPECTED_LOCAL_FILES", {local_path: (len(data), checksum)})
    monkeypatch.setattr(check, "git_output", lambda *args: provenance)
    check.check_local_source_intake_identity()
    source_file.write_bytes(data + b"x")
    with pytest.raises(check.TaskCheckError, match="local source byte-size drift"):
        check.check_local_source_intake_identity()


def test_rf033_rejects_unignored_provenance(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    evidence = tmp_path / "evidence.md"
    evidence.write_text(
        "USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER",
        encoding="utf-8",
    )
    ignore = tmp_path / ".gitignore"
    ignore.write_text("# unrelated\n", encoding="utf-8")
    monkeypatch.setattr(check, "RF033_INTAKE_EVIDENCE", evidence)
    monkeypatch.setattr(check, "RF033_GITIGNORE", ignore)
    with pytest.raises(check.TaskCheckError, match="narrow local provenance"):
        check.check_local_source_intake_identity()


def test_rf034_one_shot_refuses_any_existing_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths = {
        "RF034_RESULT_JSON": tmp_path / "result.json",
        "RF034_RESULT_TEXT": tmp_path / "report.txt",
        "RF034_DERIVED_CSV": tmp_path / "derived.csv",
        "RF034_DERIVED_PART": tmp_path / "derived.csv.part",
    }
    for key, path in paths.items():
        monkeypatch.setattr(check, key, path)
    for path in paths.values():
        path.write_bytes(b"synthetic-existing-output")
        with pytest.raises(check.TaskCheckError, match="no rerun"):
            check.check_rf034_output_absence()
        path.unlink()
    check.check_rf034_output_absence()


def test_rf034_offline_source_hashes_accept_only_frozen_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "raw"
    root.mkdir()
    fixture = root / "2003/05/BID_candles_hour_1.json"
    fixture.parent.mkdir(parents=True)
    raw = b"synthetic-raw-file-metadata-only"
    fixture.write_bytes(raw)
    protocol = tmp_path / "protocol.md"
    protocol.write_text("synthetic", encoding="utf-8")
    monkeypatch.setattr(check, "RF023_SNAPSHOT_ROOT", root)
    monkeypatch.setattr(check, "RF034_PREPARATION_PROTOCOL", protocol)
    monkeypatch.setattr(
        check,
        "RF034_SOURCE_HASHES",
        {"2003/05/BID_candles_hour_1.json": (len(raw), hashlib.sha256(raw).hexdigest())},
    )
    check.check_rf034_frozen_source_hashes()
    fixture.write_bytes(raw + b"x")
    with pytest.raises(check.TaskCheckError, match="source size mismatch"):
        check.check_rf034_frozen_source_hashes()


def test_rf034_result_identity_uses_only_synthetic_geometry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import json

    csv_path = tmp_path / "rows.csv"
    csv_path.write_text(",".join(check.RF034_EXPECTED_CSV_FIELDS) + "\n", encoding="utf-8")
    csv_hash = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    json_path = tmp_path / "result.json"
    text_path = tmp_path / "report.txt"
    result = {
        "schema_version": "hyp0005-data-feasibility-prep-1",
        "task_id": "ATS2-RF-023",
        "hypothesis_id": "HYP-0005",
        "git_commit": "SYNTHETIC_COMMIT",
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
        "segments": [
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
        ],
        "source_files": [
            {
                "relative_path": "data/external/dukascopy/EURUSD/H1/" + relative,
                "sha256": digest,
                "source_format": "JETTA_JSON",
                "source_url": "LOCAL_FROZEN_COPY",
            }
            for relative, (_, digest) in check.RF034_SOURCE_HASHES.items()
        ],
        "derived_csv_sha256": csv_hash,
        "derived_row_count": 1,
        "geometry": {
            "eligible_rows_by_segment": {"LEFT_UNSEEN": 1, "RIGHT_UNSEEN": 1},
            "eligible_rows_by_bucket": {"CORE_ACTIVE": 1, "OFF_HOURS": 1},
            "expected_market_hours_by_segment": {"LEFT_UNSEEN": 2, "RIGHT_UNSEEN": 2},
            "missing_market_hours_by_segment": {"LEFT_UNSEEN": 0, "RIGHT_UNSEEN": 0},
        },
        "preparation_decision": "READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE",
    }
    json_path.write_text(json.dumps(result), encoding="utf-8")
    text_path.write_text(
        "Decision: READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE\n"
        "Outcome metrics computed: False\n"
        "Primary claim evaluated: False\n"
        "Information boundary: NO_CONFIRMATORY_OUTCOME_COMPUTED\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(check, "RF034_RESULT_JSON", json_path)
    monkeypatch.setattr(check, "RF034_RESULT_TEXT", text_path)
    monkeypatch.setattr(check, "RF034_DERIVED_CSV", csv_path)
    check.check_rf023_preparation_result("SYNTHETIC_COMMIT")
    result["primary_claim_evaluated"] = True
    json_path.write_text(json.dumps(result), encoding="utf-8")
    with pytest.raises(check.TaskCheckError, match="primary_claim_evaluated"):
        check.check_rf023_preparation_result("SYNTHETIC_COMMIT")


def test_rf024_manifest_loads_with_prepared_identity_only() -> None:
    """Only committed schema/manifest metadata is inspected; no quote rows."""
    from ats.schemas.dataset_manifest import load_dataset_manifest

    manifest = load_dataset_manifest(check.RF024_MANIFEST)
    assert manifest.dataset_id == "DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001"
    assert manifest.dataset_version == "1.0.0"
    assert manifest.integrity.digest == check.RF024_CSV_SHA256
    assert check.RF024_SOURCE_BUNDLE_SHA256 in manifest.source.snapshot_reference
    assert check.RF024_RF023_JSON_SHA256 in manifest.source.snapshot_reference
    assert "USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER" in (
        manifest.source.source_reference
    )
    assert manifest.ordering.keys == ("event_time",)
    assert manifest.ordering.tie_break_keys == ("sequence",)
    assert manifest.quality_policy.missing == "ALLOW_DECLARED_GAPS"


def test_rf024_review_and_schema_are_pre_outcome_metadata() -> None:
    import json

    review = check.RF024_REVIEW.read_text(encoding="utf-8")
    schema = json.loads(check.RF024_SCHEMA.read_text(encoding="utf-8"))
    assert "Review decision: `CONDITIONAL`" in review
    assert "STAGED_PENDING_EXACT_MAIN_PASS" in review
    assert "NO_CONFIRMATORY_OUTCOME_COMPUTED" in review
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(check.RF034_EXPECTED_CSV_FIELDS)
    assert set(schema["properties"]) == set(check.RF034_EXPECTED_CSV_FIELDS)
    assert "relative_spread" not in schema["properties"]
    assert "abs_next_1h_return" not in schema["properties"]


def test_rf035_runner_freeze_rejects_existing_synthetic_reveal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "synthetic-first-reveal.json"
    output.write_bytes(b"synthetic-never-a-market-result")
    monkeypatch.setattr(check, "RF035_PROTO_RECORD", tmp_path / "record.md")
    monkeypatch.setattr(check, "RF035_RUNNER", tmp_path / "runner.py")
    monkeypatch.setattr(check, "RF035_RUNNER_TEST", tmp_path / "test_runner.py")
    monkeypatch.setattr(check, "RF035_RESULT_JSON", output)
    monkeypatch.setattr(check, "RF035_RESULT_TEXT", tmp_path / "absent-result.txt")
    for name in ("record.md", "runner.py", "test_runner.py"):
        (tmp_path / name).write_text("synthetic", encoding="utf-8")
    with pytest.raises(check.TaskCheckError, match="unexpected HYP-0005 confirmatory first reveal"):
        check.check_rf035_pre_reveal_runner_freeze()


def test_rf036_preparation_blocks_any_existing_synthetic_reveal_artifact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Never read or calculate prices: reject each reserved output path."""
    result = tmp_path / "synthetic-result.json"
    report = tmp_path / "synthetic-result.txt"
    sentinel = tmp_path / "synthetic-consumed.json"
    monkeypatch.setattr(check, "RF035_RESULT_JSON", result)
    monkeypatch.setattr(check, "RF035_RESULT_TEXT", report)
    monkeypatch.setattr(check, "RF036_CONSUMED_SENTINEL", sentinel)
    # Real protocol/state are public prereveal metadata; no protected CSV is read.
    check.check_rf036_gate_preparation()
    for path in (result, report, sentinel):
        path.write_bytes(b"synthetic-never-market-outcome")
        with pytest.raises(check.TaskCheckError, match="reveal output exists"):
            check.check_rf036_gate_preparation()
        path.unlink()
    check.check_rf036_gate_preparation()


def test_rf037_preserves_rf036_gate_and_immutable_runner_blob() -> None:
    main_source = inspect.getsource(check.main)
    assert "check_rf036_gate_preparation(require_absence=False)" in main_source
    assert "run_first_reveal_once(" not in main_source
    assert "--execute-first-reveal" not in main_source
    assert "observations_from_keys(" not in main_source
    assert "evaluate_synthetic_or_revealed(" not in main_source
    assert check.RF036_GATE_DOC.name == "HYP-0005-PROTOTYPE-01-REVEAL-GATE.md"
    assert check.RF035_RUNNER_BLOB == "814193997768605fe60607d66dfd755a9323f339"
