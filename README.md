# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

ATS — Strategy Factory для воспроизводимого исследования алгоритмических торговых систем.

## Текущее состояние

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- Instrument: EUR/USD.
- Timeframe: 1H.
- Current task: `ATS2-M3-004 — Cheap prototype`.

PROTO-01 записан до просмотра результата:

`research/reviews/HYP-0001-PROTOTYPE-01.md`

Период заранее зафиксирован: 2021–2025.

## Сейчас

Подготовить данные:

`uv run --frozen python tools/proto01_eurusd.py prepare`

Потом передать:

`reports/local_ci/PROTO01_DATA_REPORT.txt`

Результат теста пока не запускать.
