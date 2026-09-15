# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M1_RESEARCH_METHODOLOGY / IN_PROGRESS`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Последняя завершённая task:

`ATS2-M1-007 — Experiment registration schema`.

Artifact:

`governance/methodology/EXPERIMENT_REGISTRATION.md`.

Experiment templates теперь разделяют preregistration (`manifest.yaml`), observed result (`result.json`) и interpretation/decision (`conclusion.md`).

Следующая ready task:

`ATS2-M1-008 — Experiment registry`.

Следующий artifact:

`experiments/REGISTRY.csv`.

## Canonical ATS v2

- Program governance: `governance/program/`;
- Methodology: `governance/methodology/`;
- Research templates: `governance/methodology/templates/`;
- Formal experiments: `experiments/`;
- Execution queue: `governance/backlog/PROGRAM_BACKLOG_V2.md`;
- Legacy ATS v1: `legacy/v1/`.

## Быстрый старт

1. `AI_HANDOFF.md`.
2. `AGENTS.md`.
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
5. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. Для текущей работы: `governance/methodology/EXPERIMENT_REGISTRATION.md` и `experiments/README.md`.
7. Проверка: `python tools/validate_repo.py`.

## Boundary

A formal `EXP-...` is registered before result observation and has evidence class `REGISTERED_EXPERIMENT`; this does not by itself mean validated edge. Registry is an index, not an alternative manifest. Reference Strategy #1, broker, capital, live risk limits and production execution are not selected at this stage.
