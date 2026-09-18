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

`ATS2-M2-007 — Cost model interface`.

Primary artifact:

`src/ats/costs/interface.py`

Implemented boundary:

- `CostModelConfig` declares a complete ordered component set;
- applicable components require explicit parameters and receive no numeric defaults;
- a genuinely non-applicable component is represented explicitly with a reason;
- `CostInput` is deterministic and independent of Strategy logic;
- `CostComponentResult / CostResult` contain modeled cost contributions only;
- every applicable result carries an explicit unit;
- canonical JSON serialization rejects non-finite values;
- `apply_cost_model` requires exact input identity, configured component order and applicability;
- the model cannot silently omit a configured component;
- no analytics, gross/net aggregation, broker or live execution behavior is introduced.

Tests:

`tests/test_cost_interface.py`

The suite uses synthetic non-market fixture units and explicit fee/spread-proxy assumptions plus an explicit non-applicable slippage proxy. These are software fixtures only and are not research evidence.

## M2-007 closure check

Windows OWNER workflow:

`ATS_TASK_CHECK.bat`

Current `tools/current_task_check.py` is configured for:

`ATS2-M2-007 — Cost model interface`

It runs:

1. `tests/test_cost_interface.py`;
2. repository validator;
3. full ATS Local CI.

Shareable report:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

Reusable Local CI failure lessons and preventive rules:

`governance/program/LOCAL_CI_TROUBLESHOOTING.md`

Before changing code after a launcher FAIL, classify the first failing stage. Raw runtime reports remain local and are not committed.

M2-007 is finally closed only after PASS on the exact final HEAD.

## Current ready task after M2-007 PASS

`ATS2-M2-008 — Standard analytics/report`

Canonical next artifact:

`src/ats/analytics/standard.py`

Goal: define deterministic baseline run analytics/results while preserving separate gross effect, modeled costs and net effect and marking inapplicable metrics explicitly.

M2-008 must not add broker/live execution, portfolio logic or Reference Strategy #1.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/LOCAL_CI_TROUBLESHOOTING.md` when diagnosing a launcher/Local CI failure.
6. `governance/program/REFERENCE_CONSUMER_PROFILE.md`.
7. `src/ats/data/loader.py`.
8. `src/ats/strategy/interface.py`.
9. `src/ats/replay/engine.py`.
10. `src/ats/costs/interface.py`.
11. `tests/test_cost_interface.py`.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last implemented task: `ATS2-M2-007`.
- Closure checker: `ATS2-M2-007`.
- Next task after PASS: `ATS2-M2-008`.
- Next artifact: `src/ats/analytics/standard.py`.
- Reference Strategy #1 selection allowed now? — no.
- Pipeline counts remain zero? — yes.
