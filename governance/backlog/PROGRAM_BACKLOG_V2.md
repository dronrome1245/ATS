# ATS Program Backlog v2

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 2.0  
**Статус:** BASELINE  
**Дата:** 15 сентября 2026 года  
**WBS:** `governance/program/PROGRAM_WBS_V2.md`  
**Repository Structure:** `governance/program/REPOSITORY_STRUCTURE_V2.md`

## 1. Назначение

Этот backlog превращает Program WBS в исполнимую очередь работ.

Правила:

- task получает стабильный ID и не переиспользуется;
- сроки не назначаются без фактического исполнителя, входов и оценки сложности;
- одновременно активируется минимально необходимое число дорогих задач;
- дальние milestones не детализируются преждевременно;
- `DONE` требует deliverable, выполненный Definition of Done и синхронизированный handoff/state;
- `BLOCKED` всегда содержит конкретную зависимость или отсутствующее решение.

## 2. Статусы и приоритеты

Статусы: `DONE`, `IN_PROGRESS`, `READY`, `BLOCKED`, `NOT_STARTED`, `PARKED`, `CANCELLED`.

Приоритеты:

- `P0` — critical path текущего milestone;
- `P1` — следующий research milestone/supporting capability;
- `P2` — следующий technical milestone;
- `P3` — future epic без преждевременной детализации.

## 3. Текущая execution queue

1. `ATS2-M0-008` — Research entity templates — `DONE`.
2. `ATS2-M0-009` — Governance v2 path migration — `DONE`.
3. `ATS2-M0-010` — Legacy v1 index/classification — `DONE`.
4. `ATS2-M0-011` — Legacy physical migration and unresolved-question carryover — `READY`.
5. `ATS2-M0-012` — Final link/validator sweep — после structural migrations.
6. `ATS2-M0-013` — M0 Exit Review — после всех обязательных M0 tasks.

До `ATS2-M0-013 = DONE` задачи M1 не переводятся в `READY`.

# 4. M0 — Program Rebaseline

| Task ID | WBS | Priority | Status | Responsible | Dependencies | Deliverable | Definition of Done / block reason |
|---|---|---:|---|---|---|---|---|
| `ATS2-M0-001` | `WBS-0.1` | P0 | DONE | OWNER | — | `governance/program/PROGRAM_CHARTER_V2.md` | Mission, scope, success/failure criteria и milestones зафиксированы |
| `ATS2-M0-002` | `WBS-0.2` | P0 | DONE | OWNER / PROGRAM | M0-001 | `governance/program/OPERATING_MODEL_V2.md` | Entities, contours, states, roles и decision points определены |
| `ATS2-M0-003` | `WBS-0.3` | P0 | DONE | RESEARCH / RISK / VALIDATION | M0-001, M0-002 | `governance/methodology/STRATEGY_LIFECYCLE_V2.md` | Research Funnel и Strategy Lifecycle определены |
| `ATS2-M0-004` | `WBS-0.4` | P0 | DONE | RESEARCH / VALIDATION | M0-002, M0-003 | `governance/methodology/RESEARCH_METHODOLOGY_V1.md` | Evidence и economic usefulness формализованы |
| `ATS2-M0-005` | `WBS-0.5` | P0 | DONE | PROGRAM | M0-001…004 | `governance/program/PROGRAM_WBS_V2.md` | M0–M8 разложены на work packages |
| `ATS2-M0-006` | `WBS-0.6` | P0 | DONE | PROGRAM / DEVELOPMENT | M0-005 | `governance/program/REPOSITORY_STRUCTURE_V2.md` | Target layout, canonical locations и migration rules определены |
| `ATS2-M0-007` | `WBS-0.7` | P0 | DONE | PROGRAM | M0-005, M0-006 | `governance/backlog/PROGRAM_BACKLOG_V2.md` | M0–M2 имеют executable tasks; M3–M8 остаются epics |
| `ATS2-M0-008` | `WBS-0.8` | P0 | DONE | RESEARCH / PROGRAM | M0-004, M0-006, M0-007 | `governance/methodology/templates/README.md` + templates | Idea, Hypothesis, Candidate, Experiment и Strategy Version создаются без повторного проектирования |
| `ATS2-M0-009` | `WBS-0.6`, `WBS-0.12` | P0 | DONE | PROGRAM / DEVELOPMENT | M0-008 | Canonical v2 governance tree | Current v2 перенесён в `governance/`; старые current-v2 copies удалены; state/handoff/validator переключены |
| `ATS2-M0-010` | `WBS-0.12` | P0 | DONE | PROGRAM | M0-009 | `legacy/v1/README.md` + `legacy/v1/MIGRATION_INDEX.md` | 15 v1 artifacts классифицированы как `HISTORY`, `REFERENCE` или `REVIEW_NEEDED`; target paths и carryover disposition определены |
| `ATS2-M0-011` | `WBS-0.12` | P0 | READY | PROGRAM / DEVELOPMENT | M0-010 | `legacy/v1/` populated + `legacy/v1/CARRYOVER.md` | Перенести 15 artifacts строго по `MIGRATION_INDEX.md`; удалить старые legacy locations после проверки; remap review-needed/OQ items в `CARRYOVER.md`; добавить в v2 backlog только отсутствующие concrete future tasks без выдумывания значений |
| `ATS2-M0-012` | `WBS-0.10`, `WBS-0.12` | P0 | BLOCKED | DEVELOPMENT / PROGRAM | M0-011 | Final M0 validator/link sweep | **Блокировка:** legacy physical migration не завершена. После неё validator проверяет target paths, отсутствие old legacy locations как operational source и handoff/state consistency |
| `ATS2-M0-013` | M0 Exit | P0 | BLOCKED | OWNER / PROGRAM | M0-008…012 | `governance/program/M0_EXIT_REVIEW.md` | **Блокировка:** остаются physical legacy migration и final sweep. Exit review подтверждает WBS-0.1…0.12, зелёный CI и корректный handoff в M1 |

Cross-cutting capabilities `WBS-0.9` canonical state, `WBS-0.10` validator v2 и `WBS-0.11` AI handoff уже действуют; финальный validator hardening остаётся в `ATS2-M0-012`.

# 5. M1 — Research Factory

Все M1 tasks блокируются `ATS2-M0-013`.

| Task ID | WBS | Priority | Status | Responsible | Dependencies | Deliverable |
|---|---|---:|---|---|---|---|
| `ATS2-M1-001` | `WBS-1.1` | P1 | BLOCKED | RESEARCH | M0-013 | Idea intake process + tested Idea template |
| `ATS2-M1-002` | `WBS-1.2` | P1 | BLOCKED | RESEARCH | M1-001 | Hypothesis model + tested template |
| `ATS2-M1-003` | `WBS-1.3` | P1 | BLOCKED | DATA | M1-002 | Data Feasibility review model |
| `ATS2-M1-004` | `WBS-1.4` | P1 | BLOCKED | RESEARCH | M1-002, M1-003 | Cheap Prototype protocol |
| `ATS2-M1-005` | `WBS-1.5` | P1 | BLOCKED | RESEARCH | M1-004 | Economic Pre-Screen rubric |
| `ATS2-M1-006` | `WBS-1.6` | P1 | BLOCKED | RESEARCH / VALIDATION | M1-005 | Candidate promotion process |
| `ATS2-M1-007` | `WBS-1.7` | P1 | BLOCKED | RESEARCH / DEVELOPMENT | M1-002, M0-013 | Experiment registration schema |
| `ATS2-M1-008` | `WBS-1.8` | P1 | BLOCKED | PROGRAM / RESEARCH | M1-007 | Experiment registry |
| `ATS2-M1-009` | `WBS-1.9` | P1 | BLOCKED | VALIDATION | M0-013 | Evidence taxonomy operationalization |
| `ATS2-M1-010` | `WBS-1.10` | P1 | BLOCKED | OWNER / RESEARCH | M1-001…009 | Research review protocol |
| `ATS2-M1-011` | M1 Exit | P1 | BLOCKED | OWNER / PROGRAM | M1-001…010 | M1 exit decision |

# 6. M2 — Shared Research Platform MVP

M2 tasks остаются `PARKED` до M1 Exit.

`ATS2-M2-000 — Reference Consumer Profile` устраняет циклическую зависимость между stack decision и будущим выбором Strategy #1: profile задаёт требования первого vertical slice, но не выбирает edge/instrument.

| Task ID | WBS | Priority | Status | Dependencies | Deliverable |
|---|---|---:|---|---|---|
| `ATS2-M2-000` | WBS refinement | P2 | PARKED | M1-011 | Reference Consumer Profile |
| `ATS2-M2-001` | `WBS-2.1` | P2 | PARKED | M1-011, M2-000 | Research stack ADR |
| `ATS2-M2-002` | `WBS-2.2` | P2 | PARKED | M2-001 | Environment specification |
| `ATS2-M2-003` | `WBS-2.3` | P2 | PARKED | M1-003, M2-001 | Dataset manifest support |
| `ATS2-M2-004` | `WBS-2.4` | P2 | PARKED | M2-003 | Base data loader |
| `ATS2-M2-005` | `WBS-2.5` | P2 | PARKED | M2-001 | Minimal Strategy API |
| `ATS2-M2-006` | `WBS-2.6` | P2 | PARKED | M2-004, M2-005 | Deterministic backtest/replay core |
| `ATS2-M2-007` | `WBS-2.7` | P2 | PARKED | M2-006 | Cost model interface |
| `ATS2-M2-008` | `WBS-2.8` | P2 | PARKED | M2-006, M2-007 | Standard baseline analytics |
| `ATS2-M2-009` | `WBS-2.9` | P2 | PARKED | M1-007, M2-002…008 | Manifest-driven experiment runner |
| `ATS2-M2-010` | `WBS-2.10` | P2 | PARKED | M2-004…009 | Research platform tests |
| `ATS2-M2-011` | M2 Exit | P2 | PARKED | M2-001…010 | M2 exit decision |

# 7. Future epics M3–M8

| Epic ID | Milestone | Status | Activation condition |
|---|---|---|---|
| `ATS2-EPIC-M3` | Reference Strategy #1 | PARKED | M1 + M2 Exit |
| `ATS2-EPIC-M4` | Validation Framework | PARKED | Strategy #1 `S05 PASS` |
| `ATS2-EPIC-M5` | Execution Platform | PARKED | Candidate `S07 PASS` |
| `ATS2-EPIC-M6` | Reference Strategy #2 | PARKED | Shared platform + first validated line |
| `ATS2-EPIC-M7` | Portfolio Layer | PARKED | Минимум две portfolio-relevant strategy lines |
| `ATS2-EPIC-M8` | Controlled Live Portfolio | PARKED | Portfolio layer + OWNER capital decisions |

# 8. Backlog operating rules

- `02_СЛЕДУЮЩИЙ_ШАГ.md` указывает одну program-level next task.
- Новая task добавляется только при обязательном deliverable, carryover, evidence gap или доказанной reusable need.
- Physical/structural migration всегда обновляет links, validator и handoff.
- Legacy document не становится current v2 автоматически.
- Material program task не закрывается до синхронизации backlog/state/status/next-step/handoff.

# 9. Следующий шаг

Текущая ready task:

`ATS2-M0-011 — Legacy physical migration and unresolved-question carryover`.

Canonical next artifact:

`legacy/v1/CARRYOVER.md`.

Использовать `legacy/v1/MIGRATION_INDEX.md` как единственный migration plan для 15 ATS v1 artifacts. Сначала создавать target copies, затем проверять, затем удалять старые paths. Review-needed содержание переносится в current v2 только через явный carryover/backlog item, а не копированием legacy policy.