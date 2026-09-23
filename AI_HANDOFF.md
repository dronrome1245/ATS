# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: отклонена на R3.
- Strategy #2: отклонена на R3.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Verified RF-007 closure

OWNER launcher PASS was confirmed on exact commit:

`21942dccc1985bfc422579c185e9836610627b8b`

Evidence included pinned Ruff lint/format, pytest collection `149 tests`, full pytest `149 passed`, canonical RF-006 result validation, full Local CI, current task PASS and launcher PASS.

Canonical last completed artifact:

`research/reviews/HYP-0003-DATA-FEASIBILITY.md`

RF-007 froze all nine source-qualified currencies, common possible development start `2003-08-03T21:00:00Z`, and the pre-protected development-data acquisition/normalization/quality contract.

Data Feasibility remains `CONDITIONAL` and information boundary remains `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

## RF-008 HYP-0003 development data preparation

Current task:

`ATS2-RF-008 — HYP-0003 development data preparation`

Canonical next artifact:

`research/reviews/HYP-0003-DEVELOPMENT-DATA-PREP.md`

Runner:

`tools/hyp0003_development_data.py`

RF-008 attempts `217` source months × `9` source pairs × `2` sides = `3906` Dukascopy monthly H1 source objects. Acquisition is resumable from local frozen source files.

Local outputs:

- `data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv`;
- `reports/local_ci/HYP0003_DEVELOPMENT_DATA.json`;
- `reports/local_ci/HYP0003_DEVELOPMENT_DATA_REPORT.txt`.

RF-008 records source/data hashes, coverage, missing-market-hour and monthly-cutoff eligibility statistics. It does not calculate formation returns, ranks, baskets, holding returns or any HYP-0003 cell.

Protected-tail months at or after `2021-09-01T00:00:00Z` are prohibited.

Run `ATS_TASK_CHECK.bat` and return `reports/local_ci/CURRENT_TASK_REPORT.txt`.

After exact-head PASS and report review:

`ATS2-RF-009 — HYP-0003 development data freeze`.
