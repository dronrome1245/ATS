# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Program model: ATS v2 / Strategy Factory.
- Current phase: `M1_RESEARCH_METHODOLOGY` / Research Factory.
- Status: `IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- G01–G13: `legacy/v1/`, history/reference only.
- Real trading, demo, allocation and scaling remain disallowed current actions.

## 2. Последний завершённый шаг

`ATS2-M1-007 — Experiment registration schema` — `DONE`.

Artifact:

`governance/methodology/EXPERIMENT_REGISTRATION.md`

Aligned templates:

- `governance/methodology/templates/experiment/manifest.yaml`;
- `governance/methodology/templates/experiment/result.json`;
- `governance/methodology/templates/experiment/conclusion.md`.

Formal Experiment rules now require:

- stable `EXP-YYYYMMDD-nnn`;
- real `HYP-xxxx` linkage;
- Candidate/Strategy/Strategy Version linkage when those entities exist;
- code/implementation/environment identity;
- dataset/source snapshot/period and transformation context;
- parameters/configuration;
- random seed/protocol or explicit `NOT_APPLICABLE`;
- cost/execution assumptions;
- predefined question;
- primary/secondary metrics;
- predefined decision rule;
- research stage and evidence class `REGISTERED_EXPERIMENT`;
- `REGISTERED` manifest committed before corresponding result observation.

Material changes after registration require a new Experiment ID. Cheap Prototype remains `EXPLORATORY_PROTOTYPE` and cannot be retroactively upgraded.

Structural testing created no fictitious Experiment ID/result.

`experiments/README.md` was also rebaselined away from ATS v1 registry paths and invented universal deposit/leverage requirements.

## 3. Текущая ready task

`ATS2-M1-008 — Experiment registry`

Canonical next artifact:

`experiments/REGISTRY.csv`

Goal: make positive, negative, failed, cancelled and superseded formal experiments discoverable by stable ID while keeping each experiment package as the authoritative detailed record.

## 4. Что должно быть определено в M1-008

- one canonical registry path;
- Experiment ID uniqueness;
- status/research-stage/evidence-class columns;
- Hypothesis and optional Candidate/Strategy lineage;
- canonical experiment package/manifest reference;
- registration anchor/context reference;
- result/conclusion presence;
- outcome/decision fields when known;
- supersede lineage;
- retention of negative/cancelled/failed entries;
- integrity rules preventing registry rows from becoming an alternate manifest;
- structural test without fictitious experiment rows.

## 5. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/methodology/EXPERIMENT_REGISTRATION.md`.
6. `experiments/README.md`.
7. `governance/methodology/templates/experiment/manifest.yaml`.
8. `governance/methodology/templates/experiment/result.json`.
9. `governance/methodology/templates/experiment/conclusion.md`.

## 6. Boundaries

Registry is an index, not the source of experiment truth. `REGISTERED_EXPERIMENT` means preregistered, not validated. Do not create fake rows, fake results or fake Strategy linkage for process testing. Do not choose Reference Strategy #1, broker, jurisdiction, live platform, capital allocation or risk limits.

## 7. Completion protocol

Material program task is complete only after deliverable, backlog, canonical state, human status, next-step, AI handoff and validator/entrypoints where relevant are synchronized.

## 8. Проверка восстановления контекста

- Current phase? — `M1_RESEARCH_METHODOLOGY`.
- Last completed? — `ATS2-M1-007`, `governance/methodology/EXPERIMENT_REGISTRATION.md`.
- Next task? — `ATS2-M1-008`.
- Next artifact? — `experiments/REGISTRY.csv`.
- Real Experiments created by structural test? — `0`.
- Can registry replace manifest/result/conclusion? — no.
- Can a completed prototype be retroactively called preregistered? — no.
