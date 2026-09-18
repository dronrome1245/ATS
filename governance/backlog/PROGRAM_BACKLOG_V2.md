# ATS Program Backlog v2

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 2.0  
**Статус:** BASELINE  
**Дата:** 18 сентября 2026 года  
**WBS:** `governance/program/PROGRAM_WBS_V2.md`  
**Repository Structure:** `governance/program/REPOSITORY_STRUCTURE_V2.md`

## 1. Назначение

Backlog превращает Program WBS в исполнимую очередь работ. Material program task не считается завершённой до синхронизации state/status/next-step/handoff и полного локального quality gate. На Windows стандартный OWNER workflow — `ATS_TASK_CHECK.bat`, который формирует `reports/local_ci/CURRENT_TASK_REPORT.txt`. GitHub Actions не является completion gate.

## 2. Текущая execution queue

1. `ATS2-M0-013` — M0 Exit Review — `DONE`.
2. `ATS2-M1-001…011` — M1 Research Methodology — `DONE / PASS`.
3. `ATS2-M2-000` — Reference Consumer Profile — `DONE`.
4. `ATS2-M2-001` — Research stack ADR — `DONE`.
5. `ATS2-M2-002` — Reproducible environment — `DONE`.
6. `ATS2-M2-003` — Dataset manifest support — `DONE`.
7. `ATS2-M2-004` — Base data loader — `DONE`.
8. `ATS2-M2-005` — Minimal Strategy research interface — `DONE`.
9. `ATS2-M2-006` — Deterministic backtest/replay — `READY`.
10. `ATS2-M2-007` — Cost model interface — `BLOCKED` by M2-006.
11. `ATS2-M2-008` — Standard analytics/report — `BLOCKED` by M2-006/M2-007.
12. `ATS2-M2-009` — Manifest-driven experiment runner — `BLOCKED` by M2-002…008.
13. `ATS2-M2-010` — Research platform tests — `BLOCKED` by M2-004…009.
14. `ATS2-M2-011` — M2 Exit — `BLOCKED` by M2-000…010.

Program-level current next task — `ATS2-M2-006`.

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
| `ATS2-M2-001` | `WBS-2.1` | P1 | DONE | M2-000 | `governance/decisions/ADR-0001-RESEARCH-STACK.md` | Accepted stack is CPython 3.13 + uv/pyproject/uv.lock, Pydantic v2 + PyYAML boundary validation, NumPy 2.x analytics, typed ordered-record replay semantics, pytest + Ruff; heavier data/live frameworks are deferred until a real consumer needs them |
| `ATS2-M2-002` | `WBS-2.2` | P1 | DONE | M2-001 | `governance/program/RESEARCH_ENVIRONMENT_SPEC.md` + `pyproject.toml` + `.python-version` + `uv.lock` + environment fingerprint/test | Canonical environment supports Windows x86_64 and Linux x86_64 with CPython 3.13.15 + uv 0.12.13; direct/transitive dependencies and install artifacts are locked; `uv sync --frozen` / `uv run --frozen` workflow, fingerprint and environment test are defined |
| `ATS2-M2-003` | `WBS-2.3` | P1 | DONE | M2-001, M2-002 | `governance/program/DATASET_MANIFEST_SPEC.md` + `data/manifests/DATASET_TEMPLATE.yaml` + `src/ats/schemas/dataset_manifest.py` + tests | Stable dataset ID/version, source/snapshot, coverage, event/availability time, deterministic ordering/tie-break, explicit quality policy, transformation lineage, integrity metadata and known limitations are typed and validated with safe YAML/Pydantic using synthetic non-market fixtures |
| `ATS2-M2-004` | `WBS-2.4` | P1 | DONE | M2-003 | `src/ats/data/loader.py` + deterministic loader fixtures/tests | UTF-8 CSV reference data load deterministically from a validated Dataset Manifest with explicit RFC3339 time semantics, ordering/tie-break, duplicate/malformed/out-of-order policies, coverage enforcement and optional SHA-256 verification |
| `ATS2-M2-005` | `WBS-2.5` | P1 | DONE | M2-001, M2-004 | `src/ats/strategy/interface.py` + `tests/test_strategy_interface.py` | Immutable run/observation inputs, generic deterministic state transition, broker-neutral serializable decisions/diagnostics and loader-record bridge are defined without wall-clock/network/broker dependencies |
| `ATS2-M2-006` | `WBS-2.6` | P1 | READY | M2-004, M2-005 | `src/ats/replay/engine.py` + deterministic replay tests | Same frozen loader output + run context + research strategy produces reproducible ordered decision/state/diagnostic trace without hidden wall-clock/network inputs |
| `ATS2-M2-007` | `WBS-2.7` | P1 | BLOCKED | M2-006 | Cost model interface | Costs are explicit experiment inputs and reported separately from gross output |
| `ATS2-M2-008` | `WBS-2.8` | P1 | BLOCKED | M2-006, M2-007 | Standard analytics/report | Baseline output exposes effect/P&L, risk/path, events/trades and costs as applicable |
| `ATS2-M2-009` | `WBS-2.9` | P1 | BLOCKED | M2-002…008 | Manifest-driven experiment runner | Registered experiment context can be replayed by a documented procedure without rewriting preregistration |
| `ATS2-M2-010` | `WBS-2.10` | P1 | BLOCKED | M2-004…009 | Research platform tests | Critical calculations have deterministic non-market fixtures/regression checks |
| `ATS2-M2-011` | M2 Exit | P1 | BLOCKED | M2-000…010 | M2 exit decision | Minimal reusable vertical research stack can reproduce an end-to-end baseline registered experiment workflow |

`M2-000…005` still do not select Reference Strategy #1. M2-005 adds only a broker-neutral research-logic contract and synthetic fixture logic; it does not add a trading strategy or research evidence.

## 5. M3 and later

Reference Strategy #1 selection remains in M3 after M2 Exit. M2 must not invent a market, instrument, trading hypothesis, return target or live execution environment just to drive platform design.

Carryover from ATS v1 remains governed by `legacy/v1/CARRYOVER.md`.

## 6. Следующий шаг

Current program-level ready task:

`ATS2-M2-006 — Deterministic backtest/replay`.

Canonical next artifact:

`src/ats/replay/engine.py`.

M2-006 must consume the M2 loader and Strategy/Research interface to produce a deterministic ordered trace. It must not implement costs, analytics, broker/live execution or Reference Strategy #1.
