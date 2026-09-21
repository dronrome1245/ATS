# M2 Exit Review — Shared Research Platform MVP

**Task:** `ATS2-M2-011`  
**Milestone:** `M2_RESEARCH_PLATFORM_MVP`  
**Decision:** `PASS`  
**Date:** 21 September 2026

## 1. Purpose

This review decides whether ATS has built the minimum reusable Research Platform MVP required to enter M3 Reference Strategy #1 work.

`PASS` means the platform can reproducibly load declared research data, run deterministic research logic, apply explicit costs, produce standard analytics/results and support a frozen Experiment context with automated acceptance checks.

It does **not** mean that a trading strategy is profitable, validated, selected for live use or admitted to any capital allocation.

## 2. Exit criteria

Program WBS defines M2 Exit as a minimum reusable vertical research stack.

For this review, the exit requires:

1. `WBS-2.0` through `WBS-2.10` complete;
2. the Reference Consumer Profile acceptance path is materialized and deterministic;
3. the platform can represent frozen Experiment context without rewriting preregistration;
4. explicit cost and applicability semantics are preserved;
5. the canonical environment and full Local CI pass on the accepted M2 implementation;
6. synthetic platform fixtures remain software evidence only and do not create fictitious research identities;
7. live/broker/portfolio capabilities remain outside M2 scope.

All criteria are satisfied.

## 3. WBS evidence

| Work package | Result | Canonical evidence |
|---|---|---|
| `WBS-2.0` Reference Consumer Profile | PASS | `governance/program/REFERENCE_CONSUMER_PROFILE.md` |
| `WBS-2.1` Research stack ADR | PASS | `governance/decisions/ADR-0001-RESEARCH-STACK.md` |
| `WBS-2.2` Reproducible environment | PASS | `governance/program/RESEARCH_ENVIRONMENT_SPEC.md`, `pyproject.toml`, `.python-version`, `uv.lock` |
| `WBS-2.3` Dataset Manifest | PASS | `governance/program/DATASET_MANIFEST_SPEC.md`, `src/ats/schemas/dataset_manifest.py` |
| `WBS-2.4` Base data loader | PASS | `src/ats/data/loader.py`, deterministic fixture/tests |
| `WBS-2.5` Strategy research interface | PASS | `src/ats/strategy/interface.py`, `tests/test_strategy_interface.py` |
| `WBS-2.6` Deterministic replay | PASS | `src/ats/replay/engine.py`, `tests/test_replay_engine.py` |
| `WBS-2.7` Cost model interface | PASS | `src/ats/costs/interface.py`, `tests/test_cost_interface.py` |
| `WBS-2.8` Standard analytics/report | PASS | `src/ats/analytics/standard.py`, `tests/test_standard_analytics.py` |
| `WBS-2.9` Manifest-driven runner | PASS | `src/ats/runner/experiment.py`, `tests/test_experiment_runner.py` |
| `WBS-2.10` Research platform tests | PASS | `tests/test_research_platform.py`, `tests/fixtures/platform/reference_consumer_expected.json` |

## 4. Reference Consumer acceptance

The M2 acceptance fixture demonstrates:

`Dataset Manifest → loader → Strategy/Research interface → replay → explicit costs → standard analytics/result → exact rerun`.

The committed expected result binds:

- Dataset ID/version and SHA-256;
- deterministic run context;
- ordered decisions and diagnostics;
- explicit applicable and `NOT_APPLICABLE` cost components;
- gross effect, modeled costs, net effect and path metrics;
- exact repeated canonical output.

The separate M2-009 runner suite verifies frozen registered-manifest orchestration, including code/environment/data identity checks and immutable preregistration bytes.

The acceptance fixture is deliberately not a real formal Experiment. It has no Idea, Hypothesis, Candidate, Strategy or Experiment identity and creates no Experiment Registry row.

## 5. Reproducibility and Local CI evidence

Accepted M2 implementation commit:

`953eac0e88608d782a825d7039c1eb1bf14577c6`

OWNER Local CI report on 21 September 2026 confirmed:

- M2-010 targeted acceptance package: 13 passed;
- complete pytest suite: 83 passed;
- working tree: CLEAN;
- repository validator: PASS;
- Ruff lint: PASS;
- Ruff format: PASS;
- environment fingerprint: PASS;
- CPython: 3.13.15;
- uv: 0.12.13;
- `ATS LOCAL CI: PASS`;
- `ATS CURRENT TASK CHECK: PASS`;
- `ATS TASK LAUNCHER: PASS`.

A repository audit also confirmed that all 29 artifacts listed as completed under M2 exist and that `experiments/REGISTRY.csv` has zero data rows.

## 6. Known limits that are not M2 blockers

M2 intentionally does not provide or prove:

- a selected Reference Strategy #1;
- a market, instrument or trading hypothesis;
- profitability or validated edge;
- a real registered market Experiment;
- production broker/exchange integration;
- live market data;
- Strategy Risk Mandate;
- capital allocation or portfolio logic;
- demo/shadow/live admission;
- production recovery/reconciliation;
- class-specific deep validation.

These belong to M3 or later milestones. Their absence is consistent with the Reference Consumer Profile and M2 scope.

The generic runner also leaves `machine_outcome` null unless a future stage provides a safely machine-evaluable registered decision rule. Human/stage interpretation remains in the Experiment conclusion/review process.

## 7. Safety boundary after M2

M2 Exit does **not** authorize:

- demo/shadow trading;
- real-money trading;
- minimal live trading;
- capital allocation;
- leverage or risk limits;
- Strategy Risk Mandate;
- broker/account selection;
- scaling;
- profit withdrawal.

All current live/capital safety permissions remain false.

M2 Exit only permits ATS to begin M3 research work, starting with a deliberate Reference Strategy #1 selection decision.

## 8. Decision

`M2_RESEARCH_PLATFORM_MVP = COMPLETED / PASS`.

ATS may enter:

`M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.

First M3 task:

`ATS2-M3-001 — Select Reference Strategy #1`

Work package:

`WBS-3.1`

Canonical next artifact:

`governance/program/REFERENCE_STRATEGY_1_SELECTION.md`

No Reference Strategy has been selected by this Exit Review. M3-001 must make that choice explicitly using available-data and execution-clarity criteria rather than treating the first convenient idea as already approved.

## 9. Transition-commit closure

This review records the M2 Exit decision based on the accepted platform implementation and Local CI evidence above.

The `ATS2-M2-011` repository transition itself remains subject to the normal exact-commit Local CI Gate. The phase transition is operationally closed only after `ATS_TASK_CHECK.bat` passes on the final commit containing this review, synchronized state/backlog/handoff and validator changes.
