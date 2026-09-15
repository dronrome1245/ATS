# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования и проверки алгоритмических торговых систем.

## Текущее состояние

- Phase: `M1_RESEARCH_METHODOLOGY / IN_PROGRESS`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Последняя завершённая task:

`ATS2-M1-009 — Evidence taxonomy operationalization`.

Artifact:

`governance/methodology/EVIDENCE_TAXONOMY.md`.

Taxonomy разделяет `source_class` и `qualified_evidence_class`; result attractiveness не повышает evidence class автоматически. Registry и Evidence Index templates используют ту же модель.

Следующая ready task:

`ATS2-M1-010 — Research review protocol`.

Следующий artifact:

`governance/methodology/RESEARCH_REVIEW_PROTOCOL.md`.

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
6. Для текущей работы: `governance/methodology/EVIDENCE_TAXONOMY.md`, `governance/methodology/RESEARCH_METHODOLOGY_V1.md`, `experiments/README.md`.
7. Поиск experiments: `python tools/search_experiments.py --help`.
8. Проверка repository: `python tools/validate_repo.py`.

## Boundary

Evidence classification ограничивает допустимую силу claim; более слабый class не заменяет class, требуемый конкретным review protocol. Reference Strategy #1 на текущем шаге не выбирается.
