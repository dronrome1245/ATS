# ATS Operating Model v2

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 2.0  
**Статус:** BASELINE FOR REBASELINE  
**Родительский документ:** `PROGRAM_CHARTER_V2.md`

## 1. Назначение

Operating Model описывает, как ATS работает как постоянная программа исследований и разработки: какие сущности существуют, как идея превращается в стратегию, чем research отличается от validation, когда возникает live-risk, как развивается платформа и как несколько стратегий объединяются в портфель.

## 2. Пять контуров

1. **Research Factory** — поиск, дешёвая проверка и ранняя отбраковка идей.
2. **Shared Trading Platform** — повторно используемые данные, backtest/replay, Strategy API, analytics, risk, execution и operations.
3. **Strategy Lifecycle** — глубокая проверка перспективной стратегии.
4. **Portfolio & Capital** — allocation и portfolio-level risk.
5. **Operations & Governance** — версии, evidence, deployment, monitoring, incidents и change control.

## 3. Основные сущности

### Program

Постоянная программа `ATS`. Не завершается после первой стратегии.

### Idea

Неформализованное наблюдение о потенциальной закономерности. Ещё не является стратегией.

### Hypothesis

Проверяемое утверждение о рынке, включающее предполагаемый механизм edge, рынок, условия, ожидаемый эффект и способ опровержения.

### Prototype

Минимальная реализация гипотезы для ответа на вопрос: виден ли эффект, достойный дальнейшего исследования?

### Strategy Candidate

Гипотеза, прошедшая дешёвый screening и получившая право на более дорогой research/validation.

### Strategy

Формально определённая торговая система с уникальным ID, классом, рынком, правилами и историей версий.

### Strategy Version

Неизменяемая конкретная версия стратегии, связанная с code revision, configuration, parameters, data, cost assumptions и evidence.

### Experiment

Один воспроизводимый исследовательский запуск с ID, hypothesis, strategy version, code revision, dataset, period, parameters, cost model, result и conclusion.

### Dataset

Версионированный набор данных с происхождением, периодом, timezone, правилами очистки и устойчивым идентификатором.

### Evidence

Артефакт, подтверждающий или опровергающий утверждение: backtest, robustness map, OOS report, stress report, execution comparison, demo/live log и т.д.

### Platform Capability

Повторно используемая возможность платформы, возникшая из фактической потребности одной или нескольких стратегий.

### Deployment

Конкретный запущенный экземпляр Strategy Version: simulation, shadow, demo, minimal live или production live.

### Portfolio

Совокупность одобренных live-стратегий и правил распределения капитала и риска.

## 4. Идентификаторы

Рекомендуемая иерархия:

```text
ATS
├── IDEA-xxx
├── HYP-xxx
├── STRAT-xxx
│   ├── v1.0
│   └── v2.0
├── EXP-YYYYMMDD-nnn
├── DATA-xxx-vn
├── DEPLOY-xxx
└── PORT-xxx
```

## 5. Жизненный цикл идеи

```text
DRAFT
  ↓
SCREENING
  ├── REJECTED
  ├── PARKED
  └── PROTOTYPE
          ↓
     ECONOMIC_SCREEN
          ├── REJECTED
          ├── PARKED
          └── CANDIDATE
```

### DRAFT

Идея зафиксирована, но не проверена.

### SCREENING

Проверяются mechanism, data availability, cheap-test feasibility и очевидные sources of bias.

### PROTOTYPE

Создаётся минимальная количественная проверка.

### ECONOMIC_SCREEN

Оценивается, достаточно ли велик потенциальный эффект относительно costs, capital и complexity.

### CANDIDATE

Идея допускается к формальному Strategy Lifecycle.

## 6. Крупные состояния стратегии

```text
CANDIDATE → RESEARCH → VALIDATION → VALIDATED → LIVE_PREPARATION
→ DEMO/SHADOW → MINIMAL_LIVE → ACTIVE → SCALED
```

Дополнительные состояния:

`FAILED`, `PAUSED`, `SUPERSEDED`, `RETIRED`.

### RESEARCH

Разрешены изменение логики, exploratory analysis и подбор разумной спецификации. Реальный капитал запрещён.

### VALIDATION

Основные правила уже стабилизированы. Проводятся robustness, независимые срезы и economic validation. Существенное изменение логики возвращает стратегию в research.

### VALIDATED

Исследовательские критерии выполнены, но права на live ещё нет.

### LIVE_PREPARATION

Проектируются execution, stress, recovery, logs, risk controls и deployment.

### DEMO/SHADOW

Реальная инфраструктура без значимого финансового exposure.

### MINIMAL_LIVE

Минимальный реальный риск для проверки исполнения и поведения модели.

### ACTIVE

Стратегия получает ограниченный постоянный allocation.

### SCALED

Allocation повышен на основании новой live-статистики.

### PAUSED

Создание нового риска остановлено из-за anomaly, execution divergence, drawdown или operational issue.

### RETIRED

Эксплуатация завершена, evidence сохраняется.

## 7. Decision Points

### DP1 — Idea Admission

Есть ли смысл проверять идею? Решение: `SCREEN / PARK / REJECT`.

### DP2 — Candidate Promotion

Есть ли достаточно предварительного evidence для дорогого research? Оцениваются magnitude, costs, sample, stability, complexity, data quality и operational feasibility.

### DP3 — Validation Admission

Стратегия достаточно формализована, чтобы прекратить свободную подгонку и начать objective validation? После решения фиксируются основные правила и protocol.

### DP4 — Live Preparation

Достаточно ли research evidence, чтобы инвестировать в production-quality execution?

### DP5 — Live Admission

Можно ли допустить конкретную Strategy Version к реальному financial risk? Только здесь strategy-level risk mandate становится обязательным.

### DP6 — Scaling

Достаточны ли новые live evidence для увеличения allocation? Старый backtest не является достаточным основанием.

### DP7 — Portfolio Admission

Полезна ли стратегия текущему портфелю с учётом correlation, factor overlap, capital competition и marginal contribution?

## 8. Research, Validation и Production

### Research

Цель — понять рынок и проверить edge. Допускаются notebooks, prototype code, exploratory analysis и изменение параметров. Результат research не считается live proof без validation.

### Validation

Цель — проверить, не является ли edge артефактом research. Требуются зафиксированная версия, protocol, независимые данные и reproducibility.

### Production

Цель — воспроизводимо исполнять уже определённую стратегию. Требуются risk control, persistent state, idempotency, monitoring, reconciliation, recovery, immutable releases и incident handling.

## 9. Separation of risk responsibilities

```text
Market Data
   ↓
Strategy → Trading Intent
   ↓
Strategy Risk
   ↓
Portfolio Risk
   ↓
Execution
   ↓
Broker
```

Strategy определяет желаемое действие. Strategy Risk определяет допустимость локального риска. Portfolio Risk определяет допустимость с учётом всех стратегий. Запрет любого risk-контроля окончателен.

## 10. Platform Development Model

Платформа строится demand-driven:

`Strategy need → Minimum capability → Reuse opportunity → Shared capability → Next strategy → Generalization`

Состояния capability:

`NEED → PROTOTYPE → REUSABLE → SHARED → HARDENED`.

Не каждый prototype обязан становиться shared component.

## 11. Минимальный Research Platform MVP

До Reference Strategy #1 достаточно:

1. experiment manifest;
2. data loading;
3. базового backtest/replay;
4. transaction cost model;
5. Strategy interface;
6. performance report;
7. experiment registry;
8. binding `code + data + config + result`.

Execution engine, news ingestion, portfolio engine и production monitoring добавляются по реальной потребности.

## 12. Reference Strategy #1

Должна иметь доступные данные, сравнительно простую логику, понятный execution model и возможность ручной проверки. Её задача — пройти вертикальный путь Idea → Evidence и проверить минимальную платформу.

## 13. Reference Strategy #2

Должна предъявить другой класс требований, предпочтительно event/news-driven или иной тип данных/исполнения. Цель — проверить универсальность архитектуры и отделить shared capabilities от strategy-specific кода.

## 14. Параллельная работа и WIP

Нормальное состояние программы допускает одновременно много дешёвых идей, меньше prototypes, несколько candidates и единицы production/live кандидатов. Конкретные WIP limits определяются после измерения фактической пропускной способности.

## 15. Минимальные артефакты

### Idea

`Idea ID, statement, rationale, market, required data, cheap test, result, decision`.

### Candidate

Hypothesis specification, preliminary evidence, data feasibility, known risks, estimated research cost и promotion decision.

### Validated Strategy

Strategy specification, version manifest, data manifest, experiment history, robustness, independent/OOS evidence, economic viability и known failure modes.

### Live Strategy

Дополнительно: strategy risk mandate, deployment manifest, stop policy, recovery, monitoring, execution reconciliation и allocation decision.

### Portfolio

Inventory, allocations, correlation/exposure, risk contribution, drawdown aggregation, concentration и portfolio stop policy.

## 16. Роли и decision rights

- **OWNER:** mission, scope, capital, live admission, allocation, scaling и критические risk policies.
- **RESEARCHER:** ideas, prototypes, research, promotion recommendations.
- **DEVELOPER:** platform, strategy implementation, tests, production code.
- **DATA REVIEWER:** provenance, integrity, timestamps и dataset versioning.
- **VALIDATION / INDEPENDENT REVIEWER:** protocol, leakage control, evidence quality.
- **RISK REVIEWER:** strategy и portfolio risk, tail scenarios, stop conditions.
- **EXECUTION REVIEWER:** model/live comparison, slippage, latency, fills и costs.
- **OPERATIONS:** deployment, monitoring, runtime, incidents, recovery.

Один человек может совмещать роли, но логические decision rights остаются раздельными.

## 17. Program Risk и Strategy Risk

### Program-level

Общий капитал ATS, portfolio drawdown, concentration constraints и program-level emergency stops.

### Strategy-level

Allocation, trade/event risk, daily loss, strategy drawdown, position/exposure limits и stop conditions.

Локальные лимиты всегда подчиняются program-level policy.

## 18. Research не требует live-risk mandate

Research без реального exposure может идти до выбора allocation конкретной стратегии. Но demo не считается profitability proof, backtest не является основанием для неограниченного капитала, а minimal live запрещён без strategy risk mandate.

## 19. Experiment Discipline

Формальный evidence experiment должен однозначно фиксировать минимум:

`experiment_id, hypothesis_id, strategy_version, code_revision, dataset_id, period, parameters, cost_model, environment, result, conclusion`.

Exploratory scratch-runs могут быть легче, но не являются формальным evidence без регистрации.

## 20. Evidence hierarchy

`Exploratory observation → Registered backtest → Validation evidence → Independent OOS → Stress evidence → Demo/shadow → Minimal live → Scaled live`.

## 21. Change Control

- **Minor:** не меняет сделки; может не требовать полной revalidation.
- **Material:** может менять сделки; создаёт новую Strategy Version и повтор затронутых стадий.
- **Structural:** меняет источник edge или архитектуру; может потребовать возврата к Candidate/Research.

## 22. Stop Conditions

Создание нового риска прекращается при unknown position, broken reconciliation, corrupted data, limit violation, unavailable protection layer, execution anomaly, materially degraded model/live behaviour или critical platform failure.

Остановка новых сделок не означает автоматическое закрытие существующих позиций: поведение открытых позиций задаётся live protocol.

## 23. Strategy Health after Launch

ACTIVE не является вечным статусом. Постоянно оцениваются expected vs realized performance, execution quality, drawdown, regime behaviour, edge degradation, capacity и correlation drift.

Решения: `CONTINUE / REDUCE / PAUSE / REVALIDATE / RETIRE`.

## 24. Program State v2

Предлагаемые состояния программы:

`REBASELINE → BUILDING_RESEARCH_CAPABILITY → BUILDING_PLATFORM → VALIDATING_STRATEGIES → LIVE_EXPERIMENTATION → PORTFOLIO_OPERATION`.

На зрелых стадиях часть состояний может пересекаться.

## 25. Что меняется относительно v1

Было: один проект, одна стратегия, 13 последовательных ворот, G01 risk mandate блокирует начало.

Становится: одна программа, много идей/candidates, несколько Strategy Lifecycles, одна Shared Platform, несколько live-стратегий и portfolio-level capital allocation. Risk mandate появляется там, где возникает реальный exposure.

## 26. Что сохраняется

Reproducibility, independent testing, version control, protected final data, независимый risk controller, stress, execution validation, staged scaling, запрет martingale/rescue funding и сохранение negative evidence.

## 27. Ближайший operational flow

`M0 Program Rebaseline → M1 Research Methodology → M2 Minimal Research Platform → Idea #1 → Cheap Prototype → Candidate → Reference Strategy #1 → Validation → Platform improvements → Reference Strategy #2`.

Ближайшая цель — доказать способность ATS честно и воспроизводимо проверять разные торговые гипотезы.
