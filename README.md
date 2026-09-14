# ATS

> **AI / новый чат:** сначала откройте [`AI_HANDOFF.md`](AI_HANDOFF.md), затем `AGENTS.md`. Там зафиксированы текущее состояние, canonical backlog и следующий обязательный task.

**ATS — Algorithmic Trading Systems** — программа исследований, разработки, проверки и эксплуатации алгоритмических торговых стратегий.

Цель ATS — построить воспроизводимую **Strategy Factory**: процесс и общую платформу, позволяющие генерировать гипотезы, быстро отбраковывать слабые идеи, подтверждать экономически значимые стратегии, проверять реальное исполнение и со временем формировать диверсифицированный портфель источников edge.

## Текущее состояние

ATS проходит `M0_PROGRAM_REBASELINE`.

Canonical state:

`03_СОСТОЯНИЕ_ПРОЕКТА.yaml`

Canonical execution queue:

`governance/backlog/PROGRAM_BACKLOG_V2.md`

Последний завершённый work package:

`WBS-0.8 — Research entity templates`

Canonical template index:

`governance/methodology/templates/README.md`

Следующая ready task:

`ATS2-M0-009 — Governance v2 path migration`

Canonical next artifact anchor:

`governance/program/PROGRAM_CHARTER_V2.md`

## Пять контуров ATS

1. **Research Factory** — Idea → Rationale → Data Feasibility → Cheap Prototype → Economic Screen → Candidate.
2. **Shared Trading Platform** — данные, backtest/replay, Strategy API, analytics, risk, execution и operations.
3. **Strategy Lifecycle** — глубокая validation конкретной Strategy Version.
4. **Portfolio & Capital** — portfolio-level allocation, diversification и risk.
5. **Operations & Governance** — versions, evidence, deployment, monitoring, incidents и change control.

## Research entity templates

Template package позволяет без повторного проектирования структуры создавать:

- Idea;
- Hypothesis;
- Candidate;
- formal Experiment;
- Strategy Version.

Шаблоны не содержат выдуманных торговых или финансовых фактов.

## Быстрый старт

1. Новый AI-чат: `AI_HANDOFF.md`.
2. Agent rules: `AGENTS.md`.
3. Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
4. Next action: `02_СЛЕДУЮЩИЙ_ШАГ.md`.
5. Backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. WBS: `00_Управление_проектом/v2/PROGRAM_WBS_V2.md`.
7. Repository target layout: `00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md`.
8. Templates: `governance/methodology/templates/README.md`.
9. Запускать `python tools/validate_repo.py` для структурной проверки.

Текущая governance migration является структурной: содержание принятых baseline documents не меняется, меняются canonical paths и ссылки.

Старая модель G01–G13 сохранена как ATS v1 history/reference и не является current program roadmap.

## Ограничение ответственности

Репозиторий организует исследования, разработку, контроль качества, риска и evidence. Он не гарантирует прибыльность и не заменяет юридическую, налоговую или регуляторную проверку применительно к конкретной эксплуатации.
