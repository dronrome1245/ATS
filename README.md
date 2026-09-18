# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Последний реализованный work package:

`ATS2-M2-005 — Minimal Strategy research interface`.

Primary artifact:

`src/ats/strategy/interface.py`.

Interface baseline:

- immutable run context and observations;
- loader-record bridge;
- deterministic generic state transition contract;
- broker-neutral canonical-JSON decisions;
- serializable diagnostics;
- no injected wall-clock/network/broker/live state.

Следующая task после M2-005 Local CI PASS:

`ATS2-M2-006 — Deterministic backtest/replay`.

Следующий artifact:

`src/ats/replay/engine.py`.

## Windows task check

Запустить:

`ATS_TASK_CHECK.bat`

После завершения отправить:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

## Boundary

M2 builds safe research infrastructure only. Reference Strategy #1, broker/live environment, capital and risk limits remain outside current scope.
