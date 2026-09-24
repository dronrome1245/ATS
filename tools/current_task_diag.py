#!/usr/bin/env python3
"""Diagnose one RF-008 cached source candle without running full acquisition."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
from datetime import UTC, datetime
from pathlib import Path
import hyp0003_development_data as prep

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SYMBOL = "AUDUSD"
DEFAULT_MONTH = "2007-04"
DEFAULT_TIMESTAMP = "2007-04-09T11:00:00Z"
NEIGHBOR_COUNT = 2


def parse_month(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m").replace(tzinfo=UTC)


def parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed.astimezone(UTC)


def git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def orientation_for_symbol(symbol: str) -> str:
    matches = [
        orientation
        for candidate_symbol, orientation in prep.CANDIDATES.values()
        if candidate_symbol == symbol
    ]
    if len(matches) != 1:
        raise ValueError(f"symbol is not a unique RF-008 candidate: {symbol}")
    return matches[0]


def js_math_round_positive(value: float) -> int:
    return math.floor(value + 0.5)


def print_jetta_metadata(path: Path, side: str) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    multiplier = payload.get("multiplier")
    print(f"{side} Jetta multiplier: {multiplier}")
    print(f"{side} Jetta shift: {payload.get('shift')}")
    print(f"{side} Jetta base timestamp: {payload.get('timestamp')}")
    print(f"{side} Jetta encoded candles: {len(payload.get('times', []))}")
    for field in ("open", "high", "low", "close"):
        value = payload.get(field)
        print(f"{side} Jetta base {field}: {value}")
        if isinstance(value, (int, float)) and isinstance(multiplier, (int, float)):
            if multiplier > 0:
                scaled = float(value) / float(multiplier)
                print(
                    f"{side} Jetta base {field} units: "
                    f"python_round={round(scaled)}; "
                    f"js_math_round={js_math_round_positive(scaled)}"
                )


def available_formats(symbol: str, month: datetime) -> list[tuple[str, dict[str, Path]]]:
    formats: list[tuple[str, dict[str, Path]]] = []
    jetta = {
        side: prep.jetta_raw_path(symbol, month, side)
        for side in ("BID", "ASK")
    }
    legacy = {
        side: prep.raw_path(symbol, month, side)
        for side in ("BID", "ASK")
    }
    if any(path.exists() for path in jetta.values()):
        formats.append((prep.SOURCE_FORMAT_JETTA_JSON, jetta))
    if any(path.exists() for path in legacy.values()):
        formats.append((prep.SOURCE_FORMAT_BI5, legacy))
    return formats


def print_neighbor_rows(
    bid_rows: dict[datetime, prep.Ohlc],
    ask_rows: dict[datetime, prep.Ohlc],
    target: datetime,
) -> None:
    common = sorted(set(bid_rows).intersection(ask_rows))
    if target not in common:
        print("Target timestamp is not present on both sides.")
        return

    index = common.index(target)
    start = max(0, index - NEIGHBOR_COUNT)
    end = min(len(common), index + NEIGHBOR_COUNT + 1)
    print("\nNeighbor rows:")
    for timestamp in common[start:end]:
        bid = bid_rows[timestamp]
        ask = ask_rows[timestamp]
        deltas = tuple(ask[i] - bid[i] for i in range(4))
        marker = " <TARGET>" if timestamp == target else ""
        print(f"  {prep.iso_z(timestamp)}{marker}")
        print(f"    BID: {bid}")
        print(f"    ASK: {ask}")
        print(f"    ASK-BID: {deltas}")


def diagnose_format(
    symbol: str,
    month: datetime,
    target: datetime,
    source_format: str,
    paths: dict[str, Path],
) -> bool:
    print(f"\n== source format: {source_format} ==")
    for side in ("BID", "ASK"):
        path = paths[side]
        state = "present" if path.exists() and path.stat().st_size > 0 else "missing"
        print(f"{side} path: {path.relative_to(ROOT)} [{state}]")

    if not all(path.exists() and path.stat().st_size > 0 for path in paths.values()):
        print("Pair is incomplete in this format; skipping decode.")
        return False

    for side in ("BID", "ASK"):
        path = paths[side]
        print(f"{side} sha256: {prep.sha256_file(path)}")
        if source_format == prep.SOURCE_FORMAT_JETTA_JSON:
            print_jetta_metadata(path, side)

    bid_rows = prep.decode_source_object(
        paths["BID"],
        month,
        symbol,
        source_format,
    )
    ask_rows = prep.decode_source_object(
        paths["ASK"],
        month,
        symbol,
        source_format,
    )

    print(f"BID decoded rows: {len(bid_rows)}")
    print(f"ASK decoded rows: {len(ask_rows)}")
    print_neighbor_rows(bid_rows, ask_rows, target)

    if target not in bid_rows or target not in ask_rows:
        return True

    orientation = orientation_for_symbol(symbol)
    print(f"Orientation: {orientation}")
    try:
        normalized = prep.normalize_pair_ohlc(
            bid_rows[target],
            ask_rows[target],
            orientation,
        )
    except prep.DevelopmentDataPrepError as exc:
        print(f"Normalization result: BLOCKED — {exc}")
    else:
        print(f"Normalization result: PASS — {normalized}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="RF-008 cached-candle diagnostic")
    parser.add_argument("--symbol", default=DEFAULT_SYMBOL)
    parser.add_argument("--month", default=DEFAULT_MONTH)
    parser.add_argument("--timestamp", default=DEFAULT_TIMESTAMP)
    args = parser.parse_args()

    symbol = args.symbol.upper()
    try:
        month = parse_month(args.month)
        target = parse_timestamp(args.timestamp)
    except ValueError as exc:
        print(f"[FAIL] invalid diagnostic arguments: {exc}")
        return 2

    print("ATS CURRENT TASK DIAGNOSTIC")
    print("Task: ATS2-RF-008 — HYP-0003 development data preparation")
    print(f"Commit: {git_head()}")
    print(f"Symbol: {symbol}")
    print(f"Month: {month:%Y-%m}")
    print(f"Timestamp: {prep.iso_z(target)}")
    print("Network access: DISABLED_BY_DESIGN")
    print("Information boundary: NO_HYPOTHESIS_OUTCOME_COMPUTED")

    formats = available_formats(symbol, month)
    if not formats:
        print("[FAIL] no cached source objects found for requested symbol/month")
        return 1

    decoded_any = False
    for source_format, paths in formats:
        try:
            decoded_any = (
                diagnose_format(symbol, month, target, source_format, paths)
                or decoded_any
            )
        except (OSError, ValueError, json.JSONDecodeError, prep.DevelopmentDataPrepError) as exc:
            print(f"Diagnostic decode blocked for {source_format}: {exc}")

    if not decoded_any:
        print("[FAIL] no complete cached BID/ASK pair could be decoded")
        return 1

    print("\nATS TASK DIAGNOSTIC: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
