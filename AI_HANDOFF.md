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

## Verified RF-019 closure

OWNER `ATS_TASK_CHECK.bat` PASS was confirmed on exact main commit:

`95174c2922fd5882c995ff14b3031d690ecc80bf`

Canonical last completed artifact:

`research/reviews/HYP-0004-PROTOTYPE-01.md`

RF-019 froze HYP-0004 / PROTO-01 without revealing a development outcome.

Frozen runner:

`tools/hyp0004_proto01.py`

Frozen runner Git blob:

`cbc9a46bf5e5296615f51c0ea564153968bc2a55`

Frozen dataset:

`DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001@1.0.0`

Prepared CSV SHA-256:

`3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6`

## RF-020 HYP-0004 PROTO-01 reveal

Current task:

`ATS2-RF-020 — HYP-0004 PROTO-01 reveal`

The exact-main task checker must:

1. verify the frozen runner Git blob and frozen dataset SHA-256;
2. run governance validation and full Local CI;
3. execute the exact frozen runner only after those gates pass;
4. validate the resulting dataset identity, geometry, bucket metrics, primary Booleans and frozen decision routing;
5. retain an existing valid result for the exact reveal commit without recomputation.

Frozen primary inequalities:

`median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)`

and:

`median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)`

Both must pass for the positive route.

Positive route:

`CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4`

Negative route:

`STOP_HYP0004`

Before reveal, information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

Future canonical result:

`reports/research/HYP-0004-PROTOTYPE-01-result.json`

After exact-main RF-020 PASS:

`ATS2-RF-021 — HYP-0004 PROTO-01 result canonicalization and routing`

must canonicalize the exact local result without changing the frozen research contract.
