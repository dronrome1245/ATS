# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

ATS — Strategy Factory для воспроизводимого исследования алгоритмических торговых систем.

## Текущее состояние

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- Reference Strategy #1: rejected at Cheap Prototype.
- HYP-0001 / PROTO-01 outcome: `REJECT`.

The fixed EUR/USD 1H breakout prototype produced 1006 signals. Mean signal return was negative and below the unconditional baseline.

Canonical result:

`reports/research/HYP-0001-PROTOTYPE-01-result.json`

No parameter rescue/optimization is allowed inside HYP-0001.

## Current closure check

`ATS2-M3-004 — Cheap prototype`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M3-005 — M3 early-rejection closeout / platform learning review`

Next artifact:

`governance/program/M3_EXIT_REVIEW.md`
