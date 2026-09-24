#!/usr/bin/env python3
"""Diagnose one RF-008 cached source candle without running full acquisition."""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import hyp0003_development_data as prep

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SYMBOL = "AUDUSD"
DEFAULT_MONTH = "2007-04"
DEFAULT_TIMESTAMP = "2007-04-09T11:00:00Z"
TASK_REPORT_PATH = ROOT / "reports" / "local_ci" / "CURRENT_TASK_REPORT.txt"
FAILURE_PATTERN = re.compile(
    r"HYP-0003 DEVELOPMENT DATA PREP BLOCKED: "
    r"(?P<symbol>[A-Z]{6}) "
    r"(?P<month>\d{4}-\d{2}) "
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) "
    r"(?P<source_format>[A-Z0-9_]+):"
)
JETTA_CANDLE_FAILURE_PATTERN = re.compile(
    r"HYP-0003 DEVELOPMENT DATA PREP BLOCKED: invalid Jetta (?P<field>high|low|OHLC geometry) in "
    r".*[\\/](?P<symbol>[A-Z]{6})[\\/]H1[\\/](?P<year>\d{4})[\\/](?P<month>\d{2})"
    r"[\\/](?P<side>BID|ASK)_candles_hour_1\.json: "
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+00:00)"
)
NEIGHBOR_COUNT = 2
SCAN_TOP_EXAMPLES = 20


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


def latest_report_target() -> tuple[str, str, str] | None:
    if not TASK_REPORT_PATH.is_file():
        return None
    try:
        lines = TASK_REPORT_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        match = FAILURE_PATTERN.search(line)
        if match is not None:
            return (
                match.group("symbol"),
                match.group("month"),
                match.group("timestamp"),
            )
        jetta_match = JETTA_CANDLE_FAILURE_PATTERN.search(line)
        if jetta_match is not None:
            return (
                jetta_match.group("symbol"),
                f"{jetta_match.group('year')}-{jetta_match.group('month')}",
                jetta_match.group("timestamp"),
            )
    return None


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
                    f"scaled={scaled:.17g}; "
                    f"python_round={round(scaled)}; "
                    f"js_math_round={js_math_round_positive(scaled)}"
                )


def ohlc_is_internally_valid(values: prep.Ohlc) -> bool:
    open_price, high_price, low_price, close_price = values
    return (
        all(math.isfinite(value) and value > 0 for value in values)
        and high_price >= max(open_price, close_price)
        and high_price >= low_price
        and low_price <= min(open_price, close_price)
    )


def forensic_jetta_rows(
    path: Path,
    month: datetime,
    use_js_round: bool,
) -> list[tuple[datetime, prep.Ohlc, tuple[int, int, int, int], bool]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    multiplier = float(payload["multiplier"])
    shift = int(payload["shift"])
    timestamp_ms = int(payload["timestamp"])
    base_values = [float(payload[name]) for name in ("open", "high", "low", "close")]
    deltas = [payload[name] for name in ("opens", "highs", "lows", "closes")]
    rounder = js_math_round_positive if use_js_round else round
    units = [rounder(value / multiplier) for value in base_values]
    scale = prep.multiplier_scale(multiplier)
    end = prep.next_month(month)
    rows: list[tuple[datetime, prep.Ohlc, tuple[int, int, int, int], bool]] = []

    for index, time_delta in enumerate(payload["times"]):
        timestamp_ms += int(time_delta) * shift
        step_deltas = tuple(int(column[index]) for column in deltas)
        for field_index, delta in enumerate(step_deltas):
            units[field_index] += delta
        timestamp = datetime.fromtimestamp(timestamp_ms / 1000.0, tz=UTC)
        if not month <= timestamp < end:
            continue
        values = tuple(round(value * multiplier, scale) for value in units)
        rows.append(
            (
                timestamp,
                values,
                step_deltas,
                ohlc_is_internally_valid(values),
            )
        )
    return rows


def print_forensic_jetta_target(
    path: Path,
    month: datetime,
    side: str,
    target: datetime,
) -> None:
    print(f"\n{side} Jetta forensic reconstruction:")
    modes = (
        ("python_round", False),
        ("js_math_round", True),
    )
    for label, use_js_round in modes:
        rows = forensic_jetta_rows(path, month, use_js_round)
        timestamps = [row[0] for row in rows]
        if target not in timestamps:
            print(f"  {label}: target timestamp not present")
            continue
        index = timestamps.index(target)
        start = max(0, index - NEIGHBOR_COUNT)
        end = min(len(rows), index + NEIGHBOR_COUNT + 1)
        print(f"  mode={label}")
        for timestamp, values, step_deltas, valid in rows[start:end]:
            marker = " <TARGET>" if timestamp == target else ""
            print(f"    {prep.iso_z(timestamp)}{marker}")
            print(f"      OHLC: {values}")
            print(f"      encoded deltas: {step_deltas}")
            print(f"      internally_valid: {valid}")


def geometry_violation_units(units: list[int]) -> int:
    open_units, high_units, low_units, close_units = units
    return max(
        0,
        max(open_units, close_units) - high_units,
        low_units - high_units,
        low_units - min(open_units, close_units),
    )


def cached_jetta_paths() -> list[Path]:
    candidate_symbols = {symbol for symbol, _orientation in prep.CANDIDATES.values()}
    paths: list[Path] = []
    for path in prep.RAW_ROOT.glob("*/H1/*/*/*_candles_hour_1.json"):
        relative = path.relative_to(prep.RAW_ROOT)
        if len(relative.parts) != 5:
            continue
        symbol, timeframe, year_text, month_text, _filename = relative.parts
        if symbol not in candidate_symbols or timeframe != "H1":
            continue
        try:
            month = datetime(
                int(year_text),
                int(month_text),
                1,
                tzinfo=UTC,
            )
        except ValueError:
            continue
        if month >= prep.DATA_END:
            continue
        if path.is_file() and path.stat().st_size > 0:
            paths.append(path)
    return sorted(paths)


def scan_jetta_file(
    path: Path,
) -> tuple[Counter[int], list[dict[str, object]], int]:
    relative = path.relative_to(prep.RAW_ROOT)
    symbol, _timeframe, year_text, month_text, filename = relative.parts
    side = filename.split("_", 1)[0]
    month = datetime(int(year_text), int(month_text), 1, tzinfo=UTC)
    payload = json.loads(path.read_text(encoding="utf-8"))

    multiplier = float(payload["multiplier"])
    shift = int(payload["shift"])
    timestamp_ms = int(payload["timestamp"])
    base_values = [float(payload[name]) for name in ("open", "high", "low", "close")]
    deltas = [payload[name] for name in ("opens", "highs", "lows", "closes")]
    units = [round(value / multiplier) for value in base_values]
    rounding_mismatches = sum(
        round(value / multiplier) != js_math_round_positive(value / multiplier)
        for value in base_values
    )

    histogram: Counter[int] = Counter()
    examples: list[dict[str, object]] = []
    end = prep.next_month(month)

    for index, time_delta in enumerate(payload["times"]):
        timestamp_ms += int(time_delta) * shift
        for field_index, column in enumerate(deltas):
            units[field_index] += int(column[index])
        timestamp = datetime.fromtimestamp(timestamp_ms / 1000.0, tz=UTC)
        if not month <= timestamp < end:
            continue

        violation = geometry_violation_units(units)
        histogram[violation] += 1
        if violation > 0:
            examples.append(
                {
                    "violation_units": violation,
                    "symbol": symbol,
                    "month": f"{month:%Y-%m}",
                    "side": side,
                    "timestamp": prep.iso_z(timestamp),
                    "units": tuple(units),
                    "path": str(relative).replace("\\", "/"),
                }
            )

    return histogram, examples, rounding_mismatches


def print_scan_histogram(histogram: Counter[int]) -> None:
    exact_limit = 20
    print("\nGeometry violation histogram (encoded units):")
    for units in range(exact_limit + 1):
        count = histogram.get(units, 0)
        if count or units <= 2:
            print(f"  {units}: {count}")
    above = sum(count for units, count in histogram.items() if units > exact_limit)
    if above:
        print(f"  >{exact_limit}: {above}")


def scan_cached_jetta_geometry() -> int:
    paths = cached_jetta_paths()
    print("\n== cache-wide Jetta OHLC geometry scan ==")
    print(f"Cached Jetta files selected: {len(paths)}")
    print("Protected-tail files read: 0")
    print(f"Current production tolerance: {prep.JETTA_OHLC_TOLERANCE_UNITS} unit")

    total_histogram: Counter[int] = Counter()
    all_examples: list[dict[str, object]] = []
    file_errors: list[str] = []
    group_max: dict[tuple[str, str], int] = {}
    rounding_mismatches = 0

    for path in paths:
        try:
            histogram, examples, file_rounding_mismatches = scan_jetta_file(path)
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            file_errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue

        total_histogram.update(histogram)
        all_examples.extend(examples)
        rounding_mismatches += file_rounding_mismatches

        relative = path.relative_to(prep.RAW_ROOT)
        symbol = relative.parts[0]
        side = relative.parts[-1].split("_", 1)[0]
        file_max = max(histogram, default=0)
        group_max[(symbol, side)] = max(
            group_max.get((symbol, side), 0),
            file_max,
        )

    total_candles = sum(total_histogram.values())
    violating = total_candles - total_histogram.get(0, 0)
    beyond = sum(
        count for units, count in total_histogram.items() if units > prep.JETTA_OHLC_TOLERANCE_UNITS
    )
    maximum = max(total_histogram, default=0)

    print(f"Files scanned successfully: {len(paths) - len(file_errors)}")
    print(f"File errors: {len(file_errors)}")
    print(f"Candles scanned: {total_candles}")
    print(f"Candles with any geometry discrepancy: {violating}")
    print(f"Candles beyond current tolerance: {beyond}")
    print(f"Maximum geometry violation units: {maximum}")
    print(f"Base-field Python/JS rounding mismatches: {rounding_mismatches}")
    print_scan_histogram(total_histogram)

    print("\nMaximum violation by symbol/side:")
    for (symbol, side), value in sorted(group_max.items()):
        print(f"  {symbol} {side}: {value}")

    if all_examples:
        ranked = sorted(
            all_examples,
            key=lambda item: (
                -int(item["violation_units"]),
                str(item["symbol"]),
                str(item["side"]),
                str(item["timestamp"]),
            ),
        )
        print(f"\nTop {min(SCAN_TOP_EXAMPLES, len(ranked))} violating candles:")
        for item in ranked[:SCAN_TOP_EXAMPLES]:
            print(
                "  "
                f"{item['violation_units']} units | "
                f"{item['symbol']} {item['side']} {item['timestamp']} | "
                f"OHLC units={item['units']} | {item['path']}"
            )

    if file_errors:
        print("\nFile errors:")
        for error in file_errors[:SCAN_TOP_EXAMPLES]:
            print(f"  {error}")

    print("\nInformation boundary: NO_HYPOTHESIS_OUTCOME_COMPUTED")
    print("Network access: DISABLED_BY_DESIGN")
    print("ATS JETTA GEOMETRY SCAN: COMPLETE")
    return 0 if not file_errors else 1


def available_formats(symbol: str, month: datetime) -> list[tuple[str, dict[str, Path]]]:
    formats: list[tuple[str, dict[str, Path]]] = []
    jetta = {side: prep.jetta_raw_path(symbol, month, side) for side in ("BID", "ASK")}
    legacy = {side: prep.raw_path(symbol, month, side) for side in ("BID", "ASK")}
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

    try:
        bid_rows = prep.decode_source_object(
            paths["BID"],
            month,
            symbol,
            source_format,
        )
    except prep.DevelopmentDataPrepError as exc:
        print(f"Strict BID decode: BLOCKED — {exc}")
        if source_format == prep.SOURCE_FORMAT_JETTA_JSON:
            print_forensic_jetta_target(paths["BID"], month, "BID", target)
            print_forensic_jetta_target(paths["ASK"], month, "ASK", target)
        return True

    try:
        ask_rows = prep.decode_source_object(
            paths["ASK"],
            month,
            symbol,
            source_format,
        )
    except prep.DevelopmentDataPrepError as exc:
        print(f"Strict ASK decode: BLOCKED — {exc}")
        if source_format == prep.SOURCE_FORMAT_JETTA_JSON:
            print_forensic_jetta_target(paths["BID"], month, "BID", target)
            print_forensic_jetta_target(paths["ASK"], month, "ASK", target)
        return True

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
    parser.add_argument("--symbol")
    parser.add_argument("--month")
    parser.add_argument("--timestamp")
    parser.add_argument(
        "--scan-jetta-geometry",
        action="store_true",
        help="Scan all cached pre-protected Jetta H1 candles for OHLC geometry discrepancies.",
    )
    args = parser.parse_args()

    if args.scan_jetta_geometry:
        print("ATS CURRENT TASK DIAGNOSTIC")
        print("Task: ATS2-RF-008 — HYP-0003 development data preparation")
        print(f"Commit: {git_head()}")
        return scan_cached_jetta_geometry()

    report_target = latest_report_target()
    report_symbol, report_month, report_timestamp = report_target or (
        DEFAULT_SYMBOL,
        DEFAULT_MONTH,
        DEFAULT_TIMESTAMP,
    )
    symbol = (args.symbol or report_symbol).upper()
    month_text = args.month or report_month
    timestamp_text = args.timestamp or report_timestamp

    try:
        month = parse_month(month_text)
        target = parse_timestamp(timestamp_text)
    except ValueError as exc:
        print(f"[FAIL] invalid diagnostic arguments: {exc}")
        return 2

    print("ATS CURRENT TASK DIAGNOSTIC")
    print("Task: ATS2-RF-008 — HYP-0003 development data preparation")
    print(f"Commit: {git_head()}")
    print(f"Symbol: {symbol}")
    print(f"Month: {month:%Y-%m}")
    print(f"Timestamp: {prep.iso_z(target)}")
    print(
        "Target source: "
        + ("CURRENT_TASK_REPORT.txt" if report_target is not None else "frozen default")
    )
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
                diagnose_format(symbol, month, target, source_format, paths) or decoded_any
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
