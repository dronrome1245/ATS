# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: отклонена на R3.
- Strategy #2: отклонена на R3.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Verified RF-003 closure

OWNER launcher PASS was confirmed on exact commit:

`be11af8bfa3fb7386babb4ebab67d4e70c50924f`

Evidence included pinned Ruff lint/format, pytest collection `141 tests`, full pytest `141 passed`, full Local CI, current task PASS and launcher PASS.

Canonical last completed artifact:

`research/ideas/IDEA-0003.md`

Selected family:

`S3-FAM-02 — CROSS_SECTIONAL_CURRENCY_MOMENTUM`

## RF-004 HYP-0003 formation

Current task:

`ATS2-RF-004 — HYP-0003 formation`

Canonical next artifact:

`research/hypotheses/HYP-0003.md`

HYP-0003 is a development-stage Hypothesis, not the final confirmatory claim.

It freezes:

- monthly cross-sectional ranking;
- formation periods `1, 3, 6, 9, 12 months`;
- holding periods `1, 3, 6, 9, 12 months`;
- exactly `25` declared development variants;
- top/bottom one-sixth winner/loser baskets;
- side-aware BID/ASK execution;
- a broad-region rule based on the median cell mean, at least `13 / 25` positive-mean cells, and breadth across at least three formation and three holding periods.

The exact currency universe, provider and development dates are still unresolved and belong to Data Feasibility.

If HYP-0003 passes development, ATS must create a new fixed Hypothesis ID for a separate previously unseen confirmatory block. The development result cannot be relabeled as confirmation.

Run `ATS_TASK_CHECK.bat` and return `reports/local_ci/CURRENT_TASK_REPORT.txt`.

After exact-head PASS:

`ATS2-RF-005 — HYP-0003 Data Feasibility`.
