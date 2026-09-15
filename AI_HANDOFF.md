# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Program model: ATS v2 / Strategy Factory.
- Current phase: `M1_RESEARCH_METHODOLOGY` / Research Factory.
- Status: `IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0 Program Rebaseline: `COMPLETED / PASS`.
- G01–G13: `legacy/v1/`, history/reference only.
- Real trading, demo, allocation and scaling remain disallowed current actions.

## 2. Последний завершённый шаг

`ATS2-M1-008 — Experiment registry` — `DONE`.

Artifacts/capabilities:

- `experiments/REGISTRY.csv` — canonical searchable Experiment index;
- `experiments/README.md` — registry schema/lifecycle/integrity rules;
- `tools/search_experiments.py` — canonical lightweight search CLI.

Registry rules:

- one row per real `EXP-YYYYMMDD-nnn`;
- rows are never deleted because result is negative, failed, cancelled or superseded;
- indexed fields include status, research stage, evidence class, Idea/Hypothesis/Candidate/Strategy lineage, package/manifest path, registration revision/timestamps, outcome/decision and supersede lineage;
- Registry is an index only; `manifest.yaml → result.json → conclusion.md` remains authoritative;
- initial registry has header only and zero fictitious rows.

Current `strategy_pipeline.experiments_registered = 0`.

## 3. Текущая ready task

`ATS2-M1-009 — Evidence taxonomy operationalization`

Canonical next artifact:

`governance/methodology/EVIDENCE_TAXONOMY.md`

Goal: define operational evidence classes and the exact claim strength / forbidden claims associated with each class.

## 4. Что должно быть определено в M1-009

- exploratory observation/prototype evidence;
- registered experiment evidence;
- validation evidence;
- independent examination evidence;
- stress evidence;
- demo/shadow evidence;
- minimal/live evidence;
- allowed claims per class;
- prohibited claims per class;
- prerequisites for class promotion;
- no promotion based only on attractive result;
- negative evidence retention;
- relationship to Experiment Registry and Candidate/Strategy evidence indexes;
- structural taxonomy test without fictitious market evidence.

## 5. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/methodology/RESEARCH_METHODOLOGY_V1.md`.
6. `governance/methodology/EXPERIMENT_REGISTRATION.md`.
7. `experiments/README.md` and `experiments/REGISTRY.csv`.
8. relevant Candidate/Strategy evidence index templates.

## 6. Boundaries

Registry discoverability does not upgrade evidence quality. `REGISTERED_EXPERIMENT` means preregistered context, not validation. Demo/shadow is not profitability proof; historical backtest is not live-execution proof. Do not choose Reference Strategy #1, broker, jurisdiction, live platform, capital allocation or risk limits in M1-009.

## 7. Completion protocol

Material program task is complete only after deliverable, backlog, canonical state, human status, next-step, AI handoff and validator/entrypoints where relevant are synchronized.

## 8. Проверка восстановления контекста

- Current phase? — `M1_RESEARCH_METHODOLOGY`.
- Last completed? — `ATS2-M1-008`, `experiments/REGISTRY.csv`.
- Next task? — `ATS2-M1-009`.
- Next artifact? — `governance/methodology/EVIDENCE_TAXONOMY.md`.
- Real Experiments currently registered? — `0`.
- Can Registry replace manifest/result/conclusion? — no.
- Does searchable mean evidence is stronger? — no.
