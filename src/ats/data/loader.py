"""Deterministic reference-format data loader for ATS M2."""

from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ats.schemas.dataset_manifest import (
    AvailabilityMode,
    DatasetManifest,
    DuplicatePolicy,
    IntegrityAlgorithm,
    MalformedPolicy,
    MissingPolicy,
    OutOfOrderPolicy,
)


RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)


class DatasetLoadError(ValueError):
    """Raised when dataset bytes violate the validated Dataset Manifest contract."""


class MalformedRowError(DatasetLoadError):
    """Raised for row-local defects governed by malformed-row policy."""


@dataclass(frozen=True, slots=True)
class LoadedRecord:
    """One immutable record with normalized research-time metadata."""

    source_line: int
    event_time: datetime
    availability_time: datetime
    fields: tuple[tuple[str, str], ...]

    def value(self, field_name: str) -> str:
        """Return the original string value for one field."""

        for name, value in self.fields:
            if name == field_name:
                return value
        raise KeyError(field_name)


@dataclass(frozen=True, slots=True)
class LoadedDataset:
    """Immutable deterministic loader result."""

    dataset_id: str
    dataset_version: str
    source_location: str
    computed_sha256: str
    records: tuple[LoadedRecord, ...]
    source_row_count: int
    dropped_malformed_count: int
    duplicate_discard_count: int
    out_of_order_detected: bool
    missing_policy: MissingPolicy


def _parse_timestamp(value: str, *, field_name: str, source_line: int) -> datetime:
    if RFC3339_RE.fullmatch(value) is None:
        raise MalformedRowError(
            f"line {source_line}: invalid RFC3339 timestamp in {field_name}: {value!r}"
        )
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise MalformedRowError(
            f"line {source_line}: invalid RFC3339 timestamp in {field_name}: {value!r}"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise MalformedRowError(
            f"line {source_line}: timestamp in {field_name} must be timezone-aware"
        )
    return parsed


def _resolve_local_path(root: Path, location: str) -> Path:
    if "://" in location:
        raise DatasetLoadError("M2 base loader supports local file paths only")
    candidate = Path(location)
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate.resolve()


def _compute_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _required_fields(manifest: DatasetManifest) -> tuple[str, ...]:
    names = list(manifest.ordering.keys + manifest.ordering.tie_break_keys)
    names.append(manifest.time_semantics.event_time_field)
    names.append(manifest.time_semantics.availability_time_field)
    return tuple(dict.fromkeys(names))


def _record_key(record: LoadedRecord, manifest: DatasetManifest) -> tuple[datetime | str, ...]:
    parts: list[datetime | str] = []
    for field_name in manifest.ordering.keys + manifest.ordering.tie_break_keys:
        if field_name == manifest.time_semantics.event_time_field:
            parts.append(record.event_time)
        elif field_name == manifest.time_semantics.availability_time_field:
            parts.append(record.availability_time)
        else:
            parts.append(record.value(field_name))
    return tuple(parts)


def _parse_row(
    row: dict[str | None, str | None],
    *,
    header: tuple[str, ...],
    manifest: DatasetManifest,
    source_line: int,
) -> LoadedRecord:
    if None in row or any(value is None for value in row.values()):
        raise MalformedRowError(f"line {source_line}: malformed CSV field count")

    typed_row = {
        name: value
        for name, value in row.items()
        if name is not None and value is not None
    }

    for field_name in _required_fields(manifest):
        if not typed_row.get(field_name, "").strip():
            raise MalformedRowError(f"line {source_line}: required field is blank: {field_name}")

    event_field = manifest.time_semantics.event_time_field
    event_time = _parse_timestamp(
        typed_row[event_field],
        field_name=event_field,
        source_line=source_line,
    )

    if not (manifest.coverage.start <= event_time <= manifest.coverage.end):
        raise DatasetLoadError(
            f"line {source_line}: event time outside manifest coverage: {event_time.isoformat()}"
        )

    if manifest.time_semantics.availability_mode is AvailabilityMode.SAME_AS_EVENT_TIME:
        availability_time = event_time
    else:
        availability_field = manifest.time_semantics.availability_time_field
        availability_time = _parse_timestamp(
            typed_row[availability_field],
            field_name=availability_field,
            source_line=source_line,
        )

    fields = tuple((name, typed_row[name]) for name in header)
    return LoadedRecord(
        source_line=source_line,
        event_time=event_time,
        availability_time=availability_time,
        fields=fields,
    )


def _deduplicate(
    records: list[LoadedRecord],
    manifest: DatasetManifest,
) -> tuple[list[LoadedRecord], int]:
    policy = manifest.quality_policy.duplicates
    keyed = [(_record_key(record, manifest), record) for record in records]

    if policy is DuplicatePolicy.REJECT:
        seen: set[tuple[datetime | str, ...]] = set()
        for key, record in keyed:
            if key in seen:
                raise DatasetLoadError(
                    f"line {record.source_line}: duplicate ordering identity: {key!r}"
                )
            seen.add(key)
        return records, 0

    if policy is DuplicatePolicy.KEEP_FIRST:
        seen: set[tuple[datetime | str, ...]] = set()
        kept: list[LoadedRecord] = []
        for key, record in keyed:
            if key in seen:
                continue
            seen.add(key)
            kept.append(record)
        return kept, len(records) - len(kept)

    last_index: dict[tuple[datetime | str, ...], int] = {}
    for index, (key, _) in enumerate(keyed):
        last_index[key] = index
    kept = [record for index, (key, record) in enumerate(keyed) if last_index[key] == index]
    return kept, len(records) - len(kept)


def load_dataset(manifest: DatasetManifest, *, root: str | Path) -> LoadedDataset:
    """Load one local CSV dataset deterministically under a validated Manifest."""

    if manifest.storage.format != "CSV":
        raise DatasetLoadError(
            f"unsupported storage format for M2 base loader: {manifest.storage.format!r}"
        )
    if manifest.time_semantics.timestamp_representation != "RFC3339":
        raise DatasetLoadError(
            "M2 base loader supports timestamp_representation='RFC3339' only"
        )

    root_path = Path(root).resolve()
    source_path = _resolve_local_path(root_path, manifest.storage.location)
    if not source_path.is_file():
        raise DatasetLoadError(f"dataset file does not exist: {source_path}")

    computed_sha256 = _compute_sha256(source_path)
    if manifest.integrity.algorithm is IntegrityAlgorithm.SHA256:
        if computed_sha256 != manifest.integrity.digest:
            raise DatasetLoadError(
                "dataset SHA256 mismatch: "
                f"expected {manifest.integrity.digest}, got {computed_sha256}"
            )

    parsed_records: list[LoadedRecord] = []
    dropped_malformed = 0
    source_row_count = 0

    with source_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise DatasetLoadError("CSV header is missing")
        header = tuple(reader.fieldnames)
        if any(not name for name in header):
            raise DatasetLoadError("CSV header contains a blank field name")
        if len(header) != len(set(header)):
            raise DatasetLoadError("CSV header contains duplicate field names")

        missing_columns = [name for name in _required_fields(manifest) if name not in header]
        if missing_columns:
            raise DatasetLoadError(
                "CSV header missing Manifest-required fields: " + ", ".join(missing_columns)
            )

        for source_line, row in enumerate(reader, start=2):
            source_row_count += 1
            try:
                parsed_records.append(
                    _parse_row(
                        row,
                        header=header,
                        manifest=manifest,
                        source_line=source_line,
                    )
                )
            except MalformedRowError:
                if manifest.quality_policy.malformed is MalformedPolicy.DROP:
                    dropped_malformed += 1
                    continue
                raise

    records, duplicate_discard_count = _deduplicate(parsed_records, manifest)
    keys = [_record_key(record, manifest) for record in records]
    out_of_order_detected = any(
        current < previous for previous, current in zip(keys, keys[1:], strict=False)
    )

    if out_of_order_detected:
        if manifest.quality_policy.out_of_order is OutOfOrderPolicy.REJECT:
            raise DatasetLoadError("dataset rows violate the declared ordering contract")
        records = sorted(records, key=lambda record: _record_key(record, manifest))

    return LoadedDataset(
        dataset_id=manifest.dataset_id,
        dataset_version=manifest.dataset_version,
        source_location=manifest.storage.location,
        computed_sha256=computed_sha256,
        records=tuple(records),
        source_row_count=source_row_count,
        dropped_malformed_count=dropped_malformed,
        duplicate_discard_count=duplicate_discard_count,
        out_of_order_detected=out_of_order_detected,
        missing_policy=manifest.quality_policy.missing,
    )
