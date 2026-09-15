# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Program model: ATS v2 / Strategy Factory.
- Current phase: `M1_RESEARCH_METHODOLOGY`.
- Human meaning: M1 Research Factory.
- Status: `IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- `M0_PROGRAM_REBASELINE` завершён с `PASS`.
- G01–G13 находятся в `legacy/v1/` и не являются current roadmap.
- Реальная торговля, demo, allocation и scaling сейчас не разрешены.

## 2. Последний завершённый шаг

`ATS2-M0-013 — M0 Exit Review` — `DONE / PASS`.

Последний завершённый artifact:

`governance/program/M0_EXIT_REVIEW.md`

M0 подтвердил program governance, methodology, WBS/backlog, repository structure, research templates, canonical state, validator, AI handoff и legacy isolation.

## 3. Текущая ready task

`ATS2-M1-001 — Idea intake process`

Canonical next artifact:

`governance/methodology/IDEA_INTAKE_PROCESS.md`

Цель — operationalize создание и первичный screening Idea на базе существующего `governance/methodology/templates/IDEA_TEMPLATE.md`.

Не создавать фиктивную trading idea только ради проверки процесса.

## 4. Что должно быть определено в M1-001

- stable Idea ID `IDEA-xxxx`;
- обязательные поля;
- граница observation → Idea → Hypothesis;
- статусы Idea;
- screening decisions `SCREEN / PARK / REJECT`;
- сохранение отрицательных решений;
- критерий перехода к M1-002 Hypothesis model;
- использование template без invented values;
- deterministic handoff для следующего агента.

## 5. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/M0_EXIT_REVIEW.md` — при необходимости понять переход M0→M1.
6. `governance/methodology/RESEARCH_METHODOLOGY_V1.md`.
7. `governance/methodology/STRATEGY_LIFECYCLE_V2.md`.
8. `governance/methodology/templates/IDEA_TEMPLATE.md`.
9. Только затем связанные research artifacts.

Не загружать весь репозиторий без необходимости.

## 6. Current canonical ATS v2

Program governance:

- `governance/program/PROGRAM_CHARTER_V2.md`;
- `governance/program/OPERATING_MODEL_V2.md`;
- `governance/program/PROGRAM_WBS_V2.md`;
- `governance/program/REPOSITORY_STRUCTURE_V2.md`.

Methodology:

- `governance/methodology/STRATEGY_LIFECYCLE_V2.md`;
- `governance/methodology/RESEARCH_METHODOLOGY_V1.md`;
- `governance/methodology/templates/`.

Execution queue:

- `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Legacy/reference:

- `legacy/v1/README.md`;
- `legacy/v1/MIGRATION_INDEX.md`;
- `legacy/v1/CARRYOVER.md`.

## 7. Запреты и boundaries

Без явного OWNER decision нельзя:

- выделять real capital;
- утверждать Strategy Risk Mandate;
- разрешать demo/live admission;
- менять allocation/scaling;
- выдумывать broker/jurisdiction/instrument/return/risk limits;
- объявлять exploratory result formal evidence;
- ослаблять independent evidence rules;
- вводить martingale, unlimited averaging или rescue funding.

Reference Strategy #1 выбирается не в M1-001, а позже после M1/M2 readiness согласно WBS.

## 8. Completion protocol

Material program task не считается завершённой до синхронизации:

1. основного deliverable;
2. `governance/backlog/PROGRAM_BACKLOG_V2.md`;
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
4. `01_СТАТУС_ПРОЕКТА.md`;
5. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
6. `AI_HANDOFF.md`;
7. entrypoints/validator при изменении invariants.

## 9. Проверка восстановления контекста

Новый агент должен ответить без догадок:

- Что такое ATS? — Strategy Factory program.
- Какой milestone завершён? — M0 Program Rebaseline.
- Текущая phase? — `M1_RESEARCH_METHODOLOGY` / Research Factory.
- Что делать следующим? — `ATS2-M1-001`.
- Какой next artifact? — `governance/methodology/IDEA_INTAKE_PROCESS.md`.
- Можно ли сейчас выбирать Reference Strategy #1 или real allocation? — нет.
