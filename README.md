# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- Reference class: `SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT`.
- Research instrument: `EURUSD`.
- Idea: `IDEA-0001 — SCREENING`.
- Hypothesis: `HYP-0001 — READY_FOR_DATA_FEASIBILITY`.
- Data Feasibility: `CONDITIONAL`.

Canonical review:

`research/reviews/HYP-0001-DATA_FEASIBILITY.md`

Dukascopy EUR/USD 1H BID/ASK data is structurally suitable, but the actual source snapshot must be frozen, aligned and hashed before the prototype runs.

## Current closure check

`ATS2-M3-003 — Data feasibility`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M3-004 — Cheap prototype`

Next artifact:

`research/reviews/HYP-0001-PROTOTYPE-01.md`

No prototype result, Candidate, Strategy ID or Experiment exists yet.

## Boundary

Broker/live trading, capital allocation, Strategy Risk Mandate, leverage and scaling remain outside current scope.
