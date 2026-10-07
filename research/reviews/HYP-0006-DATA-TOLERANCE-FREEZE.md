# HYP-0006 Pre-Reveal Data / Tolerance Freeze

Task: `ATS2-RF-028`  
Hypothesis ID: `HYP-0006`  
Research step: `15/22 — зафиксировать конкретные данные и временные допуски`  
Status: `STAGED_PRE_REVEAL_FREEZE`

## 1. Purpose

RF-028 freezes the exact HYP-0006 development source identities, event inventory rule, anchor
selection rules and numeric timestamp tolerances before any HYP-0006 market outcome is calculated.

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

RF-028 must not calculate:

- `pre_abs_60m_return`;
- `post_abs_60m_return`;
- either distribution median;
- the primary inequality;
- directional event returns;
- trading P&L.

## 2. RF-027 exact-main evidence admitted into the freeze

RF-027 exact-main completion commit:

`bbbdbd301b610dfc61316c9ff82015fb0e039a47`

RF-027 decision:

`READY_FOR_DATA_FEASIBILITY_FREEZE`

Frozen evidence class:

`DEVELOPMENT_EXPLORATORY_ONLY`

Development interval:

`2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z`

Exact source/event identities:

- event inventory source: `BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS`;
- event-time semantics: `BLS_ANNUAL_SCHEDULE_US_EASTERN`;
- quote source: `DUKASCOPY_HOURLY_TICK_BI5`;
- BLS snapshots: `19`;
- candidate CPI events: `217`;
- resolved CPI event times: `217`;
- complete timestamp-geometry events: `217`;
- required/acquired BI5 objects: `1085 / 1085`;
- missing BI5 objects: `0`;
- HYP-0005 protected source requests: `0`.

Frozen hashes:

- BLS snapshot manifest SHA-256:
  `3837c463b36914c2276e9985a8a70a8ead13ca0e4b16901a22cb4fd2dece6ee4`;
- BLS snapshot bundle SHA-256:
  `5306799d4c4196941d701e661df2fa4255682783b966e7bcfd69f702a1ead341`;
- BLS calendar CSV SHA-256:
  `646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9`;
- full source bundle SHA-256:
  `5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425`;
- timestamp geometry CSV SHA-256:
  `e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034`.

Planned frozen development dataset identity:

`DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001@1.0.0`

## 3. Frozen anchor definitions

For each candidate event with official public release time `t`:

### PRE_60_ANCHOR

Target:

`t - 60 minutes`

Selection:

1. identify the previous-or-equal and next-or-equal Dukascopy tick timestamps around the target;
2. choose the timestamp with the smaller absolute gap to the target;
3. if the two gaps are equal, choose the previous timestamp;
4. require selected absolute gap `<= 30,000 ms`.

Frozen rule:

`NEAREST_TO_T_MINUS_60M_WITHIN_30000MS_TIE_PREVIOUS`

### PRE_RELEASE_ANCHOR

Selection:

1. choose the last Dukascopy tick timestamp strictly before `t`;
2. require staleness `<= 30,000 ms`;
3. a quote at or after `t` is prohibited.

Frozen rule:

`LAST_QUOTE_STRICTLY_BEFORE_RELEASE_MAX_STALENESS_30000MS`

### POST_60_ANCHOR

Target:

`t + 60 minutes`

Selection:

1. identify the previous-or-equal and next-or-equal Dukascopy tick timestamps around the target;
2. choose the timestamp with the smaller absolute gap to the target;
3. if the two gaps are equal, choose the previous timestamp;
4. require selected absolute gap `<= 30,000 ms`.

Frozen rule:

`NEAREST_TO_T_PLUS_60M_WITHIN_30000MS_TIE_PREVIOUS`

## 4. Frozen quote-row tie-break

If multiple raw Dukascopy records share the selected millisecond timestamp:

`LAST_RAW_RECORD_AT_SELECTED_MILLISECOND`

BID and ASK must come from the same raw `>IIIff` tick record.

Frozen pairing rule:

`BID_AND_ASK_FROM_SAME_RAW_TICK_RECORD`

No side mixing, interpolation, forward fill or synthetic spread repair is allowed.

## 5. Frozen event eligibility

An event is eligible only when all three required anchors satisfy the frozen rules above.

If any anchor fails:

`EXCLUDE_EVENT_IF_ANY_REQUIRED_ANCHOR_FAILS_FROZEN_GAP_RULE`

The exclusion is a data-feasibility consequence only. No event may be excluded based on future
return size, direction, spread attractiveness or whether it supports the hypothesis.

The exact eligible denominator is produced mechanically by the RF-028 runner from the hash-frozen
RF-027 geometry CSV. It is not selected manually.

Same-time BLS policy remains:

`FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION`

## 6. Why 30 seconds is frozen now

The tolerance is fixed before outcome inspection and applies symmetrically to the `t-60m` and
`t+60m` anchors. Thirty seconds is less than one percent of the 60-minute horizon and prevents a
materially stale timestamp from silently representing an hourly endpoint.

The same 30-second cap on the strictly pre-release anchor prevents an old quote from being treated
as the immediate pre-publication state while preserving the rule that the release tick itself may
never enter the pre-event anchor.

RF-028 does not change this tolerance based on HYP-0006 returns because those returns are not
available to RF-028.

## 7. RF-028 deterministic runner

Tool:

`tools/hyp0006_data_tolerance_freeze.py`

Synthetic tests:

`tests/test_hyp0006_data_tolerance_freeze.py`

The runner reads only:

- the exact local RF-027 machine result;
- the hash-frozen RF-027 timestamp-geometry CSV.

It does not load BID/ASK price values and cannot calculate the HYP-0006 outcome.

Local result:

`reports/local_ci/HYP0006_DATA_TOLERANCE_FREEZE.json`

Local shareable report:

`reports/local_ci/HYP0006_DATA_TOLERANCE_FREEZE_REPORT.txt`

Valid positive decision:

`FREEZE_DATA_AND_TOLERANCES`

Blocking decision:

`INSUFFICIENT_ANCHOR_GEOMETRY_UNDER_FROZEN_TOLERANCES`

## 8. Post-freeze immutability

After the first HYP-0006 market reveal, the following may not be changed and retested as the same
first reveal:

- event source or event-time semantics;
- quote provider/source bundle;
- development interval;
- CPI event class;
- 60-minute horizons;
- anchor selection side/tie-break;
- `30,000 ms` boundary tolerance;
- `30,000 ms` pre-release staleness limit;
- duplicate timestamp tie-break;
- BID/ASK same-record pairing;
- same-time event policy;
- missing-data exclusion rule;
- eligible event denominator emitted by RF-028;
- source/data hashes.

Any material change after reveal requires a new research attempt and cannot retroactively replace
the first reveal.

## 9. Current gate

Run RF-028 only after exact-head preflight and merge to exact main.

The RF-028 exact-main run may inspect timestamp geometry only.

Information boundary remains:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`
