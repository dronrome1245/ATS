# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- Real trading, demo, allocation and scaling remain disallowed.

## Last implemented work package

`ATS2-M2-005 — Minimal Strategy research interface`.

Primary artifact:

`src/ats/strategy/interface.py`

Implemented boundary:

- immutable `ResearchRunContext`;
- immutable `ResearchObservation` with event/availability time;
- `observation_from_loaded_record` bridge from M2-004;
- broker-neutral `ResearchDecision` with canonical JSON serialization;
- `ResearchDiagnostic`;
- generic `StrategyStep[state]`;
- `ResearchStrategy[state]` protocol with `initial_state` and `on_observation`;
- finite JSON-scalar payload constraint for the M2 baseline.

The interface does not inject wall clock, network, broker, account, allocation or live-risk objects.

Synthetic conformance tests:

`tests/test_strategy_interface.py`

The fixture strategy is software-only and is not an ATS research entity or evidence.

## M2-005 closure check

Windows OWNER workflow:

`ATS_TASK_CHECK.bat`

Current `tools/current_task_check.py` is configured for:

`ATS2-M2-005 — Minimal Strategy research interface`

It runs:

1. `tests/test_strategy_interface.py`;
2. repository validator;
3. full ATS Local CI.

Shareable report:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

M2-005 is finally closed only after PASS on the exact final HEAD.

## Current ready task after M2-005 PASS

`ATS2-M2-006 — Deterministic backtest/replay`

Canonical next artifact:

`src/ats/replay/engine.py`

Goal: consume a deterministic `LoadedDataset`, `ResearchRunContext` and `ResearchStrategy`, process observations in declared order, and produce a reproducible state/decision/diagnostic trace.

M2-006 must not add cost modelling, analytics, broker/live execution or Reference Strategy #1.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/REFERENCE_CONSUMER_PROFILE.md`.
6. `src/ats/data/loader.py`.
7. `src/ats/strategy/interface.py`.
8. `tests/test_strategy_interface.py`.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last implemented task: `ATS2-M2-005`.
- Closure checker: `ATS2-M2-005`.
- Next task after PASS: `ATS2-M2-006`.
- Next artifact: `src/ats/replay/engine.py`.
- Reference Strategy #1 selection allowed now? — no.
- Pipeline counts remain zero? — yes.
