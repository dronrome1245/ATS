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

## Verified RF-016 closure

OWNER `ATS_TASK_CHECK.bat` PASS was confirmed on exact main commit:

`3628010fc04045de040794c482e57ccd2639f99b`

Canonical last completed artifact:

`research/reviews/HYP-0004-DATA-FEASIBILITY.md`

RF-016 recorded `CONDITIONAL` feasibility with `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

## RF-017 HYP-0004 development data preparation

Current task:

`ATS2-RF-017 — HYP-0004 development data preparation`

Canonical next artifact:

`research/reviews/HYP-0004-DEVELOPMENT-DATA-PREP.md`

Canonical tool:

`tools/hyp0004_development_data.py`

Synthetic tests:

`tests/test_hyp0004_development_data.py`

RF-017 verifies the frozen HYP-0003 parent dataset SHA-256, filters only the preselected EUR/USD rows, validates exact UTC hour semantics and paired `bid_open/ask_open`, assigns the fixed UTC buckets, and counts exact-next-hour data geometry.

Planned derived dataset:

`DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001`

Local path:

`data/derived/HYP-0004-DEV-01-EURUSD-H1.csv`

Runtime result:

`reports/local_ci/HYP0004_DEVELOPMENT_DATA.json`

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

RF-017 does not calculate absolute-return or relative-spread distributions and does not evaluate either primary HYP-0004 inequality.

After exact-main RF-017 PASS:

`ATS2-RF-018 — HYP-0004 development data freeze`

must canonicalize the local preparation result before prototype work.
