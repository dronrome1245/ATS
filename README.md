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

`ATS2-M2-008 — Standard analytics/report`.

Primary artifact:

`src/ats/analytics/standard.py`.

Analytics baseline:

- deterministic replay/run identity and technical counts;
- explicit effect semantics and units;
- separate gross effect, modeled costs and net effect;
- baseline effect distribution and absolute max drawdown when applicable;
- explicit `NOT_APPLICABLE` instead of invented metrics;
- explicit trade/event count semantics;
- canonical JSON plus deterministic Markdown report;
- no broker/live, portfolio or strategy-specific assumptions.

Следующая task после M2-008 Local CI PASS:

`ATS2-M2-009 — Manifest-driven experiment runner`.

Следующий artifact:

`src/ats/runner/experiment.py`.

## Windows task check

Запустить:

`ATS_TASK_CHECK.bat`

После завершения отправить:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

## Boundary

M2 builds safe research infrastructure only. Reference Strategy #1, broker/live environment, capital and risk limits remain outside current scope.
