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

It is not reopened by M4.

## M4-001

Validation rules are now materialized in:

`governance/methodology/VALIDATION_FRAMEWORK.md`

The framework separates development, validation and protected independent examination; requires pre-result criteria; and requires explicit treatment of overlap/dependence and research freedom.

## Current closure check

`ATS2-M4-001 — Validation protocol framework`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M4-002 — Parameter sensitivity tooling`

Initial implementation target:

`src/ats/validation/sensitivity.py`
