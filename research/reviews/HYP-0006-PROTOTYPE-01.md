# HYP-0006 / PROTO-01 — Pre-Reveal Prototype Freeze

Task: `ATS2-RF-029`
Research step: `16/22 — freeze the first structural prototype before reveal`
Parent: `IDEA-0005 / HYP-0006`
Evidence classification: `DEVELOPMENT / EXPLORATORY ONLY`
Status: `STAGED_PRE_REVEAL`
Information boundary: `NO_HYPOTHESIS_OUTCOME_COMPUTED`

## Purpose / one question

On the **exact 216 eligible scheduled U.S. CPI events** mechanically identified before
performance inspection, does EUR/USD have a larger **median absolute** 60-minute
movement after CPI publication than during the immediately preceding 60 minutes?

This is one nondirectional structural question, **not** a trading strategy or P&L test.

Frozen primary inequality, inherited from HYP-0006:

`median(post_abs_60m_return) > median(pre_abs_60m_return)`

No minimum effect threshold, alternative horizon, CPI category, instrument, direction,
favorable event subset or year may be selected after market-result inspection.

## Lineage and exact immutable inputs

Completed RF-028 exact-main and full local launcher PASS:

`e7f05a0d237c4d78a8a0edb93710619e6ad2ba00`

RF-028 local machine result:

`reports/local_ci/HYP0006_DATA_TOLERANCE_FREEZE.json`

Exact file SHA-256 (raw bytes):

`1b575682b959070f4a0981b7cd13d70626f1e169d221d0c9fb2383fc679fd5fb`

RF-027 exact-main PASS commit:

`bbbdbd301b610dfc61316c9ff82015fb0e039a47`

RF-027 local result:

`reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP.json`

Frozen dataset:

`DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001@1.0.0`

- Market: `FX_SPOT_OTC`
- Instrument: `EURUSD`
- Event class: scheduled U.S. CPI publications, official BLS frozen local annual schedules
- Event timestamp: frozen BLS Eastern-time-to-UTC publication schedule
- Development interval: `2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z`
- Raw quote source: `DUKASCOPY_HOURLY_TICK_BI5`, canonical local BI5 snapshots
- BLS snapshots: `19`
- Source BI5 objects: `1085 / 1085`, zero missing
- Candidate CPI events: `217`
- Eligible CPI events: **216**, exact ordered IDs from RF-028 result
- Ineligible: **1** — `BLS-CPI-20030815`
- Exclusion reason: `POST_60_ANCHOR_GAP_EXCEEDS_30000MS`, nearest gap **60,047 ms**
- Denominator rule: `216 + 1 = 217`
- Protected HYP-0005 source requests: `0`

Frozen source bundle SHA-256:

`5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425`

Frozen timestamp geometry CSV:

`data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv`

Frozen geometry SHA-256:

`e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034`

Frozen BLS manifest SHA-256:

`3837c463b36914c2276e9985a8a70a8ead13ca0e4b16901a22cb4fd2dece6ee4`

Frozen BLS snapshot bundle SHA-256:

`5306799d4c4196941d701e661df2fa4255682783b966e7bcfd69f702a1ead341`

Frozen BLS CPI calendar SHA-256:

`646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9`

A candidate is never discarded based on future EUR/USD price movement. The one
exclusion is the already-frozen RF-028 timestamp-geometry result, not a performance filter.

## Three required synchronized BID/ASK quote anchors

For each eligible event with public release timestamp `t`:

1. `PRE_60_ANCHOR`: nearest tick timestamp to `t - 60 minutes`; maximum
   **30,000 ms** absolute gap; equal gap selects the **previous** timestamp.
2. `PRE_RELEASE_ANCHOR`: last quote strictly before `t`; maximum
   **30,000 ms** staleness; quote at/after `t` is forbidden.
3. `POST_60_ANCHOR`: nearest tick timestamp to `t + 60 minutes`; maximum
   **30,000 ms** absolute gap; equal gap selects the **previous** timestamp.

For every selected millisecond, choose:

`LAST_RAW_RECORD_AT_SELECTED_MILLISECOND`

For each anchor, BID and ASK are extracted from the **same**
Dukascopy `>IIIff` raw tick record; price divisor `100000`. Crossed/invalid quotes
and data gaps fail closed. No interpolation, forward fill, synthetic spread repair,
alternative vendor, event replacement or network requests.

Selected anchor sides and gaps **must match** the pre-outcome
`geometry_evaluations` frozen by RF-028, or the prototype fails without a reveal.
Missing/changed local BI5 objects are source integrity blockers, not negative market results.

## Frozen calculations

For each selected anchor, using the same-record BID/ASK:

`mid = (bid + ask) / 2`

`pre_abs_60m_return = abs(mid_pre_release / mid_pre_60 - 1)`

`post_abs_60m_return = abs(mid_post_60 / mid_pre_release - 1)`

`relative_spread = (ask - bid) / mid`

Each eligible event contributes exactly one pre value and one post value.
Neither direction, sign, event weight nor extra return horizon is part of the
primary comparison.

Primary metrics are the **separate medians** of the complete 216-element
pre and post absolute-return distributions. They are compared using exact
unrounded values; no post-result exception or magnitude threshold is permitted.

## Mandatory non-decision diagnostics

Preserve and report all 216 event identities and both individual absolute
returns. Report:

- median quoted relative spread at the strictly pre-release tick;
- median quoted relative spread at the **first observed tick at or after t**,
  using the last raw record at the selected millisecond;
- calendar-year event count, eligible-denominator share, pre and post median
  absolute returns; maximum one-year share;
- same-time BLS publication labels/flags and flagged event count.

The first post-release quote is **diagnostic only**. Its absence does not
remove the event, and no extra performance-conditioned selection is permitted.
Same-time release clusters stay in the primary denominator:
`FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION`.

These diagnostics cannot rescue a failed primary inequality or establish
executable trade profitability.

## Exact pre-written decision rule

`REJECT / STOP_HYP0006` if:

`median(post_abs_60m_return) <= median(pre_abs_60m_return)`

`ADVANCE_TO_ECONOMIC_SCREEN` if and only if:

`median(post_abs_60m_return) > median(pre_abs_60m_return)`

However this is a **structural, nondirectional** result; a positive result is
development evidence only, **not automatic R4 admission**. The mandatory next action is:

`CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4`

The label preserves ordinary prototype vocabulary without asserting a trading
signal, cost-adjusted performance or validated edge.

Any source/contract failure before a valid result is a technical blocker,
not a primary-claim REJECT, and cannot authorize changes to frozen data/rules.

## Implementation and reveal separation

Frozen prospective runner:

`tools/hyp0006_proto01.py`

Runner Git blob at initial staging:

`6afb870c035bc5ae76f773784a5fa3db15d680fd`

Synthetic-only tests:

`tests/test_hyp0006_proto01.py`

Expected future local reveal result:

`reports/local_ci/HYP0006_PROTO01_RESULT.json`

Expected future shareable result:

`reports/local_ci/HYP0006_PROTO01_RESULT_REPORT.txt`

RF-029 **must not execute real-data prototype calculations**. Its current-task
gate may only check lineage, hashes, contracts, runner blob and synthetic tests.
The runner's default CLI invocation returns `REVEAL_BLOCKED_PRE_FREEZE` and does not
load price records; an explicit `--execute-first-reveal` is reserved for a
**separate later authorized exact-main reveal gate**.

Do not manually launch the runner with reveal mode in RF-029.

## Immutability, evidence, search accounting

Frozen BEFORE first HYP-0006 market outcome: event universe, eligible ordered IDs,
source/geometry hashes, source semantics, 60-minute horizons, 30,000 ms tolerances,
anchor-selection tie-breaks, duplicate handling, quote pairing, calculations,
diagnostics, decision rule and prospective runner blob.

After reveal, do not alter this contract and present a repeat as the first reveal.
Negative outcomes are retained. HYP-0005 confirmatory blocks remain protected.
No protected/independent data are promoted to independent HYP-0006 evidence.
No Candidate, Strategy Version, trading P&L or capital decision is created here.

**RF-029 completion requires exact-head preflight, squash merge, and exact-main
`ATS CURRENT TASK CHECK: PASS` + `ATS TASK LAUNCHER: PASS` without market reveal.**
