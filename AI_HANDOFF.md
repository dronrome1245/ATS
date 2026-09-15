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

`ATS2-M1-005 — Economic Pre-Screen` — `DONE`.

Artifacts:

- `governance/methodology/ECONOMIC_PRE_SCREEN.md`;
- `governance/methodology/templates/ECONOMIC_PRE_SCREEN_TEMPLATE.md`.

Economic Pre-Screen is the R4 research-budget gate. It assesses E1–E9: magnitude, preliminary net economics/cost sensitivity, opportunity diversity, capital use, risk/path/concentration, capacity, operational burden, evidence/search weakness and economic margin of safety.

Decision model:

`ADVANCE_TO_CANDIDATE_REVIEW / RETURN_TO_RESEARCH / PARK / REJECT`.

There is no universal return target, minimum trade count or capital threshold. A positive Pre-Screen does not create a Candidate and is not validation evidence.

## 3. Текущая ready task

`ATS2-M1-006 — Candidate promotion process`

Canonical next artifact:

`governance/methodology/CANDIDATE_PROMOTION_PROCESS.md`

Goal: formalize how a successful Research Funnel becomes a Strategy Candidate only through an explicit `PROMOTE / PARK / REJECT` decision.

## 4. Что должно быть определено в M1-006

- required R0–R4 artifacts;
- entry condition `ADVANCE_TO_CANDIDATE_REVIEW`;
- stable Candidate identity and lineage;
- preservation of exploratory/evidence limitations;
- known risks/failure modes and unresolved questions;
- proposed research scope through S05;
- `PROMOTE / PARK / REJECT` decision model;
- Candidate creation only on `PROMOTE`;
- relationship to future Strategy ID / S01;
- alignment of `CANDIDATE_TEMPLATE.md`;
- structural test without fictitious strategy content.

## 5. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/methodology/IDEA_INTAKE_PROCESS.md`.
6. `governance/methodology/HYPOTHESIS_MODEL.md`.
7. `governance/methodology/DATA_FEASIBILITY_REVIEW.md`.
8. `governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md`.
9. `governance/methodology/ECONOMIC_PRE_SCREEN.md`.
10. `governance/methodology/templates/CANDIDATE_TEMPLATE.md`.

## 6. Boundaries

Candidate promotion grants permission for deeper research only. It does not establish validated edge, approve live trading or allocate capital. Do not choose Reference Strategy #1, broker, jurisdiction, live platform, capital allocation or risk limits in M1-006.

## 7. Completion protocol

Material program task is complete only after deliverable, backlog, canonical state, human status, next-step, AI handoff and validator/entrypoints where relevant are synchronized.

## 8. Проверка восстановления контекста

- Current phase? — `M1_RESEARCH_METHODOLOGY`.
- Last completed? — `ATS2-M1-005`, `governance/methodology/ECONOMIC_PRE_SCREEN.md`.
- Next task? — `ATS2-M1-006`.
- Next artifact? — `governance/methodology/CANDIDATE_PROMOTION_PROCESS.md`.
- Candidates created by methodology test? — `0`.
- Does positive Pre-Screen prove profitability? — no.
