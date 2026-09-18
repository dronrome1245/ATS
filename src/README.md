# Source code

ATS is in `M2_RESEARCH_PLATFORM_MVP`.

Canonical stack decision:

`governance/decisions/ADR-0001-RESEARCH-STACK.md`

Canonical materialized environment:

`governance/program/RESEARCH_ENVIRONMENT_SPEC.md`

M2 source code uses:

- CPython `3.13.15` as the exact reproducibility baseline;
- uv `0.12.13` + `pyproject.toml` + committed `uv.lock`;
- Pydantic `2.13.5` + PyYAML `6.0.3` at manifest/config boundaries;
- NumPy `2.5.3` for baseline numerical analytics;
- standard-library CSV/JSON and a typed ordered-record interface for the initial loader/replay path;
- pytest `9.1.1` + Ruff `0.16.7` for the current quality baseline.

Planned package boundary:

```text
src/ats/
├── schemas/
├── data/
├── strategy/
├── replay/
├── costs/
├── analytics/
└── runner/
```

M2 is not DataFrame-first and does not baseline pandas, Polars, PyArrow, DuckDB, an external backtesting framework, Docker, broker adapters or live execution. Such capabilities are added only after a real consumer demonstrates the need.

A concrete Reference Strategy #1 is not selected until M3. Deterministic synthetic software fixtures used for platform tests are not research entities or trading evidence.

The environment baseline, Dataset Manifest boundary and base data loader are complete at repository-artifact level. The next program-level implementation step after M2-004 Local CI PASS is `ATS2-M2-005 — Minimal Strategy research interface`; replay remains a later work package.


## Implemented M2 boundary

`ATS2-M2-003` materializes the first typed platform boundary:

- `ats.schemas.dataset_manifest.DatasetManifest`;
- `ats.schemas.dataset_manifest.load_dataset_manifest`;
- safe YAML parsing plus immutable Pydantic validation;
- explicit event-time / information-availability semantics;
- deterministic ordering/tie-break metadata;
- quality, lineage and integrity metadata.

`ATS2-M2-004 — Base data loader` is now materialized in `ats.data.loader`. It consumes the Dataset Manifest contract rather than inventing dataset semantics in code.


## Base loader boundary

Implemented loader behavior:

- immutable `LoadedRecord` / `LoadedDataset`;
- UTF-8 CSV reference format;
- RFC3339 timezone-aware event and availability times;
- deterministic ordering and tie-breaks;
- explicit duplicate/malformed/out-of-order policies;
- SHA-256 integrity verification;
- manifest coverage enforcement;
- stable manifest storage location in output instead of host-specific absolute paths.

Generic missing-event inference is intentionally absent because the Manifest does not define a universal calendar/frequency.

The next implementation boundary is `ATS2-M2-005 — Minimal Strategy research interface`, expected under `src/ats/strategy/`.
