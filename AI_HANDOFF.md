# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: `REJECTED_AT_R3`.
- Strategy #2: `REJECTED_AT_R3`.
- Strategy #3 / HYP-0003: `REJECTED_AT_R3`.
- Strategy #4 / HYP-0005: active confirmatory line; RF-023 externally source-blocked.
- Strategy #5 / HYP-0006: active Data Feasibility preparation.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Current executable stage

`Research Factory → Strategy #5 → HYP-0006 → Data Feasibility preparation → ATS2-RF-027`

RF-027 checks official event identity/timing and granular quote-source geometry only.

It does **not** compute a HYP-0006 market outcome.

## Last completed task

RF-026 closed exact-main OWNER PASS on:

`5e0ff9e4481e5dc28c14a73adcf32433715973a3`

Canonical RF-026 artifact:

`research/reviews/HYP-0006-DATA-FEASIBILITY.md`

Decision:

`CONDITIONAL`

## HYP-0006 fixed research claim

Canonical Hypothesis:

`research/hypotheses/HYP-0006.md`

Frozen before outcome inspection:

- market: `FX_SPOT_OTC`;
- instrument: `EURUSD`;
- event class: scheduled U.S. CPI publication;
- previous-60m versus next-60m structural comparison;
- `PRE_RELEASE_ANCHOR` strictly before public release time;
- primary claim: `median(post_abs_60m_return) > median(pre_abs_60m_return)`;
- no directional return sign;
- no trading-P&L claim.

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

## RF-027 frozen preparation protocol

Protocol:

`research/reviews/HYP-0006-DATA-FEASIBILITY-PREP.md`

Tool:

`tools/hyp0006_data_feasibility.py`

Tests:

`tests/test_hyp0006_data_feasibility.py`

Development interval:

`2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z`

Evidence class:

`DEVELOPMENT / EXPLORATORY ONLY`

Event denominator:

all official archived BLS CPI HTML releases in the frozen interval.

Primary event timestamp:

official CPI archive embargo/publication header, with annual BLS schedule cross-check.

Same-time BLS policy:

`FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION`

Granular quote source:

`DUKASCOPY_HOURLY_TICK_BI5`

RF-027 requests only the bounded hourly tick objects required to measure timestamp geometry around
`t-60m`, strictly before `t`, and `t+60m`.

The geometry output contains timestamps/distances and source hashes only; no BID/ASK price, midpoint,
return or P&L field is allowed.

## RF-027 valid preparation decisions

- `READY_FOR_DATA_FEASIBILITY_FREEZE`;
- `UNRESOLVED_OFFICIAL_EVENT_TIMES`;
- `OFFICIAL_TIME_CROSSCHECK_MISMATCH`;
- `INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY`.

These are Data Feasibility outcomes, not HYP-0006 market outcomes.

Network/decompression/source-protocol failure is a technical blocker and is not a negative
Hypothesis result.

## HYP-0005 boundary remains intact

RF-023 remains separately open.

Frozen HYP-0005 periods/provider/rules/decision criteria remain unchanged.

Information boundary:

`NO_CONFIRMATORY_OUTCOME_COMPUTED`

RF-027 must retain:

`protected_hyp0005_source_requests = 0`

## Next gate

Current task:

`ATS2-RF-027 — HYP-0006 Data Feasibility preparation`

OWNER must first provide exact-head preflight PASS for the agent branch. GPT then merges it.

After exact-main RF-027 runs the preparation successfully, OWNER sends:

- `CURRENT_TASK_REPORT.txt`;
- `HYP0006_DATA_FEASIBILITY_PREP.json`.

Only then can ATS decide whether RF-028 may freeze the exact dataset/tolerances.

Next task after an eligible RF-027 preparation result:

`ATS2-RF-028 — HYP-0006 pre-reveal data/tolerance freeze`
