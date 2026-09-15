# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M1_RESEARCH_METHODOLOGY / IN_PROGRESS`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Последняя завершённая task:

`ATS2-M1-005 — Economic Pre-Screen`.

Artifacts:

- `governance/methodology/ECONOMIC_PRE_SCREEN.md`;
- `governance/methodology/templates/ECONOMIC_PRE_SCREEN_TEMPLATE.md`.

Следующая ready task:

`ATS2-M1-006 — Candidate promotion process`.

Следующий artifact:

`governance/methodology/CANDIDATE_PROMOTION_PROCESS.md`.

## Canonical ATS v2

- Program governance: `governance/program/`;
- Methodology: `governance/methodology/`;
- Research templates: `governance/methodology/templates/`;
- Execution queue: `governance/backlog/PROGRAM_BACKLOG_V2.md`;
- Legacy ATS v1: `legacy/v1/`.

## Быстрый старт

1. `AI_HANDOFF.md`.
2. `AGENTS.md`.
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
5. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. Для текущей работы: `governance/methodology/ECONOMIC_PRE_SCREEN.md` и `governance/methodology/templates/CANDIDATE_TEMPLATE.md`.
7. Проверка: `python tools/validate_repo.py`.

## Boundary

M1 operationalizes the Research Factory. Positive Economic Pre-Screen only permits Candidate review; it does not create a Candidate, validate edge or allocate capital. Reference Strategy #1, broker, capital, live risk limits and production execution are not selected at this stage.
