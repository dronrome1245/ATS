# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

ATS — Strategy Factory для воспроизводимого исследования алгоритмических торговых систем.

## Текущее состояние

- M0: `COMPLETED / PASS`
- M1: `COMPLETED / PASS`
- M2: `COMPLETED / PASS`
- M3: `COMPLETED / PASS`
- M4 Validation Framework: `IN_PROGRESS`

Reference Strategy #1 remains:

`HYP-0001 / PROTO-01 = REJECT`

## M4 tooling

Validation Framework:

`governance/methodology/VALIDATION_FRAMEWORK.md`

Parameter sensitivity:

`src/ats/validation/sensitivity.py`

Declared time/regime slicing:

`src/ats/validation/slicing.py`

## Current closure check

`ATS2-M4-003 — Time/regime slicing`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M4-004 — Observation concentration analysis`

Initial implementation target:

`src/ats/validation/concentration.py`
