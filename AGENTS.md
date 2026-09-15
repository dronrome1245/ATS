# AGENTS.md — правила работы ИИ и программных агентов в ATS

## 1. Назначение

Агент помогает формализовать гипотезы, вести исследования, проектировать platform capabilities, реализовывать стратегии, проверять evidence и поддерживать целостность репозитория.

Агент не принимает за OWNER решения о капитале, live admission, scaling или изменении критических risk policies.

## 2. Первый файл для нового чата

При первом входе в репозиторий, после потери контекста или перед продолжением незнакомой работы **сначала прочитать `AI_HANDOFF.md`**.

Если `AI_HANDOFF.md`, `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`, `governance/backlog/PROGRAM_BACKLOG_V2.md` и `02_СЛЕДУЮЩИЙ_ШАГ.md` противоречат друг другу, содержательную работу не продолжать до устранения расхождения.

## 3. Обязательный порядок чтения

1. `AI_HANDOFF.md`;
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` — canonical machine-readable state;
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
4. `governance/backlog/PROGRAM_BACKLOG_V2.md` — canonical execution queue;
5. `governance/program/PROGRAM_CHARTER_V2.md`;
6. `governance/program/OPERATING_MODEL_V2.md`;
7. `governance/program/PROGRAM_WBS_V2.md` — для program work;
8. `governance/program/REPOSITORY_STRUCTURE_V2.md` — для structural/migration work;
9. `governance/methodology/RESEARCH_METHODOLOGY_V1.md` — для research;
10. `governance/methodology/STRATEGY_LIFECYCLE_V2.md` — для конкретной стратегии;
11. только затем связанные code/data/test/report artifacts.

Не загружать весь репозиторий без необходимости.

## 4. Canonical state и current governance

Единственный canonical machine-readable state ATS:

`03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.

Current ATS v2 governance находится только в:

- `governance/program/`;
- `governance/methodology/`;
- `governance/backlog/`.

Человекочитаемые представления:

- `01_СТАТУС_ПРОЕКТА.md`;
- `02_СЛЕДУЮЩИЙ_ШАГ.md`;
- `AI_HANDOFF.md`.

Старая модель G01–G13 и документы ATS v1 являются history/reference до их migration в `legacy/v1/`; они не являются current roadmap.

## 5. Модель ATS v2

ATS — не одна стратегия и не один robot project.

Программа состоит из:

- Research Factory;
- Shared Trading Platform;
- Strategy Lifecycle;
- Portfolio & Capital;
- Operations & Governance.

Текущая работа управляется milestones M0–M8, `governance/program/PROGRAM_WBS_V2.md` и canonical backlog.

## 6. Research discipline

Агент обязан различать exploratory observation, registered experiment, validation evidence, independent evidence, demo/shadow evidence и live evidence.

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

К material changes относятся entry/exit, filters, position management, risk logic, material parameters, data source/protocol и cost/execution assumptions.

Minor refactor, не способный изменить торговые решения, может не требовать полного lifecycle, но должен быть документирован.

## 9. Independent Examination

Перед independent examination должны быть заморожены version, parameters, data block, cost model и decision criteria.

После раскрытия результата этот evidence block считается известным. Изменение стратегии создаёт новую research iteration.

## 10. Platform development

Платформа развивается demand-driven:

`Strategy need → Minimum capability → Reuse → Shared capability → Hardening`.

Агент не должен создавать крупную универсальную infrastructure без конкретного потребителя и проверяемого deliverable.

## 11. Risk separation

`Strategy Intent → Strategy Risk → Portfolio Risk → Execution`.

Отрицательное решение risk layer окончательно для создания нового риска. Неисправность strategy logic не должна отключать protective controls.

## 12. Live boundary

Research и validation без реального exposure могут выполняться без strategy-level allocation.

Перед minimal live должны существовать lifecycle evidence, live protocol и OWNER-approved Strategy Risk Mandate.

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

Canonical templates находятся в `governance/methodology/templates/`.

## 15. Completion / handoff protocol

Любой существенный program-level шаг считается завершённым только после синхронизации:

1. основного deliverable;
2. `governance/backlog/PROGRAM_BACKLOG_V2.md`;
3. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
4. `01_СТАТУС_ПРОЕКТА.md`;
5. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
6. `AI_HANDOFF.md`;
7. README/start guide, если изменилась точка входа;
8. validator/tests, если изменились paths или invariants.

Нельзя сообщать OWNER, что шаг завершён, если backlog/state/handoff всё ещё указывают на предыдущую task.

## 16. Проверка репозитория

Перед завершением изменения проверить:

```bash
python tools/validate_repo.py
```

Validator должен подтверждать canonical v2 state, governance paths, обязательные artifacts и согласованность `next_artifact`/`next_task_id` между state, backlog, handoff и next action.

## 17. Принцип безопасности

При unknown state, broken reconciliation, corrupted data, unavailable protection layer или risk-limit violation система должна прекращать создание нового риска и формировать diagnostic event. Действия с уже открытыми позициями задаются отдельным live protocol.
