# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: `REJECTED_AT_R3`.
- Strategy #2: `REJECTED_AT_R3`.
- Strategy #3 / HYP-0003: `REJECTED_AT_R3`.
- Strategy #4 / HYP-0005: active confirmatory line; RF-023 externally source-blocked.
- Strategy #5 / HYP-0006: active parallel line at Data Feasibility.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Current executable stage

`Research Factory → Strategy #5 → HYP-0006 → Data Feasibility → ATS2-RF-026`

This stage verifies source/timestamp/coverage feasibility only.

It does **not** compute a HYP-0006 market outcome.

## RF-025 exact-main closure

RF-025 closed only after OWNER exact-main `ATS_TASK_CHECK.bat` PASS on:

`9b0a6c8898a7ebf9b03167a871ad02af96ca2807`

The exact-main report confirmed:

- branch `main`;
- HYP-0005 frozen artifacts unchanged;
- no HYP-0006 Data Feasibility runner/dataset/outcome artifact existed during RF-025;
- repository validator PASS;
- pinned Ruff lint PASS;
- pinned Ruff format PASS;
- `194 passed`;
- environment fingerprint PASS;
- `ATS CURRENT TASK CHECK: PASS`;
- `ATS TASK LAUNCHER: PASS`.

## HYP-0006 fixed research claim

Canonical Hypothesis:

`research/hypotheses/HYP-0006.md`

Already frozen before outcome inspection:

- market: `FX_SPOT_OTC`;
- instrument: `EURUSD`;
- event class: scheduled U.S. CPI publication;
- pre-event horizon: previous 60 minutes;
- post-event horizon: next 60 minutes;
- common event boundary: strictly pre-release eligible synchronized quote;
- primary claim: `median(post_abs_60m_return) > median(pre_abs_60m_return)`;
- no directional return sign;
- no trading-P&L claim.

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

## RF-026 Data Feasibility decision

Canonical review:

`research/reviews/HYP-0006-DATA-FEASIBILITY.md`

Decision:

`CONDITIONAL`

Verified source classes:

- U.S. Bureau of Labor Statistics official release schedules and CPI archived releases for event identity/publication time;
- Dukascopy historical EUR/USD tick data as the granular quote-source candidate.

Frozen development-source interval:

`2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z`

Evidence classification:

`DEVELOPMENT / EXPLORATORY ONLY`

Same-time BLS event policy:

`FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION`

H1 data are insufficient for HYP-0006 event anchors; later preparation requires tick or sufficiently fine BID/ASK observations.

Prototype authorization:

`NOT_YET_AUTHORIZED`

## What remains open inside Data Feasibility

Before any HYP-0006 outcome calculation, ATS still must machine-verify and freeze:

- the complete BLS CPI event denominator in the development interval;
- official release-time conversion to UTC, including historical U.S. DST rules;
- schedule/archive consistency;
- exact Dukascopy EUR/USD tick acquisition path;
- granular coverage around every candidate event;
- coherent BID/ASK semantics;
- numeric PRE_60 / PRE_RELEASE / POST_60 anchor tolerances;
- whole-period missing/quality geometry;
- source-object and prepared-data hashes.

These are Data Feasibility facts, not hypothesis outcome metrics.

## HYP-0005 boundary remains intact

RF-023 remains separately open under Strategy #4.

Do not change HYP-0005:

- frozen unseen periods;
- provider family;
- hypothesis rules;
- decision criteria.

Information boundary:

`NO_CONFIRMATORY_OUTCOME_COMPUTED`

HYP-0006 development may not use either HYP-0005 frozen unseen segment.

## Next task

Current:

`ATS2-RF-026 — HYP-0006 Data Feasibility`

After RF-026 exact-main PASS:

`ATS2-RF-027 — HYP-0006 Data Feasibility preparation`

RF-027 may verify event/quote identity, timing, coverage, hashes and anchor geometry only.

It must retain:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`
