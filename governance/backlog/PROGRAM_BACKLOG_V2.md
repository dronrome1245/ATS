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
16. `ATS2-M3-002` — Idea & rationale — `DONE`.
17. `ATS2-M3-003` — Data feasibility — `DONE / CONDITIONAL`.
18. `ATS2-M3-004` — Cheap prototype — `DONE / REJECT`.
19. `ATS2-M3-005` — M3 early-rejection closeout / platform learning review — `DONE / PASS`.
20. `ATS2-M4-001` — Validation protocol framework — `DONE`.
21. `ATS2-M4-002` — Parameter sensitivity tooling — `DONE`.
22. `ATS2-M4-003` — Time/regime slicing — `DONE`.
23. `ATS2-M4-004` — Observation concentration analysis — `DONE`.
24. `ATS2-M4-005` — Dependence-preserving resampling framework — `DONE`.
25. `ATS2-M4-006` — Independent exam protocol — `DONE`.
26. `ATS2-M4-007` — Multiple-research accounting — `DONE`.
27. `ATS2-M4-008` — Technical strategy validation profile — `DONE`.
28. `ATS2-M6-000` — Market Pattern Discovery capability — `DONE`.
29. `ATS2-M6-001` — First bounded discovery run — `DONE`.
30. `ATS2-M6-002` — Strategy #2 class selection and Idea intake — `DONE`.
31. `ATS2-M6-003` — HYP-0002 formation — `DONE`.
32. `ATS2-M6-004` — HYP-0002 Data Feasibility preparation — `DONE`.
33. `ATS2-M6-005` — HYP-0002 Data Feasibility freeze — `DONE`.
34. `ATS2-M6-006` — HYP-0002 PROTO-01 freeze — `READY`.

Program-level current next task — `ATS2-M6-006`.

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
| `ATS2-M3-002` | `WBS-3.2` | P1 | DONE | M3-001 | `research/ideas/IDEA-0001.md` + `research/hypotheses/HYP-0001.md` | `IDEA-0001` is screened and `HYP-0001` fixes a 24-bar breakout condition, 24-bar primary horizon, BID/ASK execution premise and falsification path before prototype results |
| `ATS2-M3-003` | `WBS-3.3` | P1 | DONE / CONDITIONAL | M3-002 | `research/reviews/HYP-0001-DATA_FEASIBILITY.md` | Dukascopy EUR/USD 1H BID/ASK path is structurally suitable; actual snapshot/coverage must be frozen before prototype execution, and PROTO-01 economic claims remain before-financing unless rollover/commission inputs are added |
| `ATS2-M3-004` | `WBS-3.4` | P1 | DONE / REJECT | M3-002, M3-003 CONDITIONAL | `research/reviews/HYP-0001-PROTOTYPE-01.md` + dataset manifest + `reports/research/HYP-0001-PROTOTYPE-01-result.json` | 1006 fixed-rule signals were observed; signal mean return was negative and below baseline, so the preregistered rule produced `REJECT` and the line stops before Economic Pre-Screen |
| `ATS2-M3-005` | `WBS-3.11 (early-rejection path)` | P1 | DONE / PASS | M3-004 REJECT | `governance/program/M3_EXIT_REVIEW.md` | R3 rejection is preserved; WBS-3.5–3.10 are not entered; real-data/platform learnings are recorded; M3 Exit = PASS without tuning HYP-0001 |

Because PROTO-01 returned `REJECT`, WBS-3.5–3.10 are not entered for this research line. The remaining M3 work is the early-rejection platform-learning/exit path under WBS-3.11.

Reference Strategy #1 class and EUR/USD research instrument are selected, and `HYP-0001` fixes the initial 24-bar research parameters; no Candidate, Strategy ID or Experiment has yet been created.

Carryover from ATS v1 remains governed by `legacy/v1/CARRYOVER.md`.

## 6. M4 — Validation Framework

| Task ID | WBS | Priority | Status | Dependencies | Deliverable | Definition of Done |
|---|---|---:|---|---|---|---|
| `ATS2-M4-001` | `WBS-4.1` | P1 | DONE | M3 PASS, M1 methodology | `governance/methodology/VALIDATION_FRAMEWORK.md` | Development/validation/independent boundaries, mandatory validation dimensions, dependence/overlap treatment, decision rules and tooling contracts are defined without inventing a Candidate or reopening HYP-0001 |
| `ATS2-M4-002` | `WBS-4.2` | P1 | DONE | M4-001, M2 platform | `src/ats/validation/sensitivity.py` + `tests/test_validation_sensitivity.py` | Ordered predefined variants are all evaluated and serialized; missing/extra/non-finite metrics fail closed; the result exposes `NO_AUTOMATIC_SELECTION` and no best/winner ranking |
| `ATS2-M4-003` | `WBS-4.3` | P1 | DONE | M4-001, M4-002 | `src/ats/validation/slicing.py` + `tests/test_validation_slicing.py` | Every declared slice is reported in plan order; exhaustive/overlap/empty-slice policies are explicit; unknown membership and metric-contract violations fail closed |
| `ATS2-M4-004` | `WBS-4.4` | P1 | DONE | M4-001, M4-003 | `src/ats/validation/concentration.py` + `tests/test_validation_concentration.py` | Full observation/group set is retained; predeclared top-count diagnostics quantify absolute concentration; zero-denominator cases are explicit; no outlier is removed automatically |
| `ATS2-M4-005` | `WBS-4.5` | P1 | DONE | M4-001, M4-004 | `src/ats/validation/resampling.py` + `tests/test_validation_resampling.py` | Whole declared blocks are resampled with replacement under an explicit seed/method; internal block order and full selection trace are preserved; no IID fallback exists in the API |
| `ATS2-M4-006` | `WBS-4.6` | P1 | DONE | M4-001, M4-005 | `governance/methodology/INDEPENDENT_EXAM_PROTOCOL.md` | Freeze manifest fixes version/code/config/data/costs/metrics/rule before reveal; reveal is irreversible; only PASS/FAIL exists; post-reveal repair cannot restore independence |
| `ATS2-M4-007` | `WBS-4.7` | P1 | DONE | M4-001, M4-006, experiment/discovery history | `governance/methodology/MULTIPLE_RESEARCH_ACCOUNTING.md` | Material Research Attempts, bounded-search denominators, negative/discarded outcomes, data/cost changes, returns to research and consumed protected blocks remain traceable to the selected version |
| `ATS2-M4-008` | `WBS-4.8` | P1 | DONE | M4-001…007 | `governance/methodology/TECHNICAL_STRATEGY_VALIDATION_PROFILE.md` | Technical price-driven strategy profile makes V1–V7 concrete, declares applicability/required evidence and specifies what must be frozen before S06/S07 |
| `ATS2-M6-000` | `WBS-6.0` | P1 | DONE | M2, M3 learnings, M4-008 | `governance/methodology/MARKET_PATTERN_DISCOVERY.md` + reusable bounded-search tooling | Search Manifest contract, deterministic full-denominator engine and synthetic contract tests are available without creating market evidence |
| `ATS2-M6-001` | `WBS-6.0` | P1 | DONE | M6-000 | `research/discovery/SEARCH-EURUSD-H1-2021-2025-001.yaml` + `reports/research/SEARCH-EURUSD-H1-2021-2025-001-summary.md` | Exact-head run evaluated all 16 alternatives, retained full denominator and returned `SHORTLIST_FOR_IDEA_INTAKE` with five reversal variants |
| `ATS2-M6-002` | `WBS-6.1` | P1 | DONE | M6-001 | `governance/program/REFERENCE_STRATEGY_2_SELECTION.md` + `research/ideas/IDEA-0002.md` | Selected the two-sided return-tail reversal class and screened IDEA-0002 without promoting one discovery cell as a winner |
| `ATS2-M6-003` | `WBS-6.2` | P1 | DONE | M6-002 | `research/hypotheses/HYP-0002.md` | Froze the post-discovery two-sided 24H reversal formulation and required development-only thresholds plus unseen confirmatory data |
| `ATS2-M6-004` | `WBS-6.2` | P1 | DONE | M6-003 | `research/reviews/HYP-0002-DATA-FEASIBILITY-PREP.md` + local preparation report | Froze Q10_DEV/Q90_DEV and the disjoint 2026-01 through 2026-08 Dukascopy BID/ASK block with no HYP-0002 outcome calculation |
| `ATS2-M6-005` | `WBS-6.2` | P1 | DONE | M6-004 | `research/reviews/HYP-0002-DATA-FEASIBILITY.md` + confirmatory Dataset Manifest | Recorded CONDITIONAL feasibility and froze thresholds, confirmatory data identity, timing and cost limitations before outcome reveal |
| `ATS2-M6-006` | `WBS-6.2` | P1 | READY | M6-005 | `research/reviews/HYP-0002-PROTOTYPE-01.md` + frozen runner/tests | Freeze one two-sided confirmatory prototype question, exact four-inequality decision rule and deterministic implementation without running the confirmatory result |

## 7. Следующий шаг

Current program-level ready task:

`ATS2-M6-006 — HYP-0002 PROTO-01 freeze`.

Canonical artifact:

`research/reviews/HYP-0002-PROTOTYPE-01.md`.

The prototype question, frozen thresholds/data identity, both tail sides, all four primary inequalities, decision rule and exact runner are fixed before the first confirmatory result is computed.

The M6-006 closure checker does not execute `tools/hyp0002_proto01.py`. After exact-head PASS, a separate task may run the frozen prototype once.
