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

## M4 tooling/methodology

- Validation Framework: `governance/methodology/VALIDATION_FRAMEWORK.md`
- Parameter sensitivity: `src/ats/validation/sensitivity.py`
- Declared slicing: `src/ats/validation/slicing.py`
- Observation concentration: `src/ats/validation/concentration.py`
- Dependence-preserving resampling: `src/ats/validation/resampling.py`
- Independent exam protocol: `governance/methodology/INDEPENDENT_EXAM_PROTOCOL.md`
- Multiple-research accounting: `governance/methodology/MULTIPLE_RESEARCH_ACCOUNTING.md`
- Technical strategy validation profile: `governance/methodology/TECHNICAL_STRATEGY_VALIDATION_PROFILE.md`

## Market Pattern Discovery

Bounded systematic price-pattern discovery methodology:

`governance/methodology/MARKET_PATTERN_DISCOVERY.md`

Execution of WBS-6.0 remains blocked until the M4-008 closure check passes.

## Current closure check

`ATS2-M4-008 — Technical strategy validation profile`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M6-000 — Market Pattern Discovery`

M4.9/M4.10 remain strategy-level work for the first future S05 PASS Candidate.
