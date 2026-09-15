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

`ATS2-M1-003 — Data Feasibility review` — `DONE`.

Artifacts:

- `governance/methodology/DATA_FEASIBILITY_REVIEW.md`;
- `governance/methodology/templates/DATA_FEASIBILITY_TEMPLATE.md`.

Data Feasibility now evaluates source/access, coverage, granularity, timestamp semantics, decision-time information availability, revisions/corrections, missing/bad data, universe/survivorship/selection bias, leakage, traceability, relevant cost/execution inputs, licensing constraints and known gaps before prototype work.

Decision model: `FEASIBLE / CONDITIONAL / PARK / REJECT`.

`FEASIBLE` permits Cheap Prototype. `CONDITIONAL` permits only a constrained prototype; a condition that materially changes the Hypothesis requires a new Hypothesis.

## 3. Текущая ready task

`ATS2-M1-004 — Cheap Prototype protocol`

Canonical next artifact:

`governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md`

Goal: define the minimum-cost quantitative check of one early research question without treating prototype output as registered/validation evidence.

## 4. Что должно быть определено в M1-004

- admissible Data Feasibility outcomes;
- one limited prototype question;
- minimum inputs and assumptions;
- data/source snapshot trace;
- applicable cost assumptions;
- exploratory implementation boundaries;
- minimum run/result record;
- early decision model;
- retention of negative results;
- boundary between prototype and formal Experiment;
- structural protocol test without fictitious research content.

## 5. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/methodology/IDEA_INTAKE_PROCESS.md`.
6. `governance/methodology/HYPOTHESIS_MODEL.md`.
7. `governance/methodology/DATA_FEASIBILITY_REVIEW.md`.
8. `governance/methodology/RESEARCH_METHODOLOGY_V1.md`.
9. relevant templates.

## 6. Boundaries

Data Feasibility is not evidence of edge. Cheap Prototype is not validation. Do not choose Reference Strategy #1, broker, jurisdiction, live platform, capital allocation or risk limits in M1-004.

## 7. Completion protocol

Material program task is complete only after deliverable, backlog, canonical state, human status, next-step, AI handoff and validator/entrypoints where relevant are synchronized.

## 8. Проверка восстановления контекста

- Current phase? — `M1_RESEARCH_METHODOLOGY`.
- Last completed? — `ATS2-M1-003`, `governance/methodology/DATA_FEASIBILITY_REVIEW.md`.
- Next task? — `ATS2-M1-004`.
- Next artifact? — `governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md`.
- Can Data Feasibility be treated as edge evidence? — no.
- Can a prototype ignore recorded feasibility constraints? — no.
