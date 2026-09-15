# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика.

Если вы AI-агент и впервые получили доступ к этому репозиторию, не начинайте с выбора стратегии, торгового кода, брокера или risk limits. Сначала восстановите состояние по этому документу и canonical artifacts.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Current phase: `M0_PROGRAM_REBASELINE`.
- Status: `IN_PROGRESS`.
- Program model: ATS v2 / Strategy Factory.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Реальная торговля, allocation и scaling сейчас не являются текущей задачей.
- G01–G13 относятся к ATS v1 и не являются current roadmap.

## 2. Canonical ATS v2 documents

Program governance:

1. `governance/program/PROGRAM_CHARTER_V2.md`
2. `governance/program/OPERATING_MODEL_V2.md`
3. `governance/program/PROGRAM_WBS_V2.md`
4. `governance/program/REPOSITORY_STRUCTURE_V2.md`

Methodology:

5. `governance/methodology/STRATEGY_LIFECYCLE_V2.md`
6. `governance/methodology/RESEARCH_METHODOLOGY_V1.md`
7. `governance/methodology/templates/README.md`

Execution queue:

8. `governance/backlog/PROGRAM_BACKLOG_V2.md`

## 3. Последний завершённый шаг

`ATS2-M0-009 — Governance v2 path migration` завершена.

Current-v2 documents перенесены из временного `00_Управление_проектом/v2/` в target `governance/` tree. State/backlog/entrypoints/validator должны ссылаться только на target paths. Старые current-v2 копии не являются source of truth и удаляются после проверки миграции.

## 4. Следующая ready task

`ATS2-M0-010 — Legacy v1 index/classification`

Следующий artifact:

`legacy/v1/README.md`

Цель: создать однозначный legacy index ATS v1, классифицировать старые документы как `history`, `reference` или `review-needed`, задать target paths и отметить актуальные unresolved questions для последующего carryover.

После 0.10:

- `ATS2-M0-011` physical legacy migration + unresolved-question carryover;
- `ATS2-M0-012` final link/validator sweep;
- `ATS2-M0-013` M0 Exit Review.

## 5. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. Для program work — relevant files in `governance/program/`.
6. Для research — `governance/methodology/RESEARCH_METHODOLOGY_V1.md` и templates.
7. Для конкретной стратегии — `governance/methodology/STRATEGY_LIFECYCLE_V2.md`.
8. Только затем code/data/test/report artifacts.

Не загружать весь репозиторий без необходимости.

## 6. Completion / handoff protocol

Program-level task не считается завершённой, пока синхронизированы:

1. основной deliverable;
2. `governance/backlog/PROGRAM_BACKLOG_V2.md`;
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
4. `01_СТАТУС_ПРОЕКТА.md`;
5. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
6. `AI_HANDOFF.md`;
7. README/start guide, если менялась точка входа;
8. validator/tests, если менялись paths или invariants.

Нельзя сообщать OWNER, что шаг завершён, если backlog/state/handoff всё ещё указывают на предыдущую task.

## 7. Неподлежащие самовольному изменению решения

Без явного решения OWNER нельзя:

- выделять реальный капитал;
- утверждать Strategy Risk Mandate;
- разрешать live admission;
- менять allocation/scaling;
- выдумывать broker/jurisdiction/instrument/return/risk limits;
- ослаблять independent evidence rules;
- вводить martingale, unlimited averaging или rescue funding;
- объявлять стратегию profitable/validated только по привлекательному backtest.

## 8. Проверка восстановления контекста

Новый агент должен без догадок ответить:

- Что такое ATS? — Strategy Factory / program, а не один robot project.
- Какая текущая фаза? — `M0_PROGRAM_REBASELINE`.
- Где canonical state? — `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Где execution queue? — `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Где current governance? — `governance/program/` и `governance/methodology/`.
- Что завершено последним? — `ATS2-M0-009` governance path migration.
- Что делать следующим? — `ATS2-M0-010`, создать `legacy/v1/README.md`.
- Можно ли сейчас выбирать real allocation? — нет.
- Являются ли G01–G13 current roadmap? — нет.

Если ответы отличаются, сначала устранить расхождение backlog/state/handoff/next action.
