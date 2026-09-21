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

## Reference Strategy #1

Selected class:

`SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT`

Canonical selection:

`governance/program/REFERENCE_STRATEGY_1_SELECTION.md`

Decision interval is 1H. Holding period is not fixed; a position may remain open across multiple bars or days until a later specified exit signal.

## Current research entity

`IDEA-0001 — BTCUSDT 1H Long/Flat Trend-Breakout`

Artifact:

`research/ideas/IDEA-0001.md`

Status:

`SCREENING`

Idea context:

- `CRYPTO_SPOT`;
- proposed instrument `BTCUSDT` on Binance spot;
- completed 1H bars only;
- earliest action after signal information becomes available;
- no end-of-day flat requirement;
- no numeric lookback/threshold/stop/sizing/fixed holding period selected.

Idea proposition: a preregistered upward trend/breakout state on completed BTCUSDT 1H bars may be followed by more positive subsequent movement than a declared baseline. This remains unproven.

Current Binance public information confirms BTCUSDT is a spot-trading symbol and public market-data access exists. Binance Public Data documents 1h kline archives and checksums. These facts support data-path plausibility only.

## Current task

`ATS2-M3-002 — Idea & rationale` — `IN_PROGRESS`.

Immediate next artifact:

`research/hypotheses/HYP-0001.md`

M3-002 is not complete until HYP-0001 is materialized.

## Closure checker

`tools/current_task_check.py` is configured for M3-002 completion and requires both:

- `research/ideas/IDEA-0001.md`;
- `research/hypotheses/HYP-0001.md`.

Until HYP-0001 exists, do not interpret a task-check failure for the missing artifact as a code defect.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `research/ideas/IDEA-0001.md`.
5. `governance/methodology/HYPOTHESIS_MODEL.md`.
6. `governance/methodology/templates/HYPOTHESIS_TEMPLATE.md`.
7. `governance/methodology/DATA_FEASIBILITY_REVIEW.md`.
8. `governance/backlog/PROGRAM_BACKLOG_V2.md`.

## Recovery check

- Current milestone: `M3_REFERENCE_STRATEGY_1`.
- Last completed task: `ATS2-M3-001`.
- Current task: `ATS2-M3-002`.
- Current WBS: `WBS-3.2`.
- Idea registered: `IDEA-0001`.
- Idea status: `SCREENING`.
- Ideas registered count: 1.
- Next artifact: `research/hypotheses/HYP-0001.md`.
- Candidate/Strategy/Experiment created? — no.
- Live/demo/allocation/scaling allowed? — no.
