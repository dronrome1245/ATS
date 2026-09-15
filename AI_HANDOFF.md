# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Program model: ATS v2 / Strategy Factory.
- Current phase: `M1_RESEARCH_METHODOLOGY` / Research Factory.
- Status: `IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- G01–G13: `legacy/v1/`, history/reference only.
- Real trading, demo, allocation and scaling remain disallowed current actions.

## 2. Последний завершённый шаг

`ATS2-M1-004 — Cheap Prototype protocol` — `DONE`.

Artifacts:

- `governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md`;
- `governance/methodology/templates/CHEAP_PROTOTYPE_TEMPLATE.md`.

Cheap Prototype now means one pre-written quantitative question, minimum implementation, explicit data/timing/cost assumptions, result/iteration accounting and one outcome among:

`ADVANCE_TO_ECONOMIC_SCREEN / ITERATE / PARK / REJECT`.

Prototype evidence class is `EXPLORATORY_PROTOTYPE`. It is not a registered Experiment or validation evidence. Formal evidence requires a future pre-registered `EXP-...` rerun.

## 3. Текущая ready task

`ATS2-M1-005 — Economic Pre-Screen`

Canonical next artifact:

`governance/methodology/ECONOMIC_PRE_SCREEN.md`

Goal: define whether preliminary effect/economics justify a full research budget and possible later Candidate promotion.

## 4. Что должно быть определено в M1-005

- admissible prototype inputs/outcomes;
- preliminary effect magnitude;
- gross/net economics and cost sensitivity;
- opportunity frequency/diversity;
- capital use/efficiency;
- risk/path/concentration characteristics;
- capacity/scalability;
- operational/data/execution complexity;
- evidence weakness and search degrees of freedom;
- economic margin of safety;
- clear `PROMOTE / PARK / REJECT / RETURN_TO_RESEARCH` style decision model;
- structural rubric test without invented returns/capital.

## 5. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/methodology/IDEA_INTAKE_PROCESS.md`.
6. `governance/methodology/HYPOTHESIS_MODEL.md`.
7. `governance/methodology/DATA_FEASIBILITY_REVIEW.md`.
8. `governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md`.
9. `governance/methodology/RESEARCH_METHODOLOGY_V1.md`.
10. relevant templates.

## 6. Boundaries

Cheap Prototype is preliminary/exploratory. Do not infer profitability or validation from an attractive prototype. Do not choose Reference Strategy #1, broker, jurisdiction, live platform, capital allocation or risk limits in M1-005.

## 7. Completion protocol

Material program task is complete only after deliverable, backlog, canonical state, human status, next-step, AI handoff and validator/entrypoints where relevant are synchronized.

## 8. Проверка восстановления контекста

- Current phase? — `M1_RESEARCH_METHODOLOGY`.
- Last completed? — `ATS2-M1-004`, `governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md`.
- Next task? — `ATS2-M1-005`.
- Next artifact? — `governance/methodology/ECONOMIC_PRE_SCREEN.md`.
- Active prototypes created by process test? — `0`.
- Can Cheap Prototype be cited as formal validation evidence? — no.
