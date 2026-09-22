# Cheap Prototype Record — HYP-0002 / PROTO-01

## Identity

- Hypothesis ID: `HYP-0002`
- Data Feasibility review: `research/reviews/HYP-0002-DATA-FEASIBILITY.md`
- Prototype sequence: `PROTO-01`
- Created on: `2026-09-22`
- Status: `FROZEN_NOT_RUN`

## Prototype question

On the frozen 2026-01 through 2026-08 EUR/USD H1 confirmatory dataset, do **both** development-calibrated 24H return-tail reversal sides satisfy both HYP-0002 primary inequalities under the fixed after-spread / before-financing quote-return measurement?

The four required inequalities are:

1. high-tail/DOWN mean signed 24H return `> 0`;
2. high-tail/DOWN mean signed 24H return `>` unconditional DOWN baseline mean;
3. low-tail/UP mean signed 24H return `> 0`;
4. low-tail/UP mean signed 24H return `>` unconditional UP baseline mean.

PROTO-01 does not search alternate thresholds, lookbacks, horizons, sides, markets or periods.

## Expected direction / form

Inherited from `HYP-0002`:

- `R24 >= Q90_DEV` → DOWN reversal;
- `R24 <= Q10_DEV` → UP reversal.

Frozen development thresholds:

- `Q10_DEV = -0.005141454111`
- `Q90_DEV = 0.005394148971`

Both sides are part of one primary claim.

## Data and scope

- Dataset: `DATA-DUKASCOPY-EURUSDH1-HYP0002-001@1.0.0`
- Manifest: `data/manifests/DATA-DUKASCOPY-EURUSDH1-HYP0002-001.yaml`
- Prepared CSV: `data/derived/HYP-0002-CONFIRM-01-EURUSD-H1.csv`
- Prepared CSV SHA-256: `d62a7103478da2a79a0992310005bcd0afc8dc0010088dccd2ed0e54e2ec112f`
- Source bundle SHA-256: `ccbf5ceff1ee1a5a1cb62dead3af531ce05ae4f71e4da32140b526326e686392`
- Observation period: `2026-01-01T00:00:00Z <= event_time < 2026-09-01T00:00:00Z`
- Aligned rows: `4,153`
- Missing expected tradable hours: `0`
- Eligible 24-before/24-after timestamps before tail filtering: `2,414`

Relevant Data Feasibility constraints:

- use only the frozen development thresholds above;
- do not recalibrate from confirmatory data;
- gaps break continuity and are not filled;
- use exact BID/ASK side conventions;
- retain overlap/dependence diagnostics;
- result label is `QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING`;
- no full-net, validation, independent-evidence or live-execution claim is allowed.

## Transformation / feature summary

For every eligible signal timestamp `t`:

`R24(t) = MID_CLOSE(t) / MID_CLOSE(t-24) - 1`

where:

`MID_CLOSE = (BID_CLOSE + ASK_CLOSE) / 2`

A signal is classified only by the frozen thresholds:

- high tail when `R24(t) >= Q90_DEV`;
- low tail when `R24(t) <= Q10_DEV`.

No quantile is estimated from the confirmatory block.

## Minimal baseline implementation

For every eligible timestamp:

- UP signed return = `exit_bid_open / entry_ask_open - 1`;
- DOWN signed return = `entry_bid_open / exit_ask_open - 1`;
- entry = next eligible 1H open after the completed signal bar;
- exit = open 24 contiguous hours after entry.

The unconditional UP and DOWN baselines use the same eligible timestamps and the same side-specific formulas without tail filtering.

High-tail events are evaluated only with DOWN signed returns. Low-tail events are evaluated only with UP signed returns.

## Cost / execution approximation

- Spread: represented directly by BID/ASK entry/exit sides.
- Commission: not included.
- Financing/rollover: not included.
- Slippage/latency: not available from 1H quote bars.

Every result must be labeled:

`QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING`

## Planned metrics

For each tail side:

1. event count;
2. mean signed 24H return;
3. median signed 24H return;
4. positive-return share;
5. unconditional same-direction mean;
6. event mean minus unconditional baseline;
7. overlapping event-window count/share.

Shared context:

- aligned rows;
- eligible 24-before/24-after timestamps;
- exact dataset identity/hash;
- exact frozen thresholds.

No significance threshold is introduced at R3.

## Pre-run decision rule

Frozen before result:

- `ADVANCE_TO_ECONOMIC_SCREEN`: both tail sides have at least one valid event, all four primary inequalities pass, and no blocking data/implementation defect is present.
- `REJECT`: both tail sides have at least one valid event and one or more of the four primary inequalities fail.
- `PARK`: either tail side has zero valid events, so the two-sided claim cannot be answered on the frozen block.
- `ITERATE`: only for a correctable data/implementation defect discovered before a valid interpretable outcome; never for tuning an unfavorable result.

If one side fails while the other passes, the result is `REJECT` for HYP-0002. A one-sided follow-up requires a new Hypothesis ID.

## Implementation references

- Frozen runner: `tools/hyp0002_proto01.py`
- Synthetic contract tests: `tests/test_hyp0002_proto01.py`
- Local prepared CSV: `data/derived/HYP-0002-CONFIRM-01-EURUSD-H1.csv`
- Future local machine result: `reports/local_ci/HYP0002_PROTO01_RESULT.json`
- Future local result report: `reports/local_ci/HYP0002_PROTO01_RESULT_REPORT.txt`
- Future canonical machine result after review: `reports/research/HYP-0002-PROTOTYPE-01-result.json`

The current M6-006 closure does **not** execute the frozen runner.

## Result summary

`NOT_RUN`

No confirmatory outcome has been calculated at this freeze point.

## Data / implementation anomalies

None observed at freeze time. Any later runtime defect must be repaired without changing the frozen research question, thresholds, period or decision rule.

## Search and iteration accounting

- Prototype iterations inspected so far: `0 results`
- Parameter / variant count in this iteration: `1 fixed two-sided rule`
- Markets / instruments inspected: `1 — EURUSD`
- Material data-source changes: `0`
- Prior discovery alternatives already inspected before HYP-0002: `16`

## Interpretation

Not applicable before execution.

## Outcome

- Decision: `NOT_RUN`
- Reason: `PROTOCOL_FROZEN_BEFORE_CONFIRMATORY_REVEAL`
- Resulting action: after exact-head OWNER launcher PASS, run the frozen PROTO-01 once on the frozen dataset.

## Evidence classification

- Evidence class: `EXPLORATORY_PROTOTYPE`
- Registered Experiment ID: `NOT_APPLICABLE`
