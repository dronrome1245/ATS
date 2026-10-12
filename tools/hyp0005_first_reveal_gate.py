#!/usr/bin/env python3
"""RF-037 exact-main HYP-0005 one-shot confirmatory reveal gate.

No direct CLI launch. The first market-outcome call is guarded by an
exclusive, durable consumed marker. Existing complete results are only
checked against their preserved SHA-256 receipt, never recomputed.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTHORIZATION = "OWNER_AUTHORIZED_HYP0005_FIRST_REVEAL_ONCE_2026_10_12"
RF036_MAIN_COMMIT = "1facc2604e701cc05b34118e8c3295070bfd9eaa"
RUNNER_BLOB = "814193997768605fe60607d66dfd755a9323f339"
CSV_SHA256 = "b1091c4975665b2b0cd4f58627a10aceaab7aeff5076431abb6abc74c0a054c1"
SOURCE_SHA256 = "65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2"
PREP_SHA256 = "d2eadd9a64da74ae79e2a0008426147953f24beb8c23f66557a721a7b8a65381"
DATASET_ID = "DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001"
RESULT_JSON = ROOT / "reports/local_ci/HYP0005_PROTO01_RESULT.json"
RESULT_TEXT = ROOT / "reports/local_ci/HYP0005_PROTO01_RESULT_REPORT.txt"
CONSUMED = ROOT / "reports/local_ci/HYP0005_PROTO01_FIRST_REVEAL_CONSUMED.json"
RECEIPT = ROOT / "reports/local_ci/HYP0005_PROTO01_FIRST_REVEAL_RECEIPT.json"
RUNNER_RELATIVE = "tools/hyp0005_proto01.py"

EXPECTED_GEOMETRY = {
    "eligible_exact_next_hour_count": 1991,
    "eligible_rows_by_bucket": {
        "CORE_ACTIVE": 838,
        "OFF_HOURS": 837,
        "TRANSITION": 316,
    },
    "eligible_rows_by_segment": {"LEFT_UNSEEN": 1542, "RIGHT_UNSEEN": 449},
    "expected_market_hours_by_segment": {"LEFT_UNSEEN": 1560, "RIGHT_UNSEEN": 453},
    "missing_market_hours_by_segment": {"LEFT_UNSEEN": 3, "RIGHT_UNSEEN": 0},
    "total_rows_by_bucket": {"CORE_ACTIVE": 839, "OFF_HOURS": 837, "TRANSITION": 334},
    "total_rows_by_segment": {"LEFT_UNSEEN": 1557, "RIGHT_UNSEEN": 453},
    "ineligible_closed_market_next_hour_count": 16,
    "ineligible_missing_expected_next_hour_count": 3,
    "ineligible_segment_end_count": 0,
}


class FirstRevealGateError(RuntimeError):
    """Technical gate failure; not a negative HYP-0005 market result."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FirstRevealGateError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    ).stdout.strip()


def _check_exact_main(expected_commit: str) -> None:
    require(_git("branch", "--show-current") == "main", "first reveal only on main")
    require(_git("rev-parse", "HEAD") == expected_commit, "exact main HEAD mismatch")
    require(_git("rev-parse", "origin/main") == expected_commit, "origin/main drift")
    require(
        not _git("status", "--porcelain=v1", "-uall"),
        "non-clean first reveal worktree",
    )
    require(
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", RF036_MAIN_COMMIT, expected_commit],
            cwd=ROOT,
            check=False,
        ).returncode
        == 0,
        "RF-036 frozen gate not an ancestor",
    )
    require(
        _git("rev-parse", f"HEAD:{RUNNER_RELATIVE}") == RUNNER_BLOB,
        "runner HEAD drift",
    )
    require(
        _git("hash-object", "--", RUNNER_RELATIVE) == RUNNER_BLOB,
        "runner worktree drift",
    )
    for path in (RESULT_JSON, RESULT_TEXT, CONSUMED, RECEIPT):
        relative = path.relative_to(ROOT).as_posix()
        require(
            subprocess.run(
                ["git", "check-ignore", "--quiet", "--", relative],
                cwd=ROOT,
                check=False,
            ).returncode
            == 0,
            f"one-shot artifact must be git-ignored: {relative}",
        )


def _verify_frozen_input_hashes() -> None:
    """No quote-value interpretation before consuming authorization."""
    from tools import hyp0005_proto01 as frozen_runner

    frozen_runner.verify_frozen_files()


def _invoke_frozen_runner() -> dict[str, Any]:
    """Exactly one market outcome invocation; tests replace this with a synthetic stub."""
    from tools import hyp0005_proto01 as frozen_runner

    return frozen_runner.run_first_reveal_once(authorized=True)


def _write_new_json(path: Path, record: dict[str, Any]) -> None:
    """Exclusive creation + durable flush. Never replace any one-shot artifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(record, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def _check_new_result(result: dict[str, Any], expected_commit: str) -> tuple[str, bool]:
    """Check immutable output contract, not a new price calculation or revised rule."""
    require(
        RESULT_JSON.is_file() and RESULT_TEXT.is_file(),
        "incomplete frozen result pair",
    )
    saved = json.loads(RESULT_JSON.read_text(encoding="utf-8"))
    require(
        isinstance(saved, dict) and saved == result, "saved output differs from runner"
    )
    for key, expected in {
        "schema_version": "hyp0005-confirmatory-proto01-result-1",
        "hypothesis_id": "HYP-0005",
        "parent_idea_id": "IDEA-0004",
        "prototype_id": "PROTO-01",
        "evidence_class": "CONFIRMATORY_STRUCTURAL_NOT_INDEPENDENT_EXAM",
        "measurement_label": "H1_OPEN_PROXY_STRUCTURAL_NO_TRADING_PNL",
        "outcome_metrics_computed": True,
        "primary_claim_evaluated": True,
    }.items():
        require(saved.get(key) == expected, f"frozen result identity mismatch: {key}")
    require(saved.get("geometry") == EXPECTED_GEOMETRY, "revealed geometry drift")
    require(
        saved.get("run_context", {}).get("git_commit") == expected_commit,
        "reveal commit drift",
    )
    dataset = saved.get("dataset")
    require(isinstance(dataset, dict), "missing result dataset")
    for key, expected in {
        "dataset_id": DATASET_ID,
        "dataset_version": "1.0.0",
        "derived_csv_sha256": CSV_SHA256,
        "source_bundle_sha256": SOURCE_SHA256,
        "boundary_availability_mode": "H1_OPEN_PROXY_AT_EVENT_TIME",
        "exact_tick_boundary_time_known": False,
        "confirmatory_preparation_sha256": PREP_SHA256,
    }.items():
        require(dataset.get(key) == expected, f"frozen result dataset drift: {key}")

    primary = saved.get("primary")
    require(isinstance(primary, dict), "missing result primary fields")
    movement = primary.get("movement_inequality_pass")
    spread = primary.get("spread_inequality_pass")
    both = primary.get("both_primary_inequalities_pass")
    require(
        type(movement) is bool and type(spread) is bool and type(both) is bool,
        "malformed primary decision flags",
    )
    require(both == (movement and spread), "inconsistent primary decision flags")
    buckets = saved.get("bucket_metrics")
    require(isinstance(buckets, dict), "missing bucket statistics")
    require(
        set(buckets) == {"CORE_ACTIVE", "OFF_HOURS", "TRANSITION"},
        "unexpected buckets",
    )
    for bucket, expected in EXPECTED_GEOMETRY["eligible_rows_by_bucket"].items():
        metrics = buckets[bucket]
        require(isinstance(metrics, dict), f"missing bucket metrics: {bucket}")
        require(
            metrics.get("observation_count") == expected,
            f"bucket count drift: {bucket}",
        )
        for name in (
            "mean_abs_next_1h_return",
            "median_abs_next_1h_return",
            "median_relative_spread",
        ):
            value = metrics.get(name)
            require(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and math.isfinite(value),
                f"invalid result metric: {bucket}/{name}",
            )
    core = buckets["CORE_ACTIVE"]
    off = buckets["OFF_HOURS"]
    require(
        movement
        == (core["median_abs_next_1h_return"] > off["median_abs_next_1h_return"]),
        "movement decision inconsistent with stored medians",
    )
    require(
        spread == (core["median_relative_spread"] <= off["median_relative_spread"]),
        "spread decision inconsistent with stored medians",
    )
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
    require(saved.get("decision") == decision, "frozen decision route drift")
    require(saved.get("decision_reason") == reason, "frozen reason route drift")
    require(saved.get("next_action") == action, "frozen next action route drift")
    require(
        isinstance(saved.get("calendar_year_diagnostics"), dict),
        "missing year diagnostics",
    )
    summary = RESULT_TEXT.read_text(encoding="utf-8")
    for marker in (
        "HYP-0005 CONFIRMATORY STRUCTURAL PROTO-01 REVEAL",
        f"Git commit: {expected_commit}",
        f"Decision: {decision}",
        f"Reason: {reason}",
        f"Next action: {action}",
        f"Both predeclared inequalities pass: {both}",
        "No directional trading strategy, economic proof, or independent examination",
    ):
        require(marker in summary, f"frozen result text missing marker: {marker}")
    return decision, both


def _validate_saved_receipt(expected_commit: str) -> dict[str, Any]:
    """Already revealed: compare saved file hashes only; NEVER invoke runner again."""
    require(
        CONSUMED.is_file() and RECEIPT.is_file(), "consumed marker/receipt incomplete"
    )
    require(
        RESULT_JSON.is_file() and RESULT_TEXT.is_file(), "saved result pair incomplete"
    )
    consumed = json.loads(CONSUMED.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    require(
        isinstance(consumed, dict) and isinstance(receipt, dict),
        "invalid saved gate receipt",
    )
    for document in (consumed, receipt):
        require(
            document.get("authorization") == AUTHORIZATION,
            "wrong one-shot authorization",
        )
        require(
            document.get("git_commit") == expected_commit, "wrong saved reveal commit"
        )
        require(
            document.get("runner_git_blob") == RUNNER_BLOB,
            "wrong saved runner identity",
        )
        require(
            document.get("dataset_csv_sha256") == CSV_SHA256,
            "wrong saved dataset identity",
        )
    require(
        consumed.get("state") == "CONSUMED_BEFORE_OUTCOME", "invalid consumed state"
    )
    require(
        receipt.get("status") == "FIRST_REVEAL_COMPLETED_ONCE",
        "invalid receipt status",
    )
    require(
        sha256_file(RESULT_JSON) == receipt.get("result_json_sha256"),
        "preserved result JSON SHA-256 mismatch",
    )
    require(
        sha256_file(RESULT_TEXT) == receipt.get("report_text_sha256"),
        "preserved result report SHA-256 mismatch",
    )
    return receipt


def execute_or_verify_once(
    *, expected_commit: str, authorized: bool = False
) -> dict[str, Any]:
    """One irreversible first reveal on approved exact main; hash-only on later calls."""
    require(authorized is True, "explicit OWNER first reveal authorization is required")
    _check_exact_main(expected_commit)
    _verify_frozen_input_hashes()

    if CONSUMED.exists():
        return _validate_saved_receipt(expected_commit)
    require(
        not RESULT_JSON.exists() and not RESULT_TEXT.exists() and not RECEIPT.exists(),
        "first reveal artifact already present without consumed marker; no rerun",
    )
    _write_new_json(
        CONSUMED,
        {
            "schema_version": "hyp0005-first-reveal-consumed-1",
            "task_id": "ATS2-RF-037",
            "authorization": AUTHORIZATION,
            "git_commit": expected_commit,
            "runner_git_blob": RUNNER_BLOB,
            "dataset_csv_sha256": CSV_SHA256,
            "state": "CONSUMED_BEFORE_OUTCOME",
            "consumed_at": datetime.now(UTC).isoformat(),
        },
    )
    try:
        result = _invoke_frozen_runner()
        decision, both = _check_new_result(result, expected_commit)
        receipt = {
            "schema_version": "hyp0005-first-reveal-receipt-1",
            "task_id": "ATS2-RF-037",
            "status": "FIRST_REVEAL_COMPLETED_ONCE",
            "authorization": AUTHORIZATION,
            "git_commit": expected_commit,
            "runner_git_blob": RUNNER_BLOB,
            "dataset_csv_sha256": CSV_SHA256,
            "source_bundle_sha256": SOURCE_SHA256,
            "result_json_sha256": sha256_file(RESULT_JSON),
            "report_text_sha256": sha256_file(RESULT_TEXT),
            "decision": decision,
            "both_primary_inequalities_pass": both,
            "completed_at": datetime.now(UTC).isoformat(),
        }
        _write_new_json(RECEIPT, receipt)
        return receipt
    except Exception as exc:
        raise FirstRevealGateError(
            "first reveal authorization CONSUMED; technical blocker after consumed marker. "
            "Preserve every artifact and report failure. No automatic retry or retuning."
        ) from exc


def main() -> int:
    """Standalone invocation is prohibited; OWNER exact-main task gate is required."""
    print("RF-037 DIRECT EXECUTION BLOCKED: run only through ATS_TASK_CHECK.bat")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
