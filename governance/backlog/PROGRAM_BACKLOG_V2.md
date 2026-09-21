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
9. `ATS2-M2-006` — Deterministic backtest/replay — `DONE`.
10. `ATS2-M2-007` — Cost model interface — `DONE`.
11. `ATS2-M2-008` — Standard analytics/report — `DONE`.
12. `ATS2-M2-009` — Manifest-driven experiment runner — `DONE`.
13. `ATS2-M2-010` — Research platform tests — `DONE`.
14. `ATS2-M2-011` — M2 Exit — `DONE / PASS`.
15. `ATS2-M3-001` — Select Reference Strategy #1 — `DONE`.
16. `ATS2-M3-002` — Idea & rationale — `READY`.

Program-level current next task — `ATS2-M3-002`.

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
| `ATS2-M2-006` | `WBS-2.6` | P1 | DONE | M2-004, M2-005 | `src/ats/replay/engine.py` + `tests/test_replay_engine.py` | Same frozen loader output + run context + research strategy produces reproducible ordered observation/state/decision/diagnostic trace with availability-time causality checks and no hidden wall-clock/network inputs |
| `ATS2-M2-007` | `WBS-2.7` | P1 | DONE | M2-006 | `src/ats/costs/interface.py` + tests | Costs are explicit deterministic inputs applied outside strategy logic and kept separate from gross effects/results |
| `ATS2-M2-008` | `WBS-2.8` | P1 | DONE | M2-006, M2-007 | `src/ats/analytics/standard.py` + `tests/test_standard_analytics.py` | Baseline output exposes effect/P&L, risk/path, events/trades and costs as applicable |
| `ATS2-M2-009` | `WBS-2.9` | P1 | DONE | M2-002…008 | `src/ats/runner/experiment.py` + `tests/test_experiment_runner.py` | Registered experiment context can be replayed by a documented procedure without rewriting preregistration |
| `ATS2-M2-010` | `WBS-2.10` | P1 | DONE | M2-004…009 | `tests/test_research_platform.py` + `tests/fixtures/platform/reference_consumer_expected.json` | Critical calculations have deterministic non-market fixtures/regression checks |
| `ATS2-M2-011` | M2 Exit | P1 | DONE / PASS | M2-000…010 | `governance/program/M2_EXIT_REVIEW.md` | Minimal reusable vertical research stack can reproduce an end-to-end baseline registered experiment workflow |

M2 Exit decision: `PASS`. The platform milestone is complete; this does not create research evidence for a trading strategy.

## 5. M3 — Reference Strategy #1

| Task ID | WBS | Priority | Status | Dependencies | Deliverable | Definition of Done |
|---|---|---:|---|---|---|---|
| `ATS2-M3-001` | `WBS-3.1` | P1 | DONE | M1 PASS, M2 PASS | `governance/program/REFERENCE_STRATEGY_1_SELECTION.md` | Selected `SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT` as the first reference strategy class without selecting parameters, instrument, vendor or claiming profitability |
| `ATS2-M3-002` | `WBS-3.2` | P1 | READY | M3-001 | `research/ideas/IDEA-0001.md` + `research/hypotheses/HYP-0001.md` | A real screened Idea and falsifiable Hypothesis are registered for the selected class with rationale, information premise, expected effect, falsification path and required data |

Later M3 work remains governed by `WBS-3.3`–`WBS-3.11` in `governance/program/PROGRAM_WBS_V2.md` and is instantiated into executable backlog tasks as dependencies become ready.

Reference Strategy #1 class is selected, but no instrument, parameter set, Candidate, Strategy ID or Experiment has yet been created.

Carryover from ATS v1 remains governed by `legacy/v1/CARRYOVER.md`.

## 6. Следующий шаг

Current program-level ready task:

`ATS2-M3-002 — Idea & rationale`.

Canonical next artifact:

`research/ideas/IDEA-0001.md`.

M3-002 must register the first real Idea and corresponding falsifiable Hypothesis for the selected 1H long/flat trend-breakout class. It must not choose parameters by inspecting a profitable backtest.
