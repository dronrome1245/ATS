# ATS AI Handoff

## Current program state

- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- M2: `COMPLETED / PASS`.
- M3: `COMPLETED / PASS`.
- M4: `IN_PROGRESS`.
- HYP-0001 / PROTO-01: `REJECTED_AT_R3`.
- No Candidate/Strategy/live permission exists.

## M4-001 Validation Framework

Canonical artifact:

`governance/methodology/VALIDATION_FRAMEWORK.md`

Core boundary:

`DEVELOPMENT → VALIDATION → INDEPENDENT_EXAMINATION`

- Development may choose/change the system.
- Validation evaluates a fixed-enough version under a registered pre-result protocol.
- Independent Examination is a separate one-shot protected-block `PASS / FAIL` exam.
- No tuning on validation data.
- Validation result strength follows `EVIDENCE_TAXONOMY.md`; registration alone is not `VALIDATION_EVIDENCE`.

Mandatory validation dimensions are:

- parameter neighbourhood;
- time/regime slicing;
- observation dependence/overlap;
- concentration/outliers;
- cost/execution sensitivity;
- appropriate dependence-preserving resampling;
- research freedom/multiple-research accounting.

A future strategy-specific Validation Profile must fix applicable axes, data blocks, primary metrics and decision rules before validation results.

M3 PROTO-01 overlap (`71.8688%`) is retained only as the program lesson motivating explicit dependence handling. Rejected HYP-0001 is not validation input.

## Current closure check

Current checker closes:

`ATS2-M4-001 — Validation protocol framework`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M4-002 — Parameter sensitivity tooling`

Work package:

`WBS-4.2`

Initial artifact:

`src/ats/validation/sensitivity.py`

The tool must evaluate predefined neighbourhoods and expose the full region. It must not select only the best result or create research evidence by itself.
