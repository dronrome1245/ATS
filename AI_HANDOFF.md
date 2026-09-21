# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- M2: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Live/demo/allocation/scaling remain disallowed.

## Last implemented task

`ATS2-M3-001 — Select Reference Strategy #1`

Canonical artifact:

`governance/program/REFERENCE_STRATEGY_1_SELECTION.md`

Selected class:

`SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT`

Meaning:

- one instrument;
- 1H bars;
- long/flat first reference implementation;
- trend/breakout family;
- decisions only from completed 1H-bar information;
- no action before the next information-available execution point;
- position may span multiple 1H bars or calendar days until an explicit exit signal;
- no shorting, borrow, leverage or portfolio layer required for the first research line.

No instrument, venue, data vendor, numeric parameter, cost value or capital/risk limit is selected yet.

The class was selected for platform fit, data-path feasibility, clear timing semantics and low infrastructure burden. Research literature is provenance only and is not treated as proof of profitability.

## M3-001 closure check

Current `tools/current_task_check.py` is configured for:

`ATS2-M3-001 — Select Reference Strategy #1`

Run:

`ATS_TASK_CHECK.bat`

Shareable report:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

## Current ready task after PASS

`ATS2-M3-002 — Idea & rationale`

Work package:

`WBS-3.2`

Immediate next artifact:

`research/ideas/IDEA-0001.md`

Expected M3-002 deliverables:

- `research/ideas/IDEA-0001.md`;
- `research/hypotheses/HYP-0001.md`.

The Idea/Hypothesis must be created before Data Feasibility and before any parameter search.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/program/REFERENCE_STRATEGY_1_SELECTION.md`.
5. `governance/methodology/IDEA_INTAKE_PROCESS.md`.
6. `governance/methodology/HYPOTHESIS_MODEL.md`.
7. `governance/methodology/DATA_FEASIBILITY_REVIEW.md`.
8. `governance/backlog/PROGRAM_BACKLOG_V2.md`.

## Recovery check

- Current milestone: `M3_REFERENCE_STRATEGY_1`.
- Last implemented task: `ATS2-M3-001`.
- Closure checker: `ATS2-M3-001`.
- Selected class: `SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT`.
- Current ready task after PASS: `ATS2-M3-002`.
- Current WBS after PASS: `WBS-3.2`.
- Next artifact: `research/ideas/IDEA-0001.md`.
- Ideas registered now? — no.
- Candidate/Strategy/Experiment created? — no.
- Live/demo/allocation/scaling allowed? — no.
