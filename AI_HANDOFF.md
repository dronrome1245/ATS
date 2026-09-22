# ATS AI Handoff

## Current program state

- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- M2: `COMPLETED / PASS`.
- M3: `COMPLETED / PASS`.
- M4: `IN_PROGRESS`.
- HYP-0001 / PROTO-01: `REJECTED_AT_R3`.
- No Candidate/Strategy/live permission exists.

## M4-004 Concentration analysis

Implementation:

`src/ats/validation/concentration.py`

Tests:

`tests/test_validation_concentration.py`

Contract:

- every supplied observation is retained;
- observation IDs are unique and values finite;
- `top_counts` are predeclared positive integers;
- top-observation concentration uses absolute contribution magnitude;
- optional groups are all retained in first-seen order;
- group concentration uses absolute net group effect;
- zero denominators produce explicit null shares;
- output declares `ABSOLUTE_MAGNITUDE_DIAGNOSTIC_ONLY`;
- output declares `NO_AUTOMATIC_OUTLIER_REMOVAL`.

This tooling exposes concentration; it does not remove outliers or create evidence by itself.

## Local CI failure control

`LOCAL_CI_FAILURE_REGISTRY.md` records recurring causes. The fast-preflight control for recurrent FORMAT failures was verified on `cac82301...` with fast gate PASS followed by 105 tests and full launcher PASS.

## Current closure check

`ATS2-M4-004 — Observation concentration analysis`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M4-005 — Dependence-preserving resampling framework`

Initial artifact:

`src/ats/validation/resampling.py`


## Market Pattern Discovery

Canonical methodology:

`governance/methodology/MARKET_PATTERN_DISCOVERY.md`

Purpose: systematically search for bounded price-dynamics patterns without presenting data-mined findings as validation evidence.

Rules:

- development data only;
- Search Manifest fixes pattern families/horizons/filters/search budget;
- full search-space count and failed alternatives are retained;
- outputs remain `EXPLORATORY_OBSERVATION`;
- shortlist may create a new Idea/Hypothesis only;
- protected validation/independent blocks are not used for discovery.

Roadmap bridge:

`M4.1–M4.8 → WBS-6.0 discovery / Strategy #2 research → first S05 PASS Candidate → M4.9/M4.10 → M5`

This removes the post-M3 early-rejection candidate-sourcing deadlock.
