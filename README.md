# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

ATS — Strategy Factory для воспроизводимого исследования алгоритмических торговых систем.

## Текущее состояние

- M0: `COMPLETED / PASS`
- M1: `COMPLETED / PASS`
- M2: `COMPLETED / PASS`
- M3: `COMPLETED / PASS`
- M4 reusable validation baseline WBS-4.1…4.8: `COMPLETED`
- M4 strategy-specific WBS-4.9/WBS-4.10: blocked until an eligible S05 PASS Candidate
- M6 Reference Strategy #2 lane: `IN_PROGRESS`

Reference Strategy #1 remains:

`HYP-0001 / PROTO-01 = REJECT`

## Current work

`ATS2-M6-000 — Market Pattern Discovery`

Core artifacts:

- `governance/methodology/MARKET_PATTERN_DISCOVERY.md`
- `governance/methodology/templates/discovery/SEARCH_MANIFEST_TEMPLATE.yaml`
- `src/ats/discovery/bounded.py`
- `tests/test_discovery_bounded.py`

Discovery is exploratory hypothesis generation. It preserves the full declared alternative set and cannot directly create validation evidence.

## Current closure check

Run:

`ATS_TASK_CHECK.bat`

Then return:

`reports/local_ci/CURRENT_TASK_REPORT.txt`
