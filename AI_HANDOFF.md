# ATS AI Handoff

## Current program state

- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- M2: `COMPLETED / PASS`.
- M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6 Reference Strategy #2 lane: `IN_PROGRESS`.
- HYP-0001 / PROTO-01: `REJECTED_AT_R3`.
- No Candidate/Strategy/live permission exists.

## Verified M6-000 closure

OWNER launcher PASS was confirmed on exact commit:

`d5a7e8c60cfacf3fd0ff19dee6f2ebd0c672dba9`

Evidence included repository validator PASS, pinned Ruff lint/format PASS, `133 passed`, full Local CI PASS, M6-000 task check PASS and launcher PASS.

Canonical last completed artifact:

`governance/methodology/templates/discovery/SEARCH_MANIFEST_TEMPLATE.yaml`

## M6-001 First bounded discovery run

Frozen Search Manifest:

`research/discovery/SEARCH-EURUSD-H1-2021-2025-001.yaml`

The run is development-only and uses the already known 2021–2025 EURUSD H1 dataset. It evaluates 16 predeclared return-tail continuation/reversal alternatives across 6H/24H lookbacks and 6H/24H forward horizons.

The entire dataset is development-known for this research lane. It cannot become protected independent evidence for a pattern sourced by this search.

Runner:

`tools/discover_eurusd_h1.py`

The runner verifies the frozen implementation revision and dataset identity, writes the full result to ignored local reports and emits only exploratory shortlist outcomes.

## Current execution

Current task:

`ATS2-M6-001 — First bounded discovery run`

Canonical next artifact:

`research/discovery/SEARCH-EURUSD-H1-2021-2025-001.yaml`

Run:

`ATS_TASK_CHECK.bat`

Then return:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

No Strategy #2 selection occurs until the discovery result is reviewed.
