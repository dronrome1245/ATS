# HYP-0006 Data Feasibility Preparation

Task: `ATS2-RF-027`  
Hypothesis ID: `HYP-0006`  
Status: `PREPARATION_PROTOCOL_FROZEN_OFFLINE_BLS_SNAPSHOTS`  
Date: 29 September 2026

## Purpose

RF-027 machine-verifies the official U.S. CPI event denominator and granular EUR/USD BID/ASK
timestamp geometry required by HYP-0006.

RF-027 computes **no HYP-0006 return, pre/post distribution, primary inequality or trading P&L**.

## Why the source architecture changed

Two exact-main RF-027 attempts passed Local CI and then failed before event acquisition because the
official BLS website returned HTTP 403 to the automated client:

- `a4c6331949e9c71fc68eb1baa870d20a03518d48`;
- `2ce019bb51b0e45e900c0555ed44be5a3433e23a`.

Both failures are classified:

`TECHNICAL_SOURCE_ACCESS_FAILURE`

They are not HYP-0006 negative results.

The repeated access failure proves that normal RF-027 execution must not depend on live BLS HTTP
availability.

## Frozen development interval

Only CPI events with official BLS scheduled release timestamp inside:

`2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z`

may enter this preparation.

Evidence classification:

`DEVELOPMENT / EXPLORATORY ONLY`

## Canonical BLS source architecture

The official source class remains the U.S. Bureau of Labor Statistics.

Live BLS network access during normal RF-027 runtime is:

`PROHIBITED`

Canonical source intake is a one-time set of official annual BLS schedule snapshots.

Manifest:

`data/reference/HYP-0006-BLS-SCHEDULE-SNAPSHOT-MANIFEST.csv`

Required years:

`2003..2021`

Required raw snapshot location:

`data/raw/bls/hyp0006/schedules/YYYY.html`

OWNER intake instructions:

`research/reviews/HYP-0006-BLS-SNAPSHOT-INTAKE.md`

Raw snapshots are not committed to Git.

For every snapshot RF-027 records:

- official source URL;
- local raw snapshot path;
- SHA-256;
- calendar year.

## Frozen local CPI calendar

RF-027 derives a local event calendar from the 19 official schedule snapshots:

`data/derived/HYP-0006-BLS-CPI-CALENDAR-2003-2021.csv`

The calendar contains only:

- event identity;
- local release date;
- local release clock time;
- UTC release timestamp;
- historical U.S. Eastern timezone semantics;
- official BLS schedule label;
- same-time BLS release labels;
- source year;
- official source URL;
- raw snapshot identity and SHA-256.

It contains no market price, return or P&L field.

Result source identity:

`BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS`

Timestamp semantics:

`BLS_ANNUAL_SCHEDULE_US_EASTERN`

## Historical U.S. Eastern conversion

Annual BLS schedule clock times are interpreted as U.S. Eastern Time.

Historical DST rule:

- through 2006: first Sunday in April through last Sunday in October;
- from 2007 onward: second Sunday in March through first Sunday in November.

UTC conversion is deterministic and is performed before any EUR/USD observation is selected.

## Event denominator

The denominator is every official BLS schedule row identifying the Consumer Price Index whose
converted release timestamp lies inside the frozen development interval.

No event may be removed because of future EUR/USD behavior.

Duplicate CPI rows for the same date are allowed only if their official release clock is identical.
Conflicting official clock times are blocking.

Same-time BLS event policy:

`FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION`

## Missing source inputs

If one or more required BLS annual snapshot files are absent, RF-027 must stop with:

`OWNER_INPUT_REQUIRED_BLS_SCHEDULE_SNAPSHOTS`

This is an OWNER input requirement, not a Hypothesis result and not a data-feasibility rejection.

Malformed/unparseable official snapshot content is a technical/source-integrity blocker.

RF-027 must never silently fall back to:

- a third-party economic calendar;
- inferred monthly dates;
- current BLS pages substituted for missing historical snapshots;
- manually typed event dates;
- live BLS HTTP retrieval.

## Granular EUR/USD source

Quote source remains:

`DUKASCOPY_HOURLY_TICK_BI5`

Candidate endpoints recorded for architecture review:

1. `https://datafeed.dukascopy.com/datafeed`
2. `https://www.dukascopy.com/datafeed`

Runtime fail-fast rule:

`FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF`

Normal RF-027 execution may issue only the first external request for a required tick object. If that request returns an HTTP/network/access failure, execution stops immediately and reports the blocker to OWNER.

The second candidate endpoint is **not** an automatic fallback. It may be tried only in a later OWNER-authorized attempt or explicit source-architecture decision.

No automatic retry loop, alternate hostname fallback, mirror or provider substitution is permitted after the first external failure.

Object path:

`EURUSD/{YEAR}/{ZERO_BASED_MONTH}/{DAY}/{HOUR}h_ticks.bi5`

Each object is LZMA-compressed and must decode into 20-byte big-endian records:

`>IIIff`

RF-027 validates:

- ordered millisecond timestamps;
- finite positive BID/ASK;
- `ASK >= BID`;
- finite non-negative volume fields.

Quote prices are inspected only for source integrity and are not written to the BLS calendar or
geometry dataset.

## Bounded tick-object rule

For each frozen CPI timestamp `t`, RF-027 requests only hourly objects spanning:

`floor(t - 60m) - 1h` through `floor(t + 60m) + 1h`

inclusive.

This permits timestamp-only geometry around:

- `t - 60m`;
- strictly before `t`;
- `t + 60m`.

RF-027 must reject any request outside the development interval or inside either frozen HYP-0005
unseen segment.

Required invariant:

`protected_hyp0005_source_requests = 0`

## Geometry only

RF-027 may calculate only timestamp/source geometry:

- nearest previous/next tick distance around `t - 60m`;
- last tick distance strictly before `t`;
- nearest previous/next tick distance around `t + 60m`;
- missing tick-object count;
- duplicate tick-timestamp count;
- source object hashes;
- event counts;
- same-time BLS flags.

RF-027 does not freeze the final numeric anchor tolerance. That is RF-028 work.

## Local outputs

Machine result:

`reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP.json`

Shareable summary:

`reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP_REPORT.txt`

Frozen-calendar candidate:

`data/derived/HYP-0006-BLS-CPI-CALENDAR-2003-2021.csv`

Tick geometry:

`data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv`

## Valid preparation decisions

`READY_FOR_DATA_FEASIBILITY_FREEZE`

Meaning: all required official BLS snapshots are present and parseable, the CPI denominator is
non-empty, event times are deterministic, HYP-0005 protected requests are zero, and at least one
event has complete granular tick timestamp geometry.

`UNRESOLVED_OFFICIAL_EVENT_TIMES`

Meaning: official snapshot content cannot produce an unambiguous CPI release timestamp.

`INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY`

Meaning: BLS calendar preparation succeeds but the bounded Dukascopy pass produces no event with
complete timestamp geometry.

These are Data Feasibility preparation decisions, not HYP-0006 market outcomes.

## Explicitly prohibited RF-027 output

RF-027 must not calculate or write:

- `pre_abs_60m_return`;
- `post_abs_60m_return`;
- return mean/median/quantile/distribution;
- the primary HYP-0006 inequality;
- directional event returns;
- trading P&L.

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

## Next step

After exact-main RF-027 PASS and review of the preparation JSON:

`ATS2-RF-028 — HYP-0006 pre-reveal data/tolerance freeze`

must freeze the exact BLS calendar SHA-256, source snapshot bundle SHA-256, eligible-event rules,
Dukascopy source identity and numeric anchor tolerances before any HYP-0006 outcome calculation.
