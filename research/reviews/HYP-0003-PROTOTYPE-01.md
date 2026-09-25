# Cheap Prototype Record — HYP-0003 / PROTO-01

## Identity

- Hypothesis ID: `HYP-0003`
- Data Feasibility review: `research/reviews/HYP-0003-DATA-FEASIBILITY.md`
- Prototype sequence: `PROTO-01`
- Created on: `2026-09-25`
- Status: `FROZEN_PRE_REVEAL`

## Prototype question

On the exact frozen HYP-0003 development dataset, does the complete predeclared 25-cell cross-sectional currency-momentum grid satisfy the HYP-0003 broad-region rule under quote-executable after-spread / before-financing measurement?

PROTO-01 evaluates all `25 / 25` declared combinations:

- formation months: `1, 3, 6, 9, 12`;
- holding months: `1, 3, 6, 9, 12`.

No cell may be omitted, added, retuned or relabeled after reveal.

## Expected direction / form

Inherited from `HYP-0003`.

The broad-region claim passes only if all three pre-written conditions hold:

1. median of the 25 cell mean winner-minus-loser returns is `> 0`;
2. at least `13 / 25` cell mean returns are `> 0`;
3. positive-mean cells span at least `3 / 5` distinct formation periods and at least `3 / 5` distinct holding periods.

A single favorable cell cannot rescue failure of the breadth rule.

## Frozen data and scope

Dataset:

`DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001@1.0.0`

Manifest:

`data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001.yaml`

Prepared CSV:

`data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv`

Prepared CSV SHA-256:

`8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2`

Source bundle SHA-256:

`9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a`

Coverage:

`2003-08-03T21:00:00Z <= event_time < 2021-09-01T00:00:00Z`

Protected tail beginning `2021-09-01T00:00:00Z` is unavailable to this runner.

The frozen source universe remains:

`AUD, CAD, CHF, EUR, GBP, JPY, NOK, NZD, SEK`

## Ranking and formation calculation

For source month `M`, define:

- current cutoff = the last expected Dukascopy FX market-hour H1 open in `M`;
- ranking anchor = first calendar instant of month `M+1`;
- cutoff information availability = current cutoff plus one hour.

For formation length `f`, a currency is ranking-eligible only if its exact current cutoff bar and the exact cutoff bar of source month `M-f` both exist.

Formation return uses normalized quote mid-closes:

`MID_CLOSE = (BID_CLOSE + ASK_CLOSE) / 2`

`FORMATION_RETURN = CURRENT_MID_CLOSE / START_MID_CLOSE - 1`

The cross-section must contain at least six eligible currencies.

Rank strongest to weakest by formation return with currency code as the deterministic ascending tie-break.

Basket size is frozen as:

`basket_size = max(1, ceil(eligible_currency_count / 6))`

The strongest `basket_size` currencies are winners and the weakest `basket_size` currencies are losers.

## Entry, holding and executable return

The portfolio entry timestamp is the first expected FX H1 market-hour open at or after current-cutoff availability.

For holding length `h`, the holding calendar anchor is the ranking anchor shifted forward `h` calendar months. The portfolio exit timestamp is the first expected FX H1 market-hour open at or after that anchor.

Entry and exit timestamps are global for the monthly portfolio, not chosen separately from each currency's observed data.

After rank/basket selection, every selected member must have exact rows at both entry and exit timestamps. If any selected winner or loser is missing either required row, that entire monthly portfolio observation for the cell is ineligible. No lower-ranked replacement currency is substituted.

Winner long signed return:

`exit_bid_open / entry_ask_open - 1`

Loser short signed return:

`entry_bid_open / exit_ask_open - 1`

Monthly winner-minus-loser portfolio return:

`mean(winner_long_returns) + mean(loser_short_returns)`

This is the operational side-aware executable version of long winners / short losers.

## Missing-data and anti-leakage rules

- Ranking eligibility uses only current and historical cutoff information.
- Future entry/exit availability never changes ranking membership.
- Missing execution data after selection drops the whole monthly cell observation; it never causes basket substitution.
- No stale cutoff bar may replace the exact expected cutoff.
- No interpolation or forward fill is allowed.
- No protected-tail row may be read.
- All 25 variants use the same rules.

## Cost / execution approximation

- Spread: represented directly by BID/ASK entry and exit sides.
- Commission: not modeled.
- Financing/rollover: not modeled and materially relevant for multi-month holds.
- Slippage/live fill realism: not modeled.
- H1 bar opens are quote observations, not guaranteed live fills.

Every result is labeled:

`QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING`

No economic-profitability claim is authorized from PROTO-01 alone.

## Planned per-cell metrics

For every one of the 25 cells report:

1. formation months;
2. holding months;
3. valid monthly portfolio observation count;
4. mean winner-minus-loser return;
5. median winner-minus-loser return;
6. positive-return share;
7. overlapping holding-window count/share;
8. mean membership-turnover share across consecutive valid portfolio observations;
9. minimum and maximum ranking-eligible currency count.

Membership turnover is the average of winner-side and loser-side equal-weight replacement fractions between consecutive valid observations. It is a structural turnover diagnostic, not a commission estimate.

Holding-window overlap is counted when a portfolio entry occurs before the running maximum exit timestamp of earlier valid observations for that cell.

## Breadth summary

The result must report:

- median of all 25 cell mean returns;
- count of positive-mean cells;
- distinct formation periods represented by positive-mean cells;
- distinct holding periods represented by positive-mean cells;
- Boolean status of each of the three HYP-0003 breadth criteria.

No best-cell ranking or automatic winner selection is produced.

## Pre-run decision rule

`PARK`:

- one or more of the 25 cells has zero valid monthly portfolio observations, so the complete frozen grid cannot answer the broad-region question.

`REJECT`:

- all 25 cells have at least one valid observation and one or more of the three HYP-0003 breadth criteria fail.

`ADVANCE_TO_ECONOMIC_SCREEN`:

- all 25 cells have at least one valid observation and all three breadth criteria pass.

HYP-0003 adds a stricter mandatory routing rule to the standard R3 outcome vocabulary: even if PROTO-01 returns `ADVANCE_TO_ECONOMIC_SCREEN`, ATS must first create a new fixed confirmatory Hypothesis ID and test it on a previously unseen block. HYP-0003 itself may not enter R4 Economic Pre-Screen directly from the development surface.

`ITERATE` is reserved only for a correctable data/implementation defect identified before a valid interpretable reveal. It is not available to rescue an unfavorable breadth result.

## Implementation references

- Frozen runner: `tools/hyp0003_proto01.py`
- Synthetic contract tests: `tests/test_hyp0003_proto01.py`
- Local result: `reports/local_ci/HYP0003_PROTO01_RESULT.json`
- Local result report: `reports/local_ci/HYP0003_PROTO01_RESULT_REPORT.txt`
- Future canonical result: `reports/research/HYP-0003-PROTOTYPE-01-result.json`

RF-010 freezes these artifacts and must not execute the runner against the frozen development CSV.

RF-011 is the separate reveal task.

## Search and iteration accounting

- Prototype iterations inspected before reveal: `0 results`
- Declared parameter variants: `25`
- Markets/universe inspected: `1 frozen nine-currency FX universe`
- Material data-source changes after RF-009 freeze: `0`
- Hidden or discarded variants: `0`

## Result summary

`PENDING_RF011_REVEAL`

## Data / implementation anomalies

`NONE_REVEALED — runner has not been executed on the frozen development dataset`

## Interpretation

No HYP-0003 development outcome is known at RF-010 freeze.

## Outcome

- Decision: `PENDING_RF011_REVEAL`
- Reason: `PROTO01_FROZEN_NOT_EXECUTED`
- Resulting action: execute the exact frozen runner once under RF-011 after exact-head OWNER PASS.

## Evidence classification

- Evidence class after reveal: `EXPLORATORY_PROTOTYPE`
- Registered Experiment ID: `NOT_APPLICABLE`
