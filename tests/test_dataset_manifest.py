from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from ats.schemas.dataset_manifest import DatasetManifest, load_dataset_manifest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data" / "manifests" / "DATASET_TEMPLATE.yaml"


def template_mapping() -> dict:
    with TEMPLATE.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle)
    assert isinstance(loaded, dict)
    return loaded


def validate(data: dict) -> DatasetManifest:
    return DatasetManifest.model_validate(data)


def test_canonical_template_loads() -> None:
    manifest = load_dataset_manifest(TEMPLATE)

    assert manifest.dataset_id == "DATA-SYNTHETIC-M2-001"
    assert manifest.dataset_version == "1.0.0"
    assert manifest.ordering.keys == ("event_time",)
    assert manifest.ordering.tie_break_keys == ("sequence",)


def test_unknown_fields_are_rejected() -> None:
    data = template_mapping()
    data["unexpected"] = "not allowed"

    with pytest.raises(ValidationError):
        validate(data)


def test_naive_coverage_timestamp_is_rejected() -> None:
    data = template_mapping()
    data["coverage"]["start"] = "2026-01-01T00:00:00"

    with pytest.raises(ValidationError, match="timezone-aware"):
        validate(data)


def test_reversed_coverage_is_rejected() -> None:
    data = template_mapping()
    data["coverage"]["start"] = "2026-01-02T00:00:00Z"
    data["coverage"]["end"] = "2026-01-01T00:00:00Z"

    with pytest.raises(ValidationError, match="coverage.start"):
        validate(data)


def test_inconsistent_same_time_availability_is_rejected() -> None:
    data = template_mapping()
    data["time_semantics"]["availability_time_field"] = "published_at"

    with pytest.raises(ValidationError, match="SAME_AS_EVENT_TIME"):
        validate(data)


def test_explicit_availability_requires_distinct_field() -> None:
    data = template_mapping()
    data["time_semantics"]["availability_mode"] = "EXPLICIT_FIELD"

    with pytest.raises(ValidationError, match="EXPLICIT_FIELD"):
        validate(data)


def test_tie_break_is_required() -> None:
    data = template_mapping()
    data["ordering"]["tie_break_keys"] = []

    with pytest.raises(ValidationError):
        validate(data)


def test_event_time_must_be_first_ordering_key() -> None:
    data = template_mapping()
    data["ordering"]["keys"] = ["sequence", "event_time"]
    data["ordering"]["tie_break_keys"] = ["record_id"]

    with pytest.raises(ValidationError, match="first ordering key"):
        validate(data)


def test_ordering_and_tie_break_keys_must_not_overlap() -> None:
    data = template_mapping()
    data["ordering"]["tie_break_keys"] = ["event_time"]

    with pytest.raises(ValidationError, match="must not overlap"):
        validate(data)


def test_invalid_sha256_metadata_is_rejected() -> None:
    data = template_mapping()
    data["integrity"] = {
        "algorithm": "SHA256",
        "digest": "abc123",
        "reason": None,
    }

    with pytest.raises(ValidationError, match="64-hex"):
        validate(data)


def test_valid_sha256_metadata_is_accepted() -> None:
    data = template_mapping()
    data["integrity"] = {
        "algorithm": "SHA256",
        "digest": "a" * 64,
        "reason": None,
    }

    manifest = validate(data)

    assert manifest.integrity.digest == "a" * 64


def test_dataset_version_requires_semver() -> None:
    data = template_mapping()
    data["dataset_version"] = "v1"

    with pytest.raises(ValidationError, match="MAJOR.MINOR.PATCH"):
        validate(data)


def test_unsafe_yaml_tag_is_rejected(tmp_path: Path) -> None:
    unsafe = tmp_path / "unsafe.yaml"
    unsafe.write_text("!!python/object/apply:os.system ['echo unsafe']\n", encoding="utf-8")

    with pytest.raises(yaml.constructor.ConstructorError):
        load_dataset_manifest(unsafe)


def test_model_is_immutable() -> None:
    manifest = load_dataset_manifest(TEMPLATE)

    with pytest.raises(ValidationError):
        manifest.dataset_version = "2.0.0"


def test_template_mapping_helper_returns_independent_data() -> None:
    original = template_mapping()
    copied = deepcopy(original)
    copied["dataset_version"] = "2.0.0"

    assert original["dataset_version"] == "1.0.0"
