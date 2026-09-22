# ATS AI Handoff

## Current program state

- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- M2: `COMPLETED / PASS`.
- M3: `COMPLETED / PASS`.
- M4: `IN_PROGRESS`.
- HYP-0001 / PROTO-01: `REJECTED_AT_R3`.
- No Candidate/Strategy/live permission exists.

## M4-005 Dependence-preserving resampling

Implementation:

`src/ats/validation/resampling.py`

Tests:

`tests/test_validation_resampling.py`

Contract:

- supported method is explicit `BLOCK_BOOTSTRAP`;
- caller declares block semantics;
- source blocks are non-empty, finite and uniquely identified;
- resampling selects whole blocks with replacement;
- within-block order is preserved;
- every replicate records selected block IDs and flattened values;
- seed/repetitions/blocks-per-replicate are explicit;
- output declares `DECLARED_BLOCKS_PRESERVED`;
- there is no implicit IID fallback.

This tooling is infrastructure only and creates no validation evidence by itself.

## Market Pattern Discovery

Canonical methodology:

`governance/methodology/MARKET_PATTERN_DISCOVERY.md`

Roadmap bridge remains:

`M4.1–M4.8 → WBS-6.0 discovery / Strategy #2 research → first S05 PASS Candidate → M4.9/M4.10 → M5`

## Current closure check

`ATS2-M4-005 — Dependence-preserving resampling framework`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M4-006 — Independent exam protocol`

Initial artifact:

`governance/methodology/INDEPENDENT_EXAM_PROTOCOL.md`
