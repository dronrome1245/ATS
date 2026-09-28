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

## Current stage

`Research Factory → Strategy #4 → HYP-0005 → Data Feasibility preparation → ATS2-RF-023`

## Canonical last completed artifact

`research/hypotheses/HYP-0005.md`

## Verified RF-022 closure

OWNER `ATS_TASK_CHECK.bat` PASS was confirmed on exact main commit:

`136b62b52922abc1556396377c6cd6fca88fba75`

HYP-0005 is now the active confirmatory structural Hypothesis.

## RF-023 preparation contract

Current task:

`ATS2-RF-023 — HYP-0005 confirmatory Data Feasibility preparation`

Protocol:

`research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md`

Tool:

`tools/hyp0005_data_feasibility.py`

Tests:

`tests/test_hyp0005_data_feasibility.py`

Dataset candidate:

`DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0`

Prepared local CSV:

`data/derived/HYP-0005-CONF-01-EURUSD-H1.csv`

Frozen unseen segments:

- `LEFT_UNSEEN = [2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)`;
- `RIGHT_UNSEEN = [2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)`.

Consumed project interval excluded from HYP-0005 confirmatory evidence:

`[2003-08-03T21:00:00Z, 2026-09-01T00:00:00Z)`.

Boundary semantics:

`H1_OPEN_PROXY_AT_EVENT_TIME`

Exact tick boundary known:

`false`

RF-023 may prepare source/data identity and geometry only. It may not calculate HYP-0005 spread/return medians or primary inequalities.

Information boundary:

`NO_CONFIRMATORY_OUTCOME_COMPUTED`

After RF-023 exact-main PASS and upload of the exact local machine result:

`ATS2-RF-024 — HYP-0005 confirmatory Data Feasibility freeze`

must canonicalize the exact preparation result and freeze/route the Data Feasibility decision.

Direct R4 remains blocked.
