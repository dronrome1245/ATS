# HYP-0003 Data Feasibility Review

**Task:** `ATS2-RF-005`  
**Hypothesis ID:** `HYP-0003`  
**Review status:** `CONDITIONAL`  
**Date:** 23 September 2026

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
- ASK below BID after normalization: blocking;
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
