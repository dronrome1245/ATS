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

`ATS2-M2-002 — Reproducible environment` — `DONE`.

Canonical specification:

`governance/program/RESEARCH_ENVIRONMENT_SPEC.md`

Materialized environment artifacts:

- `.python-version` → CPython `3.13.15`;
- `pyproject.toml` → Python `>=3.13,<3.14`, uv `0.12.13`, exact direct dependency pins and Linux x86_64 resolution environment;
- `uv.lock` → exact dependency graph plus install wheel URLs/SHA-256 for the canonical host;
- `tools/environment_fingerprint.py`;
- `tests/test_environment_baseline.py`;
- `.github/workflows/validate.yml` → frozen uv workflow.

Canonical host/runtime baseline:

- Linux x86_64;
- CPython `3.13.15`;
- uv `0.12.13`;
- Pydantic `2.13.5`;
- PyYAML `6.0.3`;
- NumPy `2.5.3`;
- pytest `9.1.1`;
- Ruff `0.16.7`.

Canonical environment commands:

```bash
uv python install 3.13.15
uv sync --frozen
uv run --frozen python tools/validate_repo.py
uv run --frozen pytest tests/test_environment_baseline.py
uv run --frozen python tools/environment_fingerprint.py
uv run --frozen ruff check tools/environment_fingerprint.py tests/test_environment_baseline.py
```

The lock is structurally compatible with uv frozen-sync selection on Linux x86_64. Offline empty-cache verification stops only because locked wheel bytes cannot be downloaded, not because a compatible locked distribution is absent.

## Current ready task

`ATS2-M2-003 — Dataset manifest support`

Canonical next artifact:

`governance/program/DATASET_MANIFEST_SPEC.md`

Expected implementation boundary:

- `data/manifests/DATASET_TEMPLATE.yaml`;
- `src/ats/schemas/dataset_manifest.py`;
- schema/validation tests using synthetic non-market fixtures.

## M2-003 must define

- stable Dataset ID/version and material-change rules;
- source/source-snapshot reference without inventing a vendor;
- schema/storage reference;
- coverage/scope metadata;
- timezone and timestamp representation;
- observation/event time versus information-availability time;
- deterministic ordering/tie-break semantics;
- duplicate/missing/malformed/out-of-order policy;
- transformation lineage;
- checksum/integrity metadata;
- known limitations/research impact;
- external/raw data reference policy;
- safe YAML + Pydantic validation.

M2-003 must not implement the base loader beyond the minimum needed to parse/validate a Manifest.

## CI operational note

Recent GitHub-hosted Actions attempts before M2-002 ended before any step ran (`runner_id=0`, `steps=[]`). Treat such a run as infrastructure/scheduling failure, not repository validation evidence. The current workflow is configured for the frozen environment and should be evaluated only when a runner actually executes its steps.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/RESEARCH_ENVIRONMENT_SPEC.md`.
6. `governance/decisions/ADR-0001-RESEARCH-STACK.md`.
7. `governance/program/REFERENCE_CONSUMER_PROFILE.md`.
8. `data/README.md` and M1 Data Feasibility methodology.

## Boundary

M2 builds research infrastructure only. Do not select Reference Strategy #1, market, instrument, broker, jurisdiction, capital allocation, risk limits or live environment.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last completed: `ATS2-M2-002`.
- Next task: `ATS2-M2-003`.
- Next artifact: `governance/program/DATASET_MANIFEST_SPEC.md`.
- Canonical Python/host? — `CPython 3.13.15 / Linux x86_64`.
- Reference Strategy #1 selection allowed now? — no.
- Pipeline counts remain zero? — yes.
