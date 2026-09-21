# ATS AI Handoff

## Current program state

- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- M2: `COMPLETED / PASS`.
- M3: `COMPLETED / PASS`.
- M4: `IN_PROGRESS`.
- HYP-0001 / PROTO-01: `REJECTED_AT_R3`.
- No Candidate/Strategy/live permission exists.

## M4-003 Declared slicing

Implementation:

`src/ats/validation/slicing.py`

Tests:

`tests/test_validation_slicing.py`

Contract:

- slices are declared before evaluation;
- every declared slice is reported in plan order;
- exhaustive coverage can be required;
- overlap can be explicitly forbidden or allowed;
- unassigned and multiply-assigned observations are counted;
- empty-slice policy is explicit;
- unknown or duplicate memberships fail closed;
- evaluator must return exactly the declared finite metric set;
- output declares `ALL_DECLARED_SLICES_REPORTED`.

This tooling cannot selectively drop an unfavorable period/regime and creates no evidence by itself.

## Current closure check

`ATS2-M4-003 — Time/regime slicing`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M4-004 — Observation concentration analysis`

Initial artifact:

`src/ats/validation/concentration.py`

The next tool must expose concentration/outlier dependence without automatically deleting observations.
