# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Последняя завершённая task:

`ATS2-M2-002 — Reproducible environment`.

Canonical specification:

`governance/program/RESEARCH_ENVIRONMENT_SPEC.md`.

M2 environment baseline: Linux x86_64, CPython `3.13.15`, uv `0.12.13`, exact locked Pydantic/PyYAML/NumPy/pytest/Ruff dependencies, `uv sync --frozen`, environment fingerprint and non-market baseline test.

Следующая ready task:

`ATS2-M2-003 — Dataset manifest support`.

Следующий artifact:

`governance/program/DATASET_MANIFEST_SPEC.md`.

## Canonical ATS v2

- Program governance: `governance/program/`;
- Architecture decisions: `governance/decisions/`;
- Methodology: `governance/methodology/`;
- Formal experiments and registry: `experiments/`;
- Data policy/manifests: `data/`;
- Source/platform code: `src/`;
- Execution queue: `governance/backlog/PROGRAM_BACKLOG_V2.md`;
- Legacy ATS v1: `legacy/v1/`.

## Быстрый старт

1. `AI_HANDOFF.md`.
2. `AGENTS.md`.
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
5. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. Environment: `governance/program/RESEARCH_ENVIRONMENT_SPEC.md`, `pyproject.toml`, `.python-version`, `uv.lock`.
7. Setup: `uv sync --frozen`.
8. Проверка repository: `uv run --frozen python tools/validate_repo.py`.
9. Environment test: `uv run --frozen pytest tests/test_environment_baseline.py`.

## Boundary

M2 materializes safe research infrastructure only. Reference Strategy #1, broker/live environment, capital and risk limits remain outside current scope. Dataset Manifest support is next; base loader/replay are not yet implemented.
