# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика.

Если вы AI-агент и впервые получили доступ к этому репозиторию, не начинайте с выбора стратегии, написания торгового кода, брокера или risk limits. Сначала восстановите состояние по этому документу и canonical artifacts.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Current phase: `M0_PROGRAM_REBASELINE`.
- Status: `IN_PROGRESS`.
- Program model: ATS v2 / Strategy Factory.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Реальная торговля, allocation и scaling сейчас не являются текущей задачей.
- Старые G01–G13 относятся к ATS v1 и не являются current roadmap программы.

## 2. Что уже принято и зафиксировано

Текущая база ATS v2 включает:

1. `00_Управление_проектом/v2/PROGRAM_CHARTER_V2.md`;
2. `00_Управление_проектом/v2/OPERATING_MODEL_V2.md`;
3. `00_Управление_проектом/v2/STRATEGY_LIFECYCLE_V2.md`;
4. `00_Управление_проектом/v2/RESEARCH_METHODOLOGY_V1.md`;
5. `00_Управление_проектом/v2/PROGRAM_WBS_V2.md`;
6. `00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md`;
7. `governance/backlog/PROGRAM_BACKLOG_V2.md`;
8. `governance/methodology/templates/README.md` и entity template package;
9. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
10. `tools/validate_repo.py`.

Текущие пути `00_Управление_проектом/v2/` для baseline governance documents временные и должны быть мигрированы следующей task.

## 3. Последний завершённый шаг

`ATS2-M0-008 / WBS-0.8 — Research entity templates` завершён.

Canonical template index:

`governance/methodology/templates/README.md`

Template package покрывает:

- Idea;
- Hypothesis;
- Candidate;
- formal Experiment: manifest/result/conclusion;
- Strategy Version: version manifest/specification/parameters/evidence index.

Шаблоны не подставляют выдуманные факты: `null` означает ещё не зафиксированное значение, `NOT_APPLICABLE` — действительно неприменимое поле.

## 4. Следующая ready task

`ATS2-M0-009 — Governance v2 path migration`

Canonical next artifact anchor:

`governance/program/PROGRAM_CHARTER_V2.md`

Задача — перенести current-v2 baseline documents из `00_Управление_проектом/v2/` в target tree:

- program documents → `governance/program/`;
- methodology documents → `governance/methodology/`.

Templates уже находятся в target methodology tree.

Migration должна атомарно обновить state, backlog references, README/start guide, AGENTS, AI handoff, cross-links и validator. Старые current-v2 файлы удаляются только после создания и проверки новых копий.

После `ATS2-M0-009 = DONE` следующей ready task становится `ATS2-M0-010 — Legacy v1 index/classification`.

## 5. Что делать новому AI-агенту

1. Прочитать `AGENTS.md`.
2. Прочитать `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. Прочитать `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. Прочитать `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. Для текущей migration прочитать `00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md`.
6. Выполнить именно `ATS2-M0-009`, если OWNER не дал другое явное указание.
7. Не менять содержание baseline documents в рамках structural migration.
8. Не возвращаться к legacy G01 как к current task.

## 6. Completion / handoff protocol

После material program-level шага синхронизировать:

1. основной artifact/deliverable;
2. canonical backlog;
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
4. `01_СТАТУС_ПРОЕКТА.md`;
5. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
6. `AI_HANDOFF.md`;
7. README/start guide, если они содержат изменившуюся точку входа;
8. validator/tests, если изменилась обязательная структура или invariants.

Нельзя сообщать OWNER, что шаг завершён, если backlog/state/handoff всё ещё указывают на предыдущую работу.

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
- Где backlog? — `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Что завершено последним? — Research entity templates (`ATS2-M0-008`).
- Что делать следующим? — Governance v2 path migration (`ATS2-M0-009`).
- Какой next artifact anchor? — `governance/program/PROGRAM_CHARTER_V2.md`.
- Можно ли сейчас выбирать real allocation? — нет.

Если ответы отличаются, сначала устранить расхождение backlog/state/handoff/next action.
