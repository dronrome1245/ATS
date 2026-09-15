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
2. `ATS2-M1-001` — Idea intake process — `READY`.
3. `ATS2-M1-002` — Hypothesis model — после M1-001.
4. `ATS2-M1-003` — Data Feasibility review — после M1-002.
5. `ATS2-M1-004` — Cheap Prototype protocol — после M1-002/M1-003.
6. `ATS2-M1-005` — Economic Pre-Screen — после M1-004.
7. `ATS2-M1-006` — Candidate promotion — после M1-005.

Program-level current next task остаётся только `ATS2-M1-001`, даже если отдельный supporting work теоретически имеет выполненные зависимости.

## 3. M0 — Program Rebaseline

| Task ID | WBS | Status | Deliverable / result |
|---|---|---|---|
| `ATS2-M0-001` | `WBS-0.1` | DONE | `governance/program/PROGRAM_CHARTER_V2.md` |
| `ATS2-M0-002` | `WBS-0.2` | DONE | `governance/program/OPERATING_MODEL_V2.md` |
| `ATS2-M0-003` | `WBS-0.3` | DONE | `governance/methodology/STRATEGY_LIFECYCLE_V2.md` |
| `ATS2-M0-004` | `WBS-0.4` | DONE | `governance/methodology/RESEARCH_METHODOLOGY_V1.md` |
| `ATS2-M0-005` | `WBS-0.5` | DONE | `governance/program/PROGRAM_WBS_V2.md` |
| `ATS2-M0-006` | `WBS-0.6` | DONE | `governance/program/REPOSITORY_STRUCTURE_V2.md` |
| `ATS2-M0-007` | `WBS-0.7` | DONE | `governance/backlog/PROGRAM_BACKLOG_V2.md` |
| `ATS2-M0-008` | `WBS-0.8` | DONE | Research entity templates |
| `ATS2-M0-009` | `WBS-0.6`, `WBS-0.12` | DONE | Canonical governance path migration |
| `ATS2-M0-010` | `WBS-0.12` | DONE | Legacy index/classification |
| `ATS2-M0-011` | `WBS-0.12` | DONE | Physical legacy migration + `CARRYOVER.md` |
| `ATS2-M0-012` | `WBS-0.10`, `WBS-0.12` | DONE | `M0_FINAL_SWEEP.md` + hardened validator |
| `ATS2-M0-013` | M0 Exit | DONE | `governance/program/M0_EXIT_REVIEW.md` — `PASS` |

`M0_PROGRAM_REBASELINE = COMPLETED`.

## 4. M1 — Research Factory

| Task ID | WBS | Priority | Status | Dependencies | Deliverable | Definition of Done / activation |
|---|---|---:|---|---|---|---|
| `ATS2-M1-001` | `WBS-1.1` | P1 | READY | M0-013 | `governance/methodology/IDEA_INTAKE_PROCESS.md` + tested Idea template | Idea можно зарегистрировать с stable ID, rationale, market/horizon, required data и screening decision без придумывания структуры |
| `ATS2-M1-002` | `WBS-1.2` | P1 | BLOCKED | M1-001 | Hypothesis model + tested template | Hypothesis содержит falsifiable statement, mechanism, expected effect и falsification path |
| `ATS2-M1-003` | `WBS-1.3` | P1 | BLOCKED | M1-002 | Data Feasibility review model | Проверяются availability, timestamp semantics, bias/leakage risks, costs и known gaps |
| `ATS2-M1-004` | `WBS-1.4` | P1 | BLOCKED | M1-002, M1-003 | Cheap Prototype protocol | Prototype отвечает на один ранний вопрос и не считается formal validation |
| `ATS2-M1-005` | `WBS-1.5` | P1 | BLOCKED | M1-004 | Economic Pre-Screen rubric | До Candidate оцениваются magnitude, likely costs, opportunities, capital use и complexity |
| `ATS2-M1-006` | `WBS-1.6` | P1 | BLOCKED | M1-005 | Candidate promotion process | `PROMOTE / PARK / REJECT` опирается на сохранённые preliminary evidence |
| `ATS2-M1-007` | `WBS-1.7` | P1 | BLOCKED | M1-002 | Experiment registration schema | Formal experiment связывает code, data, params, costs, predefined question и result |
| `ATS2-M1-008` | `WBS-1.8` | P1 | BLOCKED | M1-007 | Experiment registry | Положительные и отрицательные formal experiments находятся по stable ID |
| `ATS2-M1-009` | `WBS-1.9` | P1 | NOT_STARTED | M0-013 | Evidence taxonomy operationalization | Dependency выполнена, но activation отложена для WIP discipline; taxonomy должна связать evidence class с допустимыми решениями |
| `ATS2-M1-010` | `WBS-1.10` | P1 | BLOCKED | M1-001…009 | Research review protocol | Повторяемая процедура решает `PROMOTE / PARK / REJECT` |
| `ATS2-M1-011` | M1 Exit | P1 | BLOCKED | M1-001…010 | M1 exit decision | Idea → Prototype → Candidate decision выполняется воспроизводимо |

## 5. M2 and later

M2 остаётся `PARKED` до M1 Exit. `ATS2-M2-000 — Reference Consumer Profile` должен предшествовать `ATS2-M2-001 — Research stack ADR`, чтобы stack не выбирался в вакууме.

Reference Strategy #1 выбирается только в M3 после M1 и M2 Exit. Carryover из ATS v1 учитывается при будущей декомпозиции M2/M5/M7 через `legacy/v1/CARRYOVER.md`.

## 6. Следующий шаг

Текущая program-level ready task:

`ATS2-M1-001 — Idea intake process`.

Canonical next artifact:

`governance/methodology/IDEA_INTAKE_PROCESS.md`.

Задача должна operationalize создание и первичный screening Idea, используя существующий `governance/methodology/templates/IDEA_TEMPLATE.md`, но не регистрировать выдуманную торговую идею только ради проверки процесса.
