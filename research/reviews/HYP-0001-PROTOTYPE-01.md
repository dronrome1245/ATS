# Cheap Prototype Record — HYP-0001 / PROTO-01

## Identity

- Hypothesis ID: `HYP-0001`
- Data Feasibility review: `research/reviews/HYP-0001-DATA_FEASIBILITY.md`
- Prototype sequence: `PROTO-01`
- Created on: `2026-09-21`
- Status: `COMPLETED / REJECT`

## Prototype question

Does the fixed EUR/USD 1H 24-bar upward-breakout condition produce a positive average executable long return over the next 24 contiguous market hours, and is that average higher than the ordinary 24-hour executable EUR/USD return over the same frozen dataset?

PROTO-01 does not search for a better lookback, holding period, market or direction.

## Expected direction / form

Inherited from `HYP-0001`:

`mean(signal executable 24-bar return) > 0`

and:

`mean(signal executable 24-bar return) > mean(unconditional executable 24-bar return)`

The 24-bar lookback and 24-bar forward horizon are fixed before any result is seen.

## Data and scope

- Data source: Dukascopy EUR/USD historical 1H BID + ASK candle files.
- Observation period fixed before result: `2021-01-01T00:00:00Z <= bar_open < 2026-01-01T00:00:00Z`.
- Five complete calendar years are used so the period is not chosen after seeing performance.
- Data snapshot reference: `data/manifests/DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml`.
- Preparation command: `uv run --frozen python tools/proto01_eurusd.py prepare`.
- Shareable preparation report: `reports/local_ci/PROTO01_DATA_REPORT.txt`.
- Prepared rows: `31,296`.
- Missing expected tradable hours: `0`.
- Prepared CSV SHA-256: `aeda05d90994259a22e25d882398218aead968941fe0b1c73eb34894841291c0`.
- Source bundle SHA-256: `cf378faaae58424112d289315b2ec076f4100775f2613a5d2d685ec46a02aba4`.
- Eligible 24-before / 24-after timestamps before signal filtering: `18,485`.

Before calculation may run, all requested BID/ASK files must download, receive SHA-256 fingerprints, align exactly by timestamp, contain no duplicates, and produce a deterministic prepared CSV. Missing hours are not filled. Weekend/session gaps break the required 24-hour window.

Raw Dukascopy files and prepared market-data CSV remain local and are not committed to Git.

## Transformation / feature summary

Preparation is deterministic:

1. download monthly `BID_candles_hour_1.bi5` and `ASK_candles_hour_1.bi5`;
2. decompress and decode each 1H candle;
3. convert timestamps to UTC;
4. align BID and ASK by exact hourly timestamp;
5. reject duplicates and impossible OHLC values;
6. keep only 2021-01-01 through 2025-12-31;
7. write one ordered CSV with BID/ASK OHLC and bar availability time.

## Minimal baseline implementation

For each timestamp with a complete contiguous window:

1. breakout = current completed BID close is above the highest BID high of the previous 24 completed bars;
2. entry = ASK open of the next hour;
3. exit/valuation = BID open 24 contiguous hours after entry;
4. executable return = `exit_bid / entry_ask - 1`;
5. unconditional baseline = the same return for every eligible timestamp without the breakout filter.

No same-close entry is permitted.

## Cost / execution approximation

- Spread: included through ASK entry and BID exit.
- Commission: not included.
- Financing/rollover: not included.
- Slippage/latency: not available from 1H candles.

Every result must be labeled:

`QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING`

PROTO-01 is not a full net-profit test and not a live execution simulation.

## Planned metrics

Primary:

1. aligned 1H bars;
2. eligible 24-before / 24-after timestamps;
3. breakout signal count;
4. mean executable 24-bar signal return;
5. mean unconditional executable 24-bar return;
6. signal mean minus baseline mean.

Context:

- median signal return;
- positive-return share;
- overlapping signal-window count/share;
- detected data-gap count.

## Pre-run decision rule

Fixed before result:

- `ADVANCE_TO_ECONOMIC_SCREEN`: at least 100 valid breakout observations, signal mean > 0, signal mean > baseline, and no blocking defect.
- `REJECT`: at least 100 valid observations and either primary inequality fails.
- `PARK`: fewer than 100 valid breakout observations.
- `ITERATE`: only for a correctable data/implementation defect; never for tuning an unfavorable result.

The 100-observation rule is a minimum descriptive sample for this cheap prototype, not a statistical-significance threshold.

## Implementation references

- Tool: `tools/proto01_eurusd.py`
- Local prepared CSV: `data/derived/HYP-0001-PROTO-01-EURUSD-H1.csv`
- Future Dataset Manifest: `data/manifests/DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml`
- Preparation report: `reports/local_ci/PROTO01_DATA_REPORT.txt`
- Future machine result: `reports/research/HYP-0001-PROTOTYPE-01-result.json`
- Future result report: `reports/local_ci/PROTO01_RESULT_REPORT.txt`

## Result summary

PROTO-01 was run once on the frozen 2021–2025 dataset.

Primary results:

- valid breakout signals: `1006`;
- mean executable 24-bar return after breakout: `-0.0002301573` (about `-0.0230%`);
- unconditional executable 24-bar mean: `-0.0000647136` (about `-0.0065%`);
- signal minus baseline: `-0.0001654436` (about `-0.0165%`);
- median signal return: `-0.0004042483` (about `-0.0404%`);
- positive-return share: `45.8250%`;
- overlapping signal windows: `723 / 1006` (`71.87%`).

The sample-count condition was satisfied, but both primary inequalities failed: signal mean was below zero and below the unconditional baseline.

## Data / implementation anomalies

No blocking data or implementation anomaly was reported by the fixed run. The high overlap between signal forward windows is retained as a dependence limitation.

## Search and iteration accounting

- Prototype iterations inspected so far: `1`
- Parameter / variant count: `1 fixed rule`
- Markets / instruments: `1 — EURUSD`
- Material data-source changes: `0`

## Interpretation

No interpretation yet.

## Outcome

- Decision: `REJECT`
- Reason: `ONE_OR_BOTH_PRIMARY_HYPOTHESIS_INEQUALITIES_FAILED`
- Resulting action: stop this HYP-0001 research line before Economic Pre-Screen. Retain the negative result and do not change lookback, horizon, instrument or period inside HYP-0001 to rescue it.

## Evidence classification

- Evidence class: `EXPLORATORY_PROTOTYPE`
- Registered Experiment ID: `NOT_APPLICABLE`
