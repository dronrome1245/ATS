# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — программа исследований, разработки, проверки и эксплуатации алгоритмических торговых стратегий. Цель — воспроизводимая Strategy Factory, а не один robot project.

## Текущее состояние

- Phase: `M1_RESEARCH_METHODOLOGY / IN_PROGRESS`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Current governance: `governance/program/`.
- Current methodology: `governance/methodology/`.

Последняя завершённая task:

`ATS2-M0-013 — M0 Exit Review`.

Artifact:

`governance/program/M0_EXIT_REVIEW.md`.

Следующая program-level ready task:

`ATS2-M1-001 — Idea intake process`.

Следующий artifact:

`governance/methodology/IDEA_INTAKE_PROCESS.md`.

## Canonical ATS v2

Program:

- `governance/program/PROGRAM_CHARTER_V2.md`;
- `governance/program/OPERATING_MODEL_V2.md`;
- `governance/program/PROGRAM_WBS_V2.md`;
- `governance/program/REPOSITORY_STRUCTURE_V2.md`.

Methodology:

- `governance/methodology/STRATEGY_LIFECYCLE_V2.md`;
- `governance/methodology/RESEARCH_METHODOLOGY_V1.md`;
- `governance/methodology/templates/`.

## Быстрый старт

1. `AI_HANDOFF.md`.
2. `AGENTS.md`.
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
5. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. Для текущей работы — `governance/methodology/RESEARCH_METHODOLOGY_V1.md` и `governance/methodology/templates/IDEA_TEMPLATE.md`.
7. Проверка репозитория — `python tools/validate_repo.py`.

ATS v1 G01–G13 хранится в `legacy/v1/` как historical/reference layer и не является current roadmap.

## Текущая boundary

M1 строит Research Factory. На текущем шаге не выбираются Reference Strategy #1, broker, real capital, live risk limits или production execution platform.

## Ограничение ответственности

Репозиторий организует research, engineering, evidence, risk и operations. Он не гарантирует прибыльность и не заменяет юридическую, налоговую или регуляторную проверку.
