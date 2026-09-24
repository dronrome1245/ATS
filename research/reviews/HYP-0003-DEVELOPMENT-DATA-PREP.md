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

Each source object is cached under `data/external/dukascopy/`. Cached non-empty objects are reused. The current provider-native primary path is Dukascopy's `https://jetta.dukascopy.com/v1` compact JSON H1 monthly bucket API. Existing/legacy Dukascopy BI5 monthly objects remain accepted as a cache-compatible fallback. Transient network/5xx/socket failures use bounded retry batches. Source absence is recorded only when the available provider-native paths classify the object as absent; technical failure on any unresolved path remains blocking.

This endpoint change does not change provider, frozen source pair, month, side, event-time interval or information boundary. Raw provider bytes remain local/external and are not committed.

Jetta compact JSON gaps are not expanded into synthetic flat candles. RF-008 reconstructs only timestamps explicitly represented by the provider response, preserving the frozen no-forward-fill/no-interpolation rule.

For each frozen `symbol/month`, BID and ASK are an atomic source pair. Both sides must use the same source encoding/path class (`JETTA_JSON` or legacy `BI5`). A partial cache may be completed only if the second side is obtained from the same format; otherwise RF-008 falls back to a coherent pair from the alternate Dukascopy path. Mixed `JETTA_JSON + BI5` BID/ASK pairs are prohibited.

## Source encoding and price scaling

Jetta compact JSON carries its own positive price `multiplier`, which is applied exactly to its delta-encoded OHLC columns. Legacy BI5 uses the frozen point divisor below.

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

All normalized prices must be finite and positive. Source-format validation is applied according to the provider encoding contract rather than by imposing one generic OHLC geometry rule across BI5 and Jetta.

RF-008 diagnostic evidence showed that Dukascopy/Jetta H1 BID and ASK candles are side-specific aggregates. Component-wise `ASK >= BID` is therefore **not** a valid invariant for separately aggregated OHLC extrema: the BID high/low and ASK high/low can represent different intra-hour quote events. RF-008 must not reject, clip or synthesize spread merely because corresponding OHLC extrema cross after separate aggregation.

This correction does not relax source coherence: BID and ASK must still use the same source format for a given `symbol/month`, have aligned H1 event timestamps, and pass independent OHLC validity checks. Any later execution calculation must consume the appropriate quote side explicitly rather than treating aggregated BID/ASK extrema as synchronous executable quotes.

For `JETTA_JSON`, compact integer-delta OHLC fields are reconstructed exactly and preserved as provided by the provider encoding. Cache-wide diagnostics over the currently acquired pre-protected cache found rare internal geometry discrepancies in encoded units, but the provider-native Jetta consumer reconstructs those fields without an OHLC-ordering rejection. Therefore Jetta high/low geometry discrepancy is diagnostic-only in RF-008 and is not a blocking condition by itself.

RF-008 still blocks malformed Jetta payloads, non-finite/non-positive prices, invalid time deltas, duplicate/out-of-order timestamps and timestamp/source-format incoherence. Reconstructed Jetta values must never be clipped, reordered, spread-repaired, interpolated or forward-filled. Legacy `BI5` OHLC geometry validation remains strict.

Source-format-specific validation is performed during source decoding. Quote normalization is limited to DIRECT/INVERSE mapping plus finite/positive output checks and must not impose a stricter generic OHLC rule downstream.

## Time and quality contract

- timezone: `UTC`;
- event time: H1 bar open;
- availability time: event time plus one hour;
- market-hour calendar: existing regression-tested Dukascopy FX DST/weekend rule;
- ordering: event time first, then frozen currency order;
- no forward fill or interpolation.

Duplicates, out-of-order BI5/JSON records, malformed compact JSON, non-finite/non-positive prices, strict BI5 OHLC violations, mixed source formats within a BID/ASK month-pair, one-sided BID/ASK availability and BID/ASK timestamp mismatch are blocking. Jetta internal high/low geometry discrepancies are reported diagnostically rather than used as an invented ATS rejection threshold. Missing expected market hours on both sides are reported rather than filled.

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
