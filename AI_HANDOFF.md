# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: отклонена на R3.
- Strategy #2: отклонена на R3.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Verified RF-002 closure

OWNER launcher PASS was confirmed on exact commit:

`040a0c78dc3829c7ca534397dc55691eaae1a4fd`

Evidence included pinned Ruff lint/format, pytest collection `141 tests`, full pytest `141 passed`, full Local CI, current task PASS and launcher PASS.

Canonical last completed artifact:

`governance/program/STRATEGY_3_IDEA_SOURCING.md`

## RF-003 Strategy #3 family selection and Idea intake

Current task:

`ATS2-RF-003 — Strategy #3 family selection and Idea intake`

Canonical next artifact:

`research/ideas/IDEA-0003.md`

Selection artifact:

`governance/program/STRATEGY_3_FAMILY_SELECTION.md`

Selected family:

`S3-FAM-02 — CROSS_SECTIONAL_CURRENCY_MOMENTUM`

Idea:

`IDEA-0003 — Cross-Sectional Currency Momentum`

Status:

`SCREENING`

The selection is based on materially different mechanism, plausible multi-instrument data path, cheap falsification and platform value. It is not a claim of profitability.

Exact currency universe, provider, lookback, holding/rebalance horizon, ranking rule and target magnitude remain unselected.

Development parameter tuning will be allowed under a bounded search policy with full variant accounting. Confirmatory data cannot be tuned against and remain independent evidence for the same claim.

Run `ATS_TASK_CHECK.bat` and return `reports/local_ci/CURRENT_TASK_REPORT.txt`.

After exact-head PASS:

`ATS2-RF-004 — HYP-0003 formation`.
