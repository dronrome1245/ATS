# ATS Program WBS v2

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 2.0  
**Статус:** BASELINE  
**Дата:** 15 сентября 2026 года  
**Родительские документы:** `PROGRAM_CHARTER_V2.md`, `OPERATING_MODEL_V2.md`, `STRATEGY_LIFECYCLE_V2.md`, `RESEARCH_METHODOLOGY_V1.md`

## 1. Назначение

Эта WBS разлагает ATS Program на управляемые work packages от текущего Program Rebaseline до контролируемого live-портфеля.

WBS является **deliverable-oriented**, а не календарным планом. Сроки не назначаются, пока не определены исполнитель, доступность входов и фактическая сложность соответствующего work package.

Обозначения scope:

- `P` — program-level capability, создаётся один раз и повторно используется;
- `S` — strategy-level work, выполняется для конкретной Strategy / Strategy Version;
- `P/S` — общий framework на уровне программы и его применение на уровне стратегии.

Правило выполнения:

> Work package считается завершённым только при наличии указанного deliverable и выполненного Definition of Done. Завершение work package само по себе не означает переход стратегии или программы на следующий milestone, если зависимые критерии не выполнены.

---

## 2. Milestones программы

| Milestone | Назначение | Exit result |
|---|---|---|
| `M0_PROGRAM_REBASELINE` | Переопределить ATS как Strategy Factory | Однозначные Charter, Operating Model, Lifecycle, Research Methodology, WBS, repository structure, backlog, templates и canonical state |
| `M1_RESEARCH_METHODOLOGY` | Сделать research воспроизводимым и управляемым | Рабочий Research Funnel, experiment protocol и economic/statistical screening |
| `M2_RESEARCH_PLATFORM_MVP` | Создать минимальную общую исследовательскую платформу | Можно воспроизводимо загружать данные, запускать baseline experiments и получать стандартный report |
| `M3_REFERENCE_STRATEGY_1` | Проверить вертикальный research flow на первой стратегии | Strategy #1 либо проходит к S05, либо корректно отвергается раньше; в обоих случаях сохраняются reproducible evidence и platform learnings |
| `M4_VALIDATION_FRAMEWORK` | Стандартизировать глубокую проверку edge | Robustness, independent examination, stress/evidence framework применимы к кандидатам |
| `M5_EXECUTION_PLATFORM` | Подготовить подтверждённую стратегию к реальному исполнению | Demo/shadow-capable execution stack, state, reconciliation, monitoring и risk controls |
| `M6_REFERENCE_STRATEGY_2` | Проверить универсальность платформы на другом классе стратегии | Вторая стратегия использует общую платформу и расширяет её только по доказанной потребности |
| `M7_PORTFOLIO_LAYER` | Перейти от независимых стратегий к portfolio management | Общие exposure, correlation, allocation и portfolio-risk механизмы |
| `M8_CONTROLLED_LIVE_PORTFOLIO` | Эксплуатировать несколько подтверждённых стратегий | Ограниченный live-портфель с monitoring, evidence-based allocation и operational controls |

---

# 3. WBS 0 — Program Governance & Rebaseline

| ID | Scope | Milestone | Work package | Deliverable | Dependencies | Responsible role | Definition of Done |
|---|---|---|---|---|---|---|---|
| `WBS-0.1` | P | M0 | Program Charter | `PROGRAM_CHARTER_V2.md` | — | OWNER | Миссия, scope, success/failure criteria, contours и milestones однозначно определены |
| `WBS-0.2` | P | M0 | Operating Model | `OPERATING_MODEL_V2.md` | 0.1 | OWNER / PROGRAM | Сущности, состояния, decision points и роли определены без зависимости от одной стратегии |
| `WBS-0.3` | P | M0 | Strategy Lifecycle | `STRATEGY_LIFECYCLE_V2.md` | 0.1–0.2 | RESEARCH / RISK / VALIDATION | Путь `Idea → Research → Validation → Live → Scaling` определён, economic viability присутствует до дорогой validation |
| `WBS-0.4` | P | M0 | Research Methodology | `RESEARCH_METHODOLOGY_V1.md` | 0.2–0.3 | RESEARCH / VALIDATION | Разделены exploratory, registered, validation и independent evidence; определены reproducibility и economic usefulness |
| `WBS-0.5` | P | M0 | Program WBS | `PROGRAM_WBS_V2.md` | 0.1–0.4 | PROGRAM | M0–M8 разложены на work packages с dependencies, roles и DoD |
| `WBS-0.6` | P | M0 | Repository Structure v2 | `REPOSITORY_STRUCTURE_V2.md` | 0.5 | PROGRAM / DEVELOPMENT | Определены canonical locations для program, research, strategies, data, experiments, platform, reports и legacy |
| `WBS-0.7` | P | M0 | Program Backlog v2 | machine-readable или Markdown backlog v2 | 0.5–0.6 | PROGRAM | Каждый ближайший work package представлен исполнимой задачей с приоритетом и связью с WBS |
| `WBS-0.8` | P | M0 | Research entity templates | Templates Idea, Hypothesis, Candidate, Experiment, Strategy Version | 0.4–0.6 | RESEARCH / PROGRAM | Новый объект каждого типа можно создать без придумывания структуры заново |
| `WBS-0.9` | P | M0 | Canonical state v2 | `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` schema v2 | 0.1–0.5 | PROGRAM | Один machine-readable source of truth содержит current phase, last completed, next artifact и safety state |
| `WBS-0.10` | P | M0 | Repository validator v2 | `tools/validate_repo.py` v2 | 0.6, 0.9 | DEVELOPMENT | Validator проверяет v2 canonical files и handoff/state synchronization, не требует G01–G13 как текущую модель |
| `WBS-0.11` | P | M0 | AI handoff protocol | `AI_HANDOFF.md` + agent pointers | 0.2, 0.9 | PROGRAM | Новый AI-чат может определить текущее состояние и next action без истории разговора |
| `WBS-0.12` | P | M0 | Legacy classification | Legacy index/marks | 0.6 | PROGRAM | ATS v1 документы сохранены как history/reference и не могут быть ошибочно приняты за current roadmap |

### Exit M0

M0 закрывается, когда выполнены `WBS-0.1`–`WBS-0.12`, validator проходит на main, а новый агент однозначно определяет следующий milestone без внешнего контекста.

---

# 4. WBS 1 — Research Factory

| ID | Scope | Milestone | Work package | Deliverable | Dependencies | Responsible role | Definition of Done |
|---|---|---|---|---|---|---|---|
| `WBS-1.1` | P | M1 | Idea intake model | Idea Card schema/process | M0 | RESEARCH | Идею можно зарегистрировать с rationale, market, horizon и required data |
| `WBS-1.2` | P | M1 | Hypothesis model | Hypothesis template | 1.1 | RESEARCH | Hypothesis содержит falsifiable statement, mechanism и expected effect |
| `WBS-1.3` | P | M1 | Data feasibility review | Data Feasibility template | 1.2 | DATA | Проверяются availability, timestamp semantics, bias risks и cost relevance |
| `WBS-1.4` | P | M1 | Cheap prototype protocol | Prototype rules | 1.2–1.3 | RESEARCH | Определено, что prototype отвечает на один ранний вопрос и не считается formal validation |
| `WBS-1.5` | P | M1 | Economic pre-screen | Pre-screen rubric | 1.4 | RESEARCH | До Candidate оцениваются magnitude, costs, opportunities, capital use и complexity |
| `WBS-1.6` | P | M1 | Candidate promotion | Candidate Manifest + decision rubric | 1.5 | RESEARCH / VALIDATION | `PROMOTE / PARK / REJECT` опирается на сохранённые preliminary evidence |
| `WBS-1.7` | P | M1 | Experiment registration | Experiment manifest schema | 0.8, 1.2 | RESEARCH / DEVELOPMENT | Formal experiment однозначно связывает code, data, params, costs, question и result |
| `WBS-1.8` | P | M1 | Experiment registry | Searchable registry | 1.7 | PROGRAM / RESEARCH | Положительные и отрицательные formal experiments сохраняются и находятся по ID |
| `WBS-1.9` | P | M1 | Evidence classification | Evidence taxonomy | 0.4 | VALIDATION | Различаются exploratory, registered, validation, independent, demo/shadow и live evidence |
| `WBS-1.10` | P | M1 | Research review cadence | Review protocol | 1.1–1.9 | OWNER / RESEARCH | Есть повторяемая процедура принятия решений по ideas/prototypes/candidates без обязательных календарных сроков |

### Exit M1

Можно зарегистрировать новую идею, провести дешёвую проверку, сохранить experiment и принять воспроизводимое решение `PROMOTE / PARK / REJECT`.

---

# 5. WBS 2 — Shared Research Platform MVP

| ID | Scope | Milestone | Work package | Deliverable | Dependencies | Responsible role | Definition of Done |
|---|---|---|---|---|---|---|---|
| `WBS-2.0` | P | M2 | Reference Consumer Profile | `REFERENCE_CONSUMER_PROFILE.md` | M1 | PROGRAM / DEVELOPMENT / RESEARCH | Определён минимальный абстрактный ordered-data research consumer, достаточный для выбора первого vertical stack без выбора конкретной Strategy #1, рынка, инструмента или live environment |
| `WBS-2.1` | P | M2 | Technology decision for research MVP | Research stack ADR | 2.0 | DEVELOPMENT | Выбран минимальный стек по Consumer Profile, reproducibility, data/replay, experiment и testing requirements; решение не зависит от ещё не выбранной M3 Strategy #1 |
| `WBS-2.2` | P | M2 | Project/environment reproducibility | Environment specification | 2.1 | DEVELOPMENT | Новый environment воспроизводимо запускает один и тот же registered experiment |
| `WBS-2.3` | P | M2 | Dataset manifest support | Data manifest tooling | 1.3, 2.1 | DATA / DEVELOPMENT | Dataset имеет stable ID, source, period и transformation trace |
| `WBS-2.4` | P | M2 | Base data loader | Data loading capability | 2.3 | DEVELOPMENT / DATA | Reference data читаются детерминированно с явными timezone/ordering rules |
| `WBS-2.5` | P | M2 | Strategy research interface | Minimal Strategy API | 2.1 | DEVELOPMENT | Baseline strategy может получать data и возвращать decisions/trades без broker-specific code |
| `WBS-2.6` | P | M2 | Backtest/replay core | Minimal deterministic engine | 2.4–2.5 | DEVELOPMENT | Один input manifest даёт воспроизводимый trade/result output |
| `WBS-2.7` | P | M2 | Cost model interface | Fees/spread/slippage abstraction | 2.6 | DEVELOPMENT / RESEARCH | Costs являются explicit experiment input, а не скрытой константой |
| `WBS-2.8` | P | M2 | Standard analytics | Baseline metrics/report | 2.6–2.7 | RESEARCH / DEVELOPMENT | Каждый run выдаёт стандартный минимум P&L, drawdown, trades, costs и distributions |
| `WBS-2.9` | P | M2 | Experiment runner | Manifest-driven runner | 1.7, 2.2–2.8 | DEVELOPMENT | Registered experiment можно повторить одной документированной процедурой |
| `WBS-2.10` | P | M2 | Research platform tests | Unit/replay regression tests | 2.4–2.9 | TESTER / DEVELOPMENT | Критические расчёты имеют automated checks и известный deterministic fixture |

### Exit M2

Есть минимальный reusable vertical research stack. Он не обязан поддерживать news, portfolio или live execution, пока этого не требует подтверждённый consumer.

---

# 6. WBS 3 — Reference Strategy #1

| ID | Scope | Milestone | Work package | Deliverable | Dependencies | Responsible role | Definition of Done |
|---|---|---|---|---|---|---|---|
| `WBS-3.1` | S | M3 | Select Reference Strategy #1 | Selection decision | M1, M2 | OWNER / RESEARCH | Выбрана простая strategy class с доступными данными и понятной execution model |
| `WBS-3.2` | S | M3 | Idea & rationale | Idea/Hypothesis artifacts | 3.1 | RESEARCH | Есть falsifiable market hypothesis и rationale |
| `WBS-3.3` | S | M3 | Data feasibility | Strategy data review | 3.2 | DATA | Данные позволяют честно проверить hypothesis, known gaps сохранены |
| `WBS-3.4` | S | M3 | Cheap prototype | Prototype result | 3.2–3.3 | RESEARCH | Получен первый quantitative result без production overengineering |
| `WBS-3.5` | S | M3 | Economic pre-screen | Promotion decision | 3.4 `ADVANCE_TO_ECONOMIC_SCREEN` | RESEARCH | Strategy проходит R4 либо закрывается с сохранённым reason/evidence |
| `WBS-3.6` | S | M3 | Candidate admission | Candidate Manifest | 3.5 PASS | RESEARCH / VALIDATION | Strategy получает ID и formal research budget only after evidence |
| `WBS-3.7` | S | M3 | Strategy specification | Versioned specification | 3.6 | RESEARCH | Rules реализуемы другим developer без смысловых уточнений |
| `WBS-3.8` | S | M3 | Research protocol | Data split + evaluation protocol | 3.7 | RESEARCH / DATA / VALIDATION | Development/validation/independent blocks и evaluation rules зафиксированы |
| `WBS-3.9` | S | M3 | Baseline implementation | Strategy Version + experiment | 3.7–3.8, M2 | DEVELOPMENT | Strategy запускается через shared platform и trades проверены |
| `WBS-3.10` | S | M3 | Economic Viability S05 | Economic Viability Report | 3.9 | RESEARCH / VALIDATION | Оценены net edge, risk, capital use, evidence, costs, capacity и complexity; принято PASS/REJECT/PARK |
| `WBS-3.11` | P/S | M3 | Platform learning review | Capability gaps / M3 closeout report | 3.4 terminal `REJECT` **or** 3.9–3.10 | DEVELOPMENT / RESEARCH | Для раннего rejection сохраняется причина остановки и platform/data learnings; для прошедшей линии отделены strategy-specific needs от reusable platform improvements |

### Exit M3

Reference Strategy #1 прошла путь минимум до S05 либо была корректно отвергнута; в обоих случаях ATS получил reproducible evidence и конкретные platform learnings.

---

# 7. WBS 4 — Validation Framework

| ID | Scope | Milestone | Work package | Deliverable | Dependencies | Responsible role | Definition of Done |
|---|---|---|---|---|---|---|---|
| `WBS-4.1` | P | M4 | Validation protocol framework | Validation standard | M3, 0.4 | VALIDATION | Определены допустимые forms of validation и правила выбора под strategy class |
| `WBS-4.2` | P | M4 | Parameter sensitivity tooling | Sensitivity analysis capability | 4.1, M2 | DEVELOPMENT / VALIDATION | Можно оценивать neighbourhood, а не только best point |
| `WBS-4.3` | P | M4 | Time/regime slicing | Regime analysis capability | 4.1 | RESEARCH / DEVELOPMENT | Results сравниваются по periods/regimes без ручного selective reporting |
| `WBS-4.4` | P | M4 | Trade concentration analysis | Concentration report | 4.1 | VALIDATION | Видна зависимость результата от few trades/outliers |
| `WBS-4.5` | P | M4 | Resampling framework | Bootstrap/Monte Carlo interface | 4.1 | VALIDATION / DEVELOPMENT | Tail/path uncertainty можно оценивать reproducibly там, где метод применим |
| `WBS-4.6` | P | M4 | Independent exam protocol | Freeze + exam manifest | 4.1 | VALIDATION | Version/data/criteria freeze происходит до раскрытия independent result |
| `WBS-4.7` | P | M4 | Multiple-research accounting | Research history linkage | 1.8, 4.1 | VALIDATION | Decision review видит количество существенных исследовательских попыток и selection history |
| `WBS-4.8` | P | M4 | Class-specific profiles | Validation profiles | 4.1 | VALIDATION / RESEARCH | Как минимум технический профиль определён; новые profiles добавляются по потребности |
| `WBS-4.9` | S | M4 | Validate first promoted Candidate | S06 report | S05 PASS for a promoted Candidate, 4.1–4.8 | VALIDATION | Robustness criteria применены без post-hoc изменения hypothesis; rejected research lines не возвращаются в validation |
| `WBS-4.10` | S | M4 | Independent exam first promoted Candidate | S07 exam report | 4.9 PASS | INDEPENDENT_REVIEWER | Frozen version получает однозначный PASS/FAIL на independent evidence |

### Exit M4

Существует reusable validation framework, а хотя бы один Candidate прошёл или честно не прошёл formal robustness/independent pipeline.

---

# 8. WBS 5 — Execution Platform & Live Readiness

| ID | Scope | Milestone | Work package | Deliverable | Dependencies | Responsible role | Definition of Done |
|---|---|---|---|---|---|---|---|
| `WBS-5.1` | P/S | M5 | Live environment decision | Broker/platform/account ADR for candidate | S07 PASS | OWNER / EXECUTION / LEGAL_REVIEW | Проверены legal instrument, broker conditions, algo availability и execution constraints |
| `WBS-5.2` | P | M5 | Market/live data adapter | Runtime data adapter | 5.1 | DEVELOPMENT | Data freshness/order/errors контролируются и журналируются |
| `WBS-5.3` | P | M5 | Execution intent model | Order intent schema | 5.1 | DEVELOPMENT | Strategy output отделён от broker request и имеет persistent ID |
| `WBS-5.4` | P | M5 | Strategy risk controller | Independent strategy risk layer | 5.3 | DEVELOPMENT / RISK | Risk layer может окончательно блокировать creation of new risk |
| `WBS-5.5` | P | M5 | Execution adapter | Broker/platform adapter | 5.1, 5.3–5.4 | DEVELOPMENT / EXECUTION | Handles success/reject/partial fill/requote/slippage paths relevant to platform |
| `WBS-5.6` | P | M5 | Persistent state & reconciliation | State/recovery subsystem | 5.5 | DEVELOPMENT / OPERATIONS | Restart восстанавливает known state, unknown position вызывает safe mode |
| `WBS-5.7` | P | M5 | Idempotency | Duplicate-order protection | 5.3, 5.6 | DEVELOPMENT | Повтор processing одного intent не создаёт uncontrolled duplicate risk |
| `WBS-5.8` | P | M5 | Audit logging | End-to-end decision trail | 5.2–5.7 | DEVELOPMENT / OPERATIONS | Восстанавливается chain `data → intent → risk → request → response → position` |
| `WBS-5.9` | P | M5 | Monitoring & alerts | Runtime observability | 5.6–5.8 | OPERATIONS | Critical states и protection failures обнаруживаются и диагностируются |
| `WBS-5.10` | P | M5 | Emergency/stop controls | Stop mechanisms | 5.4, 5.9 | RISK / OPERATIONS | New risk можно независимо запретить; open-position policy определяется live protocol |
| `WBS-5.11` | S | M5 | Strategy Risk Mandate | Owner-approved mandate | 4.10 PASS, 5.1 | OWNER / RISK | Allocation/limits/stop rules основаны на strategy evidence, а не выдуманы до research |
| `WBS-5.12` | S | M5 | Stress & live protocol | S08 stress report + live protocol | 5.2–5.11 | RISK / VALIDATION | Execution degradation/failure scenarios укладываются в approved mandate либо strategy не допускается дальше |
| `WBS-5.13` | S | M5 | Demo/shadow acceptance | S09 report | 5.12 PASS | TESTER / EXECUTION | Нет unexplained trades; restart/reconcile/alerts/stop controls подтверждены |
| `WBS-5.14` | S | M5 | Minimal live experiment | S10 execution report | 5.13 PASS + OWNER live decision | OWNER / EXECUTION / RISK | Minimal real exposure даёт measured model-vs-actual costs/execution; decision PASS/PAUSE/FAIL сохранён |

### Exit M5

ATS имеет reusable execution skeleton и как минимум один validated candidate способен пройти demo/shadow; минимальный live выполняется только после отдельного OWNER decision.

---

# 9. WBS 6 — Reference Strategy #2 & Platform Generalization

| ID | Scope | Milestone | Work package | Deliverable | Dependencies | Responsible role | Definition of Done |
|---|---|---|---|---|---|---|---|
| `WBS-6.0` | P | M6 | Market Pattern Discovery | `governance/methodology/MARKET_PATTERN_DISCOVERY.md` + bounded Search Manifest/result history | M1, M2, M3 learnings, 4.8 | RESEARCH / DEVELOPMENT / VALIDATION | Можно воспроизводимо искать bounded price-dynamics patterns на development data; search space, failed alternatives и shortlist history сохраняются; discovery не создаёт validation evidence |
| `WBS-6.1` | S | M6 | Select Strategy #2 | Selection decision | 6.0 or explicit Idea intake, M3 learnings | OWNER / RESEARCH | Выбран существенно иной strategy/data/execution profile из bounded discovery/idea intake без заявления edge до Research Funnel |
| `WBS-6.2` | S | M6 | Run Research Funnel | R0–R4 artifacts | 6.1, M1 | RESEARCH / DATA | Strategy #2 получает independent promotion decision |
| `WBS-6.3` | P/S | M6 | Identify new data needs | Data capability decision | 6.2 | DATA / DEVELOPMENT | Новые feeds/timestamps/features добавляются только при подтверждённой need |
| `WBS-6.4` | P | M6 | Extend Strategy API | Generalized interfaces | 6.2–6.3 | DEVELOPMENT | Новая стратегия не требует ломать semantics Strategy #1; shared abstraction подтверждена двумя consumers |
| `WBS-6.5` | P | M6 | Event/news data support if required | Event ingestion/replay capability | 6.3 | DEVELOPMENT / DATA | Publication time, consensus/actual/revision semantics воспроизводимы для relevant events |
| `WBS-6.6` | S | M6 | Baseline & Economic Viability #2 | S04–S05 reports | 6.2–6.5 | RESEARCH / DEVELOPMENT | Strategy #2 достигает честного S05 decision на shared platform |
| `WBS-6.7` | P | M6 | Platform reuse review | Reuse/generalization report | 6.6 or terminal 6.2 early-rejection outcome | DEVELOPMENT / PROGRAM | Ясно, какие компоненты действительно shared, какие должны остаться strategy-specific, и какие learnings сохраняются при раннем Research Funnel rejection |
| `WBS-6.8` | S | M6 | Validation handoff #2 | S06–S07 through M4.9/M4.10 when justified | 6.6 PASS, 4.1–4.8 | VALIDATION | Если Strategy #2 является первым promoted Candidate, её S06/S07 исполняют M4.9/M4.10; при FAIL evidence сохраняется и M5 не открывается |

### Exit M6

ATS доказал, что Research Factory и Shared Platform применимы минимум к двум различным strategy profiles или выявил конкретные архитектурные ограничения с сохранённым evidence.

---

# 10. WBS 7 — Portfolio & Capital Layer

| ID | Scope | Milestone | Work package | Deliverable | Dependencies | Responsible role | Definition of Done |
|---|---|---|---|---|---|---|---|
| `WBS-7.1` | P | M7 | Portfolio inventory | Strategy/deployment inventory | Минимум 2 portfolio candidates | PORTFOLIO / PROGRAM | Все candidates имеют version, status, allocation eligibility и exposure metadata |
| `WBS-7.2` | P | M7 | Common exposure model | Exposure taxonomy | 7.1 | RISK / DEVELOPMENT | Exposure агрегируется across strategies по релевантным dimensions |
| `WBS-7.3` | P | M7 | Correlation/dependence analysis | Dependence report tooling | 7.1 | RESEARCH / RISK | Оцениваются return/drawdown/regime overlaps, а не только headline correlation |
| `WBS-7.4` | P | M7 | Portfolio risk engine | Portfolio-level limits | 7.2–7.3 | RISK / DEVELOPMENT | Portfolio Risk может ограничить strategy intent независимо от local strategy allowance |
| `WBS-7.5` | P | M7 | Allocation framework | Allocation policy | 7.2–7.4 | OWNER / RISK | Allocation учитывает evidence, marginal risk, capacity и diversification; policy versioned |
| `WBS-7.6` | P | M7 | Portfolio drawdown controls | Portfolio stop/reduction policy | 7.4–7.5 | OWNER / RISK | Определены program-level response states without ad-hoc loss chasing |
| `WBS-7.7` | P | M7 | Capital utilization analytics | Capital efficiency report | 7.1–7.5 | PORTFOLIO | Видны committed/used capital и simultaneous demand |
| `WBS-7.8` | S | M7 | Portfolio admission decisions | S11 decisions | 7.1–7.7 | OWNER / RISK | Каждая live candidate получает ACTIVE/WATCH/REJECT с documented rationale |

### Exit M7

Решения о capital allocation принимаются на portfolio level, а стратегия не может самостоятельно создать риск, запрещённый Portfolio Risk.

---

# 11. WBS 8 — Controlled Live Portfolio & Operations

| ID | Scope | Milestone | Work package | Deliverable | Dependencies | Responsible role | Definition of Done |
|---|---|---|---|---|---|---|---|
| `WBS-8.1` | P | M8 | Deployment model | Immutable deployment manifest | M5, M7 | OPERATIONS / DEVELOPMENT | Каждый running deployment связан с exact strategy/code/config/risk versions |
| `WBS-8.2` | P | M8 | Release/rollback procedure | Release runbook | 8.1 | OPERATIONS | Можно воспроизводимо deploy/rollback без silent config drift |
| `WBS-8.3` | P | M8 | Incident management | Incident protocol & registry | M5 | OPERATIONS | Critical incidents получают ID, timeline, cause, action и evidence impact assessment |
| `WBS-8.4` | P | M8 | Strategy health monitoring | Health state model | M5, M7 | OPERATIONS / VALIDATION | Strategy может перейти NORMAL/WATCH/REDUCED/PAUSED/REVALIDATION/RETIRED по documented evidence |
| `WBS-8.5` | P | M8 | Model-vs-live monitoring | Drift/execution comparison | 8.1, M5 | EXECUTION / VALIDATION | Costs, fills, drawdown и behaviour регулярно сравниваются с expected ranges |
| `WBS-8.6` | P | M8 | Portfolio monitoring | Portfolio dashboard/report | M7 | RISK / OPERATIONS | Visible exposures, concentration, drawdown, strategy status и allocation |
| `WBS-8.7` | S | M8 | Controlled scaling protocol | S12 evidence blocks | S11 ACTIVE | OWNER / RISK | Каждая increase decision использует new live evidence после предыдущего allocation |
| `WBS-8.8` | P/S | M8 | Pause/revalidation/retirement | Lifecycle operation | 8.4–8.7 | OWNER / VALIDATION / RISK | Degraded strategy можно reduce/pause/revalidate/retire без потери experiment/evidence history |
| `WBS-8.9` | P | M8 | Profit/reserve governance | Program-level withdrawal policy | Stable live portfolio evidence | OWNER | Profit withdrawal отделён от strategy validation и учитывает reserves, portfolio risk, costs и applicable obligations |
| `WBS-8.10` | P | M8 | Operational review loop | Periodic operating review protocol | 8.1–8.9 | OWNER / OPERATIONS | Program continuously converts live evidence into explicit continue/reduce/pause/scale decisions |

### Exit M8

Существует ограниченный live-портфель из доказанных Strategy Versions, где capital allocation, runtime state, execution quality, portfolio risk и scaling decisions прослеживаются до evidence и owner decisions.

---

# 12. Сквозные правила зависимостей

1. **Research precedes production.** Production capability не создаётся без подтверждённого consumer, кроме минимальных scaffolding needs.
2. **Economic viability precedes expensive validation.** S05 должен отсекать экономически слабые системы раньше S06/S07 и production hardening.
3. **Independent evidence precedes live readiness.** Live engineering не используется для спасения strategy, которая не прошла research evidence.
4. **Strategy risk precedes real exposure.** Конкретный Strategy Risk Mandate обязателен до minimal live, но не до safe research.
5. **Live evidence precedes scaling.** Старый backtest не может сам обосновать новый allocation tier.
6. **Portfolio risk dominates local permission.** Strategy-level permission не отменяет portfolio-level запрет.
7. **Material strategy changes invalidate affected evidence.** Возврат определяется `STRATEGY_LIFECYCLE_V2.md`.
8. **Handoff is part of completion.** Program-level work не закрывается, пока canonical state, human status, next action и AI handoff не синхронизированы.

---

# 13. Критический логический путь

Минимальный путь к первому meaningful live candidate:

`M0 → M1 → M2 → M3(vertical flow; PASS or early REJECT) → M4.1–M4.8 → M6.0–M6.6 until first S05 PASS Candidate → M4.9–M4.10(S07 PASS) → M5(S09 PASS) → OWNER live decision → S10`

Минимальный путь к portfolio capability:

`first validated/live candidate + later distinct strategy evidence → минимум два portfolio candidates → M7 → M8`

M6 research/discovery may overlap M4 after reusable work packages 4.1–4.8; M5 remains blocked until S07 PASS. Эта последовательность не запрещает параллельный дешёвый Research Funnel для других идей.

---

# 14. Work-in-progress принцип

WIP ограничивается стоимостью стадии:

- много `Idea/Screening` допустимо;
- меньше `Prototype/Candidate`;
- немного deep validation candidates;
- ещё меньше simultaneous live admissions.

Численные WIP limits вводятся только после появления фактической пропускной способности Research Factory.

---

# 15. Что WBS намеренно не фиксирует

WBS не устанавливает без evidence и OWNER decision:

- конкретный broker;
- instrument;
- timeframe;
- programming language торгового runtime;
- cloud/VPS provider;
- размер капитала;
- target annual return;
- risk percentage;
- minimum trade count;
- сроки выполнения milestones.

Эти решения принимаются в соответствующем work package на основании его входов.

---

# 16. Текущая точка исполнения

На 22 сентября 2026 года:

- M0 Program Rebaseline — `COMPLETED / PASS`;
- M1 Research Methodology — `COMPLETED / PASS`;
- M2 Research Platform MVP — `COMPLETED / PASS`;
- M3 Reference Strategy #1 — `COMPLETED / PASS`;
- Reference Strategy #1 research outcome — `REJECTED_AT_R3`;
- M4 Validation Framework — `IN_PROGRESS`;
- `WBS-4.1 — Validation protocol framework` — `DONE`;
- `WBS-4.2 — Parameter sensitivity tooling` — `DONE`;
- `WBS-4.3 — Time/regime slicing` — `DONE`;
- `WBS-4.4 — Trade/observation concentration` — `DONE`;
- `WBS-4.5 — Resampling framework` — `DONE`;
- `WBS-4.6 — Independent exam protocol` — `DONE`;
- `WBS-4.7 — Multiple-research accounting` — `DONE`, OWNER closure confirmed on commit `c3a29500ed5872b11d6fe7dc9429d31165251496`;
- `WBS-4.8 — Class-specific profiles` — `DONE`, exact OWNER launcher PASS confirmed on commit `50f8e7fda9460473af674f9aad45ad9c5831c44f`;
- technical profile artifact: `governance/methodology/TECHNICAL_STRATEGY_VALIDATION_PROFILE.md`;
- `WBS-6.0 — Market Pattern Discovery` — `DONE`; reusable capability and first bounded run are complete;
- M6-000 closure is confirmed on `d5a7e8c60cfacf3fd0ff19dee6f2ebd0c672dba9`;
- M6-001 closure is confirmed on `d08e11f236c2318269314de64da85a7eacbb9105`;
- first discovery outcome: `SHORTLIST_FOR_IDEA_INTAKE`, five of sixteen alternatives, all reversal;
- `WBS-6.1 — Select Strategy #2` — `DONE`, exact OWNER launcher PASS confirmed on commit `34805510000d56ea78e112dc8b4bf7ea574a2cf8`;
- `WBS-6.2 — Run Research Funnel` — `IN_PROGRESS`;
- HYP-0002 formation is `DONE`, exact OWNER launcher PASS confirmed on commit `84aff042c7d57a0e001c35a5a75d29369f983e60`;
- HYP-0002 Data Feasibility preparation is `DONE`, exact OWNER launcher PASS confirmed on commit `8b1e2dbc0e604c7fb3ca8297e0f61f252147619a`;
- HYP-0002 Data Feasibility freeze is `DONE`, exact OWNER launcher PASS confirmed on commit `2f99bbbe688c3f2fc28ea7994f7cc700948af5c7`;
- HYP-0002 PROTO-01 freeze is `DONE`, exact OWNER launcher PASS confirmed on commit `ca7ed470f0aac6a1fed2a1c5a4d487f5fd56557e`;
- HYP-0002 PROTO-01 reveal is `DONE / REJECT`, exact OWNER launcher PASS confirmed on commit `96d7b90ac908cacccfefbccbe8daa06867b2f18c`;
- Reference Strategy #2 research outcome is `REJECTED_AT_R3`;
- WBS-6.3–6.6 and WBS-6.8 are not entered for this rejected line;
- Reference Strategy #2 early-rejection reuse review is `DONE`, exact OWNER launcher PASS confirmed on commit `e1440d999abe4744e9604c06910b8bf1c8449b03`;
- both Reference Strategy #1 and #2 remain rejected at R3;
- M4.9/M4.10 remain blocked until a future research line earns Candidate/S05 eligibility;
- current step is M6 Exit Review.

The current execution target is:

`ATS2-M6-009 — M6 Exit Review`

The proposed M6 decision is PASS against the two-profile Research Factory/platform-generalization exit criterion. It does not claim strategy success and does not open M5. After operational M6 closure, the roadmap requires a separate rebaseline for Strategy #3 sourcing.
