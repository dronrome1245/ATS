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
**Repeat observed:** 2026-09-21 on `c8a0225acafba15d59dcd35d5bf3aceee716ced3` in `src/ats/runner/experiment.py`  
**Repeat observed:** 2026-09-21 on `cd348024bd907225ea15219786ef5ad54ebdea1d` in `src/ats/validation/sensitivity.py` and `tools/current_task_check.py` after a manual line-length preflight incorrectly implied formatting readiness  
**Repeat observed:** 2026-09-21 on `9f912b7b5e350d287ed76ce4bffe7a67722faf58` in `src/ats/validation/slicing.py` after remote authoring without pinned Ruff execution  
**Fixed first occurrence by:** `fd09a08de2a234ac1249a9e44ee7e21f32f4a7cd`  
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
2. when an execution environment with the pinned Ruff version is available, run the formatter/check on the exact changed file before presenting a candidate HEAD;
3. if pinned Ruff was not actually executed, do not describe formatting as preflight-passed; syntax inspection is not a substitute for `ruff format --check`;
4. never infer that passing tests + lint means format also passes;
5. if Local CI supplies an exact formatter diff, apply that canonical layout rather than hand-inventing another equivalent layout;
6. manual line-length checks, syntax compilation and visual style inspection are **not** Ruff-format preflight and must never be described as such;
7. before asking OWNER to run the launcher after remote Python edits, state formatting as either `VERIFIED_BY_PINNED_RUFF` or `NOT_YET_VERIFIED_BY_RUFF`; there is no intermediate "looks formatted" state.

**Escalation**

This failure class is now recurring at the technical-control threshold. Documentation alone is insufficient. `ATS_TASK_CHECK.bat` must run the fast Local CI gate before the full task check so format/lint/validator failures stop the workflow before the expensive full pytest stage.

**Scope:** agents and any tooling that writes directly to the remote repository.

### LCI-003 — uv missing from PATH on a new Windows host

**First observed:** 2026-09-19  
**Class:** `ENVIRONMENT`

**Symptom**

`ATS_TASK_CHECK.bat` stops before repository sync/environment sync with:

`ERROR: uv is not available on PATH.`

and returns launcher exit code `12`.

**Root cause**

The Windows host has not completed the ATS environment bootstrap, or `uv` is installed but its executable directory is not visible in the process `PATH`.

This is not a Strategy/replay/cost/analytics code failure. No pytest, validator, Ruff or environment fingerprint stage has run.

**Correct response**

Install the project-pinned `uv 0.12.13` using the official uv installer, open a new terminal/session so the updated PATH is visible, verify `uv --version`, install the pinned Python baseline, then rerun the launcher.

Canonical Windows bootstrap:

```powershell
$installer = Join-Path $env:TEMP "uv-0.12.13-install.ps1"
Invoke-WebRequest -UseBasicParsing "https://astral.sh/uv/0.12.13/install.ps1" -OutFile $installer
powershell -ExecutionPolicy ByPass -File $installer
```

The download-to-file form is the ATS-preferred Windows bootstrap because it avoids shell/pipeline parsing problems observed with nested `irm ... | iex` execution.

Then open a new PowerShell session and run:

```powershell
where.exe uv
uv --version
uv python install 3.13.15
uv sync --frozen
```

Expected uv version prefix:

`uv 0.12.13`

If `uv --version` still fails after installation, diagnose PATH visibility before changing ATS source code.

A later `uv python install 3.13.15` warning such as:

`Executable already exists ... python3.13.exe but is not managed by uv; use --force`

does not by itself mean the ATS project is blocked. uv refuses to overwrite an executable it does not manage unless `--force` is supplied. Do **not** use `--force` merely to silence this warning. First continue with `uv sync --frozen`; uv can use a compatible CPython 3.13.15 discovered on the host or a managed installation without replacing the unrelated launcher executable.

On a migrated/copied working directory, `uv sync --frozen` may also report:

`Ignoring existing virtual environment linked to non-existent Python interpreter`

This means the repository-local `.venv` points to an interpreter path that existed on the previous computer. The environment is disposable. Let `uv sync --frozen` recreate/synchronize it. If sync cannot recover it automatically, remove only the repository-local `.venv` and rerun `uv sync --frozen`; do not edit project code or `uv.lock`.

**Preventive rule**

A newly provisioned ATS host must complete the pinned tool bootstrap before the task launcher is expected to pass. Treat launcher exit code `12` as an environment/bootstrap failure and never as evidence of a code defect.

**Scope:** OWNER workflow and agents.

### LCI-004 — Repository validator marker drift from Markdown formatting

**First observed:** 2026-09-21 on `e4f397b4a985be314c75e4385d59030e77fcbfcd`  
**Repeat observed:** 2026-09-21 on `c8a0225acafba15d59dcd35d5bf3aceee716ced3` after a selective marker preflight missed three newly declared README markers  
**Repeat observed:** 2026-09-21 on `0c9823fe48c1e562d516ac311d956893afdec44f` after the M2→M3 transition changed `PROGRAM_WBS_V2.md` while an unchanged validator marker still expected the old M2 wording  
**Class:** `VALIDATOR`

**Symptom**

Targeted tests, full pytest, Ruff lint/format and environment fingerprint pass, but the repository validator reports a missing content marker for text that is visibly present in the target governance file with different capitalization or Markdown emphasis.

Observed example: the troubleshooting file contained `Do **not** use --force ...` while the validator expected the literal lower-case/plain-Markdown wording.

**Root cause**

The validator marker was coupled to presentation details instead of a stable semantic fragment. Markdown emphasis or capitalization changed the raw text while the required rule remained present.

**Correct response**

Do not change product/runtime logic. Fix the validator to search for a stable semantic phrase already present in the canonical document, then rerun the full launcher on the new exact HEAD.

**Preventive rule**

Repository content markers should validate durable invariants, identifiers or semantic phrases and should avoid dependence on capitalization, Markdown emphasis or prose punctuation when those details are not themselves governance requirements.

Whenever `CONTENT_MARKERS` is changed, preflight must audit **every newly added or modified marker against its exact target file**. In addition, whenever a validator-targeted file is changed, preflight must audit **all existing markers that target that file**, even if `tools/validate_repo.py` itself was not edited. Checking only a selected subset is not sufficient and must not be reported as a complete marker preflight.

**Scope:** agents and repository-maintenance tooling.


### LCI-005 — Windows shortcut artifact makes Local CI tree dirty

**First observed:** 2026-09-21 on `01603925a5c3d690e5e6cbfbcbaedc40e42a76e8`  
**Class:** `DIRTY_TREE`

**Symptom**

Repository validation passes, but Full Local CI stops before Ruff/pytest because `git status --porcelain` reports an untracked Windows shortcut such as:

`reports/local_ci/ATS_TASK_CHECK.bat - ... .lnk`

The shortcut is not ATS source, research evidence or a required runtime report.

**Root cause**

Windows Explorer / shell interaction can create a `.lnk` shortcut inside `reports/local_ci/`. That directory intentionally contains local runtime outputs, but the shortcut was not covered by the runtime ignore policy, so exact-commit verification treated the worktree as dirty.

**Correct response**

Do not change research logic or validation code. Keep meaningful untracked source files blocking, but classify shell-created shortcuts in the local-report directory as disposable runtime artifacts.

The repository ignores only:

`reports/local_ci/*.lnk`

This scope is deliberately narrow. ATS does **not** globally ignore `*.lnk`.

**Preventive rule**

1. Local CI runtime directories must explicitly ignore known OS-generated disposable artifacts that do not carry research/code evidence.
2. Ignore rules must be narrowly scoped so accidental real source files still make the completion gate fail.
3. The validator must assert the runtime ignore rule so it cannot silently disappear.
4. When a dirty-tree failure occurs, inspect the exact `git status --porcelain` entry before deleting files or changing source code.

**Scope:** OWNER Windows workflow and agents.


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
