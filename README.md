# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M1_RESEARCH_METHODOLOGY / IN_PROGRESS`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Последняя завершённая task:

`ATS2-M1-008 — Experiment registry`.

Artifacts:

- `experiments/REGISTRY.csv`;
- registry rules: `experiments/README.md`;
- search CLI: `tools/search_experiments.py`.

Registry имеет один durable row на реальный `EXP-...`, сохраняет negative/cancelled/superseded history и индексирует canonical package без дублирования manifest/result/conclusion. Initial registry содержит zero fictitious rows.

Следующая ready task:

`ATS2-M1-009 — Evidence taxonomy operationalization`.

Следующий artifact:

`governance/methodology/EVIDENCE_TAXONOMY.md`.

## Canonical ATS v2

- Program governance: `governance/program/`;
- Methodology: `governance/methodology/`;
- Research templates: `governance/methodology/templates/`;
- Formal experiments and registry: `experiments/`;
- Execution queue: `governance/backlog/PROGRAM_BACKLOG_V2.md`;
- Legacy ATS v1: `legacy/v1/`.

## Быстрый старт

1. `AI_HANDOFF.md`.
2. `AGENTS.md`.
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
5. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. Для текущей работы: `governance/methodology/RESEARCH_METHODOLOGY_V1.md`, `governance/methodology/EXPERIMENT_REGISTRATION.md`, `experiments/README.md`.
7. Поиск experiments: `python tools/search_experiments.py --help`.
8. Проверка repository: `python tools/validate_repo.py`.

## Boundary

Searchable Registry is an index, not evidence promotion. A `REGISTERED_EXPERIMENT` is preregistered but not automatically validation evidence. Reference Strategy #1, broker, capital, live risk limits and production execution are not selected at this stage.
