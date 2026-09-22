# ATS Program Charter v2

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 2.0  
**Статус:** BASELINE FOR REBASELINE  
**Дата:** 14 сентября 2026 года

## 1. Назначение программы

ATS — программа исследований, разработки и эксплуатации алгоритмических торговых систем. Она должна создать воспроизводимый процесс и общую программную платформу, позволяющие формулировать торговые гипотезы, быстро и дёшево отбраковывать слабые идеи, разрабатывать стратегии разных классов, объективно проверять наличие торгового преимущества, переводить подтверждённые стратегии к реальному исполнению и объединять независимые стратегии в портфель.

ATS не является проектом разработки одного торгового робота. Единицей развития программы является способность систематически создавать и проверять новые стратегии, а единицей допуска к капиталу — конкретная версия конкретной стратегии.

## 2. Миссия

Построить повторяемую исследовательскую и инженерную систему, позволяющую находить, создавать, проверять, запускать и масштабировать алгоритмические торговые стратегии различных классов с целью формирования диверсифицированного портфеля экономически значимых источников торгового преимущества.

## 3. Главные вопросы

### Уровень программы

> Способны ли мы регулярно превращать торговые идеи в объективно проверенные стратегии и формировать из подтверждённых источников edge экономически интересный портфель?

### Уровень стратегии

> Имеет ли конкретная версия стратегии экономически значимое статистическое преимущество после реалистичных расходов, ухудшения условий и перехода к реальному исполнению при контролируемом риске?

Отрицательный ответ по отдельной стратегии является нормальным и полезным результатом, если он получен до существенных затрат времени, инфраструктуры или капитала.

## 4. Целевые активы программы

1. **Research capability** — способность как формулировать идеи вручную, так и систематически выявлять bounded закономерности рыночной/ценовой динамики, превращая их в проверяемые гипотезы с сохранением search history, а затем объективно проверять эти гипотезы.
2. **Shared trading platform** — повторно используемая инфраструктура данных, исследований, тестирования и исполнения.
3. **Strategy portfolio** — набор независимо подтверждённых стратегий различных типов.
4. **Operational capability** — способность безопасно запускать, наблюдать, останавливать и масштабировать реальные стратегии.

Новые стратегии должны со временем добавляться быстрее и качественнее за счёт накопленной инфраструктуры, данных, методологии и опыта.

## 5. Классы стратегий

Архитектура программы должна допускать, в частности:

- trend following;
- breakout;
- momentum;
- mean reversion;
- volatility-based;
- statistical / relative-value;
- event-driven;
- macro/news-driven;
- session/time effects;
- cross-market;
- и другие проверяемые гипотезы.

Наличие класса в списке не означает наличия у него edge. Каждая гипотеза проверяется независимо.

## 6. Пять постоянных контуров

### A. Research Factory

`Bounded Pattern Discovery / Idea Intake → Rationale → Data Feasibility → Cheap Test → Economic Screen → Candidate`

Оптимизируется на скорость получения evidence, низкую стоимость отбраковки, воспроизводимость и сохранение отрицательных результатов.

### B. Shared Trading Platform

Целевые возможности: market/event data, normalization, feature computation, backtest/replay, Strategy API, experiment tracking, analytics, risk engine, execution, adapters, state, reconciliation, audit, monitoring и recovery.

Платформа развивается по фактическим потребностям стратегий и не является самоцелью.

### C. Strategy Lifecycle

Каждый перспективный кандидат проходит отдельный контролируемый lifecycle: формализация → economic viability → data protocol → implementation → validation → independent exam → stress/live readiness → demo/shadow → minimal live → portfolio admission → scaling → continuous monitoring.

### D. Portfolio & Capital

Учитывает корреляции, exposure, drawdown, концентрацию, marginal contribution to risk, capital utilization, capacity и conflicts между стратегиями.

### E. Operations & Governance

Обеспечивает версионирование, manifests, evidence, change control, deployment, monitoring, incidents, rollback и post-trade reconciliation.

## 7. Основные принципы

### Profit and risk are joint constraints

ATS не оптимизируется только на безопасность и не оптимизируется только на прибыль. Стратегия должна одновременно показывать экономически значимый edge, приемлемый риск, достаточную доказательность и реализуемость в реальном исполнении.

### Risk is a constraint, not the product

Минимизация риска сама по себе не является целью. Risk management должен ограничивать необратимые потери, предотвращать неконтролируемые сценарии и определять допустимый масштаб подтверждённого edge.

### Economic viability is mandatory

Положительный backtest недостаточен. Оцениваются net return, drawdown, capital utilization, sample/evidence, costs, turnover, capacity, scalability, operational complexity и portfolio contribution.

### Research is cheaper than production

Research без реального exposure не должен блокироваться отсутствием allocation для конкретной live-стратегии. Требования к капиталу и риску усиливаются по мере приближения к live.

### Fail cheaply

Большинство идей не обязаны становиться стратегиями. Полноценная validation, production engineering и реальный капитал доступны только кандидатам, прошедшим более дешёвые фильтры.

### Evidence before conviction

Красивый equity curve, привлекательная идея или несколько прибыльных сделок не являются достаточным доказательством.

### Avoid overfitting

Гипотеза, protocol, разбиение данных и критерии должны фиксироваться до использования соответствующего независимого evidence.

### One result belongs to one version

Каждый значимый результат привязан к конкретным коду, версии стратегии, параметрам, данным, cost model и условиям исполнения.

### Strategy and protection are separate

Стратегия формирует намерение; защитный и портфельный risk-контуры определяют допустимость создания риска.

### Real execution is a separate hypothesis

Исторический результат не доказывает возможность получить тот же результат у брокера. Spread, commission, slippage, latency, fills, rejects, liquidity, recovery и reconciliation проверяются отдельно.

### No loss-chasing

Запрещены мартингейл, неконтролируемое усреднение, автоматическое повышение риска после убытка и автоматическое rescue funding после stop condition.

### Negative evidence is retained

Неудачные гипотезы и эксперименты сохраняются как часть исследовательской базы.

## 8. Research Funnel

- **R0 Idea** — наблюдение или источник потенциального edge.
- **R1 Rationale** — экономическая/структурная причина.
- **R2 Data Feasibility** — возможность честной проверки.
- **R3 Cheap Prototype** — минимальная реализация основного эффекта.
- **R4 Economic Screen** — есть ли потенциал, оправдывающий дальнейшие ресурсы.
- **R5 Candidate** — допуск к формальному Strategy Lifecycle.

## 9. Успех отдельной стратегии

Оценивается по группам:

- **Edge:** net expectancy, profitability, устойчивость, объяснимый механизм.
- **Risk:** drawdown, tail loss, adverse sequences, concentration.
- **Evidence:** effective sample, independence, OOS, sensitivity, regime coverage.
- **Economics:** return on required capital, utilization, costs, capacity, operational burden.
- **Portfolio value:** correlation, diversification, exposure overlap, incremental return/risk.
- **Execution:** expected vs actual costs, latency, slippage, rejects, model/live divergence.

Численные критерии задаются отдельной методологией и protocol конкретной стратегии, а не этим Charter.

## 10. Успех программы

ATS должен улучшать:

- research throughput;
- time to first evidence;
- rejection efficiency;
- reproducibility;
- измеримый funnel `Ideas → Prototypes → Candidates → Validated → Demo → Live`;
- reuse платформенных возможностей;
- diversity источников edge;
- качество совокупного портфеля после расходов и рисков.

## 11. Scope

В программу входят research, market/event data, data quality, backtesting/replay, experiment management, statistical validation, robustness, Strategy API, risk/portfolio management, broker integration, execution, demo/shadow/live testing, monitoring, reconciliation, incidents, evidence и staged scaling.

Не являются целью: гарантирование прибыли, доказательство заранее выбранного убеждения, выбор только по максимальному backtest return, скрытие отрицательных результатов, компенсация отсутствия edge плечом, продажа сигналов, управление средствами третьих лиц или замена юридической/налоговой проверки.

## 12. Модель развития платформы

`Strategy need → Minimum capability → Strategy evidence → Generalize → Next strategy`

Не допускается преждевременная разработка большой универсальной платформы без проверяемой потребности.

## 13. Reference Strategies

### Reference Strategy #1

Относительно простая стратегия с доступными данными и понятным execution model. Цель — проверить research workflow, Strategy API, backtester/replay, experiment tracking и validation. Отрицательный экономический результат не является провалом этапа, если процесс сработал корректно.

### Reference Strategy #2

Стратегия другого класса, предпочтительно event/news-driven или требующая иного типа данных/исполнения. Цель — проверить, что архитектура действительно является платформой, а не решением под Strategy #1.

## 14. Уровни риска

- **Research Risk:** ошибки выводов, данных, переоптимизация, потеря времени; реального exposure нет.
- **Strategy Live Risk:** риск капитала конкретной live-стратегии; задаётся strategy risk mandate.
- **Portfolio Risk:** совокупный риск всех работающих стратегий; имеет приоритет над локальными решениями.

## 15. Capital progression

`Research → Validation → Demo/Shadow → Minimal Live → Evidence → Higher Allocation`

Существенное увеличение allocation требует новых доказательств после предыдущего уровня риска.

## 16. Milestones

- **M0 Program Rebaseline** — новая миссия, operating model, lifecycle, WBS и структура репозитория.
- **M1 Research Methodology** — funnel, experiment protocol, economic screening и statistical validation.
- **M2 Research Platform MVP** — быстрые воспроизводимые исследования простых стратегий.
- **M3 Reference Strategy #1** — полный research/validation flow первой стратегии.
- **M4 Validation Framework** — robustness, OOS, stress и evidence management как стандарт.
- **M5 Execution Platform** — demo/shadow и минимальный live-контур.
- **M6 Reference Strategy #2** — стратегия другого класса.
- **M7 Portfolio Layer** — совместный анализ и управление несколькими стратегиями.
- **M8 Controlled Live Portfolio** — ограниченный портфель live-стратегий с portfolio-level risk management.

## 17. Определение успеха ATS

ATS успешен, когда создан воспроизводимый механизм, способный регулярно формировать проверяемые гипотезы, быстро отбраковывать слабые, объективно подтверждать перспективные, повторно использовать инфраструктуру, обнаруживать model/live divergence, контролировать риск и постепенно предоставлять капитал доказанным edge.

## 18. Определение провала ATS

Системным провалом являются ситуации, когда программа не способна отличать edge от переоптимизации, систематически пропускает ложные стратегии в live, не воспроизводит собственные эксперименты, скрывает отрицательные результаты, требует строить всё заново для каждой стратегии или допускает неконтролируемый риск.

## 19. Статус старых G01–G13

Существующая модель G01–G13 сохраняется как историческая основа, но больше не является roadmap всей программы. Её сильные части переходят в `Strategy Lifecycle v2`. После завершения rebaseline старый lifecycle должен быть помечен как superseded, без фиктивного выставления `PASS` старым воротам.

## 20. Ближайшая цель

Завершить **M0 Program Rebaseline**: Operating Model v2, Strategy Lifecycle v2, Research Methodology v1, Program WBS, Repository Structure v2 и новая machine-readable state model.
