# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика, который впервые открывает репозиторий или продолжает работу после паузы.

Если вы AI-агент и получили доступ к этому репозиторию, **не начинайте с выбора стратегии, написания торгового кода, брокера или risk limits**. Сначала восстановите текущее состояние по этому документу и указанным canonical artifacts.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Current phase: `M0_PROGRAM_REBASELINE`.
- Status: `IN_PROGRESS`.
- Program model: ATS v2 / Strategy Factory.
- Реальная торговля, allocation и scaling сейчас не являются текущей задачей.
- Старые G01–G13 относятся к ATS v1 и **не являются текущим roadmap программы**.

## 2. Что уже принято и зафиксировано

Следующие документы являются текущей базой ATS v2:

1. `00_Управление_проектом/v2/PROGRAM_CHARTER_V2.md`
   - ATS — программа/Strategy Factory, а не один торговый робот.
   - Цель — воспроизводимо находить, проверять, запускать и со временем объединять несколько экономически полезных стратегий.

2. `00_Управление_проектом/v2/OPERATING_MODEL_V2.md`
   - пять контуров: Research Factory, Shared Trading Platform, Strategy Lifecycle, Portfolio & Capital, Operations & Governance;
   - разделены Idea, Hypothesis, Strategy, Strategy Version, Experiment, Evidence, Deployment, Portfolio.

3. `00_Управление_проектом/v2/STRATEGY_LIFECYCLE_V2.md`
   - дешёвый Research Funnel предшествует дорогой validation;
   - обязательный `Economic Viability` до глубоких затрат;
   - Strategy Risk Mandate появляется перед реальным exposure, а не перед безопасным research;
   - independent examination, stress, demo/shadow, minimal live и controlled scaling сохранены.

4. `00_Управление_проектом/v2/RESEARCH_METHODOLOGY_V1.md`
   - exploratory research отделён от formal evidence;
   - formal experiment должен быть воспроизводим;
   - стратегия должна отдельно доказать evidence of edge и economic usefulness;
   - отрицательные результаты сохраняются.

5. `00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml`
   - machine-readable program state на время M0.

## 3. Где мы остановились

Последний завершённый содержательный шаг:

`ATS Research Methodology v1` создан и записан в репозиторий.

Следующий обязательный артефакт:

`00_Управление_проектом/v2/PROGRAM_WBS_V2.md`

Его задача — разложить ATS Program на управляемые work packages по milestones M0–M8 с зависимостями, deliverables, ответственными ролями и Definition of Done.

После WBS в M0 остаются как минимум:

- `REPOSITORY_STRUCTURE_V2.md`;
- Program Backlog v2;
- Research entity templates;
- миграция validator/state model с v1 на окончательный v2 canonical state.

## 4. Что делать новому AI-агенту

Порядок действий обязателен:

1. Прочитать `AGENTS.md`.
2. Прочитать `00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml`.
3. Прочитать `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. Прочитать только родительские документы, необходимые для следующего шага.
5. Сверить, не появился ли уже указанный `next_artifact`.
6. Выполнить именно следующий незавершённый шаг, если пользователь не дал другое явное указание.
7. Не возвращаться к legacy G01 как к текущей задаче.
8. Не выдумывать отсутствующие финансовые, торговые или юридические параметры.

## 5. Правило завершения любого существенного шага

Работа **не считается завершённой**, пока контекст для следующего чата не обновлён.

После каждого принятого program-level шага агент должен проверить и при необходимости синхронно обновить:

1. созданный/изменённый основной artifact;
2. `00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml`;
3. `01_СТАТУС_ПРОЕКТА.md`;
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
5. этот `AI_HANDOFF.md` — секции «Что уже принято», «Где мы остановились» и «Следующий обязательный артефакт»;
6. `README.md` / `00_НАЧАТЬ_ЗДЕСЬ.md`, если изменилась верхнеуровневая модель или точка входа;
7. validator/tests, если структура репозитория или обязательные артефакты изменились.

Нельзя завершать шаг сообщением «готово», если state/handoff всё ещё указывают на предыдущую работу.

## 6. Source of truth во время M0

На период `M0_PROGRAM_REBASELINE`:

- program state v2: `00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml`;
- human status: `01_СТАТУС_ПРОЕКТА.md`;
- next action: `02_СЛЕДУЮЩИЙ_ШАГ.md`;
- AI handoff: `AI_HANDOFF.md`.

Корневой `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` является legacy ATS v1 и временно сохранён для совместимости старого validator. Он не должен использоваться для выбора текущей задачи.

После завершения M0 должен остаться один окончательный canonical machine-readable state, а переходное правило должно быть удалено.

## 7. Неподлежащие самовольному изменению решения

Без явного решения OWNER нельзя:

- выделять реальный капитал;
- утверждать Strategy Risk Mandate;
- разрешать live admission;
- менять allocation/scaling;
- выдумывать broker/jurisdiction/instrument/return/risk limits;
- ослаблять independent evidence rules;
- вводить martingale, unlimited averaging или rescue funding;
- объявлять стратегию прибыльной/validated только по привлекательному backtest.

## 8. Как понять, что контекст восстановлен правильно

Новый агент после чтения должен уметь без догадок ответить:

- Что такое ATS? — Strategy Factory / program, а не один робот.
- Какая текущая фаза? — `M0_PROGRAM_REBASELINE`.
- Что уже завершено? — Charter v2, Operating Model v2, Strategy Lifecycle v2, Research Methodology v1.
- Что делать следующим? — `PROGRAM_WBS_V2.md`.
- Можно ли сейчас выбирать реальный allocation? — нет.
- Являются ли G01–G13 текущим roadmap? — нет, это legacy ATS v1.

Если ответы отличаются, остановить содержательную работу и сначала устранить расхождение в state/handoff.
