# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- M2: `COMPLETED / PASS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Real trading, demo, allocation and scaling remain disallowed.

## Last completed milestone

`M2_RESEARCH_PLATFORM_MVP`

Exit task:

`ATS2-M2-011 — M2 Exit`

Canonical review:

`governance/program/M2_EXIT_REVIEW.md`

Decision:

`PASS`

M2 established the minimum reusable research stack:

`Dataset Manifest → loader → Strategy/Research interface → deterministic replay → explicit costs → standard analytics/result → manifest-driven runner → automated acceptance/regression tests`

Accepted M2 implementation evidence includes exact commit `953eac0e88608d782a825d7039c1eb1bf14577c6`, 13 targeted M2-010 tests, 83 total tests, clean working tree, repository validator PASS, Ruff lint/format PASS, pytest PASS and environment fingerprint PASS.

Synthetic M2 fixtures created no formal Idea/Hypothesis/Candidate/Strategy/Experiment evidence. Experiment Registry remained empty.

## M2-011 closure check

Current `tools/current_task_check.py` is configured for:

`ATS2-M2-011 — M2 Exit`

It rechecks M2 acceptance tests, repository validator and the full Local CI on the exact transition commit.

Shareable report:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

## Current M3 task after M2-011 gate PASS

`ATS2-M3-001 — Select Reference Strategy #1`

Work package:

`WBS-3.1`

Canonical next artifact:

`governance/program/REFERENCE_STRATEGY_1_SELECTION.md`

No Reference Strategy is selected yet.

The selection decision should favor a simple strategy class with genuinely available data and a sufficiently clear execution model for the first vertical use of the M2 platform. Selection itself is not evidence of profitability or validation.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/program/M2_EXIT_REVIEW.md`.
5. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
6. `governance/program/PROGRAM_WBS_V2.md`.
7. `governance/methodology/IDEA_INTAKE_PROCESS.md`.
8. `governance/methodology/HYPOTHESIS_MODEL.md`.
9. `governance/methodology/DATA_FEASIBILITY_REVIEW.md`.
10. `governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md`.
11. `governance/methodology/ECONOMIC_PRE_SCREEN.md`.

## Recovery check

- Current milestone: `M3_REFERENCE_STRATEGY_1`.
- Last completed task: `ATS2-M2-011`.
- Closure checker: `ATS2-M2-011`.
- Current ready task after closure gate: `ATS2-M3-001`.
- Current WBS: `WBS-3.1`.
- Next artifact: `governance/program/REFERENCE_STRATEGY_1_SELECTION.md`.
- Reference Strategy selected? — no.
- Reference Strategy selection allowed in M3? — yes.
- Live/demo/allocation/scaling allowed? — no.
- Pipeline counts remain zero? — yes.
