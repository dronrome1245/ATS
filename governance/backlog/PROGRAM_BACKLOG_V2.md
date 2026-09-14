# ATS Program Backlog v2

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 2.0  
**Статус:** BASELINE  
**Дата:** 15 сентября 2026 года  
**WBS:** `00_Управление_проектом/v2/PROGRAM_WBS_V2.md`  
**Repository Structure:** `00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md`

## 1. Назначение

Этот backlog превращает Program WBS в исполнимую очередь работ.

WBS остаётся baseline декомпозиции M0–M8. Backlog отвечает на более практический вопрос: **что конкретно делать дальше, в каком порядке, при каких зависимостях и какой проверяемый результат должен появиться**.

Правила:

- task получает стабильный ID и не переиспользуется;
- сроки не назначаются без фактического исполнителя, входов и оценки сложности;
- одновременно активируется минимально необходимое число дорогих задач;
- дальние milestones не детализируются преждевременно;
- закрытие task требует deliverable и выполнения Definition of Done;
- после material program-level task синхронизируются canonical state, status, next action и AI handoff;
- task не может считаться `DONE`, если canonical handoff всё ещё указывает на неё как на незавершённую.

---

## 2. Статусы

| Status | Значение |
|---|---|
| `DONE` | Deliverable существует, DoD выполнен, handoff/state синхронизированы |
| `IN_PROGRESS` | Работа фактически выполняется сейчас |
| `READY` | Все зависимости выполнены; задача является допустимым следующим действием |
| `BLOCKED` | Зависимость или необходимое решение отсутствует; причина указана явно |
| `NOT_STARTED` | Задача определена, но ещё не активирована |
| `PARKED` | Намеренно отложена до приближения соответствующего milestone |
| `CANCELLED` | Задача больше не требуется; причина сохраняется в backlog |

---

## 3. Приоритеты

| Priority | Значение |
|---|---|
| `P0` | Критический путь текущего milestone; без задачи нельзя продвигать program state |
| `P1` | Ближайший следующий milestone или обязательная supporting capability |
| `P2` | Следующий технический milestone после P1; не активировать раньше входов |
| `P3` | Future epic / later-stage work, сохраняется для видимости без ранней детализации |

Priority не является обещанием календарного срока.

---

## 4. Текущая execution queue

Текущий допустимый порядок:

1. `ATS2-M0-008` — Research entity templates — `DONE`.
2. `ATS2-M0-009` — Governance v2 path migration — `READY`.
3. `ATS2-M0-010` — Legacy v1 index/classification — после governance migration.
4. `ATS2-M0-011` — Legacy physical migration and unresolved-question carryover — после classification.
5. `ATS2-M0-012` — Final link/validator sweep — после structural migrations.
6. `ATS2-M0-013` — M0 Exit Review — после всех обязательных M0 tasks.

До `ATS2-M0-013 = DONE` задачи M1 не переводятся в `READY`.

---

# 5. M0 — Program Rebaseline

| Task ID | WBS | Scope | Priority | Status | Responsible | Dependencies | Deliverable | Definition of Done / block reason |
|---|---|---:|---:|---|---|---|---|---|
| `ATS2-M0-001` | `WBS-0.1` | P | P0 | DONE | OWNER | — | `PROGRAM_CHARTER_V2.md` | Mission, scope, success/failure criteria и milestones зафиксированы |
| `ATS2-M0-002` | `WBS-0.2` | P | P0 | DONE | OWNER / PROGRAM | M0-001 | `OPERATING_MODEL_V2.md` | Entities, contours, states, roles и decision points определены |
| `ATS2-M0-003` | `WBS-0.3` | P | P0 | DONE | RESEARCH / RISK / VALIDATION | M0-001, M0-002 | `STRATEGY_LIFECYCLE_V2.md` | Research Funnel и lifecycle Strategy Version определены |
| `ATS2-M0-004` | `WBS-0.4` | P | P0 | DONE | RESEARCH / VALIDATION | M0-002, M0-003 | `RESEARCH_METHODOLOGY_V1.md` | Evidence of edge и economic usefulness разделены и формализованы |
| `ATS2-M0-005` | `WBS-0.5` | P | P0 | DONE | PROGRAM | M0-001…004 | `PROGRAM_WBS_V2.md` | M0–M8 имеют deliverable-oriented decomposition, roles, dependencies и DoD |
| `ATS2-M0-006` | `WBS-0.6` | P | P0 | DONE | PROGRAM / DEVELOPMENT | M0-005 | `REPOSITORY_STRUCTURE_V2.md` | Target layout, entity locations, naming и migration rules определены |
| `ATS2-M0-007` | `WBS-0.7` | P | P0 | DONE | PROGRAM | M0-005, M0-006 | `governance/backlog/PROGRAM_BACKLOG_V2.md` | M0 remainder и ближайшие M1/M2 work packages представлены исполнимыми tasks |
| `ATS2-M0-008` | `WBS-0.8` | P | P0 | DONE | RESEARCH / PROGRAM | M0-004, M0-006, M0-007 | `governance/methodology/templates/README.md` + entity templates | Idea, Hypothesis, Candidate, Experiment и Strategy Version создаются без повторного проектирования структуры; templates согласованы с Lifecycle/Methodology и не содержат выдуманных фактов |
| `ATS2-M0-009` | `WBS-0.6`, `WBS-0.12` | P | P0 | READY | PROGRAM / DEVELOPMENT | M0-008 | V2 governance migration commit | Charter/Operating/WBS/Structure переносятся в `governance/program/`, Lifecycle/Methodology/templates — в `governance/methodology/`; все canonical links, handoff, state, backlog references и validator обновляются атомарно; старые current-v2 paths после проверки удаляются |
| `ATS2-M0-010` | `WBS-0.12` | P | P0 | BLOCKED | PROGRAM | M0-009 | `legacy/v1/README.md` + migration index | **Блокировка:** выполнить после current-v2 path migration, чтобы current и legacy пространства были однозначно разделены. Index классифицирует каждый v1 artifact как history/reference/review-needed |
| `ATS2-M0-011` | `WBS-0.12` | P | P0 | BLOCKED | PROGRAM / DEVELOPMENT | M0-010 | `legacy/v1/` populated + carryover list | **Блокировка:** нужен утверждённый legacy index. V1 program/product/architecture/regulations/registers переносятся без потери истории; ещё актуальные открытые вопросы переносятся в v2 backlog отдельными tasks |
| `ATS2-M0-012` | `WBS-0.10`, `WBS-0.12` | P | P0 | BLOCKED | DEVELOPMENT / PROGRAM | M0-009, M0-011 | Final M0 validator/link sweep | **Блокировка:** structural moves ещё не завершены. После них validator проверяет target paths, отсутствие current refs на legacy как source of truth и handoff/state consistency |
| `ATS2-M0-013` | M0 Exit | P | P0 | BLOCKED | OWNER / PROGRAM | M0-008…012 | `M0_EXIT_REVIEW.md` либо эквивалентное принятое решение | **Блокировка:** остаются governance/legacy migrations и final sweep. Exit review подтверждает WBS-0.1…0.12, зелёный CI и способность нового агента определить M1 next action без внешнего контекста |

### Уже завершённые cross-cutting M0 capabilities

Следующие WBS work packages выполнены и не требуют отдельной активной task:

- `WBS-0.9` Canonical state v2 — `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
- `WBS-0.10` Repository validator v2 — текущий validator действует, финальный path sweep остаётся в `ATS2-M0-012`;
- `WBS-0.11` AI handoff protocol — `AI_HANDOFF.md` и agent pointers.

---

# 6. M1 — Research Factory

Все задачи M1 блокируются `ATS2-M0-013` до официального закрытия M0. Они уже достаточно близки, чтобы иметь executable definition.

| Task ID | WBS | Scope | Priority | Status | Responsible | Dependencies | Deliverable | Definition of Done / block reason |
|---|---|---:|---:|---|---|---|---|---|
| `ATS2-M1-001` | `WBS-1.1` | P | P1 | BLOCKED | RESEARCH | M0-013 | Idea intake process + tested Idea template | **Блокировка:** M0 не закрыт. После старта M1 Idea можно зарегистрировать с ID, rationale, market/horizon и required data |
| `ATS2-M1-002` | `WBS-1.2` | P | P1 | BLOCKED | RESEARCH | M1-001 | Hypothesis model + tested template | **Блокировка:** Idea intake ещё не operational. Hypothesis содержит falsifiable statement, mechanism, expected effect и falsification path |
| `ATS2-M1-003` | `WBS-1.3` | P | P1 | BLOCKED | DATA | M1-002 | Data Feasibility review model | **Блокировка:** Hypothesis model не operational. Review покрывает availability, timestamps, bias/leakage risks, costs и known gaps |
| `ATS2-M1-004` | `WBS-1.4` | P | P1 | BLOCKED | RESEARCH | M1-002, M1-003 | Cheap Prototype protocol | **Блокировка:** нужны Hypothesis и Data Feasibility models. Protocol ограничивает prototype одним ранним вопросом и отделяет его от formal validation |
| `ATS2-M1-005` | `WBS-1.5` | P | P1 | BLOCKED | RESEARCH | M1-004 | Economic Pre-Screen rubric | **Блокировка:** prototype protocol ещё не принят. Rubric оценивает magnitude, likely costs, opportunities, capital usage и complexity до Candidate |
| `ATS2-M1-006` | `WBS-1.6` | P | P1 | BLOCKED | RESEARCH / VALIDATION | M1-005 | Candidate promotion process | **Блокировка:** Economic Pre-Screen отсутствует. `PROMOTE / PARK / REJECT` привязано к сохранённым preliminary evidence |
| `ATS2-M1-007` | `WBS-1.7` | P | P1 | BLOCKED | RESEARCH / DEVELOPMENT | M0-008, M1-002 | Experiment registration schema | **Блокировка:** M0 не закрыт и Hypothesis model ещё не operational. Manifest связывает code, data, parameters, costs, predefined question и result |
| `ATS2-M1-008` | `WBS-1.8` | P | P1 | BLOCKED | PROGRAM / RESEARCH | M1-007 | Experiment registry | **Блокировка:** formal Experiment schema не operational. Положительные и отрицательные experiments находятся по stable ID |
| `ATS2-M1-009` | `WBS-1.9` | P | P1 | BLOCKED | VALIDATION | M0-013 | Evidence taxonomy operationalization | **Блокировка:** M0 не закрыт. Taxonomy связывает exploratory, registered, validation, independent, demo/shadow и live evidence с допустимыми решениями |
| `ATS2-M1-010` | `WBS-1.10` | P | P1 | BLOCKED | OWNER / RESEARCH | M1-001…009 | Research review protocol | **Блокировка:** upstream Research Factory components ещё не operational. Review может повторяемо решать `PROMOTE / PARK / REJECT` |
| `ATS2-M1-011` | M1 Exit | P | P1 | BLOCKED | OWNER / PROGRAM | M1-001…010 | M1 exit decision | **Блокировка:** M1 tasks не выполнены. Exit подтверждает, что Idea → Prototype → Candidate decision можно провести воспроизводимо |

---

# 7. M2 — Shared Research Platform MVP

M2 содержит только ближайшие prerequisites и platform work из WBS. Задачи остаются `PARKED` до M1 Exit; это сознательно предотвращает строительство универсальной платформы без research consumer.

## Dependency refinement

В WBS `WBS-2.1` требует выбирать stack с учётом Reference Strategy #1, тогда как `WBS-3.1` формально выбирает саму Reference Strategy после M2. Чтобы не создать циклическую зависимость, backlog вводит подготовительную task `ATS2-M2-000`:

- она **не выбирает торговую стратегию или инструмент**;
- она фиксирует минимальный consumer profile для первого vertical slice: простой data model, доступная история, понятная execution semantics и возможность ручной проверки;
- фактическая Reference Strategy #1 остаётся решением M3.

| Task ID | WBS | Scope | Priority | Status | Responsible | Dependencies | Deliverable | Definition of Done / activation condition |
|---|---|---:|---:|---|---|---|---|---|
| `ATS2-M2-000` | WBS refinement | P | P2 | PARKED | RESEARCH / DEVELOPMENT | M1-011 | Reference Consumer Profile | Активировать после M1 Exit. Profile задаёт требования первого research vertical slice без выбора конкретного edge/instrument |
| `ATS2-M2-001` | `WBS-2.1` | P | P2 | PARKED | DEVELOPMENT | M1-011, M2-000 | Research stack ADR | Минимальный stack выбран по reproducibility/data/consumer needs, а не по желанию построить универсальную платформу |
| `ATS2-M2-002` | `WBS-2.2` | P | P2 | PARKED | DEVELOPMENT | M2-001 | Environment specification | Новый environment воспроизводимо запускает registered experiment |
| `ATS2-M2-003` | `WBS-2.3` | P | P2 | PARKED | DATA / DEVELOPMENT | M1-003, M2-001 | Dataset manifest support | Dataset получает stable ID, source, period и transformation trace |
| `ATS2-M2-004` | `WBS-2.4` | P | P2 | PARKED | DEVELOPMENT / DATA | M2-003 | Base data loader | Reference-class data читаются детерминированно с явными timezone/ordering rules |
| `ATS2-M2-005` | `WBS-2.5` | P | P2 | PARKED | DEVELOPMENT | M2-001 | Minimal Strategy API | Strategy получает data и возвращает decisions/trades без broker-specific code |
| `ATS2-M2-006` | `WBS-2.6` | P | P2 | PARKED | DEVELOPMENT | M2-004, M2-005 | Deterministic backtest/replay core | Один manifest даёт воспроизводимый trade/result output |
| `ATS2-M2-007` | `WBS-2.7` | P | P2 | PARKED | DEVELOPMENT / RESEARCH | M2-006 | Cost model interface | Fees/spread/slippage являются explicit experiment inputs |
| `ATS2-M2-008` | `WBS-2.8` | P | P2 | PARKED | RESEARCH / DEVELOPMENT | M2-006, M2-007 | Standard baseline analytics | Run выдаёт стандартный минимум P&L, drawdown, trades, costs и distributions |
| `ATS2-M2-009` | `WBS-2.9` | P | P2 | PARKED | DEVELOPMENT | M1-007, M2-002…008 | Manifest-driven experiment runner | Registered experiment повторяется документированной процедурой |
| `ATS2-M2-010` | `WBS-2.10` | P | P2 | PARKED | TESTER / DEVELOPMENT | M2-004…009 | Research platform tests | Критические расчёты имеют deterministic fixture и automated regression checks |
| `ATS2-M2-011` | M2 Exit | P | P2 | PARKED | OWNER / PROGRAM | M2-001…010 | M2 exit decision | Минимальный reusable research vertical slice воспроизводимо запускает experiment и report |

---

# 8. Future epics M3–M8

Эти milestones намеренно не разворачиваются сейчас в активные detailed tasks. Их детализация выполняется при приближении milestone и наличии фактических evidence/inputs.

| Epic ID | Milestone | Priority | Status | Activation condition | Outcome |
|---|---|---:|---|---|---|
| `ATS2-EPIC-M3` | Reference Strategy #1 | P3 | PARKED | M1 + M2 Exit | Первая стратегия проходит `R0 → S05` и проверяет research factory/platform |
| `ATS2-EPIC-M4` | Validation Framework | P3 | PARKED | Strategy #1 `S05 PASS` | Robustness, independent examination и validation framework проверены на реальном candidate |
| `ATS2-EPIC-M5` | Execution Platform | P3 | PARKED | Candidate `S07 PASS` | Demo/shadow-capable execution, state, reconciliation, monitoring и risk controls |
| `ATS2-EPIC-M6` | Reference Strategy #2 | P3 | PARKED | Shared platform + первая validated line | Стратегия другого класса проверяет универсальность общей платформы |
| `ATS2-EPIC-M7` | Portfolio Layer | P3 | PARKED | Минимум две portfolio-relevant strategy lines | Exposure/correlation/allocation/portfolio-risk management |
| `ATS2-EPIC-M8` | Controlled Live Portfolio | P3 | PARKED | Portfolio layer + OWNER capital decisions | Ограниченный live-портфель с monitoring и evidence-based allocation |

---

# 9. Backlog operating rules

## 9.1 Единственная program-level next task

`02_СЛЕДУЮЩИЙ_ШАГ.md` указывает только на одну основную program-level работу. Наличие многих `READY` tasks в будущем не должно превращаться в параллельное выполнение без явной необходимости.

## 9.2 Декомпозиция по мере приближения

- M0, M1, M2 — детализированы сейчас;
- M3–M8 — остаются epics;
- перед началом нового milestone его WBS packages превращаются в executable tasks с фактическими dependencies и evidence requirements.

## 9.3 Новые задачи

Новая task добавляется, если:

- обнаружен обязательный deliverable;
- migration/review выявила сохраняющийся вопрос;
- strategy/platform work создаёт доказанную reusable need;
- incident/evidence gap требует корректирующей работы.

Task не добавляется только ради идеи «когда-нибудь пригодится».

## 9.4 Blocked discipline

`BLOCKED` обязан иметь причину и upstream dependency/decision. Нельзя использовать `BLOCKED` как синоним отсутствия приоритета.

## 9.5 Done discipline

Перед `DONE` проверить:

1. deliverable существует;
2. DoD выполнен;
3. ссылки/validator обновлены, если структура изменилась;
4. canonical state/handoff синхронизированы для material program-level task;
5. отрицательные результаты/evidence не удалены.

---

# 10. Следующий шаг

Текущая ready task:

`ATS2-M0-009 — Governance v2 path migration`.

Задача должна атомарно перенести current-v2 governance documents в target tree:

- Charter / Operating Model / Program WBS / Repository Structure → `governance/program/`;
- Strategy Lifecycle / Research Methodology → `governance/methodology/`;
- templates уже находятся в target `governance/methodology/templates/`.

В том же логическом изменении обновляются все ссылки, canonical state, handoff, backlog references и validator. Старые current-v2 пути удаляются только после успешной проверки новых canonical путей.
