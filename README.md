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

`ATS2-M2-010 — Research platform tests`.

Primary artifact:

`tests/test_research_platform.py`.

Committed acceptance result:

`tests/fixtures/platform/reference_consumer_expected.json`.

M2 acceptance baseline:

- deterministic synthetic Dataset Manifest/loader path;
- deterministic Strategy state/decision/diagnostic trace;
- explicit applicable and not-applicable cost components;
- standard gross/cost/net analytics;
- committed expected regression result;
- exact repeated-run equality;
- no formal research IDs or Experiment Registry row for the software fixture;
- manifest-runner suite remains part of the M2-010 targeted closure package.

Следующая task после M2-010 Local CI PASS:

`ATS2-M2-011 — M2 Exit`.

Следующий artifact:

`governance/program/M2_EXIT_REVIEW.md`.

## Windows task check

Запустить:

`ATS_TASK_CHECK.bat`

После завершения отправить:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

## Boundary

M2 builds safe research infrastructure only. Reference Strategy #1, broker/live environment, capital and risk limits remain outside current scope.
