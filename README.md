# ATS

> **AI / новый чат:** сначала откройте [`AI_HANDOFF.md`](AI_HANDOFF.md), затем `AGENTS.md`. Там зафиксированы текущее состояние, canonical backlog и следующий обязательный task.

**ATS — Algorithmic Trading Systems** — программа исследований, разработки, проверки и эксплуатации алгоритмических торговых стратегий.

Цель ATS — построить воспроизводимую **Strategy Factory**: процесс и общую платформу, позволяющие генерировать гипотезы, быстро отбраковывать слабые идеи, подтверждать экономически значимые стратегии, проверять реальное исполнение и со временем формировать диверсифицированный портфель источников edge.

## Текущее состояние

ATS проходит `M0_PROGRAM_REBASELINE`.

Canonical machine-readable state:

`03_СОСТОЯНИЕ_ПРОЕКТА.yaml`

Canonical execution queue:

`governance/backlog/PROGRAM_BACKLOG_V2.md`

Уже зафиксированы:

- `AI_HANDOFF.md`;
- `00_Управление_проектом/v2/PROGRAM_CHARTER_V2.md`;
- `00_Управление_проектом/v2/OPERATING_MODEL_V2.md`;
- `00_Управление_проектом/v2/STRATEGY_LIFECYCLE_V2.md`;
- `00_Управление_проектом/v2/RESEARCH_METHODOLOGY_V1.md`;
- `00_Управление_проектом/v2/PROGRAM_WBS_V2.md`;
- `00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md`;
- `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Следующая task:

`ATS2-M0-008 — Research entity templates`

Следующий artifact/index:

`governance/methodology/templates/README.md`

## Пять контуров ATS

1. **Research Factory** — Idea → Rationale → Data Feasibility → Cheap Prototype → Economic Screen → Candidate.
2. **Shared Trading Platform** — данные, backtest/replay, Strategy API, analytics, risk, execution и operations.
3. **Strategy Lifecycle** — глубокая validation конкретной Strategy Version.
4. **Portfolio & Capital** — portfolio-level allocation, diversification и risk.
5. **Operations & Governance** — versions, evidence, deployment, monitoring, incidents и change control.

## Program Backlog v2

Backlog деталирует M0, M1 и M2 в executable tasks с stable ID, priority/status, dependencies, role, deliverable и Definition of Done.

M3–M8 пока остаются future epics и будут детализироваться только при появлении фактических входов.

## Главный принцип

Каждая стратегия должна доказать две вещи:

1. существует достаточно убедительный evidence of edge;
2. edge имеет достаточную экономическую ценность относительно капитала, риска, издержек и сложности.

Risk management является ограничением и механизмом безопасного масштабирования подтверждённого edge, а не самостоятельной целью.

## Быстрый старт

1. Новый AI-чат или незнакомый разработчик: `AI_HANDOFF.md`.
2. Правила для агентов: `AGENTS.md`.
3. Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
4. Непосредственное действие: `02_СЛЕДУЮЩИЙ_ШАГ.md`.
5. Execution queue: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. Program WBS: `00_Управление_проектом/v2/PROGRAM_WBS_V2.md`.
7. Target repository layout: `00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md`.
8. Перед research читать `RESEARCH_METHODOLOGY_V1.md`.
9. Для конкретной Strategy Version использовать `STRATEGY_LIFECYCLE_V2.md`.
10. Запускать `python tools/validate_repo.py` для структурной проверки репозитория.

Старая модель G01–G13 сохранена как ATS v1 history/reference и не является current program roadmap.

## Ограничение ответственности

Репозиторий организует исследования, разработку, контроль качества, риска и evidence. Он не гарантирует прибыльность и не заменяет юридическую, налоговую или регуляторную проверку применительно к конкретной эксплуатации.
