# AGENTS.md — правила работы ИИ и программных агентов в ATS

## 1. Назначение

Агент помогает формализовать гипотезы, вести исследования, проектировать platform capabilities, реализовывать стратегии, проверять evidence и поддерживать целостность репозитория.

Агент не принимает за OWNER решения о капитале, live admission, scaling или изменении критических risk policies.

## 2. Обязательный порядок чтения

Во время `M0_PROGRAM_REBASELINE` перед содержательной работой читать:

1. `00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml`;
2. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
3. `00_Управление_проектом/v2/PROGRAM_CHARTER_V2.md`;
4. `00_Управление_проектом/v2/OPERATING_MODEL_V2.md`;
5. для research — `00_Управление_проектом/v2/RESEARCH_METHODOLOGY_V1.md`;
6. для конкретной стратегии — `00_Управление_проектом/v2/STRATEGY_LIFECYCLE_V2.md`;
7. только затем связанные code/data/test/report artifacts.

Не загружать весь репозиторий без необходимости.

## 3. Переходное состояние

Корневой `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` содержит state model ATS v1 и временно сохраняется для истории и совместимости существующего `tools/validate_repo.py`.

Во время rebaseline актуальное program-level состояние v2 находится в `00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml`, а человекочитаемые представления — в `01_СТАТУС_ПРОЕКТА.md` и `02_СЛЕДУЮЩИЙ_ШАГ.md`.

После завершения M0 должен остаться один однозначный canonical machine-readable state.

## 4. Модель ATS v2

ATS — не одна стратегия и не один robot project.

Программа состоит из:

- Research Factory;
- Shared Trading Platform;
- Strategy Lifecycle;
- Portfolio & Capital;
- Operations & Governance.

Старые G01–G13 не являются текущим roadmap программы. Они сохраняются как legacy и источник требований, перенесённых в `Strategy Lifecycle v2`.

## 5. Research discipline

Агент обязан различать:

- exploratory observation;
- registered experiment;
- validation evidence;
- independent evidence;
- demo/shadow evidence;
- live evidence.

Exploratory result нельзя представлять как formal proof без соответствующего experiment manifest.

Каждый formal experiment должен иметь однозначные code/data/config/cost assumptions и conclusion. Negative experiments не удаляются.

## 6. Жёсткие запреты

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

## 7. Работа с Strategy Version

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

## 8. Independent Examination

Перед independent examination должны быть заморожены version, parameters, data block, cost model и decision criteria.

После раскрытия результата этот evidence block считается известным. Изменение стратегии создаёт новую research iteration; нельзя продолжать называть повторный тест тем же независимым экзаменом без отдельного обоснования.

## 9. Platform development

Платформа развивается demand-driven:

`Strategy need → Minimum capability → Reuse → Shared capability → Hardening`.

Агент не должен создавать крупную универсальную infrastructure без конкретного потребителя и проверяемого deliverable.

## 10. Risk separation

Логический порядок:

`Strategy Intent → Strategy Risk → Portfolio Risk → Execution`.

Отрицательное решение risk layer окончательно для создания нового риска.

Неисправность strategy logic не должна отключать protective controls.

## 11. Live boundary

Research и validation без реального exposure могут выполняться без strategy-level allocation.

Перед minimal live должны существовать соответствующие lifecycle evidence, live protocol и owner-approved Strategy Risk Mandate.

Demo/shadow не считается доказательством profitability, а historical backtest не считается доказательством live execution.

## 12. Decision rights

Без явного решения OWNER агент не меняет:

- program-level capital policy;
- Strategy Risk Mandate;
- live admission;
- allocation;
- scaling decision;
- profit withdrawal policy;
- critical stop rules.

## 13. Experiment naming

Формальные experiments используют уникальный ID вида `EXP-YYYYMMDD-nnn` и содержат manifest с Strategy Version, code revision, dataset, parameters, cost model, result и conclusion.

## 14. Проверка репозитория

Перед предложением завершённого изменения запускать или проверять применимость:

```bash
python tools/validate_repo.py
```

Текущий validator всё ещё содержит часть структурных требований v1. Его миграция входит в M0 и не должна приводить к удалению legacy evidence до утверждения новой структуры.

После появления исполняемого platform/strategy code к structural validation должны добавляться профильные unit, integration, replay и failure tests.

## 15. Принцип безопасности

При unknown state, broken reconciliation, corrupted data, unavailable protection layer или risk-limit violation система должна прекращать создание нового риска и формировать diagnostic event. Действия с уже открытыми позициями задаются отдельным live protocol.
