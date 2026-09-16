# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- Real trading, demo, allocation and scaling remain disallowed.

## Last completed

`ATS2-M2-001 — Research stack ADR` — `DONE`.

Canonical artifact:

`governance/decisions/ADR-0001-RESEARCH-STACK.md`

Accepted M2 technology baseline:

- CPython 3.13 series;
- `pyproject.toml` + uv + committed `uv.lock`;
- Pydantic v2 + PyYAML at machine-contract boundaries;
- NumPy 2.x for baseline numerical analytics;
- typed ordered-record/event replay contract, not DataFrame-first core semantics;
- initial CSV/JSON/YAML formats behind interfaces;
- pytest + Ruff quality gates;
- planned package boundary `src/ats/{schemas,data,strategy,replay,costs,analytics,runner}`.

Deferred until a real consumer requires them: pandas, Polars, PyArrow, DuckDB, external backtesting frameworks, mandatory Docker, Rust/C++ core, broker/live adapters, news ingestion, portfolio/distributed infrastructure.

Reference Strategy #1 is still not selected.

## Current ready task

`ATS2-M2-002 — Reproducible environment`

Canonical next artifact:

`governance/program/RESEARCH_ENVIRONMENT_SPEC.md`

Required executable environment artifacts:

- `pyproject.toml`;
- `.python-version`;
- committed `uv.lock`.

Goal: pin the exact runtime/dependency environment and documented `uv sync` / `uv run` workflow before implementing later M2 platform capabilities.

## M2-002 must define/materialize

- exact CPython 3.13 patch;
- project metadata / `requires-python`;
- exact runtime/dev dependency resolution;
- frozen uv lock workflow;
- clean environment setup command;
- canonical validator/test/lint/format commands;
- environment/version fingerprint;
- CI boundary for governance validator versus platform tests;
- update policy for Python/dependency/lock changes.

Do not implement Dataset Manifest/loader/Strategy API/replay as part of M2-002 except minimal scaffolding required to prove environment/tool execution.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/decisions/ADR-0001-RESEARCH-STACK.md`.
6. `governance/program/REFERENCE_CONSUMER_PROFILE.md`.
7. `governance/program/PROGRAM_WBS_V2.md`.
8. `.github/workflows/validate.yml` and repository tool/readme files as needed.

## Boundary

M2 builds research infrastructure only. Do not select Reference Strategy #1, market, instrument, broker, jurisdiction, capital allocation, risk limits or live environment.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last completed: `ATS2-M2-001`.
- Next task: `ATS2-M2-002`.
- Next artifact: `governance/program/RESEARCH_ENVIRONMENT_SPEC.md`.
- Stack ADR accepted? — yes.
- Reference Strategy #1 selection allowed now? — no.
- Pipeline counts remain zero? — yes.
