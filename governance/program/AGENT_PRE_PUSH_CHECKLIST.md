# ATS Agent Pre-Push Checklist

**Status:** ACTIVE  
**Scope:** every agent/tool that writes ATS repository content, especially through remote repository APIs that bypass local Git hooks.

## 1. Core rule

Before any material remote repository write, the agent must evaluate this checklist against the exact proposed content.

A task is not complete because a remote commit exists. Completion still requires `ATS_TASK_CHECK.bat = PASS` on the exact HEAD being closed.

## 2. Context and task identity

Before editing:

1. read `AI_HANDOFF.md`, `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`, `02_СЛЕДУЮЩИЙ_ШАГ.md` and `governance/backlog/PROGRAM_BACKLOG_V2.md`;
2. stop substantive work if those files disagree;
3. capture the exact current `next_task_id`, `last_completed_artifact` and `next_artifact` from canonical state;
4. do not advance to the next task until the current exact HEAD has a launcher PASS.

## 3. Change-scope check

Before writing:

1. enumerate every file that will change;
2. avoid unrelated cleanup or refactoring during a task-closure fix;
3. if a failure report exists, fix the first confirmed failing stage and the narrowest supported cause first;
4. do not modify research/runtime logic for network, environment, formatting or handoff-only failures.

## 4. Remote Python rule

Any Python content written through a remote repository API bypasses local hooks.

If the exact project-pinned Ruff version has not run on the exact proposed Python content, its status is:

`FORMAT_UNVERIFIED_UNTIL_PINNED_RUFF`

Rules:

1. never call such content Ruff-verified;
2. prefer not to change Python during governance-only fixes;
3. preserve previously Ruff-confirmed layouts when only constants/strings/task identity change;
4. for `tools/current_task_check.py`, change task constants/strings and required artifact paths without reflowing a previously confirmed template unless logic truly changes;
5. when OWNER Local CI provides an exact Ruff diff, **Exact Ruff diff is authoritative**; apply it literally instead of inventing an equivalent layout;
6. lint success, syntax compilation, line-length inspection and visual inspection do not equal Ruff-format verification.

## 5. Validator marker audit

If `tools/validate_repo.py` changes:

1. verify every new or modified `CONTENT_MARKERS` entry against the exact target-file text;
2. do not use a marker that depends unnecessarily on Markdown emphasis, capitalization or punctuation;
3. compile the validator after editing.

If any existing validator-targeted file changes, audit **all existing markers for that target file**, even when validator code itself did not change.

## 6. Canonical state reconciliation

Before commit, mechanically verify exact-string identity:

1. `last_completed_artifact` appears in `AI_HANDOFF.md`;
2. `next_artifact` appears in both `AI_HANDOFF.md` and `02_СЛЕДУЮЩИЙ_ШАГ.md`;
3. `next_task_id` appears in both `AI_HANDOFF.md` and `02_СЛЕДУЮЩИЙ_ШАГ.md`;
4. Program Backlog status agrees with the canonical current/next task;
5. human-readable status/README/start guide do not claim a later task than canonical state.

Narrative equivalence is not sufficient for stable IDs and paths.

## 7. Pre-push checks

Before moving the remote branch:

1. reject placeholder tokens prohibited by the repository validator in current operational content;
2. check changed Python for syntax errors;
3. audit local Markdown references introduced or changed by the patch;
4. if an environment with project-pinned tools is available, run the fast gate on the exact proposed content before push;
5. if pinned Ruff is unavailable, preserve `FORMAT_UNVERIFIED_UNTIL_PINNED_RUFF` status and do not claim preflight PASS.

## 8. Required pre-launch declaration

Before asking OWNER to run `ATS_TASK_CHECK.bat`, state:

- exact commit SHA;
- current task ID;
- whether Python changed;
- Ruff status: `VERIFIED_BY_PINNED_RUFF` or `FORMAT_UNVERIFIED_UNTIL_PINNED_RUFF`;
- canonical state reconciliation: `PASS` or the exact mismatch;
- validator marker audit: `PASS`, `N/A`, or the exact unresolved issue;
- task completion status: always `PENDING_OWNER_LAUNCHER` until exact-head PASS.

## 9. Failure handling

When the launcher returns FAIL:

1. identify the **First failing stage**;
2. classify it under the existing `LCI-###` cause where applicable;
3. fix only the narrowest confirmed cause;
4. update durable failure knowledge when the recurrence changes the preventive rule or count;
5. rerun the launcher on the new exact HEAD;
6. do not declare completion without `ATS TASK LAUNCHER: PASS`.

## 10. Completion boundary

No material task may be marked closed and no next task may become active until all are true:

1. deliverable/state/backlog/handoff are synchronized;
2. exact HEAD is known;
3. OWNER launcher returns `ATS TASK LAUNCHER: PASS`;
4. the PASS report names that exact HEAD;
5. only then may canonical state advance to the next task.
