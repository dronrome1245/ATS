# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: rejected at R3.
- Strategy #2: rejected at R3.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Verified RF-010 closure

OWNER `ATS_TASK_CHECK.bat` PASS was confirmed on exact main commit:

`dbb93b2510334561c7c38aa14b859aa42a420bbc`

Canonical last completed artifact:

`research/reviews/HYP-0003-PROTOTYPE-01.md`

RF-010 froze the complete HYP-0003 PROTO-01 25-cell formation/ranking/basket/execution/metrics/breadth contract without evaluating the development dataset.

Frozen runner:

`tools/hyp0003_proto01.py`

Frozen runner Git blob:

`d65746f39476ba3fee8cf59acfd0b2f82af9c663`

Information boundary at RF-010 closure:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

## RF-011 HYP-0003 PROTO-01 reveal

Current task:

`ATS2-RF-011 — HYP-0003 PROTO-01 reveal`

Canonical next artifact after result review:

`reports/research/HYP-0003-PROTOTYPE-01-result.json`

RF-011 verifies the exact frozen runner, frozen dataset identity and full Local CI before executing the runner once. It retains all 25 cells and applies the pre-written breadth decision rule.

If the result is positive under all breadth criteria, HYP-0003 still cannot enter R4 directly; the frozen next-action is `CREATE_NEW_CONFIRMATORY_HYPOTHESIS_BEFORE_R4`.

If the breadth rule fails, HYP-0003 is rejected at R3.

Protected tail remains unavailable.

Run `ATS_AGENT_PREFLIGHT.bat` on the reveal agent branch and return `AGENT_PREFLIGHT_REPORT.txt`. The reveal itself occurs only after merge to exact `main`.
