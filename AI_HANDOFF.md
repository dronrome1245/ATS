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

`ATS2-M2-006 — Deterministic backtest/replay`.

Primary artifact:

`src/ats/replay/engine.py`

Implemented boundary:

- `run_replay` consumes `LoadedDataset + ResearchRunContext + ResearchStrategy`;
- loader records become ordered `ResearchObservation` values;
- strategy initialization occurs once per replay;
- one `on_observation` transition occurs per loaded record;
- immutable `ReplayFrame` captures observation, state-before/state-after, decisions and diagnostics;
- immutable `ReplayResult` binds dataset identity/version/hash/context and ordered trace;
- availability time may not regress in the M2 single-stream replay;
- a decision may not claim a time before the current observation becomes available;
- engine injects no wall clock, network, broker, cost model or analytics.

Tests:

`tests/test_replay_engine.py`

The suite includes a vertical synthetic chain:

`Dataset Manifest → loader → Strategy interface → replay`

These are software fixtures only and are not research evidence.

## M2-006 closure check

Windows OWNER workflow:

`ATS_TASK_CHECK.bat`

Current `tools/current_task_check.py` is configured for:

`ATS2-M2-006 — Deterministic backtest/replay`

It runs:

1. `tests/test_replay_engine.py`;
2. repository validator;
3. full ATS Local CI.

Shareable report:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

M2-006 is finally closed only after PASS on the exact final HEAD.

## Current ready task after M2-006 PASS

`ATS2-M2-007 — Cost model interface`

Canonical next artifact:

`src/ats/costs/interface.py`

Goal: define explicit deterministic cost assumptions/components outside Strategy logic and keep modeled costs separate from gross effects/results.

M2-007 must not add analytics, broker/live execution or Reference Strategy #1.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/REFERENCE_CONSUMER_PROFILE.md`.
6. `src/ats/data/loader.py`.
7. `src/ats/strategy/interface.py`.
8. `src/ats/replay/engine.py`.
9. `tests/test_replay_engine.py`.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last implemented task: `ATS2-M2-006`.
- Closure checker: `ATS2-M2-006`.
- Next task after PASS: `ATS2-M2-007`.
- Next artifact: `src/ats/costs/interface.py`.
- Reference Strategy #1 selection allowed now? — no.
- Pipeline counts remain zero? — yes.
