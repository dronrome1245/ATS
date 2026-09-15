# ATS

> **AI / новый чат:** сначала прочитайте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — программа исследований, разработки, проверки и эксплуатации алгоритмических торговых стратегий. Цель — воспроизводимая Strategy Factory, а не один торговый робот.

## Текущее состояние

- Phase: `M0_PROGRAM_REBASELINE / IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Current governance: `governance/program/`.
- Current methodology: `governance/methodology/`.
- Legacy ATS v1: `legacy/v1/`.

Последняя завершённая task:

`ATS2-M0-012 — Final link/validator sweep`.

Sweep evidence:

`governance/program/M0_FINAL_SWEEP.md`

Следующая ready task:

`ATS2-M0-013 — M0 Exit Review`.

Следующий artifact:

`governance/program/M0_EXIT_REVIEW.md`.

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

## Быстрый старт

1. `AI_HANDOFF.md`.
2. `AGENTS.md`.
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
5. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. Проверка: `python tools/validate_repo.py`.

ATS v1 G01–G13 является historical/reference layer и не является current roadmap.

M0 Exit Review не является разрешением на live trading и не выбирает Strategy #1, broker, capital allocation или risk limits.

## Ограничение ответственности

Репозиторий организует research, engineering, evidence, risk и operations. Он не гарантирует прибыльность и не заменяет юридическую, налоговую или регуляторную проверку.
