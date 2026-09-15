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

`ATS2-M1-001 — Idea intake process` — `DONE`.

Artifact:

`governance/methodology/IDEA_INTAKE_PROCESS.md`

Idea intake now defines stable `IDEA-xxxx` IDs, provenance, duplicate/overlap review, minimum intake fields, `SCREEN / PARK / REJECT`, status mapping and retention of negative decisions. `IDEA_TEMPLATE.md` is aligned and was structurally tested without registering a fictitious Idea.

## 3. Текущая ready task

`ATS2-M1-002 — Hypothesis model`

Canonical next artifact:

`governance/methodology/HYPOTHESIS_MODEL.md`

Goal: define how a screened Idea becomes a falsifiable Hypothesis and align/test `governance/methodology/templates/HYPOTHESIS_TEMPLATE.md` without inventing a Hypothesis for process testing.

## 4. Что должно быть определено в M1-002

- stable `HYP-xxxx` ID;
- parent Idea linkage;
- Statement / Mechanism / Market / Condition / Horizon / Direction;
- explicit Falsification;
- Required data and Known biases;
- falsifiability admission rule;
- allowed unknowns before Data Feasibility;
- Hypothesis status/decision model;
- material-reformulation change control;
- structural template acceptance test.

## 5. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/methodology/IDEA_INTAKE_PROCESS.md`.
6. `governance/methodology/RESEARCH_METHODOLOGY_V1.md`.
7. `governance/methodology/templates/HYPOTHESIS_TEMPLATE.md`.

## 6. Boundaries

Idea `SCREEN` is not evidence of edge. M1-002 does not choose Reference Strategy #1, broker, jurisdiction, live platform, capital allocation or risk limits. Quantitative testing waits for the applicable Data Feasibility/research protocol.

## 7. Completion protocol

Material program task is complete only after deliverable, backlog, canonical state, human status, next-step, AI handoff and validator/entrypoints where relevant are synchronized.

## 8. Проверка восстановления контекста

- Current phase? — `M1_RESEARCH_METHODOLOGY`.
- Last completed? — `ATS2-M1-001`, `governance/methodology/IDEA_INTAKE_PROCESS.md`.
- Next task? — `ATS2-M1-002`.
- Next artifact? — `governance/methodology/HYPOTHESIS_MODEL.md`.
- Ideas registered by process test? — `0`.
- Can screening be treated as edge evidence? — no.
