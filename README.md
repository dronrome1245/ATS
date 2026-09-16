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

`ATS2-M2-001 — Research stack ADR`.

Artifact:

`governance/decisions/ADR-0001-RESEARCH-STACK.md`.

M2 baseline: CPython 3.13, uv/pyproject/uv.lock, Pydantic v2 + PyYAML, NumPy 2.x, typed ordered-record replay semantics, pytest + Ruff. DataFrame-first/live/broker/heavy distributed stacks не входят в baseline.

Следующая ready task:

`ATS2-M2-002 — Reproducible environment`.

Следующий artifact:

`governance/program/RESEARCH_ENVIRONMENT_SPEC.md`.

Executable environment artifacts: `pyproject.toml`, `.python-version`, committed `uv.lock`.

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
6. Для текущей работы: `governance/decisions/ADR-0001-RESEARCH-STACK.md` и `governance/program/REFERENCE_CONSUMER_PROFILE.md`.
7. Проверка repository: `python tools/validate_repo.py`.

## Boundary

M2 materializes safe research infrastructure only. Reference Strategy #1, broker/live environment, capital and risk limits remain outside current scope.
