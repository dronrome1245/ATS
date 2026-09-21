# Data

## Purpose

`data/` stores Dataset Manifests, provenance and data-control metadata for ATS v2. Large, licensed or broker/vendor datasets are not committed to Git merely because a research run uses them.

## ATS v2 data rules

Every dataset used for formal research must become identifiable through a manifest that records, as applicable:

- stable dataset ID/version;
- source or source-snapshot reference;
- schema/reference format;
- coverage/period;
- timezone and timestamp semantics;
- ordering/tie-breaking semantics;
- missing/bad/duplicate-data policy;
- transformation/preparation reference;
- checksum/hash where practical;
- known limitations and licensing/storage constraints.

A material cleaning/transformation change creates a new dataset version/context rather than silently changing historical evidence.

Development, validation and independent evidence partitions are governed by the current Research Methodology and Strategy Lifecycle. A protected evidence block stops being independent after it is revealed/used for the corresponding decision.

## M2 boundary

`WBS-2.3` Dataset Manifest support and `WBS-2.4` deterministic base loader are implemented at repository-artifact level.

M2 may use synthetic non-market fixtures for software tests. Such fixtures are platform-test inputs only: they do not receive research entity/Experiment IDs and are not trading evidence.

M3 introduced the first real research dataset: Dukascopy EUR/USD 1H BID/ASK for 2021–2025. Its canonical manifest is `data/manifests/DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml`. Raw licensed/vendor files remain outside Git; the repository retains identity, transformation and integrity metadata.


## Dataset Manifest implementation

Canonical M2 Dataset Manifest contract:

- `governance/program/DATASET_MANIFEST_SPEC.md`;
- template: `data/manifests/DATASET_TEMPLATE.yaml`;
- typed validator: `src/ats/schemas/dataset_manifest.py`;
- tests: `tests/test_dataset_manifest.py`.

The Manifest stores dataset identity and semantics, not licensed/raw dataset bytes. Material source/coverage/schema/time/order/quality/transformation changes require a new `dataset_version`.

M2-003 uses only synthetic non-market template data. M2-004 now provides deterministic record loading and optional runtime SHA-256 verification.


## Base data loader

`ATS2-M2-004` implements the minimum deterministic reference-format loader in:

`src/ats/data/loader.py`

Current baseline:

- local UTF-8 CSV only;
- explicit repository/root resolution, no hidden current-directory dependency;
- RFC3339 timezone-aware event/availability parsing from Dataset Manifest semantics;
- event-time first ordering plus declared tie-break keys;
- non-time ordering/tie-break fields use their exact source strings in the M2 reference format;
- duplicate policy: `REJECT | KEEP_FIRST | KEEP_LAST`;
- malformed policy: `REJECT | DROP`;
- out-of-order policy: `REJECT | SORT_BY_ORDERING_CONTRACT`;
- optional SHA-256 byte verification;
- coverage violations always block loading and cannot be hidden by `malformed: DROP`;
- missing/gap policy is carried into the immutable loader result but generic M2 does not invent a calendar/frequency to infer absent records.

Canonical synthetic fixture:

- `tests/fixtures/datasets/ordered_events.manifest.yaml`;
- `tests/fixtures/datasets/ordered_events.csv`;
- `tests/fixtures/datasets/ordered_events.schema.json`.

The CSV fixture is pinned to LF in `.gitattributes` so SHA-256 is stable across Windows and Linux checkouts.

These fixtures are software tests only and are not research evidence.


## M3 real-data learning

Reference Strategy #1 demonstrated that a generic hourly frequency is not enough to define tradable observations for FX. The preparation path had to remove closed-market weekend hours and test daylight-saving boundaries explicitly.

The prepared EUR/USD dataset contains 31,296 expected tradable H1 rows with zero missing expected tradable hours. It is bound by SHA-256 in the Dataset Manifest. This dataset supported one exploratory prototype that was rejected; the data record is retained for reproducibility, not as proof of edge.
