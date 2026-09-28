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

`Research Factory → Strategy #4 → HYP-0004 → R3 Cheap Prototype → ATS2-RF-021`

## Canonical last completed artifact

`research/reviews/HYP-0004-PROTOTYPE-01.md`

## Verified RF-020 reveal

OWNER `ATS_TASK_CHECK.bat` PASS was confirmed on exact main commit:

`60371d16b71c1e7d1fb0ccd83c5104984e4b740a`

The exact frozen HYP-0004 runner was executed once after full Local CI PASS.

Frozen runner Git blob:

`cbc9a46bf5e5296615f51c0ea564153968bc2a55`

Frozen dataset:

`DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001@1.0.0`

Dataset SHA-256:

`3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6`

Canonical machine result:

`reports/research/HYP-0004-PROTOTYPE-01-result.json`

Exact result SHA-256:

`1c9b2cb1a1628599e935ee61fd8c9b152d7bd3447969b065c920c8d13e3e5230`

Result:

- movement inequality: `PASS`;
- spread inequality: `PASS`;
- both primary inequalities: `PASS`;
- machine decision: `ADVANCE_TO_ECONOMIC_SCREEN`;
- decision reason: `BOTH_PRIMARY_INEQUALITIES_MET`;
- frozen next action: `CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4`.

Primary medians:

- CORE_ACTIVE abs next-1h return: `0.0006982268977376305`;
- OFF_HOURS abs next-1h return: `0.0003493061509638462`;
- CORE_ACTIVE relative spread: `4.018781312113313e-05`;
- OFF_HOURS relative spread: `6.690913261869393e-05`.

The result remains:

`EXPLORATORY_PROTOTYPE / STRUCTURAL_H1_OPEN_PROXY_NO_TRADING_PNL`

Exact tick-level boundary time remains unknown.

## RF-021 routing

Current task:

`ATS2-RF-021 — HYP-0004 PROTO-01 result canonicalization and routing`

RF-021 preserves the exact result and selects the confirmatory branch of the frozen positive route.

Reason:

- HYP-0004 is structural and non-directional;
- no directional trading rule was tested;
- no trading P&L was computed;
- moving directly to a trading formulation would introduce additional research freedom after observing development data;
- a fixed confirmatory structural replication is the lower-freedom continuation.

Next task after RF-021 exact-main PASS:

`ATS2-RF-022 — HYP-0005 confirmatory hypothesis formation`

Planned Hypothesis:

`HYP-0005 — EUR/USD Fixed-UTC Intraday Activity Contrast Confirmatory Replication`

No confirmatory dataset or unseen boundary is selected by RF-021. HYP-0005 must be registered before any confirmatory outcome is observed.

Direct R4 entry remains blocked.
