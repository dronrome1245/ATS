# HYP-0005 Confirmatory Data Feasibility Preparation

Task: `ATS2-RF-023`  
Work package: `WBS-RF.2`  
Hypothesis ID: `HYP-0005`  
Status: `PREPARATION_PROTOCOL_FROZEN`  
Date: 28 September 2026

## Purpose

Prepare machine evidence for the HYP-0005 confirmatory Data Feasibility decision without computing any HYP-0005 outcome metric.

RF-023 is a preparation task. RF-024 will canonicalize the preparation result, create the formal Data Feasibility review and freeze the exact confirmatory dataset identity if the preparation result permits it.

## Why RF-023 is split from the freeze

The exact source-object hashes, prepared-data hash, row geometry and source snapshot can only be established on the OWNER machine after acquiring the source bytes.

Therefore RF-023 follows the established ATS preparation/freeze pattern:

`protocol + acquisition tool → exact-main machine preparation → canonical freeze task`

No Data Feasibility decision is represented as frozen until RF-024 consumes the exact RF-023 local result.

## Consumed EUR/USD project interval

Project research has already consumed EUR/USD data continuously across:

`2003-08-03T21:00:00Z <= event_time < 2026-09-01T00:00:00Z`

This union is formed by prior ATS development/confirmatory work, including HYP-0004 development and the later EUR/USD blocks used by earlier hypotheses.

RF-023 must not reuse this interval as unseen HYP-0005 confirmatory evidence.

## Frozen unseen coverage rule

RF-023 uses all mechanically identified Dukascopy EUR/USD H1 history that is outside the consumed interval and available under the following two pre-result segments:

### LEFT_UNSEEN

`2003-05-04T21:00:00Z <= event_time < 2003-08-03T21:00:00Z`

The start is the canonical Dukascopy EURUSD H1 history-start timestamp already recorded by ATS source metadata.

The end is exactly the HYP-0004 development start.

### RIGHT_UNSEEN

`2026-09-01T00:00:00Z <= event_time < 2026-09-26T00:00:00Z`

The start is exactly after the latest previously consumed EUR/USD block.

The end is the start of the last fully completed UTC Saturday before RF-023 preparation was defined. This avoids a partial current trading week and is fixed before RF-023 source acquisition.

The two segments are selected by project information boundaries and calendar completeness, not by HYP-0005 outcomes.

No other historical subperiod is searched.

## Source

Provider/source family:

`Dukascopy EURUSD H1 BID + ASK historical candles`

Source symbol:

`EURUSD`

Orientation:

`DIRECT`

Source months implied by the frozen segments:

- 2003-05
- 2003-06
- 2003-07
- 2003-08
- 2026-09

Expected coherent source objects:

`5 months × 2 sides = 10 objects`

The preparation tool may use the established coherent Jetta JSON path or the established legacy BI5 fallback, but BID and ASK for one month must come from one coherent source format.

## Frozen timing semantics

Research boundary:

`H1_OPEN_PROXY_AT_EVENT_TIME`

For every retained row:

- `event_time` = H1 bar-open timestamp;
- `availability_time = event_time` for the boundary-open proxy;
- `source_bar_completion_time = event_time + 1 hour`;
- exact tick boundary time known = `false`.

This remains an H1 open proxy, not proof of an executable tick exactly at the clock boundary.

## Frozen bucket mapping

- `CORE_ACTIVE`: UTC 07–16
- `TRANSITION`: UTC 17–20
- `OFF_HOURS`: UTC 21–23 and 00–06

The preparation may assign the frozen bucket label because it depends only on event time.

## Permitted preparation calculations

RF-023 may calculate only data-feasibility quantities:

- source-object identities and SHA-256 hashes;
- source-bundle SHA-256;
- exact retained row count;
- source/derived coverage;
- expected and missing market-hour counts;
- exact-next-hour eligibility geometry;
- counts by frozen UTC bucket;
- counts by frozen confirmatory segment;
- duplicate/order/quote-coherence checks;
- prepared CSV SHA-256.

These quantities may determine whether the dataset is mechanically usable.

## Prohibited calculations

RF-023 must not calculate or report:

- `relative_spread` values or medians;
- `abs_next_1h_return` values or medians;
- movement inequality result;
- spread inequality result;
- combined HYP-0005 primary result;
- favorable-year selection;
- alternate UTC windows;
- alternate horizons;
- directional P&L or trading-rule metrics.

Information boundary:

`NO_CONFIRMATORY_OUTCOME_COMPUTED`

## Prepared dataset candidate

Dataset candidate ID:

`DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0`

Local prepared CSV:

`data/derived/HYP-0005-CONF-01-EURUSD-H1.csv`

The CSV must contain only:

- event time;
- boundary availability time;
- source-bar completion time;
- deterministic sequence;
- confirmatory segment;
- source symbol;
- BID open;
- ASK open;
- frozen UTC bucket.

It must not contain HYP-0005 outcome columns.

## Local outputs

Tool:

`tools/hyp0005_data_feasibility.py`

Tests:

`tests/test_hyp0005_data_feasibility.py`

Local-only machine result:

`reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP.json`

Shareable local summary:

`reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP_REPORT.txt`

Both local reports and the prepared CSV remain ignored by Git.

## Preparation decisions

`READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE`

requires:

- coherent BID/ASK source acquisition;
- no overlap with the consumed project interval;
- at least one exact-next-hour eligible observation in both frozen unseen segments;
- non-zero exact-next-hour eligible `CORE_ACTIVE` and `OFF_HOURS` geometry;
- deterministic source/data hashes;
- no HYP-0005 outcome calculation.

`INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY`

is a valid data-feasibility result if the frozen unseen segments cannot provide the minimum mechanical geometry above.

Technical download/decode/integrity failure is not reclassified as an unfavorable research result.

## Observed source-availability blocker

On 28 September 2026, the exact-main RF-023 preparation reached source acquisition without computing any HYP-0005 outcome.

A targeted OWNER diagnostic then established:

- the Jetta September 2026 EUR/USD BID request returned HTTP 400 with `From time is too late`;
- the Jetta September 2026 EUR/USD ASK request returned the same source-side rejection;
- the Jetta August 2026 BID and ASK control requests both returned HTTP 200;
- BI5 September requests were unavailable with HTTP 503 during the same diagnostic;
- no HYP-0005 outcome field was requested or computed.

This is a source-availability blocker, not `INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY` and not a HYP-0005 research result.

The frozen `LEFT_UNSEEN`, `RIGHT_UNSEEN`, provider family, bucket mapping and decision rules are unchanged. RF-023 must not replace September with a previously consumed block or select another period after this availability observation.

The next permitted action is to retry the same frozen RF-023 acquisition only after a coherent September 2026 BID/ASK source pair becomes available. Month-end is an earliest sensible retry point, not a guarantee of provider publication.

Information boundary remains:

`NO_CONFIRMATORY_OUTCOME_COMPUTED`

## Next task

After RF-023 exact-main OWNER PASS and upload of the exact local machine result:

`ATS2-RF-024 — HYP-0005 confirmatory Data Feasibility freeze`

RF-024 will either freeze the exact prepared dataset/review under the preparation decision or route the line according to Data Feasibility methodology.

No HYP-0005 prototype runner may be frozen or executed before RF-024 exact-main PASS.
