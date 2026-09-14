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
- какой следующий шаг разрешён;
- какие legacy-файлы нельзя ошибочно принимать за актуальный roadmap.

Если `AI_HANDOFF.md`, program state и `02_СЛЕДУЮЩИЙ_ШАГ.md` противоречат друг другу, содержательную работу не продолжать до устранения расхождения.

## 3. Обязательный порядок чтения

Во время `M0_PROGRAM_REBASELINE` перед содержательной работой читать:

1. `AI_HANDOFF.md`;
2. `00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml`;
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
4. `00_Управление_проектом/v2/PROGRAM_CHARTER_V2.md`;
5. `00_Управление_проектом/v2/OPERATING_MODEL_V2.md`;
6. для research — `00_Управление_проектом/v2/RESEARCH_METHODOLOGY_V1.md`;
7. для конкретной стратегии — `00_Управление_проектом/v2/STRATEGY_LIFECYCLE_V2.md`;
8. только затем связанные code/data/test/report artifacts.

Не загружать весь репозиторий без необходимости.

## 4. Переходное состояние

Корневой `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` содержит state model ATS v1 и временно сохраняется для истории и совместимости существующего `tools/validate_repo.py`.

Во время rebaseline актуальное program-level состояние v2 находится в `00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml`, человекочитаемые представления — в `01_СТАТУС_ПРОЕКТА.md` и `02_СЛЕДУЮЩИЙ_ШАГ.md`, а краткий handoff для нового контекста — в `AI_HANDOFF.md`.

После завершения M0 должен остаться один однозначный canonical machine-readable state.

## 5. Модель ATS v2

ATS — не одна стратегия и не один robot project.

Программа состоит из:

- Research Factory;
- Shared Trading Platform;
- Strategy Lifecycle;
- Portfolio & Capital;
- Operations & Governance.

Старые G01–G13 не являются текущим roadmap программы. Они сохраняются как legacy и источник требований, перенесённых в `Strategy Lifecycle v2`.

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
2. `00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml`;
3. `01_СТАТУС_ПРОЕКТА.md`;
4. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
5. `AI_HANDOFF.md`;
6. `README.md` и `00_НАЧАТЬ_ЗДЕСЬ.md`, если изменилась верхнеуровневая модель;
7. validator/tests, если изменились обязательная структура или invariants.

Нельзя сообщать OWNER, что шаг завершён, если handoff/state всё ещё указывают на предыдущую задачу.

## 16. Проверка репозитория

Перед предложением завершённого изменения запускать или проверять применимость:

```bash
python tools/validate_repo.py
```

Текущий validator всё ещё содержит часть структурных требований v1. Его миграция входит в M0 и не должна приводить к удалению legacy evidence до утверждения новой структуры.

После появления исполняемого platform/strategy code к structural validation должны добавляться профильные unit, integration, replay и failure tests.

## 17. Принцип безопасности

При unknown state, broken reconciliation, corrupted data, unavailable protection layer или risk-limit violation система должна прекращать создание нового риска и формировать diagnostic event. Действия с уже открытыми позициями задаются отдельным live protocol.
