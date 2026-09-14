# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика.

Если вы AI-агент и впервые получили доступ к этому репозиторию, не начинайте с выбора стратегии, написания торгового кода, брокера или risk limits. Сначала восстановите состояние по этому документу и canonical artifacts.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Current phase: `M0_PROGRAM_REBASELINE`.
- Status: `IN_PROGRESS`.
- Program model: ATS v2 / Strategy Factory.
- Canonical machine-readable state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
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
7. `governance/backlog/PROGRAM_BACKLOG_V2.md` — executable queue для M0 и ближайших M1/M2 работ.
8. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` — единственный canonical machine-readable state v2.
9. `tools/validate_repo.py` — structural validator v2.

## 3. Последний завершённый содержательный шаг

Последний завершённый artifact:

`governance/backlog/PROGRAM_BACKLOG_V2.md`

Это `WBS-0.7`.

Backlog ввёл:

- stable Task ID;
- priority/status model;
- explicit dependencies и block reasons;
- executable M0/M1/M2 tasks;
- future epics для M3–M8 без преждевременной детализации;
- текущую execution queue;
- dependency refinement для M2 через `Reference Consumer Profile`, чтобы не создавать цикл между stack decision и будущим выбором Reference Strategy #1.

## 4. Следующий обязательный артефакт

`governance/methodology/templates/README.md`

Это task `ATS2-M0-008`, связанная с `WBS-0.8 — Research entity templates`.

Минимальный набор templates должен покрыть:

- Idea;
- Hypothesis;
- Candidate;
- formal Experiment manifest/conclusion;
- Strategy Version.

Templates должны соответствовать Operating Model, Strategy Lifecycle, Research Methodology и naming rules. Они не должны содержать выдуманные торговые/финансовые значения.

После `ATS2-M0-008 = DONE` backlog должен перевести `ATS2-M0-009` Governance v2 path migration из `BLOCKED` в `READY`.

## 5. Что делать новому AI-агенту

Порядок действий:

1. Прочитать `AGENTS.md`.
2. Прочитать `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. Прочитать `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. Прочитать `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. Для текущей задачи прочитать `OPERATING_MODEL_V2.md`, `STRATEGY_LIFECYCLE_V2.md`, `RESEARCH_METHODOLOGY_V1.md` и `REPOSITORY_STRUCTURE_V2.md`.
6. Сверить, не появился ли уже canonical `next_artifact`.
7. Выполнить именно `ATS2-M0-008`, если OWNER не дал другое явное указание.
8. Не возвращаться к legacy G01 как к current task.
9. Не выдумывать отсутствующие финансовые, торговые или юридические параметры.

## 6. Правило завершения любого существенного шага

Работа не считается завершённой, пока контекст следующего чата не синхронизирован.

После program-level шага проверить и при необходимости обновить:

1. основной artifact;
2. `governance/backlog/PROGRAM_BACKLOG_V2.md`;
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
- Где execution queue? — `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Что завершено последним? — Program Backlog v2 (`WBS-0.7`).
- Что делать следующим? — `governance/methodology/templates/README.md` / `ATS2-M0-008` (`WBS-0.8`).
- Можно ли сейчас выбирать real allocation? — нет.
- Являются ли G01–G13 current roadmap? — нет, это legacy ATS v1.

Если ответы отличаются, сначала устранить расхождение backlog/state/handoff/next action.
