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

`ATS2-M2-010 — Research platform tests`.

Primary artifact:

`tests/test_research_platform.py`

Committed expected result:

`tests/fixtures/platform/reference_consumer_expected.json`

Implemented acceptance boundary:

- canonical Dataset Manifest and synthetic CSV are loaded with integrity verification;
- one deterministic Strategy fixture consumes the ordered observations;
- replay preserves ordered decisions and diagnostics;
- explicit fee cost is modeled separately and slippage remains explicitly `NOT_APPLICABLE`;
- standard analytics preserves gross/cost/net separation and baseline path metrics;
- committed expected result freezes dataset identity/hash, context, decisions, diagnostics, costs and analytics;
- two runs from the same frozen inputs are required to be exactly equal under canonical JSON;
- acceptance fixture contains no Idea/Hypothesis/Candidate/Strategy/Experiment identity;
- Experiment Registry remains empty;
- M2-010 closure package also reruns `tests/test_experiment_runner.py` so manifest-driven runner behavior remains part of platform acceptance.

The acceptance fixture is software correctness evidence only and not research/trading evidence.

## M2-010 closure check

Windows OWNER workflow:

`ATS_TASK_CHECK.bat`

Current `tools/current_task_check.py` is configured for:

`ATS2-M2-010 — Research platform tests`

It runs:

1. `tests/test_research_platform.py` plus `tests/test_experiment_runner.py`;
2. repository validator;
3. full ATS Local CI.

Shareable report:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

Reusable Local CI failure lessons:

`governance/program/LOCAL_CI_TROUBLESHOOTING.md`

M2-010 is finally closed only after PASS on the exact final HEAD.

## Current ready task after M2-010 PASS

`ATS2-M2-011 — M2 Exit`

Canonical next artifact:

`governance/program/M2_EXIT_REVIEW.md`

Goal: perform a formal milestone exit review against completed M2 artifacts, Reference Consumer Profile acceptance criteria and exact Local CI evidence before changing the program phase.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/REFERENCE_CONSUMER_PROFILE.md`.
6. `governance/program/PROGRAM_WBS_V2.md`.
7. `tests/test_research_platform.py`.
8. `tests/fixtures/platform/reference_consumer_expected.json`.
9. `tests/test_experiment_runner.py`.
10. `governance/program/LOCAL_CI_TROUBLESHOOTING.md` when diagnosing Local CI.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last implemented task: `ATS2-M2-010`.
- Closure checker: `ATS2-M2-010`.
- Next task after PASS: `ATS2-M2-011`.
- Next artifact: `governance/program/M2_EXIT_REVIEW.md`.
- Reference Strategy #1 selection allowed now? — no; only after explicit M2 Exit transition to M3.
- Pipeline counts remain zero? — yes.
