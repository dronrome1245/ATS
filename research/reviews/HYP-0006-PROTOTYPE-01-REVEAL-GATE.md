# HYP-0006 PROTO-01 — First Development Reveal Gate

Task: `ATS2-RF-030`
Research step: `17/22 — one first predeclared development reveal`
Parent lineage: `IDEA-0005 / HYP-0006 / PROTO-01`
Status: `STAGED_REVEAL_NOT_EXECUTED`

## Boundary and original freeze

RF-029 exact-main success was confirmed on commit:
`94df9ede91522f473872b25a6d8023fd64182878`.

The complete pre-outcome PROTO-01 contract was frozen in:
`research/reviews/HYP-0006-PROTOTYPE-01.md`.

The frozen runner is exactly:
`tools/hyp0006_proto01.py`

Its Git blob must stay:
`6afb870c035bc5ae76f773784a5fa3db15d680fd`.

It is **forbidden** to edit or replace the frozen runner as part of RF-030,
or to execute it during RF-030 agent preflight. Its explicit
`--execute-first-reveal` invocation is authorized **only** by the
later exact-main RF-030 completion launcher after a successful exact-head
agent preflight and squash merge.

Information boundary before that exact-main first invocation:
`NO_HYPOTHESIS_OUTCOME_COMPUTED`.

## Exact frozen dataset and permitted observations

- `DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001@1.0.0`
- `FX_SPOT_OTC / EURUSD`
- Frozen BLS U.S. scheduled CPI publication timestamps
- Development interval: `2003-08-03T21:00:00Z` through exclusive `2021-09-01T00:00:00Z`
- Raw quote source: `DUKASCOPY_HOURLY_TICK_BI5`, offline and hash-frozen
- BLS annual schedule snapshots: 19
- Required raw BI5 hourly objects: 1085; all must be checked by SHA-256 locally
- 217 candidate CPI events
- 216 eligible CPI event IDs in exact frozen RF-028 JSON order
- 1 excluded CPI event `BLS-CPI-20030815`, solely on frozen
  `POST_60_ANCHOR_GAP_EXCEEDS_30000MS` / 60047 ms
- Every selected time anchor obeys frozen 30,000 ms tolerances,
  strict pre-release rule, tie previous and same-record BID/ASK pairing
- All HYP-0005 protected/unseen segments remain off-limits

Previous RF-028 exact-main commit:
`e7f05a0d237c4d78a8a0edb93710619e6ad2ba00`.

Exact RF-028 JSON SHA-256:
`1b575682b959070f4a0981b7cd13d70626f1e169d221d0c9fb2383fc679fd5fb`.

RF-027 exact-main:
`bbbdbd301b610dfc61316c9ff82015fb0e039a47`.

Frozen source-bundle SHA-256:
`5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425`.

Frozen geometry CSV SHA-256:
`e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034`.

## Primary hypothesis, predetermined before any market values

For each eligible event with publication time t, compute:

`mid = (bid + ask) / 2`

`pre_abs_60m_return = abs(mid_pre_release / mid_pre_60 - 1)`

`post_abs_60m_return = abs(mid_post_60 / mid_pre_release - 1)`

On all 216 paired observations, evaluate exactly one inequality:

`median(post_abs_60m_return) > median(pre_abs_60m_return)`

If the inequality is false: `REJECT / STOP_HYP0006`.

If true: `ADVANCE_TO_ECONOMIC_SCREEN` as an exploratory structural
label only; mandatory routing is
`CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4`.

This does **not** establish a directional entry, net edge, trading strategy,
P&L, or independent evidence. No post-reveal modifications to universe,
time boundaries, price/anchor selection, return formulas, metrics,
decision criterion or runner are authorized.

## Controlled one-shot sequence

1. OWNER executes `.\ATS_AGENT_PREFLIGHT.bat` on exact RF-030 agent HEAD.
   It runs synthetic tests but **no reveal**.
2. Only on exact agent preflight PASS does GPT squash-merge the PR.
3. OWNER updates to exact merged `main` and executes
   `.\ATS_TASK_CHECK.bat` exactly once.
4. The exact-main task checker first verifies:
   clean working tree, canonical contract/lineage, frozen runner Git blob,
   full Local CI, exact RF-027/RF-028 local result identities, and
   hash of **every one of 1085** frozen local BI5 objects.
5. Only after all prechecks PASS and absent existing reveal artifacts,
   the task checker invokes the **unchanged** frozen runner once:
   `tools/hyp0006_proto01.py --execute-first-reveal`.
6. Preserve all 216 event results, summary medians, spread/year diagnostics,
   primary inequality decision, exact commit and result SHA-256.
7. If result artifacts already exist for the same exact commit,
   **validate the existing pair only**, do not rerun/reveal again.
   Partial, mismatched, corrupt or stale artifacts are a stop, not a reason
   for silent deletion or repeated execution.
8. Source/metadata/runner failure is a technical blocker and **never**
   a negative finding about HYP-0006.

Expected local outputs:
`reports/local_ci/HYP0006_PROTO01_RESULT.json`
`reports/local_ci/HYP0006_PROTO01_RESULT_REPORT.txt`
`reports/local_ci/CURRENT_TASK_REPORT.txt`

RF-030 completion is only after exact-main
`ATS CURRENT TASK CHECK: PASS` and `ATS TASK LAUNCHER: PASS` and
a review of the emitted result. The one-time result is
`DEVELOPMENT_REVEALED_EXPLORATORY_ONLY`, not protected or independent.

No next Technical ID or irreversible post-reveal adjustment is authorized
until this gate completes and the result is retained, including negative findings.
