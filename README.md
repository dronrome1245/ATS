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

`ATS2-M2-004 — Base data loader`.

Canonical specification:

`src/ats/data/loader.py`.

Dataset Manifest baseline: safe YAML + immutable Pydantic model, stable dataset ID/version, explicit time/availability/order/quality/lineage/integrity semantics, validated only with synthetic non-market metadata.

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
8. Один раз включить hooks: `git config core.hooksPath .githooks`.
9. Быстрая проверка: `uv run --frozen python tools/verify_repo.py --fast`.
10. Полный completion gate: `uv run --frozen python tools/verify_repo.py`.

## Quality gate

GitHub Actions не используется как completion gate. Политика: `governance/program/LOCAL_CI_GATE.md`. Полный локальный gate должен дать `ATS LOCAL CI: PASS` перед push material task.

## Boundary

M2 materializes safe research infrastructure only. Reference Strategy #1, broker/live environment, capital and risk limits remain outside current scope. Dataset Manifest is implemented; base data loader is next and replay is not yet implemented.
