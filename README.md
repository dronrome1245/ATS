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

`ATS2-M2-009 — Manifest-driven experiment runner`.

Primary artifact:

`src/ats/runner/experiment.py`.

Runner baseline:

- frozen registered manifest is read-only and SHA-256 bound;
- runtime code/environment/implementation identity must match registration;
- registered Dataset ID/source snapshot must match the Dataset Manifest;
- registered params/config/seed feed the Strategy/Replay context;
- explicit registered costs feed the cost interface;
- standard analytics/result are produced without changing preregistration;
- unsupported registered metrics block the run;
- no dynamic import from untrusted manifest text and no hidden wall clock;
- tests use transient software-only manifests and create no formal evidence.

Следующая task после M2-009 Local CI PASS:

`ATS2-M2-010 — Research platform tests`.

Следующий artifact:

`tests/test_research_platform.py`.

## Windows task check

Запустить:

`ATS_TASK_CHECK.bat`

После завершения отправить:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

## Boundary

M2 builds safe research infrastructure only. Reference Strategy #1, broker/live environment, capital and risk limits remain outside current scope.
