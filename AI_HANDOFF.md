# ATS AI Handoff

## Current program state

- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- M2: `COMPLETED / PASS`.
- M3: `COMPLETED / PASS`.
- M4: `IN_PROGRESS`.
- HYP-0001 / PROTO-01: `REJECTED_AT_R3`.
- No Candidate/Strategy/live permission exists.

## M4-002 Parameter Sensitivity

Implementation:

`src/ats/validation/sensitivity.py`

Tests:

`tests/test_validation_sensitivity.py`

Contract:

- caller predeclares ordered parameter names, metric names and all variants;
- every variant is evaluated in caller order;
- evaluator receives read-only parameter mapping;
- evaluator must return exactly the declared metric set;
- non-finite/malformed values fail closed;
- output is deterministic and includes `selection_policy = NO_AUTOMATIC_SELECTION`;
- there is no best/winner/rank selection API.

This tooling is infrastructure only. It creates no Candidate, Experiment or validation evidence by itself.

## Current closure check

Current checker closes:

`ATS2-M4-002 — Parameter sensitivity tooling`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M4-003 — Time/regime slicing`

Work package:

`WBS-4.3`

Initial artifact:

`src/ats/validation/slicing.py`

The next tool must expose all declared slices and must not selectively omit unfavorable periods/regimes.
