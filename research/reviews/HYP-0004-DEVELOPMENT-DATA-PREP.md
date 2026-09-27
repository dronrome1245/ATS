# HYP-0004 Development Data Preparation

Task: `ATS2-RF-017`  
Hypothesis ID: `HYP-0004`  
Status: `PREPARATION_PROTOCOL_FROZEN`  
Date: 27 September 2026

## Purpose

RF-017 materializes a dedicated HYP-0004 development-data candidate from the already frozen HYP-0003 development dataset.

It may verify parent identity, filter the fixed EUR/USD rows, validate boundary BID/ASK coherence, assign the predeclared UTC buckets and count exact-next-hour geometry.

It computes **no absolute-return distribution, no relative-spread distribution, no bucket mean/median and neither primary HYP-0004 inequality**.

## Frozen parent identity

Parent dataset ID:

`DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001`

Parent local path:

`data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv`

Expected parent prepared-data SHA-256:

`8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2`

Parent source-bundle SHA-256:

`9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a`

RF-017 must fail closed if the local parent file is absent or its SHA-256 differs from the frozen identity. It must not substitute another vendor, an untracked CSV or a differently prepared parent.

Restoring/reproducing the parent under the existing HYP-0003 acquisition contract is a separate operational prerequisite if the frozen local parent file is unavailable.

## Frozen HYP-0004 subset rule

Only parent rows satisfying all three fixed identity fields are admitted:

- `currency = EUR`;
- `source_symbol = EURUSD`;
- `source_orientation = DIRECT`.

No performance value may influence row inclusion.

The parent interval remains:

`2003-08-03T21:00:00Z <= event_time <= 2021-08-31T23:00:00Z`

RF-017 does not request or inspect a later HYP-0004 outcome block.

## Boundary fields

Required parent fields for HYP-0004 preparation:

- `event_time`;
- `availability_time`;
- `currency`;
- `source_symbol`;
- `source_orientation`;
- `sequence`;
- `bid_open`;
- `ask_open`.

For every retained parent row:

- event time must be an exact UTC hourly boundary;
- parent-row availability time must equal `event_time + 1 hour`, preserving the completed-H1 lineage contract;
- BID/ASK must be finite and positive;
- `ask_open >= bid_open`;
- retained event times must be unique and strictly increasing;
- source identity must remain `EURUSD / DIRECT`.

No high/low/close field is used by RF-017.

For the derived open-only dataset, the frozen development proxy is:

- `availability_time = event_time`;
- `parent_row_availability_time = event_time + 1 hour`;
- availability mode: `H1_OPEN_PROXY_AT_EVENT_TIME`;
- exact tick-level timestamp of the first quote inside the H1 bucket remains unknown.

This is a declared development approximation for the bar-open proxy admitted by RF-016. It does not claim tick-exact boundary latency and must remain visible in RF-018 limitations.

## Frozen UTC bucket mapping

Bucket assignment depends only on `event_time.hour`:

- `CORE_ACTIVE`: 07–16 UTC;
- `TRANSITION`: 17–20 UTC;
- `OFF_HOURS`: 21–23 UTC and 00–06 UTC.

No DST conversion, local-session label or alternative-hour search is permitted.

RF-017 may count rows and exact-next-hour geometry by bucket and calendar year because those are data-shape facts, not HYP-0004 outcomes.

## Exact-next-hour geometry

A retained boundary at `t` is eligible for the future one-hour structural prototype only when a retained row exists at exactly `t + 1 hour` and both boundaries are expected Dukascopy FX market hours under the frozen market-hour calendar.

RF-017 must classify ineligible boundaries as:

- expected closed-market next hour;
- missing expected tradable next hour;
- right-edge dataset boundary.

No stale row, interpolation, forward fill or alternative lag may replace a missing exact next-hour row.

The geometry report must preserve the full denominator.

## Dedicated development dataset identity

Planned dataset ID:

`DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001`

Dataset version:

`1.0.0`

Local path:

`data/derived/HYP-0004-DEV-01-EURUSD-H1.csv`

The derived CSV contains only:

- `event_time`;
- derived open-proxy `availability_time`;
- `parent_row_availability_time`;
- deterministic derived `sequence`;
- original `parent_sequence`;
- `source_symbol`;
- `bid_open`;
- `ask_open`;
- `utc_bucket`.

It contains no future outcome column, midpoint return, relative spread or HYP-0004 decision field.

## Required local outputs

Canonical tool:

`tools/hyp0004_development_data.py`

Synthetic tests:

`tests/test_hyp0004_development_data.py`

Local machine result:

`reports/local_ci/HYP0004_DEVELOPMENT_DATA.json`

Shareable preparation summary:

`reports/local_ci/HYP0004_DEVELOPMENT_DATA_REPORT.txt`

The machine result must record at minimum:

- exact task commit;
- parent dataset ID and verified SHA-256;
- derived dataset ID/version;
- derived row count and SHA-256;
- first/last retained event time;
- duplicate/out-of-order/malformed/boundary-crossing counts;
- boundary availability mode and the fact that exact tick boundary time is unknown;
- eligible/ineligible exact-next-hour counts;
- total and eligible counts by UTC bucket;
- total and eligible counts by calendar year;
- `outcome_metrics_computed = false`;
- `primary_claim_evaluated = false`;
- information boundary `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

## Valid preparation decisions

`READY_FOR_DEVELOPMENT_DATA_FREEZE`

The frozen parent identity is verified, the EUR/USD subset is valid, paired boundary opens are coherent, and the data contain at least one exact-next-hour eligible observation in both `CORE_ACTIVE` and `OFF_HOURS`.

`INSUFFICIENT_DEVELOPMENT_DATA`

Preparation completes honestly but the frozen data contain insufficient eligible geometry to test both primary HYP-0004 buckets.

Parent hash mismatch, malformed rows, duplicate/out-of-order retained timestamps, invalid source identity or `ask_open < bid_open` are technical/data-integrity blockers, not a valid negative research decision.

## Information boundary

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

RF-017 may not calculate:

- `abs_next_1h_return`;
- `relative_spread`;
- any mean/median return or spread by bucket;
- either primary HYP-0004 inequality;
- trading P&L.

## Next step

After exact-main OWNER launcher PASS and review of the RF-017 local machine result:

`ATS2-RF-018 — HYP-0004 development data freeze`

RF-018 must freeze the derived dataset identity and quality/geometry facts before any HYP-0004 structural prototype is authorized.
