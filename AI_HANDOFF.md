# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: rejected at R3.
- Strategy #2: rejected at R3.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Verified RF-008 closure

OWNER `ATS_TASK_CHECK.bat` PASS was confirmed on exact main commit:

`63e1bc9c7e1ba2e001ecdd9918244d83db0e58c3`

Canonical last completed artifact:

`research/reviews/HYP-0003-DEVELOPMENT-DATA-PREP.md`

RF-008 completed all `217` source months and acquired `3906 / 3906` expected Dukascopy H1 BID/ASK source objects with `0` missing. The preparation decision was `READY_FOR_DEVELOPMENT_DATA_FREEZE`.

Frozen RF-008 evidence to canonicalize in RF-009:

- dataset: `DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001@1.0.0`;
- prepared rows: `1,014,509`;
- prepared CSV SHA-256: `8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2`;
- source bundle SHA-256: `9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a`;
- common usable interval: `2003-08-03T21:00:00Z` through `2021-08-31T23:00:00Z`;
- monthly ranking points with at least six currencies: `207`;
- longest declared 12/12 geometry points: `184`;
- protected-tail source objects requested: `0`;
- information boundary: `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

## RF-009 HYP-0003 development data freeze

Current task:

`ATS2-RF-009 — HYP-0003 development data freeze`

Canonical next artifact:

`data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001.yaml`

RF-009 creates the canonical RF-008 result, Dataset Manifest/schema and Data Feasibility freeze update. It verifies the local prepared CSV against the exact RF-008 SHA and does not rerun acquisition or calculate any HYP-0003 momentum outcome.

Protected tail at or after `2021-09-01T00:00:00Z` remains prohibited.

Run `ATS_TASK_CHECK.bat` and return `reports/local_ci/CURRENT_TASK_REPORT.txt`.
