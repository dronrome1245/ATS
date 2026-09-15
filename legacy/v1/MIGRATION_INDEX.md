# ATS v1 Migration Index

**Task:** `ATS2-M0-010`  
**Status:** BASELINE  
**Purpose:** классифицировать ATS v1 artifacts до физической миграции в `legacy/v1/`.

## 1. Правило

Classification описывает, как использовать документ **после** архивации:

- `HISTORY` — только история/traceability;
- `REFERENCE` — полезный справочный материал, но current source of truth находится в ATS v2;
- `REVIEW_NEEDED` — перед любым переносом смысла в current v2 требуется отдельный review/decision/task.

Все перечисленные файлы физически архивируются в `legacy/v1/` в `ATS2-M0-011`. `REVIEW_NEEDED` не означает, что старый файл остаётся current.

## 2. Полный inventory

| # | Current v1 path | Classification | Legacy target | Причина | Carryover action |
|---|---|---|---|---|---|
| 1 | `00_Управление_проектом/БЭКЛОГ_ЗАДАЧ.md` | `HISTORY` | `legacy/v1/program-management/БЭКЛОГ_ЗАДАЧ.md` | Старый backlog полностью привязан к G01–G13 и заменён `PROGRAM_BACKLOG_V2.md` | Не переносить tasks автоматически; v2 backlog уже покрывает программу |
| 2 | `00_Управление_проектом/ДОРОЖНАЯ_КАРТА.md` | `REFERENCE` | `legacy/v1/program-management/ДОРОЖНАЯ_КАРТА.md` | Историческая последовательность G01–G13; полезна для traceability mapping в Lifecycle v2 | Current lifecycle — `governance/methodology/STRATEGY_LIFECYCLE_V2.md` |
| 3 | `00_Управление_проектом/МАТРИЦА_ВОРОТ.md` | `REFERENCE` | `legacy/v1/program-management/МАТРИЦА_ВОРОТ.md` | Содержит полезные evidence/return rules, уже переработанные в v2 | Использовать только как source rationale; критерии v2 задаются Lifecycle/Methodology |
| 4 | `00_Управление_проектом/РЕЕСТР_ЭКСПЕРИМЕНТОВ.csv` | `HISTORY` | `legacy/v1/program-management/РЕЕСТР_ЭКСПЕРИМЕНТОВ.csv` | Реестр пуст и использует gate-oriented schema v1 | Новый Experiment model задаётся templates и будущим M1 registry |
| 5 | `01_Контур_продукта/ВИДЕНИЕ_И_ЦЕЛИ.md` | `REFERENCE` | `legacy/v1/product/ВИДЕНИЕ_И_ЦЕЛИ.md` | Основные принципы доказательности/версий/защиты уже включены в Program Charter v2 | Current mission/scope — `governance/program/PROGRAM_CHARTER_V2.md` |
| 6 | `01_Контур_продукта/ФУНКЦИОНАЛЬНЫЕ_ТРЕБОВАНИЯ.md` | `REVIEW_NEEDED` | `legacy/v1/product/ФУНКЦИОНАЛЬНЫЕ_ТРЕБОВАНИЯ.md` | Содержит полезные risk/execution/state/logging/testing/version requirements, но они сформулированы для одного робота | В `CARRYOVER.md` создать review item для M2/M5 platform requirements; не копировать как current requirements без review |
| 7 | `02_Архитектура_и_решения/АРХИТЕКТУРА_РОБОТА.md` | `REVIEW_NEEDED` | `legacy/v1/architecture/АРХИТЕКТУРА_РОБОТА.md` | Компоненты protective/execution/state/audit полезны, но архитектура слишком robot-centric для Strategy Factory | В `CARRYOVER.md` создать architecture review item перед platform/execution architecture |
| 8 | `02_Архитектура_и_решения/БАЗОВЫЙ_СТЕК.md` | `REVIEW_NEEDED` | `legacy/v1/architecture/БАЗОВЫЙ_СТЕК.md` | Repo stack частично актуален, runtime stack не принят; MT5/MQL5 лишь кандидат | Технологический runtime пересмотреть в `ATS2-M2-001 Research stack ADR`; не считать MT5 принятым |
| 9 | `02_Архитектура_и_решения/ADR/ADR-0001-13-ворот.md` | `HISTORY` | `legacy/v1/architecture/ADR/ADR-0001-13-ворот.md` | Решение нормализует именно superseded G01–G13 model | Сохранить только историю причин v1 |
| 10 | `02_Архитектура_и_решения/ADR/ADR-0002-защитный-контур.md` | `REFERENCE` | `legacy/v1/architecture/ADR/ADR-0002-защитный-контур.md` | Принцип независимого risk/protective layer остаётся действующим и уже перенесён в v2 | Current source — Operating Model / Lifecycle / AGENTS; новый ADR нужен только если появится архитектурное решение implementation-level |
| 11 | `02_Архитектура_и_решения/ADR/ADR-0003-независимый-период.md` | `REFERENCE` | `legacy/v1/architecture/ADR/ADR-0003-независимый-период.md` | Принцип one-shot independent evidence сохранён в v2 Methodology/Lifecycle | Current source — `RESEARCH_METHODOLOGY_V1.md` и `STRATEGY_LIFECYCLE_V2.md` |
| 12 | `03_Нормативная_база_и_правила/ИСТОЧНИКИ.md` | `REVIEW_NEEDED` | `legacy/v1/regulations/ИСТОЧНИКИ.md` | Внешние источники привязаны к иллюстративным FCA/MT5 assumptions и должны проверяться на актуальность/применимость | Создать future legal/platform source review только при выборе jurisdiction/broker/platform |
| 13 | `03_Нормативная_база_и_правила/РЕГЛАМЕНТЫ.md` | `REVIEW_NEEDED` | `legacy/v1/regulations/РЕГЛАМЕНТЫ.md` | Содержит полезный checklist, но юрисдикция/инструмент/broker не определены и G02 superseded | Перенести checklist в future Live Environment/legal review task, а не объявлять current policy |
| 14 | `04_Реестры_и_связи/РЕЕСТР_АРТЕФАКТОВ.csv` | `HISTORY` | `legacy/v1/registers/РЕЕСТР_АРТЕФАКТОВ.csv` | Реестр объявляет старые v1 docs ACTIVE/source-of-truth и поэтому не может оставаться operational | Current sources определяются state/handoff/backlog/validator v2 |
| 15 | `05_Коллизии/ОТКРЫТЫЕ_ВОПРОСЫ.md` | `REVIEW_NEEDED` | `legacy/v1/collisions/ОТКРЫТЫЕ_ВОПРОСЫ.md` | OQ-001…009 содержат реальные незакрытые решения, но их прежняя блокирующая логика G01/G02 больше не соответствует v2 | Каждый OQ remap в `CARRYOVER.md`; research не блокируется вопросами, относящимися только к будущему live |

## 3. Итог классификации

- `HISTORY`: 4 artifacts;
- `REFERENCE`: 5 artifacts;
- `REVIEW_NEEDED`: 6 artifacts;
- всего: 15 artifacts.

## 4. Review-needed carryover map

Следующий шаг не должен автоматически создавать финансовые или торговые решения. Он должен только перенести незакрытые вопросы в корректные v2 stages.

### Functional requirements

Источник: `01_Контур_продукта/ФУНКЦИОНАЛЬНЫЕ_ТРЕБОВАНИЯ.md`.

Нужно сохранить для будущего review группы требований:

- independent Strategy Risk / Portfolio Risk;
- stable intent ID / idempotency;
- state recovery and reconciliation;
- safe mode on unknown position;
- reject/partial-fill/slippage/latency logging;
- end-to-end audit trail;
- stress/fault testing;
- Strategy Version linkage.

Потенциальные owners: M2 platform design и M5 execution/live readiness.

### Robot architecture

Источник: `02_Архитектура_и_решения/АРХИТЕКТУРА_РОБОТА.md`.

Полезные concepts должны быть рассмотрены при будущей platform architecture, но не копируются буквально. В частности: market data adapter, strategy intent, protective controller, execution adapter, persistent state, audit, watchdog, test/replay contour.

### Technology stack

Источник: `02_Архитектура_и_решения/БАЗОВЫЙ_СТЕК.md`.

Repo tooling Git/GitHub/Markdown/YAML/Python/GitHub Actions уже фактически используется. Trading runtime/API/database/cloud/VPS/monitoring остаются undecided. MT5/MQL5 остаётся только историческим кандидатом.

### Regulatory sources and rules

Источники: `ИСТОЧНИКИ.md`, `РЕГЛАМЕНТЫ.md`.

Они используются только как checklist/reference после проверки актуальности. Юрисдикция, broker entity, legal instrument, algo permission и tax treatment требуют свежих authoritative sources при S08/M5; старые записи не являются применимым правом автоматически.

### Open questions OQ-001…009

Предварительный remap:

| Old OQ | v2 disposition |
|---|---|
| `OQ-001` currency/experiment capital | Defer to Program Capital Policy / S08+; не блокирует safe research |
| `OQ-002` max loss/DD/duration | Defer to Program/Strategy Risk Mandate before real exposure |
| `OQ-003` share of total capital | Defer to Program Capital Policy / portfolio governance |
| `OQ-004` jurisdiction/tax residence | Defer to Live Environment/legal review before broker/live decision |
| `OQ-005` legal instrument | Resolve when concrete Strategy Candidate reaches live environment selection |
| `OQ-006` broker/entity/account | Resolve in M5/S08, not during M0/M1 research |
| `OQ-007` execution platform | Split: research stack addressed in M2; live execution platform decided later in M5 |
| `OQ-008` instrument/horizon/hypothesis | Resolve through Reference Strategy #1 selection and Research Funnel, not as program-wide prerequisite |
| `OQ-009` tick/data source/history | Resolve per hypothesis/Data Feasibility and Dataset Manifest; not universal program prerequisite |

`ATS2-M0-011` must convert these dispositions into `legacy/v1/CARRYOVER.md` and, where a concrete future task is not already represented in v2 backlog/WBS, add one without inventing values.

## 5. Objects explicitly not migrated into legacy namespace

The following remain current top-level infrastructure and are **not** part of this legacy move:

- `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` — already migrated to canonical v2 state;
- `README.md`, `00_НАЧАТЬ_ЗДЕСЬ.md`, `AGENTS.md`, `AI_HANDOFF.md`, `01_СТАТУС_ПРОЕКТА.md`, `02_СЛЕДУЮЩИЙ_ШАГ.md` — current entrypoints;
- `data/`, `experiments/`, `reports/`, `src/`, `tests/`, `tools/` — retained top-level by Repository Structure v2 and reviewed/evolved in place.

Any stale v1 wording in retained top-level infrastructure is handled by `ATS2-M0-012 Final link/validator sweep`, not by archiving the whole directory.

## 6. Definition of Done ATS2-M0-010

Task is complete when:

1. every designated v1 artifact has exactly one classification and target path;
2. review-needed artifacts have explicit carryover intent;
3. no legacy file is promoted automatically to current v2;
4. open questions are remapped to correct v2 stages without inventing answers;
5. physical migration can proceed deterministically from this index.
