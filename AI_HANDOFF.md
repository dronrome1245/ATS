# ATS AI Handoff

## Current state

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- Reference Strategy #1 research line: `REJECTED_AT_R3`.
- Idea: `IDEA-0001`.
- Hypothesis: `HYP-0001`.
- Prototype: `PROTO-01`.
- Prototype outcome: `REJECT`.
- No Candidate/Strategy ID/Experiment/live permission exists.

## Frozen prototype result

Canonical machine result:

`reports/research/HYP-0001-PROTOTYPE-01-result.json`

Run commit:

`6115b1c7114e942a4f3e76795ce8d25b552cf849`

Dataset:

`DATA-DUKASCOPY-EURUSDH1-PROTO01-001 / 1.0.0`

Metrics:

- breakout signals: `1006`;
- mean signal return: `-0.0002301573`;
- baseline mean: `-0.0000647136`;
- signal minus baseline: `-0.0001654436`;
- signal positive share: `0.4582505`;
- overlapping signal-window share: `0.7186879`.

Decision rule was fixed before the result. Both primary HYP-0001 inequalities failed, therefore outcome is `REJECT` with reason `ONE_OR_BOTH_PRIMARY_HYPOTHESIS_INEQUALITIES_FAILED`.

Economic label:

`QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING`

Commission, rollover and live-fill slippage were not modeled. The result is exploratory negative evidence, not validation evidence.

## Methodology consequence

Cheap Prototype protocol says `REJECT` stops this research line before Economic Pre-Screen.

Therefore:

- do not run WBS-3.5 Economic Pre-Screen for HYP-0001;
- do not create Candidate/Strategy ID;
- do not retune lookback/horizon/instrument inside HYP-0001;
- retain all negative history.

## Current closure check

Current checker closes:

`ATS2-M3-004 — Cheap prototype`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M3-005 — M3 early-rejection closeout / platform learning review`

Work package:

`WBS-3.11 (early-rejection path)`

Next artifact:

`governance/program/M3_EXIT_REVIEW.md`
