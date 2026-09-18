# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- Real trading, demo, allocation and scaling remain disallowed.

## Last completed

`ATS2-M2-003 — Dataset manifest support` — `DONE`.

Canonical specification:

`governance/program/DATASET_MANIFEST_SPEC.md`

Materialized Dataset Manifest boundary:

- template: `data/manifests/DATASET_TEMPLATE.yaml`;
- typed immutable model: `src/ats/schemas/dataset_manifest.py`;
- safe YAML loader: `load_dataset_manifest`;
- tests: `tests/test_dataset_manifest.py`;
- pytest source path: `src/`.

Contract covers stable dataset ID/version, source/snapshot, storage/schema reference, timezone-aware coverage, event-time versus information-availability semantics, deterministic ordering/tie-break, explicit quality policy, transformation lineage, integrity metadata and known limitations.

Material source/coverage/schema/time/order/quality/transformation changes require a new `dataset_version`.

The canonical template is synthetic non-market metadata only. It is not an Idea, Hypothesis, Experiment, Strategy or trading evidence.

## Environment / quality gate

Supported hosts:

- Windows x86_64 — primary local host;
- Linux x86_64 — supported secondary host.

Runtime:

- CPython `3.13.15`;
- uv `0.12.13`;
- frozen `uv.lock`.

Canonical Windows OWNER workflow:

`ATS_TASK_CHECK.bat`

The BAT is stable. It performs fast-forward pull and frozen environment sync, then executes task-specific `tools/current_task_check.py` plus the full Local CI Gate. Shareable report: `reports/local_ci/CURRENT_TASK_REPORT.txt`.

For the pending M2-003 closure check, `tools/current_task_check.py` validates Dataset Manifest tests + repository validator + full Local CI. After PASS it should be updated for M2-004 without changing the BAT. GitHub Actions is not used as a completion gate.

## Current ready task

`ATS2-M2-004 — Base data loader`

Canonical next artifact:

`src/ats/data/loader.py`

Goal: consume a validated Dataset Manifest and load the reference-format synthetic records deterministically with explicit timestamp/order/tie-break and declared quality-policy handling.

## M2-004 boundary

M2-004 should implement only the data loading layer needed by the Reference Consumer Profile:

- load a supported reference format;
- preserve/normalize timestamp semantics from the Manifest;
- deterministic ordering and tie-break;
- explicit duplicate/missing/malformed/out-of-order handling according to Manifest policy;
- runtime integrity verification where applicable;
- deterministic synthetic fixtures/tests.

Do not implement Strategy API, replay, cost model, analytics, broker/live integration or Reference Strategy #1 in M2-004.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/DATASET_MANIFEST_SPEC.md`.
6. `src/ats/schemas/dataset_manifest.py`.
7. `data/manifests/DATASET_TEMPLATE.yaml`.
8. `governance/program/REFERENCE_CONSUMER_PROFILE.md`.
9. `governance/program/RESEARCH_ENVIRONMENT_SPEC.md`.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last completed: `ATS2-M2-003`.
- Next task: `ATS2-M2-004`.
- Next artifact: `src/ats/data/loader.py`.
- Reference Strategy #1 selection allowed now? — no.
- Pipeline counts remain zero? — yes.
