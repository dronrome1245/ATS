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

`Research Factory → Strategy #4 → HYP-0005 → Hypothesis Formation → ATS2-RF-022`

## Canonical last completed artifact

`reports/research/HYP-0004-PROTOTYPE-01-result.json`

## Verified RF-021 closure

OWNER `ATS_TASK_CHECK.bat` PASS was confirmed on exact main commit:

`79cb1d36bd544cc14db49ea5f6e85ef138a579eb`

RF-021 preserved the exact HYP-0004 result and selected confirmatory structural routing.

HYP-0004 result SHA-256:

`1c9b2cb1a1628599e935ee61fd8c9b152d7bd3447969b065c920c8d13e3e5230`

The HYP-0004 development result remains exploratory structural evidence only.

## RF-022 HYP-0005 formation

Current task:

`ATS2-RF-022 — HYP-0005 confirmatory hypothesis formation`

Canonical artifact:

`research/hypotheses/HYP-0005.md`

HYP-0005:

- parent Idea: `IDEA-0004`;
- development predecessor: `HYP-0004`;
- role: `CONFIRMATORY_STRUCTURAL_REPLICATION`;
- status: `READY_FOR_DATA_FEASIBILITY`;
- market: `FX_SPOT_OTC`;
- instrument: `EURUSD`;
- horizon: `NEXT_1H`.

Fixed UTC buckets:

- CORE_ACTIVE: `07–16`;
- TRANSITION: `17–20`;
- OFF_HOURS: `21–23` and `00–06`.

Primary HYP-0005 claim requires BOTH:

`median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)`

and:

`median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)`.

No magnitude threshold is imported from the HYP-0004 result.

RF-022 selects no confirmatory provider, snapshot, exact coverage or dataset identity and computes no confirmatory outcome.

Information boundary:

`NO_CONFIRMATORY_OUTCOME_COMPUTED`

Next task after RF-022 exact-main PASS:

`ATS2-RF-023 — HYP-0005 confirmatory Data Feasibility`

RF-023 must establish and freeze one genuinely unseen confirmatory block before any HYP-0005 outcome calculation.

Direct R4 entry remains blocked.
