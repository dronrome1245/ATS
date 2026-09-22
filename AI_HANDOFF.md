# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6 Reference Strategy #2 lane: `IN_PROGRESS`.
- HYP-0001 / PROTO-01: `REJECTED_AT_R3`.
- No Candidate/Strategy Version/live permission exists.

## Verified M6-003 closure

OWNER launcher PASS was confirmed on exact commit `84aff042c7d57a0e001c35a5a75d29369f983e60` with repository validator PASS, pinned Ruff PASS, `138 passed`, full Local CI PASS, task check PASS and launcher PASS.

Canonical last completed artifact:

`research/hypotheses/HYP-0002.md`

## M6-004 HYP-0002 Data Feasibility preparation

Canonical preparation artifact:

`research/reviews/HYP-0002-DATA-FEASIBILITY-PREP.md`

Tool:

`tools/hyp0002_data_feasibility.py`

Frozen information boundary:

- development calibration remains the canonical 2021–2025 EURUSD H1 snapshot;
- the tool computes development-only `Q10_DEV` and `Q90_DEV`;
- confirmatory source is Dukascopy EURUSD 1H BID/ASK;
- confirmatory period is 2026-01-01 through 2026-08-31 UTC;
- preparation records hashes/coverage only;
- `NO_HYPOTHESIS_OUTCOME_COMPUTED` prohibits HYP-0002 result calculation.

## Current closure check

Current task: `ATS2-M6-004 — HYP-0002 Data Feasibility preparation`

Canonical next artifact: `research/reviews/HYP-0002-DATA-FEASIBILITY-PREP.md`

Run `ATS_TASK_CHECK.bat` and return `reports/local_ci/CURRENT_TASK_REPORT.txt`.

The report will contain Q10_DEV/Q90_DEV plus confirmatory hashes/coverage. Do not run a HYP-0002 outcome calculation before the formal Data Feasibility review is committed.
