# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: `REJECTED_AT_R3`.
- Strategy #2: `REJECTED_AT_R3`.
- Strategy #3 / HYP-0003: `REJECTED_AT_R3`.
- Strategy #4 / HYP-0005: active confirmatory line; RF-023 remains externally source-blocked.
- Strategy #5 / HYP-0006: active Data Feasibility preparation.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Current executable stage

`Research Factory → Strategy #5 → HYP-0006 → RF-027 Data Feasibility preparation`

RF-027 verifies only official CPI event identity/timing and EUR/USD tick timestamp geometry.

It does **not** compute a HYP-0006 market outcome.

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

## HYP-0006 fixed research claim

Canonical Hypothesis:

`research/hypotheses/HYP-0006.md`

Frozen before outcome inspection:

- market: `FX_SPOT_OTC`;
- instrument: `EURUSD`;
- event class: scheduled U.S. CPI publication;
- pre-event horizon: previous 60 minutes;
- post-event horizon: next 60 minutes;
- `PRE_RELEASE_ANCHOR` strictly before public release;
- primary structural claim:
  `median(post_abs_60m_return) > median(pre_abs_60m_return)`;
- no directional return sign;
- no trading-P&L claim.

## RF-026 closure

Canonical completed artifact:

`research/reviews/HYP-0006-DATA-FEASIBILITY.md`

Current next artifact:

`research/reviews/HYP-0006-DATA-FEASIBILITY-PREP.md`

RF-026 closed exact-main PASS on:

`5e0ff9e4481e5dc28c14a73adcf32433715973a3`

Data Feasibility decision:

`CONDITIONAL`

Development interval:

`2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z`

Evidence class:

`DEVELOPMENT / EXPLORATORY ONLY`

## Why RF-027 source architecture changed

Two exact-main RF-027 attempts passed Local CI and then failed before event acquisition because live
BLS HTTP access returned 403:

- `a4c6331949e9c71fc68eb1baa870d20a03518d48`;
- `2ce019bb51b0e45e900c0555ed44be5a3433e23a`.

Both are:

`TECHNICAL_SOURCE_ACCESS_FAILURE`

Neither computed a HYP-0006 outcome.

ATS therefore no longer treats live BLS availability as a normal runtime dependency.

## Current RF-027 architecture

Protocol:

`research/reviews/HYP-0006-DATA-FEASIBILITY-PREP.md`

Snapshot intake instructions:

`research/reviews/HYP-0006-BLS-SNAPSHOT-INTAKE.md`

Snapshot manifest:

`data/reference/HYP-0006-BLS-SCHEDULE-SNAPSHOT-MANIFEST.csv`

Required official BLS annual schedule snapshots:

`2003..2021`

Local raw path:

`data/raw/bls/hyp0006/schedules/YYYY.html`

Normal RF-027 live BLS network mode:

`PROHIBITED`

Once the 19 official snapshots exist locally, the runner creates:

`data/derived/HYP-0006-BLS-CPI-CALENDAR-2003-2021.csv`

Source identity:

`BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS`

Timestamp semantics:

`BLS_ANNUAL_SCHEDULE_US_EASTERN`

The calendar is hashed before any EUR/USD outcome is computed.

## Current RF-027 source status

The one-time official BLS snapshot intake is complete locally.

Canonical local bundle:

- years: `2003..2021`;
- count: `19`;
- path: `data/raw/bls/hyp0006/schedules/YYYY.html`;
- content preserved during filename normalization.

The latest exact-main RF-027 run passed governance and full Local CI, then:

- produced the local BLS CPI calendar;
- found `217` CPI events;
- produced BLS calendar SHA-256
  `646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9`;
- stopped on Dukascopy tick acquisition for
  `2004-03-17T12:00:00Z`;
- last proven source error: `HTTP 503`;
- created no geometry CSV and no final RF-027 result JSON.

This is:

`TECHNICAL_SOURCE_ACCESS_FAILURE`

It is not a HYP-0006 result.

Repository-wide source discipline:

`FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF`

After the first proven external HTTP/network/access failure, automatic retries, alternate endpoints and fallbacks stop immediately. A new external attempt requires explicit OWNER authorization after that first failure is reported.

## EUR/USD source geometry

Quote source remains:

`DUKASCOPY_HOURLY_TICK_BI5`

RF-027 requests only bounded tick objects around each frozen CPI timestamp and calculates
timestamp-distance geometry only.

Required invariant:

`protected_hyp0005_source_requests = 0`

RF-027 may not write CPI-event return distributions, the HYP-0006 primary inequality or P&L.

## HYP-0005 boundary

HYP-0005 remains separate and unchanged.

Information boundary:

`NO_CONFIRMATORY_OUTCOME_COMPUTED`

## Next gate

Current corrective Git branch:

`agent/rf027-dukascopy-source-blocker`

Current task remains:

`ATS2-RF-027`

Next gate: exact-head preflight of governance synchronization for the Dukascopy source blocker.

After exact-head PASS, GPT merges the correction.

Do **not** immediately rerun the full RF-027 launcher. One controlled retry of the same frozen RF-027
is allowed only after separate evidence that the Dukascopy source has recovered and OWNER authorizes
that retry.

If HTTP 503 repeats persistently, stop retries and open a Data Feasibility source-architecture
decision that preserves Dukascopy/tick semantics. Do not substitute a third-party event or quote
source automatically.

Only after exact-main RF-027 preparation PASS:

`ATS2-RF-028 — HYP-0006 pre-reveal data/tolerance freeze`

will freeze the exact BLS calendar SHA-256, source snapshot bundle SHA-256, eligible-event rules and
numeric anchor tolerances before any market reveal.
