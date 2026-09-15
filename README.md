# ATS

> **AI / новый чат:** сначала откройте [`AI_HANDOFF.md`](AI_HANDOFF.md), затем `AGENTS.md`. Там зафиксированы текущее состояние, canonical backlog и следующая task.

**ATS — Algorithmic Trading Systems** — программа исследований, разработки, проверки и эксплуатации алгоритмических торговых стратегий.

Цель ATS — построить воспроизводимую **Strategy Factory**: процесс и общую платформу, позволяющие генерировать гипотезы, быстро отбраковывать слабые идеи, подтверждать экономически значимые стратегии, проверять реальное исполнение и со временем формировать диверсифицированный портфель источников edge.

## Текущее состояние

ATS проходит `M0_PROGRAM_REBASELINE`.

- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Current program governance: `governance/program/`.
- Current methodology: `governance/methodology/`.

Последняя завершённая task:

`ATS2-M0-009 — Governance v2 path migration`.

Следующая ready task:

`ATS2-M0-010 — Legacy v1 index/classification`.

Следующий artifact:

`legacy/v1/README.md`.

## Canonical ATS v2 documents

Program:

- `governance/program/PROGRAM_CHARTER_V2.md`;
- `governance/program/OPERATING_MODEL_V2.md`;
- `governance/program/PROGRAM_WBS_V2.md`;
- `governance/program/REPOSITORY_STRUCTURE_V2.md`.

Methodology:

- `governance/methodology/STRATEGY_LIFECYCLE_V2.md`;
- `governance/methodology/RESEARCH_METHODOLOGY_V1.md`;
- `governance/methodology/templates/README.md`.

## Пять контуров ATS

1. **Research Factory** — Idea → Rationale → Data Feasibility → Cheap Prototype → Economic Screen → Candidate.
2. **Shared Trading Platform** — данные, backtest/replay, Strategy API, analytics, risk, execution и operations.
3. **Strategy Lifecycle** — validation конкретной Strategy Version.
4. **Portfolio & Capital** — portfolio-level allocation, diversification и risk.
5. **Operations & Governance** — versions, evidence, deployment, monitoring, incidents и change control.

## Быстрый старт

1. `AI_HANDOFF.md`.
2. `AGENTS.md`.
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
5. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. `governance/program/PROGRAM_WBS_V2.md`.
7. `governance/program/REPOSITORY_STRUCTURE_V2.md`.
8. `governance/methodology/RESEARCH_METHODOLOGY_V1.md`.
9. Для конкретной Strategy Version — `governance/methodology/STRATEGY_LIFECYCLE_V2.md`.
10. Проверка репозитория — `python tools/validate_repo.py`.

Старая модель G01–G13 сохранена как ATS v1 history/reference и не является current program roadmap.

## Ограничение ответственности

Репозиторий организует исследования, разработку, контроль качества, риска и evidence. Он не гарантирует прибыльность и не заменяет юридическую, налоговую или регуляторную проверку применительно к конкретной эксплуатации.
