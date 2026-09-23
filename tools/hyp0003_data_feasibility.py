#!/usr/bin/env python3
"""Probe Dukascopy H1 source availability for HYP-0003 without computing returns."""

from __future__ import annotations

import hashlib
import json
import lzma
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEARCH_FLOOR = datetime(1990, 1, 1, tzinfo=UTC)
PROTECTED_START = datetime(2021, 9, 1, tzinfo=UTC)
LAST_DEVELOPMENT_MONTH = datetime(2021, 8, 1, tzinfo=UTC)
MINIMUM_FEASIBLE_CURRENCIES = 6
RECORD = struct.Struct(">IIIIIf")
DOWNLOAD_BASES = (
    "https://datafeed.dukascopy.com/datafeed",
    "https://www.dukascopy.com/datafeed",
)
USER_AGENT = "ATS-Research/1.0"
PROBE_BATCH_BACKOFF_SECONDS = (5.0, 15.0, 30.0)
RAW_ROOT = ROOT / "data" / "external" / "dukascopy"
REPORT_JSON = ROOT / "reports" / "local_ci" / "HYP0003_DATA_FEASIBILITY.json"
REPORT_TEXT = ROOT / "reports" / "local_ci" / "HYP0003_DATA_FEASIBILITY_REPORT.txt"

CANDIDATES: dict[str, tuple[str, str]] = {
    "AUD": ("AUDUSD", "DIRECT"),
    "CAD": ("USDCAD", "INVERSE"),
    "CHF": ("USDCHF", "INVERSE"),
    "EUR": ("EURUSD", "DIRECT"),
    "GBP": ("GBPUSD", "DIRECT"),
    "JPY": ("USDJPY", "INVERSE"),
    "NOK": ("USDNOK", "INVERSE"),
    "NZD": ("NZDUSD", "DIRECT"),
    "SEK": ("USDSEK", "INVERSE"),
}


class ProbeError(RuntimeError):
    """Raised for technical failures that must not be treated as source absence."""


@dataclass(frozen=True)
class ProbeObject:
    symbol: str
    month: str
    side: str
    relative_path: str
    source_url: str
    sha256: str
    record_count: int
    first_timestamp: str
    last_timestamp: str


def git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def next_month(value: datetime) -> datetime:
    if value.month == 12:
        return datetime(value.year + 1, 1, 1, tzinfo=UTC)
    return datetime(value.year, value.month + 1, 1, tzinfo=UTC)


def previous_month(value: datetime) -> datetime:
    if value.month == 1:
        return datetime(value.year - 1, 12, 1, tzinfo=UTC)
    return datetime(value.year, value.month - 1, 1, tzinfo=UTC)


def month_number(value: datetime) -> int:
    return value.year * 12 + value.month - 1


def month_from_number(value: int) -> datetime:
    year, month_index = divmod(value, 12)
    return datetime(year, month_index + 1, 1, tzinfo=UTC)


def raw_path(symbol: str, month: datetime, side: str) -> Path:
    return (
        RAW_ROOT
        / symbol
        / "H1"
        / str(month.year)
        / f"{month.month:02d}"
        / f"{side}_candles_hour_1.bi5"
    )


def source_url(base: str, symbol: str, month: datetime, side: str) -> str:
    source_month = month.month - 1
    return (
        f"{base}/{symbol}/{month.year}/{source_month:02d}/"
        f"{side}_candles_hour_1.bi5"
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_bytes(url: str, timeout: int = 30) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            headers = {
                "last_modified": response.headers.get("Last-Modified", ""),
                "etag": response.headers.get("ETag", ""),
            }
    except urllib.error.HTTPError as exc:
        if exc.code in {404, 410}:
            raise FileNotFoundError(url) from exc
        raise ProbeError(f"HTTP {exc.code} while probing {url}") from exc
    except urllib.error.URLError as exc:
        raise ProbeError(f"network error while probing {url}: {exc}") from exc
    if not body:
        raise ProbeError(f"empty source object: {url}")
    return body, headers


def download_probe(
    symbol: str,
    month: datetime,
    side: str,
) -> tuple[Path, dict[str, str]] | None:
    if month >= PROTECTED_START:
        raise ProbeError("protected-tail source month requested by RF-006")

    destination = raw_path(symbol, month, side)
    if destination.exists() and destination.stat().st_size > 0:
        return destination, {
            "source_url": "LOCAL_FROZEN_COPY",
            "last_modified": "",
            "etag": "",
        }

    missing_count = 0
    technical_errors: list[str] = []
    for base in DOWNLOAD_BASES:
        url = source_url(base, symbol, month, side)
        for attempt in range(1, 4):
            try:
                body, headers = fetch_bytes(url)
                destination.parent.mkdir(parents=True, exist_ok=True)
                temporary = destination.with_suffix(destination.suffix + ".part")
                temporary.write_bytes(body)
                temporary.replace(destination)
                headers["source_url"] = url
                return destination, headers
            except FileNotFoundError:
                missing_count += 1
                break
            except ProbeError as exc:
                technical_errors.append(f"{url} attempt {attempt}: {exc}")
                if attempt < 3:
                    time.sleep(float(attempt))

    if technical_errors:
        raise ProbeError(" | ".join(technical_errors[-4:]))
    if missing_count == len(DOWNLOAD_BASES):
        return None
    raise ProbeError(f"indeterminate source state for {symbol} {month:%Y-%m} {side}")


def inspect_probe(
    symbol: str,
    month: datetime,
    side: str,
    path: Path,
    source: dict[str, str],
) -> ProbeObject:
    try:
        decoded = lzma.decompress(path.read_bytes())
    except lzma.LZMAError as exc:
        raise ProbeError(f"cannot decompress {path}") from exc
    if not decoded or len(decoded) % RECORD.size:
        raise ProbeError(f"invalid BI5 record length: {path}")

    record_count = len(decoded) // RECORD.size
    first_seconds = RECORD.unpack_from(decoded, 0)[0]
    last_seconds = RECORD.unpack_from(decoded, len(decoded) - RECORD.size)[0]
    end = next_month(month)
    month_seconds = int((end - month).total_seconds())
    if not 0 <= first_seconds <= last_seconds < month_seconds:
        raise ProbeError(f"invalid BI5 timestamp offsets: {path}")

    return ProbeObject(
        symbol=symbol,
        month=month.strftime("%Y-%m"),
        side=side,
        relative_path=str(path.relative_to(ROOT)).replace("\\", "/"),
        source_url=source["source_url"],
        sha256=sha256_file(path),
        record_count=record_count,
        first_timestamp=iso_z(month + timedelta(seconds=first_seconds)),
        last_timestamp=iso_z(month + timedelta(seconds=last_seconds)),
    )


def probe_side(symbol: str, month: datetime, side: str) -> ProbeObject | None:
    downloaded = download_probe(symbol, month, side)
    if downloaded is None:
        return None
    path, source = downloaded
    return inspect_probe(symbol, month, side, path, source)


def probe_side_resilient(symbol: str, month: datetime, side: str) -> ProbeObject | None:
    attempts = len(PROBE_BATCH_BACKOFF_SECONDS) + 1
    last_error: ProbeError | None = None
    for batch in range(attempts):
        try:
            return probe_side(symbol, month, side)
        except ProbeError as exc:
            last_error = exc
            if batch == attempts - 1:
                break
            delay = PROBE_BATCH_BACKOFF_SECONDS[batch]
            print(
                f"Dukascopy probe batch failed for {symbol} {month:%Y-%m} {side}; "
                f"retrying in {delay:.0f}s",
                file=sys.stderr,
            )
            time.sleep(delay)
    raise ProbeError(
        f"cannot classify {symbol} {month:%Y-%m} {side} "
        f"after {attempts} probe batches: {last_error}"
    )


def probe_month(symbol: str, month: datetime) -> tuple[ProbeObject, ProbeObject] | None:
    bid = probe_side_resilient(symbol, month, "BID")
    ask = probe_side_resilient(symbol, month, "ASK")
    if bid is None and ask is None:
        return None
    if bid is None or ask is None:
        raise ProbeError(f"one-sided H1 source availability: {symbol} {month:%Y-%m}")
    return bid, ask


def find_first_available_month(symbol: str) -> tuple[datetime, ProbeObject, ProbeObject] | None:
    if probe_month(symbol, LAST_DEVELOPMENT_MONTH) is None:
        return None

    low = month_number(SEARCH_FLOOR)
    high = month_number(LAST_DEVELOPMENT_MONTH)
    while low < high:
        middle = (low + high) // 2
        month = month_from_number(middle)
        if probe_month(symbol, month) is None:
            low = middle + 1
        else:
            high = middle

    first_month = month_from_number(low)
    first_pair = probe_month(symbol, first_month)
    if first_pair is None:
        raise ProbeError(f"binary availability search failed for {symbol}")

    if first_month == SEARCH_FLOOR:
        raise ProbeError(f"search floor is too recent for {symbol}")

    prior = previous_month(first_month)
    if probe_month(symbol, prior) is not None:
        raise ProbeError(f"availability is not monotonic around first month for {symbol}")

    return first_month, first_pair[0], first_pair[1]


def normalized_bid_ask(
    source_bid: float,
    source_ask: float,
    orientation: str,
) -> tuple[float, float]:
    if source_bid <= 0 or source_ask <= 0 or source_ask < source_bid:
        raise ValueError("invalid source BID/ASK")
    if orientation == "DIRECT":
        return source_bid, source_ask
    if orientation == "INVERSE":
        return 1.0 / source_ask, 1.0 / source_bid
    raise ValueError(f"unknown quote orientation: {orientation}")


def probe_bundle_hash(objects: list[ProbeObject]) -> str:
    payload = [
        {
            "symbol": item.symbol,
            "month": item.month,
            "side": item.side,
            "sha256": item.sha256,
            "record_count": item.record_count,
            "first_timestamp": item.first_timestamp,
            "last_timestamp": item.last_timestamp,
        }
        for item in sorted(objects, key=lambda item: (item.symbol, item.month, item.side))
    ]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def prepare() -> dict[str, Any]:
    symbol_results: list[dict[str, Any]] = []
    probe_objects: list[ProbeObject] = []
    retained: list[str] = []
    first_usable_times: list[datetime] = []

    for currency, (symbol, orientation) in CANDIDATES.items():
        print(f"Probing {currency} via {symbol}...")
        first = find_first_available_month(symbol)
        last_pair = probe_month(symbol, LAST_DEVELOPMENT_MONTH)

        if first is None or last_pair is None:
            symbol_results.append(
                {
                    "currency": currency,
                    "symbol": symbol,
                    "orientation": orientation,
                    "status": "SOURCE_UNAVAILABLE_AT_DEVELOPMENT_BOUNDARY",
                }
            )
            continue

        first_month, first_bid, first_ask = first
        last_bid, last_ask = last_pair
        objects = [first_bid, first_ask, last_bid, last_ask]
        probe_objects.extend(objects)

        first_usable = max(
            datetime.strptime(first_bid.first_timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=UTC
            ),
            datetime.strptime(first_ask.first_timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=UTC
            ),
        )
        retained.append(currency)
        first_usable_times.append(first_usable)
        symbol_results.append(
            {
                "currency": currency,
                "symbol": symbol,
                "orientation": orientation,
                "status": "SOURCE_AVAILABLE",
                "first_available_month": first_month.strftime("%Y-%m"),
                "first_usable_timestamp": iso_z(first_usable),
                "first_probe": {
                    "bid": first_bid.__dict__,
                    "ask": first_ask.__dict__,
                },
                "last_development_probe": {
                    "bid": last_bid.__dict__,
                    "ask": last_ask.__dict__,
                },
            }
        )

    common_start = max(first_usable_times) if first_usable_times else None
    decision = (
        "READY_FOR_FREEZE_REVIEW"
        if len(retained) >= MINIMUM_FEASIBLE_CURRENCIES and common_start is not None
        else "INSUFFICIENT_SOURCE_UNIVERSE"
    )
    return {
        "schema_version": "hyp0003-data-feasibility-probe-1",
        "hypothesis_id": "HYP-0003",
        "git_commit": git_head(),
        "candidate_currencies": list(CANDIDATES),
        "retained_source_currencies": retained,
        "retained_currency_count": len(retained),
        "minimum_required_currency_count": MINIMUM_FEASIBLE_CURRENCIES,
        "common_possible_development_start": iso_z(common_start) if common_start else None,
        "development_end_exclusive": iso_z(PROTECTED_START),
        "protected_tail_start": iso_z(PROTECTED_START),
        "probe_bundle_sha256": probe_bundle_hash(probe_objects) if probe_objects else None,
        "probe_object_count": len(probe_objects),
        "symbol_results": symbol_results,
        "preparation_decision": decision,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "ATS HYP-0003 DATA FEASIBILITY PREPARATION",
        "=========================================",
        f"Git commit: {payload['git_commit']}",
        "Hypothesis: HYP-0003",
        f"Preparation decision: {payload['preparation_decision']}",
        (
            "Retained source currencies: "
            + ", ".join(payload["retained_source_currencies"])
        ),
        f"Retained currency count: {payload['retained_currency_count']}",
        f"Minimum required: {payload['minimum_required_currency_count']}",
        (
            "Common possible development start: "
            f"{payload['common_possible_development_start']}"
        ),
        f"Development end exclusive: {payload['development_end_exclusive']}",
        f"Probe objects: {payload['probe_object_count']}",
        f"Probe bundle SHA256: {payload['probe_bundle_sha256']}",
        "Information boundary: NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "",
        "SYMBOL AVAILABILITY",
        "-------------------",
    ]
    for item in payload["symbol_results"]:
        summary = f"{item['currency']} {item['symbol']}: {item['status']}"
        if "first_available_month" in item:
            summary += (
                f"; first_month={item['first_available_month']}; "
                f"first_usable={item['first_usable_timestamp']}"
            )
        lines.append(summary)

    lines += [
        "",
        "NEXT STEP",
        "---------",
        "Send CURRENT_TASK_REPORT.txt to ChatGPT.",
        "Do not run any HYP-0003 momentum development calculation yet.",
    ]
    REPORT_TEXT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main() -> int:
    try:
        payload = prepare()
        write_reports(payload)
    except (OSError, ProbeError, ValueError) as exc:
        print(f"HYP-0003 DATA FEASIBILITY PREP BLOCKED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
