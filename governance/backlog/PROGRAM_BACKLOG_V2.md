# ATS Program Backlog v2

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 2.0  
**Статус:** BASELINE  
**Дата:** 15 сентября 2026 года  
**WBS:** `governance/program/PROGRAM_WBS_V2.md`  
**Repository Structure:** `governance/program/REPOSITORY_STRUCTURE_V2.md`

## 1. Назначение

Backlog превращает Program WBS в исполнимую очередь работ. Material program task не считается завершённой до синхронизации state/status/next-step/handoff.

## 2. Текущая execution queue

1. `ATS2-M0-013` — M0 Exit Review — `DONE`.
2. `ATS2-M1-001` — Idea intake process — `DONE`.
3. `ATS2-M1-002` — Hypothesis model — `DONE`.
4. `ATS2-M1-003` — Data Feasibility review — `DONE`.
5. `ATS2-M1-004` — Cheap Prototype protocol — `DONE`.
6. `ATS2-M1-005` — Economic Pre-Screen — `READY`.
7. `ATS2-M1-006` — Candidate promotion — после M1-005.

Program-level current next task — `ATS2-M1-005`.

## 3. M0 — Program Rebaseline

`M0_PROGRAM_REBASELINE = COMPLETED / PASS`.

Canonical exit evidence: `governance/program/M0_EXIT_REVIEW.md`.

## 4. M1 — Research Factory

| Task ID | WBS | Priority | Status | Dependencies | Deliverable | Definition of Done / activation |
|---|---|---:|---|---|---|---|
| `ATS2-M1-001` | `WBS-1.1` | P1 | DONE | M0-013 | `governance/methodology/IDEA_INTAKE_PROCESS.md` + aligned Idea template | Stable `IDEA-xxxx` ID, provenance, duplicate check, minimum intake fields, `SCREEN/PARK/REJECT`, preserved negative decisions and structural template acceptance test are defined without registering a fictitious Idea |
| `ATS2-M1-002` | `WBS-1.2` | P1 | DONE | M1-001 | `governance/methodology/HYPOTHESIS_MODEL.md` + aligned Hypothesis template | Screened Idea can become a falsifiable `HYP-xxxx` with mechanism, conditions, horizons, information-time premise, falsification, required data and change control |
| `ATS2-M1-003` | `WBS-1.3` | P1 | DONE | M1-002 | `governance/methodology/DATA_FEASIBILITY_REVIEW.md` + `DATA_FEASIBILITY_TEMPLATE.md` | Review checks source/access, coverage, granularity, timestamp/information-time semantics, revisions, missing/bad data, survivorship/selection, leakage, traceability, relevant costs and known gaps; decision is `FEASIBLE/CONDITIONAL/PARK/REJECT` without invented vendor/dataset |
| `ATS2-M1-004` | `WBS-1.4` | P1 | DONE | M1-002, M1-003 | `governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md` + `CHEAP_PROTOTYPE_TEMPLATE.md` | One prototype answers one pre-written quantitative question with minimum implementation, explicit data/timing/cost assumptions and search accounting; outcome is `ADVANCE_TO_ECONOMIC_SCREEN/ITERATE/PARK/REJECT`; prototype remains `EXPLORATORY_PROTOTYPE` and cannot be retroactively represented as formal Experiment evidence |
| `ATS2-M1-005` | `WBS-1.5` | P1 | READY | M1-004 | `governance/methodology/ECONOMIC_PRE_SCREEN.md` + rubric/template | До Candidate оцениваются magnitude, likely costs, opportunities, capital use, risk characteristics, capacity and operational complexity; решение однозначно определяет, стоит ли тратить полноценный research budget |
| `ATS2-M1-006` | `WBS-1.6` | P1 | BLOCKED | M1-005 | Candidate promotion process | `PROMOTE / PARK / REJECT` опирается на сохранённые preliminary evidence |
| `ATS2-M1-007` | `WBS-1.7` | P1 | NOT_STARTED | M1-002 | Experiment registration schema | Dependency выполнена, но activation отложена по WIP discipline; formal experiment должен связать code, data, params, costs, predefined question и result |
| `ATS2-M1-008` | `WBS-1.8` | P1 | BLOCKED | M1-007 | Experiment registry | Положительные и отрицательные formal experiments находятся по stable ID |
| `ATS2-M1-009` | `WBS-1.9` | P1 | NOT_STARTED | M0-013 | Evidence taxonomy operationalization | Dependency выполнена, но activation отложена по WIP discipline |
| `ATS2-M1-010` | `WBS-1.10` | P1 | BLOCKED | M1-001…009 | Research review protocol | Повторяемая процедура решает `PROMOTE / PARK / REJECT` |
| `ATS2-M1-011` | M1 Exit | P1 | BLOCKED | M1-001…010 | M1 exit decision | Idea → Prototype → Candidate decision выполняется воспроизводимо |

## 5. M2 and later

M2 остаётся `PARKED` до M1 Exit. `ATS2-M2-000 — Reference Consumer Profile` должен предшествовать `ATS2-M2-001 — Research stack ADR`.

Reference Strategy #1 выбирается только в M3 после M1 и M2 Exit. Carryover из ATS v1 учитывается через `legacy/v1/CARRYOVER.md`.

## 6. Следующий шаг

Текущая program-level ready task:

`ATS2-M1-005 — Economic Pre-Screen`.

Canonical next artifact:

`governance/methodology/ECONOMIC_PRE_SCREEN.md`.

Задача должна определить, как после Cheap Prototype оценить экономическую ценность research line до Candidate admission: magnitude, preliminary net economics, opportunity frequency, capital efficiency, risk/path characteristics, capacity/scalability, evidence weakness and operational complexity. Prototype result остаётся preliminary/exploratory и не подменяет formal validation.