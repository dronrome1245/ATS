# ATS M2 Dataset Manifest Specification

**Task:** `ATS2-M2-003`  
**Work package:** `WBS-2.3`  
**Status:** BASELINE  
**Consumer contract:** `governance/program/REFERENCE_CONSUMER_PROFILE.md`  
**Environment:** `governance/program/RESEARCH_ENVIRONMENT_SPEC.md`

## 1. Purpose

Dataset Manifest is the canonical machine-readable identity and semantics contract for one research dataset version.

It answers: **what data version is this, where did it come from, what does time mean, how is deterministic order defined, what preparation occurred, and what integrity/limitations are known?**

A Manifest is metadata. It is not the dataset itself, does not replace Data Feasibility Review, and does not create research evidence.

## 2. Boundary

M2-003 defines and validates Dataset Manifest metadata only.

It does not:

- select a market, instrument, vendor or Reference Strategy #1;
- download or ingest market data;
- implement the base data loader beyond reading/parsing the manifest file itself;
- verify dataset bytes against a checksum at runtime;
- implement replay, Strategy API, costs or analytics;
- create Idea/Hypothesis/Candidate/Experiment records.

Synthetic non-market fixtures are used only to test schema behavior.

## 3. Canonical artifacts

- specification: `governance/program/DATASET_MANIFEST_SPEC.md`;
- template: `data/manifests/DATASET_TEMPLATE.yaml`;
- typed boundary: `src/ats/schemas/dataset_manifest.py`;
- tests: `tests/test_dataset_manifest.py`.

The YAML file is loaded only with `yaml.safe_load`. The loaded mapping is validated by Pydantic v2 with unknown fields rejected.

## 4. Identity and versioning

Each manifest contains:

- `dataset_id` — stable logical dataset identity using canonical `DATA-<SOURCE>-<PURPOSE>-NNN` naming;
- `dataset_version` — immutable semantic version in `MAJOR.MINOR.PATCH` form;
- human-readable description.

The pair `dataset_id + dataset_version` identifies one immutable research-data context.

A **material data change requires a new dataset version**. Material changes include, as applicable:

- different source snapshot;
- coverage change;
- schema/field semantic change;
- timestamp or information-availability semantic change;
- ordering/tie-break change;
- duplicate/missing/malformed handling change;
- transformation/preparation change;
- changed dataset bytes when integrity identity is expected to remain frozen.

A manifest must never be silently edited to make a completed historical experiment appear to have used a later dataset version.

## 5. Source and storage reference

The manifest records:

- `source_reference` — source/provenance locator or descriptive source identity;
- `snapshot_reference` — immutable or versioned snapshot reference;
- `format` — storage/reference format;
- `location` — local or external locator without credentials;
- `schema_reference` — schema or field-definition identity.

Large, private or licensed data remains outside Git. Git stores the manifest, not credentials or restricted bytes.

## 6. Coverage

Coverage contains timezone-aware `start` and `end` timestamps and a scope description.

Rules:

- both timestamps must carry timezone information;
- `start <= end`;
- coverage describes the represented dataset version, not a trading recommendation or experiment result.

## 7. Time and information availability semantics

The manifest explicitly separates:

- `event_time_field` — observation/event timestamp;
- `availability_time_field` — timestamp at which the information is available to research logic;
- `availability_mode`.

Supported M2 modes:

- `SAME_AS_EVENT_TIME` — availability field must equal event-time field;
- `EXPLICIT_FIELD` — availability field must be distinct and supplied by the dataset.

The manifest also records a documented timezone label and timestamp representation.

No research component may silently assume event time equals information-availability time.

## 8. Deterministic ordering

The manifest defines:

- ordered `keys`;
- one or more `tie_break_keys`;
- direction, currently `ASCENDING`.

Rules:

- event time must be the first ordering key;
- tie-break keys are mandatory;
- key names must be unique across the combined ordering contract.

This makes equal-time ordering explicit before the base loader is implemented.

## 9. Data-quality policy

M2 records explicit policies for:

- duplicate records;
- missing records/gaps;
- malformed records;
- out-of-order records.

Allowed baseline policies are deliberately small:

- duplicates: `REJECT | KEEP_FIRST | KEEP_LAST`;
- missing: `REJECT | ALLOW_DECLARED_GAPS`;
- malformed: `REJECT | DROP`;
- out-of-order: `REJECT | SORT_BY_ORDERING_CONTRACT`.

The Manifest declares policy. WBS-2.4 implements the loader behavior.

## 10. Transformation lineage

Transformation metadata contains:

- zero or more parent dataset references;
- preparation/code/reference identity;
- ordered human-readable transformation steps.

A raw/identity dataset may have no parents and no transformation steps, but the preparation reference must still make that explicit.

Any material preparation change creates a new dataset version.

## 11. Integrity metadata

Integrity metadata supports:

### SHA-256 available

- `algorithm: SHA256`;
- lowercase 64-hex `digest`;
- `reason: null`.

### Integrity not available

- `algorithm: NOT_AVAILABLE`;
- `digest: null`;
- non-empty `reason`.

M2-003 validates this metadata structurally. Actual byte verification is performed by the loader/integrity path in WBS-2.4 or later.

## 12. Known limitations

`known_limitations` is an explicit list of known gaps, biases, scope restrictions or other research-impacting limitations.

An empty list means no limitation has been recorded, not that the dataset is proven complete or unbiased.

Data Feasibility Review remains responsible for hypothesis-specific assessment of survivorship, selection bias, leakage and adequacy.

## 13. Safe parsing and failure behavior

`load_dataset_manifest(path)`:

1. reads UTF-8 text;
2. uses `yaml.safe_load`;
3. requires one top-level mapping;
4. validates through the immutable Pydantic model;
5. rejects unknown fields and inconsistent cross-field semantics.

Malformed or unsafe YAML fails closed.

## 14. Structural acceptance

The M2-003 test suite must demonstrate at least:

- canonical synthetic template loads successfully;
- unknown fields are rejected;
- naive coverage timestamps are rejected;
- reversed coverage is rejected;
- inconsistent availability semantics are rejected;
- missing deterministic tie-break is rejected;
- event time not first in ordering is rejected;
- invalid SHA-256 metadata is rejected;
- unsafe YAML tags are rejected.

These are software/schema tests only and are not trading evidence.

## 15. Definition of Done

M2-003 is complete when:

- specification, template, typed model/loader and tests are committed;
- Dataset Manifest semantics satisfy the Reference Consumer Profile;
- material-change/new-version policy is explicit;
- no real market/vendor/instrument facts were invented;
- validator and project entrypoints are synchronized;
- state/backlog/handoff advance to `ATS2-M2-004 — Base data loader`;
- the exact final commit passes the full Local CI Gate.
