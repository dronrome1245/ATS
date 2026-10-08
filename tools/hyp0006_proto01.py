#!/usr/bin/env python3
"""HYP-0006 PROTO-01: frozen structural CPI-event reveal runner.

NEVER execute during RF-029. RF-029 freezes this code and runs synthetic
contract tests only. A later separately gated reveal task may execute it.
No network/source-acquisition path is implemented.
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import lzma
import math
import statistics
import struct
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HYPOTHESIS_ID = "HYP-0006"
PROTO_ID = "PROTO-01"
RF027_COMMIT = "bbbdbd301b610dfc61316c9ff82015fb0e039a47"
RF028_COMMIT = "e7f05a0d237c4d78a8a0edb93710619e6ad2ba00"

FROZEN_RF028_JSON_SHA256 = "1b575682b959070f4a0981b7cd13d70626f1e169d221d0c9fb2383fc679fd5fb"
FROZEN_SOURCE_BUNDLE_SHA256 = "5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425"
FROZEN_GEOMETRY_SHA256 = "e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034"
FROZEN_DATASET_ID = "DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001"
FROZEN_DATASET_VERSION = "1.0.0"
FROZEN_CANDIDATE_COUNT = 217
FROZEN_ELIGIBLE_COUNT = 216
FROZEN_INELIGIBLE_ID = "BLS-CPI-20030815"
FROZEN_TOLERANCE_MS = 30_000
PRICE_DIVISOR = 100_000
TICK_RECORD = struct.Struct(">IIIff")

RF027_RESULT = ROOT / "reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP.json"
RF028_RESULT = ROOT / "reports/local_ci/HYP0006_DATA_TOLERANCE_FREEZE.json"
GEOMETRY_CSV = ROOT / "data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv"
RAW_TICKS_ROOT = ROOT / "data/raw/dukascopy/hyp0006/EURUSD"
REVEAL_JSON = ROOT / "reports/local_ci/HYP0006_PROTO01_RESULT.json"
REVEAL_TEXT = ROOT / "reports/local_ci/HYP0006_PROTO01_RESULT_REPORT.txt"

type Quote = tuple[datetime, int, int]


class PrototypeError(RuntimeError):
    """Exact frozen input/quote contract is not satisfied."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise PrototypeError(f"required local frozen input absent: {path}")
    result = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise PrototypeError(f"expected JSON mapping: {path}")
    return result


def require_value(result: dict[str, Any], key: str, expected: Any) -> None:
    if result.get(key) != expected:
        raise PrototypeError(f"frozen identity mismatch for {key}")


def load_frozen_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    if sha256_file(RF028_RESULT) != FROZEN_RF028_JSON_SHA256:
        raise PrototypeError("RF-028 JSON SHA-256 changed")
    rf028 = load_json(RF028_RESULT)
    for key, expected in {
        "task_id": "ATS2-RF-028",
        "hypothesis_id": HYPOTHESIS_ID,
        "git_commit": RF028_COMMIT,
        "rf027_git_commit": RF027_COMMIT,
        "dataset_id": FROZEN_DATASET_ID,
        "dataset_version": FROZEN_DATASET_VERSION,
        "candidate_event_count": FROZEN_CANDIDATE_COUNT,
        "eligible_event_count": FROZEN_ELIGIBLE_COUNT,
        "ineligible_event_count": 1,
        "source_bundle_sha256": FROZEN_SOURCE_BUNDLE_SHA256,
        "geometry_csv_sha256": FROZEN_GEOMETRY_SHA256,
        "boundary_max_abs_gap_ms": FROZEN_TOLERANCE_MS,
        "pre_release_max_staleness_ms": FROZEN_TOLERANCE_MS,
        "boundary_tie_break": "PREVIOUS_ON_EQUAL_GAP",
        "pre_release_rule": "LAST_QUOTE_STRICTLY_BEFORE_RELEASE",
        "duplicate_timestamp_tie_break": "LAST_RAW_RECORD_AT_SELECTED_MILLISECOND",
        "price_pairing_rule": "BID_AND_ASK_FROM_SAME_RAW_TICK_RECORD",
        "same_time_event_policy": "FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION",
        "missing_data_policy": ("EXCLUDE_EVENT_IF_ANY_REQUIRED_ANCHOR_FAILS_FROZEN_GAP_RULE"),
        "freeze_decision": "FREEZE_DATA_AND_TOLERANCES",
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    }.items():
        require_value(rf028, key, expected)

    eligible_ids = rf028.get("eligible_event_ids")
    ineligible = rf028.get("ineligible_events")
    evaluations = rf028.get("geometry_evaluations")
    if not isinstance(eligible_ids, list) or len(eligible_ids) != FROZEN_ELIGIBLE_COUNT:
        raise PrototypeError("RF-028 eligible ID denominator changed")
    if len(set(eligible_ids)) != FROZEN_ELIGIBLE_COUNT:
        raise PrototypeError("RF-028 duplicate eligible ID")
    if ineligible != [
        {
            "event_id": FROZEN_INELIGIBLE_ID,
            "exclusion_reasons": ["POST_60_ANCHOR_GAP_EXCEEDS_30000MS"],
        }
    ]:
        raise PrototypeError("RF-028 ineligible event identity changed")
    if not isinstance(evaluations, list) or len(evaluations) != FROZEN_CANDIDATE_COUNT:
        raise PrototypeError("RF-028 geometry evaluation denominator changed")
    if sha256_file(GEOMETRY_CSV) != FROZEN_GEOMETRY_SHA256:
        raise PrototypeError("RF-027 timestamp geometry SHA-256 changed")

    rf027 = load_json(RF027_RESULT)
    for key, expected in {
        "task_id": "ATS2-RF-027",
        "git_commit": RF027_COMMIT,
        "candidate_event_count": FROZEN_CANDIDATE_COUNT,
        "acquired_tick_object_count": 1085,
        "missing_tick_object_count": 0,
        "protected_hyp0005_source_requests": 0,
        "source_bundle_sha256": FROZEN_SOURCE_BUNDLE_SHA256,
        "geometry_csv_sha256": FROZEN_GEOMETRY_SHA256,
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    }.items():
        require_value(rf027, key, expected)

    if len(rf027.get("events", [])) != FROZEN_CANDIDATE_COUNT:
        raise PrototypeError("RF-027 event array incomplete")
    if len(rf027.get("tick_objects", [])) != 1085:
        raise PrototypeError("RF-027 raw BI5 inventory incomplete")
    if len({v.get("event_id") for v in rf027["events"]}) != FROZEN_CANDIDATE_COUNT:
        raise PrototypeError("RF-027 duplicate event ID")
    rf027_ids = {v["event_id"] for v in rf027["events"]}
    if rf027_ids != set(eligible_ids) | {FROZEN_INELIGIBLE_ID}:
        raise PrototypeError("RF-027 and RF-028 denominators disagree")
    return rf027, rf028


def parse_utc(timestamp: str) -> datetime:
    value = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if value.tzinfo is None or value.utcoffset() != timedelta():
        raise PrototypeError(f"non-UTC event timestamp: {timestamp}")
    return value.astimezone(UTC)


def required_hours(release: datetime) -> list[datetime]:
    pre_hour = (release - timedelta(minutes=60)).replace(minute=0, second=0, microsecond=0)
    post_hour = (release + timedelta(minutes=60)).replace(minute=0, second=0, microsecond=0)
    first = pre_hour - timedelta(hours=1)
    last = post_hour + timedelta(hours=1)
    count = int((last - first).total_seconds() // 3600) + 1
    return [first + timedelta(hours=index) for index in range(count)]


def tick_path(hour: datetime) -> Path:
    return (
        RAW_TICKS_ROOT
        / str(hour.year)
        / f"{hour.month:02d}"
        / f"{hour.day:02d}"
        / f"{hour.hour:02d}h_ticks.bi5"
    )


def decode_quotes(path: Path, hour: datetime, identity: dict[str, Any]) -> list[Quote]:
    expected_path = path.relative_to(ROOT).as_posix()
    if identity.get("relative_path") != expected_path:
        raise PrototypeError("frozen raw object path identity mismatch")
    if not path.is_file() or sha256_file(path) != identity.get("sha256"):
        raise PrototypeError(f"frozen raw BI5 missing or hash mismatch: {expected_path}")
    try:
        payload = lzma.decompress(path.read_bytes())
    except lzma.LZMAError as exc:
        raise PrototypeError(f"BI5 decode failed: {expected_path}") from exc
    if not payload or len(payload) % TICK_RECORD.size:
        raise PrototypeError(f"invalid BI5 record length: {expected_path}")

    quotes: list[Quote] = []
    previous_ms = -1
    for offset in range(0, len(payload), TICK_RECORD.size):
        ms, ask_raw, bid_raw, ask_vol, bid_vol = TICK_RECORD.unpack_from(payload, offset)
        if not previous_ms <= ms < 3_600_000 or ask_raw < bid_raw or bid_raw <= 0:
            raise PrototypeError(f"invalid BI5 timestamp or BID/ASK: {expected_path}")
        if not all(math.isfinite(v) and v >= 0 for v in (ask_vol, bid_vol)):
            raise PrototypeError(f"invalid BI5 quote volume: {expected_path}")
        quotes.append((hour + timedelta(milliseconds=ms), bid_raw, ask_raw))
        previous_ms = ms

    if identity.get("record_count") != len(quotes):
        raise PrototypeError(f"frozen tick record count mismatch: {expected_path}")
    return quotes


def select_nearest(quotes: list[Quote], target: datetime) -> tuple[Quote, str, int]:
    timestamps = [item[0] for item in quotes]
    before = bisect.bisect_right(timestamps, target) - 1
    after = bisect.bisect_left(timestamps, target)
    candidates: list[tuple[int, int, str]] = []
    if before >= 0:
        candidates.append(
            (round((target - timestamps[before]).total_seconds() * 1000), 0, "PREVIOUS")
        )
    if after < len(quotes):
        candidates.append((round((timestamps[after] - target).total_seconds() * 1000), 1, "NEXT"))
    if not candidates:
        raise PrototypeError("missing nearest tick")
    gap, _, side = min(candidates)
    if gap > FROZEN_TOLERANCE_MS:
        raise PrototypeError("selected nearest tick exceeds frozen 30s tolerance")
    selected = before if side == "PREVIOUS" else after
    final_index = bisect.bisect_right(timestamps, timestamps[selected]) - 1
    return quotes[final_index], side, gap


def select_pre_release(quotes: list[Quote], release: datetime) -> tuple[Quote, int]:
    timestamps = [item[0] for item in quotes]
    index = bisect.bisect_left(timestamps, release) - 1
    if index < 0:
        raise PrototypeError("no tick strictly before release")
    gap = round((release - timestamps[index]).total_seconds() * 1000)
    if gap > FROZEN_TOLERANCE_MS or not quotes[index][0] < release:
        raise PrototypeError("pre-release quote violates frozen 30s strict-before rule")
    return quotes[index], gap


def first_post_release(quotes: list[Quote], release: datetime) -> Quote | None:
    timestamps = [item[0] for item in quotes]
    index = bisect.bisect_left(timestamps, release)
    if index == len(quotes):
        return None
    # Duplicate selected millisecond: LAST_RAW_RECORD, also for diagnostic quote.
    final_index = bisect.bisect_right(timestamps, timestamps[index]) - 1
    return quotes[final_index]


def mid(quote: Quote) -> float:
    return (quote[1] + quote[2]) / (2 * PRICE_DIVISOR)


def relative_spread(quote: Quote) -> float:
    return (quote[2] - quote[1]) / ((quote[1] + quote[2]) / 2)


def absolute_return(first: Quote, last: Quote) -> float:
    return abs(mid(last) / mid(first) - 1)


def one_event(
    event: dict[str, Any],
    geometry: dict[str, Any],
    identities: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    release = parse_utc(event["release_time_utc"])
    records: list[Quote] = []
    for hour in required_hours(release):
        identity = identities.get(hour.isoformat().replace("+00:00", "Z"))
        if identity is None:
            raise PrototypeError("missing frozen tick-hour identity")
        records.extend(decode_quotes(tick_path(hour), hour, identity))
    if not records:
        raise PrototypeError("empty quote window")
    if any(records[i][0] > records[i + 1][0] for i in range(len(records) - 1)):
        raise PrototypeError("out-of-order multi-hour quote window")

    pre60, pre_side, pre_gap = select_nearest(records, release - timedelta(minutes=60))
    before, before_gap = select_pre_release(records, release)
    post60, post_side, post_gap = select_nearest(records, release + timedelta(minutes=60))
    if (
        (pre_side, pre_gap) != (geometry["pre60_selected_side"], geometry["pre60_selected_gap_ms"])
        or before_gap != geometry["pre_release_last_gap_ms"]
        or (post_side, post_gap)
        != (geometry["post60_selected_side"], geometry["post60_selected_gap_ms"])
    ):
        raise PrototypeError(f"anchor differs from frozen RF-028 geometry: {event['event_id']}")
    diagnostic_quote = first_post_release(records, release)
    return {
        "event_id": event["event_id"],
        "release_time_utc": event["release_time_utc"],
        "same_time_bls_labels": event["same_time_bls_labels"],
        "pre_abs_60m_return": absolute_return(pre60, before),
        "post_abs_60m_return": absolute_return(before, post60),
        "pre_release_relative_spread": relative_spread(before),
        "first_post_release_relative_spread": (
            relative_spread(diagnostic_quote) if diagnostic_quote else None
        ),
    }


def primary_decision(pre_median: float, post_median: float) -> tuple[bool, str, str]:
    passed = post_median > pre_median
    if passed:
        return (
            True,
            "ADVANCE_TO_ECONOMIC_SCREEN",
            "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
        )
    return False, "REJECT", "STOP_HYP0006"


def prepare_first_reveal() -> dict[str, Any]:
    rf027, rf028 = load_frozen_inputs()
    events = {item["event_id"]: item for item in rf027["events"]}
    geometry = {item["event_id"]: item for item in rf028["geometry_evaluations"]}
    identities = {item["hour_start"]: item for item in rf027["tick_objects"]}
    if len(identities) != 1085 or len(geometry) != FROZEN_CANDIDATE_COUNT:
        raise PrototypeError("duplicate frozen tick/hour or event identities")

    observations: list[dict[str, Any]] = []
    for event_id in rf028["eligible_event_ids"]:
        if event_id not in events or event_id not in geometry or not geometry[event_id]["eligible"]:
            raise PrototypeError("event is not in the frozen eligible denominator")
        observations.append(one_event(events[event_id], geometry[event_id], identities))
    if len(observations) != FROZEN_ELIGIBLE_COUNT:
        raise PrototypeError("revealed observation count differs from frozen 216")

    pre = [item["pre_abs_60m_return"] for item in observations]
    post = [item["post_abs_60m_return"] for item in observations]
    pre_median = statistics.median(pre)
    post_median = statistics.median(post)
    passed, decision, next_action = primary_decision(pre_median, post_median)
    year_groups: dict[int, list[dict[str, Any]]] = {}
    for observation in observations:
        year = parse_utc(observation["release_time_utc"]).year
        year_groups.setdefault(year, []).append(observation)
    year_diagnostics = [
        {
            "year": year,
            "count": len(items),
            "share_of_eligible": len(items) / FROZEN_ELIGIBLE_COUNT,
            "median_pre_abs_return": statistics.median(
                item["pre_abs_60m_return"] for item in items
            ),
            "median_post_abs_return": statistics.median(
                item["post_abs_60m_return"] for item in items
            ),
        }
        for year, items in sorted(year_groups.items())
    ]
    same_time_count = sum(bool(v["same_time_bls_labels"]) for v in observations)
    first_post_spreads = [
        v["first_post_release_relative_spread"]
        for v in observations
        if v["first_post_release_relative_spread"] is not None
    ]
    return {
        "schema_version": "hyp0006-proto01-reveal-1",
        "hypothesis_id": HYPOTHESIS_ID,
        "prototype_id": PROTO_ID,
        "git_commit": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "rf028_git_commit": RF028_COMMIT,
        "rf028_json_sha256": FROZEN_RF028_JSON_SHA256,
        "dataset_id": FROZEN_DATASET_ID,
        "dataset_version": FROZEN_DATASET_VERSION,
        "source_bundle_sha256": FROZEN_SOURCE_BUNDLE_SHA256,
        "geometry_csv_sha256": FROZEN_GEOMETRY_SHA256,
        "evidence_classification": "DEVELOPMENT_EXPLORATORY_ONLY",
        "candidate_event_count": FROZEN_CANDIDATE_COUNT,
        "eligible_event_count": FROZEN_ELIGIBLE_COUNT,
        "ineligible_event_count": 1,
        "ineligible_event_ids": [FROZEN_INELIGIBLE_ID],
        "event_observations": observations,
        "median_pre_abs_60m_return": pre_median,
        "median_post_abs_60m_return": post_median,
        "primary_inequality_pass": passed,
        "prototype_decision": decision,
        "next_action": next_action,
        "median_pre_release_relative_spread": statistics.median(
            v["pre_release_relative_spread"] for v in observations
        ),
        "median_first_post_release_relative_spread": (
            statistics.median(first_post_spreads) if first_post_spreads else None
        ),
        "same_time_bls_flagged_event_count": same_time_count,
        "calendar_year_diagnostics": year_diagnostics,
        "max_calendar_year_event_share": max(
            (v["share_of_eligible"] for v in year_diagnostics), default=0.0
        ),
        "outcome_metrics_computed": True,
        "primary_claim_evaluated": True,
        "information_boundary": "DEVELOPMENT_REVEALED_EXPLORATORY_ONLY",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute-first-reveal", action="store_true")
    args = parser.parse_args()
    if not args.execute_first_reveal:
        print("REVEAL_BLOCKED_PRE_FREEZE: explicit later task required")
        return 2
    if REVEAL_JSON.exists() or REVEAL_TEXT.exists():
        print("REVEAL_ALREADY_PRESENT: do not re-run a first reveal")
        return 2
    try:
        result = prepare_first_reveal()
    except (PrototypeError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"PROTO-01 SOURCE_OR_CONTRACT_BLOCKED: {exc}")
        return 1
    REVEAL_JSON.parent.mkdir(parents=True, exist_ok=True)
    REVEAL_JSON.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    lines = [
        "HYP-0006 PROTO-01 FIRST REVEAL",
        f"Decision: {result['prototype_decision']}",
        f"Eligible: {result['eligible_event_count']}",
        f"Median pre absolute return: {result['median_pre_abs_60m_return']}",
        f"Median post absolute return: {result['median_post_abs_60m_return']}",
        f"Primary inequality pass: {result['primary_inequality_pass']}",
        f"Next action: {result['next_action']}",
        "EVIDENCE: DEVELOPMENT / EXPLORATORY ONLY; no trading-P&L claim.",
    ]
    REVEAL_TEXT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
