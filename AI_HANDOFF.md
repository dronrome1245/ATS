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

`ATS2-M1-002 — Hypothesis model` — `DONE`.

Artifact:

`governance/methodology/HYPOTHESIS_MODEL.md`

Hypothesis formation now defines stable `HYP-xxxx`, Parent Idea linkage, falsifiable Statement, Mechanism, Conditions, Horizons, expected Direction, decision-time information premise, Falsification, Required data, Known biases, cheap research question and change control. `HYPOTHESIS_TEMPLATE.md` is aligned and structurally tested without registering a fictitious Hypothesis.

Decision `DATA_FEASIBILITY` means readiness for data review only; it is not evidence of edge and does not authorize prototype work.

## 3. Текущая ready task

`ATS2-M1-003 — Data Feasibility review`

Canonical next artifact:

`governance/methodology/DATA_FEASIBILITY_REVIEW.md`

Goal: define how ATS decides whether available data can honestly test a concrete Hypothesis before Cheap Prototype work.

## 4. Что должно быть определено в M1-003

- Hypothesis linkage;
- required data/source types;
- coverage and granularity;
- timezone and timestamp semantics;
- decision-time information availability;
- revisions/restatements/corporate actions/event corrections;
- missing/bad data handling;
- universe/survivorship/selection risks;
- leakage/overlap risks;
- transformation trace and dataset identity;
- cost/execution inputs relevant to the early test;
- explicit known gaps;
- feasibility decision/status model;
- structural acceptance test without invented vendor or dataset.

## 5. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/methodology/IDEA_INTAKE_PROCESS.md`.
6. `governance/methodology/HYPOTHESIS_MODEL.md`.
7. `governance/methodology/RESEARCH_METHODOLOGY_V1.md`.
8. relevant templates.

## 6. Boundaries

No fictitious research consumer is created for process testing. Do not choose a universal vendor, Reference Strategy #1, broker, jurisdiction, live platform, capital allocation or risk limits. Quantitative prototype work starts only after a Data Feasibility decision.

## 7. Completion protocol

Material program task is complete only after deliverable, backlog, canonical state, human status, next-step, AI handoff and validator/entrypoints where relevant are synchronized.

## 8. Проверка восстановления контекста

- Current phase? — `M1_RESEARCH_METHODOLOGY`.
- Last completed? — `ATS2-M1-002`, `governance/methodology/HYPOTHESIS_MODEL.md`.
- Next task? — `ATS2-M1-003`.
- Next artifact? — `governance/methodology/DATA_FEASIBILITY_REVIEW.md`.
- Can a `DATA_FEASIBILITY` Hypothesis be treated as edge evidence? — no.
- Can Cheap Prototype start before data review? — no.
