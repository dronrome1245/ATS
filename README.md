# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования и проверки алгоритмических торговых систем.

## Текущее состояние

- Phase: `M1_RESEARCH_METHODOLOGY / IN_PROGRESS`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Последняя завершённая task:

`ATS2-M1-010 — Research review protocol`.

Canonical package:

- `governance/methodology/RESEARCH_REVIEW_PROTOCOL.md`;
- `governance/methodology/RESEARCH_REVIEW_CHECKS.md`;
- `governance/methodology/RESEARCH_REVIEW_DECISIONS.md`;
- `governance/methodology/templates/RESEARCH_REVIEW_TEMPLATE.md`.

Следующая ready task:

`ATS2-M1-011 — M1 Exit Review`.

Следующий artifact:

`governance/program/M1_EXIT_REVIEW.md`.

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
6. Для текущей работы: `governance/methodology/RESEARCH_REVIEW_PROTOCOL.md`, `governance/methodology/EVIDENCE_TAXONOMY.md`, `experiments/README.md`.
7. Проверка repository: `python tools/validate_repo.py`.

## Boundary

M1 Research Review is event-driven and stage-aware; it does not upgrade evidence classes or invent missing inputs. M1 Exit Review is the last step before any transition to M2. Reference Strategy #1 is not selected yet.
