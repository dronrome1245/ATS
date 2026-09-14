# ATS Repository Structure v2

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 2.0  
**Статус:** BASELINE  
**Родительские документы:** `PROGRAM_CHARTER_V2.md`, `OPERATING_MODEL_V2.md`, `STRATEGY_LIFECYCLE_V2.md`, `RESEARCH_METHODOLOGY_V1.md`, `PROGRAM_WBS_V2.md`

## 1. Назначение

Этот документ определяет целевую структуру репозитория ATS v2, канонические места хранения сущностей программы и правила миграции от исторической структуры ATS v1.

Цели структуры:

- новый AI-чат или разработчик быстро находит source of truth;
- program-level и strategy-level артефакты не смешиваются;
- исследования отделены от исполняемой платформы;
- Strategy Version, Experiment, Dataset и Evidence имеют однозначные места и связи;
- общая платформа не дублируется внутри каждой стратегии;
- live/operations-артефакты отделены от research;
- legacy ATS v1 сохраняется, но не может быть принят за текущий roadmap;
- структура может расширяться от первой reference strategy к портфелю без полной реорганизации.

Структура является logical architecture репозитория. Массовое перемещение существующих файлов выполняется отдельными задачами Program Backlog после фиксации migration map.

---

## 2. Принципы структуры

### 2.1 Один canonical program state

Единственный machine-readable state программы:

`03_СОСТОЯНИЕ_ПРОЕКТА.yaml`

Другие state-файлы верхнего уровня запрещены, если они претендуют на тот же источник истины.

### 2.2 Один handoff для нового контекста

Краткое восстановление состояния:

`AI_HANDOFF.md`

Правила агента:

`AGENTS.md`

### 2.3 Program и Strategy разделены

Program governance определяет процесс и общие capabilities.

Каждая стратегия имеет собственный каталог и lifecycle evidence.

### 2.4 Shared code не живёт внутри стратегии

Если capability нужна нескольким стратегиям или является инфраструктурной, она переносится в общий platform layer.

Strategy-specific logic остаётся в каталоге стратегии.

### 2.5 Data не смешиваются с reports и code

Raw/derived data, manifests, experiment outputs и human reports являются разными типами артефактов и хранятся отдельно.

### 2.6 Evidence должен быть адресуемым

Формальный вывод должен ссылаться на конкретный Experiment ID, Strategy Version, Dataset ID и report/evidence artifact.

### 2.7 Legacy остаётся доступным, но явно маркируется

ATS v1 не удаляется ради истории решений. После миграции legacy-файлы должны находиться в отдельном пространстве имён либо иметь явный legacy index.

---

## 3. Целевая структура верхнего уровня

```text
ATS/
├── README.md
├── 00_НАЧАТЬ_ЗДЕСЬ.md
├── AGENTS.md
├── AI_HANDOFF.md
├── 01_СТАТУС_ПРОЕКТА.md
├── 02_СЛЕДУЮЩИЙ_ШАГ.md
├── 03_СОСТОЯНИЕ_ПРОЕКТА.yaml
├── SECURITY.md
│
├── governance/
│   ├── program/
│   ├── methodology/
│   ├── decisions/
│   └── backlog/
│
├── research/
│   ├── ideas/
│   ├── hypotheses/
│   ├── candidates/
│   └── reviews/
│
├── strategies/
│   └── STRAT-.../
│
├── platform/
│   ├── data/
│   ├── backtest/
│   ├── strategy_api/
│   ├── analytics/
│   ├── risk/
│   ├── execution/
│   ├── state/
│   └── monitoring/
│
├── data/
│   ├── manifests/
│   ├── raw/
│   ├── derived/
│   └── external/
│
├── experiments/
│   └── EXP-YYYYMMDD-nnn/
│
├── reports/
│   ├── research/
│   ├── validation/
│   ├── execution/
│   └── portfolio/
│
├── portfolio/
│   ├── policies/
│   ├── allocations/
│   └── reviews/
│
├── operations/
│   ├── deployments/
│   ├── runbooks/
│   ├── incidents/
│   └── reconciliations/
│
├── src/
├── tests/
├── tools/
│
└── legacy/
    └── v1/
```

На M0 эта структура является target layout. Каталоги создаются только когда появляется первый реальный артефакт соответствующего типа; пустые каталоги ради внешнего вида не требуются.

---

# 4. Root — program entrypoints

В корне остаются только документы, которые новый человек или AI должен увидеть без навигации по дереву.

## Canonical root files

| Файл | Назначение |
|---|---|
| `README.md` | Краткое описание ATS и быстрый старт |
| `00_НАЧАТЬ_ЗДЕСЬ.md` | Человекочитаемая последовательность чтения |
| `AGENTS.md` | Обязательные правила AI/automation |
| `AI_HANDOFF.md` | Снимок «что принято / где остановились / что дальше» |
| `01_СТАТУС_ПРОЕКТА.md` | Human-readable program state |
| `02_СЛЕДУЮЩИЙ_ШАГ.md` | Единственная непосредственная следующая program-level работа |
| `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` | Canonical machine-readable program state |
| `SECURITY.md` | Репозиторные и секретные данные / security policy |

Прочая методология и планирование в корень не добавляются.

---

# 5. `governance/` — управление программой

Целевое назначение: program-level документы, не принадлежащие конкретной стратегии.

```text
governance/
├── program/
│   ├── PROGRAM_CHARTER_V2.md
│   ├── OPERATING_MODEL_V2.md
│   ├── PROGRAM_WBS_V2.md
│   └── REPOSITORY_STRUCTURE_V2.md
├── methodology/
│   ├── STRATEGY_LIFECYCLE_V2.md
│   └── RESEARCH_METHODOLOGY_V1.md
├── decisions/
│   └── ADR-....md
└── backlog/
    └── PROGRAM_BACKLOG_V2.md
```

До физической миграции текущие файлы в `00_Управление_проектом/v2/` считаются каноническими. Перенос в `governance/` должен выполняться одной управляемой migration task с обновлением всех ссылок и validator.

---

# 6. `research/` — Research Factory

Здесь живут объекты до formal Strategy Version.

```text
research/
├── ideas/
│   └── IDEA-0001.md
├── hypotheses/
│   └── HYP-0001.md
├── candidates/
│   └── CAND-0001/
│       ├── CANDIDATE.md
│       └── evidence_index.md
└── reviews/
    └── research-review-YYYY-MM-DD.md
```

## Правила

- Idea должна быть лёгкой и дешёвой в создании.
- Hypothesis появляется, когда утверждение стало falsifiable.
- Candidate создаётся только после Economic Pre-Screen.
- rejected/parked объекты не удаляются; меняется их status.
- exploratory notebooks/scripts могут ссылаться на Idea/Hypothesis, но не считаются formal evidence автоматически.

---

# 7. `strategies/` — lifecycle конкретных стратегий

Каждая стратегия получает стабильный Strategy ID.

Пример:

```text
strategies/
└── STRAT-TECH-BREAKOUT-001/
    ├── STRATEGY.md
    ├── strategy.yaml
    ├── versions/
    │   ├── v1.0/
    │   │   ├── VERSION.yaml
    │   │   ├── SPECIFICATION.md
    │   │   ├── PARAMETERS.yaml
    │   │   └── EVIDENCE_INDEX.md
    │   └── v1.1/
    ├── research/
    ├── validation/
    ├── live/
    └── retirement/
```

## `STRATEGY.md`

Стабильное описание стратегии как долгоживущей сущности:

- Strategy ID;
- class;
- economic rationale;
- current status;
- ссылки на версии.

## `strategy.yaml`

Machine-readable identity и текущая Strategy Version.

## `versions/`

Immutable context конкретной версии. Material change создаёт новый каталог версии.

Внутри версии не должны храниться большие raw datasets или дублированный shared platform code.

---

# 8. `platform/` — shared capabilities

Логическая декомпозиция общей платформы:

```text
platform/
├── data/
├── backtest/
├── strategy_api/
├── analytics/
├── risk/
├── execution/
├── state/
└── monitoring/
```

Назначение компонентов:

| Каталог | Ответственность |
|---|---|
| `data/` | ingestion, normalization, timestamp handling, data interfaces |
| `backtest/` | replay/simulation engine и execution assumptions для research |
| `strategy_api/` | общий контракт стратегии с платформой |
| `analytics/` | стандартные метрики и reports |
| `risk/` | Strategy Risk и позже Portfolio Risk primitives |
| `execution/` | order intents, broker adapters, fills/errors |
| `state/` | persistence, recovery, reconciliation primitives |
| `monitoring/` | health, logs, alerts, model/live observation |

Capability создаётся только из доказанной потребности Strategy/Research work package.

---

# 9. `data/` — данные и manifests

```text
data/
├── manifests/
│   └── DATA-....yaml
├── raw/
├── derived/
└── external/
```

## `manifests/`

Версионируемые метаданные Dataset:

- Dataset ID;
- source;
- time range;
- timezone;
- acquisition/creation method;
- cleaning/transformation chain;
- checksum/immutable identifier, когда применимо;
- access constraints;
- relation to protected independent periods.

## `raw/`

Неизменяемые исходные данные, если лицензия и размер позволяют хранение в репозитории/связанном storage.

Большие, лицензируемые или чувствительные данные не обязаны храниться в Git; manifest указывает внешний storage/reference.

## `derived/`

Воспроизводимые преобразованные данные.

## `external/`

Только metadata/pointers на внешние datasets, если сами данные не хранятся в Git.

Секретные broker exports и персональные данные не сохраняются в репозитории.

---

# 10. `experiments/` — формальные эксперименты

Каждый formal experiment получает каталог:

```text
experiments/
└── EXP-20260915-001/
    ├── manifest.yaml
    ├── result.json
    ├── conclusion.md
    └── artifacts/
```

## `manifest.yaml`

Обязательно связывает:

- Experiment ID;
- Hypothesis ID;
- Strategy ID/Version, если уже существует;
- code revision;
- Dataset ID;
- period;
- parameters;
- cost/execution model;
- predefined question;
- research stage.

## `result.json`

Machine-readable ключевые результаты.

## `conclusion.md`

Интерпретация, ограничения, решение `PROMOTE / PARK / REJECT / PASS / FAIL` в зависимости от стадии.

Отрицательный experiment сохраняется полностью.

---

# 11. `reports/` — human-readable evidence

Reports не являются первичным storage experiment raw output.

```text
reports/
├── research/
├── validation/
├── execution/
└── portfolio/
```

Каждый report должен ссылаться на исходные Experiment IDs / Strategy Version / Dataset IDs.

Крупные бинарные артефакты могут храниться вне Git при наличии устойчивой ссылки/идентификатора.

---

# 12. `portfolio/` — portfolio-level решения

Создаётся не раньше фактической необходимости M7.

```text
portfolio/
├── policies/
├── allocations/
└── reviews/
```

## `policies/`

- program-level capital policy;
- concentration constraints;
- portfolio stop rules;
- allocation methodology.

## `allocations/`

История утверждённых allocations с версией и датой решения OWNER.

## `reviews/`

Correlation/exposure/risk contribution/capacity reviews.

---

# 13. `operations/` — эксплуатация

Создаётся по мере появления M5+.

```text
operations/
├── deployments/
├── runbooks/
├── incidents/
└── reconciliations/
```

## `deployments/`

Deployment manifests для demo/shadow/minimal-live/live.

## `runbooks/`

Recovery, restart, emergency stop, broker outage и другие операционные процедуры.

## `incidents/`

Immutable incident records и postmortems.

## `reconciliations/`

Model ↔ broker/runtime сверки исполнения и состояния.

Секреты и credentials здесь не хранятся.

---

# 14. `src/`, `tests/`, `tools/`

## `src/`

Исполняемый код ATS, когда выбран фактический технологический стек.

При необходимости он может отражать logical modules из `platform/`, но документация capability и исходный код не обязаны физически иметь идентичное дерево.

## `tests/`

- unit;
- integration;
- replay;
- failure/fault-injection;
- regression;
- validation of critical risk/execution invariants.

## `tools/`

Repository/research support tooling, которое не является live trading runtime.

`tools/validate_repo.py` относится сюда.

---

# 15. `legacy/` — ATS v1

Целевая структура:

```text
legacy/
└── v1/
    ├── README.md
    ├── program-management/
    ├── product/
    ├── architecture/
    ├── regulations/
    └── registers/
```

`legacy/v1/README.md` должен объяснять:

- период действия ATS v1;
- почему модель superseded;
- какие сильные элементы перенесены в v2;
- что документы v1 не являются текущими instructions/state.

До физического переноса существующие документы v1 остаются на старых путях, но README/AGENTS/state должны явно классифицировать их как legacy.

---

# 16. Canonical entity locations

| Entity | Canonical target location |
|---|---|
| Program State | `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` |
| AI Handoff | `AI_HANDOFF.md` |
| Program governance | `governance/program/` |
| Research methodology | `governance/methodology/` |
| ADR / program decisions | `governance/decisions/` |
| Program Backlog | `governance/backlog/PROGRAM_BACKLOG_V2.md` |
| Idea | `research/ideas/IDEA-....md` |
| Hypothesis | `research/hypotheses/HYP-....md` |
| Candidate | `research/candidates/CAND-..../` |
| Strategy | `strategies/STRAT-..../` |
| Strategy Version | `strategies/STRAT-..../versions/vN.N/` |
| Dataset Manifest | `data/manifests/DATA-....yaml` |
| Experiment | `experiments/EXP-YYYYMMDD-nnn/` |
| Human report | `reports/<class>/` |
| Deployment | `operations/deployments/` |
| Portfolio policy/allocation | `portfolio/` |
| ATS v1 history | `legacy/v1/` |

Во время M0 фактический canonical path уже существующих v2 governance documents остаётся `00_Управление_проектом/v2/` до отдельной migration task. Это временное исключение должно быть устранено перед закрытием WBS-0.12.

---

# 17. Naming rules

## IDs

- Idea: `IDEA-0001`
- Hypothesis: `HYP-0001`
- Candidate: `CAND-0001`
- Strategy: `STRAT-<CLASS>-<NAME>-NNN`
- Experiment: `EXP-YYYYMMDD-nnn`
- Dataset: `DATA-<SOURCE>-<PURPOSE>-NNN`
- Deployment: `DEPLOY-YYYYMMDD-nnn`
- Incident: `INC-YYYYMMDD-nnn`

Идентификаторы после выдачи не переиспользуются.

## Strategy Version

Semantic-style version `vMAJOR.MINOR` используется как identity исследовательской версии; правила увеличения version будут закреплены отдельным template/change-control документом.

---

# 18. Что хранится в Git, а что нет

## В Git

- manifests;
- specifications;
- source code;
- configs без секретов;
- experiment metadata/results разумного размера;
- human reports;
- decision records;
- tests;
- reproducibility instructions.

## Не в Git по умолчанию

- passwords/tokens/private keys;
- broker credentials;
- account identifiers, если они чувствительны;
- персональные документы;
- большие market datasets;
- данные с лицензией, запрещающей redistribution;
- runtime secrets;
- объёмные ephemeral logs.

Для внешнего объекта в Git остаётся manifest/reference, достаточный для воспроизводимости при наличии разрешённого доступа.

---

# 19. Migration map из текущей структуры

| Текущий объект | Целевое место | Действие |
|---|---|---|
| `00_Управление_проектом/v2/*.md` | `governance/program/` или `governance/methodology/` | Перенести после создания Program Backlog и обновить все ссылки атомарно |
| `00_Управление_проектом/ДОРОЖНАЯ_КАРТА.md` | `legacy/v1/program-management/` | Legacy migration |
| `00_Управление_проектом/МАТРИЦА_ВОРОТ.md` | `legacy/v1/program-management/` | Legacy migration |
| `00_Управление_проектом/БЭКЛОГ_ЗАДАЧ.md` | `legacy/v1/program-management/` | Legacy migration |
| `01_Контур_продукта/*` | `legacy/v1/product/` | Сохранить как v1 history; нужные требования переносить в v2 отдельными decisions |
| `02_Архитектура_и_решения/*` | `legacy/v1/architecture/` либо актуальный ADR v2 после review | Не переносить автоматически как current design |
| `03_Нормативная_база_и_правила/*` | `legacy/v1/regulations/` либо governance reference после review | Review перед promotion в v2 |
| `04_Реестры_и_связи/*` | `legacy/v1/registers/` | Legacy migration |
| `05_Коллизии/*` | legacy + перенос ещё актуальных вопросов в v2 backlog | Не терять unresolved history |
| `data/`, `experiments/`, `reports/` | Сохранить top-level, перестроить внутреннюю схему | Эволюционная миграция |
| `src/`, `tests/`, `tools/` | Сохранить top-level | Обновлять по мере появления platform code |

---

# 20. Migration rules

1. Не делать массовый move без Program Backlog item и проверяемого migration scope.
2. Перед move найти все ссылки на старый путь.
3. В одном логическом изменении обновить path, ссылки, validator и handoff, если затронут canonical artifact.
4. Не удалять ATS v1 evidence только потому, что он устарел.
5. Не повышать legacy document до current v2 без review.
6. После каждого migration step запускать repository validator.
7. Если новый path меняет source of truth, сначала обновляется canonical state, затем human entrypoints.

---

# 21. Минимальная структура до Reference Strategy #1

До начала M3 не требуется создавать весь target tree.

Минимально необходимы:

```text
governance/   или временно 00_Управление_проектом/v2/
research/
├── ideas/
├── hypotheses/
└── candidates/
data/
├── manifests/
experiments/
reports/
src/
tests/
tools/
```

`portfolio/` и большая часть `operations/` создаются только при фактической потребности соответствующих milestones.

---

# 22. Definition of Done WBS-0.6

`WBS-0.6 Repository Structure v2` считается завершённым, когда:

1. определены root entrypoints и единственный canonical state;
2. определены canonical target locations Program, Research, Strategy, Platform, Data, Experiment, Report, Portfolio, Operations и Legacy;
3. описаны naming/ID rules;
4. описана граница Git/external storage;
5. существует migration map для текущей структуры;
6. migration не требует преждевременного создания пустой production architecture;
7. следующий Program Backlog может превратить migration и создание templates в исполнимые задачи.

---

# 23. Следующий шаг

После принятия Repository Structure v2 создаётся:

`PROGRAM_BACKLOG_V2.md`

Backlog должен превратить WBS, начиная с оставшихся M0 work packages, в упорядоченные исполнимые задачи с priority, status, dependencies и конкретным deliverable.