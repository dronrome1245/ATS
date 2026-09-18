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

`ATS2-M2-008 — Standard analytics/report`.

Primary artifact:

`src/ats/analytics/standard.py`

Implemented boundary:

- analytics consumes deterministic replay metadata/counts plus explicit economic inputs;
- `EffectSeries` requires declared semantics, unit and finite ordered increments;
- gross effect is separate from modeled cost components/aggregate and net effect;
- net effect exists only when an applicable modeled cost total has the same unit as gross effect;
- all-not-applicable costs do not become a hidden numeric zero;
- effect distribution exposes count/mean/min/max when meaningful;
- path output exposes absolute cumulative max drawdown in the declared effect unit;
- Strategy decisions are counted as decisions and are not inferred to be trades;
- trade/event/opportunity count must be declared explicitly or marked `NOT_APPLICABLE`;
- machine-readable output follows the M1 `result.json` section vocabulary where applicable;
- deterministic Markdown rendering is available for a minimum human-readable report;
- no Sharpe, return percentage, win rate, capital metric or market semantics are fabricated.

Tests:

`tests/test_standard_analytics.py`

The suite uses synthetic non-market effect units and does not create research evidence.

## M2-008 closure check

Windows OWNER workflow:

`ATS_TASK_CHECK.bat`

Current `tools/current_task_check.py` is configured for:

`ATS2-M2-008 — Standard analytics/report`

It runs:

1. `tests/test_standard_analytics.py`;
2. repository validator;
3. full ATS Local CI.

Shareable report:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

Reusable Local CI failure lessons and preventive rules:

`governance/program/LOCAL_CI_TROUBLESHOOTING.md`

Before changing code after a launcher FAIL, classify the first failing stage. Raw runtime reports remain local and are not committed.

M2-008 is finally closed only after PASS on the exact final HEAD.

## Current ready task after M2-008 PASS

`ATS2-M2-009 — Manifest-driven experiment runner`

Canonical next artifact:

`src/ats/runner/experiment.py`

Goal: connect frozen Experiment context to the existing deterministic loader → replay → costs → analytics path and produce machine-readable run output without rewriting preregistration.

M2-009 must not add broker/live execution, portfolio logic or Reference Strategy #1.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/LOCAL_CI_TROUBLESHOOTING.md` when diagnosing a launcher/Local CI failure.
6. `governance/program/REFERENCE_CONSUMER_PROFILE.md`.
7. `governance/methodology/EXPERIMENT_REGISTRATION.md`.
8. `governance/methodology/templates/experiment/manifest.yaml`.
9. `governance/methodology/templates/experiment/result.json`.
10. `src/ats/replay/engine.py`.
11. `src/ats/costs/interface.py`.
12. `src/ats/analytics/standard.py`.
13. `tests/test_standard_analytics.py`.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last implemented task: `ATS2-M2-008`.
- Closure checker: `ATS2-M2-008`.
- Next task after PASS: `ATS2-M2-009`.
- Next artifact: `src/ats/runner/experiment.py`.
- Reference Strategy #1 selection allowed now? — no.
- Pipeline counts remain zero? — yes.
