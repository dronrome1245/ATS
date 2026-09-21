# Reference Strategy #1 Selection

**Task:** `ATS2-M3-001`  
**Work package:** `WBS-3.1`  
**Decision:** `SELECT`  
**Date:** 21 September 2026

## 1. Purpose

This decision selects the **strategy class** that will be used as ATS Reference Strategy #1 for the first real vertical pass through the Research Funnel and the M2 platform.

Selection is not evidence of edge, profitability, validation, live readiness or capital suitability.

## 2. Selected strategy class

**Selected class:** `SINGLE_INSTRUMENT_DAILY_LONG_FLAT_TREND_BREAKOUT`

Human-readable description:

**Single-instrument daily long/flat trend-following / breakout.**

The class boundary is:

- one instrument at a time;
- one deterministic daily-bar stream;
- price/OHLC-driven trend or breakout logic;
- long/flat state only for the first reference implementation;
- signal uses only completed-bar information;
- any resulting action may occur no earlier than the next information-available execution point;
- no short sale, borrow, leverage, funding-rate, portfolio-allocation or multi-asset requirement is part of the first reference class.

No numeric lookback, threshold, stop, holding period, position size or cost value is selected by this decision.

## 3. Why this class is selected

### Platform fit

The class maps directly onto the M2 Reference Consumer Profile:

`ordered bars → deterministic research state → decision intent → replay → explicit costs → analytics/result`.

It does not require a new event engine, order-book model, news pipeline, multi-stream join or portfolio layer merely to answer the first research question.

### Data feasibility

Daily OHLC-like data is available from multiple current data paths.

One practical example is Binance Public Data, which publishes public spot market files in daily/monthly archives and provides checksum files. This demonstrates that a reproducible frozen data path can exist for a spot-market implementation without requiring a live broker connection.

Alpha Vantage documents daily time-series APIs across equities and FX/crypto categories, showing another possible data path, although exact history/access terms differ by endpoint.

These observations establish **candidate data availability only**. This decision does not choose Binance, Alpha Vantage or any other vendor.

### Execution clarity

A daily completed-bar signal with earliest-next-bar action has a clean information boundary:

1. bar closes;
2. the completed bar becomes available;
3. strategy state and signal are updated;
4. simulated execution is evaluated only after that information point.

This is materially easier to audit than intraday microstructure-dependent logic.

### Research precedent

Time-series momentum/trend-following is a well-studied research class. Moskowitz, Ooi and Pedersen documented time-series momentum across liquid futures markets, and later historical work studied trend following over much longer samples.

Those publications are **research provenance**, not evidence that the ATS implementation, a future selected instrument or any parameterization will be profitable.

## 4. Alternatives considered

| Strategy class | M3-001 disposition | Main reason |
|---|---|---|
| Single-instrument daily trend-following / breakout | **SELECT** | Minimal data surface, deterministic timing, low infrastructure burden, clear falsification path |
| Single-instrument daily mean reversion | DEFER | More sensitive to entry-price/fill assumptions and typically higher turnover/cost sensitivity for a first vertical test |
| Intraday momentum or mean reversion | DEFER | Requires materially stronger intraday data, session and microstructure handling |
| Cross-sectional momentum / relative strength | DEFER | Requires multi-instrument universe construction, synchronization and survivorship controls |
| Event/news strategy | DEFER | Requires additional event ingestion and decision-time timestamp semantics not needed for the first platform consumer |

Deferred classes are not rejected as research ideas. They are simply worse first consumers for the current platform milestone.

## 5. Deliberately unresolved fields

The following are **not selected in M3-001**:

- market / asset class;
- exact instrument;
- venue;
- data vendor;
- historical period;
- timezone/bar-boundary convention;
- exact trend/breakout definition;
- entry/exit lookbacks;
- position sizing;
- stop logic;
- fee/spread/slippage values;
- capital, leverage or risk limits;
- broker or live execution platform.

These are resolved only by the later Idea/Hypothesis, Data Feasibility, protocol and lifecycle steps with explicit evidence.

## 6. Data-source observations for the next stage

Current source observations to be verified during Data Feasibility:

- Binance Public Data: public spot/futures archive, daily/monthly files, checksum support; spot timestamps from 2025 onward are documented in microseconds.
- Alpha Vantage: documented daily time-series interfaces for equities and FX/crypto; exact entitlement/history availability must be checked for the chosen instrument and use case.

The future Dataset Manifest must freeze the actual source/snapshot, timestamp semantics, coverage and integrity reference. No source is approved merely by appearing in this selection note.

## 7. Research integrity

The selection was made before running a backtest for Reference Strategy #1.

No parameter search, instrument ranking or result comparison was used to choose the selected class.

The first real Idea/Hypothesis must therefore begin from the class-level rationale above rather than from a discovered profitable parameter set.

## 8. Safety boundary

This selection does not authorize:

- demo/shadow trading;
- real-money trading;
- capital allocation;
- leverage;
- Strategy Risk Mandate;
- broker/account selection;
- scaling.

All existing live/capital safety flags remain unchanged.

## 9. External references

Research provenance:

- Moskowitz, Ooi, Pedersen, **Time Series Momentum**, Journal of Financial Economics, 2012: https://doi.org/10.1016/j.jfineco.2011.11.003
- Hurst, Ooi, Pedersen, **A Century of Evidence on Trend-Following Investing**: https://www.aqr.com/insights/research/journal-article/a-century-of-evidence-on-trend-following-investing

Data-path observations:

- Binance Public Data: https://github.com/binance/binance-public-data
- Alpha Vantage API documentation: https://www.alphavantage.co/documentation/

## 10. Decision and next step

`ATS2-M3-001 = DONE`.

Reference Strategy #1 class is:

`SINGLE_INSTRUMENT_DAILY_LONG_FLAT_TREND_BREAKOUT`

Next work package:

`ATS2-M3-002 — Idea & rationale`

Work package:

`WBS-3.2`

Immediate next artifact:

`research/ideas/IDEA-0001.md`

M3-002 must register the first real Idea and formulate the corresponding falsifiable Hypothesis without using a profitable backtest as the rationale.
