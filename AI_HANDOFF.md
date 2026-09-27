# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: `REJECTED_AT_R3`.
- Strategy #2: `REJECTED_AT_R3`.
- Strategy #3 / HYP-0003: `REJECTED_AT_R3`.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Verified RF-018 closure

OWNER `ATS_TASK_CHECK.bat` PASS was confirmed on exact main commit:

`6d388c500d2c5e1671e11700966b713b95a395b8`

Canonical last completed artifact:

`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001.yaml`

RF-018 froze:

- `DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001@1.0.0`;
- `112900` rows;
- `111938` exact-next-hour eligible rows;
- derived SHA-256 `3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6`;
- `H1_OPEN_PROXY_AT_EVENT_TIME`;
- exact tick boundary time unknown;
- `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

## RF-019 HYP-0004 PROTO-01 freeze

Current task:

`ATS2-RF-019 — HYP-0004 PROTO-01 freeze`

Canonical prototype artifact:

`research/reviews/HYP-0004-PROTOTYPE-01.md`

Frozen runner:

`tools/hyp0004_proto01.py`

Synthetic contract tests:

`tests/test_hyp0004_proto01.py`

Runner Git blob:

`a42da4454249cf124e7664e1efc3632efcad002d`

The prototype decision requires both:

`median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)`

and:

`median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)`

`TRANSITION` is reporting-only.

A positive structural result is routed to:

`CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4`

A failed primary inequality routes to:

`STOP_HYP0004`

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

RF-019 freezes code and decision logic but does not run the development dataset.

After exact-main RF-019 PASS:

`ATS2-RF-020 — HYP-0004 PROTO-01 reveal`

may execute the exact frozen runner once.
