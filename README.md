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

- Validation Framework: `governance/methodology/VALIDATION_FRAMEWORK.md`
- Parameter sensitivity: `src/ats/validation/sensitivity.py`
- Declared slicing: `src/ats/validation/slicing.py`
- Observation concentration: `src/ats/validation/concentration.py`
- Dependence-preserving resampling: `src/ats/validation/resampling.py`

## Market Pattern Discovery

Bounded systematic price-pattern discovery is defined in:

`governance/methodology/MARKET_PATTERN_DISCOVERY.md`

Discovery remains exploratory and feeds new Idea/Hypothesis objects through the normal Research Funnel.

## Current closure check

`ATS2-M4-005 — Dependence-preserving resampling framework`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M4-006 — Independent exam protocol`

Next artifact:

`governance/methodology/INDEPENDENT_EXAM_PROTOCOL.md`
