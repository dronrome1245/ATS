# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования и проверки алгоритмических торговых систем.

## Текущее состояние

- Phase: `M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- M1 Research Methodology: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Последняя завершённая task:

`ATS2-M1-011 — M1 Exit Review` (`PASS`).

Canonical exit artifact:

`governance/program/M1_EXIT_REVIEW.md`.

Следующая ready task:

`ATS2-M2-000 — Reference Consumer Profile`.

Следующий artifact:

`governance/program/REFERENCE_CONSUMER_PROFILE.md`.

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
6. Для текущей работы: `governance/program/M1_EXIT_REVIEW.md`, `governance/program/PROGRAM_WBS_V2.md`, `governance/program/PROGRAM_CHARTER_V2.md`.
7. Проверка repository: `python tools/validate_repo.py`.

## Boundary

M2 builds the minimum reproducible research platform. `M2-000` defines an abstract consumer profile; it does not select a concrete Reference Strategy #1, market, instrument, broker, capital policy or live environment. Concrete Strategy #1 selection remains M3 work.
