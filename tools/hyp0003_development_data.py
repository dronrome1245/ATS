#!/usr/bin/env python3
"""Prepare the full HYP-0003 development dataset without computing momentum outcomes."""

from __future__ import annotations

import csv
import hashlib
import json
import lzma
import math
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_START = datetime(2003, 8, 3, 21, tzinfo=UTC)
DATA_END = datetime(2021, 9, 1, tzinfo=UTC)
FIRST_SOURCE_MONTH = datetime(2003, 8, 1, tzinfo=UTC)
LAST_SOURCE_MONTH = datetime(2021, 8, 1, tzinfo=UTC)
MINIMUM_ELIGIBLE_CURRENCIES = 6
RECORD = struct.Struct(">IIIIIf")
DOWNLOAD_BASES = (
    "https://datafeed.dukascopy.com/datafeed",
    "https://www.dukascopy.com/datafeed",
)
JETTA_API_ROOT = "https://jetta.dukascopy.com/v1"
SOURCE_FORMAT_BI5 = "BI5"
SOURCE_FORMAT_JETTA_JSON = "JETTA_JSON"
JETTA_OHLC_TOLERANCE_UNITS = 1
USER_AGENT = "ATS-Research/1.0"
DOWNLOAD_BATCH_BACKOFF_SECONDS = (5.0, 15.0, 30.0)
SUCCESS_THROTTLE_SECONDS = 0.10
RAW_ROOT = ROOT / "data" / "external" / "dukascopy"
DERIVED_PATH = ROOT / "data" / "derived" / "HYP-0003-DEV-01-G10EXUSD-H1.csv"
REPORT_JSON = ROOT / "reports" / "local_ci" / "HYP0003_DEVELOPMENT_DATA.json"
REPORT_TEXT = ROOT / "reports" / "local_ci" / "HYP0003_DEVELOPMENT_DATA_REPORT.txt"
RF006_RESULT_PATH = ROOT / "reports" / "research" / "HYP-0003-DATA-FEASIBILITY-PREP-result.json"
DATASET_ID = "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001"
DATASET_VERSION = "1.0.0"
EXPECTED_PROBE_BUNDLE_SHA256 = "a88add123fd42e83396ba17de13cf65fedf18d8e0a5e1eca476ed6338c91b45e"

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
POINT_DIVISORS = {
    "AUDUSD": 100_000,
    "USDCAD": 100_000,
    "USDCHF": 100_000,
    "EURUSD": 100_000,
    "GBPUSD": 100_000,
    "USDJPY": 1_000,
    "USDNOK": 100_000,
    "NZDUSD": 100_000,
    "USDSEK": 100_000,
}
FIELDNAMES = (
    "event_time",
    "availability_time",
    "currency",
    "source_symbol",
    "source_orientation",
    "sequence",
    "bid_open",
    "bid_high",
    "bid_low",
    "bid_close",
    "ask_open",
    "ask_high",
    "ask_low",
    "ask_close",
)

Ohlc = tuple[float, float, float, float]
NormalizedPair = tuple[Ohlc, Ohlc]


class DevelopmentDataPrepError(RuntimeError):
    """Raised when RF-008 cannot honestly prepare the frozen development dataset."""


def progress(message: str) -> None:
    print(message, flush=True)


def emit_progress(percent: int) -> None:
    print(f"@@PROGRESS {percent}", flush=True)


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


def shift_months(value: datetime, months: int) -> datetime:
    index = value.year * 12 + value.month - 1 + months
    year, month_index = divmod(index, 12)
    return datetime(year, month_index + 1, value.day, value.hour, tzinfo=UTC)


def development_months() -> list[datetime]:
    values: list[datetime] = []
    current = FIRST_SOURCE_MONTH
    while current <= LAST_SOURCE_MONTH:
        values.append(current)
        current = next_month(current)
    return values


def nth_weekday_of_month(year: int, month: int, weekday: int, occurrence: int) -> int:
    first = datetime(year, month, 1, tzinfo=UTC)
    offset = (weekday - first.weekday()) % 7
    return 1 + offset + 7 * (occurrence - 1)


def us_dst_active_utc(value: datetime) -> bool:
    year = value.year
    march_sunday = nth_weekday_of_month(year, 3, 6, 2)
    november_sunday = nth_weekday_of_month(year, 11, 6, 1)
    start = datetime(year, 3, march_sunday, 7, tzinfo=UTC)
    end = datetime(year, 11, november_sunday, 6, tzinfo=UTC)
    return start <= value < end


def is_fx_market_hour(value: datetime) -> bool:
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


def monthly_cutoff(month: datetime) -> datetime:
    candidate = next_month(month) - timedelta(hours=1)
    while candidate >= month:
        if is_fx_market_hour(candidate):
            return candidate
        candidate -= timedelta(hours=1)
    raise DevelopmentDataPrepError(f"no expected market hour in {month:%Y-%m}")


def supports_longest_12_12_geometry(month: datetime) -> bool:
    ranking_anchor = next_month(month)
    formation_start = shift_months(ranking_anchor, -12)
    holding_end = shift_months(ranking_anchor, 12)
    return formation_start >= DATA_START and holding_end < DATA_END


def raw_path(symbol: str, month: datetime, side: str) -> Path:
    return (
        RAW_ROOT
        / symbol
        / "H1"
        / str(month.year)
        / f"{month.month:02d}"
        / f"{side}_candles_hour_1.bi5"
    )


def jetta_raw_path(symbol: str, month: datetime, side: str) -> Path:
    return (
        RAW_ROOT
        / symbol
        / "H1"
        / str(month.year)
        / f"{month.month:02d}"
        / f"{side}_candles_hour_1.json"
    )


def source_url(base: str, symbol: str, month: datetime, side: str) -> str:
    source_month = month.month - 1
    return f"{base}/{symbol}/{month.year}/{source_month:02d}/{side}_candles_hour_1.bi5"


def jetta_instrument_code(symbol: str) -> str:
    if len(symbol) != 6 or not symbol.isalpha():
        raise DevelopmentDataPrepError(f"invalid FX symbol for Jetta API: {symbol}")
    return f"{symbol[:3]}-{symbol[3:]}"


def jetta_source_url(symbol: str, month: datetime, side: str) -> str:
    instrument = jetta_instrument_code(symbol)
    return f"{JETTA_API_ROOT}/candles/hour/{instrument}/{side}/{month.year}/{month.month}"


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
        raise DevelopmentDataPrepError(f"HTTP {exc.code} while fetching {url}") from exc
    except (urllib.error.URLError, OSError) as exc:
        raise DevelopmentDataPrepError(f"network error while fetching {url}: {exc}") from exc
    if not body:
        raise DevelopmentDataPrepError(f"empty source object: {url}")
    return body, headers


def download_jetta_source_once(
    symbol: str,
    month: datetime,
    side: str,
) -> tuple[Path, dict[str, str]] | None:
    destination = jetta_raw_path(symbol, month, side)
    if destination.exists() and destination.stat().st_size > 0:
        return destination, {
            "source_url": "LOCAL_FROZEN_COPY",
            "source_format": SOURCE_FORMAT_JETTA_JSON,
            "last_modified": "",
            "etag": "",
        }

    url = jetta_source_url(symbol, month, side)
    try:
        body, headers = fetch_bytes(url)
    except FileNotFoundError:
        return None

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    temporary.write_bytes(body)
    temporary.replace(destination)
    headers["source_url"] = url
    headers["source_format"] = SOURCE_FORMAT_JETTA_JSON
    if SUCCESS_THROTTLE_SECONDS:
        time.sleep(SUCCESS_THROTTLE_SECONDS)
    return destination, headers


def download_legacy_source_once(
    symbol: str,
    month: datetime,
    side: str,
) -> tuple[Path, dict[str, str]] | None:
    destination = raw_path(symbol, month, side)
    if destination.exists() and destination.stat().st_size > 0:
        return destination, {
            "source_url": "LOCAL_FROZEN_COPY",
            "source_format": SOURCE_FORMAT_BI5,
            "last_modified": "",
            "etag": "",
        }

    missing = 0
    technical_errors: list[str] = []
    for base in DOWNLOAD_BASES:
        url = source_url(base, symbol, month, side)
        try:
            body, headers = fetch_bytes(url)
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_suffix(destination.suffix + ".part")
            temporary.write_bytes(body)
            temporary.replace(destination)
            headers["source_url"] = url
            headers["source_format"] = SOURCE_FORMAT_BI5
            if SUCCESS_THROTTLE_SECONDS:
                time.sleep(SUCCESS_THROTTLE_SECONDS)
            return destination, headers
        except FileNotFoundError:
            missing += 1
        except DevelopmentDataPrepError as exc:
            technical_errors.append(f"{url}: {exc}")

    if technical_errors:
        raise DevelopmentDataPrepError(" | ".join(technical_errors[-2:]))
    if missing == len(DOWNLOAD_BASES):
        return None
    raise DevelopmentDataPrepError(f"indeterminate source state for {symbol} {month:%Y-%m} {side}")


def download_source_once(
    symbol: str,
    month: datetime,
    side: str,
) -> tuple[Path, dict[str, str]] | None:
    if month >= DATA_END:
        raise DevelopmentDataPrepError("protected-tail source month requested by RF-008")

    jetta_cache = jetta_raw_path(symbol, month, side)
    legacy_cache = raw_path(symbol, month, side)
    if jetta_cache.exists() and jetta_cache.stat().st_size > 0:
        return download_jetta_source_once(symbol, month, side)
    if legacy_cache.exists() and legacy_cache.stat().st_size > 0:
        return download_legacy_source_once(symbol, month, side)

    jetta_error: DevelopmentDataPrepError | None = None
    try:
        jetta = download_jetta_source_once(symbol, month, side)
    except DevelopmentDataPrepError as exc:
        jetta_error = exc
    else:
        if jetta is not None:
            return jetta

    legacy_error: DevelopmentDataPrepError | None = None
    try:
        legacy = download_legacy_source_once(symbol, month, side)
    except DevelopmentDataPrepError as exc:
        legacy_error = exc
    else:
        if legacy is not None:
            return legacy

    if jetta_error is None and legacy_error is None:
        return None

    errors = [
        f"Jetta: {jetta_error}" if jetta_error is not None else "",
        f"legacy BI5: {legacy_error}" if legacy_error is not None else "",
    ]
    detail = " | ".join(item for item in errors if item)
    raise DevelopmentDataPrepError(f"all Dukascopy source paths failed: {detail}")


def download_source_resilient(
    symbol: str,
    month: datetime,
    side: str,
) -> tuple[Path, dict[str, str]] | None:
    attempts = len(DOWNLOAD_BATCH_BACKOFF_SECONDS) + 1
    last_error: DevelopmentDataPrepError | None = None
    for batch in range(attempts):
        try:
            return download_source_once(symbol, month, side)
        except DevelopmentDataPrepError as exc:
            last_error = exc
            if batch == attempts - 1:
                break
            delay = DOWNLOAD_BATCH_BACKOFF_SECONDS[batch]
            progress(
                f"[network] {symbol} {month:%Y-%m} {side} failed; "
                f"retrying in {delay:.0f}s (batch {batch + 2}/{attempts})"
            )
            time.sleep(delay)
    raise DevelopmentDataPrepError(
        f"cannot acquire {symbol} {month:%Y-%m} {side} after {attempts} batches: {last_error}"
    )


def _nonempty(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def _source_format_priority(symbol: str, month: datetime) -> tuple[str, str]:
    jetta_cached = any(_nonempty(jetta_raw_path(symbol, month, side)) for side in ("BID", "ASK"))
    legacy_cached = any(_nonempty(raw_path(symbol, month, side)) for side in ("BID", "ASK"))
    if legacy_cached and not jetta_cached:
        return SOURCE_FORMAT_BI5, SOURCE_FORMAT_JETTA_JSON
    return SOURCE_FORMAT_JETTA_JSON, SOURCE_FORMAT_BI5


def download_source_pair_from_format(
    symbol: str,
    month: datetime,
    source_format: str,
) -> dict[str, tuple[Path, dict[str, str]]] | None:
    if source_format == SOURCE_FORMAT_JETTA_JSON:
        downloader = download_jetta_source_once
    elif source_format == SOURCE_FORMAT_BI5:
        downloader = download_legacy_source_once
    else:
        raise DevelopmentDataPrepError(f"unknown pair source format: {source_format}")

    result: dict[str, tuple[Path, dict[str, str]]] = {}
    missing: list[str] = []
    for side in ("BID", "ASK"):
        downloaded = downloader(symbol, month, side)
        if downloaded is None:
            missing.append(side)
        else:
            result[side] = downloaded

    if not missing:
        return result
    if len(missing) == 2:
        return None
    raise DevelopmentDataPrepError(
        f"one-sided {source_format} source absence for {symbol} {month:%Y-%m}: missing {missing[0]}"
    )


def download_source_pair_once(
    symbol: str,
    month: datetime,
) -> dict[str, tuple[Path, dict[str, str]]] | None:
    if month >= DATA_END:
        raise DevelopmentDataPrepError("protected-tail source month requested by RF-008")

    errors: list[str] = []
    for source_format in _source_format_priority(symbol, month):
        try:
            pair = download_source_pair_from_format(symbol, month, source_format)
        except DevelopmentDataPrepError as exc:
            errors.append(f"{source_format}: {exc}")
            continue
        if pair is not None:
            return pair

    if errors:
        raise DevelopmentDataPrepError(
            "coherent BID/ASK source pair unavailable: " + " | ".join(errors)
        )
    return None


def download_source_pair_resilient(
    symbol: str,
    month: datetime,
) -> dict[str, tuple[Path, dict[str, str]]] | None:
    attempts = len(DOWNLOAD_BATCH_BACKOFF_SECONDS) + 1
    last_error: DevelopmentDataPrepError | None = None
    for batch in range(attempts):
        try:
            return download_source_pair_once(symbol, month)
        except DevelopmentDataPrepError as exc:
            last_error = exc
            if batch == attempts - 1:
                break
            delay = DOWNLOAD_BATCH_BACKOFF_SECONDS[batch]
            progress(
                f"[network] coherent {symbol} {month:%Y-%m} BID/ASK pair failed; "
                f"retrying in {delay:.0f}s (batch {batch + 2}/{attempts})"
            )
            time.sleep(delay)
    raise DevelopmentDataPrepError(
        f"cannot acquire coherent {symbol} {month:%Y-%m} BID/ASK pair "
        f"after {attempts} batches: {last_error}"
    )


def decode_month(
    path: Path,
    month: datetime,
    point_divisor: int,
) -> dict[datetime, Ohlc]:
    try:
        raw = lzma.decompress(path.read_bytes())
    except lzma.LZMAError as exc:
        raise DevelopmentDataPrepError(f"cannot decompress {path}") from exc
    if not raw or len(raw) % RECORD.size:
        raise DevelopmentDataPrepError(f"invalid decoded BI5 length: {path}")

    end = next_month(month)
    rows: dict[datetime, Ohlc] = {}
    previous_timestamp: datetime | None = None
    for offset in range(0, len(raw), RECORD.size):
        seconds, open_raw, close_raw, low_raw, high_raw, _volume = RECORD.unpack_from(raw, offset)
        timestamp = month + timedelta(seconds=seconds)
        if not month <= timestamp < end:
            raise DevelopmentDataPrepError(
                f"unexpected timestamp {timestamp.isoformat()} in {path}"
            )
        if timestamp in rows:
            raise DevelopmentDataPrepError(f"duplicate timestamp in {path}: {timestamp}")
        if previous_timestamp is not None and timestamp < previous_timestamp:
            raise DevelopmentDataPrepError(f"out-of-order timestamp in {path}: {timestamp}")
        previous_timestamp = timestamp

        values = (
            open_raw / point_divisor,
            high_raw / point_divisor,
            low_raw / point_divisor,
            close_raw / point_divisor,
        )
        open_price, high_price, low_price, close_price = values
        if not all(math.isfinite(value) and value > 0 for value in values):
            raise DevelopmentDataPrepError(f"non-positive/non-finite price in {path}")
        if high_price < max(open_price, close_price) or high_price < low_price:
            raise DevelopmentDataPrepError(f"invalid high in {path}: {timestamp}")
        if low_price > min(open_price, close_price):
            raise DevelopmentDataPrepError(f"invalid low in {path}: {timestamp}")
        rows[timestamp] = values
    return rows


def multiplier_scale(multiplier: float) -> int:
    exponent = Decimal(str(multiplier)).as_tuple().exponent
    return max(0, -int(exponent))


def jetta_ohlc_units_are_valid(units: list[int]) -> bool:
    open_units, high_units, low_units, close_units = units
    tolerance = JETTA_OHLC_TOLERANCE_UNITS
    return (
        high_units + tolerance >= max(open_units, close_units)
        and high_units + tolerance >= low_units
        and low_units - tolerance <= min(open_units, close_units)
    )


def decode_jetta_month(path: Path, month: datetime) -> dict[datetime, Ohlc]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DevelopmentDataPrepError(f"cannot decode Jetta JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise DevelopmentDataPrepError(f"invalid Jetta payload type: {path}")

    columns = ("times", "opens", "highs", "lows", "closes", "volumes")
    if any(not isinstance(payload.get(name), list) for name in columns):
        raise DevelopmentDataPrepError(f"invalid Jetta columns: {path}")

    length = len(payload["times"])
    if any(len(payload[name]) != length for name in columns[1:]):
        raise DevelopmentDataPrepError(f"mismatched Jetta column lengths: {path}")
    if length == 0:
        return {}

    multiplier = payload.get("multiplier")
    shift = payload.get("shift")
    timestamp_ms = payload.get("timestamp")
    base_values = [payload.get(name) for name in ("open", "high", "low", "close")]
    if not isinstance(multiplier, (int, float)) or not math.isfinite(multiplier) or multiplier <= 0:
        raise DevelopmentDataPrepError(f"invalid Jetta multiplier: {path}")
    if shift != 3_600_000:
        raise DevelopmentDataPrepError(f"unexpected Jetta H1 shift: {path}")
    if not isinstance(timestamp_ms, int):
        raise DevelopmentDataPrepError(f"invalid Jetta timestamp: {path}")
    if any(
        not isinstance(value, (int, float)) or not math.isfinite(value) for value in base_values
    ):
        raise DevelopmentDataPrepError(f"invalid Jetta base candle: {path}")

    deltas = [payload[name] for name in ("opens", "highs", "lows", "closes")]
    if any(not isinstance(value, int) for column in deltas for value in column):
        raise DevelopmentDataPrepError(f"non-integer Jetta price delta: {path}")

    scale = multiplier_scale(float(multiplier))
    units = [round(float(value) / float(multiplier)) for value in base_values]
    end = next_month(month)
    rows: dict[datetime, Ohlc] = {}
    previous_timestamp: datetime | None = None

    for index, time_delta in enumerate(payload["times"]):
        if not isinstance(time_delta, int) or time_delta < 0:
            raise DevelopmentDataPrepError(f"invalid Jetta time delta: {path}")
        timestamp_ms += time_delta * shift
        for field_index, column in enumerate(deltas):
            units[field_index] += int(column[index])

        timestamp = datetime.fromtimestamp(timestamp_ms / 1000.0, tz=UTC)
        if not month <= timestamp < end:
            raise DevelopmentDataPrepError(
                f"unexpected Jetta timestamp {timestamp.isoformat()} in {path}"
            )
        if timestamp in rows:
            raise DevelopmentDataPrepError(f"duplicate Jetta timestamp in {path}: {timestamp}")
        if previous_timestamp is not None and timestamp < previous_timestamp:
            raise DevelopmentDataPrepError(f"out-of-order Jetta timestamp in {path}: {timestamp}")
        previous_timestamp = timestamp

        values = tuple(round(value * float(multiplier), scale) for value in units)
        if not all(math.isfinite(value) and value > 0 for value in values):
            raise DevelopmentDataPrepError(f"invalid Jetta price in {path}: {timestamp}")
        if not jetta_ohlc_units_are_valid(units):
            raise DevelopmentDataPrepError(f"invalid Jetta OHLC geometry in {path}: {timestamp}")
        rows[timestamp] = values

    return rows


def decode_source_object(
    path: Path,
    month: datetime,
    symbol: str,
    source_format: str,
) -> dict[datetime, Ohlc]:
    if source_format == SOURCE_FORMAT_JETTA_JSON:
        return decode_jetta_month(path, month)
    if source_format == SOURCE_FORMAT_BI5:
        return decode_month(path, month, POINT_DIVISORS[symbol])
    raise DevelopmentDataPrepError(f"unknown source format: {source_format}")


def invert_ohlc(values: Ohlc) -> Ohlc:
    open_price, high_price, low_price, close_price = values
    return (
        1.0 / open_price,
        1.0 / low_price,
        1.0 / high_price,
        1.0 / close_price,
    )


def normalize_pair_ohlc(
    source_bid: Ohlc,
    source_ask: Ohlc,
    orientation: str,
) -> NormalizedPair:
    if orientation == "DIRECT":
        bid, ask = source_bid, source_ask
    elif orientation == "INVERSE":
        bid, ask = invert_ohlc(source_ask), invert_ohlc(source_bid)
    else:
        raise DevelopmentDataPrepError(f"unknown source orientation: {orientation}")

    for label, values in (("BID", bid), ("ASK", ask)):
        open_price, high_price, low_price, close_price = values
        if not all(math.isfinite(value) and value > 0 for value in values):
            raise DevelopmentDataPrepError(f"normalized {label} has invalid price")
        if high_price < max(open_price, close_price) or high_price < low_price:
            raise DevelopmentDataPrepError(f"normalized {label} has invalid high")
        if low_price > min(open_price, close_price):
            raise DevelopmentDataPrepError(f"normalized {label} has invalid low")
    return bid, ask


def source_bundle_hash(source_files: list[dict[str, str]]) -> str:
    payload = [
        {
            "symbol": item["symbol"],
            "month": item["month"],
            "side": item["side"],
            "sha256": item["sha256"],
        }
        for item in sorted(
            source_files,
            key=lambda item: (
                item["symbol"],
                item["month"],
                item["side"],
            ),
        )
    ]
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def expected_market_times(month: datetime) -> list[datetime]:
    start = max(month, DATA_START)
    end = min(next_month(month), DATA_END)
    if start >= end:
        return []
    first_hour = start.replace(minute=0, second=0, microsecond=0)
    if first_hour < start:
        first_hour += timedelta(hours=1)
    hours = int((end - first_hour).total_seconds() // 3600)
    return [
        first_hour + timedelta(hours=offset)
        for offset in range(hours)
        if is_fx_market_hour(first_hour + timedelta(hours=offset))
    ]


def load_frozen_rf006_result() -> dict[str, Any]:
    try:
        payload = json.loads(RF006_RESULT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DevelopmentDataPrepError(f"cannot load frozen RF-006 result: {exc}") from exc

    checks = {
        "preparation_decision": "READY_FOR_FREEZE_REVIEW",
        "retained_source_currencies": list(CANDIDATES),
        "retained_currency_count": len(CANDIDATES),
        "common_possible_development_start": iso_z(DATA_START),
        "development_end_exclusive": iso_z(DATA_END),
        "probe_bundle_sha256": EXPECTED_PROBE_BUNDLE_SHA256,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    }
    for key, expected in checks.items():
        if payload.get(key) != expected:
            raise DevelopmentDataPrepError(
                f"frozen RF-006 result mismatch for {key}: {payload.get(key)!r}"
            )
    return payload


def empty_symbol_stats(
    currency: str,
    symbol: str,
    orientation: str,
) -> dict[str, Any]:
    return {
        "currency": currency,
        "symbol": symbol,
        "orientation": orientation,
        "aligned_rows": 0,
        "expected_market_hours": 0,
        "missing_market_hours": 0,
        "cutoff_eligible_months": 0,
        "cutoff_ineligible_missing_months": 0,
        "first_usable_timestamp": None,
        "last_usable_timestamp": None,
        "duplicate_count": 0,
        "out_of_order_count": 0,
        "malformed_count": 0,
        "impossible_quote_count": 0,
    }


def build_dataset() -> dict[str, Any]:
    load_frozen_rf006_result()
    months = development_months()
    source_files: list[dict[str, str]] = []
    missing_source_objects: list[dict[str, str]] = []
    symbol_stats = {
        currency: empty_symbol_stats(currency, symbol, orientation)
        for currency, (symbol, orientation) in CANDIDATES.items()
    }
    monthly_points: list[dict[str, Any]] = []

    DERIVED_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = DERIVED_PATH.with_suffix(DERIVED_PATH.suffix + ".part")
    if temporary.exists():
        temporary.unlink()

    sequence = 0
    last_progress = -1
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDNAMES,
            lineterminator="\n",
        )
        writer.writeheader()

        for month_index, month in enumerate(months, start=1):
            expected_times = expected_market_times(month)
            expected_set = set(expected_times)
            cutoff = monthly_cutoff(month)
            month_rows: dict[str, dict[datetime, NormalizedPair]] = {}

            for currency, (symbol, orientation) in CANDIDATES.items():
                decoded_by_side: dict[
                    str,
                    dict[datetime, Ohlc],
                ] = {}
                downloaded_pair = download_source_pair_resilient(symbol, month)
                if downloaded_pair is None:
                    for side in ("BID", "ASK"):
                        missing_source_objects.append(
                            {
                                "symbol": symbol,
                                "month": month.strftime("%Y-%m"),
                                "side": side,
                            }
                        )
                        decoded_by_side[side] = {}
                    pair_source_format = "SOURCE_ABSENT"
                else:
                    pair_formats = {
                        headers["source_format"] for _, headers in downloaded_pair.values()
                    }
                    if len(pair_formats) != 1:
                        raise DevelopmentDataPrepError(
                            f"mixed source formats for {symbol} {month:%Y-%m}: "
                            f"{sorted(pair_formats)}"
                        )
                    pair_source_format = next(iter(pair_formats))
                    for side in ("BID", "ASK"):
                        path, headers = downloaded_pair[side]
                        decoded_by_side[side] = decode_source_object(
                            path,
                            month,
                            symbol,
                            pair_source_format,
                        )
                        source_files.append(
                            {
                                "symbol": symbol,
                                "month": month.strftime("%Y-%m"),
                                "side": side,
                                "sha256": sha256_file(path),
                                "source_format": pair_source_format,
                                "relative_path": str(path.relative_to(ROOT)).replace("\\", "/"),
                                "source_url": headers["source_url"],
                                "last_modified": headers["last_modified"],
                                "etag": headers["etag"],
                            }
                        )

                bid_times = expected_set.intersection(decoded_by_side["BID"])
                ask_times = expected_set.intersection(decoded_by_side["ASK"])
                if bid_times != ask_times:
                    raise DevelopmentDataPrepError(
                        f"BID/ASK timestamp mismatch for "
                        f"{symbol} {month:%Y-%m}: "
                        f"missing ASK={len(bid_times - ask_times)}, "
                        f"missing BID={len(ask_times - bid_times)}"
                    )

                aligned_times = sorted(bid_times)
                stats = symbol_stats[currency]
                stats["expected_market_hours"] += len(expected_times)
                stats["missing_market_hours"] += len(expected_times) - len(aligned_times)
                stats["aligned_rows"] += len(aligned_times)

                if aligned_times:
                    first = aligned_times[0]
                    last = aligned_times[-1]
                    if stats["first_usable_timestamp"] is None:
                        stats["first_usable_timestamp"] = iso_z(first)
                    stats["last_usable_timestamp"] = iso_z(last)

                if cutoff in bid_times:
                    stats["cutoff_eligible_months"] += 1
                else:
                    stats["cutoff_ineligible_missing_months"] += 1

                normalized: dict[
                    datetime,
                    NormalizedPair,
                ] = {}
                for timestamp in aligned_times:
                    try:
                        normalized[timestamp] = normalize_pair_ohlc(
                            decoded_by_side["BID"][timestamp],
                            decoded_by_side["ASK"][timestamp],
                            orientation,
                        )
                    except DevelopmentDataPrepError as exc:
                        raise DevelopmentDataPrepError(
                            f"{symbol} {month:%Y-%m} {iso_z(timestamp)} {pair_source_format}: {exc}"
                        ) from exc
                month_rows[currency] = normalized

            all_timestamps = sorted(
                {timestamp for rows in month_rows.values() for timestamp in rows}
            )
            for timestamp in all_timestamps:
                for currency, (symbol, orientation) in CANDIDATES.items():
                    item = month_rows[currency].get(timestamp)
                    if item is None:
                        continue
                    bid, ask = item
                    writer.writerow(
                        {
                            "event_time": iso_z(timestamp),
                            "availability_time": iso_z(timestamp + timedelta(hours=1)),
                            "currency": currency,
                            "source_symbol": symbol,
                            "source_orientation": orientation,
                            "sequence": sequence,
                            "bid_open": f"{bid[0]:.12f}",
                            "bid_high": f"{bid[1]:.12f}",
                            "bid_low": f"{bid[2]:.12f}",
                            "bid_close": f"{bid[3]:.12f}",
                            "ask_open": f"{ask[0]:.12f}",
                            "ask_high": f"{ask[1]:.12f}",
                            "ask_low": f"{ask[2]:.12f}",
                            "ask_close": f"{ask[3]:.12f}",
                        }
                    )
                    sequence += 1

            eligible_currencies = [
                currency for currency in CANDIDATES if cutoff in month_rows[currency]
            ]
            ranking_anchor = next_month(month)
            if ranking_anchor >= DATA_END:
                point_status = "PROTECTED_BOUNDARY"
            elif len(eligible_currencies) >= MINIMUM_ELIGIBLE_CURRENCIES:
                point_status = "ELIGIBLE_GE6"
            else:
                point_status = "INSUFFICIENT_CURRENCIES"
            monthly_points.append(
                {
                    "source_month": month.strftime("%Y-%m"),
                    "cutoff_event_time": iso_z(cutoff),
                    "cutoff_availability_time": iso_z(cutoff + timedelta(hours=1)),
                    "ranking_month_anchor": iso_z(ranking_anchor),
                    "eligible_currencies": eligible_currencies,
                    "eligible_currency_count": len(eligible_currencies),
                    "status": point_status,
                    "supports_longest_12_12_geometry": (
                        point_status == "ELIGIBLE_GE6" and supports_longest_12_12_geometry(month)
                    ),
                }
            )

            if month_index == 1 or month_index % 12 == 0 or month_index == len(months):
                progress(
                    f"[month {month_index}/{len(months)}] "
                    f"{month:%Y-%m}; rows={sequence}; "
                    f"acquired_objects={len(source_files)}; "
                    f"missing_objects={len(missing_source_objects)}"
                )
            percent = min(
                99,
                76 + round(month_index * 23 / len(months)),
            )
            if percent != last_progress:
                emit_progress(percent)
                last_progress = percent

    if sequence == 0:
        temporary.unlink(missing_ok=True)
        raise DevelopmentDataPrepError("prepared development dataset has no rows")
    temporary.replace(DERIVED_PATH)

    first_values = [
        stats["first_usable_timestamp"]
        for stats in symbol_stats.values()
        if stats["first_usable_timestamp"] is not None
    ]
    last_values = [
        stats["last_usable_timestamp"]
        for stats in symbol_stats.values()
        if stats["last_usable_timestamp"] is not None
    ]
    common_start = max(first_values) if len(first_values) == len(CANDIDATES) else None
    common_end = min(last_values) if len(last_values) == len(CANDIDATES) else None

    eligible_points = [point for point in monthly_points if point["status"] == "ELIGIBLE_GE6"]
    longest_points = [point for point in monthly_points if point["supports_longest_12_12_geometry"]]
    decision = (
        "READY_FOR_DEVELOPMENT_DATA_FREEZE"
        if eligible_points and longest_points and common_start is not None
        else "INSUFFICIENT_DEVELOPMENT_DATA"
    )

    return {
        "schema_version": "hyp0003-development-data-prep-1",
        "task_id": "ATS2-RF-008",
        "hypothesis_id": "HYP-0003",
        "git_commit": git_head(),
        "development_dataset_id": DATASET_ID,
        "development_dataset_version": DATASET_VERSION,
        "preparation_decision": decision,
        "period_start": iso_z(DATA_START),
        "period_end_exclusive": iso_z(DATA_END),
        "source_month_count": len(months),
        "source_objects_expected": len(months) * len(CANDIDATES) * 2,
        "source_objects_acquired": len(source_files),
        "source_objects_missing": len(missing_source_objects),
        "source_files": source_files,
        "missing_source_objects": missing_source_objects,
        "source_bundle_sha256": source_bundle_hash(source_files),
        "prepared_csv_relative_path": str(DERIVED_PATH.relative_to(ROOT)).replace("\\", "/"),
        "prepared_csv_sha256": sha256_file(DERIVED_PATH),
        "prepared_row_count": sequence,
        "common_usable_start": common_start,
        "common_usable_end": common_end,
        "eligible_monthly_ranking_points_ge6": len(eligible_points),
        "eligible_longest_12_12_geometry_points": len(longest_points),
        "monthly_points": monthly_points,
        "symbol_stats": list(symbol_stats.values()),
        "protected_tail_source_objects_requested": 0,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "ATS HYP-0003 DEVELOPMENT DATA PREPARATION",
        "=========================================",
        f"Git commit: {payload['git_commit']}",
        "Hypothesis: HYP-0003",
        f"Preparation decision: {payload['preparation_decision']}",
        (
            f"Dataset ID: {payload['development_dataset_id']}"
            f"@{payload['development_dataset_version']}"
        ),
        (f"Period: {payload['period_start']} to {payload['period_end_exclusive']}"),
        f"Source months: {payload['source_month_count']}",
        f"Source objects expected: {payload['source_objects_expected']}",
        f"Source objects acquired: {payload['source_objects_acquired']}",
        f"Source objects missing: {payload['source_objects_missing']}",
        f"Source bundle SHA256: {payload['source_bundle_sha256']}",
        f"Prepared rows: {payload['prepared_row_count']}",
        f"Prepared CSV SHA256: {payload['prepared_csv_sha256']}",
        f"Common usable start: {payload['common_usable_start']}",
        f"Common usable end: {payload['common_usable_end']}",
        (
            "Eligible monthly ranking points (>=6 currencies): "
            f"{payload['eligible_monthly_ranking_points_ge6']}"
        ),
        (
            "Eligible longest 12/12 geometry points: "
            f"{payload['eligible_longest_12_12_geometry_points']}"
        ),
        "Protected-tail source objects requested: 0",
        "Information boundary: NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "",
        "SYMBOL QUALITY SUMMARY",
        "----------------------",
    ]
    for item in payload["symbol_stats"]:
        lines.append(
            f"{item['currency']} {item['symbol']}: "
            f"rows={item['aligned_rows']}; "
            f"missing_market_hours={item['missing_market_hours']}; "
            f"cutoff_eligible={item['cutoff_eligible_months']}; "
            f"cutoff_missing="
            f"{item['cutoff_ineligible_missing_months']}"
        )
    lines += [
        "",
        "NEXT STEP",
        "---------",
        "Send CURRENT_TASK_REPORT.txt to ChatGPT.",
        "Do not calculate HYP-0003 momentum/ranking/basket outcomes yet.",
    ]
    REPORT_TEXT.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    print("\n".join(lines), flush=True)


def prepare() -> int:
    emit_progress(76)
    progress("[contract] RF-007 frozen development-data contract loaded")
    payload = build_dataset()
    write_reports(payload)
    return 0


def main() -> int:
    try:
        return prepare()
    except (DevelopmentDataPrepError, OSError, ValueError) as exc:
        print(
            f"HYP-0003 DEVELOPMENT DATA PREP BLOCKED: {exc}",
            file=sys.stderr,
            flush=True,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
