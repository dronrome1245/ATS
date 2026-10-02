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
BLS_SNAPSHOT_MANIFEST = ROOT / "data" / "reference" / "HYP-0006-BLS-SCHEDULE-SNAPSHOT-MANIFEST.csv"
BLS_CALENDAR_CSV = ROOT / "data" / "derived" / "HYP-0006-BLS-CPI-CALENDAR-2003-2021.csv"
DUKASCOPY_BASES = (
    "https://datafeed.dukascopy.com/datafeed",
    "https://www.dukascopy.com/datafeed",
)
SOURCE_SYMBOL = "EURUSD"
PRICE_DIVISOR = 100_000
USER_AGENT = "ATS-Research/1.0"
EXTERNAL_SOURCE_FAILURE_POLICY = "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF"

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

BLS_CALENDAR_FIELDS = (
    "event_id",
    "release_date_local",
    "release_time_local",
    "release_time_utc",
    "timezone_semantics",
    "schedule_label",
    "same_time_bls_labels",
    "source_year",
    "source_url",
    "source_snapshot_relative_path",
    "source_snapshot_sha256",
)

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


class OwnerInputRequiredError(PreparationError):
    """Raised when the one-time local BLS snapshot bundle is incomplete."""


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


class ScheduleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data:
            self.parts.append(data)


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


def load_bls_snapshot_manifest() -> list[dict[str, str]]:
    if not BLS_SNAPSHOT_MANIFEST.is_file():
        raise PreparationError(f"missing BLS snapshot manifest: {BLS_SNAPSHOT_MANIFEST}")

    with BLS_SNAPSHOT_MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        expected_header = ("year", "source_url", "snapshot_relative_path")
        if tuple(reader.fieldnames or ()) != expected_header:
            raise PreparationError("invalid BLS snapshot manifest header")
        rows = [dict(row) for row in reader]

    expected_years = list(range(2003, 2022))
    actual_years: list[int] = []
    for row in rows:
        try:
            year = int(row["year"])
        except (TypeError, ValueError) as exc:
            raise PreparationError("invalid BLS snapshot manifest year") from exc
        expected_url = f"https://www.bls.gov/schedule/{year}/home.htm"
        expected_path = f"data/raw/bls/hyp0006/schedules/{year}.html"
        if row["source_url"] != expected_url:
            raise PreparationError(f"unexpected BLS source URL for {year}")
        if row["snapshot_relative_path"] != expected_path:
            raise PreparationError(f"unexpected BLS snapshot path for {year}")
        actual_years.append(year)

    if actual_years != expected_years:
        raise PreparationError(
            f"BLS snapshot manifest years mismatch: {actual_years} != {expected_years}"
        )
    return rows


def load_bls_schedule_snapshots(
    manifest_rows: list[dict[str, str]],
) -> tuple[dict[int, list[dict[str, Any]]], dict[int, SourceObject]]:
    missing: list[str] = []
    schedule_by_year: dict[int, list[dict[str, Any]]] = {}
    source_by_year: dict[int, SourceObject] = {}

    for row in manifest_rows:
        year = int(row["year"])
        snapshot_path = ROOT / row["snapshot_relative_path"]
        if not snapshot_path.is_file() or snapshot_path.stat().st_size <= 0:
            missing.append(row["snapshot_relative_path"])
            continue

        entries = schedule_entries(snapshot_path.read_bytes(), year)
        cpi_entries = [
            item for item in entries if "consumer price index" in str(item["label"]).lower()
        ]
        if not cpi_entries:
            raise PreparationError(f"BLS snapshot {year} contains no parseable CPI schedule rows")

        schedule_by_year[year] = entries
        source_by_year[year] = SourceObject(
            category="BLS_SCHEDULE_SNAPSHOT",
            identity=str(year),
            relative_path=row["snapshot_relative_path"],
            source_url=row["source_url"],
            sha256=sha256_file(snapshot_path),
        )

    if missing:
        joined = ", ".join(missing)
        raise OwnerInputRequiredError("OWNER_INPUT_REQUIRED_BLS_SCHEDULE_SNAPSHOTS: " + joined)

    return schedule_by_year, source_by_year


def bls_snapshot_bundle_hash(source_by_year: dict[int, SourceObject]) -> str:
    payload = [
        {
            "year": year,
            "source_url": source_by_year[year].source_url,
            "relative_path": source_by_year[year].relative_path,
            "sha256": source_by_year[year].sha256,
        }
        for year in sorted(source_by_year)
    ]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


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
        raise PreparationError(
            "live BLS network access is disabled; use frozen local schedule snapshots"
        )
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

    if not urls:
        raise PreparationError(f"no source URL configured for {label}")

    url = urls[0]
    try:
        body, headers = fetch_bytes(url)
    except FileNotFoundError:
        if missing_ok:
            return None
        raise PreparationError(f"required source object missing: {label}") from None
    except PreparationError as exc:
        raise PreparationError(f"{EXTERNAL_SOURCE_FAILURE_POLICY}: {label}: {exc}") from exc

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    temporary.write_bytes(body)
    temporary.replace(destination)
    headers["source_url"] = url
    return destination, headers


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
    text = payload.decode("utf-8", errors="replace")
    entries: list[dict[str, Any]] = []
    seen: set[tuple[date, str, str]] = set()

    def append_entry(row_date: date, row_clock: str, label: str) -> None:
        normalized_label = re.sub(r"\s+", " ", label).strip()
        if not normalized_label or not re.search(r"[A-Za-z]", normalized_label):
            return
        key = (row_date, row_clock, normalized_label)
        if key in seen:
            return
        seen.add(key)
        entries.append(
            {
                "date": row_date,
                "clock": row_clock,
                "label": normalized_label,
            }
        )

    table_parser = TableRowParser()
    table_parser.feed(text)
    for cells in table_parser.rows:
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
        if candidates:
            append_entry(row_date, row_clock, max(candidates, key=len))

    text_parser = ScheduleTextParser()
    text_parser.feed(text)
    current_year = year
    for raw_line in "\n".join(text_parser.parts).splitlines():
        line = re.sub(r"[ \t]+", " ", raw_line).strip()
        clock_match = CLOCK_RE.search(line)
        if clock_match is None:
            continue
        date_matches = list(MONTH_RE.finditer(line[: clock_match.start()]))
        if not date_matches:
            continue
        date_match = date_matches[-1]
        month_key = date_match.group(1).lower().rstrip(".")
        month = MONTHS.get(month_key)
        if month is None:
            continue
        if date_match.group(3):
            current_year = int(date_match.group(3))
        try:
            row_date = date(current_year, month, int(date_match.group(2)))
        except ValueError:
            continue
        row_clock = parse_schedule_clock(clock_match.group(0))
        if row_clock is None:
            continue
        append_entry(row_date, row_clock, line[: date_match.start()])

    entries.sort(key=lambda item: (item["date"], item["clock"], item["label"]))
    return entries


def schedule_local_datetime(entry: dict[str, Any]) -> datetime:
    row_date = entry["date"]
    if not isinstance(row_date, date):
        raise PreparationError("schedule entry date has invalid type")
    clock = str(entry["clock"])
    hour_text, minute_text = clock.split(":", 1)
    return datetime.combine(row_date, dt_time(int(hour_text), int(minute_text)))


def archive_url_for_release_date(release_date: date) -> str:
    stamp = release_date.strftime("%m%d%Y")
    return f"https://www.bls.gov/news.release/archives/cpi_{stamp}.htm"


def cpi_schedule_candidates(
    schedule_by_year: dict[int, list[dict[str, Any]]],
    source_by_year: dict[int, SourceObject],
) -> list[dict[str, Any]]:
    by_date: dict[date, dict[str, Any]] = {}
    for year, entries in schedule_by_year.items():
        source = source_by_year.get(year)
        if source is None:
            raise PreparationError(f"missing BLS snapshot source identity for {year}")
        for entry in entries:
            if "consumer price index" not in str(entry["label"]).lower():
                continue
            local_dt = schedule_local_datetime(entry)
            release_utc = eastern_local_to_utc(local_dt, "ET")
            if not DEVELOPMENT_START <= release_utc < DEVELOPMENT_END:
                continue

            candidate = {
                "date": local_dt.date(),
                "clock": str(entry["clock"]),
                "label": str(entry["label"]),
                "release_time_utc": release_utc,
                "source_year": year,
                "source_url": source.source_url,
                "source_snapshot_relative_path": source.relative_path,
                "source_snapshot_sha256": source.sha256,
            }
            existing = by_date.get(local_dt.date())
            if existing is None:
                by_date[local_dt.date()] = candidate
                continue
            if existing["clock"] != candidate["clock"]:
                raise PreparationError(
                    "conflicting official CPI schedule times for "
                    f"{local_dt.date().isoformat()}: "
                    f"{existing['clock']} != {candidate['clock']}"
                )

            existing_year = int(existing["source_year"])
            preferred_year = local_dt.date().year
            existing_rank = (existing_year != preferred_year, existing_year)
            candidate_rank = (year != preferred_year, year)
            if candidate_rank < existing_rank:
                by_date[local_dt.date()] = candidate

    return [by_date[key] for key in sorted(by_date)]


def same_time_schedule_labels(
    entries: list[dict[str, Any]],
    release_date: date,
    clock: str,
) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                str(item["label"])
                for item in entries
                if item["date"] == release_date
                and item["clock"] == clock
                and "consumer price index" not in str(item["label"]).lower()
            }
        )
    )


def write_bls_calendar_csv(
    candidates: list[dict[str, Any]],
    schedule_by_year: dict[int, list[dict[str, Any]]],
) -> str:
    BLS_CALENDAR_CSV.parent.mkdir(parents=True, exist_ok=True)
    temporary = BLS_CALENDAR_CSV.with_suffix(BLS_CALENDAR_CSV.suffix + ".part")

    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=BLS_CALENDAR_FIELDS,
            lineterminator="\n",
        )
        writer.writeheader()
        for candidate in candidates:
            release_date = candidate["date"]
            if not isinstance(release_date, date):
                raise PreparationError("CPI candidate date has invalid type")
            release_utc = candidate["release_time_utc"]
            if not isinstance(release_utc, datetime):
                raise PreparationError("CPI candidate UTC time has invalid type")
            clock = str(candidate["clock"])
            same_time_labels = same_time_schedule_labels(
                schedule_by_year[int(candidate["source_year"])],
                release_date,
                clock,
            )
            writer.writerow(
                {
                    "event_id": f"BLS-CPI-{release_date:%Y%m%d}",
                    "release_date_local": release_date.isoformat(),
                    "release_time_local": clock,
                    "release_time_utc": iso_z(release_utc),
                    "timezone_semantics": "US_EASTERN_HISTORICAL_DST",
                    "schedule_label": str(candidate["label"]),
                    "same_time_bls_labels": "|".join(same_time_labels),
                    "source_year": int(candidate["source_year"]),
                    "source_url": str(candidate["source_url"]),
                    "source_snapshot_relative_path": str(
                        candidate["source_snapshot_relative_path"]
                    ),
                    "source_snapshot_sha256": str(candidate["source_snapshot_sha256"]),
                }
            )

    temporary.replace(BLS_CALENDAR_CSV)
    return sha256_file(BLS_CALENDAR_CSV)


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
    complete_geometry_count: int,
) -> str:
    if candidate_event_count <= 0:
        return "UNRESOLVED_OFFICIAL_EVENT_TIMES"
    if complete_geometry_count <= 0:
        return "INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY"
    return "READY_FOR_DATA_FEASIBILITY_FREEZE"


def prepare() -> dict[str, Any]:
    source_objects: list[SourceObject] = []
    tick_objects: list[TickObject] = []

    emit_progress(82)
    manifest_rows = load_bls_snapshot_manifest()
    schedule_by_year, source_by_year = load_bls_schedule_snapshots(manifest_rows)
    source_objects.extend(source_by_year[year] for year in sorted(source_by_year))

    candidates = cpi_schedule_candidates(schedule_by_year, source_by_year)
    if not candidates:
        raise PreparationError("frozen BLS schedule snapshots produced no CPI events")

    bls_calendar_sha256 = write_bls_calendar_csv(candidates, schedule_by_year)
    bls_snapshot_sha256 = bls_snapshot_bundle_hash(source_by_year)

    event_records: list[EventRecord] = []
    requested_hours: set[datetime] = set()
    missing_hour_count_total = 0
    protected_source_requests = 0
    same_time_cluster_count = 0
    complete_geometry_count = 0
    tick_cache: dict[datetime, tuple[TickObject, list[datetime]] | None] = {}

    total = len(candidates)
    for index, candidate in enumerate(candidates, start=1):
        release_date = candidate["date"]
        release_utc = candidate["release_time_utc"]
        if not isinstance(release_date, date) or not isinstance(release_utc, datetime):
            raise PreparationError("invalid frozen BLS calendar event type")

        schedule_clock = str(candidate["clock"])
        schedule_entries_for_year = schedule_by_year[int(candidate["source_year"])]
        same_time_labels = same_time_schedule_labels(
            schedule_entries_for_year,
            release_date,
            schedule_clock,
        )
        if same_time_labels:
            same_time_cluster_count += 1

        progress(f"[event {index}/{total}] {release_date.isoformat()}")

        hours = required_tick_hours(release_utc)
        required_count = len(hours)
        requested_hours.update(hours)
        event_times: list[datetime] = []
        missing_count = 0

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

        source_sha = str(candidate["source_snapshot_sha256"])
        event_records.append(
            EventRecord(
                event_id=f"BLS-CPI-{release_date:%Y%m%d}",
                archive_release_date=release_date.isoformat(),
                archive_url=str(candidate["source_url"]),
                archive_sha256=source_sha,
                archive_zone_label="ET",
                archive_local_time=f"{release_date.isoformat()} {schedule_clock}",
                release_time_utc=iso_z(release_utc),
                release_time_status="RESOLVED_FROZEN_BLS_SCHEDULE_SNAPSHOT",
                schedule_crosscheck_status="FROZEN_OFFICIAL_SCHEDULE",
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
        complete_geometry_count=complete_geometry_count,
    )
    emit_progress(98)

    result = {
        "schema_version": "hyp0006-data-feasibility-prep-2",
        "task_id": TASK_ID,
        "hypothesis_id": HYPOTHESIS_ID,
        "git_commit": git_head(),
        "development_start": iso_z(DEVELOPMENT_START),
        "development_end_exclusive": iso_z(DEVELOPMENT_END),
        "evidence_classification": "DEVELOPMENT_EXPLORATORY_ONLY",
        "event_inventory_source": "BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS",
        "event_time_source": "BLS_ANNUAL_SCHEDULE_US_EASTERN",
        "bls_snapshot_manifest_relative_path": str(BLS_SNAPSHOT_MANIFEST.relative_to(ROOT)).replace(
            "\\", "/"
        ),
        "bls_snapshot_manifest_sha256": sha256_file(BLS_SNAPSHOT_MANIFEST),
        "bls_snapshot_count": len(source_by_year),
        "bls_snapshot_bundle_sha256": bls_snapshot_sha256,
        "bls_calendar_csv_relative_path": str(BLS_CALENDAR_CSV.relative_to(ROOT)).replace(
            "\\", "/"
        ),
        "bls_calendar_csv_sha256": bls_calendar_sha256,
        "quote_source": "DUKASCOPY_HOURLY_TICK_BI5",
        "candidate_event_count": len(event_records),
        "resolved_event_time_count": len(event_records),
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
        f"BLS snapshots: {result['bls_snapshot_count']}",
        f"BLS snapshot bundle SHA-256: {result['bls_snapshot_bundle_sha256']}",
        f"BLS calendar SHA-256: {result['bls_calendar_csv_sha256']}",
        f"Candidate CPI events: {result['candidate_event_count']}",
        f"Resolved event times: {result['resolved_event_time_count']}",
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
    except OwnerInputRequiredError as exc:
        print(f"[OWNER INPUT REQUIRED] RF-027 preparation: {exc}", flush=True)
        return 1
    except (PreparationError, OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"[FAIL] RF-027 preparation: {exc}", flush=True)
        return 1

    emit_progress(100)
    print(f"[PASS] RF-027 preparation: {result['preparation_decision']}", flush=True)
    print(f"Information boundary: {result['information_boundary']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
