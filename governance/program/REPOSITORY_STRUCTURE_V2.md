# ATS Repository Structure v2

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 2.0  
**Статус:** BASELINE  
**Canonical location:** `governance/program/REPOSITORY_STRUCTURE_V2.md`

## 1. Назначение

Этот документ определяет canonical структуру ATS v2 и правила размещения program, research, strategy, platform, data, experiment, evidence, portfolio, operations и legacy artifacts.

Основные цели:

- новый AI-чат или разработчик быстро находит source of truth;
- program-level и strategy-level artifacts не смешиваются;
- exploratory research отделён от formal evidence;
- shared platform отделена от strategy-specific logic;
- Strategy Version, Experiment, Dataset и Evidence имеют устойчивые identities и locations;
- legacy ATS v1 физически и логически отделён от current ATS v2;
- структура расширяется по фактической потребности, без создания пустой универсальной платформы заранее.

---

## 2. Root entrypoints

В корне остаются только глобальные точки входа и repository-wide policies:

| Path | Назначение |
|---|---|
| `README.md` | Краткое описание ATS и быстрый старт |
| `00_НАЧАТЬ_ЗДЕСЬ.md` | Порядок восстановления контекста |
| `AGENTS.md` | Правила AI/automation |
| `AI_HANDOFF.md` | Текущий handoff между чатами/агентами |
| `01_СТАТУС_ПРОЕКТА.md` | Human-readable program status |
| `02_СЛЕДУЮЩИЙ_ШАГ.md` | Единственная непосредственная program-level next task |
| `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` | Единственный canonical machine-readable state |
| `SECURITY.md` | Security/secrets policy |

Другие program documents в root не добавляются.

---

## 3. Canonical top-level structure

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
│   │   └── templates/
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

Пустые каталоги ради внешнего вида не обязательны. Они создаются при появлении первого реального artifact соответствующего типа.

---

## 4. `governance/` — current ATS v2 governance

Current program governance хранится только здесь.

```text
governance/
├── program/
│   ├── PROGRAM_CHARTER_V2.md
│   ├── OPERATING_MODEL_V2.md
│   ├── PROGRAM_WBS_V2.md
│   └── REPOSITORY_STRUCTURE_V2.md
├── methodology/
│   ├── STRATEGY_LIFECYCLE_V2.md
│   ├── RESEARCH_METHODOLOGY_V1.md
│   └── templates/
├── decisions/
│   └── ADR-....md
└── backlog/
    └── PROGRAM_BACKLOG_V2.md
```

`00_Управление_проектом/v2/` больше не является current ATS v2 location. После `ATS2-M0-009` migrated copies в этом старом path запрещены validator-ом.

---

## 5. `research/` — Research Factory entities

До появления formal Strategy Version используются:

```text
research/
├── ideas/
│   └── IDEA-0001.md
├── hypotheses/
│   └── HYP-0001.md
├── candidates/
│   └── CAND-0001/
│       ├── CANDIDATE.md
│       └── EVIDENCE_INDEX.md
└── reviews/
    └── research-review-YYYY-MM-DD.md
```

Правила:

- Idea должна быть дешёвой в создании;
- Hypothesis должна быть falsifiable до formal evidence;
- Candidate создаётся только после `R4 Economic Pre-Screen = PROMOTE`;
- rejected/parked entities не удаляются;
- exploratory output не становится formal evidence автоматически.

Canonical templates: `governance/methodology/templates/`.

---

## 6. `strategies/` — Strategy и Strategy Version

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

`STRATEGY.md` описывает долгоживущую strategy entity. `strategy.yaml` хранит machine-readable identity/current version. Каталог `versions/` содержит immutable research context конкретных версий.

Material change создаёт новую Strategy Version; историческая версия не переписывается.

---

## 7. `platform/` — reusable capabilities

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

Shared capability появляется из доказанной потребности strategy/research work package. Код, специфичный только для одной стратегии, не переносится в shared layer без основания.

---

## 8. `data/`

```text
data/
├── manifests/
│   └── DATA-....yaml
├── raw/
├── derived/
└── external/
```

Dataset manifest фиксирует ID, source, coverage, timezone/timestamp semantics, transformation chain, checksum/identifier, access constraints и связь с protected evidence periods.

Большие, лицензируемые или чувствительные datasets могут находиться вне Git; в репозитории остаётся достаточный metadata reference. Credentials, private broker exports и personal data в Git не хранятся.

---

## 9. `experiments/`

Formal experiment:

```text
experiments/
└── EXP-20260915-001/
    ├── manifest.yaml
    ├── result.json
    ├── conclusion.md
    └── artifacts/
```

Manifest связывает Experiment ID, Hypothesis, Strategy Version при наличии, code revision, Dataset ID, period, parameters, cost/execution model, predefined question и research stage.

Отрицательные experiments сохраняются полностью.

---

## 10. `reports/`

```text
reports/
├── research/
├── validation/
├── execution/
└── portfolio/
```

Human-readable report должен ссылаться на исходные Experiment IDs, Strategy Version и Dataset IDs. Reports не заменяют experiment manifest/raw evidence.

---

## 11. `portfolio/`

Создаётся при фактической потребности M7:

```text
portfolio/
├── policies/
├── allocations/
└── reviews/
```

Здесь хранятся program-level capital/risk policies, versioned allocation decisions и portfolio reviews.

---

## 12. `operations/`

Создаётся по мере M5+:

```text
operations/
├── deployments/
├── runbooks/
├── incidents/
└── reconciliations/
```

Содержит deployment manifests, recovery/emergency procedures, immutable incident records/postmortems и model↔runtime/broker reconciliations. Secrets здесь не хранятся.

---

## 13. `src/`, `tests/`, `tools/`

- `src/` — executable ATS code после выбора фактического stack;
- `tests/` — unit/integration/replay/failure/regression tests;
- `tools/` — repository/research support tooling, не live trading runtime.

`tools/validate_repo.py` является repository validator.

---

## 14. `legacy/v1/`

ATS v1 сохраняется как history/reference, но физически отделяется от current ATS v2.

Target:

```text
legacy/v1/
├── README.md
├── program-management/
├── product/
├── architecture/
├── regulations/
└── registers/
```

`legacy/v1/README.md` является обязательным index: объясняет период действия v1, причину supersede, классификацию artifacts, перенос сильных требований в v2 и список review-needed/carryover items.

Ни один legacy document не становится current v2 governance без отдельного review/decision.

---

## 15. Canonical entity locations

| Entity | Canonical location |
|---|---|
| Program State | `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` |
| AI Handoff | `AI_HANDOFF.md` |
| Program Charter | `governance/program/PROGRAM_CHARTER_V2.md` |
| Operating Model | `governance/program/OPERATING_MODEL_V2.md` |
| Program WBS | `governance/program/PROGRAM_WBS_V2.md` |
| Repository Structure | `governance/program/REPOSITORY_STRUCTURE_V2.md` |
| Strategy Lifecycle | `governance/methodology/STRATEGY_LIFECYCLE_V2.md` |
| Research Methodology | `governance/methodology/RESEARCH_METHODOLOGY_V1.md` |
| Research Templates | `governance/methodology/templates/` |
| Program Backlog | `governance/backlog/PROGRAM_BACKLOG_V2.md` |
| ADR / Program decisions | `governance/decisions/` |
| Idea | `research/ideas/IDEA-....md` |
| Hypothesis | `research/hypotheses/HYP-....md` |
| Candidate | `research/candidates/CAND-..../` |
| Strategy | `strategies/STRAT-..../` |
| Strategy Version | `strategies/STRAT-..../versions/vN.N/` |
| Dataset Manifest | `data/manifests/DATA-....yaml` |
| Experiment | `experiments/EXP-YYYYMMDD-nnn/` |
| Human Report | `reports/<class>/` |
| Deployment | `operations/deployments/` |
| Portfolio artifacts | `portfolio/` |
| ATS v1 | `legacy/v1/` |

---

## 16. Naming rules

Stable IDs:

- Idea: `IDEA-0001`
- Hypothesis: `HYP-0001`
- Candidate: `CAND-0001`
- Strategy: `STRAT-<CLASS>-<NAME>-NNN`
- Experiment: `EXP-YYYYMMDD-nnn`
- Dataset: `DATA-<SOURCE>-<PURPOSE>-NNN`
- Deployment: `DEPLOY-YYYYMMDD-nnn`
- Incident: `INC-YYYYMMDD-nnn`

ID после выдачи не переиспользуется.

Strategy Version использует `vMAJOR.MINOR` как version identity; material trade-affecting change создаёт новую version.

---

## 17. Git vs external storage

### В Git

- manifests;
- specifications;
- source code;
- non-secret configs;
- experiment metadata/results разумного размера;
- human reports;
- decision records;
- tests;
- reproducibility instructions.

### Вне Git по умолчанию

- passwords/tokens/private keys;
- broker credentials;
- sensitive account identifiers;
- personal documents;
- большие market datasets;
- non-redistributable licensed data;
- runtime secrets;
- large ephemeral logs.

Для внешних artifacts в Git хранится stable metadata/reference, необходимый для reproducibility при разрешённом доступе.

---

## 18. Migration status

### Completed: `ATS2-M0-009`

Current ATS v2 governance physically migrated:

- Program Charter → `governance/program/PROGRAM_CHARTER_V2.md`;
- Operating Model → `governance/program/OPERATING_MODEL_V2.md`;
- Program WBS → `governance/program/PROGRAM_WBS_V2.md`;
- Repository Structure → `governance/program/REPOSITORY_STRUCTURE_V2.md`;
- Strategy Lifecycle → `governance/methodology/STRATEGY_LIFECYCLE_V2.md`;
- Research Methodology → `governance/methodology/RESEARCH_METHODOLOGY_V1.md`;
- templates → `governance/methodology/templates/`;
- Program Backlog → `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Old current-v2 copies under `00_Управление_проектом/v2/` are not allowed to coexist with canonical files.

### Remaining: ATS v1 legacy migration

| Current v1 area | Target |
|---|---|
| `00_Управление_проектом/` legacy files | `legacy/v1/program-management/` |
| `01_Контур_продукта/` | `legacy/v1/product/` |
| `02_Архитектура_и_решения/` | `legacy/v1/architecture/` unless reviewed/promoted separately |
| `03_Нормативная_база_и_правила/` | `legacy/v1/regulations/` unless reviewed/promoted separately |
| `04_Реестры_и_связи/` | `legacy/v1/registers/` |
| `05_Коллизии/` | legacy plus explicit carryover of still-relevant questions into v2 backlog |

Physical legacy migration happens only after `ATS2-M0-010` creates `legacy/v1/README.md` and migration index.

---

## 19. Migration rules

1. Не делать mass move без Program Backlog task.
2. Перед move определить inbound references.
3. В одном логическом migration step обновлять paths, canonical state, handoff, backlog и validator.
4. Не удалять historical evidence из-за supersede.
5. Не повышать legacy document до current v2 без review.
6. После migration запускать repository validator.
7. Если меняется source of truth, state/handoff переключаются до удаления старой копии.

---

## 20. Definition of Done WBS-0.6

Repository Structure считается принятой, когда:

1. существует один canonical state;
2. canonical locations всех основных entity classes определены;
3. current governance физически находится в `governance/`;
4. naming/ID rules определены;
5. Git/external-storage boundary определена;
6. ATS v1 имеет отдельный target namespace `legacy/v1/`;
7. migrations управляются через Program Backlog и validator.

---

## 21. Текущий следующий шаг

После завершения `ATS2-M0-009` выполняется:

`ATS2-M0-010 — Legacy v1 index/classification`.

Следующий artifact:

`legacy/v1/README.md`.
