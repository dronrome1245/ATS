#!/usr/bin/env python3
"""Prepare HYP-0006 official-event and tick-source geometry without computing returns."""

from __future__ import annotations

import bisect
import csv
import hashlib
import json
import lzma
import math
import re
import struct
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime, timedelta, timezone
from datetime import time as dt_time
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ATS2-RF-027"
HYPOTHESIS_ID = "HYP-0006"

DEVELOPMENT_START = datetime(2003, 8, 3, 21, tzinfo=UTC)
DEVELOPMENT_END = datetime(2021, 9, 1, tzinfo=UTC)
HYP0005_LEFT_START = datetime(2003, 5, 4, 21, tzinfo=UTC)
HYP0005_LEFT_END = datetime(2003, 8, 3, 21, tzinfo=UTC)
HYP0005_RIGHT_START = datetime(2026, 9, 1, tzinfo=UTC)
HYP0005_RIGHT_END = datetime(2026, 9, 26, tzinfo=UTC)

BLS_ARCHIVE_INDEX_URL = "https://www.bls.gov/bls/news-release/cpi.htm"
BLS_SCHEDULE_URL_TEMPLATE = "https://www.bls.gov/schedule/{year}/home.htm"
DUKASCOPY_BASES = (
    "https://datafeed.dukascopy.com/datafeed",
    "https://www.dukascopy.com/datafeed",
)
SOURCE_SYMBOL = "EURUSD"
PRICE_DIVISOR = 100_000
BLS_CONTACT_URL = "https://github.com/dronrome1245/ATS"
BLS_REQUEST_DELAY_SECONDS = 1.0
USER_AGENT = f"ATS-Research/1.0 (+{BLS_CONTACT_URL})"
RETRY_DELAYS = (2.0, 5.0, 10.0)

RAW_BLS_ROOT = ROOT / "data" / "raw" / "bls" / "hyp0006"
RAW_DUKASCOPY_ROOT = ROOT / "data" / "raw" / "dukascopy" / "hyp0006" / SOURCE_SYMBOL
REPORT_JSON = ROOT / "reports" / "local_ci" / "HYP0006_DATA_FEASIBILITY_PREP.json"
REPORT_TEXT = ROOT / "reports" / "local_ci" / "HYP0006_DATA_FEASIBILITY_PREP_REPORT.txt"
GEOMETRY_CSV = ROOT / "data" / "derived" / "HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv"

TICK_RECORD = struct.Struct(">IIIff")
ARCHIVE_RE = re.compile(r"cpi_(\d{8})\.htm$", re.IGNORECASE)
CLOCK_RE = re.compile(r"\b(\d{1,2}):(\d{2})\s*(a\.?\s*m\.?|p\.?\s*m\.?)\b", re.IGNORECASE)
MONTH_RE = re.compile(
    r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|"
    r"Dec(?:ember)?)\.?\s+(\d{1,2})(?:,\s*(\d{4}))?\b",
    re.IGNORECASE,
)
ARCHIVE_TIME_RE = re.compile(
    r"(\d{1,2}):(\d{2})\s*(a\.?\s*m\.?|p\.?\s*m\.?)\s*"
    r"\((ET|EST|EDT)\)[,\s]*(?:[A-Za-z]+,\s*)?"
    r"([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})",
    re.IGNORECASE,
)

MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}

GEOMETRY_FIELDS = (
    "event_id",
    "archive_release_date",
    "release_time_utc",
    "archive_zone_label",
    "schedule_crosscheck_status",
    "same_time_bls_labels",
    "required_tick_object_count",
    "missing_tick_object_count",
    "pre60_prev_gap_ms",
    "pre60_next_gap_ms",
    "pre_release_last_gap_ms",
    "post60_prev_gap_ms",
    "post60_next_gap_ms",
    "quote_geometry_status",
)

FORBIDDEN_OUTPUT_FIELDS = {
    "bid",
    "ask",
    "mid",
    "midpoint",
    "pre_abs_60m_return",
    "post_abs_60m_return",
    "return",
    "pnl",
    "profit",
}


class PreparationError(RuntimeError):
    """Raised for technical/data integrity failures in RF-027."""


class SourceAccessDeniedError(PreparationError):
    """Raised when an official source explicitly denies automated access."""


@dataclass(frozen=True)
class SourceObject:
    category: str
    identity: str
    relative_path: str
    source_url: str
    sha256: str


@dataclass(frozen=True)
class TickObject:
    hour_start: str
    relative_path: str
    source_url: str
    sha256: str
    record_count: int
    first_timestamp: str
    last_timestamp: str
    duplicate_timestamp_count: int


@dataclass(frozen=True)
class EventRecord:
    event_id: str
    archive_release_date: str
    archive_url: str
    archive_sha256: str | None
    archive_zone_label: str | None
    archive_local_time: str | None
    release_time_utc: str | None
    release_time_status: str
    schedule_crosscheck_status: str
    same_time_bls_labels: tuple[str, ...]
    required_tick_object_count: int
    missing_tick_object_count: int
    pre60_prev_gap_ms: int | None
    pre60_next_gap_ms: int | None
    pre_release_last_gap_ms: int | None
    post60_prev_gap_ms: int | None
    post60_next_gap_ms: int | None
    quote_geometry_status: str


class ArchiveLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        href = dict(attrs).get("href")
        if href and ARCHIVE_RE.search(href):
            self.links.append(href)


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if stripped:
            self.parts.append(stripped)


class TableRowParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell_parts: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lowered = tag.lower()
        if lowered == "tr":
            self._row = []
        elif lowered in {"td", "th"} and self._row is not None:
            self._cell_parts = []

    def handle_data(self, data: str) -> None:
        if self._cell_parts is not None:
            stripped = data.strip()
            if stripped:
                self._cell_parts.append(stripped)

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        if lowered in {"td", "th"} and self._row is not None and self._cell_parts is not None:
            value = " ".join(self._cell_parts)
            value = re.sub(r"\s+", " ", value).strip()
            self._row.append(value)
            self._cell_parts = None
        elif lowered == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None
            self._cell_parts = None


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
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ").replace(".000000Z", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_bls_url(url: str) -> bool:
    return url.startswith("https://www.bls.gov/")


def request_headers(url: str) -> dict[str, str]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/octet-stream,*/*",
    }
    if is_bls_url(url):
        headers.update(
            {
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.bls.gov/",
            }
        )
    return headers


def fetch_bytes(url: str, timeout: int = 45) -> tuple[bytes, dict[str, str]]:
    if is_bls_url(url):
        time.sleep(BLS_REQUEST_DELAY_SECONDS)
    request = urllib.request.Request(url, headers=request_headers(url))
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
        if exc.code == 403 and is_bls_url(url):
            raise SourceAccessDeniedError(
                f"BLS HTTP 403 while fetching {url}; automated access denied"
            ) from exc
        raise PreparationError(f"HTTP {exc.code} while fetching {url}") from exc
    except (urllib.error.URLError, OSError) as exc:
        raise PreparationError(f"network error while fetching {url}: {exc}") from exc
    if not body:
        raise FileNotFoundError(url)
    return body, headers


def cached_or_fetch_any(
    urls: tuple[str, ...],
    destination: Path,
    label: str,
    *,
    missing_ok: bool,
) -> tuple[Path, dict[str, str]] | None:
    if destination.exists() and destination.stat().st_size > 0:
        return destination, {
            "source_url": "LOCAL_FROZEN_COPY",
            "last_modified": "",
            "etag": "",
        }

    attempts = len(RETRY_DELAYS) + 1
    last_error: PreparationError | None = None
    missing_urls: set[str] = set()
    for batch in range(attempts):
        for url in urls:
            try:
                body, headers = fetch_bytes(url)
                destination.parent.mkdir(parents=True, exist_ok=True)
                temporary = destination.with_suffix(destination.suffix + ".part")
                temporary.write_bytes(body)
                temporary.replace(destination)
                headers["source_url"] = url
                return destination, headers
            except FileNotFoundError:
                missing_urls.add(url)
            except SourceAccessDeniedError:
                raise
            except PreparationError as exc:
                last_error = exc
        if len(missing_urls) == len(urls):
            if missing_ok:
                return None
            raise PreparationError(f"required source object missing: {label}")
        if batch < attempts - 1 and last_error is not None:
            delay = RETRY_DELAYS[batch]
            progress(f"[network] {label} retrying in {delay:.0f}s")
            time.sleep(delay)

    if last_error is not None:
        raise PreparationError(f"{label} failed after retries: {last_error}")
    if missing_ok:
        return None
    raise PreparationError(f"required source object missing: {label}")


def visible_text(payload: bytes) -> str:
    parser = VisibleTextParser()
    parser.feed(payload.decode("utf-8", errors="replace"))
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip()


def parse_archive_index(payload: bytes) -> list[tuple[date, str]]:
    parser = ArchiveLinkParser()
    parser.feed(payload.decode("utf-8", errors="replace"))

    records: dict[date, str] = {}
    for href in parser.links:
        match = ARCHIVE_RE.search(href)
        if match is None:
            continue
        stamp = match.group(1)
        release_date = datetime.strptime(stamp, "%m%d%Y").date()
        records[release_date] = urljoin(BLS_ARCHIVE_INDEX_URL, href)
    return sorted(records.items())


def nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    first = date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    return date(year, month, 1 + offset + 7 * (n - 1))


def last_weekday(year: int, month: int, weekday: int) -> date:
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    current = next_month - timedelta(days=1)
    return current - timedelta(days=(current.weekday() - weekday) % 7)


def us_eastern_dst_active(local_day: date) -> bool:
    year = local_day.year
    if year <= 2006:
        start = nth_weekday(year, 4, 6, 1)
        end = last_weekday(year, 10, 6)
    else:
        start = nth_weekday(year, 3, 6, 2)
        end = nth_weekday(year, 11, 6, 1)
    return start <= local_day < end


def normalize_ampm_hour(hour: int, ampm: str) -> int:
    value = re.sub(r"[^a-z]", "", ampm.lower())
    if value not in {"am", "pm"}:
        raise PreparationError(f"unknown meridiem: {ampm}")
    if not 1 <= hour <= 12:
        raise PreparationError(f"invalid 12-hour clock hour: {hour}")
    if value == "am":
        return 0 if hour == 12 else hour
    return 12 if hour == 12 else hour + 12


def eastern_local_to_utc(local_dt: datetime, zone_label: str) -> datetime:
    zone = zone_label.upper()
    if zone == "EST":
        offset_hours = -5
    elif zone == "EDT":
        offset_hours = -4
    elif zone == "ET":
        offset_hours = -4 if us_eastern_dst_active(local_dt.date()) else -5
    else:
        raise PreparationError(f"unsupported BLS time-zone label: {zone_label}")
    aware = local_dt.replace(tzinfo=timezone(timedelta(hours=offset_hours)))
    return aware.astimezone(UTC)


def parse_archive_release_time(
    payload: bytes,
    expected_release_date: date,
) -> tuple[datetime, str, str] | None:
    text = visible_text(payload)
    lowered = text.lower()
    marker = lowered.find("embargoed until")
    search_text = text[marker : marker + 1600] if marker >= 0 else text[:2500]
    match = ARCHIVE_TIME_RE.search(search_text)
    if match is None:
        return None

    hour = normalize_ampm_hour(int(match.group(1)), match.group(3))
    minute = int(match.group(2))
    zone_label = match.group(4).upper()
    month_key = match.group(5).lower().rstrip(".")
    month = MONTHS.get(month_key)
    if month is None:
        return None
    release_date = date(int(match.group(7)), month, int(match.group(6)))
    if release_date != expected_release_date:
        raise PreparationError(
            "archive header date does not match archive URL: "
            f"{release_date.isoformat()} != {expected_release_date.isoformat()}"
        )
    local_dt = datetime.combine(release_date, dt_time(hour, minute))
    utc_dt = eastern_local_to_utc(local_dt, zone_label)
    local_text = local_dt.strftime("%Y-%m-%d %H:%M")
    return utc_dt, zone_label, local_text


def parse_schedule_date(text: str, year: int) -> date | None:
    match = MONTH_RE.search(text)
    if match is None:
        return None
    month_key = match.group(1).lower().rstrip(".")
    month = MONTHS.get(month_key)
    if month is None:
        return None
    parsed_year = int(match.group(3)) if match.group(3) else year
    try:
        return date(parsed_year, month, int(match.group(2)))
    except ValueError:
        return None


def parse_schedule_clock(text: str) -> str | None:
    match = CLOCK_RE.search(text)
    if match is None:
        return None
    hour = normalize_ampm_hour(int(match.group(1)), match.group(3))
    minute = int(match.group(2))
    return f"{hour:02d}:{minute:02d}"


def schedule_entries(payload: bytes, year: int) -> list[dict[str, Any]]:
    parser = TableRowParser()
    parser.feed(payload.decode("utf-8", errors="replace"))
    entries: list[dict[str, Any]] = []
    for cells in parser.rows:
        row_text = " ".join(cells)
        row_date = parse_schedule_date(row_text, year)
        row_clock = parse_schedule_clock(row_text)
        if row_date is None or row_clock is None:
            continue

        candidates = [
            cell
            for cell in cells
            if parse_schedule_date(cell, year) is None and parse_schedule_clock(cell) is None
        ]
        if not candidates:
            continue
        label = max(candidates, key=len).strip()
        if not re.search(r"[A-Za-z]", label):
            continue
        entries.append(
            {
                "date": row_date,
                "clock": row_clock,
                "label": label,
            }
        )
    return entries


def schedule_crosscheck(
    entries: list[dict[str, Any]],
    release_date: date,
    archive_local_time: str,
) -> tuple[str, tuple[str, ...]]:
    expected_clock = archive_local_time[-5:]
    cpi_rows = [
        item
        for item in entries
        if item["date"] == release_date and "consumer price index" in item["label"].lower()
    ]
    if not cpi_rows:
        return "SCHEDULE_CPI_ROW_NOT_FOUND", ()
    matching = [item for item in cpi_rows if item["clock"] == expected_clock]
    if not matching:
        return "SCHEDULE_TIME_MISMATCH", ()

    labels = tuple(
        sorted(
            {
                str(item["label"])
                for item in entries
                if item["date"] == release_date
                and item["clock"] == expected_clock
                and item["label"] != matching[0]["label"]
            }
        )
    )
    return "MATCH", labels


def floor_hour(value: datetime) -> datetime:
    return value.astimezone(UTC).replace(minute=0, second=0, microsecond=0)


def inside_hyp0005_protected(value: datetime) -> bool:
    return (
        HYP0005_LEFT_START <= value < HYP0005_LEFT_END
        or HYP0005_RIGHT_START <= value < HYP0005_RIGHT_END
    )


def required_tick_hours(release_time: datetime) -> tuple[datetime, ...]:
    first = floor_hour(release_time - timedelta(minutes=60)) - timedelta(hours=1)
    last = floor_hour(release_time + timedelta(minutes=60)) + timedelta(hours=1)
    values: list[datetime] = []
    current = first
    while current <= last:
        if not DEVELOPMENT_START <= current < DEVELOPMENT_END:
            raise PreparationError(
                f"RF-027 tick request outside development interval: {iso_z(current)}"
            )
        if inside_hyp0005_protected(current):
            raise PreparationError(
                f"RF-027 tick request enters HYP-0005 protected data: {iso_z(current)}"
            )
        values.append(current)
        current += timedelta(hours=1)
    return tuple(values)


def tick_source_url(base: str, hour_start: datetime) -> str:
    month_zero_based = hour_start.month - 1
    return (
        f"{base}/{SOURCE_SYMBOL}/{hour_start.year}/{month_zero_based:02d}/"
        f"{hour_start.day:02d}/{hour_start.hour:02d}h_ticks.bi5"
    )


def tick_raw_path(hour_start: datetime) -> Path:
    return (
        RAW_DUKASCOPY_ROOT
        / str(hour_start.year)
        / f"{hour_start.month:02d}"
        / f"{hour_start.day:02d}"
        / f"{hour_start.hour:02d}h_ticks.bi5"
    )


def decode_tick_object(
    path: Path,
    hour_start: datetime,
    source_url: str,
) -> tuple[TickObject, list[datetime]]:
    try:
        decoded = lzma.decompress(path.read_bytes())
    except lzma.LZMAError as exc:
        raise PreparationError(f"cannot decompress tick object: {path}") from exc
    if not decoded or len(decoded) % TICK_RECORD.size:
        raise PreparationError(f"invalid Dukascopy tick record length: {path}")

    times: list[datetime] = []
    duplicate_count = 0
    previous_ms: int | None = None
    for offset in range(0, len(decoded), TICK_RECORD.size):
        ms, ask_raw, bid_raw, ask_volume, bid_volume = TICK_RECORD.unpack_from(decoded, offset)
        if not 0 <= ms < 3_600_000:
            raise PreparationError(f"invalid tick millisecond offset in {path}: {ms}")
        if previous_ms is not None and ms < previous_ms:
            raise PreparationError(f"out-of-order tick timestamp in {path}")
        if previous_ms == ms:
            duplicate_count += 1
        previous_ms = ms

        ask = ask_raw / PRICE_DIVISOR
        bid = bid_raw / PRICE_DIVISOR
        if not all(math.isfinite(value) and value > 0 for value in (ask, bid)):
            raise PreparationError(f"invalid BID/ASK quote in {path}")
        if ask < bid:
            raise PreparationError(f"ASK below BID in {path}")
        if not all(math.isfinite(value) and value >= 0 for value in (ask_volume, bid_volume)):
            raise PreparationError(f"invalid tick volume in {path}")

        times.append(hour_start + timedelta(milliseconds=ms))

    try:
        relative_path = str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        relative_path = str(path).replace("\\", "/")

    metadata = TickObject(
        hour_start=iso_z(hour_start),
        relative_path=relative_path,
        source_url=source_url,
        sha256=sha256_file(path),
        record_count=len(times),
        first_timestamp=iso_z(times[0]),
        last_timestamp=iso_z(times[-1]),
        duplicate_timestamp_count=duplicate_count,
    )
    return metadata, times


def download_tick_hour(hour_start: datetime) -> tuple[TickObject, list[datetime]] | None:
    destination = tick_raw_path(hour_start)
    urls = tuple(tick_source_url(base, hour_start) for base in DUKASCOPY_BASES)
    downloaded = cached_or_fetch_any(
        urls,
        destination,
        f"Dukascopy {SOURCE_SYMBOL} {iso_z(hour_start)}",
        missing_ok=True,
    )
    if downloaded is None:
        return None
    path, headers = downloaded
    return decode_tick_object(path, hour_start, headers["source_url"])


def gap_ms(later: datetime, earlier: datetime) -> int:
    return int(round((later - earlier).total_seconds() * 1000))


def event_geometry(times: list[datetime], release_time: datetime) -> dict[str, int | None | str]:
    ordered = sorted(times)
    pre60 = release_time - timedelta(minutes=60)
    post60 = release_time + timedelta(minutes=60)

    def prev_or_equal(target: datetime) -> datetime | None:
        index = bisect.bisect_right(ordered, target) - 1
        return ordered[index] if index >= 0 else None

    def next_or_equal(target: datetime) -> datetime | None:
        index = bisect.bisect_left(ordered, target)
        return ordered[index] if index < len(ordered) else None

    def strictly_before(target: datetime) -> datetime | None:
        index = bisect.bisect_left(ordered, target) - 1
        return ordered[index] if index >= 0 else None

    pre60_prev = prev_or_equal(pre60)
    pre60_next = next_or_equal(pre60)
    pre_release = strictly_before(release_time)
    post60_prev = prev_or_equal(post60)
    post60_next = next_or_equal(post60)

    values: dict[str, int | None | str] = {
        "pre60_prev_gap_ms": gap_ms(pre60, pre60_prev) if pre60_prev else None,
        "pre60_next_gap_ms": gap_ms(pre60_next, pre60) if pre60_next else None,
        "pre_release_last_gap_ms": gap_ms(release_time, pre_release) if pre_release else None,
        "post60_prev_gap_ms": gap_ms(post60, post60_prev) if post60_prev else None,
        "post60_next_gap_ms": gap_ms(post60_next, post60) if post60_next else None,
    }
    complete = all(value is not None for value in values.values())
    values["quote_geometry_status"] = "COMPLETE_TIMESTAMP_GEOMETRY" if complete else "INCOMPLETE"
    return values


def source_bundle_hash(objects: list[SourceObject], tick_objects: list[TickObject]) -> str:
    payload = {
        "source_objects": [
            {
                "category": item.category,
                "identity": item.identity,
                "sha256": item.sha256,
            }
            for item in sorted(objects, key=lambda item: (item.category, item.identity))
        ],
        "tick_objects": [
            {
                "hour_start": item.hour_start,
                "sha256": item.sha256,
                "record_count": item.record_count,
                "duplicate_timestamp_count": item.duplicate_timestamp_count,
            }
            for item in sorted(tick_objects, key=lambda item: item.hour_start)
        ],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_geometry_csv(events: list[EventRecord]) -> str:
    if any(
        any(token in field.lower() for token in FORBIDDEN_OUTPUT_FIELDS)
        for field in GEOMETRY_FIELDS
    ):
        raise PreparationError("geometry CSV contains prohibited outcome/price field name")

    GEOMETRY_CSV.parent.mkdir(parents=True, exist_ok=True)
    temporary = GEOMETRY_CSV.with_suffix(GEOMETRY_CSV.suffix + ".part")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=GEOMETRY_FIELDS, lineterminator="\n")
        writer.writeheader()
        for event in events:
            writer.writerow(
                {
                    "event_id": event.event_id,
                    "archive_release_date": event.archive_release_date,
                    "release_time_utc": event.release_time_utc or "",
                    "archive_zone_label": event.archive_zone_label or "",
                    "schedule_crosscheck_status": event.schedule_crosscheck_status,
                    "same_time_bls_labels": "|".join(event.same_time_bls_labels),
                    "required_tick_object_count": event.required_tick_object_count,
                    "missing_tick_object_count": event.missing_tick_object_count,
                    "pre60_prev_gap_ms": (
                        "" if event.pre60_prev_gap_ms is None else event.pre60_prev_gap_ms
                    ),
                    "pre60_next_gap_ms": (
                        "" if event.pre60_next_gap_ms is None else event.pre60_next_gap_ms
                    ),
                    "pre_release_last_gap_ms": (
                        ""
                        if event.pre_release_last_gap_ms is None
                        else event.pre_release_last_gap_ms
                    ),
                    "post60_prev_gap_ms": (
                        "" if event.post60_prev_gap_ms is None else event.post60_prev_gap_ms
                    ),
                    "post60_next_gap_ms": (
                        "" if event.post60_next_gap_ms is None else event.post60_next_gap_ms
                    ),
                    "quote_geometry_status": event.quote_geometry_status,
                }
            )
    temporary.replace(GEOMETRY_CSV)
    return sha256_file(GEOMETRY_CSV)


def preparation_decision(
    candidate_event_count: int,
    unresolved_event_time_count: int,
    schedule_mismatch_count: int,
    complete_geometry_count: int,
) -> str:
    if candidate_event_count <= 0:
        return "UNRESOLVED_OFFICIAL_EVENT_TIMES"
    if unresolved_event_time_count > 0:
        return "UNRESOLVED_OFFICIAL_EVENT_TIMES"
    if schedule_mismatch_count > 0:
        return "OFFICIAL_TIME_CROSSCHECK_MISMATCH"
    if complete_geometry_count <= 0:
        return "INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY"
    return "READY_FOR_DATA_FEASIBILITY_FREEZE"


def prepare() -> dict[str, Any]:
    source_objects: list[SourceObject] = []
    tick_objects: list[TickObject] = []

    emit_progress(82)
    archive_index_path = RAW_BLS_ROOT / "cpi_archive_index.htm"
    fetched_index = cached_or_fetch_any(
        (BLS_ARCHIVE_INDEX_URL,),
        archive_index_path,
        "BLS CPI archive index",
        missing_ok=False,
    )
    assert fetched_index is not None
    index_path, index_headers = fetched_index
    source_objects.append(
        SourceObject(
            category="BLS_ARCHIVE_INDEX",
            identity="cpi_archive_index",
            relative_path=str(index_path.relative_to(ROOT)).replace("\\", "/"),
            source_url=index_headers["source_url"],
            sha256=sha256_file(index_path),
        )
    )

    candidates = [
        (release_date, url)
        for release_date, url in parse_archive_index(index_path.read_bytes())
        if DEVELOPMENT_START.date() <= release_date < DEVELOPMENT_END.date()
    ]
    if not candidates:
        raise PreparationError("BLS CPI archive index produced no events in frozen interval")

    years = sorted({release_date.year for release_date, _ in candidates})
    schedule_by_year: dict[int, list[dict[str, Any]]] = {}
    for year in years:
        destination = RAW_BLS_ROOT / "schedules" / f"{year}.htm"
        url = BLS_SCHEDULE_URL_TEMPLATE.format(year=year)
        downloaded = cached_or_fetch_any(
            (url,),
            destination,
            f"BLS schedule {year}",
            missing_ok=True,
        )
        if downloaded is None:
            schedule_by_year[year] = []
            continue
        path, headers = downloaded
        schedule_by_year[year] = schedule_entries(path.read_bytes(), year)
        source_objects.append(
            SourceObject(
                category="BLS_SCHEDULE",
                identity=str(year),
                relative_path=str(path.relative_to(ROOT)).replace("\\", "/"),
                source_url=headers["source_url"],
                sha256=sha256_file(path),
            )
        )

    event_records: list[EventRecord] = []
    requested_hours: set[datetime] = set()
    missing_hour_count_total = 0
    protected_source_requests = 0
    schedule_mismatch_count = 0
    schedule_match_count = 0
    same_time_cluster_count = 0
    unresolved_event_time_count = 0
    complete_geometry_count = 0

    tick_cache: dict[datetime, tuple[TickObject, list[datetime]] | None] = {}

    total = len(candidates)
    for index, (release_date, archive_url) in enumerate(candidates, start=1):
        progress(f"[event {index}/{total}] {release_date.isoformat()}")
        archive_name = Path(archive_url).name
        archive_path = RAW_BLS_ROOT / "releases" / archive_name
        archive_download = cached_or_fetch_any(
            (archive_url,),
            archive_path,
            f"BLS CPI archive {archive_name}",
            missing_ok=True,
        )

        archive_sha: str | None = None
        zone_label: str | None = None
        archive_local_time: str | None = None
        release_utc: datetime | None = None
        release_status = "ARCHIVE_PAGE_UNAVAILABLE"
        crosscheck_status = "NOT_RUN"
        same_time_labels: tuple[str, ...] = ()
        required_count = 0
        missing_count = 0
        geometry_values: dict[str, int | None | str] = {
            "pre60_prev_gap_ms": None,
            "pre60_next_gap_ms": None,
            "pre_release_last_gap_ms": None,
            "post60_prev_gap_ms": None,
            "post60_next_gap_ms": None,
            "quote_geometry_status": "UNRESOLVED_EVENT_TIME",
        }

        if archive_download is not None:
            page_path, page_headers = archive_download
            archive_sha = sha256_file(page_path)
            source_objects.append(
                SourceObject(
                    category="BLS_CPI_RELEASE",
                    identity=archive_name,
                    relative_path=str(page_path.relative_to(ROOT)).replace("\\", "/"),
                    source_url=page_headers["source_url"],
                    sha256=archive_sha,
                )
            )
            parsed = parse_archive_release_time(page_path.read_bytes(), release_date)
            if parsed is not None:
                release_utc, zone_label, archive_local_time = parsed
                if not DEVELOPMENT_START <= release_utc < DEVELOPMENT_END:
                    raise PreparationError(
                        f"resolved event outside frozen interval: {iso_z(release_utc)}"
                    )
                release_status = "RESOLVED_OFFICIAL_ARCHIVE_TIME"
                crosscheck_status, same_time_labels = schedule_crosscheck(
                    schedule_by_year.get(release_date.year, []),
                    release_date,
                    archive_local_time,
                )
                if crosscheck_status == "MATCH":
                    schedule_match_count += 1
                elif crosscheck_status == "SCHEDULE_TIME_MISMATCH":
                    schedule_mismatch_count += 1
                if same_time_labels:
                    same_time_cluster_count += 1

                hours = required_tick_hours(release_utc)
                required_count = len(hours)
                requested_hours.update(hours)
                event_times: list[datetime] = []
                for hour_start in hours:
                    if inside_hyp0005_protected(hour_start):
                        protected_source_requests += 1
                        raise PreparationError("HYP-0005 protected source request attempted")
                    if hour_start not in tick_cache:
                        tick_cache[hour_start] = download_tick_hour(hour_start)
                        if tick_cache[hour_start] is not None:
                            metadata, _times = tick_cache[hour_start]
                            tick_objects.append(metadata)
                    downloaded_tick = tick_cache[hour_start]
                    if downloaded_tick is None:
                        missing_count += 1
                        missing_hour_count_total += 1
                        continue
                    _metadata, times = downloaded_tick
                    event_times.extend(times)

                geometry_values = event_geometry(event_times, release_utc)
                if geometry_values["quote_geometry_status"] == "COMPLETE_TIMESTAMP_GEOMETRY":
                    complete_geometry_count += 1
            else:
                release_status = "UNRESOLVED_ARCHIVE_TIMESTAMP"

        if release_utc is None:
            unresolved_event_time_count += 1

        event_records.append(
            EventRecord(
                event_id=archive_name.removesuffix(".htm"),
                archive_release_date=release_date.isoformat(),
                archive_url=archive_url,
                archive_sha256=archive_sha,
                archive_zone_label=zone_label,
                archive_local_time=archive_local_time,
                release_time_utc=iso_z(release_utc) if release_utc else None,
                release_time_status=release_status,
                schedule_crosscheck_status=crosscheck_status,
                same_time_bls_labels=same_time_labels,
                required_tick_object_count=required_count,
                missing_tick_object_count=missing_count,
                pre60_prev_gap_ms=geometry_values["pre60_prev_gap_ms"],
                pre60_next_gap_ms=geometry_values["pre60_next_gap_ms"],
                pre_release_last_gap_ms=geometry_values["pre_release_last_gap_ms"],
                post60_prev_gap_ms=geometry_values["post60_prev_gap_ms"],
                post60_next_gap_ms=geometry_values["post60_next_gap_ms"],
                quote_geometry_status=str(geometry_values["quote_geometry_status"]),
            )
        )
        emit_progress(82 + round(index * 15 / total))

    geometry_sha256 = write_geometry_csv(event_records)
    decision = preparation_decision(
        candidate_event_count=len(event_records),
        unresolved_event_time_count=unresolved_event_time_count,
        schedule_mismatch_count=schedule_mismatch_count,
        complete_geometry_count=complete_geometry_count,
    )
    emit_progress(98)

    result = {
        "schema_version": "hyp0006-data-feasibility-prep-1",
        "task_id": TASK_ID,
        "hypothesis_id": HYPOTHESIS_ID,
        "git_commit": git_head(),
        "development_start": iso_z(DEVELOPMENT_START),
        "development_end_exclusive": iso_z(DEVELOPMENT_END),
        "evidence_classification": "DEVELOPMENT_EXPLORATORY_ONLY",
        "event_inventory_source": "BLS_CPI_ARCHIVE_INDEX",
        "quote_source": "DUKASCOPY_HOURLY_TICK_BI5",
        "candidate_event_count": len(event_records),
        "resolved_event_time_count": len(event_records) - unresolved_event_time_count,
        "unresolved_event_time_count": unresolved_event_time_count,
        "schedule_match_count": schedule_match_count,
        "schedule_mismatch_count": schedule_mismatch_count,
        "same_time_bls_cluster_count": same_time_cluster_count,
        "requested_tick_object_count": len(requested_hours),
        "acquired_tick_object_count": len(tick_objects),
        "missing_tick_object_count": missing_hour_count_total,
        "complete_timestamp_geometry_event_count": complete_geometry_count,
        "protected_hyp0005_source_requests": protected_source_requests,
        "source_bundle_sha256": source_bundle_hash(source_objects, tick_objects),
        "geometry_csv_relative_path": str(GEOMETRY_CSV.relative_to(ROOT)).replace("\\", "/"),
        "geometry_csv_sha256": geometry_sha256,
        "source_objects": [asdict(item) for item in source_objects],
        "tick_objects": [asdict(item) for item in tick_objects],
        "events": [asdict(item) for item in event_records],
        "outcome_metrics_computed": False,
        "primary_claim_evaluated": False,
        "information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "preparation_decision": decision,
    }
    return result


def write_reports(result: dict[str, Any]) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "HYP-0006 DATA FEASIBILITY PREPARATION",
        "====================================",
        f"Task: {result['task_id']}",
        f"Commit: {result['git_commit']}",
        f"Decision: {result['preparation_decision']}",
        f"Candidate CPI events: {result['candidate_event_count']}",
        f"Resolved event times: {result['resolved_event_time_count']}",
        f"Unresolved event times: {result['unresolved_event_time_count']}",
        f"Schedule matches: {result['schedule_match_count']}",
        f"Schedule mismatches: {result['schedule_mismatch_count']}",
        f"Same-time BLS clusters: {result['same_time_bls_cluster_count']}",
        f"Requested tick objects: {result['requested_tick_object_count']}",
        f"Acquired tick objects: {result['acquired_tick_object_count']}",
        f"Missing tick objects: {result['missing_tick_object_count']}",
        (
            "Complete timestamp-geometry events: "
            f"{result['complete_timestamp_geometry_event_count']}"
        ),
        f"HYP-0005 protected requests: {result['protected_hyp0005_source_requests']}",
        f"Source bundle SHA-256: {result['source_bundle_sha256']}",
        f"Geometry CSV SHA-256: {result['geometry_csv_sha256']}",
        f"Outcome metrics computed: {result['outcome_metrics_computed']}",
        f"Primary claim evaluated: {result['primary_claim_evaluated']}",
        f"Information boundary: {result['information_boundary']}",
        "",
        "NEXT STEP",
        "---------",
        "Send CURRENT_TASK_REPORT.txt and HYP0006_DATA_FEASIBILITY_PREP.json to ChatGPT.",
        "Do not calculate HYP-0006 pre/post returns or the primary inequality.",
    ]
    REPORT_TEXT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)


def main() -> int:
    print("ATS HYP-0006 DATA FEASIBILITY PREPARATION", flush=True)
    try:
        result = prepare()
        write_reports(result)
    except (PreparationError, OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"[FAIL] RF-027 preparation: {exc}", flush=True)
        return 1

    emit_progress(100)
    print(f"[PASS] RF-027 preparation: {result['preparation_decision']}", flush=True)
    print(f"Information boundary: {result['information_boundary']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
