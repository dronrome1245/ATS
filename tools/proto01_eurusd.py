#!/usr/bin/env python3
"""Prepare and run HYP-0001 PROTO-01 on EUR/USD 1H Dukascopy data."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import lzma
import statistics
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
START = datetime(2021, 1, 1, tzinfo=UTC)
END = datetime(2026, 1, 1, tzinfo=UTC)
SYMBOL = "EURUSD"
PRICE_DIVISOR = 100_000
RECORD = struct.Struct(">IIIIIf")
RAW_DIR = ROOT / "data" / "external" / "dukascopy" / SYMBOL / "H1"
DERIVED_PATH = ROOT / "data" / "derived" / "HYP-0001-PROTO-01-EURUSD-H1.csv"
MANIFEST_PATH = ROOT / "data" / "manifests" / "DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml"
DATA_REPORT_PATH = ROOT / "reports" / "local_ci" / "PROTO01_DATA_REPORT.txt"
RESULT_PATH = ROOT / "reports" / "research" / "HYP-0001-PROTOTYPE-01-result.json"
RESULT_REPORT_PATH = ROOT / "reports" / "local_ci" / "PROTO01_RESULT_REPORT.txt"
DOWNLOAD_BASES = (
    "https://datafeed.dukascopy.com/datafeed",
    "https://www.dukascopy.com/datafeed",
)
USER_AGENT = "ATS-Research/1.0"
MIN_SIGNAL_COUNT = 100


class ProtoDataError(RuntimeError):
    """Raised when the fixed prototype data contract cannot be satisfied."""


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> int:
    first = datetime(year, month, 1, tzinfo=UTC)
    offset = (weekday - first.weekday()) % 7
    return 1 + offset + 7 * (n - 1)


def us_dst_active_utc(value: datetime) -> bool:
    """Return US daylight-saving status used by Dukascopy FX trading hours."""

    year = value.year
    march_sunday = nth_weekday_of_month(year, 3, 6, 2)
    november_sunday = nth_weekday_of_month(year, 11, 6, 1)
    start = datetime(year, 3, march_sunday, 7, tzinfo=UTC)
    end = datetime(year, 11, november_sunday, 6, tzinfo=UTC)
    return start <= value < end


def is_fx_market_hour(value: datetime) -> bool:
    """Return whether an H1 bar opening at value belongs to Dukascopy FX hours."""

    weekday = value.weekday()
    if weekday < 4:
        return True
    summer = us_dst_active_utc(value)
    boundary_hour = 21 if summer else 22
    if weekday == 4:
        return value.hour < boundary_hour
    if weekday == 5:
        return False
    return value.hour >= boundary_hour


def next_month(value: datetime) -> datetime:
    if value.month == 12:
        return datetime(value.year + 1, 1, 1, tzinfo=UTC)
    return datetime(value.year, value.month + 1, 1, tzinfo=UTC)


def months() -> list[datetime]:
    values: list[datetime] = []
    current = START
    while current < END:
        values.append(current)
        current = next_month(current)
    return values


def raw_path(month: datetime, side: str) -> Path:
    return (
        RAW_DIR
        / str(month.year)
        / f"{month.month:02d}"
        / f"{side}_candles_hour_1.bi5"
    )


def source_url(base: str, month: datetime, side: str) -> str:
    source_month = month.month - 1
    return (
        f"{base}/{SYMBOL}/{month.year}/{source_month:02d}/"
        f"{side}_candles_hour_1.bi5"
    )


def fetch_bytes(url: str, timeout: int = 45) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
        headers = {
            "last_modified": response.headers.get("Last-Modified", ""),
            "etag": response.headers.get("ETag", ""),
        }
    if not body:
        raise ProtoDataError(f"empty response: {url}")
    return body, headers


def download_month(month: datetime, side: str) -> tuple[Path, dict[str, str]]:
    destination = raw_path(month, side)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size > 0:
        return destination, {
            "source_url": "LOCAL_FROZEN_COPY",
            "last_modified": "",
            "etag": "",
        }

    errors: list[str] = []
    for base in DOWNLOAD_BASES:
        url = source_url(base, month, side)
        for attempt in range(1, 4):
            try:
                body, headers = fetch_bytes(url)
                temporary = destination.with_suffix(destination.suffix + ".part")
                temporary.write_bytes(body)
                temporary.replace(destination)
                headers["source_url"] = url
                time.sleep(0.2)
                return destination, headers
            except (
                OSError,
                urllib.error.URLError,
                urllib.error.HTTPError,
                ProtoDataError,
            ) as exc:
                errors.append(f"{url} attempt {attempt}: {exc}")
                time.sleep(float(attempt))
    raise ProtoDataError(
        f"cannot download {side} {month:%Y-%m}; "
        + " | ".join(errors[-4:])
    )


def decode_month(
    path: Path,
    month: datetime,
) -> dict[datetime, tuple[float, float, float, float]]:
    try:
        raw = lzma.decompress(path.read_bytes())
    except lzma.LZMAError as exc:
        raise ProtoDataError(f"cannot decompress {path}: {exc}") from exc
    if len(raw) % RECORD.size:
        raise ProtoDataError(f"invalid decoded length for {path}")

    end = next_month(month)
    rows: dict[datetime, tuple[float, float, float, float]] = {}
    for offset in range(0, len(raw), RECORD.size):
        seconds, open_raw, close_raw, low_raw, high_raw, _ = RECORD.unpack_from(
            raw, offset
        )
        timestamp = month + timedelta(seconds=seconds)
        if not month <= timestamp < end:
            raise ProtoDataError(
                f"unexpected timestamp {timestamp.isoformat()} in {path}"
            )
        if timestamp in rows:
            raise ProtoDataError(f"duplicate timestamp in {path}: {timestamp}")

        values = (
            open_raw / PRICE_DIVISOR,
            high_raw / PRICE_DIVISOR,
            low_raw / PRICE_DIVISOR,
            close_raw / PRICE_DIVISOR,
        )
        open_price, high_price, low_price, close_price = values
        if min(values) <= 0:
            raise ProtoDataError(f"non-positive price in {path}: {timestamp}")
        if high_price < max(open_price, close_price):
            raise ProtoDataError(f"invalid high in {path}: {timestamp}")
        if low_price > min(open_price, close_price):
            raise ProtoDataError(f"invalid low in {path}: {timestamp}")
        rows[timestamp] = values
    return rows


def build_rows() -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    bid: dict[datetime, tuple[float, float, float, float]] = {}
    ask: dict[datetime, tuple[float, float, float, float]] = {}
    source_files: list[dict[str, str]] = []

    for month in months():
        for side, target in (("BID", bid), ("ASK", ask)):
            path, headers = download_month(month, side)
            decoded = decode_month(path, month)
            duplicates = set(target).intersection(decoded)
            if duplicates:
                raise ProtoDataError(
                    f"duplicate timestamp across source files: {min(duplicates)}"
                )
            target.update(decoded)
            source_files.append(
                {
                    "month": month.strftime("%Y-%m"),
                    "side": side,
                    "sha256": sha256_file(path),
                    "relative_path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "source_url": headers["source_url"],
                    "last_modified": headers["last_modified"],
                    "etag": headers["etag"],
                }
            )

    bid_times = {
        value
        for value in bid
        if START <= value < END and is_fx_market_hour(value)
    }
    ask_times = {
        value
        for value in ask
        if START <= value < END and is_fx_market_hour(value)
    }
    if bid_times != ask_times:
        raise ProtoDataError(
            "BID/ASK timestamps do not match exactly; "
            f"missing ASK={len(bid_times - ask_times)}, "
            f"missing BID={len(ask_times - bid_times)}"
        )

    timestamps = sorted(bid_times)
    if not timestamps:
        raise ProtoDataError("no aligned bars in the fixed period")

    rows: list[dict[str, Any]] = []
    for sequence, timestamp in enumerate(timestamps):
        bid_open, bid_high, bid_low, bid_close = bid[timestamp]
        ask_open, ask_high, ask_low, ask_close = ask[timestamp]
        if ask_open < bid_open:
            raise ProtoDataError(f"ASK open below BID open at {timestamp}")
        rows.append(
            {
                "event_time": iso_z(timestamp),
                "availability_time": iso_z(timestamp + timedelta(hours=1)),
                "sequence": sequence,
                "bid_open": bid_open,
                "bid_high": bid_high,
                "bid_low": bid_low,
                "bid_close": bid_close,
                "ask_open": ask_open,
                "ask_high": ask_high,
                "ask_low": ask_low,
                "ask_close": ask_close,
            }
        )
    return rows, source_files


def write_csv(rows: list[dict[str, Any]]) -> None:
    DERIVED_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DERIVED_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            formatted = dict(row)
            for key in (
                "bid_open",
                "bid_high",
                "bid_low",
                "bid_close",
                "ask_open",
                "ask_high",
                "ask_low",
                "ask_close",
            ):
                formatted[key] = f"{row[key]:.5f}"
            writer.writerow(formatted)


def parse_time(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def stats(rows: list[dict[str, Any]]) -> dict[str, Any]:
    timestamps = [parse_time(str(row["event_time"])) for row in rows]
    gaps = [
        int((current - previous).total_seconds() // 3600)
        for previous, current in zip(timestamps, timestamps[1:])
        if current - previous != timedelta(hours=1)
    ]
    eligible = 0
    for index in range(24, len(timestamps) - 25):
        window = timestamps[index - 24 : index + 26]
        if all(
            current - previous == timedelta(hours=1)
            for previous, current in zip(window, window[1:])
        ):
            eligible += 1
    calendar_hours = int((END - START).total_seconds() // 3600)
    expected_market_hours = sum(
        is_fx_market_hour(START + timedelta(hours=offset))
        for offset in range(calendar_hours)
    )
    return {
        "aligned_rows": len(rows),
        "coverage_start": iso_z(timestamps[0]),
        "coverage_end": iso_z(timestamps[-1]),
        "gap_count": len(gaps),
        "max_gap_hours": max(gaps, default=1),
        "eligible_primary_timestamps": eligible,
        "expected_market_hours": expected_market_hours,
        "closed_market_hours_excluded": calendar_hours - expected_market_hours,
        "missing_market_hours": expected_market_hours - len(rows),
    }


def bundle_hash(source_files: list[dict[str, str]]) -> str:
    text = "\n".join(
        f'{item["relative_path"]} {item["sha256"]}'
        for item in source_files
    )
    return sha256_bytes((text + "\n").encode("utf-8"))


def write_data_report(
    rows: list[dict[str, Any]],
    source_files: list[dict[str, str]],
) -> None:
    summary = stats(rows)
    lines = [
        "ATS PROTO-01 DATA PREPARATION REPORT",
        "====================================",
        f"Generated: {iso_z(datetime.now(UTC))}",
        f"Git commit: {git_head()}",
        "Prototype: HYP-0001 / PROTO-01",
        "Instrument: EURUSD",
        "Period: 2021-01-01 through 2025-12-31 UTC",
        "",
        "PREPARATION STATUS: PASS",
        f"Aligned tradable 1H rows: {summary['aligned_rows']}",
        f"Expected tradable 1H rows: {summary['expected_market_hours']}",
        f"Closed-market hours excluded: {summary['closed_market_hours_excluded']}",
        f"Missing tradable 1H rows: {summary['missing_market_hours']}",
        f"Coverage first bar: {summary['coverage_start']}",
        f"Coverage last bar: {summary['coverage_end']}",
        f"Detected session/data gaps: {summary['gap_count']}",
        f"Maximum gap hours: {summary['max_gap_hours']}",
        (
            "Eligible 24-before/24-after timestamps: "
            f"{summary['eligible_primary_timestamps']}"
        ),
        f"Prepared CSV: {DERIVED_PATH.relative_to(ROOT)}",
        f"Prepared CSV SHA256: {sha256_file(DERIVED_PATH)}",
        f"Source bundle SHA256: {bundle_hash(source_files)}",
        f"Source files: {len(source_files)}",
        "",
        "SOURCE FILE HASHES",
        "------------------",
    ]
    for item in source_files:
        lines.append(
            " | ".join(
                (
                    item["month"],
                    item["side"],
                    item["sha256"],
                    item["relative_path"],
                    item["source_url"],
                    item["last_modified"] or "NO_LAST_MODIFIED",
                    item["etag"] or "NO_ETAG",
                )
            )
        )
    lines.extend(
        (
            "",
            "NEXT STEP",
            "---------",
            "Upload this report to the ATS chat.",
            "Do not run the prototype result yet.",
            "The canonical Dataset Manifest must be committed first.",
        )
    )
    DATA_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:20]))
    print(f"\nFull report: {DATA_REPORT_PATH.relative_to(ROOT)}")


def prepare() -> int:
    if MANIFEST_PATH.exists():
        raise ProtoDataError(
            "canonical Dataset Manifest already exists; "
            "preparation must precede its commit"
        )
    rows, source_files = build_rows()
    write_csv(rows)
    write_data_report(rows, source_files)
    return 0


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.is_file():
        raise ProtoDataError(
            "Dataset Manifest is missing; prepare and review data first"
        )
    with MANIFEST_PATH.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ProtoDataError("Dataset Manifest is not a mapping")
    return data


def read_rows() -> list[dict[str, Any]]:
    if not DERIVED_PATH.is_file():
        raise ProtoDataError("prepared CSV is missing; run prepare first")
    rows: list[dict[str, Any]] = []
    with DERIVED_PATH.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            parsed: dict[str, Any] = {
                "event_time": parse_time(row["event_time"]),
                "availability_time": parse_time(row["availability_time"]),
                "sequence": int(row["sequence"]),
            }
            for key in (
                "bid_open",
                "bid_high",
                "bid_low",
                "bid_close",
                "ask_open",
                "ask_high",
                "ask_low",
                "ask_close",
            ):
                parsed[key] = float(row[key])
            rows.append(parsed)
    return rows


def valid_window(rows: list[dict[str, Any]], index: int) -> bool:
    window = rows[index - 24 : index + 26]
    return len(window) == 50 and all(
        current["event_time"] - previous["event_time"] == timedelta(hours=1)
        for previous, current in zip(window, window[1:])
    )


def evaluate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    baseline: list[float] = []
    signals: list[float] = []
    indices: list[int] = []

    for index in range(24, len(rows) - 25):
        if not valid_window(rows, index):
            continue
        value = rows[index + 25]["bid_open"] / rows[index + 1]["ask_open"] - 1
        baseline.append(value)
        prior_high = max(row["bid_high"] for row in rows[index - 24 : index])
        if rows[index]["bid_close"] > prior_high:
            signals.append(value)
            indices.append(index)

    if not baseline:
        raise ProtoDataError("no eligible baseline observations")
    if not signals:
        raise ProtoDataError("no qualifying breakout signals")

    overlaps = 0
    previous_exit: int | None = None
    for index in indices:
        entry = index + 1
        exit_index = index + 25
        if previous_exit is not None and entry <= previous_exit:
            overlaps += 1
        previous_exit = max(previous_exit or exit_index, exit_index)

    signal_mean = statistics.fmean(signals)
    baseline_mean = statistics.fmean(baseline)
    if len(signals) < MIN_SIGNAL_COUNT:
        decision = "PARK"
        reason = "FEWER_THAN_100_VALID_BREAKOUT_OBSERVATIONS"
    elif signal_mean > 0 and signal_mean > baseline_mean:
        decision = "ADVANCE_TO_ECONOMIC_SCREEN"
        reason = "BOTH_PRIMARY_HYPOTHESIS_INEQUALITIES_MET"
    else:
        decision = "REJECT"
        reason = "ONE_OR_BOTH_PRIMARY_HYPOTHESIS_INEQUALITIES_FAILED"

    return {
        "schema_version": "proto01-result-1",
        "hypothesis_id": "HYP-0001",
        "prototype_sequence": "PROTO-01",
        "evidence_class": "EXPLORATORY_PROTOTYPE",
        "economic_label": "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
        "metrics": {
            "aligned_bars": len(rows),
            "eligible_baseline_observations": len(baseline),
            "breakout_signal_count": len(signals),
            "signal_mean_return": signal_mean,
            "signal_median_return": statistics.median(signals),
            "signal_positive_share": sum(value > 0 for value in signals) / len(signals),
            "unconditional_mean_return": baseline_mean,
            "signal_minus_baseline": signal_mean - baseline_mean,
            "overlapping_signal_windows": overlaps,
            "overlapping_signal_share": overlaps / len(signals),
        },
        "decision": decision,
        "decision_reason": reason,
    }


def run_result() -> int:
    manifest = load_manifest()
    expected = manifest.get("integrity", {}).get("digest")
    actual = sha256_file(DERIVED_PATH)
    if expected != actual:
        raise ProtoDataError("prepared CSV does not match committed manifest")

    result = evaluate(read_rows())
    result["dataset"] = {
        "dataset_id": manifest.get("dataset_id"),
        "dataset_version": manifest.get("dataset_version"),
        "prepared_csv_sha256": actual,
    }
    result["run_context"] = {
        "git_commit": git_head(),
        "completed_at": iso_z(datetime.now(UTC)),
    }
    result["limitations"] = [
        "Commission is not modeled.",
        "Rollover/financing is not modeled.",
        "1H quote opens are not guaranteed live fills.",
        "Overlapping forward windows create dependent observations.",
        "This is exploratory prototype evidence, not validation evidence.",
    ]

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    metrics = result["metrics"]
    lines = [
        "ATS HYP-0001 PROTO-01 RESULT REPORT",
        "==================================",
        f"Git commit: {result['run_context']['git_commit']}",
        f"Breakout signals: {metrics['breakout_signal_count']}",
        f"Signal mean return: {metrics['signal_mean_return']:.10f}",
        f"Baseline mean return: {metrics['unconditional_mean_return']:.10f}",
        f"Signal minus baseline: {metrics['signal_minus_baseline']:.10f}",
        f"Decision: {result['decision']}",
        f"Reason: {result['decision_reason']}",
        "Economic label: QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
    ]
    RESULT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "run"))
    args = parser.parse_args()
    try:
        return prepare() if args.command == "prepare" else run_result()
    except ProtoDataError as exc:
        print(f"PROTO-01 BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
