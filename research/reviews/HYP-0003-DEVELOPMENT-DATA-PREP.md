# HYP-0003 Development Data Preparation

Task: `ATS2-RF-008`  
Hypothesis ID: `HYP-0003`  
Status: `PREPARATION_PROTOCOL_FROZEN`  
Date: 23 September 2026

## Purpose

RF-008 materializes the full pre-protected HYP-0003 development dataset under the RF-007 Data Feasibility contract.

It may acquire, decode, normalize and quality-check source data. It computes **no formation return, cross-sectional rank, winner/loser basket, variant return or 25-cell HYP-0003 outcome**.

## Frozen dataset identity

Dataset ID: `DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001`

Dataset version: `1.0.0`

Local prepared-data path: `data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv`

Future manifest: `data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001.yaml`

Future schema: `data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV.schema.json`

## Frozen source universe

`AUDUSD, USDCAD, USDCHF, EURUSD, GBPUSD, USDJPY, USDNOK, NZDUSD, USDSEK`

No source pair may be removed because of HYP-0003 performance.

## Development and protected boundaries

Prepared event-time interval:

`2003-08-03T21:00:00Z <= event_time < 2021-09-01T00:00:00Z`

Source months: `2003-08` through `2021-08` inclusive.

Source denominator: `217 months × 9 pairs × 2 sides = 3906` monthly source objects.

RF-008 must not request, read or decode a source month at or after September 2021.

Protected tail remains:

`2021-09-01T00:00:00Z <= time < 2026-09-01T00:00:00Z`

## Source protocol and resumability

Provider/source class: Dukascopy monthly H1 BID/ASK candles.

Canonical tool: `tools/hyp0003_development_data.py`.

Each source object is cached under `data/external/dukascopy/`. Cached non-empty objects are reused. Transient network/5xx/socket failures use bounded retry batches. `404/410` on both endpoints is recorded as source absence. One-sided monthly source absence, decompression failure, malformed BI5, duplicate/out-of-order timestamps and indeterminate source state are blocking.

Raw provider bytes remain local/external and are not committed.

## BI5 point scaling

Dukascopy documents point value `100000` for most FX pairs and `1000` for JPY pairs:

`https://www.dukascopy.com/wiki/en/development/data-export/`

Frozen mapping:

- `AUDUSD = 100000`;
- `USDCAD = 100000`;
- `USDCHF = 100000`;
- `EURUSD = 100000`;
- `GBPUSD = 100000`;
- `USDJPY = 1000`;
- `USDNOK = 100000`;
- `NZDUSD = 100000`;
- `USDSEK = 100000`.

The runner must not infer scale from observed price magnitude.

## Quote normalization

Direct `CURRENCYUSD` pairs preserve source BID/ASK OHLC.

For inverse `USDCURRENCY` pairs:

- normalized BID open/close = `1 / source ASK open/close`;
- normalized BID high = `1 / source ASK low`;
- normalized BID low = `1 / source ASK high`;
- normalized ASK open/close = `1 / source BID open/close`;
- normalized ASK high = `1 / source BID low`;
- normalized ASK low = `1 / source BID high`.

All normalized prices must be finite and positive and preserve executable BID/ASK ordering for open, high, low and close.

## Time and quality contract

- timezone: `UTC`;
- event time: H1 bar open;
- availability time: event time plus one hour;
- market-hour calendar: existing regression-tested Dukascopy FX DST/weekend rule;
- ordering: event time first, then frozen currency order;
- no forward fill or interpolation.

Duplicates, out-of-order BI5 records, impossible OHLC, one-sided BID/ASK availability and BID/ASK timestamp mismatch are blocking. Missing expected market hours on both sides are reported rather than filled.

## Monthly cutoff eligibility

For each calendar source month, the cutoff is the last expected Dukascopy FX market-hour open before the next calendar month begins.

A currency is cutoff-eligible only when that exact aligned bar exists. No older stale bar may be substituted.

A monthly point is structurally eligible only when at least `6` currencies are cutoff-eligible and the ranking anchor is before the protected boundary.

RF-008 also reports the count fitting the longest declared `12-month formation / 12-month holding` calendar geometry. This is a data-geometry count, not a momentum result.

## Required local outputs

- `data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv`;
- `reports/local_ci/HYP0003_DEVELOPMENT_DATA.json`;
- `reports/local_ci/HYP0003_DEVELOPMENT_DATA_REPORT.txt`.

The report includes source-object denominator/acquired/missing counts, per-object hashes, full source-bundle SHA-256, prepared CSV SHA-256/row count, per-symbol quality/coverage, cutoff eligibility, common usable interval, longest 12/12 geometry count and protected-tail request count.

## Valid preparation outcomes

`READY_FOR_DEVELOPMENT_DATA_FREEZE`

The prepared data have a common usable interval, at least one >=6-currency ranking point and at least one longest 12/12 geometry point.

`INSUFFICIENT_DEVELOPMENT_DATA`

Preparation completes honestly but the frozen data cannot support the declared development geometry.

A valid negative data decision is not a software failure. Technical network/decompression/consistency failures remain blocking.

## Information boundary

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

RF-008 may not calculate formation returns, currency ranks, baskets, holding returns, cell means or the HYP-0003 breadth rule.

## Next step

After exact-head OWNER launcher PASS and review of the RF-008 machine result:

`ATS2-RF-009 — HYP-0003 development data freeze`
