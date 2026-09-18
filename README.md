# ATS

> **AI / новый чат:** сначала откройте `AI_HANDOFF.md`, затем `AGENTS.md`.

**ATS — Algorithmic Trading Systems** — Strategy Factory для воспроизводимого исследования, проверки и дальнейшей эксплуатации алгоритмических торговых систем.

## Текущее состояние

- Phase: `M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Последняя завершённая task:

`ATS2-M2-003 — Dataset manifest support`.

Canonical specification:

`governance/program/DATASET_MANIFEST_SPEC.md`.

Dataset Manifest baseline:

- safe YAML parsing;
- immutable Pydantic model;
- canonical `DATA-<SOURCE>-<PURPOSE>-NNN` identity + semantic dataset version;
- explicit source/snapshot/storage/schema metadata;
- timezone-aware coverage;
- event-time / information-availability semantics;
- deterministic ordering/tie-break;
- explicit data-quality policy;
- transformation lineage;
- integrity metadata and known limitations;
- synthetic non-market tests only.

Следующая ready task:

`ATS2-M2-004 — Base data loader`.

Следующий artifact:

`src/ats/data/loader.py`.

## Canonical ATS v2

- Program governance: `governance/program/`;
- Architecture decisions: `governance/decisions/`;
- Methodology: `governance/methodology/`;
- Formal experiments and registry: `experiments/`;
- Data policy/manifests: `data/`;
- Source/platform code: `src/`;
- Execution queue: `governance/backlog/PROGRAM_BACKLOG_V2.md`;
- Legacy ATS v1: `legacy/v1/`.

## Быстрый старт

1. `AI_HANDOFF.md`.
2. `AGENTS.md`.
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
5. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. Dataset contract: `governance/program/DATASET_MANIFEST_SPEC.md`.
7. Environment: `governance/program/RESEARCH_ENVIRONMENT_SPEC.md`, `pyproject.toml`, `.python-version`, `uv.lock`.
8. На Windows основной интерфейс проверки: запустить `ATS_CHECK.bat`.
9. BAT сам обновит `main`, синхронизирует frozen environment, выполнит полный gate и создаст `reports/local_ci/LATEST_REPORT.txt`.
10. Для диагностики/подтверждения отправлять ChatGPT именно `LATEST_REPORT.txt`.

## Quality gate

GitHub Actions не используется как completion gate. Политика: `governance/program/LOCAL_CI_GATE.md`. `ATS_CHECK.bat` должен завершиться PASS; shareable output находится в `reports/local_ci/LATEST_REPORT.txt`.

## Boundary

M2 materializes safe research infrastructure only. Reference Strategy #1, broker/live environment, capital and risk limits remain outside current scope. Dataset Manifest is implemented; deterministic base data loader is next; Strategy API/replay are not yet implemented.
