# HYP-0003 Data Feasibility Review

Task: `ATS2-RF-005`  
Hypothesis ID: `HYP-0003`  
Review status: `CONDITIONAL`  
Date: 23 September 2026

## 1. Decision question

Can ATS obtain and freeze synchronized point-in-time multi-currency FX BID/ASK data that can evaluate the fixed 25-cell HYP-0003 development grid without performance-based universe selection, timing leakage or use of future confirmatory data?

Current decision:

`CONDITIONAL`

The source class and data semantics are plausible and externally documented, but exact instrument availability, common historical coverage and source integrity must be verified by a machine preparation step before any HYP-0003 development outcome is calculated.

## 2. Hypothesis requirements carried into the review

HYP-0003 requires:

- monthly cross-sectional ranking;
- formation periods `1, 3, 6, 9, 12 months`;
- holding periods `1, 3, 6, 9, 12 months`;
- exactly `25` declared development variants;
- at least six eligible currencies at each ranking point;
- winner/loser extreme baskets;
- side-aware BID/ASK execution;
- a full parameter-surface result, not winner-only reporting;
- no confirmatory block reveal inside HYP-0003.

Economic interpretation remains:

`QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING`

## 3. Candidate source

Primary source candidate:

Dukascopy Historical Data Export / Dukascopy historical-data service.

Official source references:

- `https://www.dukascopy.com/swiss/english/marketwatch/historical/`
- `https://www.dukascopy.com/api/data/get/historical-data-export`
- `https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/historical-data-service/`

The official material states that historical export covers multiple financial instruments, supports multiple timeframes and exposes BID/ASK prices. The historical-data service can report the first available history for instrument/feed combinations.

This establishes source plausibility, not exact HYP-0003 coverage.

## 4. Predeclared currency candidate set

To prevent return-based universe selection, the machine preparation step must start from the standard G10 currency set excluding USD:

`AUD, CAD, CHF, EUR, GBP, JPY, NOK, NZD, SEK`

Mechanical USD-pair candidates:

- `AUDUSD`
- `USDCAD`
- `USDCHF`
- `EURUSD`
- `GBPUSD`
- `USDJPY`
- `USDNOK`
- `NZDUSD`
- `USDSEK`

Inclusion/exclusion may depend only on pre-result data feasibility: source availability, BID/ASK presence, common coverage, timestamp integrity and the frozen quality policy.

A currency must not be excluded because its momentum result is unattractive.

If fewer than `6` currencies remain feasible under the frozen source/quality rules, HYP-0003 development is blocked.

## 5. Quote normalization

All currencies must be represented as currency value in USD so positive return always means appreciation of the non-USD currency versus USD.

For a direct `CURRENCYUSD` quote:

- normalized BID = source BID;
- normalized ASK = source ASK.

For an inverse `USDCURRENCY` quote:

- normalized BID = `1 / source ASK`;
- normalized ASK = `1 / source BID`.

This preserves executable side ordering after inversion.

The preparation report must verify normalized ASK >= normalized BID for every retained observation.

## 6. Cross-sectional basket rounding

HYP-0003 uses strongest and weakest one-sixth baskets.

Because the feasible cross-section may not be divisible by six, Data Feasibility freezes the operational rounding rule before results:

`basket_size = max(1, ceil(eligible_currency_count / 6))`

At each ranking timestamp:

- strongest `basket_size` currencies form the winner basket;
- weakest `basket_size` currencies form the loser basket;
- middle currencies are not in the extreme baskets.

Ties at a ranking boundary must use a deterministic currency-code tie break. No return-dependent discretionary tie handling is allowed.

## 7. Time and synchronization semantics

Required source granularity:

`1H BID/ASK bars`

H1 is finer than the monthly research decision and allows deterministic construction of month-boundary formation and execution prices without relying on daily-close conventions that may differ by source.

All source bars must be represented in UTC with:

- event time = H1 bar open;
- availability time = one hour after bar open for completed-bar information;
- explicit FX market-hour/weekend-gap handling;
- deterministic ordering;
- exact BID/ASK timestamp alignment per instrument.

Monthly ranking cutoff:

- use the last fully completed eligible H1 bar before the next calendar month begins;
- ranking information becomes usable only at that bar's availability time;
- modeled entry occurs no earlier than the first eligible quote/bar open at or after that availability time.

Exact implementation timestamps and gap behavior must be emitted by the machine preparation report before development execution is allowed.

## 8. Development versus future confirmatory boundary

HYP-0003 is development-only.

To keep a large later block unavailable for tuning, the following period is reserved and must not be processed by the HYP-0003 development preparation/runner:

`2021-09-01T00:00:00Z <= time < 2026-09-01T00:00:00Z`

Protected-tail length:

`60 full calendar months`

The machine preparation step may inspect source metadata/existence needed to establish availability, but must not calculate cross-sectional momentum features, returns or HYP-0003 outcomes on the protected tail.

Development coverage must end strictly before `2021-09-01T00:00:00Z`.

The exact common development start is unresolved until all candidate instruments are checked.

If a later fixed confirmatory Hypothesis is created, it may use some or all of the reserved tail only after a new Hypothesis freezes its parameters, dataset identity and decision rule.

## 9. Coverage and universe integrity

The preparation step must report, for every candidate symbol:

- first available usable H1 BID/ASK timestamp;
- last checked development timestamp;
- missing tradable hours;
- duplicate/out-of-order counts;
- source file count and source hashes;
- normalized quote validity;
- retained/excluded status and reason.

It must then calculate the common development interval using only retained currencies.

No performance metric may influence the common start, retained set or gap policy.

The review does not set a universal minimum number of development observations beyond HYP-0003's six-currency requirement. The preparation report must expose the number of eligible monthly ranking points for the longest 12-month formation / 12-month holding cell before a final feasibility freeze.

## 10. Missing/bad data policy

Default policy:

- duplicate timestamp: blocking for that source object until resolved;
- malformed/non-positive quote: blocking;
- synchronized scalar/tick ASK below BID after normalization: blocking;
- component-wise crossing between separately aggregated BID/ASK OHLC extrema is not by itself a bad-data signal; each side must remain internally valid and source/timestamp coherent;
- unexplained BID/ASK timestamp mismatch: blocking;
- closed-market weekend/session gaps: declared, not filled;
- missing tradable-hour bars: reported explicitly, not silently interpolated;
- stale observations at a monthly cutoff: the affected currency is ineligible for that ranking timestamp under a rule frozen before development results.

The future preparation tool must make the stale/missing cutoff rule deterministic and report affected counts.

## 11. Point-in-time universe and survivorship

The candidate currency list is fixed before development results.

These are currencies, not equities with delistings, but source availability can still change historically.

A currency is eligible at a ranking timestamp only if the frozen source/quality rule shows that its required formation and execution data were available at that time.

Current-day data completeness must not be projected backward silently.

No currency may be added after development results are seen merely because it improves the momentum surface.

## 12. Cost and execution applicability

Spread:

`REPRESENTED_BY_BID_ASK`

Commission:

`NOT_YET_MODELED`

Financing / rollover:

`NOT_YET_MODELED_AND_MATERIALLY_RELEVANT_FOR_MULTI_MONTH_HOLDS`

Slippage / live fill realism:

`NOT_MODELED`

Therefore HYP-0003 may only answer whether a quote-executable **spot-price continuation structure after spread** exists across the development grid.

Even a positive HYP-0003 development result is not an economic-profitability result.

Before Candidate promotion or formal economic claims, financing and other applicable costs must be resolved.

## 13. Known gaps

Blocking before any development outcome:

1. exact Dukascopy availability for all nine candidate USD pairs has not yet been machine verified;
2. earliest common usable H1 BID/ASK timestamp is unknown;
3. common monthly ranking-point count is unknown;
4. source-bundle hashes are not frozen;
5. deterministic stale-at-cutoff statistics are not yet measured.

Not blocking for the next preparation task:

- commission value is unknown;
- financing/rollover is unresolved;
- live-fill slippage is unresolved.

Those limitations restrict interpretation but do not prevent a development-stage structural screen after spread.

## 14. Information boundary

Current information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

No HYP-0003 variant return surface has been calculated in this review.

No protected-tail HYP-0003 outcome has been calculated.

## 15. Decision

Decision:

`CONDITIONAL`

Reason:

Dukascopy provides an appropriate documented historical-data source class with BID/ASK and multi-instrument support, and HYP-0003 now has deterministic universe, orientation, basket, timing and protected-tail rules. However exact symbol availability/common coverage and data integrity must be verified locally before the dataset can be frozen.

HYP-0003 development execution is **not authorized yet**.

## 16. Next task

After exact-head OWNER launcher PASS:

`ATS2-RF-006 — HYP-0003 Data Feasibility preparation`

The preparation task must:

- verify the nine predeclared source symbols;
- freeze the retained feasible universe without using returns;
- determine the common development start;
- keep all data at or after `2021-09-01T00:00:00Z` out of HYP-0003 development calculations;
- produce hashes and coverage/quality statistics;
- compute **no HYP-0003 momentum outcome**.


## 17. RF-007 freeze update — source-qualified universe and development-data contract

This dated update records the RF-006 exact-head preparation result and supersedes only the unresolved preparation facts in Sections 9, 13, 15 and 16. The earlier `CONDITIONAL` decision history is retained.

### 17.1 Canonical RF-006 preparation result

Exact-head OWNER launcher PASS was obtained on:

`acf197d5774116c7d9a8b742eab77c6ee3447214`

Canonical preparation result:

`reports/research/HYP-0003-DATA-FEASIBILITY-PREP-result.json`

The machine result records:

- preparation decision: `READY_FOR_FREEZE_REVIEW`;
- Dukascopy history metadata instruments: `1512`;
- history metadata SHA-256: `215ad432126018f4f871a1e10bc3f315524b84ae29d83fc3fd3adc188107417d`;
- August 2021 boundary probe objects: `18`;
- probe bundle SHA-256: `a88add123fd42e83396ba17de13cf65fedf18d8e0a5e1eca476ed6338c91b45e`;
- retained source currencies: `AUD, CAD, CHF, EUR, GBP, JPY, NOK, NZD, SEK`;
- retained currency count: `9`;
- minimum required: `6`;
- common possible development start: `2003-08-03T21:00:00Z`;
- development end exclusive: `2021-09-01T00:00:00Z`;
- information boundary: `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

Per-symbol H1 history starts recorded by RF-006:

| Currency | Source pair | Orientation | H1 history start | RF-006 status |
|---|---|---|---|---|
| AUD | AUDUSD | DIRECT | 2003-08-03T21:00:00Z | SOURCE_AVAILABLE |
| CAD | USDCAD | INVERSE | 2003-08-03T21:00:00Z | SOURCE_AVAILABLE |
| CHF | USDCHF | INVERSE | 2003-05-04T20:00:00Z | SOURCE_AVAILABLE |
| EUR | EURUSD | DIRECT | 2003-05-04T21:00:00Z | SOURCE_AVAILABLE |
| GBP | GBPUSD | DIRECT | 2003-05-04T20:00:00Z | SOURCE_AVAILABLE |
| JPY | USDJPY | INVERSE | 2003-05-04T21:00:00Z | SOURCE_AVAILABLE |
| NOK | USDNOK | INVERSE | 2003-08-03T21:00:00Z | SOURCE_AVAILABLE |
| NZD | NZDUSD | DIRECT | 2003-08-03T21:00:00Z | SOURCE_AVAILABLE |
| SEK | USDSEK | INVERSE | 2003-08-03T21:00:00Z | SOURCE_AVAILABLE |

The RF-006 probe result is source/data-feasibility evidence only. It contains no HYP-0003 momentum result.

### 17.2 Frozen source-qualified universe

The source-qualified candidate universe is frozen as all nine predeclared currencies:

`AUD, CAD, CHF, EUR, GBP, JPY, NOK, NZD, SEK`

No currency was removed by strategy return or momentum behavior.

Point-in-time eligibility may still vary at a monthly ranking timestamp under the frozen quality rules below. Such ineligibility does not remove the currency from the candidate universe and may not be used to select currencies by observed HYP-0003 performance.

### 17.3 Full development-data acquisition contract

Future development dataset identity:

- dataset ID: `DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001`;
- dataset version: `1.0.0`;
- source class: Dukascopy monthly H1 BID/ASK candles;
- target event-time interval: `2003-08-03T21:00:00Z <= event_time < 2021-09-01T00:00:00Z`;
- protected-tail rule: RF-008 must not request, read, decode or derive source months at or after September 2021;
- future manifest path: `data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001.yaml`;
- future schema path: `data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV.schema.json`;
- local prepared-data path: `data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv`.

RF-008 must attempt the monthly BID and ASK H1 source objects for every frozen source pair from August 2003 through August 2021 inclusive. Raw provider bytes remain local/external and are not committed to Git.

Acquisition must remain resumable at the source-object boundary. A cached source object with a recorded SHA-256 is reused. `404/410` source absence is recorded as source absence; timeout, reset, 5xx, decompression or indeterminate failures remain technical blockers and may not be relabeled as missing market data.

The full source-bundle SHA-256 must be calculated from a canonical, sorted serialization of each acquired object's `symbol`, `month`, `side` and object SHA-256. The RF-006 `probe_bundle_sha256` is not a substitute for that identity.

### 17.4 Quote normalization, time and quality contract

Direct `CURRENCYUSD` pairs preserve source BID and ASK sides.

For inverse `USDCURRENCY` pairs, normalized OHLC is frozen as:

- normalized BID open/close = `1 / source ASK open/close`;
- normalized BID high = `1 / source ASK low`;
- normalized BID low = `1 / source ASK high`;
- normalized ASK open/close = `1 / source BID open/close`;
- normalized ASK high = `1 / source BID low`;
- normalized ASK low = `1 / source BID high`.

All normalized quote fields must be finite and positive. Each side's OHLC must remain internally valid.

**RF-008 diagnostic correction (2026-09-24):** Dukascopy non-tick candles are side-specific BID or ASK aggregates. Corresponding BID/ASK high and low values are not guaranteed to represent the same intra-bar instant. Therefore component-wise `ASK >= BID` across separately aggregated H1 OHLC fields is not a valid candle-quality invariant and is superseded for RF-008 preparation. This does not authorize synthetic spread repair, forward fill, source mixing or relaxed timestamp alignment.

Time semantics remain:

- timezone: `UTC`;
- event time: H1 bar open;
- availability time: event time plus one hour;
- market-hour calendar: reuse the existing regression-tested Dukascopy FX `is_fx_market_hour()` semantics;
- exact BID/ASK timestamp alignment is required per symbol;
- duplicates, out-of-order records and malformed/impossible quotes are blocking;
- expected closed-market hours are declared gaps and are never filled;
- missing expected tradable-hour bars are counted explicitly and never interpolated or forward-filled.

For each calendar-month ranking boundary, the eligible cutoff bar for a currency is the aligned completed H1 bar at the **last expected Dukascopy FX market-hour open before the next calendar month begins**. If that expected bar is missing or invalid, that currency is ineligible at that ranking timestamp. RF-008 may not silently fall back to an older stale bar.

Modeled entry remains no earlier than the first eligible quote/bar open at or after the cutoff bar's availability time.

If fewer than six currencies are eligible at a ranking timestamp, HYP-0003 makes no claim for that timestamp.

### 17.5 RF-008 required preparation outputs

Before any HYP-0003 momentum cell may be evaluated, RF-008 must report at minimum:

- acquired/missing source-object counts and per-object SHA-256 identities;
- full source-bundle SHA-256;
- per-symbol first/last usable timestamps and aligned row counts;
- duplicate, out-of-order, malformed and impossible-quote counts;
- expected tradable-hour missing counts and declared session-gap counts;
- normalized quote-order validity;
- monthly cutoff ineligibility counts by currency and reason;
- final common usable development interval;
- eligible monthly ranking-point count;
- the count supporting the longest `12-month formation / 12-month holding` geometry with the holding effect ending before `2021-09-01T00:00:00Z`;
- prepared dataset SHA-256 and manifest/schema identities.

RF-008 is prohibited from calculating formation returns, cross-sectional ranks, winner/loser baskets, any of the 25 variant returns or the HYP-0003 breadth decision.

### 17.6 Feasibility decision after RF-006

Decision remains:

`CONDITIONAL`

Resolved by RF-006:

- all nine predeclared source pairs are source-qualified at the development boundary;
- the common possible development start is now known;
- provider-native metadata and boundary probe identities are frozen.

Still required before development outcome execution:

- full pre-protected source acquisition;
- full source-bundle and prepared-dataset hashes;
- whole-period quality statistics;
- deterministic monthly-cutoff eligibility statistics;
- eligible monthly ranking-point counts, including the longest 12/12 geometry.

Therefore RF-007 authorizes **development-data preparation only**. It does not authorize calculation of any HYP-0003 development outcome.

Hypothesis reformulation required:

`NO`

### 17.7 Next task

After exact-head OWNER launcher PASS for RF-007:

`ATS2-RF-008 — HYP-0003 development data preparation`

The protected tail remains unavailable to HYP-0003 development.

## 18. RF-009 development data freeze update

Task: `ATS2-RF-009`  

This update canonicalizes the exact RF-008 OWNER PASS result before any HYP-0003 development outcome is calculated. It supersedes the unresolved development-data facts in Sections 9, 13, 15 and 16 while preserving the historical `CONDITIONAL` review record and all cost/execution limitations.

### 18.1 Canonical RF-008 preparation result

Exact-head OWNER launcher PASS was obtained on:

`63e1bc9c7e1ba2e001ecdd9918244d83db0e58c3`

Canonical result:

`reports/research/HYP-0003-DEVELOPMENT-DATA-PREP-result.json`

RF-008 recorded:

- preparation decision: `READY_FOR_DEVELOPMENT_DATA_FREEZE`;
- source months: `217`;
- source objects: `3906 / 3906` acquired, `0` missing;
- source bundle SHA-256: `9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a`;
- prepared rows: `1,014,509`;
- prepared CSV SHA-256: `8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2`;
- common usable start: `2003-08-03T21:00:00Z`;
- common usable end: `2021-08-31T23:00:00Z`;
- monthly ranking points with at least six cutoff-eligible currencies: `207`;
- points supporting the longest declared 12-month formation / 12-month holding geometry: `184`;
- protected-tail source objects requested: `0`;
- information boundary: `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

### 18.2 Frozen development dataset identity

Dataset:

`DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001@1.0.0`

Canonical manifest:

`data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001.yaml`

Canonical row schema:

`data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV.schema.json`

Prepared local bytes:

`data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv`

The Dataset Manifest freezes the RF-008 source snapshot, prepared-data digest, time semantics, deterministic ordering, quality policy and transformation lineage. A source snapshot, prepared-data hash, coverage, schema, timestamp semantic or preparation change is a material dataset change and may not silently replace this version.

### 18.3 Quality result carried into the freeze

| Currency | Source pair | Prepared rows | Missing expected market hours | Cutoff-eligible months | Cutoff-missing months |
|---|---|---:|---:|---:|---:|
| AUD | AUDUSD | 112054 | 1157 | 203 | 14 |
| CAD | USDCAD | 112864 | 347 | 208 | 9 |
| CHF | USDCHF | 112879 | 332 | 208 | 9 |
| EUR | EURUSD | 112900 | 311 | 208 | 9 |
| GBP | GBPUSD | 112872 | 339 | 207 | 10 |
| JPY | USDJPY | 112872 | 339 | 208 | 9 |
| NOK | USDNOK | 112848 | 363 | 208 | 9 |
| NZD | NZDUSD | 112832 | 379 | 208 | 9 |
| SEK | USDSEK | 112388 | 823 | 207 | 10 |

These gaps/cutoff statistics are retained as data-quality facts. No currency was added or removed based on HYP-0003 returns or momentum behavior. Missing hours remain unfilled.

### 18.4 RF-009 freeze decision

Freeze decision:

`FREEZE_DEVELOPMENT_DATASET`

Reason:

RF-008 completed the full frozen source denominator, produced a stable prepared-data digest, retained all nine source-qualified currencies, exposed explicit gap/cutoff statistics, provided `207` structurally eligible >=6-currency monthly anchors and `184` anchors for the longest declared 12/12 geometry, and made zero protected-tail source requests.

The overall Data Feasibility review remains `CONDITIONAL` because commission, financing/rollover and live-fill slippage are not resolved. This freeze authorizes only the use of this exact dataset version for a later HYP-0003 development-stage structural screen after spread; it does not establish economic profitability, Candidate status, validation evidence or independent evidence.

### 18.5 Information boundary

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

RF-009 freezes metadata and bytes only. Formation returns, currency ranks, winner/loser baskets, holding returns, 25-cell means and the breadth rule remain uncomputed during this task.

The protected tail beginning `2021-09-01T00:00:00Z` remains closed.
