# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M1_RESEARCH_METHODOLOGY / IN_PROGRESS`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Последняя завершённая task:

`ATS2-M1-003 — Data Feasibility review`.

Artifacts:

- `governance/methodology/DATA_FEASIBILITY_REVIEW.md`;
- `governance/methodology/templates/DATA_FEASIBILITY_TEMPLATE.md`.

Следующая ready task:

`ATS2-M1-004 — Cheap Prototype protocol`.

Следующий artifact:

`governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md`.

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
6. Для текущей работы: `governance/methodology/HYPOTHESIS_MODEL.md`, `governance/methodology/DATA_FEASIBILITY_REVIEW.md` и `governance/methodology/RESEARCH_METHODOLOGY_V1.md`.
7. Проверка: `python tools/validate_repo.py`.

## Boundary

M1 operationalizes the Research Factory. Data Feasibility is not evidence of edge. Cheap Prototype must obey the recorded data constraints and is not formal validation. Reference Strategy #1, broker, capital, live risk limits and production execution are not selected at this stage.
