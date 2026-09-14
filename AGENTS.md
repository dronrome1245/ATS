# AGENTS.md — правила работы ИИ и программных агентов в ATS

## 1. Назначение

Агент помогает формализовать гипотезы, вести исследования, проектировать platform capabilities, реализовывать стратегии, проверять evidence и поддерживать целостность репозитория.

Агент не принимает за OWNER решения о капитале, live admission, scaling или изменении критических risk policies.

## 2. Первый файл для нового чата

При первом входе в репозиторий, после потери контекста или перед продолжением незнакомой работы **сначала прочитать `AI_HANDOFF.md`**.

`AI_HANDOFF.md` должен позволять за один проход понять:

- что такое ATS;
- текущую фазу программы;
- какие решения уже приняты;
- на каком артефакте остановились;
- какой следующий task/artifact разрешён;
- какие legacy-файлы нельзя ошибочно принимать за актуальный roadmap.

Если `AI_HANDOFF.md`, `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`, `governance/backlog/PROGRAM_BACKLOG_V2.md` и `02_СЛЕДУЮЩИЙ_ШАГ.md` противоречат друг другу, содержательную работу не продолжать до устранения расхождения.

## 3. Обязательный порядок чтения

Перед содержательной работой читать:

1. `AI_HANDOFF.md`;
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` — canonical machine-readable state;
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
4. `governance/backlog/PROGRAM_BACKLOG_V2.md` — canonical execution queue;
5. `00_Управление_проектом/v2/PROGRAM_CHARTER_V2.md`;
6. `00_Управление_проектом/v2/OPERATING_MODEL_V2.md`;
7. `00_Управление_проектом/v2/PROGRAM_WBS_V2.md` — для program work;
8. `00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md` — для structural/migration work;
9. `00_Управление_проектом/v2/RESEARCH_METHODOLOGY_V1.md` — для research;
10. `00_Управление_проектом/v2/STRATEGY_LIFECYCLE_V2.md` — для конкретной стратегии;
11. только затем связанные code/data/test/report artifacts.

Не загружать весь репозиторий без необходимости.

## 4. Canonical state и execution queue

Единственный canonical machine-readable state ATS:

`03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.

Canonical program backlog:

`governance/backlog/PROGRAM_BACKLOG_V2.md`.

State определяет текущую фазу, last completed artifact, next artifact и next task ID. Backlog содержит executable tasks, dependencies, priority/status и Definition of Done.

Человекочитаемые представления:

- `01_СТАТУС_ПРОЕКТА.md`;
- `02_СЛЕДУЮЩИЙ_ШАГ.md`;
- `AI_HANDOFF.md`.

Старая модель G01–G13 сохранена в legacy-документах как history/reference, но не является текущим roadmap программы.

## 5. Модель ATS v2

ATS — не одна стратегия и не один robot project.

Программа состоит из:

- Research Factory;
- Shared Trading Platform;
- Strategy Lifecycle;
- Portfolio & Capital;
- Operations & Governance.

Текущая работа управляется milestones M0–M8, `PROGRAM_WBS_V2.md` и canonical backlog.

## 6. Research discipline

Агент обязан различать:

- exploratory observation;
- registered experiment;
- validation evidence;
- independent evidence;
- demo/shadow evidence;
- live evidence.

Exploratory result нельзя представлять как formal proof без соответствующего experiment manifest.

Каждый formal experiment должен иметь однозначные code/data/config/cost assumptions и conclusion. Negative experiments не удаляются.

## 7. Жёсткие запреты

Агенту запрещено:

- выдумывать капитал, валюту, risk limits, broker, jurisdiction, instrument, timeframe, expected return или tax regime;
- подменять отсутствующие факты типовыми числами;
- объявлять strategy profitable или validated только по привлекательному backtest;
- менять pass/fail criteria после просмотра результата и выдавать это за прежний experiment;
- использовать protected independent period для tuning;
- скрывать failed/rejected experiments;
- повышать risk для отыгрыша;
- применять martingale, unlimited averaging или automatic rescue funding;
- обходить Strategy Risk или Portfolio Risk;
- хранить в Git secrets, account credentials, private keys, персональные документы или секретные broker exports;
- представлять результат ATS как гарантию прибыли или персональную финансовую рекомендацию.

## 8. Работа с Strategy Version

Material change, способное повлиять на trades, создаёт новую Strategy Version и требует повторной проверки затронутого evidence.

Примеры material change:

- entry/exit;
- filters;
- position management;
- risk logic;
- material parameters;
- data source/protocol;
- cost/execution assumptions.

Minor refactor, не способный изменить торговые решения, может не требовать полного lifecycle, но должен быть документирован.

## 9. Independent Examination

Перед independent examination должны быть заморожены version, parameters, data block, cost model и decision criteria.

После раскрытия результата этот evidence block считается известным. Изменение стратегии создаёт новую research iteration; нельзя продолжать называть повторный тест тем же независимым экзаменом без отдельного обоснования.

## 10. Platform development

Платформа развивается demand-driven:

`Strategy need → Minimum capability → Reuse → Shared capability → Hardening`.

Агент не должен создавать крупную универсальную infrastructure без конкретного потребителя и проверяемого deliverable.

## 11. Risk separation

Логический порядок:

`Strategy Intent → Strategy Risk → Portfolio Risk → Execution`.

Отрицательное решение risk layer окончательно для создания нового риска.

Неисправность strategy logic не должна отключать protective controls.

## 12. Live boundary

Research и validation без реального exposure могут выполняться без strategy-level allocation.

Перед minimal live должны существовать соответствующие lifecycle evidence, live protocol и owner-approved Strategy Risk Mandate.

Demo/shadow не считается доказательством profitability, а historical backtest не считается доказательством live execution.

## 13. Decision rights

Без явного решения OWNER агент не меняет:

- program-level capital policy;
- Strategy Risk Mandate;
- live admission;
- allocation;
- scaling decision;
- profit withdrawal policy;
- critical stop rules.

## 14. Experiment naming

Формальные experiments используют уникальный ID вида `EXP-YYYYMMDD-nnn` и содержат manifest с Strategy Version, code revision, dataset, parameters, cost model, result и conclusion.

## 15. Completion / handoff protocol

Любой существенный program-level шаг считается завершённым только после синхронизации контекста для следующего чата.

Перед завершением работы агент обязан проверить и при необходимости обновить:

1. основной созданный/изменённый artifact;
2. `governance/backlog/PROGRAM_BACKLOG_V2.md`;
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
4. `01_СТАТУС_ПРОЕКТА.md`;
5. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
6. `AI_HANDOFF.md`;
7. `README.md` и `00_НАЧАТЬ_ЗДЕСЬ.md`, если они содержат изменившуюся next action или модель;
8. validator/tests, если изменились обязательная структура или invariants.

Нельзя сообщать OWNER, что шаг завершён, если backlog/state/handoff всё ещё указывают на предыдущую задачу.

## 16. Проверка репозитория

Перед предложением завершённого изменения проверить:

```bash
python tools/validate_repo.py
```

Validator должен подтверждать canonical v2 state, обязательные v2 artifacts и согласованность `next_artifact`/`next_task_id` между state, backlog, handoff и `02_СЛЕДУЮЩИЙ_ШАГ.md`.

После появления исполняемого platform/strategy code к structural validation добавляются профильные unit, integration, replay и failure tests.

## 17. Принцип безопасности

При unknown state, broken reconciliation, corrupted data, unavailable protection layer или risk-limit violation система должна прекращать создание нового риска и формировать diagnostic event. Действия с уже открытыми позициями задаются отдельным live protocol.
