# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- Real trading, demo, allocation and scaling remain disallowed.

## Last implemented work package

`ATS2-M2-009 — Manifest-driven experiment runner`.

Primary artifact:

`src/ats/runner/experiment.py`

Implemented boundary:

- reads a UTF-8 YAML Experiment manifest with `yaml.safe_load`;
- requires `REGISTERED` + `REGISTERED_EXPERIMENT` before execution;
- hashes exact registered manifest bytes and never rewrites preregistration;
- builds `ResearchRunContext` from registered parameters/configuration/random seed;
- validates actual code revision, implementation reference and environment ID against registration;
- validates Dataset ID and source snapshot against the Dataset Manifest;
- parses explicit registered cost components into `CostModelConfig`;
- requires runtime cost components when costs are registered and rejects them when cost model is `NOT_APPLICABLE`;
- orchestrates existing loader → replay → costs → standard analytics boundaries;
- blocks registered metric names that the standard analytics output cannot supply;
- requires explicit timezone-aware completion time instead of reading wall clock;
- produces canonical JSON-compatible `ExperimentRunResult`, including registered manifest SHA-256, dataset version/hash, metrics, costs, risk metrics and diagnostics;
- does not dynamically import/execute implementation paths from manifest text;
- does not evaluate the human/stage decision rule automatically; `machine_outcome` remains null in the generic runner.

Tests:

`tests/test_experiment_runner.py`

Runner tests create transient manifests under pytest temporary directories. No fictitious Experiment package or Registry row is committed, and the software fixture is not research evidence.

## M2-009 closure check

Windows OWNER workflow:

`ATS_TASK_CHECK.bat`

Current `tools/current_task_check.py` is configured for:

`ATS2-M2-009 — Manifest-driven experiment runner`

It runs:

1. `tests/test_experiment_runner.py`;
2. repository validator;
3. full ATS Local CI.

Shareable report:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

Reusable Local CI failure lessons:

`governance/program/LOCAL_CI_TROUBLESHOOTING.md`

M2-009 is finally closed only after PASS on the exact final HEAD.

## Current ready task after M2-009 PASS

`ATS2-M2-010 — Research platform tests`

Canonical next artifact:

`tests/test_research_platform.py`

Goal: harden the full deterministic software chain with an end-to-end regression/acceptance fixture before M2 Exit.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/LOCAL_CI_TROUBLESHOOTING.md` when diagnosing Local CI.
6. `governance/methodology/EXPERIMENT_REGISTRATION.md`.
7. `governance/methodology/templates/experiment/manifest.yaml`.
8. `governance/methodology/templates/experiment/result.json`.
9. `src/ats/data/loader.py`.
10. `src/ats/strategy/interface.py`.
11. `src/ats/replay/engine.py`.
12. `src/ats/costs/interface.py`.
13. `src/ats/analytics/standard.py`.
14. `src/ats/runner/experiment.py`.
15. `tests/test_experiment_runner.py`.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last implemented task: `ATS2-M2-009`.
- Closure checker: `ATS2-M2-009`.
- Next task after PASS: `ATS2-M2-010`.
- Next artifact: `tests/test_research_platform.py`.
- Reference Strategy #1 selection allowed now? — no.
- Pipeline counts remain zero? — yes.
