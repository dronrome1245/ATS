# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика, который впервые открывает репозиторий или продолжает работу после паузы.

Если вы AI-агент и получили доступ к этому репозиторию, **не начинайте с выбора стратегии, написания торгового кода, брокера или risk limits**. Сначала восстановите текущее состояние по этому документу и canonical artifacts.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Current phase: `M0_PROGRAM_REBASELINE`.
- Status: `IN_PROGRESS`.
- Program model: ATS v2 / Strategy Factory.
- Canonical machine-readable state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Реальная торговля, allocation и scaling сейчас не являются текущей задачей.
- Старые G01–G13 относятся к ATS v1 и не являются текущим roadmap программы.

## 2. Что уже принято и зафиксировано

Текущая база ATS v2:

1. `00_Управление_проектом/v2/PROGRAM_CHARTER_V2.md` — миссия, scope, success criteria и milestones.
2. `00_Управление_проектом/v2/OPERATING_MODEL_V2.md` — пять контуров ATS, сущности, роли и decision points.
3. `00_Управление_проектом/v2/STRATEGY_LIFECYCLE_V2.md` — Research Funnel и путь Candidate → Validation → Live → Scaling.
4. `00_Управление_проектом/v2/RESEARCH_METHODOLOGY_V1.md` — правила evidence, reproducibility и economic usefulness.
5. `00_Управление_проектом/v2/PROGRAM_WBS_V2.md` — work packages программы M0–M8, dependencies, roles и Definition of Done.
6. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` — единственный canonical machine-readable state v2.
7. `tools/validate_repo.py` — structural validator v2.

## 3. Последний завершённый содержательный шаг

Последний завершённый artifact:

`00_Управление_проектом/v2/PROGRAM_WBS_V2.md`

Одновременно завершена техническая миграция state/validator:

- корневой `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` переведён на schema v2;
- переходный второй state удалён;
- validator больше не требует старые G01–G13 как current state;
- validator проверяет согласованность canonical `next_artifact` с handoff и файлом следующего шага.

## 4. Следующий обязательный артефакт

`00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md`

Это work package `WBS-0.6`.

Его задача — определить окончательную структуру репозитория и canonical locations для:

- program governance;
- research ideas/hypotheses/candidates;
- strategies и Strategy Versions;
- data manifests;
- experiments/evidence/reports;
- shared platform code;
- execution/operations artifacts;
- portfolio artifacts;
- legacy ATS v1.

После Repository Structure v2 в M0 остаются:

- `WBS-0.7` Program Backlog v2;
- `WBS-0.8` Research entity templates;
- `WBS-0.12` окончательная legacy classification в новой структуре.

## 5. Что делать новому AI-агенту

Порядок действий:

1. Прочитать `AGENTS.md`.
2. Прочитать `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. Прочитать `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. Прочитать `PROGRAM_WBS_V2.md` и родительские документы, необходимые для следующего work package.
5. Сверить, не появился ли уже указанный `next_artifact`.
6. Выполнить именно следующий незавершённый шаг, если OWNER не дал другое явное указание.
7. Не возвращаться к legacy G01 как к current task.
8. Не выдумывать отсутствующие финансовые, торговые или юридические параметры.

## 6. Правило завершения любого существенного шага

Работа не считается завершённой, пока контекст для следующего чата не обновлён.

После каждого принятого program-level шага синхронизировать:

1. основной artifact;
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
3. `01_СТАТУС_ПРОЕКТА.md`;
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
5. `AI_HANDOFF.md`;
6. README/start guide, если изменилась верхнеуровневая модель;
7. validator/tests, если изменилась обязательная структура или invariants.

Нельзя завершать работу сообщением «готово», если state/handoff всё ещё указывают на предыдущую задачу.

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

- Что такое ATS? — Strategy Factory / program, а не один робот.
- Какая текущая фаза? — `M0_PROGRAM_REBASELINE`.
- Где canonical state? — `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Что уже завершено? — Charter, Operating Model, Strategy Lifecycle, Research Methodology, Program WBS, state/validator v2 migration и AI handoff.
- Что делать следующим? — `REPOSITORY_STRUCTURE_V2.md` (`WBS-0.6`).
- Можно ли сейчас выбирать real allocation? — нет.
- Являются ли G01–G13 current roadmap? — нет, это legacy ATS v1.

Если ответы отличаются, сначала устранить расхождение state/handoff/next action.
