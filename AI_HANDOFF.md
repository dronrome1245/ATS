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

## Verified RF-014 closure

OWNER `ATS_TASK_CHECK.bat` PASS was confirmed on exact main commit:

`b1392ad843c57bf0ca4c2d0575f4095957b80e82`

Canonical last completed artifact:

`governance/program/STRATEGY_4_FAMILY_SELECTION.md`

Companion completed Idea:

`research/ideas/IDEA-0004.md`

RF-014 selected `S4-FAM-03 — INTRADAY_TIME_SESSION_EFFECT` for Idea Intake and screened IDEA-0004 without fixing performance-selected parameters.

## RF-015 HYP-0004 formation

Current task:

`ATS2-RF-015 — HYP-0004 formation`

Canonical next artifact:

`research/hypotheses/HYP-0004.md`

HYP-0004 is a bounded structural EUR/USD fixed-UTC claim. It fixes:

- `CORE_ACTIVE`: UTC hours 07–16;
- `TRANSITION`: UTC hours 17–20, retained but not part of the primary decision;
- `OFF_HOURS`: UTC hours 21–23 and 00–06;
- next-hour absolute midpoint return as the movement outcome;
- boundary relative BID/ASK spread as the friction diagnostic;
- two primary inequalities that must both pass;
- a rule forbidding post-result clock-window search inside HYP-0004.

HYP-0004 status is `READY_FOR_DATA_FEASIBILITY` with decision `DATA_FEASIBILITY`.

The exact provider, coverage dates and permissible boundary-lag tolerance remain unknown and must be verified before quantitative testing.

After RF-015 exact-head PASS:

`ATS2-RF-016 — HYP-0004 Data Feasibility`

must determine whether the required synchronized BID/ASK hourly-boundary information can be represented honestly and reproducibly. No HYP-0004 outcome is computed during RF-015.
