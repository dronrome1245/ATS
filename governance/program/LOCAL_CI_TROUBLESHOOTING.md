# ATS Local CI Troubleshooting & Lessons

**Status:** BASELINE  
**Scope:** reusable failure knowledge for `ATS_TASK_CHECK.bat` and the Local CI Gate  
**Canonical gate:** `governance/program/LOCAL_CI_GATE.md`

## 1. Purpose

This document is the durable repository memory for recurring or reusable Local CI failures.

Runtime files such as:

- `reports/local_ci/CURRENT_TASK_REPORT.txt`;
- `reports/local_ci/LATEST.json`;

remain local evidence and are intentionally ignored by Git. Raw machine reports are not copied into this file.

A failure is recorded here only after its class and root cause are understood well enough to produce a preventive rule.

## 2. Failure-handling rule

When `ATS_TASK_CHECK.bat` returns FAIL:

1. identify the first failing stage;
2. classify the failure before changing code;
3. do not modify source code for infrastructure/network failures;
4. fix the narrowest confirmed cause;
5. if the failure reveals a reusable lesson, add or update an entry in this document;
6. rerun the full launcher on the new exact HEAD;
7. do not declare the task closed until `ATS TASK LAUNCHER: PASS`.

Known failure classes:

- `SYNC_NETWORK` — repository synchronization/connectivity failed before code verification;
- `ENVIRONMENT` — frozen environment cannot be created or fingerprinted;
- `FORMAT` — formatter check fails while logic/tests may still pass;
- `LINT` — static lint rule fails;
- `TEST` — targeted or full pytest failure;
- `VALIDATOR` — repository/governance invariant failure;
- `DIRTY_TREE` — exact-commit verification is impossible because the worktree is modified;
- `UNKNOWN` — no code change until the failure is narrowed further.

## 3. Durable lesson format

Each reusable entry must include:

- **ID** — stable `LCI-###`;
- **First observed** — date and, when relevant, commit;
- **Class**;
- **Symptom**;
- **Root cause**;
- **Correct response**;
- **Preventive rule**;
- **Scope** — whether the rule applies to OWNER workflow, agents, or both.

Do not store secrets, credentials, private paths, raw full logs or machine-specific personal information here.

## 4. Known lessons

### LCI-001 — GitHub connectivity failure during pull

**First observed:** 2026-09-18  
**Class:** `SYNC_NETWORK`

**Symptom**

`ATS_TASK_CHECK.bat` stops at `git pull --ff-only` with an error such as:

`Failed to connect to github.com:443`

The task-specific tests, validator, Ruff and full Local CI have not run yet.

**Root cause**

The launcher cannot confirm/update the local clone because GitHub is temporarily unreachable from the OWNER machine or network path.

**Correct response**

Do not change ATS source code. Restore/wait for network access and rerun the same launcher. The failure is infrastructure-level unless a separate Git configuration/authentication problem is proven.

**Preventive rule**

Always distinguish a pre-verification synchronization failure from a code failure. A `SYNC_NETWORK` failure must never trigger speculative source changes.

**Scope:** OWNER workflow and agents.

### LCI-002 — Ruff format failure after direct remote Python edit

**First observed:** 2026-09-18 on `b3085c26342c52e6ae852962faefcaf347d43a2a`  
**Fixed by:** `fd09a08de2a234ac1249a9e44ee7e21f32f4a7cd`  
**Class:** `FORMAT`

**Symptom**

Targeted tests, full pytest, repository validator and Ruff lint pass, but `ruff format --check` reports that a maintained Python file would be reformatted.

Observed example: a multiline conditional expression in `tests/test_cost_interface.py` was logically correct but not in Ruff's canonical layout.

**Root cause**

A Python file was written directly through the remote repository path, so local Git hooks did not get a chance to run before the remote commit existed.

**Correct response**

Apply only the formatter-prescribed style change when no logic failure is present, keep it in a style-only commit when practical, then rerun the full launcher on the new exact HEAD.

**Preventive rule**

For agent-created or programmatic Python edits that bypass the repository hooks:

1. treat Ruff-compatible formatting as part of authoring, not as optional cleanup;
2. when an execution environment with the pinned Ruff version is available, run the formatter/check before presenting a candidate HEAD;
3. never infer that passing tests + lint means format also passes;
4. if Local CI supplies an exact formatter diff, apply that canonical layout rather than hand-inventing another equivalent layout.

**Scope:** agents and any tooling that writes directly to the remote repository.

## 5. Adding future lessons

Add a new entry only when all are true:

1. the failure class is known;
2. the root cause is supported by the report or reproduction;
3. the corrective action is known;
4. there is a concrete rule that can reduce recurrence or misdiagnosis.

If the same failure class repeats without a new lesson, update the existing entry only when the preventive rule itself improves.

## 6. Relationship to completion

This troubleshooting registry does not replace the Local CI Gate.

The completion evidence remains a fresh `ATS_TASK_CHECK.bat` PASS on the exact HEAD being closed. A documented lesson explains how to handle failures; it does not waive any gate.
