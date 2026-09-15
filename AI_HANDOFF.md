# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика.

Если вы впервые получили доступ к репозиторию, не начинайте с выбора стратегии, broker, instrument, risk limits или торгового кода. Сначала восстановите состояние по canonical artifacts.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Current phase: `M0_PROGRAM_REBASELINE`.
- Status: `IN_PROGRESS`.
- Program model: ATS v2 / Strategy Factory.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Current governance: `governance/program/` и `governance/methodology/`.
- Реальная торговля, allocation и scaling сейчас запрещены как program action.
- G01–G13 — legacy ATS v1, не current roadmap.

## 2. Canonical ATS v2 documents

Program:

- `governance/program/PROGRAM_CHARTER_V2.md`;
- `governance/program/OPERATING_MODEL_V2.md`;
- `governance/program/PROGRAM_WBS_V2.md`;
- `governance/program/REPOSITORY_STRUCTURE_V2.md`.

Methodology:

- `governance/methodology/STRATEGY_LIFECYCLE_V2.md`;
- `governance/methodology/RESEARCH_METHODOLOGY_V1.md`;
- `governance/methodology/templates/README.md`.

Execution queue:

- `governance/backlog/PROGRAM_BACKLOG_V2.md`.

## 3. Последний завершённый шаг

`ATS2-M0-010 — Legacy v1 index/classification` завершена.

Последний завершённый artifact:

`legacy/v1/MIGRATION_INDEX.md`

Также создан `legacy/v1/README.md`.

Inventory содержит 15 designated v1 artifacts:

- 4 `HISTORY`;
- 5 `REFERENCE`;
- 6 `REVIEW_NEEDED`.

Classification не делает legacy-файлы current. Review-needed означает, что потенциально полезный смысл требует нового v2 review/decision.

## 4. Следующая ready task

`ATS2-M0-011 — Legacy physical migration and unresolved-question carryover`

Canonical next artifact:

`legacy/v1/CARRYOVER.md`

Использовать `legacy/v1/MIGRATION_INDEX.md` как единственный migration plan.

Нужно:

1. создать target copies всех 15 legacy artifacts;
2. проверить сохранность contents;
3. удалить old v1 paths только после проверки;
4. создать `CARRYOVER.md`;
5. remap OQ-001…009 на v2 stages;
6. добавить backlog tasks только там, где нужной future task ещё нет;
7. не переносить старую blocking semantics автоматически.

Предварительный OQ remap уже записан в `MIGRATION_INDEX.md`: capital/risk вопросы относятся к future live/capital policy, jurisdiction/broker — к M5/S08, execution platform разделяется на M2 research stack и M5 live execution, hypothesis/data questions решаются per strategy через Research Funnel/Data Feasibility.

## 5. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `legacy/v1/README.md`.
6. `legacy/v1/MIGRATION_INDEX.md`.
7. Только затем source legacy files, необходимые для migration.

## 6. Completion protocol

Program-level task не считается завершённой, пока синхронизированы:

1. deliverable;
2. Program Backlog;
3. canonical state;
4. human status;
5. next step;
6. AI handoff;
7. entrypoints, если они содержат next task;
8. validator/tests при structural changes.

## 7. Запреты

Без явного решения OWNER нельзя:

- выделять реальный капитал;
- утверждать Strategy Risk Mandate;
- разрешать live admission;
- менять allocation/scaling;
- выдумывать broker/jurisdiction/instrument/return/risk limits;
- ослаблять independent evidence rules;
- вводить martingale, unlimited averaging или rescue funding;
- объявлять legacy requirement автоматически current v2 policy.

## 8. Проверка восстановления контекста

Новый агент должен ответить:

- Current phase? — `M0_PROGRAM_REBASELINE`.
- Last completed? — `ATS2-M0-010`, `legacy/v1/MIGRATION_INDEX.md`.
- Next task? — `ATS2-M0-011`.
- Next artifact? — `legacy/v1/CARRYOVER.md`.
- Migration plan? — `legacy/v1/MIGRATION_INDEX.md`.
- Можно ли сейчас выбирать live capital/broker/strategy? — нет.
