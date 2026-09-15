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
4. `ATS2-M1-003` — Data Feasibility review — `READY`.
5. `ATS2-M1-004` — Cheap Prototype protocol — после M1-003.
6. `ATS2-M1-005` — Economic Pre-Screen — после M1-004.
7. `ATS2-M1-006` — Candidate promotion — после M1-005.

Program-level current next task — `ATS2-M1-003`.

## 3. M0 — Program Rebaseline

`M0_PROGRAM_REBASELINE = COMPLETED / PASS`.

Canonical exit evidence: `governance/program/M0_EXIT_REVIEW.md`.

## 4. M1 — Research Factory

| Task ID | WBS | Priority | Status | Dependencies | Deliverable | Definition of Done / activation |
|---|---|---:|---|---|---|---|
| `ATS2-M1-001` | `WBS-1.1` | P1 | DONE | M0-013 | `governance/methodology/IDEA_INTAKE_PROCESS.md` + aligned Idea template | Stable `IDEA-xxxx` ID, provenance, duplicate check, minimum intake fields, `SCREEN/PARK/REJECT`, preserved negative decisions and structural template acceptance test are defined without registering a fictitious Idea |
| `ATS2-M1-002` | `WBS-1.2` | P1 | DONE | M1-001 | `governance/methodology/HYPOTHESIS_MODEL.md` + aligned Hypothesis template | Screened Idea can become a falsifiable `HYP-xxxx` with explicit mechanism, conditions, horizons, information-time premise, falsification rule, required data, change control and `DATA_FEASIBILITY/PARK/REJECT` decision without creating fictitious research content |
| `ATS2-M1-003` | `WBS-1.3` | P1 | READY | M1-002 | `governance/methodology/DATA_FEASIBILITY_REVIEW.md` + review template/model | Проверяются data availability, coverage, timestamp semantics, information availability, revisions, missing/bad data, survivorship/universe risks, leakage, cost inputs and known gaps before prototype work |
| `ATS2-M1-004` | `WBS-1.4` | P1 | BLOCKED | M1-002, M1-003 | Cheap Prototype protocol | Prototype отвечает на один ранний вопрос и не считается formal validation |
| `ATS2-M1-005` | `WBS-1.5` | P1 | BLOCKED | M1-004 | Economic Pre-Screen rubric | До Candidate оцениваются magnitude, likely costs, opportunities, capital use и complexity |
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

`ATS2-M1-003 — Data Feasibility review`.

Canonical next artifact:

`governance/methodology/DATA_FEASIBILITY_REVIEW.md`.

Задача должна определить, как для конкретной Hypothesis проверять возможность честного исследования данных до prototype work: source/coverage, timestamp semantics, information-time availability, revisions, universe/survivorship, missing/bad data, leakage, transformation trace, relevant cost inputs and explicit feasibility decision. Не выбирать конкретный vendor или dataset без реального consumer.
