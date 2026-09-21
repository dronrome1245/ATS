# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- M2: `COMPLETED / PASS`.
- Canonical M2 Exit Review: `governance/program/M2_EXIT_REVIEW.md`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

M2 delivered the minimum reusable research stack: deterministic data loading, Strategy/Research interface, replay, explicit costs, standard analytics/results, manifest-driven runner and end-to-end acceptance/regression tests.

No real strategy, market result or live permission was created to close M2.

## Current task

`ATS2-M3-001 — Select Reference Strategy #1`

Work package:

`WBS-3.1`

Next artifact:

`governance/program/REFERENCE_STRATEGY_1_SELECTION.md`

The selection should choose a simple strategy class with available data and a clear execution model. It is a research-program selection decision, not a profitability or live-trading decision.

## Windows task check

The current closure checker still verifies the M2 Exit transition commit:

`ATS_TASK_CHECK.bat`

After it passes, M3 work proceeds without additional M2 changes.

## Boundary

Broker/live trading, capital allocation, risk mandates and scaling remain outside the current scope.
