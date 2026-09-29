# HYP-0006 Data Feasibility Preparation

Task: `ATS2-RF-027`  
Hypothesis ID: `HYP-0006`  
Status: `PREPARATION_PROTOCOL_FROZEN`  
Date: 29 September 2026

## Purpose

RF-027 machine-verifies the official U.S. CPI event denominator and granular EUR/USD
BID/ASK source geometry required by HYP-0006.

RF-027 computes **no HYP-0006 return, pre/post distribution, primary inequality or trading P&L**.

## Frozen development interval

Only events with official BLS public release time inside:

`2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z`

may enter this preparation.

Evidence classification:

`DEVELOPMENT / EXPLORATORY ONLY`

The interval is already consumed by ATS development work and cannot later be described as
independent evidence for HYP-0006.

## Official event denominator

Canonical inventory source after the proven archive-index access blocker:

`https://www.bls.gov/schedule/{YEAR}/home.htm`

for calendar years 2003 through 2021.

RF-027 parses every official CPI schedule row whose release timestamp falls inside the frozen
development interval. No event is removed because of future EUR/USD behavior.

For each scheduled CPI event RF-027 deterministically derives the official archived-release URL from
the release date and attempts to read the archived CPI embargo/publication header.

Timestamp source order:

`ARCHIVE_HEADER_PREFERRED_SCHEDULE_FALLBACK`

- if the direct archived CPI release is accessible and its timestamp is unambiguous, that timestamp
  is used;
- if direct archived-release access is denied or the timestamp is unavailable, the official annual
  schedule date/time is used;
- if an accessible archive header disagrees with the annual schedule, the event is flagged as
  `OFFICIAL_TIME_CROSSCHECK_MISMATCH`.

Allowed archive time-zone labels:

- `EST`;
- `EDT`;
- `ET`.

`EST` is converted at UTC-05:00 and `EDT` at UTC-04:00.

Annual-schedule times are interpreted as U.S. Eastern Time.

For generic `ET`, RF-027 applies the historical U.S. Eastern DST rule:

- through 2006: DST from the first Sunday in April at 02:00 local until the last Sunday in
  October at 02:00 local;
- from 2007 onward: DST from the second Sunday in March at 02:00 local until the first Sunday
  in November at 02:00 local.

The archived release date must agree with the date encoded in its official archive URL.

## BLS same-time releases

RF-027 records other official BLS release labels scheduled for the same date and local clock time.

Same-time policy remains:

`FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION`

A same-time release never removes a CPI event during RF-027.

## Granular EUR/USD source

Frozen preparation source path:

`DUKASCOPY_HOURLY_TICK_BI5`

Candidate endpoints, tried in this order:

1. `https://datafeed.dukascopy.com/datafeed`
2. `https://www.dukascopy.com/datafeed`

Object path:

`EURUSD/{YEAR}/{ZERO_BASED_MONTH}/{DAY}/{HOUR}h_ticks.bi5`

Each object is LZMA-compressed and must decode into 20-byte big-endian records:

`>IIIff`

with:

- millisecond offset from UTC hour start;
- ASK integer price;
- BID integer price;
- ASK volume;
- BID volume.

EUR/USD price divisor:

`100000`

RF-027 validates timestamp ordering, positive finite BID/ASK values and `ASK >= BID`.
Quote prices are used only for source-quality validation and are **not written to the preparation
geometry dataset**.

## Bounded tick-object request rule

For each resolved event timestamp `t`, RF-027 requests only hourly tick objects spanning:

`floor(t - 60m) - 1h` through `floor(t + 60m) + 1h`

inclusive.

This bounded window is sufficient to measure timestamp geometry around:

- `t - 60m`;
- strictly before `t`;
- `t + 60m`;

without calculating market returns.

RF-027 must refuse any source request outside the frozen HYP-0006 development interval or inside
either frozen HYP-0005 unseen segment.

## Geometry only

For each event, RF-027 may calculate only timestamp-distance facts:

- previous/next tick distance around `t - 60m`;
- last tick distance strictly before `t`;
- previous/next tick distance around `t + 60m`;
- source-object missing count;
- quote-order/coherence violation count;
- duplicate-timestamp count;
- same-time BLS release flags.

RF-027 does **not** freeze a numeric anchor tolerance. The observed geometry is input to the next
pre-reveal freeze task.

## Missing and failure semantics

- Annual BLS schedule page unavailable/unparseable: technical blocker for the affected year.
- Direct archived CPI release HTTP 403/404/410: retain the event and use the official annual-schedule
  timestamp fallback.
- Direct archive timestamp unavailable/unparseable: retain the event and use the official annual-
  schedule timestamp fallback.
- Accessible archive timestamp that disagrees with the schedule: blocking
  `OFFICIAL_TIME_CROSSCHECK_MISMATCH`.
- Dukascopy `404/410` or an empty tick object: source object is recorded missing.
- Timeout, reset, `5xx`, decompression failure or malformed binary structure: technical blocker.
- Out-of-order tick timestamp: blocking source-integrity failure.
- `ASK < BID` or non-positive/non-finite quote: blocking source-integrity failure.
- Forward fill, interpolation and synthetic quote repair: prohibited.

Network/source technical failure is not a HYP-0006 negative result.

## Local outputs

Canonical tool:

`tools/hyp0006_data_feasibility.py`

Synthetic contract tests:

`tests/test_hyp0006_data_feasibility.py`

Local runtime outputs:

- `reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP.json`
- `reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP_REPORT.txt`
- `data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv`

Raw BLS and Dukascopy source bytes remain under ignored `data/raw/`.

The geometry CSV must contain no BID, ASK, midpoint, return or P&L field.

## Valid preparation decisions

`READY_FOR_DATA_FEASIBILITY_FREEZE`

The event denominator is non-empty, every candidate event has an official BLS release timestamp,
no accessible archive/schedule mismatch is found, source acquisition completed without technical
ambiguity, and at least one event has complete timestamp geometry around all three HYP-0006 anchors.

This decision authorizes only the next pre-reveal freeze review.

`UNRESOLVED_OFFICIAL_EVENT_TIMES`

At least one candidate CPI event remains without an unambiguous official publication timestamp.

`OFFICIAL_TIME_CROSSCHECK_MISMATCH`

At least one available BLS annual schedule disagrees with its CPI archive release time.

`INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY`

The full source pass completes but no event has complete granular tick geometry around all three
required anchors.

These are Data Feasibility preparation outcomes, not HYP-0006 market outcomes.

## Information boundary

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

RF-027 is prohibited from calculating or writing:

- `pre_abs_60m_return`;
- `post_abs_60m_return`;
- any return mean, median, quantile or distribution;
- the primary HYP-0006 Boolean;
- directional event returns;
- trading P&L.

## Next step

After exact-main RF-027 PASS and OWNER delivery of the preparation JSON:

`ATS2-RF-028 — HYP-0006 pre-reveal data/tolerance freeze`

must canonicalize the exact event/source identities, decide the mechanical eligible-event denominator,
freeze numeric anchor-selection tolerances and keep the outcome boundary closed.

## RF-027 source-access correction after exact-main technical failure

Exact-main RF-027 on commit:

`a4c6331949e9c71fc68eb1baa870d20a03518d48`

passed repository validation and the full local CI gate, then failed before event acquisition because
the official BLS CPI archive index returned HTTP 403.

This is classified as:

`TECHNICAL_SOURCE_ACCESS_FAILURE`

It is not a HYP-0006 negative result and did not compute any HYP-0006 outcome.

The official BLS event source, URL and event-denominator rule remain unchanged.

To conform to the BLS automated-retrieval policy, the corrective acquisition contract freezes:

- contactable User-Agent:
  `ATS-Research/1.0 (+https://github.com/dronrome1245/ATS)`;
- BLS Referer:
  `https://www.bls.gov/`;
- BLS Accept-Language:
  `en-US,en;q=0.9`;
- minimum delay before each BLS request:
  `1.0 second`;
- a BLS HTTP 403 fails immediately and is not repeatedly retried;
- no non-BLS mirror or third-party event calendar may silently replace the official source.

This correction changes source-access mechanics only. It does not change the HYP-0006 statement,
event class, development interval, event denominator, timestamp semantics, quote source, anchor
geometry or any outcome rule.

## RF-027 official annual-schedule fallback after repeated BLS archive-index 403

A second exact-main RF-027 attempt on:

`2ce019bb51b0e45e900c0555ed44be5a3433e23a`

again passed Local CI and again received HTTP 403 from the official CPI archive-index page before
event acquisition.

This remains:

`TECHNICAL_SOURCE_ACCESS_FAILURE`

and not a HYP-0006 result.

The event denominator is unchanged: every official BLS CPI release whose public release timestamp is
inside the frozen development interval.

The acquisition route is corrected as follows:

1. obtain the CPI denominator from official BLS annual release schedules
   `https://www.bls.gov/schedule/{YEAR}/home.htm` for 2003 through 2021;
2. derive each CPI archive URL deterministically from the official scheduled release date;
3. prefer the archived CPI release embargo/publication header when that direct archive page is
   accessible and parseable;
4. when direct archived-release access is denied or the archive timestamp is unavailable, use the
   official annual-schedule date/time as the predeclared fallback;
5. annual-schedule times are interpreted as U.S. Eastern Time using the already frozen historical
   DST rules;
6. if an accessible archive header disagrees with the official annual schedule, record
   `OFFICIAL_TIME_CROSSCHECK_MISMATCH` and do not silently choose a favorable timestamp;
7. same-time BLS releases remain
   `FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION`;
8. no third-party calendar or event source is introduced.

Result provenance must report:

`event_inventory_source = BLS_OFFICIAL_ANNUAL_SCHEDULES`

and:

`event_time_source_order = ARCHIVE_HEADER_PREFERRED_SCHEDULE_FALLBACK`

This correction changes only official-source acquisition mechanics after a proven network/access
blocker. It does not change the HYP-0006 statement, event class, development interval, event
denominator, quote source, horizons, anchor definitions or outcome rule.

