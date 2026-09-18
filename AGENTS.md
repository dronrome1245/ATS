# AGENTS.md — правила работы ИИ и программных агентов в ATS

## 1. Назначение

Агент помогает формализовать гипотезы, вести исследования, проектировать platform capabilities, реализовывать стратегии, проверять evidence и поддерживать целостность репозитория.

Агент не принимает за OWNER решения о капитале, live admission, scaling или изменении критических risk policies.

## 2. Первый файл для нового чата

При первом входе в репозиторий, после потери контекста или перед продолжением незнакомой работы **сначала прочитать `AI_HANDOFF.md`**.

Если `AI_HANDOFF.md`, `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`, `governance/backlog/PROGRAM_BACKLOG_V2.md` и `02_СЛЕДУЮЩИЙ_ШАГ.md` противоречат друг другу, содержательную работу не продолжать до устранения расхождения.

## 3. Обязательный порядок чтения

1. `AI_HANDOFF.md`;
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`;
5. relevant program files in `governance/program/`;
6. `governance/methodology/RESEARCH_METHODOLOGY_V1.md` для research;
7. `governance/methodology/STRATEGY_LIFECYCLE_V2.md` для Strategy Version work;
8. canonical templates;
9. только затем связанные code/data/test/report artifacts.

Не загружать весь репозиторий без необходимости.

## 4. Canonical state и governance

Единственный machine-readable source of truth:

`03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.

Current ATS v2 governance находится только в:

- `governance/program/`;
- `governance/methodology/`;
- `governance/backlog/`.

Человекочитаемые state views:

- `01_СТАТУС_ПРОЕКТА.md`;
- `02_СЛЕДУЮЩИЙ_ШАГ.md`;
- `AI_HANDOFF.md`.

ATS v1 физически архивирован в `legacy/v1/`. G01–G13 и другие legacy artifacts являются history/reference и не являются current roadmap, current policy или разрешением на торговлю.

## 5. Модель ATS v2

ATS — не одна стратегия и не один robot project.

Программа состоит из:

- Research Factory;
- Shared Trading Platform;
- Strategy Lifecycle;
- Portfolio & Capital;
- Operations & Governance.

Текущая работа управляется milestones M0–M8, Program WBS и canonical backlog.

## 6. Research discipline

Агент обязан различать exploratory observation, registered experiment, validation evidence, independent evidence, demo/shadow evidence и live evidence.

Exploratory result нельзя представлять как formal proof без соответствующего experiment manifest.

Каждый formal experiment должен иметь однозначные code/data/config/cost assumptions и conclusion. Negative experiments не удаляются.

Idea, Hypothesis, Candidate, Experiment и Strategy Version являются разными сущностями и не должны сливаться в один неформальный документ.

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

## 8. Strategy Version и change control

Material change, способное повлиять на trades, создаёт новую Strategy Version и требует повторной проверки затронутого evidence.

К material changes относятся entry/exit, filters, position management, risk logic, material parameters, data source/protocol и cost/execution assumptions.

Minor refactor, не способный изменить торговые решения, может не требовать полного lifecycle, но должен быть документирован.

## 9. Independent Examination

Перед independent examination должны быть заморожены version, parameters, data block, cost model и decision criteria.

После раскрытия результата evidence block считается известным. Изменение стратегии создаёт новую research iteration.

## 10. Platform development

Платформа развивается demand-driven:

`Strategy need → Minimum capability → Reuse → Shared capability → Hardening`.

Агент не должен создавать крупную универсальную infrastructure без конкретного consumer и проверяемого deliverable.

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

## 14. Naming and templates

Formal experiments используют уникальный ID вида `EXP-YYYYMMDD-nnn`.

Research entities используют stable IDs, определённые methodology/templates. ID не переиспользуются для другого объекта после rejection/retirement.

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
8. validator/tests, если изменились paths или invariants;
9. полный Local CI Gate на exact commit перед push.

Нельзя сообщать OWNER, что шаг завершён, если backlog/state/handoff всё ещё указывают на предыдущую task.

## 16. Локальная проверка репозитория

GitHub Actions не является completion gate. Перед завершением material task на exact commit выполнить:

```bash
uv run --frozen python tools/verify_repo.py
```

Быстрая developer-проверка:

```bash
uv run --frozen python tools/verify_repo.py --fast
```

Canonical policy: `governance/program/LOCAL_CI_GATE.md`. Full gate включает repository validator, pytest, Ruff lint/format и environment fingerprint. Результат `ATS LOCAL CI: PASS` обязателен перед обычным push material task.

Постоянная память по повторяемым Local CI failure classes и preventive rules находится в `governance/program/LOCAL_CI_TROUBLESHOOTING.md`. Перед изменением кода после FAIL агент обязан определить первый failing stage и классифицировать ошибку. Network/synchronization failure не является основанием менять исходники. Новый повторяемый failure lesson с подтверждённым root cause и preventive rule должен быть добавлен или уточнён в troubleshooting registry; raw runtime reports в Git не коммитятся.

Для OWNER на Windows стандартный task-completion interface — стабильный корневой `ATS_TASK_CHECK.bat`. Не менять BAT под каждую задачу; task-specific проверки размещать в `tools/current_task_check.py` и обновлять этот Python-файл при смене текущего work package. Не заставлять OWNER вручную копировать цепочки local-CI команд, если launcher может выполнить их сам. После material step просить OWNER запустить `ATS_TASK_CHECK.bat` и прислать `reports/local_ci/CURRENT_TASK_REPORT.txt` для подтверждения или диагностики.

## 17. Принцип безопасности

При unknown state, broken reconciliation, corrupted data, unavailable protection layer или risk-limit violation система должна прекращать создание нового риска и формировать diagnostic event. Действия с уже открытыми позициями задаются отдельным live protocol.
