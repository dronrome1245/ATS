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
2. `ATS2-M1-001…011` — M1 Research Methodology — `DONE / PASS`.
3. `ATS2-M2-000` — Reference Consumer Profile — `DONE`.
4. `ATS2-M2-001` — Research stack ADR — `READY`.
5. `ATS2-M2-002` — Reproducible environment — после M2-001.
6. `ATS2-M2-003` — Dataset manifest support — после M2-001.
7. `ATS2-M2-004` — Base data loader — после M2-003.
8. `ATS2-M2-005` — Minimal Strategy research interface — после M2-001.
9. `ATS2-M2-006` — Deterministic backtest/replay — после M2-004/M2-005.
10. `ATS2-M2-007` — Cost model interface — после M2-006.
11. `ATS2-M2-008` — Standard analytics/report — после M2-006/M2-007.
12. `ATS2-M2-009` — Manifest-driven experiment runner — после M2-002…008.
13. `ATS2-M2-010` — Research platform tests — после M2-004…009.
14. `ATS2-M2-011` — M2 Exit — после M2-000…010.

Program-level current next task — `ATS2-M2-001`.

## 3. M0 / M1

`M0_PROGRAM_REBASELINE = COMPLETED / PASS`.

`M1_RESEARCH_METHODOLOGY = COMPLETED / PASS`.

Canonical exits:

- `governance/program/M0_EXIT_REVIEW.md`;
- `governance/program/M1_EXIT_REVIEW.md`.

## 4. M2 — Shared Research Platform MVP

| Task ID | WBS | Priority | Status | Dependencies | Deliverable | Definition of Done |
|---|---|---:|---|---|---|---|
| `ATS2-M2-000` | `WBS-2.0` | P1 | DONE | M1 Exit PASS | `governance/program/REFERENCE_CONSUMER_PROFILE.md` | Minimum abstract ordered-data research consumer is defined without choosing a concrete market/instrument/strategy/live environment; WBS-2.0 exists and WBS-2.1 is driven by this profile |
| `ATS2-M2-001` | `WBS-2.1` | P1 | READY | M2-000 | `governance/decisions/ADR-0001-RESEARCH-STACK.md` | Select the minimum research technology stack against Consumer Profile requirements for reproducibility, ordered data, replay, costs, analytics, experiments and tests; record rejected heavier alternatives; no broker/live stack |
| `ATS2-M2-002` | `WBS-2.2` | P1 | BLOCKED | M2-001 | Reproducible environment specification | A clean supported environment can reproduce the same registered experiment context |
| `ATS2-M2-003` | `WBS-2.3` | P1 | BLOCKED | M2-001 | Dataset manifest support | Dataset identity/source/period/timestamp/transformation context is stable |
| `ATS2-M2-004` | `WBS-2.4` | P1 | BLOCKED | M2-003 | Base data loader | Reference-format data load deterministically with ordering/time semantics |
| `ATS2-M2-005` | `WBS-2.5` | P1 | BLOCKED | M2-001 | Minimal Strategy research interface | Research logic consumes ordered observations and emits serializable decisions without broker-specific code |
| `ATS2-M2-006` | `WBS-2.6` | P1 | BLOCKED | M2-004, M2-005 | Deterministic backtest/replay core | Same frozen input context produces reproducible decisions and result/trade/effect output |
| `ATS2-M2-007` | `WBS-2.7` | P1 | BLOCKED | M2-006 | Cost model interface | Costs are explicit experiment inputs and reported separately from gross output |
| `ATS2-M2-008` | `WBS-2.8` | P1 | BLOCKED | M2-006, M2-007 | Standard analytics/report | Baseline output exposes effect/P&L, risk/path, events/trades and costs as applicable |
| `ATS2-M2-009` | `WBS-2.9` | P1 | BLOCKED | M2-002…008 | Manifest-driven experiment runner | Registered experiment context can be replayed by a documented procedure without rewriting preregistration |
| `ATS2-M2-010` | `WBS-2.10` | P1 | BLOCKED | M2-004…009 | Research platform tests | Critical calculations have deterministic non-market fixtures/regression checks |
| `ATS2-M2-011` | M2 Exit | P1 | BLOCKED | M2-000…010 | M2 exit decision | Minimal reusable vertical research stack can reproduce an end-to-end baseline registered experiment workflow |

`M2-000` is not Reference Strategy #1 selection. The profile defines a software/research consumer contract only.

## 5. M3 and later

Reference Strategy #1 selection remains in M3 after M2 Exit. M2 must not invent a market, instrument, trading hypothesis, return target or live execution environment just to drive platform design.

Carryover from ATS v1 remains governed by `legacy/v1/CARRYOVER.md`.

## 6. Следующий шаг

Current program-level ready task:

`ATS2-M2-001 — Research stack ADR`.

Canonical next artifact:

`governance/decisions/ADR-0001-RESEARCH-STACK.md`.

The ADR must choose the smallest viable research stack against `governance/program/REFERENCE_CONSUMER_PROFILE.md`, explain reproducibility/data/replay/testing tradeoffs, and explicitly avoid premature live/broker/portfolio infrastructure.
