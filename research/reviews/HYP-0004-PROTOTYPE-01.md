# Cheap Prototype Record — HYP-0004 / PROTO-01

## Identity

- Hypothesis ID: `HYP-0004`
- Data Feasibility review: `research/reviews/HYP-0004-DATA-FEASIBILITY.md`
- Prototype sequence: `PROTO-01`
- Created on: `2026-09-27`
- Status: `FROZEN / NOT_REVEALED`
- Task: `ATS2-RF-019`
- Evidence class after reveal: `EXPLORATORY_PROTOTYPE`

RF-019 freezes the complete prototype contract and implementation before any HYP-0004 development outcome is calculated.

## Prototype question

On the exact frozen HYP-0004 development dataset, do both predeclared HYP-0004 primary inequalities hold under the frozen `H1_OPEN_PROXY_AT_EVENT_TIME` boundary approximation?

The primary inequalities are:

1. `median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)`;
2. `median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)`.

Both must hold.

`TRANSITION` is retained and reported but cannot rescue failure of either primary inequality.

No alternative UTC window, horizon, lag, weekday subset or instrument may be searched inside PROTO-01 after reveal.

## Frozen development dataset

Dataset:

`DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001@1.0.0`

Manifest:

`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001.yaml`

Schema:

`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV.schema.json`

Prepared CSV:

`data/derived/HYP-0004-DEV-01-EURUSD-H1.csv`

Prepared CSV SHA-256:

`3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6`

Frozen row count:

`112900`

Frozen exact-next-hour eligible count:

`111938`

Frozen eligible bucket counts:

- `CORE_ACTIVE = 47012`;
- `TRANSITION = 18189`;
- `OFF_HOURS = 46737`.

Frozen ineligible denominator:

- closed-market next hour: `940`;
- missing expected tradable next hour: `21`;
- right-edge dataset boundary: `1`.

The denominator must reconcile:

`111938 + 940 + 21 + 1 = 112900`

PROTO-01 must fail closed if the dataset hash, row count or geometry differs.

## Boundary and information-time semantics

Boundary availability mode:

`H1_OPEN_PROXY_AT_EVENT_TIME`

Exact tick boundary time known:

`false`

The frozen derived row contains:

- `event_time`;
- `availability_time = event_time`;
- `parent_row_availability_time = event_time + 1 hour`;
- `bid_open`;
- `ask_open`;
- fixed `utc_bucket`.

The H1 open is a development boundary proxy. It is not a claim that an executable tick is observed exactly at the clock boundary.

This timing limitation remains part of every PROTO-01 interpretation.

## Frozen observation eligibility

For a row at `t`, a PROTO-01 observation exists only when:

1. the frozen row at `t` is valid;
2. `t + 1 hour` is an expected Dukascopy FX market hour;
3. the frozen row at exactly `t + 1 hour` exists;
4. no stale, shifted or interpolated replacement is used.

Adjacent eligible intervals may share the boundary row at `t + 1 hour`; no interval itself may span more than the exact declared one-hour horizon.

The runner must reproduce the frozen RF-017 geometry before calculating outcomes.

## Frozen calculations

For every eligible start boundary:

`mid_t = (bid_t + ask_t) / 2`

`relative_spread_t = (ask_t - bid_t) / mid_t`

`mid_t_plus_1h = (bid_t_plus_1h + ask_t_plus_1h) / 2`

`abs_next_1h_return_t = abs(mid_t_plus_1h / mid_t - 1)`

Required quote checks:

- all BID/ASK values finite and positive;
- `ask >= bid`;
- no synthetic spread repair.

No directional return sign is used by the primary claim.

## Planned bucket metrics

For each of `CORE_ACTIVE`, `TRANSITION`, and `OFF_HOURS`, report:

1. eligible observation count;
2. mean `abs_next_1h_return`;
3. median `abs_next_1h_return`;
4. median `relative_spread`.

Only the two medians required by the HYP-0004 primary inequalities determine the prototype decision.

No minimum magnitude threshold is added after reveal.

## Calendar-year diagnostics

For every UTC bucket and represented calendar year, report:

- observation count;
- observation share within that bucket;
- median `abs_next_1h_return`;
- median `relative_spread`.

Also report the maximum single-calendar-year observation share for each bucket.

These are reporting diagnostics only. They do not change the primary decision rule and cannot be used to rescue a failed aggregate claim.

No favorable year may be selected as an alternative sample after reveal.

## Primary summary

The machine result must report exactly three Boolean primary fields:

- `movement_inequality_pass`;
- `spread_inequality_pass`;
- `both_primary_inequalities_pass`.

Definitions:

`movement_inequality_pass = median_core_abs_return > median_off_abs_return`

`spread_inequality_pass = median_core_relative_spread <= median_off_relative_spread`

`both_primary_inequalities_pass = movement_inequality_pass AND spread_inequality_pass`

`TRANSITION` never enters these Boolean calculations.

## Pre-run decision rule

`PARK`:

- `CORE_ACTIVE` or `OFF_HOURS` contains zero eligible observations, so the frozen primary comparison cannot be evaluated.

Reason label:

`PRIMARY_BUCKET_HAS_ZERO_OBSERVATIONS`

`REJECT`:

- both primary buckets contain observations and either predeclared primary inequality fails.

Reason label:

`ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED`

Next action:

`STOP_HYP0004`

`ADVANCE_TO_ECONOMIC_SCREEN`:

- both primary inequalities pass.

Reason label:

`BOTH_PRIMARY_INEQUALITIES_MET`

Because HYP-0004 is a structural, non-directional development claim, this standard R3 vocabulary does not authorize HYP-0004 itself to enter an economic trading screen immediately.

Frozen positive-result next action:

`CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4`

A positive structural result must therefore be followed by a separate fixed research decision before R4. That later object must establish an unseen-data boundary and/or a directional trading claim as appropriate.

`ITERATE` is reserved only for a correctable implementation defect identified before a valid reveal. It is not available to search alternative clock windows after an unfavorable result.

## Cost and execution interpretation

Measurement label:

`STRUCTURAL_H1_OPEN_PROXY_NO_TRADING_PNL`

- Quoted spread is directly measured as the frozen relative BID/ASK spread diagnostic.
- Commission is not part of the primary structural claim.
- Financing is not part of the next-one-hour structural claim.
- Slippage/live fill realism is not modeled.
- No trading P&L, Sharpe ratio, hit rate, position sizing or capital claim is produced.

A larger absolute movement contrast is not itself a tradable edge.

## Implementation references

Frozen runner:

`tools/hyp0004_proto01.py`

Synthetic contract tests:

`tests/test_hyp0004_proto01.py`

Future local result:

`reports/local_ci/HYP0004_PROTO01_RESULT.json`

Future shareable result:

`reports/local_ci/HYP0004_PROTO01_RESULT_REPORT.txt`

Future canonical result after reveal:

`reports/research/HYP-0004-PROTOTYPE-01-result.json`

RF-019 must not execute the frozen development dataset and must not create any of those result files.

## Search and iteration accounting before reveal

- Prototype results inspected: `0`
- Alternative UTC bucket definitions inspected inside PROTO-01: `0`
- Alternative horizons inspected inside PROTO-01: `0`
- Alternative instruments inspected inside PROTO-01: `0`
- Post-freeze data-source changes: `0`
- Hidden/discarded PROTO-01 variants: `0`

## Information boundary

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

RF-019 freezes code and decision logic only.

The runner may be imported by synthetic tests, but `run_result()` must not be executed against the frozen development CSV during RF-019.

## Next task

After exact-main OWNER launcher PASS for RF-019:

`ATS2-RF-020 — HYP-0004 PROTO-01 reveal`

RF-020 may execute the exact frozen runner once after the full Local CI gate passes on the reveal commit.

No runner, metric, decision threshold, bucket definition or dataset identity may change after the first valid reveal merely because the outcome is unattractive.
