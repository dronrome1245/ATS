from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ats.data.loader import DatasetLoadError, load_dataset
from ats.schemas.dataset_manifest import DatasetManifest, MissingPolicy, load_dataset_manifest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "datasets"
MANIFEST_PATH = FIXTURE_DIR / "ordered_events.manifest.yaml"


def fixture_mapping() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle)
    assert isinstance(loaded, dict)
    return loaded


def manifest_for(
    tmp_path: Path,
    csv_text: str,
    *,
    duplicates: str = "REJECT",
    malformed: str = "REJECT",
    out_of_order: str = "REJECT",
    integrity_algorithm: str = "NOT_AVAILABLE",
    integrity_digest: str | None = None,
    availability_mode: str = "SAME_AS_EVENT_TIME",
    availability_field: str = "event_time",
    storage_format: str = "CSV",
) -> DatasetManifest:
    csv_path = tmp_path / "events.csv"
    csv_path.write_text(csv_text, encoding="utf-8")

    data = fixture_mapping()
    data["storage"]["location"] = "events.csv"
    data["storage"]["format"] = storage_format
    data["quality_policy"]["duplicates"] = duplicates
    data["quality_policy"]["malformed"] = malformed
    data["quality_policy"]["out_of_order"] = out_of_order
    data["time_semantics"]["availability_mode"] = availability_mode
    data["time_semantics"]["availability_time_field"] = availability_field
    data["integrity"] = {
        "algorithm": integrity_algorithm,
        "digest": integrity_digest,
        "reason": None if integrity_algorithm == "SHA256" else "Test fixture integrity disabled.",
    }
    return DatasetManifest.model_validate(data)


def test_reference_fixture_loads_deterministically() -> None:
    manifest = load_dataset_manifest(MANIFEST_PATH)

    first = load_dataset(manifest, root=ROOT)
    second = load_dataset(manifest, root=ROOT)

    assert first == second
    assert first.dataset_id == "DATA-SYNTHETIC-LOADER-001"
    assert first.source_row_count == 3
    assert first.dropped_malformed_count == 0
    assert first.duplicate_discard_count == 0
    assert first.out_of_order_detected is False
    assert first.missing_policy is MissingPolicy.ALLOW_DECLARED_GAPS
    assert [record.value("value") for record in first.records] == ["alpha", "beta", "gamma"]
    assert first.records[0].event_time == first.records[0].availability_time


def test_sha256_mismatch_is_rejected(tmp_path: Path) -> None:
    manifest = manifest_for(
        tmp_path,
        "event_time,sequence,value\n2026-01-01T00:00:00Z,0001,alpha\n",
        integrity_algorithm="SHA256",
        integrity_digest="0" * 64,
    )

    with pytest.raises(DatasetLoadError, match="SHA256 mismatch"):
        load_dataset(manifest, root=tmp_path)


def test_out_of_order_reject_policy_fails(tmp_path: Path) -> None:
    manifest = manifest_for(
        tmp_path,
        (
            "event_time,sequence,value\n"
            "2026-01-01T00:01:00Z,0001,later\n"
            "2026-01-01T00:00:00Z,0001,earlier\n"
        ),
    )

    with pytest.raises(DatasetLoadError, match="ordering contract"):
        load_dataset(manifest, root=tmp_path)


def test_out_of_order_sort_policy_is_deterministic(tmp_path: Path) -> None:
    manifest = manifest_for(
        tmp_path,
        (
            "event_time,sequence,value\n"
            "2026-01-01T00:01:00Z,0001,later\n"
            "2026-01-01T00:00:00Z,0002,second\n"
            "2026-01-01T00:00:00Z,0001,first\n"
        ),
        out_of_order="SORT_BY_ORDERING_CONTRACT",
    )

    loaded = load_dataset(manifest, root=tmp_path)

    assert loaded.out_of_order_detected is True
    assert [record.value("value") for record in loaded.records] == ["first", "second", "later"]


def test_duplicate_reject_policy_fails(tmp_path: Path) -> None:
    manifest = manifest_for(
        tmp_path,
        (
            "event_time,sequence,value\n"
            "2026-01-01T00:00:00Z,0001,alpha\n"
            "2026-01-01T00:00:00Z,0001,omega\n"
        ),
    )

    with pytest.raises(DatasetLoadError, match="duplicate ordering identity"):
        load_dataset(manifest, root=tmp_path)


@pytest.mark.parametrize(
    ("policy", "expected"),
    [("KEEP_FIRST", "alpha"), ("KEEP_LAST", "omega")],
)
def test_duplicate_keep_policies_are_explicit(
    tmp_path: Path,
    policy: str,
    expected: str,
) -> None:
    manifest = manifest_for(
        tmp_path,
        (
            "event_time,sequence,value\n"
            "2026-01-01T00:00:00Z,0001,alpha\n"
            "2026-01-01T00:00:00Z,0001,omega\n"
        ),
        duplicates=policy,
    )

    loaded = load_dataset(manifest, root=tmp_path)

    assert loaded.duplicate_discard_count == 1
    assert len(loaded.records) == 1
    assert loaded.records[0].value("value") == expected


def test_malformed_reject_policy_fails(tmp_path: Path) -> None:
    manifest = manifest_for(
        tmp_path,
        (
            "event_time,sequence,value\n"
            "not-a-time,0001,bad\n"
        ),
    )

    with pytest.raises(DatasetLoadError, match="invalid RFC3339 timestamp"):
        load_dataset(manifest, root=tmp_path)


def test_malformed_drop_policy_counts_dropped_rows(tmp_path: Path) -> None:
    manifest = manifest_for(
        tmp_path,
        (
            "event_time,sequence,value\n"
            "not-a-time,0001,bad\n"
            "2026-01-01T00:00:00Z,0002,good\n"
        ),
        malformed="DROP",
    )

    loaded = load_dataset(manifest, root=tmp_path)

    assert loaded.source_row_count == 2
    assert loaded.dropped_malformed_count == 1
    assert [record.value("value") for record in loaded.records] == ["good"]


def test_explicit_availability_field_is_parsed(tmp_path: Path) -> None:
    manifest = manifest_for(
        tmp_path,
        (
            "event_time,published_at,sequence,value\n"
            "2026-01-01T00:00:00Z,2026-01-01T00:00:05Z,0001,alpha\n"
        ),
        availability_mode="EXPLICIT_FIELD",
        availability_field="published_at",
    )

    loaded = load_dataset(manifest, root=tmp_path)

    assert loaded.records[0].availability_time.isoformat() == "2026-01-01T00:00:05+00:00"


def test_event_outside_manifest_coverage_is_rejected(tmp_path: Path) -> None:
    manifest = manifest_for(
        tmp_path,
        (
            "event_time,sequence,value\n"
            "2026-01-01T00:02:00Z,0001,outside\n"
        ),
    )

    with pytest.raises(DatasetLoadError, match="outside manifest coverage"):
        load_dataset(manifest, root=tmp_path)


def test_missing_required_header_is_rejected(tmp_path: Path) -> None:
    manifest = manifest_for(
        tmp_path,
        "event_time,value\n2026-01-01T00:00:00Z,alpha\n",
    )

    with pytest.raises(DatasetLoadError, match="missing Manifest-required fields"):
        load_dataset(manifest, root=tmp_path)


def test_unsupported_storage_format_is_rejected(tmp_path: Path) -> None:
    manifest = manifest_for(
        tmp_path,
        "event_time,sequence,value\n2026-01-01T00:00:00Z,0001,alpha\n",
        storage_format="JSON",
    )

    with pytest.raises(DatasetLoadError, match="unsupported storage format"):
        load_dataset(manifest, root=tmp_path)
