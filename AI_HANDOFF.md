# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- M0/M1/M2: `COMPLETED / PASS`.
- Reference class: `SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT`.
- Instrument: `EURUSD` / EUR/USD spot FX.
- Live/demo/allocation/scaling remain disallowed.

## Research lineage

Idea:

`research/ideas/IDEA-0001.md`

- ID: `IDEA-0001`
- Status: `SCREENING`
- Context: EUR/USD, 1H, long/flat.

Hypothesis:

`research/hypotheses/HYP-0001.md`

- ID: `HYP-0001`
- Parent: `IDEA-0001`
- Status: `READY_FOR_DATA_FEASIBILITY`

## Frozen HYP-0001 claim

Signal:

A fully completed EUR/USD 1H bar has BID close strictly above the highest BID high of the preceding 24 fully completed eligible 1H bars.

Execution/effect measurement:

- signal uses completed information only;
- entry measurement begins at the next eligible ASK open;
- primary horizon is 24 eligible 1H bars;
- primary exit/valuation is the BID open 24 eligible bars after entry.

Expected primary ordering:

`mean(signal executable 24-bar return) > 0`

and:

`mean(signal executable 24-bar return) > mean(unconditional executable 24-bar return)`

The 24-bar horizon is a research measurement horizon, not yet the final strategy holding rule.

No lookback/horizon optimization is allowed after observing the result. A material reformulation after Data Feasibility requires a new Hypothesis ID.

## Closure check

Current checker:

`ATS2-M3-002 — Idea & rationale`

Run:

`ATS_TASK_CHECK.bat`

It requires both Idea and Hypothesis, repository validator and full Local CI.

## Next task after PASS

`ATS2-M3-003 — Data feasibility`

Work package:

`WBS-3.3`

Next artifact:

`research/reviews/HYP-0001-DATA_FEASIBILITY.md`

The review must establish actual BID/ASK source coverage, timestamp/session semantics, source identity, gaps, licensing/access and cost-input limitations before any Cheap Prototype.

## Recovery check

- Last implemented task: `ATS2-M3-002`.
- Current closure checker: `ATS2-M3-002`.
- Next ready task after PASS: `ATS2-M3-003`.
- Current WBS after PASS: `WBS-3.3`.
- Idea ID: `IDEA-0001`.
- Hypothesis ID: `HYP-0001`.
- Candidate/Strategy/Experiment created? — no.
- Live/demo/allocation/scaling allowed? — no.
