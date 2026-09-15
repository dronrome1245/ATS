# ATS

> **AI / новый чат:** сначала откройте [`AI_HANDOFF.md`](AI_HANDOFF.md), затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — программа исследований, разработки, проверки и эксплуатации алгоритмических торговых стратегий. Цель — воспроизводимая Strategy Factory, а не один робот.

## Текущее состояние

- Phase: `M0_PROGRAM_REBASELINE / IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Current program governance: `governance/program/`.
- Current methodology: `governance/methodology/`.
- Legacy archive: `legacy/v1/`.

Последняя завершённая task:

`ATS2-M0-011 — Legacy physical migration and unresolved-question carryover`.

Следующая ready task:

`ATS2-M0-012 — Final link/validator sweep`.

Canonical next artifact anchor:

`tools/validate_repo.py`.

## Canonical ATS v2

Program:

- `governance/program/PROGRAM_CHARTER_V2.md`;
- `governance/program/OPERATING_MODEL_V2.md`;
- `governance/program/PROGRAM_WBS_V2.md`;
- `governance/program/REPOSITORY_STRUCTURE_V2.md`.

Methodology:

- `governance/methodology/STRATEGY_LIFECYCLE_V2.md`;
- `governance/methodology/RESEARCH_METHODOLOGY_V1.md`;
- `governance/methodology/templates/README.md`.

Legacy:

- `legacy/v1/README.md`;
- `legacy/v1/MIGRATION_INDEX.md`;
- `legacy/v1/CARRYOVER.md`.

## Быстрый старт

1. `AI_HANDOFF.md`.
2. `AGENTS.md`.
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
5. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. Проверка: `python tools/validate_repo.py`.

ATS v1 G01–G13 является historical/reference layer и не является current roadmap. Legacy content не становится current v2 policy без отдельного review.

## Ограничение ответственности

Репозиторий организует research, engineering, evidence, risk и operations. Он не гарантирует прибыльность и не заменяет юридическую, налоговую или регуляторную проверку.
