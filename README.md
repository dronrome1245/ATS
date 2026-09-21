# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

ATS — Strategy Factory для воспроизводимого исследования алгоритмических торговых систем.

## Текущее состояние

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- Instrument: EUR/USD 1H.
- Current task: `ATS2-M3-004 — Cheap prototype`.
- Prototype: `PROTO-01 — READY_TO_RUN`.

Rules and 2021–2025 data are frozen before result observation.

Dataset Manifest:

`data/manifests/DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml`

Prepared CSV SHA-256:

`aeda05d90994259a22e25d882398218aead968941fe0b1c73eb34894841291c0`

## Current action

`uv run --frozen python tools/proto01_eurusd.py run`

Then share the local result report and JSON. Do not alter parameters after seeing the result.
