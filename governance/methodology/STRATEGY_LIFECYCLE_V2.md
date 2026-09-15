# ATS Strategy Lifecycle v2

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 2.0  
**Статус:** BASELINE FOR REBASELINE  
**Родительские документы:** `PROGRAM_CHARTER_V2.md`, `OPERATING_MODEL_V2.md`

## 1. Назначение

Strategy Lifecycle определяет стандартный путь конкретной торговой идеи:

`Idea → Prototype → Candidate → Research → Validation → Live → Portfolio → Scaling → Retirement`.

Он решает две задачи:

1. не тратить значительные ресурсы на слабые идеи;
2. не допускать недостаточно доказанные стратегии к существенному капиталу.

Основной принцип: чем дороже следующий этап и чем больше финансовый риск, тем сильнее должны быть доказательства.

## 2. Объект Lifecycle

Lifecycle применяется к конкретной `Strategy Version`, а не к ATS Program целиком. Каждая версия имеет собственные правила, код, параметры, данные, cost model, evidence и live-допуск. Существенно новая версия не наследует доказательства автоматически.

## 3. Общая схема

### Part A — Research Funnel

`R0 IDEA → R1 RATIONALE → R2 DATA FEASIBILITY → R3 CHEAP PROTOTYPE → R4 ECONOMIC PRE-SCREEN`.

Большинство идей должно быть отвергнуто здесь. Реальный капитал отсутствует.

### Part B — Formal Strategy Lifecycle

`S01 CANDIDATE ADMISSION → S02 RESEARCH SPECIFICATION → S03 DATA & RESEARCH PROTOCOL → S04 BASELINE IMPLEMENTATION → S05 ECONOMIC VIABILITY → S06 ROBUSTNESS & VALIDATION → S07 INDEPENDENT EXAMINATION → S08 LIVE READINESS & RISK MANDATE → S09 DEMO/SHADOW ACCEPTANCE → S10 MINIMAL LIVE → S11 ACTIVE/PORTFOLIO ADMISSION → S12 CONTROLLED SCALING → CONTINUOUS MONITORING`.

## 4. R0 — Idea

Цель — зафиксировать потенциальную рыночную закономерность.

Минимальный `Idea Card`:

- ID;
- statement;
- market;
- предполагаемый mechanism;
- horizon;
- required data.

Решение: `SCREEN / REJECT / PARK`.

## 5. R1 — Economic Rationale

Главный вопрос: почему преимущество вообще должно существовать?

Допустимые основания: behavioural, structural, liquidity, institutional, information diffusion, risk premium, microstructure или повторяющийся event mechanism.

Недостаточное основание: «на графике выглядит хорошо».

Exit criterion: существует понятная и потенциально опровергаемая hypothesis.

## 6. R2 — Data Feasibility

Проверяются availability, timestamps, survivorship, revisions, corporate actions, spreads, commissions, historical specification, period coverage и отсутствие очевидного look-ahead.

Для event/news strategies дополнительно: actual publication time, consensus availability, revisions, latency, timezone/DST и доступность информации в конкретный момент.

Решение: `FEASIBLE / DATA_GAP / REJECT`.

## 7. R3 — Cheap Prototype

Цель — получить первый количественный ответ с минимальными затратами. Допустимы notebook, Python script, SQL/query, event study или простая backtest-модель.

Production architecture, broker integration, monitoring и recovery не требуются.

Главный вопрос: есть ли сигнал достаточно сильный, чтобы продолжать?

Prototype не должен превращаться в бесконечную оптимизацию.

## 8. R4 — Economic Pre-Screen

Первый фильтр против дорогого исследования экономически слабой стратегии.

Грубо оцениваются:

- magnitude edge;
- net expectancy;
- вероятные costs;
- количество opportunities;
- required capital;
- capacity;
- drawdown characteristics;
- operational complexity.

Решение: `REJECT / PARK / PROMOTE`.

PROMOTE создаёт Strategy Candidate.

## 9. S01 — Candidate Admission

Главный вопрос: заслуживает ли идея полноценного research budget?

Inputs: Idea, rationale, preliminary evidence, data feasibility и economic pre-screen.

Фиксируются:

- Strategy ID;
- class;
- research objective;
- предполагаемый source of edge;
- known risks;
- предполагаемый validation path;
- **Strategy Economic Profile** — что будет означать «экономически интересно» для данного класса стратегии.

Economic Profile описывает required return characteristics, acceptable drawdown class, capital usage, opportunity frequency, cost sensitivity, capacity expectations и допустимую operational complexity.

Решение: `PASS / REJECT / PARK`.

## 10. S02 — Research Specification

Цель — превратить Candidate в однозначную торговую систему.

Определяются:

- market/instrument;
- timeframe или event horizon;
- feature definitions;
- entry/exit;
- stop/position management;
- filters;
- no-trade conditions;
- re-entry;
- session rules;
- exceptional conditions.

Дополнительно фиксируются:

- falsification criteria;
- evaluation metrics;
- evidence-sufficiency concept.

Другой исследователь должен понимать правила без смысловых догадок.

## 11. S03 — Data & Research Protocol

До глубокой validation фиксируются:

- data source и dataset version;
- development period;
- validation period;
- independent/final period, если применимо;
- cost/spread/slippage assumptions;
- execution assumptions;
- timezone;
- cleaning rules.

Development, validation и final evidence не смешиваются. Независимая область защищается от просмотра там, где это требуется методологией.

Для event-driven дополнительно фиксируются event taxonomy, timestamp semantics, consensus source, revision policy и event clustering rules.

Выход: `Data Manifest + Research Protocol`.

## 12. S04 — Baseline Implementation

Цель — получить корректную и воспроизводимую реализацию.

Необходимо:

- реализовать Strategy Version;
- связать code/data/config;
- проверить сделки;
- проверить position sizing;
- учесть costs;
- проверить equity/balance;
- зарегистрировать experiments;
- создать baseline report.

Минимальные проверки: unit tests критической логики, deterministic replay, контроль look-ahead, manual/visual inspection выборки сделок и воспроизводимость повторного запуска.

Решение: `TECHNICALLY_VALID / RETURN / FAIL`.

## 13. S05 — Economic Viability

Новый обязательный gate. Главный вопрос:

> Даже если эффект настоящий, стоит ли развивать эту стратегию дальше?

Проверяются одновременно:

### Profitability

Net expectancy, gross/net return, distribution of P&L.

### Risk

Drawdown, loss concentration, adverse sequences, tail behaviour.

### Capital efficiency

Required capital, time in market, margin usage, return on committed capital.

### Evidence

Effective sample, independent opportunities, dependence on few trades/events.

### Costs

Commissions, spread, slippage sensitivity, turnover.

### Capacity

Liquidity, potential size и market impact, если релевантно.

### Operational burden

Data cost, latency requirements, implementation и monitoring complexity.

PASS требует достаточного ожидаемого экономического потенциала относительно `capital + risk + complexity + opportunity cost`.

Решение: `PASS / REJECT / PARK / RETURN_TO_RESEARCH`.

## 14. S06 — Robustness & Validation

Главный вопрос: edge существует как область поведения или только как красивый набор параметров?

Проверяются neighbouring parameters, time slices, market/volatility regimes, sessions, допустимые instruments, alternative costs, input perturbations, trade concentration и outliers.

При необходимости используются walk-forward, time-series cross-validation, bootstrap и regime segmentation.

Искомый результат — широкая устойчивая область, а не одиночный optimum.

Решение: `PASS / FAIL / RETURN`.

## 15. S07 — Independent Examination

Перед экзаменом замораживаются code revision, configuration, parameters, dataset, cost model и pass/fail criteria. Создаётся immutable exam manifest.

Конкретная версия получает один разрешённый независимый экзамен на соответствующем period/evidence block. После раскрытия результата изменение стратегии создаёт новую version/research cycle.

Проверяются net result, drawdown, distribution, concentration, similarity to validation и заранее заданные pass criteria.

Решение только: `PASS / FAIL`. `Conditional pass` не используется.

## 16. S08 — Live Readiness & Strategy Risk Mandate

Именно здесь впервые обязательным становится конкретный risk mandate для реального капитала, потому что к этому моменту уже известны приблизительные return, drawdown, frequency, tail behaviour и cost sensitivity.

### Live Environment

Jurisdiction, broker, legal instrument, account type, platform, margin/leverage, commissions/swaps, minimum volume и execution model.

### Strategy Risk Mandate

Maximum allocation, risk per trade/event, aggregate exposure, daily loss, strategy drawdown, duration limits, stop conditions и funding rules.

### Stress

Spread expansion, slippage, latency, missed signals, rejects, partial fills, gaps, adverse sequencing и failure/restart scenarios. При необходимости Monte Carlo, block bootstrap и scenario analysis.

### Production readiness

Risk controller, persistent state, idempotency, reconciliation, audit trail, watchdog, emergency stop, monitoring, deployment manifest и recovery procedure.

Stress/tail risk должен укладываться в Strategy Risk Mandate и Program Risk Policy.

## 17. S09 — Demo / Shadow Acceptance

Цель — доказать корректность production implementation в реальной инфраструктуре без существенного financial risk.

Проверяются market data, clocks/timezones, connectivity, restart/recovery, broker responses, duplicate prevention, stale quotes, spread controls, reconciliation, monitoring, alerts и emergency stop.

Где возможно, выполняется shadow comparison: `Expected Decision ↔ Runtime Decision`.

Demo не является доказательством profitability.

## 18. S10 — Minimal Live

Цель — проверить реальное исполнение при минимальной разумной цене ошибки.

Оцениваются fills, spread, commissions, slippage, latency, swaps, rejects, partial execution, reconciliation и broker behaviour.

Сравниваются `Model → Expected execution → Actual execution`.

Allocation остаётся минимальным.

Решение: `PASS / PAUSE / FAIL / RETURN_TO_S08`.

## 19. S11 — Active & Portfolio Admission

Главный вопрос: полезна ли стратегия реальному портфелю?

Оцениваются live execution evidence, correlation, exposure/regime/drawdown overlap, marginal contribution to risk, capital utilization, liquidity conflicts и portfolio capacity.

Решения:

- `ACTIVE` — ограниченный постоянный allocation;
- `WATCH` — продолжение минимального наблюдения;
- `REJECT` — отсутствие portfolio admission.

Хорошая standalone strategy не обязана быть хорошей для текущего portfolio, и наоборот.

## 20. S12 — Controlled Scaling

Увеличение риска не обосновывается старым backtest. Каждая существенная ступень требует нового live evidence после предыдущего allocation.

`Allocation A → New independent live block → Review → Allocation B → New block → Review`.

Проверяются live expectancy, drawdown, costs, capacity, slippage, market impact, correlation и execution degradation.

Решения: `INCREASE / HOLD / REDUCE / PAUSE / RETIRE`.

## 21. Continuous Strategy Health

После S12 lifecycle продолжается. Статусы:

`NORMAL / WATCH / REDUCED / PAUSED / REVALIDATION / RETIRED`.

Постоянно оцениваются expected vs realized return/drawdown, cost/spread/slippage drift, fills, feature/regime behaviour, correlation drift, capacity и infrastructure health.

## 22. Причины деградации

Нужно различать:

- statistical noise;
- market regime shift;
- edge decay;
- execution decay;
- implementation defect;
- data defect;
- portfolio interaction.

Классификация причины определяет, куда возвращать стратегию.

## 23. Retirement

Стратегия переводится в `RETIRED`, если edge перестал быть экономически значимым, execution устойчиво уничтожил edge, рынок структурно изменился, стратегия заменена лучшей, operational cost превышает value или portfolio больше не нуждается в данном exposure.

Evidence и история сохраняются.

## 24. Gate statuses

Formal lifecycle использует:

`NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `PASS`, `FAIL`, `PARKED`, `SUPERSEDED`.

Неопределённость означает `BLOCKED` или `IN_PROGRESS`, но не условный PASS.

## 25. FAIL и возврат

FAIL конкретной Strategy Version не всегда означает смерть hypothesis. Можно создать новую version, если есть новая обоснованная причина.

Если evidence опровергает сам source of edge, идея должна быть REJECTED, а не спасаться бесконечной параметрической оптимизацией.

Минимальные возвраты:

- изменение economic rationale → R1/S01;
- entry/exit/position logic → минимум S02;
- data source/protocol → минимум S03;
- trade-affecting implementation bug → S04 и повтор затронутого evidence;
- изменение acceptance criteria после результата → аннулирование соответствующего evidence;
- broker/account/platform → минимум S08;
- live risk limits → повтор S08/stress;
- allocation → S12 review.

## 26. Class-specific profiles

Core Lifecycle един, но validation profile зависит от класса стратегии.

### Technical/bar-based

Look-ahead, OHLC ambiguity, intrabar modelling, parameter overfitting.

### News/event-driven

Timestamps, consensus availability, revisions, publication latency, spread explosion, event clustering.

### Statistical/relative-value

Stationarity, universe selection, survivorship, multiple testing, structural breaks.

### High-turnover

Transaction costs, fill model, latency, queue/capacity.

Один универсальный статистический тест не применяется ко всем классам.

## 27. Evidence Sufficiency

Количество сделок само по себе не является универсальным критерием. Оцениваются independent opportunities, temporal/regime coverage, dependence, concentration и event diversity.

Тысяча высоко коррелированных сигналов в одном режиме может содержать меньше evidence, чем существенно меньшая выборка независимых событий.

## 28. Economic Viability dimensions

S05 оценивает минимум:

`RETURN + RISK + CAPITAL + COMPLEXITY/COST`, а при существующем портфеле также `PORTFOLIO CONTRIBUTION`.

Нельзя выбирать стратегию по одной метрике.

## 29. Запреты

На всех стадиях запрещается:

- скрывать отрицательные experiments;
- менять критерии после просмотра результата;
- использовать final evidence для tuning;
- увеличивать risk для отыгрыша;
- martingale и unlimited averaging;
- rescue funding после stop condition;
- считать demo profitability proof;
- считать backtest live-execution proof;
- считать несколько удачных live-сделок основанием для scaling.

## 30. Минимальные артефакты

| Stage | Artifact |
|---|---|
| R0 | Idea Card |
| R1 | Economic Rationale |
| R2 | Data Feasibility Note |
| R3 | Prototype + preliminary result |
| R4 | Pre-Screen Decision |
| S01 | Candidate Manifest + Economic Profile |
| S02 | Strategy Specification |
| S03 | Data Manifest + Research Protocol |
| S04 | Baseline Version + Baseline Report |
| S05 | Economic Viability Report |
| S06 | Validation / Robustness Report |
| S07 | Independent Exam Manifest + Report |
| S08 | Live Protocol + Risk Mandate + Stress Report |
| S09 | Demo/Shadow Acceptance Report |
| S10 | Real Execution Report |
| S11 | Portfolio Admission Decision |
| S12 | Scaling Decision + new live evidence |

## 31. Freeze points

- **Research Freeze:** перед formal validation фиксируются основные правила.
- **Exam Freeze:** перед S07 фиксируется всё, способное влиять на independent result.
- **Live Freeze:** перед S09/S10 фиксируются production version, risk rules и live protocol.
- **Scaling Baseline:** перед каждым повышением allocation фиксируется исходный risk level и следующий evidence requirement.

## 32. Mapping ATS v1 → v2

| ATS v1 | ATS v2 |
|---|---|
| G01 Risk Mandate | S08 |
| G02 Broker/Jurisdiction | S08 |
| G03 Hypothesis | S02 |
| G04 Architecture/Risk | Shared Platform + S08 |
| G05 Data Protocol | S03 |
| G06 Baseline Backtest | S04 |
| — | **S05 Economic Viability** |
| G07 Robustness | S06 |
| G08 Independent Exam | S07 |
| G09 Stress/Live Protocol | S08 |
| G10 Demo | S09 |
| G11 Cent Execution | S10 |
| G12 Scaling | S11–S12 |
| G13 Profit as Income | Program/Portfolio Governance, вне Strategy Lifecycle |

Старый lifecycle после завершения rebaseline должен быть помечен `SUPERSEDED`, а не искусственно пройден.

## 33. Первый vertical slice

Для Reference Strategy #1 сначала обязателен путь:

`R0 → R4 → S01 → S05`.

То есть ATS сначала должен доказать способность взять идею, быстро проверить её, формализовать, воспроизвести baseline и определить экономическую ценность. Только после PASS S05 оправдана дорогая validation/execution infrastructure.
