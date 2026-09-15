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

`ATS2-M1-006 — Candidate promotion process` — `DONE`.

Artifacts:

- `governance/methodology/CANDIDATE_PROMOTION_PROCESS.md`;
- `governance/methodology/templates/CANDIDATE_PROMOTION_REVIEW_TEMPLATE.md`;
- `governance/methodology/templates/CANDIDATE_TEMPLATE.md`;
- `governance/methodology/templates/CANDIDATE_EVIDENCE_INDEX_TEMPLATE.md`.

Candidate Promotion review starts only after Economic Pre-Screen `ADVANCE_TO_CANDIDATE_REVIEW` and issues exactly one completed decision:

`PROMOTE / PARK / REJECT`.

Only `PROMOTE` allocates a stable `CAND-xxxx` and creates `research/candidates/CAND-xxxx/CANDIDATE.md` + `EVIDENCE_INDEX.md` with status `READY_FOR_S01`.

`PARK` and `REJECT` create no Candidate ID. `Strategy ID` remains `null` until formal S01 Candidate Admission. Candidate promotion is permission for deeper research only; it is not validated edge or live permission.

Structural testing created no fictitious Candidate, so `strategy_pipeline.candidates_active = 0`.

## 3. Текущая ready task

`ATS2-M1-007 — Experiment registration schema`

Canonical next artifact:

`governance/methodology/EXPERIMENT_REGISTRATION.md`

Goal: define how a formal `EXP-YYYYMMDD-nnn` is registered before its result is observed so it can later qualify as registered evidence.

## 4. Что должно быть определено в M1-007

- stable Experiment ID;
- Hypothesis linkage and Candidate/Strategy Version linkage when available;
- code revision / implementation reference;
- dataset identity/source snapshot/period;
- parameters/configuration;
- cost/execution assumptions;
- predefined research question;
- primary and secondary metrics;
- predefined decision rule;
- research stage/evidence class;
- random seed or explicit `NOT_APPLICABLE`;
- immutable preregistration boundary;
- amendment rules before result observation;
- prohibition on post-result rewrite as preregistration;
- manifest → result → conclusion relationship;
- structural schema test without fictitious result.

## 5. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/methodology/CANDIDATE_PROMOTION_PROCESS.md` for current upstream boundary.
6. `governance/methodology/RESEARCH_METHODOLOGY_V1.md`.
7. `governance/methodology/templates/experiment/manifest.yaml`.
8. `governance/methodology/templates/experiment/result.json`.
9. `governance/methodology/templates/experiment/conclusion.md`.

## 6. Boundaries

Cheap Prototype remains `EXPLORATORY_PROTOTYPE` and cannot be upgraded retroactively into a pre-registered Experiment. Experiment methodology does not choose Reference Strategy #1, broker, jurisdiction, live platform, capital allocation or risk limits.

## 7. Completion protocol

Material program task is complete only after deliverable, backlog, canonical state, human status, next-step, AI handoff and validator/entrypoints where relevant are synchronized.

## 8. Проверка восстановления контекста

- Current phase? — `M1_RESEARCH_METHODOLOGY`.
- Last completed? — `ATS2-M1-006`, `governance/methodology/CANDIDATE_PROMOTION_PROCESS.md`.
- Next task? — `ATS2-M1-007`.
- Next artifact? — `governance/methodology/EXPERIMENT_REGISTRATION.md`.
- Candidates created by methodology test? — `0`.
- Does `PROMOTE` mean validated/live? — no.
- Can an old prototype be assigned `EXP-...` after seeing the result and called preregistered? — no.
