"""Typed Dataset Manifest boundary for ATS M2."""

from __future__ import annotations

import re
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATASET_ID_RE = re.compile(r"^DATA-[A-Z0-9][A-Z0-9_-]*-[0-9]{3}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class StrictModel(BaseModel):
    """Immutable boundary model with unknown fields rejected."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class AvailabilityMode(StrEnum):
    SAME_AS_EVENT_TIME = "SAME_AS_EVENT_TIME"
    EXPLICIT_FIELD = "EXPLICIT_FIELD"


class DuplicatePolicy(StrEnum):
    REJECT = "REJECT"
    KEEP_FIRST = "KEEP_FIRST"
    KEEP_LAST = "KEEP_LAST"


class MissingPolicy(StrEnum):
    REJECT = "REJECT"
    ALLOW_DECLARED_GAPS = "ALLOW_DECLARED_GAPS"


class MalformedPolicy(StrEnum):
    REJECT = "REJECT"
    DROP = "DROP"


class OutOfOrderPolicy(StrEnum):
    REJECT = "REJECT"
    SORT_BY_ORDERING_CONTRACT = "SORT_BY_ORDERING_CONTRACT"


class IntegrityAlgorithm(StrEnum):
    SHA256 = "SHA256"
    NOT_AVAILABLE = "NOT_AVAILABLE"


class SourceSpec(StrictModel):
    source_reference: str = Field(min_length=1)
    snapshot_reference: str = Field(min_length=1)


class StorageSpec(StrictModel):
    format: str = Field(min_length=1)
    location: str = Field(min_length=1)
    schema_reference: str = Field(min_length=1)


class CoverageSpec(StrictModel):
    start: datetime
    end: datetime
    scope: str = Field(min_length=1)

    @field_validator("start", "end")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("coverage timestamps must be timezone-aware")
        return value

    @model_validator(mode="after")
    def require_ordered_coverage(self) -> "CoverageSpec":
        if self.start > self.end:
            raise ValueError("coverage.start must be <= coverage.end")
        return self


class TimeSemantics(StrictModel):
    timezone: str = Field(min_length=1)
    timestamp_representation: str = Field(min_length=1)
    event_time_field: str = Field(min_length=1)
    availability_time_field: str = Field(min_length=1)
    availability_mode: AvailabilityMode

    @model_validator(mode="after")
    def validate_availability_contract(self) -> "TimeSemantics":
        same_field = self.event_time_field == self.availability_time_field
        if self.availability_mode is AvailabilityMode.SAME_AS_EVENT_TIME and not same_field:
            raise ValueError(
                "SAME_AS_EVENT_TIME requires availability_time_field == event_time_field"
            )
        if self.availability_mode is AvailabilityMode.EXPLICIT_FIELD and same_field:
            raise ValueError("EXPLICIT_FIELD requires a distinct availability_time_field")
        return self


class OrderingSpec(StrictModel):
    keys: tuple[str, ...] = Field(min_length=1)
    tie_break_keys: tuple[str, ...] = Field(min_length=1)
    direction: Literal["ASCENDING"]

    @field_validator("keys", "tie_break_keys")
    @classmethod
    def require_nonempty_unique_names(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if any(not value.strip() for value in values):
            raise ValueError("ordering keys must be non-empty")
        if len(values) != len(set(values)):
            raise ValueError("ordering keys must be unique")
        return values


class QualityPolicy(StrictModel):
    duplicates: DuplicatePolicy
    missing: MissingPolicy
    malformed: MalformedPolicy
    out_of_order: OutOfOrderPolicy


class TransformationLineage(StrictModel):
    parent_datasets: tuple[str, ...] = ()
    preparation_reference: str = Field(min_length=1)
    steps: tuple[str, ...] = ()

    @field_validator("parent_datasets", "steps")
    @classmethod
    def reject_blank_items(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if any(not value.strip() for value in values):
            raise ValueError("lineage list items must be non-empty")
        return values


class IntegritySpec(StrictModel):
    algorithm: IntegrityAlgorithm
    digest: str | None
    reason: str | None

    @model_validator(mode="after")
    def validate_integrity_contract(self) -> "IntegritySpec":
        if self.algorithm is IntegrityAlgorithm.SHA256:
            if self.digest is None or SHA256_RE.fullmatch(self.digest) is None:
                raise ValueError("SHA256 integrity requires a lowercase 64-hex digest")
            if self.reason is not None:
                raise ValueError("SHA256 integrity must not carry a NOT_AVAILABLE reason")
        else:
            if self.digest is not None:
                raise ValueError("NOT_AVAILABLE integrity requires digest: null")
            if self.reason is None or not self.reason.strip():
                raise ValueError("NOT_AVAILABLE integrity requires a non-empty reason")
        return self


class DatasetManifest(StrictModel):
    schema_version: Literal["2.0"]
    dataset_id: str
    dataset_version: str
    description: str = Field(min_length=1)
    source: SourceSpec
    storage: StorageSpec
    coverage: CoverageSpec
    time_semantics: TimeSemantics
    ordering: OrderingSpec
    quality_policy: QualityPolicy
    transformation_lineage: TransformationLineage
    integrity: IntegritySpec
    known_limitations: tuple[str, ...] = ()

    @field_validator("dataset_id")
    @classmethod
    def validate_dataset_id(cls, value: str) -> str:
        if DATASET_ID_RE.fullmatch(value) is None:
            raise ValueError("dataset_id must match DATA-<SOURCE>-<PURPOSE>-NNN")
        return value

    @field_validator("dataset_version")
    @classmethod
    def validate_dataset_version(cls, value: str) -> str:
        if SEMVER_RE.fullmatch(value) is None:
            raise ValueError("dataset_version must use MAJOR.MINOR.PATCH")
        return value

    @field_validator("known_limitations")
    @classmethod
    def reject_blank_limitations(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if any(not value.strip() for value in values):
            raise ValueError("known limitations must be non-empty strings")
        return values

    @model_validator(mode="after")
    def validate_ordering_contract(self) -> "DatasetManifest":
        if self.ordering.keys[0] != self.time_semantics.event_time_field:
            raise ValueError("event_time_field must be the first ordering key")
        all_keys = self.ordering.keys + self.ordering.tie_break_keys
        if len(all_keys) != len(set(all_keys)):
            raise ValueError("ordering keys and tie-break keys must not overlap")
        return self


def parse_dataset_manifest(data: Any) -> DatasetManifest:
    """Validate a parsed manifest mapping."""

    if not isinstance(data, dict):
        raise TypeError("Dataset Manifest top level must be a mapping")
    return DatasetManifest.model_validate(data)


def load_dataset_manifest(path: str | Path) -> DatasetManifest:
    """Load one UTF-8 YAML Dataset Manifest using safe parsing."""

    manifest_path = Path(path)
    with manifest_path.open("r", encoding="utf-8") as handle:
        parsed = yaml.safe_load(handle)
    return parse_dataset_manifest(parsed)


__all__ = [
    "DatasetManifest",
    "ValidationError",
    "load_dataset_manifest",
    "parse_dataset_manifest",
]
