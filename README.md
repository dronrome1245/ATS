# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- M0/M1/M2: `COMPLETED / PASS`.
- Reference class: `SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT`.
- Research instrument: `EURUSD` / EUR/USD spot FX.

Current research artifacts:

- `research/ideas/IDEA-0001.md` — `SCREENING`;
- `research/hypotheses/HYP-0001.md` — `READY_FOR_DATA_FEASIBILITY`.

HYP-0001 fixes a 24-bar upward breakout condition and a 24-bar primary forward measurement before any prototype result.

## Current closure check

`ATS2-M3-002 — Idea & rationale`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M3-003 — Data feasibility`

Next artifact:

`research/reviews/HYP-0001-DATA_FEASIBILITY.md`

No prototype/backtest result should be generated before Data Feasibility.

## Boundary

No Candidate, Strategy ID or Experiment exists yet. Broker/live trading, capital allocation, Strategy Risk Mandate, leverage and scaling remain outside current scope.
