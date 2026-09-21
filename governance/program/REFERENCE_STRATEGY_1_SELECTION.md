# Reference Strategy #1 Selection

**Task:** `ATS2-M3-001`  
**Work package:** `WBS-3.1`  
**Decision:** `SELECT`  
**Date:** 21 September 2026

## 1. Purpose

This decision selects the **strategy class** that will be used as ATS Reference Strategy #1 for the first real vertical pass through the Research Funnel and the M2 platform.

Selection is not evidence of edge, profitability, validation, live readiness or capital suitability.

## 2. Selected strategy class

**Selected class:** `SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT`

Human-readable description:

**Single-instrument 1H long/flat trend-following / breakout.**

The class boundary is:

- one instrument at a time;
- one deterministic 1-hour bar stream;
- price/OHLC-driven trend or breakout logic;
- long/flat state only for the first reference implementation;
- signal uses only completed 1H-bar information;
- any resulting action may occur no earlier than the next information-available execution point;
- a position is **not** forced to close at the end of the day and may span multiple 1H bars or multiple calendar days until an explicit exit signal occurs;
- no short sale, borrow, leverage, funding-rate, portfolio-allocation or multi-asset requirement is part of the first reference class.

No numeric lookback, threshold, stop, holding period, position size or cost value is selected by this decision.

## 3. Why this class is selected

### Platform fit

The class maps directly onto the M2 Reference Consumer Profile:

`ordered 1H bars → deterministic research state → decision intent → replay → explicit costs → analytics/result`.

The existing platform already consumes a finite deterministically ordered event stream, so 1H does not require a different engine from the M2 baseline.

### Data feasibility

Current public data paths explicitly support hourly bars.

Binance Public Data documents `1h` as a supported kline interval, publishes spot archive files in daily/monthly form and provides checksum files. Its examples include monthly `1h` kline downloads.

Alpha Vantage documents `60min` as a supported intraday interval. Exact entitlement, history depth and suitability still depend on the future selected instrument.

These observations establish **candidate data availability only**. This decision does not choose Binance, Alpha Vantage or any other vendor.

### Execution clarity

A completed 1H-bar signal with earliest-next-available action has a clean information boundary:

1. the 1H bar closes;
2. the completed bar becomes available;
3. strategy state and signal are updated;
4. simulated execution is evaluated only after that information point.

The 1H interval provides more decision observations than a daily interval while remaining far less dependent on sub-minute microstructure than lower-frequency intraday strategies.

### Holding-period semantics

The `1H` label describes the **decision interval**, not a forced trade duration.

The position may remain open:

- for a few hours;
- across multiple sessions/days;
- until the future hypothesis/specification emits a defined exit signal.

M3-001 intentionally does not prescribe a fixed number of bars or a mandatory end-of-day flat rule.

### Research precedent

Time-series momentum/trend-following is a well-studied research class. Moskowitz, Ooi and Pedersen documented time-series momentum across liquid futures markets, and later historical work studied trend following over much longer samples.

Those publications are **research provenance**, not evidence that the ATS implementation, a future selected instrument or any parameterization will be profitable.

## 4. Alternatives considered

| Strategy class | M3-001 disposition | Main reason |
|---|---|---|
| Single-instrument 1H trend-following / breakout | **SELECT** | Fits current ordered-stream platform, gives more observations than daily bars, and keeps timing/execution assumptions auditable |
| Single-instrument daily trend-following / breakout | DEFER | Even simpler timing, but fewer observations for the first vertical research loop; retained as a possible later comparison |
| Single-instrument 1H mean reversion | DEFER | More sensitive to entry-price/fill assumptions and cost/turnover effects for the first reference line |
| Sub-hour intraday momentum or mean reversion | DEFER | Requires stronger microstructure and higher-resolution execution assumptions |
| Cross-sectional momentum / relative strength | DEFER | Requires multi-instrument universe construction, synchronization and survivorship controls |
| Event/news strategy | DEFER | Requires additional event ingestion and decision-time timestamp semantics not needed for the first platform consumer |

Deferred classes are not rejected as research ideas. They are simply not the first Reference Strategy consumer.

## 5. Deliberately unresolved fields

The following are **not selected in M3-001**:

- market / asset class;
- exact instrument;
- venue;
- data vendor;
- historical period;
- timezone and exact 1H bar-boundary convention;
- exact trend/breakout definition;
- entry/exit lookbacks;
- fixed or variable holding-period rule;
- position sizing;
- stop logic;
- fee/spread/slippage values;
- capital, leverage or risk limits;
- broker or live execution platform.

These are resolved only by later Idea/Hypothesis, Data Feasibility, protocol and lifecycle steps with explicit evidence.

## 6. Data-source observations for the next stage

Current source observations to be verified during Data Feasibility:

- Binance Public Data: public spot/futures archive, `1h` klines supported, daily/monthly files and checksum support; spot timestamps from 2025 onward are documented in microseconds.
- Alpha Vantage: documented intraday intervals include `60min`; exact entitlement/history availability must be checked for the chosen instrument and use case.

The future Dataset Manifest must freeze the actual source/snapshot, timestamp semantics, coverage and integrity reference. No source is approved merely by appearing in this selection note.

## 7. Research integrity

The selection was made before running a backtest for Reference Strategy #1.

No parameter search, instrument ranking or result comparison was used to choose the selected class.

Before M3-001 closure, OWNER changed the selected decision interval from daily bars to 1H bars. This revision occurred before any Reference Strategy backtest, Idea/Hypothesis result or Experiment observation.

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

`SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT`

Next work package:

`ATS2-M3-002 — Idea & rationale`

Work package:

`WBS-3.2`

Immediate next artifact:

`research/ideas/IDEA-0001.md`

M3-002 must register the first real Idea and formulate the corresponding falsifiable Hypothesis without using a profitable backtest as the rationale.
