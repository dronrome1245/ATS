# ATS Research Methodology v1

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 1.0  
**Статус:** BASELINE FOR REBASELINE  
**Родительские документы:** `PROGRAM_CHARTER_V2.md`, `OPERATING_MODEL_V2.md`, `STRATEGY_LIFECYCLE_V2.md`

## 1. Назначение

Research Methodology определяет, как ATS превращает торговое наблюдение в evidence и как отличает перспективный edge от результата, возникшего из шума, переоптимизации, плохих данных, неверной модели расходов или исследовательской свободы.

Методология должна одновременно:

1. увеличивать скорость проверки идей;
2. снижать вероятность ложноположительных стратегий;
3. отбраковывать экономически слабые идеи до дорогой разработки;
4. сохранять возможность исследовать разные классы стратегий;
5. делать результаты воспроизводимыми и сопоставимыми.

Методология не гарантирует прибыль и не задаёт один универсальный статистический тест или одну минимальную доходность для всех стратегий.

## 2. Основной принцип

Каждая стратегия должна доказать две независимые вещи:

### A. Evidence of edge

Есть основания считать, что наблюдаемый результат не является только следствием шума, leakage, selection bias или подгонки.

### B. Economic usefulness

Даже если эффект настоящий, его потенциальная экономическая ценность оправдывает capital, risk, complexity и дальнейшие ресурсы.

Стратегия не проходит дальше, если не выполнено хотя бы одно из этих условий.

## 3. Research не равен доказательству

ATS разделяет четыре типа работы.

### 3.1 Exploratory Research

Разрешены свободное исследование, визуализации, перебор разумных формулировок, notebooks и быстрые prototypes.

Результат exploratory work предназначен для генерации hypothesis, а не для формального PASS.

### 3.2 Registered Research

Hypothesis и experiment регистрируются. Фиксируются data, code, parameters, cost assumptions и вопрос эксперимента.

Результат может использоваться как baseline evidence.

### 3.3 Validation

Проверяется устойчивость уже сформулированной системы на данных/условиях, которые не использовались для непосредственной настройки соответствующего решения.

### 3.4 Independent Examination

Замороженная Strategy Version проверяется на заранее определённом независимом evidence block. После раскрытия результата этот block больше не является независимым для данной линии разработки.

## 4. Единица исследования

Основной единицей evidence является **зарегистрированный Experiment**.

Минимальный manifest:

```yaml
experiment_id:
hypothesis_id:
strategy_id:
strategy_version:
code_revision:
dataset_id:
data_period:
research_stage:
parameters:
cost_model:
execution_model:
random_seed:
metrics:
predefined_question:
predefined_decision_rule:
result:
conclusion:
```

Поля, не применимые к конкретному типу стратегии, явно помечаются как not applicable, а не исчезают молча.

## 5. Hypothesis Card

До значимого количественного теста hypothesis должна содержать:

1. **Statement** — что ожидается.
2. **Mechanism** — почему эффект может существовать.
3. **Market** — где эффект ожидается.
4. **Condition** — при каких условиях.
5. **Horizon** — на каком горизонте.
6. **Direction** — какой результат ожидается.
7. **Falsification** — что опровергнет идею.
8. **Required data** — какие данные нужны.
9. **Known biases** — основные риски неверного вывода.

Формулировка, которую невозможно опровергнуть, не считается исследовательской hypothesis.

## 6. Research Question First

Каждый зарегистрированный experiment должен отвечать на ограниченный вопрос.

Хорошо:

> Сохраняется ли положительная net expectancy после включения исторически реалистичного spread и комиссии?

Плохо:

> Найти самые прибыльные параметры.

Оптимизация допустима как инструмент исследования, но не должна подменять вопрос о существовании edge.

## 7. Data Discipline

Перед формальным использованием dataset фиксируются:

- source;
- acquisition date;
- coverage;
- timezone;
- timestamp semantics;
- missing data policy;
- bad data policy;
- corporate-action/revision policy;
- instrument specification;
- transformation pipeline;
- immutable identifier/hash, где возможно.

Нельзя молча заменять dataset после получения плохого результата.

## 8. Data Partitioning

Типовая схема:

### Development

Используется для исследования и построения strategy.

### Validation

Используется для проверки решений, сделанных на development.

### Independent / Final

Используется только после freeze, если такой независимый экзамен предусмотрен protocol.

Конкретные пропорции не задаются глобально: они зависят от частоты наблюдений, длины истории, режима рынка и класса стратегии.

Временные данные нельзя случайно перемешивать так, чтобы будущее влияло на прошлое.

## 9. Purging и Leakage Control

Если labels, holding periods, rolling features или overlapping events создают зависимость между соседними observations, protocol должен предотвращать информационную утечку между development/validation blocks.

Для time-series cross-validation допускаются purging/embargo-подобные правила, если они нужны для устранения overlap.

Главный принцип: observation в test block не должна использовать информацию, которая была недоступна системе на соответствующий historical timestamp.

## 10. Transaction Cost Discipline

Research не считается экономически значимым без применимой модели расходов.

По мере зрелости стратегии модель может включать:

- spread;
- commission;
- swap/financing;
- slippage;
- rejection/partial-fill effects;
- market impact/capacity, если существенны;
- data/execution infrastructure cost, если он materially affects economics.

Для раннего pre-screen допустима упрощённая консервативная модель. Для live admission требуется модель, сверенная с реальным environment.

## 11. Baseline before Optimization

До сложной оптимизации должен существовать baseline.

Baseline нужен для ответа:

- существует ли эффект без тонкой настройки;
- насколько improvement зависит от optimization;
- не является ли вся прибыль результатом narrow parameter choice.

Если edge появляется только после большого поиска параметров, research risk повышается и требует более строгой validation.

## 12. Research Degrees of Freedom

ATS должен учитывать не только лучший найденный result, но и объём поиска, который привёл к нему.

В experiment history сохраняются, где возможно:

- число исследованных strategy variants;
- число parameter combinations;
- число markets/instruments;
- число feature families;
- число попыток изменения критериев;
- discarded variants.

Чем больше researcher degrees of freedom, тем сильнее должно быть независимое подтверждение.

## 13. Multiple Testing

Если исследовано много гипотез или параметрических вариантов, лучший результат не оценивается как будто он был единственным заранее выбранным тестом.

Методология требует как минимум:

1. сохранять количество фактически проверенных alternatives;
2. не скрывать неудачные alternatives;
3. использовать независимую validation;
4. при необходимости применять statistical correction или методы, учитывающие selection bias;
5. не использовать один и тот же final period повторно для последовательного спасения стратегии.

Конкретный correction method задаётся Statistical Validation Profile соответствующего исследования.

## 14. Evidence Sufficiency

ATS не использует универсальное правило вида «нужно минимум 100 сделок».

Достаточность evidence оценивается по:

- числу independent opportunities;
- temporal coverage;
- regime coverage;
- cross-sectional/event diversity;
- dependence между observations;
- концентрации P&L;
- stability результата;
- uncertainty оценки.

Количество trades является только одним из inputs.

## 15. Effective Sample Size

Если observations зависимы, raw count завышает реальное количество информации.

Для каждой стратегии должно быть качественно или количественно оценено, насколько observations независимы.

Примеры зависимости:

- множество сигналов из одной тенденции;
- несколько инструментов, движущихся из-за одного macro event;
- overlapping positions;
- повторные входы в один и тот же market episode;
- clustered news events.

При сильной зависимости требуется больший historical coverage или иной источник независимого evidence.

## 16. Regime Coverage

Validation должна по возможности включать релевантные режимы, например:

- high/low volatility;
- trend/range;
- crisis/normal;
- different liquidity sessions;
- high/low rate environments;
- different event regimes.

Не требуется искусственно покрывать режимы, в которых стратегия по specification не должна работать. Но такие исключения должны быть определены заранее, а не после плохого результата.

## 17. Core Performance Metrics

Метрики выбираются под класс стратегии. Типовой набор может включать:

- net P&L / return;
- expectancy per trade/event;
- hit rate;
- payoff ratio;
- profit factor;
- volatility of returns;
- Sharpe-like / Sortino-like measures;
- max drawdown;
- drawdown duration;
- return-to-drawdown measures;
- tail loss measures;
- time in market;
- capital utilization;
- turnover;
- concentration by trade/event/regime;
- capacity estimates.

Ни одна из этих метрик не является универсальным single-score PASS.

## 18. Uncertainty, not only Point Estimates

По возможности отчёт показывает не только одно число, но и uncertainty:

- confidence/credible ranges, если метод корректно применим;
- bootstrap distributions;
- distribution of outcomes across time/regimes;
- sensitivity to costs/parameters;
- Monte Carlo или resampling distributions для sequence risk.

Точная статистическая техника выбирается по data-generating process, а не механически.

## 19. Robustness

Robustness должна проверять источник edge, а не просто увеличивать количество графиков.

Типовые axes:

- parameter neighbourhood;
- nearby entry/exit assumptions;
- alternative periods;
- regimes;
- sessions;
- costs;
- execution degradation;
- reasonable data perturbations;
- nearby instruments, если hypothesis предполагает переносимость.

Искомый результат: не идеальная стабильность, а отсутствие зависимости от одного хрупкого выбора.

## 20. Outlier and Concentration Analysis

Обязательно проверяется:

- доля прибыли от top-N trades/events;
- доля прибыли от одного периода;
- доля прибыли от одного regime;
- зависимость от gaps/outliers;
- результат без крупнейших winners;
- loss concentration.

Если стратегия экономически существует только благодаря одному уникальному historical episode, это должно быть явно отражено в evidence.

## 21. Sequence Risk

Одинаковый набор trades может давать разные drawdown paths.

Для стратегий, где порядок результатов релевантен, используются подходящие resampling/Monte Carlo методы с сохранением важных зависимостей. Независимое перемешивание сделок не применяется, если оно разрушает существенную serial/regime structure.

Цель — оценить диапазон plausible drawdowns и loss sequences, а не создать искусственную точность.

# ЧАСТЬ II. ECONOMIC VIABILITY FRAMEWORK

## 22. Назначение Economic Viability

S05 отвечает на вопрос:

> Достаточно ли ценен наблюдаемый edge относительно капитала, риска, издержек и сложности, чтобы продолжать дорогую validation и production work?

Economic Viability — не поиск максимальной доходности и не попытка заранее гарантировать прибыль.

## 23. Viability Dimensions

Каждая стратегия получает Economic Viability Scorecard минимум по шести измерениям.

### V1 — Net Edge

Сохраняется ли положительное ожидаемое преимущество после применимых расходов?

### V2 — Risk Efficiency

Какой drawdown/tail risk приходится принимать ради ожидаемого результата?

### V3 — Capital Efficiency

Сколько капитала реально требуется, сколько времени он занят и какую ожидаемую отдачу приносит?

### V4 — Evidence Quality

Насколько надёжен вывод с учётом sample size, dependence, regimes и research freedom?

### V5 — Capacity & Scalability

Какой капитал стратегия потенциально способна принять до существенного ухудшения execution/economics?

### V6 — Operational Burden

Какова цена данных, latency, engineering, monitoring, manual operations и failure risk?

После появления портфеля добавляется:

### V7 — Portfolio Contribution

Как стратегия меняет ожидаемую доходность, drawdown, diversification и concentration портфеля?

## 24. Margin of Safety

Стратегия не должна проходить S05, если малое реалистичное ухудшение costs или execution полностью уничтожает ожидаемый edge.

Вместо требования «максимальная прибыль» используется требование **economic margin of safety**.

Конкретные stress multipliers определяются strategy profile, market и execution environment.

## 25. Return is Required, but not Alone

Низкий risk не компенсирует экономически бесполезный result автоматически.

Высокий return не компенсирует catastrophic tail risk автоматически.

Решение принимается по профилю `Return × Risk × Capital × Evidence × Capacity × Complexity`.

## 26. Opportunity Frequency

Редкая стратегия не отвергается автоматически. Но низкая frequency повышает требования к длительности history, event diversity или дополнительному cross-sectional evidence.

Если достаточное evidence практически невозможно собрать, стратегия может быть `PARKED` даже при привлекательном preliminary return.

## 27. Operational Opportunity Cost

Две стратегии с похожей экономикой могут иметь разную ценность, если одна требует сложной ultra-low-latency инфраструктуры, дорогих data feeds и постоянного вмешательства, а другая использует существующую платформу.

Operational burden должен учитываться до production build.

## 28. PASS / PARK / REJECT в S05

### PASS

Edge потенциально достаточно ценен, evidence достаточно сильный для текущей стадии, и дальнейшая validation оправдана.

### PARK

Идея потенциально ценна, но сейчас evidence/data/platform/capacity недостаточны для разумного продолжения.

### RETURN_TO_RESEARCH

Есть конкретная исследовательская неопределённость, которую можно проверить без post-hoc изменения success criteria.

### REJECT

Экономика недостаточна либо evidence указывает, что source of edge не выдерживает разумную проверку.

# ЧАСТЬ III. STATISTICAL VALIDATION PROTOCOL

## 29. Pre-Validation Registration

Перед S06 фиксируются:

- Strategy Version;
- primary hypothesis;
- primary metrics;
- key secondary metrics;
- validation dataset/period;
- allowed parameter region;
- cost model;
- planned robustness axes;
- decision rule;
- known exceptions.

Изменения после результата регистрируются как новая research iteration, а не переписывают исходный protocol.

## 30. Primary vs Secondary Metrics

Для каждого formal validation заранее указываются primary metrics, определяющие decision, и secondary diagnostics.

Это уменьшает риск выбрать после результата именно ту метрику, которая выглядит лучше остальных.

## 31. Validation Blocks

По возможности validation анализируется не только агрегированно, но и по независимым или частично независимым blocks:

- years/quarters;
- regimes;
- event types;
- instruments;
- sessions;
- geographies/venues, если применимо.

Цель — увидеть, где именно существует или исчезает edge.

## 32. Walk-Forward

Walk-forward может использоваться, если strategy предполагает периодическое re-estimation или recalibration.

Walk-forward protocol должен моделировать реальный порядок времени: данные будущего периода не используются для настройки прошлого.

## 33. Bootstrap / Resampling

Resampling используется только при сохранении существенной структуры данных.

В зависимости от стратегии могут использоваться:

- trade-level bootstrap;
- block bootstrap;
- event-cluster resampling;
- regime-aware resampling;
- permutation/randomization tests для узких вопросов.

Метод и ограничения описываются в experiment report.

## 34. Independent Examination

Перед S07 создаётся frozen manifest. Final/independent block используется один раз для соответствующей Strategy Version и решения.

Если результат FAIL и стратегия меняется, старый final block становится частью известной истории и не должен снова называться независимым доказательством новой версии без специального обоснования.

## 35. OOS Similarity

PASS independent exam требует не только положительного итогового P&L, но и разумного соответствия характеру validation evidence.

Анализируются:

- magnitude degradation;
- drawdown;
- trade/event distribution;
- regime behaviour;
- cost sensitivity;
- concentration.

Резко отличающийся OOS profile требует объяснения даже при формально положительном P&L.

## 36. Stress Validation

После statistical validation strategy проверяется на реалистичное ухудшение assumptions:

- higher spread/commission;
- worse slippage;
- execution delay;
- missed opportunities;
- partial fills/rejects;
- data delays;
- parameter perturbations;
- adverse sequencing;
- infrastructure failures, где применимо.

Stress не обязан оставлять стратегию прибыльной при любом фантастическом сценарии. Он должен покрывать заранее определённый диапазон реалистичных adverse conditions.

# ЧАСТЬ IV. CLASS-SPECIFIC PROFILES

## 37. Technical / Bar-Based Profile

Особые риски:

- OHLC path ambiguity;
- intrabar stop/limit ordering;
- look-ahead indicators;
- parameter mining;
- session/timezone errors;
- insufficient tick realism.

Требование: backtester должен явно описывать assumptions, если порядок внутри бара неизвестен.

## 38. Event / News Profile

Особые риски:

- publication timestamp accuracy;
- consensus timestamp availability;
- revised vs initially released value;
- event clustering;
- extreme spread/slippage;
- latency dependence;
- leakage из calendar/news provider.

Evaluation unit может быть event или event cluster, а не отдельная сделка.

## 39. Statistical / Relative-Value Profile

Особые риски:

- universe selection;
- survivorship;
- structural breaks;
- non-stationarity;
- multiple testing;
- dependence между pairs/assets;
- borrow/financing constraints, если применимо.

## 40. High-Turnover / Execution-Sensitive Profile

Особые риски:

- queue position;
- fill probability;
- latency;
- spread capture assumptions;
- market impact;
- capacity;
- difference between historical quote and executable price.

Для такого класса слабая execution model может полностью обесценить historical backtest.

# ЧАСТЬ V. RESEARCH GOVERNANCE

## 41. Negative Result Registry

Каждая rejected hypothesis сохраняет минимум:

- ID;
- что проверялось;
- dataset;
- key result;
- причина rejection;
- lessons learned.

Цель — не повторять одни и те же исследования под новыми именами.

## 42. Research Decision Log

Material research decisions должны иметь краткую запись:

- decision;
- evidence;
- alternatives;
- reason;
- affected strategy/version.

## 43. Reproducibility Standard

Формальный experiment считается воспроизводимым, если другой запуск из зафиксированных inputs способен получить тот же результат в пределах заранее описанной numerical tolerance/expected randomness.

Если результат зависит от nondeterministic process, seed и distribution assumptions фиксируются, где возможно.

## 44. Research Code Quality

Exploratory code может быть быстрым и одноразовым. Но код, используемый для formal evidence, должен иметь:

- version control;
- deterministic inputs, где возможно;
- basic tests критических вычислений;
- logged configuration;
- clear output artifact.

Production standards не требуются от notebook только потому, что он существует, но evidence standards требуются от результата, который используется для решения.

## 45. No Post-Hoc Promotion

Нельзя после просмотра результата объявить secondary metric главным критерием PASS без регистрации новой research iteration.

Нельзя менять economic objective так, чтобы спасти конкретный полученный backtest.

## 46. Kill Criteria

Исследование может быть остановлено рано, если:

- отсутствует правдоподобный mechanism и effect не воспроизводится;
- data quality не позволяет честную проверку;
- edge исчезает после базовых реалистичных costs;
- результат зависит от единичных outliers;
- отсутствует robust neighbourhood;
- evidence практически невозможно накопить;
- operational complexity явно превышает возможную economic value;
- обнаружен leakage, после устранения которого effect исчезает.

Early rejection является успехом Research Factory.

## 47. Research Report Template

Формальный report должен отвечать минимум:

1. What was tested?
2. Why should the effect exist?
3. What data were used?
4. What information was available at each historical timestamp?
5. What costs/execution assumptions were used?
6. How many variants were explored?
7. What is the baseline result?
8. How uncertain is it?
9. How concentrated is P&L?
10. How does it behave across periods/regimes?
11. How sensitive is it to parameters/costs?
12. What evidence contradicts the hypothesis?
13. What is the economic viability assessment?
14. What decision follows: PASS/PARK/RETURN/REJECT?

## 48. Research KPI

Program-level metrics:

- ideas registered;
- ideas screened;
- prototypes completed;
- median time Idea → first evidence;
- early rejection rate;
- Candidate conversion rate;
- S05 PASS rate;
- S06/S07 pass rates;
- reproducibility rate;
- data/leakage incidents;
- platform capabilities reused;
- average research cost/time per rejected idea and per Candidate.

Эти KPI используются для улучшения процесса, а не для принуждения исследователей искусственно повышать pass rate.

## 49. Methodology Change Control

Изменение Research Methodology версионируется.

Новая методология не переписывает историю старых experiments. Для каждого evidence должно быть понятно, по какой версии protocol он был получен.

Material changes, способные изменить pass/fail interpretation, требуют отдельного решения и не применяются постфактум только к неудачной стратегии.

## 50. Acceptance Criteria Research Methodology v1

Методология считается пригодной для M1, если она позволяет однозначно:

1. отличить exploratory run от formal evidence;
2. зарегистрировать hypothesis и experiment;
3. зафиксировать data/cost assumptions;
4. учитывать объём research search и multiple testing;
5. оценить evidence sufficiency без универсального trade-count threshold;
6. провести S05 Economic Viability;
7. определить protocol для S06 Validation;
8. защитить S07 Independent Examination от post-hoc tuning;
9. подключить class-specific profile;
10. сохранить отрицательные результаты и воспроизвести ключевые experiments.

## 51. Следующий шаг

После принятия этой методологии необходимо завершить M0 следующими артефактами:

1. `PROGRAM_WBS_V2.md`;
2. `REPOSITORY_STRUCTURE_V2.md`;
3. новая machine-readable state model;
4. templates для Idea, Hypothesis, Experiment, Candidate и Strategy;
5. Program Backlog v2.

После M0 начинается M1/M2: реализация минимального Research Platform MVP и выбор Reference Strategy #1.
