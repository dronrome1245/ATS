# M0 Final Link & Validator Sweep

**Task:** `ATS2-M0-012`  
**Milestone:** `M0_PROGRAM_REBASELINE`  
**Status:** PASS  
**Date:** 15 September 2026

## 1. Purpose

This sweep verifies that the ATS v2 repository no longer depends operationally on pre-migration v1 paths and that the repository validator permanently enforces the current canonical structure.

## 2. Scope checked

The sweep covered:

- root AI/human entrypoints;
- canonical state and Program Backlog;
- `governance/program/` and `governance/methodology/`;
- the archived `legacy/v1/` namespace;
- removed ATS v1 source paths;
- local Markdown links in current, non-legacy documentation;
- canonical file paths declared in `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
- synchronization of `next_artifact` and `next_task_id` across state, handoff and next-step documents.

## 3. Findings

The first hardened validator run correctly failed and found two stale AI entrypoints:

1. `.github/copilot-instructions.md` still referenced the removed `00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml` path.
2. `CLAUDE.md` still referenced the same removed transitional state path.

No stale references were found in the main current program entrypoints or canonical governance after those two pointers were corrected.

## 4. Remediation

Both AI pointer files were updated to use:

- `AI_HANDOFF.md`;
- `AGENTS.md`;
- `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
- `02_СЛЕДУЮЩИЙ_ШАГ.md`;
- `governance/backlog/PROGRAM_BACKLOG_V2.md`;
- current governance under `governance/program/` and `governance/methodology/`.

Legacy G01–G13 content is explicitly treated as historical/reference material only.

## 5. Validator hardening

`tools/validate_repo.py` now additionally:

- checks that all canonical paths declared by state actually exist;
- checks that `last_completed_artifact` exists;
- rejects reappearance of migrated current-v2 and ATS v1 source paths;
- rejects stale pre-migration v1 namespaces in operational entrypoint files;
- scans current non-legacy Markdown for broken local links;
- keeps existing state/backlog/handoff synchronization and safety invariants.

## 6. Evidence

- Hardened sweep run `103` failed as expected and exposed the two stale AI pointers.
- After remediation, validation run `105` completed successfully on `main`.

The failure was therefore treated as useful validation evidence rather than bypassed by weakening the checker.

## 7. Result

`ATS2-M0-012` is complete.

Current repository structure is consistent with ATS v2 governance, legacy content is isolated under `legacy/v1/`, operational entrypoints use current canonical paths, and the validator enforces these invariants.

## 8. Next action

Proceed to:

`ATS2-M0-013 — M0 Exit Review`

Deliverable:

`governance/program/M0_EXIT_REVIEW.md`

The Exit Review must decide whether M0 can be formally closed and M1 Research Factory can begin. It must not select a trading strategy, broker, live capital allocation or risk limits as part of M0 closure.
