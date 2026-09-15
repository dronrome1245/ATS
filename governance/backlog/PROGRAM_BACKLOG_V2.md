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

1. `ATS2-M0-008` — Research entity templates — `DONE`.
2. `ATS2-M0-009` — Governance v2 path migration — `DONE`.
3. `ATS2-M0-010` — Legacy v1 index/classification — `DONE`.
4. `ATS2-M0-011` — Legacy physical migration and unresolved-question carryover — `DONE`.
5. `ATS2-M0-012` — Final link/validator sweep — `DONE`.
6. `ATS2-M0-013` — M0 Exit Review — `READY`.

До `ATS2-M0-013 = DONE` задачи M1 не переводятся в `READY`.

## 3. M0 — Program Rebaseline

| Task ID | WBS | Priority | Status | Responsible | Dependencies | Deliverable | Definition of Done / result |
|---|---|---:|---|---|---|---|---|
| `ATS2-M0-001` | `WBS-0.1` | P0 | DONE | OWNER | — | `governance/program/PROGRAM_CHARTER_V2.md` | Mission, scope, success/failure criteria и milestones зафиксированы |
| `ATS2-M0-002` | `WBS-0.2` | P0 | DONE | OWNER / PROGRAM | M0-001 | `governance/program/OPERATING_MODEL_V2.md` | Entities, contours, states, roles и decision points определены |
| `ATS2-M0-003` | `WBS-0.3` | P0 | DONE | RESEARCH / RISK / VALIDATION | M0-001, M0-002 | `governance/methodology/STRATEGY_LIFECYCLE_V2.md` | Research Funnel и Strategy Lifecycle определены |
| `ATS2-M0-004` | `WBS-0.4` | P0 | DONE | RESEARCH / VALIDATION | M0-002, M0-003 | `governance/methodology/RESEARCH_METHODOLOGY_V1.md` | Evidence и economic usefulness формализованы |
| `ATS2-M0-005` | `WBS-0.5` | P0 | DONE | PROGRAM | M0-001…004 | `governance/program/PROGRAM_WBS_V2.md` | M0–M8 разложены на work packages |
| `ATS2-M0-006` | `WBS-0.6` | P0 | DONE | PROGRAM / DEVELOPMENT | M0-005 | `governance/program/REPOSITORY_STRUCTURE_V2.md` | Target layout, canonical locations и migration rules определены |
| `ATS2-M0-007` | `WBS-0.7` | P0 | DONE | PROGRAM | M0-005, M0-006 | `governance/backlog/PROGRAM_BACKLOG_V2.md` | M0–M2 имеют executable tasks; M3–M8 остаются epics |
| `ATS2-M0-008` | `WBS-0.8` | P0 | DONE | RESEARCH / PROGRAM | M0-004, M0-006, M0-007 | Research entity templates | Idea, Hypothesis, Candidate, Experiment и Strategy Version имеют reusable templates |
| `ATS2-M0-009` | `WBS-0.6`, `WBS-0.12` | P0 | DONE | PROGRAM / DEVELOPMENT | M0-008 | Canonical v2 governance tree | Current v2 находится в `governance/`; временные current-v2 paths удалены |
| `ATS2-M0-010` | `WBS-0.12` | P0 | DONE | PROGRAM | M0-009 | `legacy/v1/README.md` + `legacy/v1/MIGRATION_INDEX.md` | 15 v1 artifacts классифицированы и получили target paths |
| `ATS2-M0-011` | `WBS-0.12` | P0 | DONE | PROGRAM / DEVELOPMENT | M0-010 | `legacy/v1/` + `legacy/v1/CARRYOVER.md` | Legacy перенесён, old source paths удалены, OQ remap выполнен |
| `ATS2-M0-012` | `WBS-0.10`, `WBS-0.12` | P0 | DONE | DEVELOPMENT / PROGRAM | M0-011 | `governance/program/M0_FINAL_SWEEP.md` + hardened validator | Sweep нашёл и исправил два stale AI pointers; canonical paths/local links проверяются автоматически; CI run 105 — success |
| `ATS2-M0-013` | M0 Exit | P0 | READY | OWNER / PROGRAM | M0-012 | `governance/program/M0_EXIT_REVIEW.md` | Подтвердить WBS-0.1…0.12, зелёный CI, корректный handoff и readiness к M1; затем закрыть M0 |

Cross-cutting `WBS-0.9` canonical state и `WBS-0.11` AI handoff действуют.

## 4. M1 — Research Factory

Все M1 tasks пока `BLOCKED` зависимостью `ATS2-M0-013`.

| Task ID | WBS | Priority | Status | Dependencies | Deliverable |
|---|---|---:|---|---|---|
| `ATS2-M1-001` | `WBS-1.1` | P1 | BLOCKED | M0-013 | Idea intake process + tested Idea template |
| `ATS2-M1-002` | `WBS-1.2` | P1 | BLOCKED | M1-001 | Hypothesis model + tested template |
| `ATS2-M1-003` | `WBS-1.3` | P1 | BLOCKED | M1-002 | Data Feasibility review model |
| `ATS2-M1-004` | `WBS-1.4` | P1 | BLOCKED | M1-002, M1-003 | Cheap Prototype protocol |
| `ATS2-M1-005` | `WBS-1.5` | P1 | BLOCKED | M1-004 | Economic Pre-Screen rubric |
| `ATS2-M1-006` | `WBS-1.6` | P1 | BLOCKED | M1-005 | Candidate promotion process |
| `ATS2-M1-007` | `WBS-1.7` | P1 | BLOCKED | M1-002, M0-013 | Experiment registration schema |
| `ATS2-M1-008` | `WBS-1.8` | P1 | BLOCKED | M1-007 | Experiment registry |
| `ATS2-M1-009` | `WBS-1.9` | P1 | BLOCKED | M0-013 | Evidence taxonomy operationalization |
| `ATS2-M1-010` | `WBS-1.10` | P1 | BLOCKED | M1-001…009 | Research review protocol |
| `ATS2-M1-011` | M1 Exit | P1 | BLOCKED | M1-001…010 | M1 exit decision |

## 5. M2 and later

M2 remains `PARKED` until M1 Exit. `ATS2-M2-000 — Reference Consumer Profile` precedes `ATS2-M2-001 — Research stack ADR`. M3–M8 remain future epics and must consult `legacy/v1/CARRYOVER.md` when decomposed.

## 6. Следующий шаг

Текущая ready task:

`ATS2-M0-013 — M0 Exit Review`.

Canonical next artifact:

`governance/program/M0_EXIT_REVIEW.md`.

Exit Review must decide whether Program Rebaseline is complete and whether M1 Research Factory may start. It does not choose a concrete strategy, broker, capital allocation or live risk limits.
