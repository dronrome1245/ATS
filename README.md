# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M1_RESEARCH_METHODOLOGY / IN_PROGRESS`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Последняя завершённая task:

`ATS2-M1-006 — Candidate promotion process`.

Artifact:

`governance/methodology/CANDIDATE_PROMOTION_PROCESS.md`.

Candidate создаётся только после explicit `PROMOTE`; `PARK/REJECT` сохраняют review без `CAND-...`. `STRAT-...` появляется только на formal S01.

Следующая ready task:

`ATS2-M1-007 — Experiment registration schema`.

Следующий artifact:

`governance/methodology/EXPERIMENT_REGISTRATION.md`.

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
6. Для текущей работы: `governance/methodology/RESEARCH_METHODOLOGY_V1.md` и `governance/methodology/templates/experiment/manifest.yaml`.
7. Проверка: `python tools/validate_repo.py`.

## Boundary

M1 operationalizes the Research Factory. Candidate promotion is not validation/live admission. Formal Experiment must be registered before result observation; exploratory prototype history cannot become preregistered evidence retroactively. Reference Strategy #1, broker, capital, live risk limits and production execution are not selected at this stage.
