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
- `pyproject.toml` → Python `>=3.13,<3.14`, uv `0.12.13`, exact direct dependency pins and Windows x86_64 + Linux x86_64 resolution environments;
- `uv.lock` → exact dependency graph plus Windows x86_64 and Linux x86_64 wheel URLs/SHA-256;
- `tools/environment_fingerprint.py`;
- `tests/test_environment_baseline.py`;
- `governance/program/LOCAL_CI_GATE.md` → canonical local quality policy;
- `tools/verify_repo.py` → full/fast Local CI runner;
- `.githooks/pre-commit` / `.githooks/pre-push` → automatic local gates.

Canonical host/runtime baseline:

- primary local host: Windows x86_64;
- supported secondary host: Linux x86_64;
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
uv run --frozen python tools/verify_repo.py --fast
uv run --frozen python tools/verify_repo.py
```

The lock contains compatible wheels for Windows x86_64 and Linux x86_64 for all platform-specific baseline dependencies.

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

## Local quality gate

GitHub Actions is intentionally not used as a completion gate. Enable repository hooks once per clone with `git config core.hooksPath .githooks`. The full canonical gate is `uv run --frozen python tools/verify_repo.py`; material work requires `ATS LOCAL CI: PASS` on the exact commit before push. Local runtime report: `reports/local_ci/LATEST.json` (gitignored).

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
- Canonical Python/hosts? — `CPython 3.13.15 / Windows x86_64 + Linux x86_64`.
- Reference Strategy #1 selection allowed now? — no.
- Pipeline counts remain zero? — yes.
