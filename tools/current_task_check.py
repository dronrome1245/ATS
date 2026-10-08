#!/usr/bin/env python3
"""RF-030: execute or validate the one-shot HYP-0006 PROTO-01 first reveal."""

from __future__ import annotations

import hashlib
import json
import math
import statistics
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-030"
TASK_NAME = "HYP-0006 PROTO-01 first development reveal"

RF027_RESULT = ROOT / "reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP.json"
RF028_RESULT = ROOT / "reports/local_ci/HYP0006_DATA_TOLERANCE_FREEZE.json"
GEOMETRY_CSV = ROOT / "data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv"
REVEAL_GATE = ROOT / "research/reviews/HYP-0006-PROTOTYPE-01-REVEAL-GATE.md"
PROTOTYPE_REVIEW = ROOT / "research/reviews/HYP-0006-PROTOTYPE-01.md"
PROTOTYPE_RUNNER = ROOT / "tools/hyp0006_proto01.py"
REVEAL_JSON = ROOT / "reports/local_ci/HYP0006_PROTO01_RESULT.json"
REVEAL_TEXT = ROOT / "reports/local_ci/HYP0006_PROTO01_RESULT_REPORT.txt"

RF027_COMMIT = "bbbdbd301b610dfc61316c9ff82015fb0e039a47"
RF028_COMMIT = "e7f05a0d237c4d78a8a0edb93710619e6ad2ba00"
RF029_COMMIT = "94df9ede91522f473872b25a6d8023fd64182878"
RF028_JSON_SHA256 = "1b575682b959070f4a0981b7cd13d70626f1e169d221d0c9fb2383fc679fd5fb"
FROZEN_GEOMETRY_SHA256 = "e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034"
FROZEN_SOURCE_SHA256 = "5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425"
FROZEN_RUNNER_GIT_BLOB = "6afb870c035bc5ae76f773784a5fa3db15d680fd"
EXPECTED_TICK_OBJECTS = 1085
EXPECTED_CANDIDATE_EVENTS = 217
EXPECTED_ELIGIBLE_EVENTS = 216
FROZEN_INELIGIBLE_ID = "BLS-CPI-20030815"

FROZEN_BLOBS = {
    "research/hypotheses/HYP-0005.md": "ebbbc89187c911485c1568dc11f5f2f9e703718a",
    "research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md": (
        "c15b2b67700dd46fc592f1208731ce6b42f6905c"
    ),
    "tools/hyp0005_data_feasibility.py": "310b23213876304ade674ef36ba17ce6d457353f",
    "tests/test_hyp0005_data_feasibility.py": "12697882da682eab699bf5b7debd7c358e56aca9",
    "research/hypotheses/HYP-0006.md": "6b3f260ceacd98adf7a6aa44205404e68e4fd4ca",
    "research/reviews/HYP-0006-DATA-FEASIBILITY.md": ("ae58099a05daec4be385c18177c74f1f22d1eb30"),
    "research/reviews/HYP-0006-DATA-TOLERANCE-FREEZE.md": (
        "0a16479ae606487c92073e32cf5d324ca9483265"
    ),
    "tools/hyp0006_data_tolerance_freeze.py": "e2b0a71ec658ba5eacf29c2733410d230f4c5f2c",
    "tests/test_hyp0006_data_tolerance_freeze.py": ("9cd465d4970e74c2ff565fb5643554e4cd209c4b"),
    "research/reviews/HYP-0006-PROTOTYPE-01.md": ("9f7bcd8480f66a37ea273cc7e158a56758b79b12"),
    "tests/test_hyp0006_proto01.py": "0858e2fc153df23996cf56914f453ebfe1b9fddf",
}


class TaskCheckError(RuntimeError):
    """A technical gate failed; this is never a negative HYP-0006 result."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TaskCheckError(message)


def git_output(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path, label: str) -> dict[str, Any]:
    require(path.is_file(), f"{label} missing: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TaskCheckError(f"{label} malformed: {exc}") from exc
    require(isinstance(value, dict), f"{label} must be a JSON mapping")
    return value


def require_values(result: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    for key, value in expected.items():
        require(result.get(key) == value, f"{label} mismatch: {key}")


def has_markers(path: Path, markers: tuple[str, ...]) -> None:
    require(path.is_file(), f"required RF-030 artifact missing: {path}")
    content = path.read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in content]
    require(not missing, f"missing marker in {path}: {missing[0] if missing else ''}")


def check_exact_main() -> str:
    print("\n== Exact-main and clean-tree gate ==", flush=True)
    branch = git_output("branch", "--show-current")
    head = git_output("rev-parse", "HEAD")
    origin_main = git_output("rev-parse", "origin/main")
    status = git_output("status", "--porcelain=v1", "-uall")
    require(branch == "main", f"reveal requires branch main, found {branch!r}")
    require(head == origin_main, f"HEAD {head} does not equal origin/main {origin_main}")
    require(not status, "working tree must be clean before reveal")
    print(f"[PASS] main exact commit: {head}", flush=True)
    print("[PASS] working tree clean", flush=True)
    return head


def check_runner_blob() -> None:
    print("\n== Frozen runner Git blob ==", flush=True)
    relative = PROTOTYPE_RUNNER.relative_to(ROOT).as_posix()
    committed = git_output("rev-parse", f"HEAD:{relative}")
    worktree = git_output("hash-object", "--", relative)
    require(committed == FROZEN_RUNNER_GIT_BLOB, "committed prototype runner blob changed")
    require(worktree == FROZEN_RUNNER_GIT_BLOB, "worktree prototype runner bytes changed")
    print(f"[PASS] frozen runner blob: {FROZEN_RUNNER_GIT_BLOB}", flush=True)


def check_frozen_lineage() -> None:
    print("\n== Frozen HYP-0005 / HYP-0006 lineage ==", flush=True)
    for relative, expected in FROZEN_BLOBS.items():
        require(
            git_output("rev-parse", f"HEAD:{relative}") == expected,
            f"protected lineage changed: {relative}",
        )
        print(f"[PASS] unchanged: {relative}", flush=True)


def check_reveal_contract() -> None:
    print("\n== RF-030 first-reveal contract ==", flush=True)
    has_markers(
        REVEAL_GATE,
        (
            "ATS2-RF-030",
            "17/22",
            RF029_COMMIT,
            RF028_JSON_SHA256,
            FROZEN_RUNNER_GIT_BLOB,
            "1085",
            "216",
            "BLS-CPI-20030815",
            "--execute-first-reveal",
            "DEVELOPMENT_REVEALED_EXPLORATORY_ONLY",
        ),
    )
    has_markers(
        PROTOTYPE_REVIEW,
        (
            "ATS2-RF-029",
            "216 + 1 = 217",
            RF028_JSON_SHA256,
            FROZEN_RUNNER_GIT_BLOB,
            "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
        ),
    )
    print("[PASS] RF-029 freeze and RF-030 reveal gate present", flush=True)


def load_frozen_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    print("\n== RF-027 / RF-028 frozen identities and denominator ==", flush=True)
    require(RF028_RESULT.is_file(), "exact RF-028 JSON missing")
    require(sha256_file(RF028_RESULT) == RF028_JSON_SHA256, "RF-028 JSON SHA-256 changed")
    require(GEOMETRY_CSV.is_file(), "frozen RF-027 geometry CSV missing")
    require(
        sha256_file(GEOMETRY_CSV) == FROZEN_GEOMETRY_SHA256,
        "frozen RF-027 geometry SHA-256 changed",
    )
    rf028 = load_json(RF028_RESULT, "RF-028 result")
    require_values(
        rf028,
        {
            "task_id": "ATS2-RF-028",
            "hypothesis_id": "HYP-0006",
            "git_commit": RF028_COMMIT,
            "rf027_git_commit": RF027_COMMIT,
            "dataset_id": "DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001",
            "dataset_version": "1.0.0",
            "candidate_event_count": EXPECTED_CANDIDATE_EVENTS,
            "eligible_event_count": EXPECTED_ELIGIBLE_EVENTS,
            "ineligible_event_count": 1,
            "source_bundle_sha256": FROZEN_SOURCE_SHA256,
            "geometry_csv_sha256": FROZEN_GEOMETRY_SHA256,
            "boundary_max_abs_gap_ms": 30000,
            "pre_release_max_staleness_ms": 30000,
            "boundary_tie_break": "PREVIOUS_ON_EQUAL_GAP",
            "pre_release_rule": "LAST_QUOTE_STRICTLY_BEFORE_RELEASE",
            "duplicate_timestamp_tie_break": "LAST_RAW_RECORD_AT_SELECTED_MILLISECOND",
            "price_pairing_rule": "BID_AND_ASK_FROM_SAME_RAW_TICK_RECORD",
            "freeze_decision": "FREEZE_DATA_AND_TOLERANCES",
            "outcome_metrics_computed": False,
            "primary_claim_evaluated": False,
            "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        },
        "RF-028 result",
    )
    eligible = rf028.get("eligible_event_ids")
    evaluations = rf028.get("geometry_evaluations")
    require(isinstance(eligible, list), "RF-028 eligible ID list missing")
    require(len(eligible) == EXPECTED_ELIGIBLE_EVENTS, "RF-028 eligible ID count changed")
    require(len(set(eligible)) == EXPECTED_ELIGIBLE_EVENTS, "RF-028 eligible IDs duplicate")
    require(
        rf028.get("ineligible_events")
        == [
            {
                "event_id": FROZEN_INELIGIBLE_ID,
                "exclusion_reasons": ["POST_60_ANCHOR_GAP_EXCEEDS_30000MS"],
            }
        ],
        "RF-028 sole exclusion changed",
    )
    require(
        isinstance(evaluations, list) and len(evaluations) == EXPECTED_CANDIDATE_EVENTS,
        "RF-028 geometry evaluation denominator changed",
    )

    rf027 = load_json(RF027_RESULT, "RF-027 result")
    require_values(
        rf027,
        {
            "task_id": "ATS2-RF-027",
            "hypothesis_id": "HYP-0006",
            "git_commit": RF027_COMMIT,
            "candidate_event_count": EXPECTED_CANDIDATE_EVENTS,
            "acquired_tick_object_count": EXPECTED_TICK_OBJECTS,
            "missing_tick_object_count": 0,
            "protected_hyp0005_source_requests": 0,
            "source_bundle_sha256": FROZEN_SOURCE_SHA256,
            "geometry_csv_sha256": FROZEN_GEOMETRY_SHA256,
            "outcome_metrics_computed": False,
            "primary_claim_evaluated": False,
            "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        },
        "RF-027 result",
    )
    events = rf027.get("events")
    tick_objects = rf027.get("tick_objects")
    require(isinstance(events, list) and len(events) == 217, "RF-027 event denominator changed")
    require(
        isinstance(tick_objects, list) and len(tick_objects) == 1085,
        "RF-027 BI5 identity denominator changed",
    )
    event_ids = [item.get("event_id") for item in events if isinstance(item, dict)]
    require(len(event_ids) == 217 and len(set(event_ids)) == 217, "RF-027 event IDs invalid")
    require(
        set(event_ids) == set(eligible) | {FROZEN_INELIGIBLE_ID},
        "RF-027 and RF-028 event lineages disagree",
    )
    print("[PASS] RF-028 raw JSON SHA-256", flush=True)
    print("[PASS] 217 candidates / 216 eligible / sole BLS-CPI-20030815 exclusion", flush=True)
    print("[PASS] protected HYP-0005 source requests: 0", flush=True)
    return rf027, rf028


def reveal_artifact_state(
    json_path: Path | None = None,
    text_path: Path | None = None,
) -> str:
    json_path = REVEAL_JSON if json_path is None else json_path
    text_path = REVEAL_TEXT if text_path is None else text_path
    json_exists = json_path.is_file()
    text_exists = text_path.is_file()
    if json_exists and text_exists:
        return "EXISTING_PAIR"
    if json_exists or text_exists:
        raise TaskCheckError("partial reveal artifacts present; preserve and stop without rerun")
    return "ABSENT"


def verify_all_bi5_objects(
    tick_objects: list[dict[str, Any]],
    *,
    root: Path | None = None,
    expected_count: int = EXPECTED_TICK_OBJECTS,
) -> None:
    print("\n== Full frozen Dukascopy BI5 availability and SHA-256 ==", flush=True)
    root = ROOT if root is None else root
    raw_root = root / "data/raw/dukascopy/hyp0006/EURUSD"
    require(len(tick_objects) == expected_count, "frozen BI5 identity count changed")
    seen_hours: set[str] = set()
    seen_paths: set[str] = set()
    for index, identity in enumerate(tick_objects, start=1):
        require(isinstance(identity, dict), f"BI5 identity {index} is malformed")
        relative = identity.get("relative_path")
        hour_start = identity.get("hour_start")
        expected_hash = identity.get("sha256")
        require(isinstance(relative, str), f"BI5 identity {index} path missing")
        require(isinstance(hour_start, str), f"BI5 identity {index} hour missing")
        require(
            isinstance(expected_hash, str)
            and len(expected_hash) == 64
            and all(char in "0123456789abcdef" for char in expected_hash),
            f"BI5 identity {index} SHA-256 malformed",
        )
        relative_path = Path(relative)
        require(not relative_path.is_absolute(), f"absolute BI5 path forbidden: {relative}")
        require(".." not in relative_path.parts, f"parent traversal in BI5 path: {relative}")
        path = root / relative_path
        require(path.is_file(), f"frozen BI5 absent: {relative}")
        try:
            path.resolve(strict=True).relative_to(raw_root.resolve(strict=True))
        except (OSError, ValueError) as exc:
            raise TaskCheckError(f"BI5 path outside frozen root: {relative}") from exc
        require(relative not in seen_paths, f"duplicate frozen BI5 path: {relative}")
        require(hour_start not in seen_hours, f"duplicate frozen BI5 hour: {hour_start}")
        require(sha256_file(path) == expected_hash, f"frozen BI5 SHA-256 mismatch: {relative}")
        seen_paths.add(relative)
        seen_hours.add(hour_start)
    print(
        f"[PASS] all {expected_count} frozen local BI5 objects present and SHA-256 exact",
        flush=True,
    )


def finite_nonnegative(value: Any, label: str) -> float:
    require(
        isinstance(value, (int, float)) and not isinstance(value, bool),
        f"{label} must be numeric",
    )
    number = float(value)
    require(math.isfinite(number) and number >= 0.0, f"{label} must be finite and nonnegative")
    return number


def result_year(value: Any) -> int:
    require(isinstance(value, str), "reveal observation timestamp missing")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise TaskCheckError(f"invalid reveal timestamp: {value}") from exc
    require(parsed.tzinfo is not None and parsed.utcoffset() is not None, "naive reveal timestamp")
    return parsed.astimezone(UTC).year


def validate_reveal_payload(
    result: dict[str, Any],
    rf027: dict[str, Any],
    rf028: dict[str, Any],
    exact_commit: str,
) -> None:
    require_values(
        result,
        {
            "schema_version": "hyp0006-proto01-reveal-1",
            "hypothesis_id": "HYP-0006",
            "prototype_id": "PROTO-01",
            "git_commit": exact_commit,
            "rf028_git_commit": RF028_COMMIT,
            "rf028_json_sha256": RF028_JSON_SHA256,
            "dataset_id": "DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001",
            "dataset_version": "1.0.0",
            "source_bundle_sha256": FROZEN_SOURCE_SHA256,
            "geometry_csv_sha256": FROZEN_GEOMETRY_SHA256,
            "evidence_classification": "DEVELOPMENT_EXPLORATORY_ONLY",
            "candidate_event_count": 217,
            "eligible_event_count": 216,
            "ineligible_event_count": 1,
            "ineligible_event_ids": [FROZEN_INELIGIBLE_ID],
            "outcome_metrics_computed": True,
            "primary_claim_evaluated": True,
            "information_boundary": "DEVELOPMENT_REVEALED_EXPLORATORY_ONLY",
        },
        "HYP-0006 reveal result",
    )
    observations = result.get("event_observations")
    eligible_ids = rf028.get("eligible_event_ids")
    require(
        isinstance(observations, list) and len(observations) == 216, "216 observations required"
    )
    require(isinstance(eligible_ids, list), "RF-028 eligible list missing")
    observed_ids = [item.get("event_id") for item in observations if isinstance(item, dict)]
    require(observed_ids == eligible_ids, "reveal event IDs/order differ from frozen RF-028 list")
    require(len(set(observed_ids)) == 216, "reveal event IDs duplicate")

    source_events = {item["event_id"]: item for item in rf027["events"] if isinstance(item, dict)}
    pre_values: list[float] = []
    post_values: list[float] = []
    pre_spreads: list[float] = []
    first_post_spreads: list[float] = []
    year_groups: dict[int, list[dict[str, Any]]] = {}
    same_time_count = 0
    for observation in observations:
        require(isinstance(observation, dict), "reveal observation malformed")
        event_id = observation["event_id"]
        source = source_events.get(event_id)
        require(source is not None, f"reveal event missing from RF-027: {event_id}")
        require(
            observation.get("release_time_utc") == source.get("release_time_utc"),
            f"release timestamp changed: {event_id}",
        )
        require(
            observation.get("same_time_bls_labels") == source.get("same_time_bls_labels"),
            f"same-time labels changed: {event_id}",
        )
        pre_values.append(
            finite_nonnegative(observation.get("pre_abs_60m_return"), "pre_abs_60m_return")
        )
        post_values.append(
            finite_nonnegative(observation.get("post_abs_60m_return"), "post_abs_60m_return")
        )
        pre_spreads.append(
            finite_nonnegative(
                observation.get("pre_release_relative_spread"),
                "pre_release_relative_spread",
            )
        )
        first_post = observation.get("first_post_release_relative_spread")
        if first_post is not None:
            first_post_spreads.append(
                finite_nonnegative(first_post, "first_post_release_relative_spread")
            )
        year_groups.setdefault(result_year(observation.get("release_time_utc")), []).append(
            observation
        )
        same_time_count += bool(observation.get("same_time_bls_labels"))

    pre_median = statistics.median(pre_values)
    post_median = statistics.median(post_values)
    require(result.get("median_pre_abs_60m_return") == pre_median, "saved pre median drift")
    require(result.get("median_post_abs_60m_return") == post_median, "saved post median drift")
    inequality_pass = post_median > pre_median
    decision = "ADVANCE_TO_ECONOMIC_SCREEN" if inequality_pass else "REJECT"
    next_action = (
        "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4"
        if inequality_pass
        else "STOP_HYP0006"
    )
    require(result.get("primary_inequality_pass") is inequality_pass, "primary inequality drift")
    require(result.get("prototype_decision") == decision, "prototype decision drift")
    require(result.get("next_action") == next_action, "predeclared routing rule drift")
    require(
        result.get("median_pre_release_relative_spread") == statistics.median(pre_spreads),
        "pre-release spread diagnostic drift",
    )
    first_post_median = statistics.median(first_post_spreads) if first_post_spreads else None
    require(
        result.get("median_first_post_release_relative_spread") == first_post_median,
        "first-post spread diagnostic drift",
    )
    require(
        result.get("same_time_bls_flagged_event_count") == same_time_count,
        "same-time event diagnostic drift",
    )

    expected_years = [
        {
            "year": year,
            "count": len(items),
            "share_of_eligible": len(items) / 216,
            "median_pre_abs_return": statistics.median(
                item["pre_abs_60m_return"] for item in items
            ),
            "median_post_abs_return": statistics.median(
                item["post_abs_60m_return"] for item in items
            ),
        }
        for year, items in sorted(year_groups.items())
    ]
    require(result.get("calendar_year_diagnostics") == expected_years, "year diagnostics drift")
    expected_max = max((item["share_of_eligible"] for item in expected_years), default=0.0)
    require(result.get("max_calendar_year_event_share") == expected_max, "year share drift")
    require(
        not ({"pnl", "net_pnl", "gross_pnl", "directional_return"} & set(result)),
        "forbidden P&L/directional field in reveal result",
    )


def expected_reveal_text(result: dict[str, Any]) -> str:
    return "\n".join(
        (
            "HYP-0006 PROTO-01 FIRST REVEAL",
            f"Decision: {result['prototype_decision']}",
            f"Eligible: {result['eligible_event_count']}",
            f"Median pre absolute return: {result['median_pre_abs_60m_return']}",
            f"Median post absolute return: {result['median_post_abs_60m_return']}",
            f"Primary inequality pass: {result['primary_inequality_pass']}",
            f"Next action: {result['next_action']}",
            "EVIDENCE: DEVELOPMENT / EXPLORATORY ONLY; no trading-P&L claim.",
            "",
        )
    )


def validate_reveal_artifacts(
    rf027: dict[str, Any],
    rf028: dict[str, Any],
    exact_commit: str,
) -> None:
    print("\n== Validate preserved first-reveal artifacts ==", flush=True)
    require(reveal_artifact_state() == "EXISTING_PAIR", "complete reveal artifact pair absent")
    result = load_json(REVEAL_JSON, "HYP-0006 reveal result")
    validate_reveal_payload(result, rf027, rf028, exact_commit)
    try:
        report = REVEAL_TEXT.read_text(encoding="utf-8")
    except OSError as exc:
        raise TaskCheckError(f"reveal text report unreadable: {exc}") from exc
    require(report == expected_reveal_text(result), "reveal text report differs from JSON result")
    print("[PASS] preserved observations: 216", flush=True)
    print("[PASS] saved medians, primary inequality and predeclared decision rule", flush=True)
    print(f"[PASS] reveal JSON SHA-256: {sha256_file(REVEAL_JSON)}", flush=True)


def run(name: str, command: list[str]) -> bool:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, check=False)
    passed = completed.returncode == 0
    print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
    return passed


def main() -> int:
    print("ATS CURRENT TASK CHECK")
    print(f"Task: {TASK_ID} — {TASK_NAME}")
    print("No BLS/Dukascopy network path or downloader is authorized.", flush=True)
    print("Pre-execution information boundary: NO_HYPOTHESIS_OUTCOME_COMPUTED", flush=True)
    invocation_started = False
    artifact_state = "UNKNOWN"
    try:
        exact_commit = check_exact_main()
        check_runner_blob()
        check_frozen_lineage()
        rf027, rf028 = load_frozen_inputs()
        check_reveal_contract()
        artifact_state = reveal_artifact_state()
        print(f"[PASS] reveal artifact state: {artifact_state}", flush=True)
        require(
            run("full Local CI before market reveal", [sys.executable, "tools/verify_repo.py"]),
            "full Local CI failed; reveal forbidden",
        )
        require(check_exact_main() == exact_commit, "exact main changed during Local CI")
        check_runner_blob()
        verify_all_bi5_objects(rf027["tick_objects"])

        if artifact_state == "ABSENT":
            require(
                reveal_artifact_state() == "ABSENT",
                "reveal artifact state changed before one-shot invocation",
            )
            print("\n== One-shot frozen runner invocation ==", flush=True)
            invocation_started = True
            completed = subprocess.run(
                [sys.executable, str(PROTOTYPE_RUNNER), "--execute-first-reveal"],
                cwd=ROOT,
                check=False,
            )
            require(completed.returncode == 0, "frozen runner returned source/contract failure")
        else:
            print(
                "[PASS] existing exact-commit artifact pair: validation only, no rerun", flush=True
            )

        validate_reveal_artifacts(rf027, rf028, exact_commit)
    except (TaskCheckError, OSError, subprocess.CalledProcessError, KeyError, TypeError) as exc:
        print(f"\n[FAIL] RF-030 TECHNICAL_SOURCE_OR_CONTRACT_BLOCKER: {exc}", flush=True)
        if invocation_started or artifact_state in {"EXISTING_PAIR", "UNKNOWN"}:
            print("Information boundary: REVEAL_STATE_PRESENT_OR_STARTED_UNVALIDATED", flush=True)
        else:
            print("Information boundary: NO_HYPOTHESIS_OUTCOME_COMPUTED", flush=True)
        print("Technical failure is not a negative HYP-0006 result.", flush=True)
        print("ATS CURRENT TASK CHECK: FAIL", flush=True)
        return 1

    print("\nInformation boundary: DEVELOPMENT_REVEALED_EXPLORATORY_ONLY", flush=True)
    print(
        "Result is preserved whether the predeclared decision is positive or negative.", flush=True
    )
    print("ATS CURRENT TASK CHECK: PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
