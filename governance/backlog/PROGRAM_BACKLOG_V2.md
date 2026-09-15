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
6. `ATS2-M1-005` — Economic Pre-Screen — `DONE`.
7. `ATS2-M1-006` — Candidate promotion — `DONE`.
8. `ATS2-M1-007` — Experiment registration schema — `DONE`.
9. `ATS2-M1-008` — Experiment registry — `DONE`.
10. `ATS2-M1-009` — Evidence taxonomy operationalization — `DONE`.
11. `ATS2-M1-010` — Research review protocol — `DONE`.
12. `ATS2-M1-011` — M1 Exit Review — `DONE / PASS`.
13. `ATS2-M2-000` — Reference Consumer Profile — `READY`.
14. `ATS2-M2-001` — Research stack ADR — `BLOCKED` by M2-000.

Program-level current next task — `ATS2-M2-000`.

## 3. M0 — Program Rebaseline

`M0_PROGRAM_REBASELINE = COMPLETED / PASS`.

Canonical exit evidence: `governance/program/M0_EXIT_REVIEW.md`.

## 4. M1 — Research Factory

`M1_RESEARCH_METHODOLOGY = COMPLETED / PASS`.

Canonical exit evidence: `governance/program/M1_EXIT_REVIEW.md`.

| Task ID | WBS | Priority | Status | Deliverable / result |
|---|---|---:|---|---|
| `ATS2-M1-001` | `WBS-1.1` | P1 | DONE | Idea intake process + aligned template |
| `ATS2-M1-002` | `WBS-1.2` | P1 | DONE | Falsifiable Hypothesis model |
| `ATS2-M1-003` | `WBS-1.3` | P1 | DONE | Data Feasibility review |
| `ATS2-M1-004` | `WBS-1.4` | P1 | DONE | Cheap Prototype protocol |
| `ATS2-M1-005` | `WBS-1.5` | P1 | DONE | Economic Pre-Screen |
| `ATS2-M1-006` | `WBS-1.6` | P1 | DONE | Candidate promotion process |
| `ATS2-M1-007` | `WBS-1.7` | P1 | DONE | Experiment preregistration |
| `ATS2-M1-008` | `WBS-1.8` | P1 | DONE | Searchable Experiment Registry |
| `ATS2-M1-009` | `WBS-1.9` | P1 | DONE | Evidence taxonomy / claim limits |
| `ATS2-M1-010` | `WBS-1.10` | P1 | DONE | Event-driven Research Review protocol |
| `ATS2-M1-011` | M1 Exit | P1 | DONE / PASS | `governance/program/M1_EXIT_REVIEW.md` |

M1 Exit confirms the structural flow:

`Idea → Hypothesis → Data Feasibility → Cheap Prototype → Economic Pre-Screen → Candidate Review → Experiment → Registry → Evidence Classification → Research Review`.

Structural testing created no fictitious trading entities/results; zero pipeline counts are intentional.

## 5. M2 — Shared Research Platform MVP

M2 begins after M1 Exit PASS.

### Entry bridge before WBS-2.1

| Task ID | WBS | Priority | Status | Dependencies | Deliverable | Definition of Done |
|---|---|---:|---|---|---|---|
| `ATS2-M2-000` | `WBS-2.0` | P1 | READY | M1 Exit PASS | `governance/program/REFERENCE_CONSUMER_PROFILE.md` | Define minimum abstract consumer requirements for the first vertical research stack without selecting a concrete market/instrument/strategy; align WBS-2.1 wording/dependency so stack selection is driven by this profile rather than a not-yet-selected M3 strategy |
| `ATS2-M2-001` | `WBS-2.1` | P1 | BLOCKED | M2-000 | Research stack ADR | Select the minimum research technology stack from reproducibility, data, replay, experiment and consumer-profile requirements; no broker/live stack |
| `ATS2-M2-002` | `WBS-2.2` | P1 | BLOCKED | M2-001 | Reproducible environment specification | A clean environment can reproduce the same registered experiment context |
| `ATS2-M2-003` | `WBS-2.3` | P1 | BLOCKED | M2-001 | Dataset manifest support | Dataset identity/source/period/timestamp/transformation context is stable |
| `ATS2-M2-004` | `WBS-2.4` | P1 | BLOCKED | M2-003 | Base data loader | Reference-format data load deterministically with ordering/time semantics |
| `ATS2-M2-005` | `WBS-2.5` | P1 | BLOCKED | M2-001 | Minimal Strategy research interface | Research logic consumes data and emits decisions without broker-specific code |
| `ATS2-M2-006` | `WBS-2.6` | P1 | BLOCKED | M2-004, M2-005 | Deterministic backtest/replay core | Same input context produces reproducible result/trade output |
| `ATS2-M2-007` | `WBS-2.7` | P1 | BLOCKED | M2-006 | Cost model interface | Costs are explicit experiment inputs |
| `ATS2-M2-008` | `WBS-2.8` | P1 | BLOCKED | M2-006, M2-007 | Standard analytics/report | Baseline output exposes P&L/effect, drawdown/risk, events/trades and costs as applicable |
| `ATS2-M2-009` | `WBS-2.9` | P1 | BLOCKED | M2-002…008 | Manifest-driven experiment runner | Registered experiment context can be replayed by documented procedure |
| `ATS2-M2-010` | `WBS-2.10` | P1 | BLOCKED | M2-004…009 | Research platform tests | Critical calculations have deterministic fixtures/regression checks |
| `ATS2-M2-011` | M2 Exit | P1 | BLOCKED | M2-000…010 | M2 exit decision | Minimal reusable vertical research stack can reproduce a baseline registered experiment workflow |

`M2-000` is deliberately not Reference Strategy #1 selection. It fixes a consumer profile, not a market thesis or trading system.

## 6. M3 and later

Reference Strategy #1 selection remains in M3 after M2 Exit. M2 must not invent a market, instrument, trading hypothesis, return target or live execution environment just to drive platform design.

Carryover from ATS v1 remains governed by `legacy/v1/CARRYOVER.md`.

## 7. Следующий шаг

Current program-level ready task:

`ATS2-M2-000 — Reference Consumer Profile`.

Canonical next artifact:

`governance/program/REFERENCE_CONSUMER_PROFILE.md`.

The profile defines the minimum research consumer contract needed to choose/build M2 capabilities while preserving the boundary that concrete Reference Strategy #1 selection happens in M3.