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

`ATS2-M2-007 — Cost model interface`.

Primary artifact:

`src/ats/costs/interface.py`.

Cost baseline:

- explicit ordered component configuration;
- no hidden numeric defaults for applicable components;
- explicit `NOT_APPLICABLE` representation with reason;
- deterministic cost inputs outside Strategy logic;
- separate serializable component/result objects;
- exact component/order/applicability validation;
- no gross/net analytics or broker/live execution behavior.

Следующая task после M2-007 Local CI PASS:

`ATS2-M2-008 — Standard analytics/report`.

Следующий artifact:

`src/ats/analytics/standard.py`.

## Windows task check

Запустить:

`ATS_TASK_CHECK.bat`

После завершения отправить:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

## Boundary

M2 builds safe research infrastructure only. Reference Strategy #1, broker/live environment, capital and risk limits remain outside current scope.
