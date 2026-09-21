# Experiments

## Назначение

`experiments/` содержит formal registered experiments ATS v2 и единый индекс их lifecycle.

Exploratory Cheap Prototype artifacts живут в Research Factory и не получают `EXP-...` задним числом.

Canonical registration methodology:

`governance/methodology/EXPERIMENT_REGISTRATION.md`

Canonical evidence taxonomy:

`governance/methodology/EVIDENCE_TAXONOMY.md`

Canonical templates:

`governance/methodology/templates/experiment/`

Canonical searchable registry:

`experiments/REGISTRY.csv`

Search CLI:

`tools/search_experiments.py`

## Canonical package

Каждый formal Experiment хранится в:

`experiments/EXP-YYYYMMDD-nnn/`

Минимальный состав:

- `manifest.yaml` — preregistered context до result observation;
- `result.json` — observed machine-readable result;
- `conclusion.md` — evaluation against the registered question/decision rule;
- optional `artifacts/` — supporting outputs согласно Git/data policy.

## Registration boundary

Formal experiment может считаться preregistered только если `manifest.yaml` со статусом `REGISTERED` зафиксирован в Git до наблюдения соответствующего результата.

Manifest связывает применимое: Experiment/Hypothesis lineage, code/implementation, dataset/source snapshot, parameters/configuration, randomness, cost/execution assumptions, predefined question, primary/secondary metrics, decision rule, research stage и immutable source class `REGISTERED_EXPERIMENT`.

`evidence_class` в Registry отражает этот source/provenance class. Отдельное поле `qualified_evidence_class` отражает strongest reviewed semantic class по `EVIDENCE_TAXONOMY.md`, например `VALIDATION_EVIDENCE` или `INDEPENDENT_EXAMINATION_EVIDENCE`, только после выполнения соответствующих prerequisites.

`research_stage = VALIDATION` сам по себе не делает Experiment validation evidence.

Не существует обязательного универсального initial deposit, leverage, capital allocation или risk limit для research Experiment. Такие inputs фиксируются только когда они реально относятся к зарегистрированному вопросу и соответствующей lifecycle stage.

## Именование

Формат: `EXP-YYYYMMDD-nnn`.

ID после выдачи не переиспользуется.

## Неизменяемость

После `REGISTERED` decision-relevant context не переписывается под увиденный result.

Material change question/data/code/config/cost/metrics/decision rule требует нового Experiment ID. Administrative non-semantic corrections допускаются только как явно записанные amendments.

Отрицательные, failed, cancelled и superseded experiments сохраняются.

# Experiment Registry

## Роль Registry

`experiments/REGISTRY.csv` — единственный program-wide searchable index formal Experiment identities и lifecycle summaries.

Registry **не является** вторым source of truth для experiment context. Полный контекст остаётся в canonical package:

`manifest.yaml → result.json → conclusion.md`.

Registry нужен, чтобы быстро найти Experiment по ID, lifecycle/status, stage, source evidence class, qualified evidence class, lineage, outcome или decision и перейти к canonical package.

## Одна строка на один Experiment ID

Правила:

1. Один `experiment_id` имеет ровно одну строку Registry.
2. Строка создаётся, когда реальный Experiment ID впервые зафиксирован в репозитории.
3. Строка никогда не удаляется из-за отрицательного, failed, cancelled или superseded результата.
4. `DRAFT` может присутствовать, если ID уже выделен и сохранён; такой row не означает preregistration.
5. При `REGISTERED` заполняются `registered_at` и `registration_revision`.
6. `registration_revision` указывает на Git revision/commit, где registered manifest уже существовал до observation соответствующего result.
7. При `RUNNING`, `COMPLETED`, `CANCELLED` или `SUPERSEDED` обновляется summary row, но исторический registered manifest не переписывается.
8. `machine_outcome` и `decision` заполняются только когда соответствующие result/conclusion существуют.
9. `qualified_evidence_class` остаётся пустым или базовым, пока отдельный review не подтвердил prerequisites более сильного semantic class.
10. `supersedes_experiment_id` / `superseded_by_experiment_id` связывают replacement lineage без удаления старого ID.
11. Registry update и canonical package должны оставаться согласованными; при конфликте package/history имеет приоритет, а Registry исправляется как индекс.

## Registry schema

| Column | Назначение |
|---|---|
| `experiment_id` | Stable `EXP-YYYYMMDD-nnn` |
| `status` | `DRAFT / REGISTERED / RUNNING / COMPLETED / CANCELLED / SUPERSEDED` |
| `research_stage` | Research/validation/independent/stress/execution stage из manifest |
| `evidence_class` | Immutable source/provenance class, normally `REGISTERED_EXPERIMENT` |
| `qualified_evidence_class` | Strongest reviewed semantic claim class from `EVIDENCE_TAXONOMY.md`, if assigned |
| `idea_id` | Parent Idea при наличии |
| `hypothesis_id` | Primary `HYP-...` |
| `candidate_id` | `CAND-...` при наличии |
| `strategy_id` | `STRAT-...` при наличии |
| `strategy_version` | Strategy Version при наличии |
| `package_path` | Canonical `experiments/EXP-.../` |
| `manifest_path` | Canonical registered manifest path |
| `registration_revision` | Git revision anchoring preregistration |
| `registered_at` | Registration timestamp from manifest |
| `completed_at` | Completion timestamp when known |
| `machine_outcome` | Machine-readable result outcome when available |
| `decision` | Human/stage decision from conclusion when available |
| `supersedes_experiment_id` | Older registration replaced by this ID |
| `superseded_by_experiment_id` | Replacement ID when this registration is superseded |

Blank cell means that value is not yet known or not populated at the current lifecycle point. It must not be interpreted as permission to invent a value.

## Search

The registry remains plain CSV so it can be searched by Git, spreadsheets, scripts and standard text tooling.

Examples:

```bash
python tools/search_experiments.py --status COMPLETED
python tools/search_experiments.py --stage VALIDATION
python tools/search_experiments.py --evidence-class REGISTERED_EXPERIMENT
python tools/search_experiments.py --qualified-evidence-class VALIDATION_EVIDENCE
python tools/search_experiments.py --decision FAIL
python tools/search_experiments.py --contains superseded
python tools/search_experiments.py --json
```

Available exact filters:

- `--id`;
- `--status`;
- `--stage`;
- `--evidence-class`;
- `--qualified-evidence-class`;
- `--idea`;
- `--hypothesis`;
- `--candidate`;
- `--strategy`;
- `--decision`;
- `--outcome`.

`--contains` performs case-insensitive substring search over all columns.

## Initial state

M1-008 created the Registry with its canonical header but zero fictitious experiment rows. M1-009 extends the empty schema with `qualified_evidence_class` before real Experiment rows exist, so no evidence migration is required.

The first data row appears only when ATS registers or persistently allocates its first real `EXP-...` object.


## M2 manifest-driven runner integration

`ats.runner.experiment` provides the M2 software boundary that consumes a frozen `REGISTERED` manifest and composes the existing Dataset Manifest loader, deterministic replay, explicit costs and standard analytics.

The runner does not rewrite preregistration and does not dynamically import implementation paths from manifest text. Actual code revision, implementation reference, environment ID, Dataset ID and source snapshot are checked against the registered context. The exact manifest bytes are SHA-256 bound into the machine-readable result context.

Platform tests use transient manifests only. A software fixture is not added to `experiments/REGISTRY.csv` and does not become `REGISTERED_EXPERIMENT` evidence merely because the runner contract is exercised.
