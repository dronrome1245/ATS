# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: отклонена на R3.
- Strategy #2: отклонена на R3.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Verified RF-005 closure

OWNER launcher PASS was confirmed on exact commit:

`859f31be6df087095b58aa993e7e3e1787c4b172`

Evidence included pinned Ruff lint/format, pytest collection `141 tests`, full pytest `141 passed`, full Local CI, current task PASS and launcher PASS.

Canonical last completed artifact:

`research/reviews/HYP-0003-DATA-FEASIBILITY.md`

## RF-006 HYP-0003 Data Feasibility preparation

Current task:

`ATS2-RF-006 — HYP-0003 Data Feasibility preparation`

Canonical next artifact:

`research/reviews/HYP-0003-DATA-FEASIBILITY-PREP.md`

Tool:

`tools/hyp0003_data_feasibility.py`

The tool probes all nine predeclared source pairs, finds first two-sided monthly H1 availability, verifies August 2021 availability, validates BI5 structure and records SHA-256 probe identities.

It does not decode price levels for strategy research, rank currencies, calculate momentum, form winner/loser baskets or evaluate any of the 25 HYP-0003 cells.

Protected-tail months at or after `2021-09-01T00:00:00Z` are not downloaded by RF-006.

Local outputs:

- `reports/local_ci/HYP0003_DATA_FEASIBILITY.json`
- `reports/local_ci/HYP0003_DATA_FEASIBILITY_REPORT.txt`

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

Run `ATS_TASK_CHECK.bat` and return `reports/local_ci/CURRENT_TASK_REPORT.txt`.

After exact-head PASS and report review:

`ATS2-RF-007 — HYP-0003 Data Feasibility freeze`.
