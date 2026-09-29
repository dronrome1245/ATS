# HYP-0006 Data Feasibility Review

Task: `ATS2-RF-026`  
Hypothesis ID: `HYP-0006`  
Review status: `CONDITIONAL`  
Date: 29 September 2026

## 1. Decision question

Can ATS represent the scheduled U.S. CPI publication time and synchronized granular EUR/USD BID/ASK observations required by HYP-0006 without using HYP-0005 protected data, without publication-time leakage and without computing the HYP-0006 outcome during Data Feasibility?

Current decision:

`CONDITIONAL`

The required source classes are externally verified as available:

- the U.S. Bureau of Labor Statistics publishes official historical release schedules and an archived CPI news-release index;
- historical CPI release records expose scheduled/embargo release dates and times in U.S. Eastern time;
- Dukascopy documents free historical FX data export from tick-by-tick through coarser periods and a historical-data service that can expose first available tick history.

This is sufficient to authorize a pre-result machine preparation step. It is not sufficient to authorize HYP-0006 outcome computation because the exact event inventory, tick-source acquisition path, granular coverage, quote-anchor tolerances, data hashes and whole-period geometry have not yet been verified on the OWNER host.

No `pre_abs_60m_return`, `post_abs_60m_return` or primary inequality is calculated in RF-026.

## 2. HYP-0006 requirements carried into the review

HYP-0006 already freezes:

- market: `FX_SPOT_OTC`;
- instrument: `EURUSD`;
- event class: scheduled U.S. Consumer Price Index publication;
- primary event timestamp: defensible public-release timestamp `t`;
- `PRE_60_ANCHOR`: eligible synchronized quote representing `t - 60 minutes`;
- `PRE_RELEASE_ANCHOR`: last eligible synchronized quote strictly before `t`;
- `POST_60_ANCHOR`: eligible synchronized quote representing `t + 60 minutes`;
- pre-event horizon: previous 60 minutes;
- post-event horizon: next 60 minutes;
- primary claim:
  `median(post_abs_60m_return) > median(pre_abs_60m_return)`;
- no directional EUR/USD return sign;
- no point-in-time consensus or surprise magnitude;
- no trading-P&L claim;
- no post-result search across event categories, instruments, horizons or favorable subperiods.

Data Feasibility may specify source identity, coverage, timestamp conversion, anchor tolerances, missing-data policy, event-cluster diagnostics and dataset identity. It may not change the claim above.

## 3. Event-source candidate

Primary event source family:

`U.S. Bureau of Labor Statistics — official release schedules and CPI archived news releases`

Official source references:

- `https://www.bls.gov/schedule/`
- `https://www.bls.gov/bls/news-release/cpi.htm`

The BLS annual schedule archive exposes historical CPI release dates and scheduled times. The archived CPI news-release index retains historical CPI releases across the HYP-0006 development era. Individual archived releases identify their transmission embargo/release time, including explicit `EST`, `EDT` or `ET` notation depending on era.

Examples verified before RF-026:

- 2003 BLS schedule: CPI releases are listed at `8:30 am`; July 2003 CPI was scheduled for 15 August 2003 at `8:30 am`;
- the archived July 2003 CPI release states embargo until `8:30 A.M. (EDT)` on 15 August 2003;
- 2021 BLS schedule states all calendar times are Eastern Time and lists CPI at `08:30 AM`;
- archived 2020/2021 CPI releases likewise identify `8:30 a.m.` release time.

These checks establish official event-time source plausibility. RF-027 must machine-verify the full frozen event inventory rather than infer missing dates.

## 4. Frozen development coverage for source preparation

HYP-0006 development-source preparation is restricted to:

`2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z`

Rationale:

- this interval is chosen before any HYP-0006 result;
- it reuses an already-consumed ATS development interval rather than reserving a new independent block;
- it is compatible with the established EUR/USD research-data lineage;
- it excludes both frozen HYP-0005 unseen segments;
- it stops before the HYP-0003 protected-tail boundary at `2021-09-01T00:00:00Z`.

Evidence classification:

`DEVELOPMENT / EXPLORATORY ONLY`

This interval may never be described as HYP-0006 independent evidence.

RF-027 must request no HYP-0006 market data outside this interval.

## 5. Frozen event-inventory rule

Candidate event denominator:

every official BLS CPI release whose public release timestamp falls inside the frozen development interval.

RF-027 must construct the denominator mechanically from official BLS sources and retain every candidate event before quote availability is assessed.

For each candidate event, RF-027 must record at minimum:

- BLS release label / reference month if available;
- official release date;
- official local release time;
- time-zone label/source semantics;
- canonical UTC release timestamp;
- annual schedule source identity;
- archived release source identity when available;
- whether schedule and archived-release timing agree;
- same-time BLS release labels from the official calendar;
- eligibility status and any data-feasibility exclusion reason.

No event may be removed because its future EUR/USD response is small, adverse or inconvenient.

## 6. Publication-time semantics

Canonical research timezone:

`UTC`

Primary event-time source order:

1. archived BLS CPI release header / embargo-publication timestamp when machine-readable and unambiguous;
2. official BLS annual release schedule as cross-check and fallback only when the review can establish equivalent publication-time semantics;
3. otherwise the event remains unresolved and is not silently assigned a third-party time.

Eastern-time conversion must be deterministic and historically correct.

For 2003–2006 U.S. daylight-saving dates, RF-027 must use the pre-2007 U.S. DST rule.

For 2007 onward, RF-027 must use the post-2007 U.S. DST rule.

The preparation tool must regression-test at least one `EST` event and one `EDT` event from the development interval against an archived BLS release.

An unresolved event-time discrepancy is a Data Feasibility exclusion/block, not permission to choose a favorable timestamp.

## 7. Same-time event clustering

BLS CPI releases commonly share the same official timestamp with `Real Earnings`.

RF-026 freezes the following policy:

`FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION`

All otherwise eligible CPI releases remain in the event denominator even when another official BLS release shares the same timestamp.

RF-027 must record same-time BLS labels as diagnostics.

The first HYP-0006 prototype may not remove same-time events after observing returns.

Non-BLS same-time macro announcements are a known attribution limitation. RF-026 does not claim that every observed post-release move is caused solely by CPI.

## 8. Quote-source candidate

Primary quote-source candidate:

`Dukascopy historical EUR/USD tick data`

Official source references:

- `https://www.dukascopy.com/swiss/english/marketwatch/historical/`
- `https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/historical-data-service/`

Dukascopy documents historical FX export from tick-by-tick through monthly periods. The historical-data service documents historical tick access and first-available-history queries.

Required source characteristics:

- EUR/USD;
- explicit tick or equivalently fine quote timestamps;
- coherent BID/ASK representation;
- enough precision to identify the last eligible synchronized quote strictly before release;
- enough coverage for both `t - 60m` and `t + 60m`;
- reproducible source-object identity and hashes.

RF-026 does not freeze an undocumented raw URL or assume exact tick inception. RF-027 must verify the exact acquisition path and development coverage on the OWNER host before the source can be frozen.

## 9. Granularity and anchor requirements

Required granularity:

`TICK OR SUB-MINUTE BID/ASK SUFFICIENT FOR EVENT-ANCHOR SELECTION`

H1 data are not sufficient for HYP-0006 because the hypothesis requires a quote strictly before a scheduled 08:30 Eastern event boundary.

RF-027 may inspect only quote timing/identity/quality geometry.

It must not calculate event returns or distribution summaries.

Before later outcome computation, Data Feasibility must freeze numeric tolerances for:

- maximum distance from `t - 60m` for `PRE_60_ANCHOR`;
- maximum staleness before `t` for `PRE_RELEASE_ANCHOR`;
- maximum distance from `t + 60m` for `POST_60_ANCHOR`;
- whether anchor selection is previous-tick, first-tick-at-or-after target, nearest-with-directional-constraint, or another deterministic rule.

The `PRE_RELEASE_ANCHOR` rule must always satisfy:

`quote_time < release_time`

No quote timestamp at or after release may serve as the pre-release anchor.

## 10. BID/ASK coherence

RF-027 must verify source semantics before any later prototype.

For every retained quote used in anchor-geometry checks:

- BID and ASK must refer to one coherent provider observation or a provider-native synchronized representation;
- values must be finite and positive;
- `ask >= bid`;
- timestamps must be deterministic and ordered;
- no synthetic spread repair is permitted;
- no side mixing across unrelated timestamps is permitted;
- no mid-only substitution is permitted.

If the exact provider export supplies one-sided tick streams rather than synchronized quote pairs, RF-027 must document the provider semantics and propose a deterministic point-in-time reconstruction rule for later freeze. It may not infer a favorable pairing from future price movement.

## 11. Missing and bad data policy

Frozen preparation policy:

- duplicate source observation with ambiguous ordering: blocking until deterministic provider semantics are established;
- out-of-order source records: blocking;
- malformed/non-positive quote: blocking for that source object;
- `ask < bid`: blocking for the proposed synchronized quote representation;
- missing event-source record: event remains in denominator and is marked event-time unresolved;
- missing quote around an event anchor: event remains in denominator and is marked quote-ineligible for the applicable reason;
- forward fill: prohibited;
- interpolation: prohibited;
- future-tick backfill into `PRE_RELEASE_ANCHOR`: prohibited;
- alternative vendor substitution after seeing HYP-0006 returns: prohibited.

RF-027 must report the complete denominator and every exclusion count.

## 12. Revisions and decision-time information

The first HYP-0006 test uses only event identity and publication timing.

It does not use:

- CPI released value;
- revised CPI value;
- market consensus;
- economic surprise;
- later classification of the release as positive/negative.

Therefore CPI value revision risk does not affect the primary HYP-0006 calculation.

The event timestamp itself remains point-in-time critical. Later corrected or reconstructed release times may not be silently substituted after HYP-0006 outcome inspection.

## 13. Selection, overlap and independence

Instrument selection:

`EURUSD — FROZEN BY HYP-0006`

Event selection:

`U.S. CPI — FROZEN BY HYP-0006`

Development period:

`FROZEN_BY_RF026_PRE_RESULT_DATA_LINEAGE_RULE`

The development interval overlaps data already exposed elsewhere in ATS and is explicitly classified as development/exploratory.

HYP-0005 protected/unseen segments consumed by HYP-0006:

`0`

RF-027 must enforce zero source requests inside:

- `LEFT_UNSEEN = [2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)`;
- `RIGHT_UNSEEN = [2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)`.

Any future validation/independent block must be separately established after HYP-0006 development and cannot automatically reuse known ATS history as independent evidence.

## 14. Planned dataset and trace identity

Candidate development dataset ID:

`DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001@1.0.0`

Planned local prepared path:

`data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv`

The future prepared dataset must contain only pre-result event/quote identity and anchor-geometry fields until a later prototype freeze authorizes return calculation.

Minimum preparation outputs:

- BLS event-source object inventory and hashes;
- candidate CPI event count;
- resolved/unresolved event-time counts;
- per-event canonical UTC release timestamp;
- same-time BLS cluster diagnostics;
- Dukascopy source-object inventory and hashes;
- quote coverage around each event;
- quote-order/coherence violations;
- anchor-availability geometry;
- counts by calendar year;
- zero requests into HYP-0005 protected segments;
- prepared geometry CSV SHA-256;
- information boundary `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

Prohibited RF-027 fields:

- `pre_abs_60m_return`;
- `post_abs_60m_return`;
- pre/post return mean, median or quantile;
- primary inequality result;
- any event-direction trading result;
- any trading P&L.

## 15. Cost and execution applicability

The HYP-0006 primary question is structural, not trading P&L.

Spread / BID-ASK:

`REQUIRED AS QUOTE-DATA QUALITY AND LATER FRICTION DIAGNOSTIC`

Commission:

`NOT_APPLICABLE_TO_PRIMARY_STRUCTURAL_CLAIM`

Financing / rollover:

`NOT_APPLICABLE_TO_PRIMARY_60-MINUTE STRUCTURAL_CLAIM`

Slippage / latency:

`NOT_MODELED IN PRIMARY STRUCTURAL CLAIM; MATERIAL FOR ANY LATER TRADING INTERPRETATION`

Passing the structural claim would not establish a profitable or executable event strategy.

## 16. Known gaps

Blocking before any HYP-0006 outcome:

1. the exact BLS event-inventory parser and source-object identities are not yet machine frozen;
2. all candidate event timestamps have not yet been reconciled against official BLS source records;
3. exact Dukascopy EUR/USD tick acquisition path and earliest usable tick history have not yet been verified on the OWNER host;
4. full development-period event-window source coverage is unknown;
5. synchronized BID/ASK tick semantics for the selected acquisition path require machine verification;
6. numeric anchor-selection tolerances are not yet frozen;
7. whole-period missing/quality/anchor geometry and source hashes are unknown;
8. dedicated prepared-data identity has not yet been frozen.

Not blocking for the source/timing preparation task:

- commission schedule;
- financing;
- live execution latency model;
- future independent-evidence block.

## 17. Information boundary

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

RF-026 has not calculated:

- `pre_abs_60m_return`;
- `post_abs_60m_return`;
- any pre/post return distribution;
- the primary inequality;
- any trading P&L.

## 18. Feasibility decision

Decision:

`CONDITIONAL`

Reason:

Official BLS sources provide a reproducible historical CPI release-calendar/archive path with explicit publication-time information, and Dukascopy documents an appropriate granular historical FX source class including tick history. These source classes are sufficient to justify a bounded machine preparation task on an already-consumed development interval. However exact full-denominator event identity, granular EUR/USD source access, tick coverage, synchronized BID/ASK semantics, anchor tolerances and source/dataset hashes must be frozen before HYP-0006 can proceed to any outcome calculation.

Prototype authorization:

`NOT_YET_AUTHORIZED`

Hypothesis reformulation required:

`NO`

## 19. Next task

After RF-026 exact-main PASS:

`ATS2-RF-027 — HYP-0006 Data Feasibility preparation`

RF-027 must verify and freeze only event/quote source identity, publication-time semantics, full event denominator, granular quote coverage, quote quality and anchor geometry.

RF-027 must retain:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

A later freeze task must canonicalize the RF-027 preparation result and freeze the exact development dataset/tolerances before a prototype runner may calculate the first HYP-0006 outcome.
