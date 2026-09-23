# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: отклонена на R3.
- Strategy #2: отклонена на R3.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Verified RF-001 closure

OWNER launcher PASS was confirmed on exact commit:

`7d8f0638cd3e11d1eab0e5de37201d73c5a1f2d5`

Evidence included pinned Ruff lint/format, pytest collection `141 tests`, full pytest `141 passed`, full Local CI, current task PASS and launcher PASS.

Canonical last completed artifact:

`governance/program/STRATEGY_3_SOURCING_REBASELINE.md`

## RF-002 Strategy #3 idea sourcing

Current task:

`ATS2-RF-002 — Strategy #3 idea sourcing`

Canonical next artifact:

`governance/program/STRATEGY_3_IDEA_SOURCING.md`

Shortlisted families:

- `S3-FAM-01` macroeconomic announcement response;
- `S3-FAM-02` cross-sectional currency momentum;
- `S3-FAM-03` intraday time/session effect.

Order-flow prediction is retained as a fourth research-relevant family but is not immediately shortlisted because a reproducible data path is not yet established.

No family is selected or ranked in RF-002.

Development parameter tuning is allowed before confirmatory freeze if the search space and all materially inspected variants are retained. Revealed confirmatory data cannot be tuned against and still remain independent evidence for the same claim.

Run `ATS_TASK_CHECK.bat` and return `reports/local_ci/CURRENT_TASK_REPORT.txt`.

After exact-head PASS:

`ATS2-RF-003 — Strategy #3 family selection and Idea intake`.
