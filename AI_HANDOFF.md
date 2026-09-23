# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6 Reference Strategy #2 & Platform Generalization: `COMPLETED / PASS`.
- HYP-0001 / PROTO-01: отклонена на R3.
- HYP-0002 / PROTO-01: отклонена на R3.
- Candidate count: `0`.
- M5/M7/M8 remain unavailable.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Verified M6 closure

OWNER launcher PASS was confirmed on exact commit:

`01953b1dd5a8c3e81a372705b2198ba8ef2027d0`

Evidence included pinned Ruff lint/format, pytest collection `141 tests`, full pytest `141 passed`, full Local CI, current task PASS and launcher PASS.

Canonical M6 exit artifact:

`governance/program/M6_EXIT_REVIEW.md`

M6 PASS means the Research Factory was exercised on two materially different strategy profiles with negative evidence preserved. It does not mean either strategy succeeded.

## RF-001 Strategy #3 sourcing rebaseline

Current task:

`ATS2-RF-001 — Strategy #3 sourcing rebaseline`

Canonical next artifact:

`governance/program/STRATEGY_3_SOURCING_REBASELINE.md`

The rebaseline creates a permanent Research Factory lane after M6:

`WBS-RF.0 → RF.1 → RF.2 → RF.3 → RF.4`

No Strategy #3 class, market, instrument, timeframe, provider, parameter or expected return is selected in advance.

M4.9/M4.10 remain blocked until a future line honestly reaches S05 PASS.

Run `ATS_TASK_CHECK.bat` and return `reports/local_ci/CURRENT_TASK_REPORT.txt`.

After exact-head PASS, advance to:

`ATS2-RF-002 — Strategy #3 idea sourcing`.
