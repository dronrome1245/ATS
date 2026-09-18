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

`ATS2-M2-004 — Base data loader`.

Primary artifact:

`src/ats/data/loader.py`.

Loader baseline:

- validated Dataset Manifest input;
- deterministic UTF-8 CSV loading;
- RFC3339 event/availability timestamps;
- explicit ordering/tie-break;
- duplicate/malformed/out-of-order policies;
- coverage enforcement;
- optional SHA-256 integrity verification;
- immutable output;
- synthetic non-market fixtures only.

Следующая task после M2-004 Local CI PASS:

`ATS2-M2-005 — Minimal Strategy research interface`.

Следующий artifact:

`src/ats/strategy/interface.py`.

## Canonical ATS v2

- Program governance: `governance/program/`;
- Architecture decisions: `governance/decisions/`;
- Methodology: `governance/methodology/`;
- Formal experiments and registry: `experiments/`;
- Data policy/manifests: `data/`;
- Source/platform code: `src/`;
- Execution queue: `governance/backlog/PROGRAM_BACKLOG_V2.md`;
- Legacy ATS v1: `legacy/v1/`.

## Windows task check

Для текущего material step запустить:

`ATS_TASK_CHECK.bat`

После завершения отправить ChatGPT:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

BAT сам обновляет repository, синхронизирует frozen environment и выполняет task-specific checks + full Local CI.

## Boundary

M2 builds safe research infrastructure only. Reference Strategy #1, broker/live environment, capital and risk limits remain outside current scope.
