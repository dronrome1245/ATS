# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- M2: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Reference Strategy #1 class selected at repository-artifact level:

`SINGLE_INSTRUMENT_DAILY_LONG_FLAT_TREND_BREAKOUT`

Canonical decision:

`governance/program/REFERENCE_STRATEGY_1_SELECTION.md`

This selects only the research class: one instrument, daily bars, long/flat trend/breakout. It does not select the instrument, vendor, numeric parameters or claim profitability.

## Current closure check

`ATS2-M3-001 — Select Reference Strategy #1`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M3-002 — Idea & rationale`

Immediate next artifact:

`research/ideas/IDEA-0001.md`

The next research step will create the first real Idea/Hypothesis, not a Candidate or live strategy.

## Boundary

Broker/live trading, capital allocation, Strategy Risk Mandate, leverage and scaling remain outside current scope.
