# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: `REJECTED_AT_R3`.
- Strategy #2: `REJECTED_AT_R3`.
- Strategy #3 / HYP-0003: `REJECTED_AT_R3`.
- Strategy #4 / HYP-0005: active confirmatory line; RF-023 is externally source-blocked.
- Strategy #5 / HYP-0006: parallel lineage-registration task RF-025 is executable.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Current executable stage

`Research Factory → Strategy #5 → IDEA-0005 / HYP-0006 formation → ATS2-RF-025`

RF-025 is a research-definition/governance task. It does not calculate a HYP-0006 market outcome.

## Canonical last completed artifact

`research/hypotheses/HYP-0005.md`

## Verified RF-022 closure

OWNER `ATS_TASK_CHECK.bat` PASS was confirmed on exact main commit:

`136b62b52922abc1556396377c6cd6fca88fba75`

That closure remains the last completed task. RF-025 is staged in an `agent/*` branch and is not complete before exact-head preflight, merge and exact-main task check.

## Strategy #4 / HYP-0005 remains separate

Open task:

`ATS2-RF-023 — HYP-0005 confirmatory Data Feasibility preparation`

External classification:

`SOURCE_AVAILABILITY_BLOCKER / NO_CONFIRMATORY_OUTCOME_COMPUTED`

OWNER diagnostic on 28 September 2026 showed:

- September 2026 Jetta EUR/USD BID and ASK each returned HTTP 400 with `From time is too late`;
- August 2026 Jetta BID and ASK controls each returned HTTP 200;
- September BI5 requests returned HTTP 503 during the diagnostic;
- hypothesis outcome fields requested: `0`.

Do not change the HYP-0005 frozen unseen segments, provider family, hypothesis rules or decision criteria.

Frozen unseen segments:

- `LEFT_UNSEEN = [2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)`;
- `RIGHT_UNSEEN = [2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)`.

Consumed project interval excluded from HYP-0005 confirmatory evidence:

`[2003-08-03T21:00:00Z, 2026-09-01T00:00:00Z)`.

HYP-0005 frozen preparation artifacts remain:

- `research/hypotheses/HYP-0005.md`;
- `research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md`;
- `tools/hyp0005_data_feasibility.py`;
- `tests/test_hyp0005_data_feasibility.py`.

RF-025 must not use either HYP-0005 unseen segment for Strategy #5 data selection, tuning or outcome calculation.

## RF-025 lineage decision

Governance permits parallel cheap research work while an unrelated external dependency blocks RF-023.

The new line is not another Hypothesis inside IDEA-0004 because the proposed mechanism changes materially:

- IDEA-0004 / HYP-0004 / HYP-0005: recurring fixed-UTC intraday participation/liquidity structure;
- IDEA-0005 / HYP-0006: scheduled macroeconomic information arrival and immediate FX price discovery.

The source concept is not invented from an observed HYP-0005 result. It comes from the already retained research family:

`S4-FAM-02 — MACROECONOMIC_ANNOUNCEMENT_RESPONSE`

recorded in `governance/program/STRATEGY_4_IDEA_SOURCING.md` and retained for future sourcing by `governance/program/STRATEGY_4_FAMILY_SELECTION.md`.

Canonical RF-025 artifacts:

- `research/ideas/IDEA-0005.md`;
- `research/hypotheses/HYP-0006.md`.

Multiple-research accounting records two new Material Research Attempts:

1. `IDEA-0005`;
2. `HYP-0006`.

## HYP-0006 frozen claim at formation

HYP-0006 fixes:

- market: `FX_SPOT_OTC`;
- instrument: `EURUSD`;
- event class: scheduled U.S. CPI publication;
- pre-event horizon: previous 60 minutes;
- post-event horizon: next 60 minutes;
- primary ordering: `median(post_abs_60m_return) > median(pre_abs_60m_return)`;
- no directional EUR/USD sign;
- no trading P&L or profitability claim;
- exact event-calendar and quote providers remain Data Feasibility questions.

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

Any quote period already inspected elsewhere in ATS must be classified as development/exploratory for HYP-0006 rather than independent evidence.

## Current task and next task

Current executable task:

`ATS2-RF-025 — Parallel Strategy #5 Idea Intake + HYP-0006 formation`

After RF-025 exact-main PASS:

`ATS2-RF-026 — HYP-0006 Data Feasibility`

must establish event-publication timing, granular BID/ASK source semantics, development coverage, event-cluster handling, missing-data rules and overlap classification before any HYP-0006 outcome.

RF-023 remains separately open and may resume later under its unchanged frozen HYP-0005 contract.
