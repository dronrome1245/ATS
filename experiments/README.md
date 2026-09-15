# Experiments

## Назначение

`experiments/` содержит formal registered experiments ATS v2 и единый индекс их lifecycle.

Exploratory Cheap Prototype artifacts живут в Research Factory и не получают `EXP-...` задним числом.

Canonical registration methodology:

`governance/methodology/EXPERIMENT_REGISTRATION.md`

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

Manifest связывает применимое:

- Experiment ID;
- Hypothesis ID;
- Candidate / Strategy / Strategy Version при наличии;
- code revision и implementation reference;
- dataset/source snapshot и period;
- parameters/configuration;
- random seed или `NOT_APPLICABLE`;
- cost/execution assumptions;
- predefined question;
- primary/secondary metrics;
- predefined decision rule;
- research stage и evidence class `REGISTERED_EXPERIMENT`.

Не существует обязательного универсального initial deposit, leverage, capital allocation или risk limit для research Experiment. Такие inputs фиксируются только когда они реально относятся к зарегистрированному вопросу и соответствующей lifecycle stage.

## Именование

Формат:

`EXP-YYYYMMDD-nnn`

ID после выдачи не переиспользуется.

## Неизменяемость

После `REGISTERED` decision-relevant context не переписывается под увиденный result.

Material change question/data/code/config/cost/metrics/decision rule требует нового Experiment ID.

Administrative non-semantic corrections допускаются только как явно записанные amendments.

Отрицательные, failed, cancelled и superseded experiments сохраняются.

# Experiment Registry

## Роль Registry

`experiments/REGISTRY.csv` — единственный program-wide searchable index formal Experiment identities и lifecycle summaries.

Registry **не является** вторым source of truth для experiment context. Полный контекст остаётся в canonical package:

`manifest.yaml → result.json → conclusion.md`.

Registry нужен, чтобы быстро найти Experiment по ID, lifecycle/status, stage, evidence class, lineage, outcome или decision и перейти к canonical package.

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
9. `supersedes_experiment_id` / `superseded_by_experiment_id` связывают replacement lineage без удаления старого ID.
10. Registry update и canonical package должны оставаться согласованными; при конфликте package/history имеет приоритет, а Registry исправляется как индекс.

## Registry schema

Столбцы `REGISTRY.csv`:

| Column | Назначение |
|---|---|
| `experiment_id` | Stable `EXP-YYYYMMDD-nnn` |
| `status` | `DRAFT / REGISTERED / RUNNING / COMPLETED / CANCELLED / SUPERSEDED` |
| `research_stage` | Research/validation/independent/stress/execution stage из manifest |
| `evidence_class` | Обычно `REGISTERED_EXPERIMENT`; точный class из registered context |
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

Canonical CLI examples:

```bash
python tools/search_experiments.py --status COMPLETED
python tools/search_experiments.py --stage VALIDATION
python tools/search_experiments.py --evidence-class REGISTERED_EXPERIMENT
python tools/search_experiments.py --decision FAIL
python tools/search_experiments.py --contains superseded
python tools/search_experiments.py --json
```

Available exact filters:

- `--id`;
- `--status`;
- `--stage`;
- `--evidence-class`;
- `--idea`;
- `--hypothesis`;
- `--candidate`;
- `--strategy`;
- `--decision`;
- `--outcome`.

`--contains` performs case-insensitive substring search over all columns.

## Initial state

M1-008 creates the Registry with its canonical header but **zero fictitious experiment rows**.

The first data row appears only when ATS registers or otherwise persistently allocates its first real `EXP-...` object.

This preserves the distinction between methodology infrastructure and actual evidence.
