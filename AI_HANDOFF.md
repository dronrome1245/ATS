# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- Real trading, demo, allocation and scaling remain disallowed.

## Last implemented work package

`ATS2-M2-004 — Base data loader`.

Primary artifact:

`src/ats/data/loader.py`

Materialized loader boundary:

- immutable `LoadedRecord` / `LoadedDataset`;
- UTF-8 CSV reference format;
- RFC3339 timezone-aware event/availability parsing;
- deterministic event-time + declared tie-break ordering;
- duplicate `REJECT / KEEP_FIRST / KEEP_LAST`;
- malformed `REJECT / DROP`;
- out-of-order `REJECT / SORT_BY_ORDERING_CONTRACT`;
- Manifest coverage enforcement;
- optional SHA-256 byte verification;
- generic missing/gap policy preserved without inventing market calendar/frequency semantics.

Canonical synthetic fixtures:

- `tests/fixtures/datasets/ordered_events.manifest.yaml`;
- `tests/fixtures/datasets/ordered_events.csv`;
- `tests/fixtures/datasets/ordered_events.schema.json`;
- `tests/test_data_loader.py`.

Fixture CSV line endings are pinned to LF through `.gitattributes` for cross-platform SHA-256 reproducibility.

This is software/platform capability only. It is not market data or research evidence.

## M2-004 closure check

Windows OWNER workflow:

`ATS_TASK_CHECK.bat`

The stable BAT updates the repository, runs frozen environment sync, then executes `tools/current_task_check.py`.

Current task checker is configured for:

`ATS2-M2-004 — Base data loader`

It runs:

1. `tests/test_data_loader.py`;
2. repository validator;
3. full ATS Local CI.

Shareable report:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

M2-004 is considered finally closed only after this report shows PASS on the exact final HEAD.

## Current ready task after M2-004 PASS

`ATS2-M2-005 — Minimal Strategy research interface`

Canonical next artifact:

`src/ats/strategy/interface.py`

Goal: define the minimum broker-agnostic research interface that consumes immutable ordered observations and emits serializable deterministic decisions.

Do not implement replay/backtest, cost model, analytics, broker/live integration or Reference Strategy #1 in M2-005.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/DATASET_MANIFEST_SPEC.md`.
6. `src/ats/schemas/dataset_manifest.py`.
7. `src/ats/data/loader.py`.
8. `tests/test_data_loader.py`.
9. `governance/program/REFERENCE_CONSUMER_PROFILE.md`.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last implemented task: `ATS2-M2-004`.
- Closure checker: `ATS2-M2-004`.
- Next task after PASS: `ATS2-M2-005`.
- Next artifact: `src/ats/strategy/interface.py`.
- Reference Strategy #1 selection allowed now? — no.
- Pipeline counts remain zero? — yes.
