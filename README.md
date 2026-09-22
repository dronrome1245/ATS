# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

ATS — Strategy Factory для воспроизводимого исследования алгоритмических торговых систем.

## Текущее состояние

- M0–M3: `COMPLETED / PASS`
- M4 reusable validation baseline WBS-4.1…4.8: `COMPLETED`
- M4.9/M4.10: blocked until an eligible S05 PASS Candidate
- M6 Reference Strategy #2 lane: `IN_PROGRESS`

Reference Strategy #1 remains:

`HYP-0001 / PROTO-01 = REJECT`

## Current work

`ATS2-M6-001 — First bounded discovery run`

Frozen manifest:

`research/discovery/SEARCH-EURUSD-H1-2021-2025-001.yaml`

Runner:

`tools/discover_eurusd_h1.py`

The search evaluates the complete 16-alternative development-only set. Any shortlist remains exploratory and must enter the normal Idea/Hypothesis funnel before stronger research claims.

## Current execution

Run:

`ATS_TASK_CHECK.bat`

Then return:

`reports/local_ci/CURRENT_TASK_REPORT.txt`
