# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика.

Если вы AI-агент и впервые получили доступ к этому репозиторию, не начинайте с выбора стратегии, написания торгового кода, брокера или risk limits. Сначала восстановите состояние по этому документу и canonical artifacts.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Current phase: `M0_PROGRAM_REBASELINE`.
- Status: `IN_PROGRESS`.
- Program model: ATS v2 / Strategy Factory.
- Canonical machine-readable state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Реальная торговля, allocation и scaling сейчас не являются текущей задачей.
- Старые G01–G13 относятся к ATS v1 и не являются current roadmap программы.

## 2. Что уже принято и зафиксировано

Текущая база ATS v2:

1. `00_Управление_проектом/v2/PROGRAM_CHARTER_V2.md` — миссия, scope, success criteria и milestones.
2. `00_Управление_проектом/v2/OPERATING_MODEL_V2.md` — пять контуров ATS, сущности, роли и decision points.
3. `00_Управление_проектом/v2/STRATEGY_LIFECYCLE_V2.md` — Research Funnel и путь Candidate → Validation → Live → Scaling.
4. `00_Управление_проектом/v2/RESEARCH_METHODOLOGY_V1.md` — evidence, reproducibility и economic usefulness.
5. `00_Управление_проектом/v2/PROGRAM_WBS_V2.md` — work packages M0–M8.
6. `00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md` — target repository architecture, canonical entity locations, naming rules и migration map.
7. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` — единственный canonical machine-readable state v2.
8. `tools/validate_repo.py` — structural validator v2.

## 3. Последний завершённый содержательный шаг

Последний завершённый artifact:

`00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md`

Это `WBS-0.6`.

Приняты ключевые структурные решения:

- root содержит только program entrypoints;
- целевой program governance находится в `governance/`;
- research entities — в `research/`;
- отдельные Strategy/Strategy Version — в `strategies/`;
- shared capabilities — в `platform/`;
- datasets/manifests, experiments, reports, portfolio и operations разделены;
- ATS v1 должен быть изолирован в `legacy/v1/` после управляемой миграции;
- массовые moves не выполняются без backlog task, обновления ссылок и validator.

## 4. Следующий обязательный артефакт

`governance/backlog/PROGRAM_BACKLOG_V2.md`

Это `WBS-0.7 — Program Backlog v2`.

Backlog должен превратить оставшиеся M0 work packages и ближайшие M1/M2 зависимости в упорядоченные исполнимые задачи с priority, status, dependencies, role, deliverable и Definition of Done.

Первая версия Backlog обязана включить:

- Research entity templates (`WBS-0.8`);
- legacy classification/migration index (`WBS-0.12`);
- migration tasks из Repository Structure v2;
- M0 exit review;
- первые задачи M1 Research Factory;
- только необходимые prerequisites M2 Research Platform MVP.

После Program Backlog следующий основной work package — `WBS-0.8 Research entity templates`.

## 5. Что делать новому AI-агенту

Порядок действий:

1. Прочитать `AGENTS.md`.
2. Прочитать `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. Прочитать `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. Прочитать `PROGRAM_WBS_V2.md` и `REPOSITORY_STRUCTURE_V2.md`.
5. Сверить, не появился ли уже canonical `next_artifact`.
6. Выполнить именно следующий незавершённый шаг, если OWNER не дал другое явное указание.
7. Не возвращаться к legacy G01 как к current task.
8. Не выдумывать отсутствующие финансовые, торговые или юридические параметры.

## 6. Правило завершения любого существенного шага

Работа не считается завершённой, пока контекст следующего чата не синхронизирован.

После program-level шага проверить и при необходимости обновить:

1. основной artifact;
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
3. `01_СТАТУС_ПРОЕКТА.md`;
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
5. `AI_HANDOFF.md`;
6. README/start guide, если они содержат изменившуюся точку входа;
7. validator/tests, если изменилась обязательная структура или invariants.

Нельзя сообщать OWNER, что шаг завершён, если state/handoff всё ещё указывают на предыдущую работу.

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
- Что завершено последним? — `REPOSITORY_STRUCTURE_V2.md` (`WBS-0.6`).
- Что делать следующим? — `governance/backlog/PROGRAM_BACKLOG_V2.md` (`WBS-0.7`).
- Можно ли сейчас выбирать real allocation? — нет.
- Являются ли G01–G13 current roadmap? — нет, это legacy ATS v1.

Если ответы отличаются, сначала устранить расхождение state/handoff/next action.
