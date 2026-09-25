# ATS Local CI Gate

**Status:** BASELINE  
**Scope:** repository-wide quality gate  
**Replaces:** GitHub Actions as the mandatory completion gate

## Purpose

ATS uses a local verification gate because hosted GitHub Actions is no longer part of the operating workflow.

GitHub remains the remote source-control repository. Repository correctness is verified on the canonical local environment before push.

## Canonical Windows owner workflow

For task completion, the stable owner launcher is:

```powershell
.\\ATS_TASK_CHECK.bat
```

When commands are shown for Windows PowerShell, repository-local BAT launchers must always include the explicit current-directory prefix `.\\`. PowerShell does not search the current directory for commands by default. Use `.\\ATS_TASK_CHECK.bat`, `.\\ATS_AGENT_PREFLIGHT.bat` and `.\\ATS_TASK_DIAG.bat`; do not instruct OWNER to run the bare BAT filename from PowerShell.

It performs repository update, frozen environment sync and the task-specific package in `tools/current_task_check.py`, then writes `reports/local_ci/CURRENT_TASK_REPORT.txt`.

The agent updates `tools/current_task_check.py` when the active task changes; the BAT remains stable.

OWNER should use `.\\ATS_TASK_CHECK.bat` in PowerShell and send `CURRENT_TASK_REPORT.txt` instead of manually copying console commands/output.

## Agent staging workflow before main

Material changes authored through remote repository APIs are staged on an `agent/*` branch first. In particular, remotely authored Python must not be merged directly to `main` when the exact pinned Ruff environment has not already checked that content.

The OWNER pre-merge launcher is:

`.\\ATS_AGENT_PREFLIGHT.bat`

It:

1. refreshes `origin/main`;
2. synchronizes the frozen uv environment;
3. verifies that the current branch is `agent/*` and the working tree is clean;
4. runs the full normal Local CI gate on the exact agent commit;
5. writes `reports/local_ci/AGENT_PREFLIGHT_REPORT.txt`.

It deliberately does **not** run task-specific acquisition or other expensive current-task runtime work.

An agent branch may be squash-merged to `main` only after `ATS AGENT PREFLIGHT: PASS` names the exact agent commit being merged. After merge, final task completion still requires `ATS_TASK_CHECK.bat` on the exact `main` commit.

## Targeted runtime diagnostic workflow

When the first failing stage is task runtime and the root cause is not yet proven, use:

`.\\ATS_TASK_DIAG.bat`

It invokes `tools/current_task_diag.py` and writes:

`reports/local_ci/CURRENT_TASK_DIAG_REPORT.txt`

For RF-008 the diagnostic runner is cache-only by design: it does not request market data from the network and does not execute all 217 source months. It inspects one requested failing source candle, source hashes, BID/ASK rows and nearby observations. A diagnostic COMPLETE result is evidence for root-cause analysis, not task completion.

## Canonical commands

Direct full completion gate, primarily for tooling/hooks:

```bash
uv run --frozen python tools/verify_repo.py
```

Fast development gate:

```bash
uv run --frozen python tools/verify_repo.py --fast
```

The full gate is authoritative for task completion. The fast gate is only a developer convenience.

## Full gate

The full gate checks:

1. working tree is clean so the verified code matches the commit being pushed;
2. `tools/validate_repo.py`;
3. the complete pytest suite;
4. Ruff lint for maintained Python surfaces, including governance validators;
5. Ruff format check for active implementation/test surfaces; legacy-style validator files remain linted but are not reformatted wholesale;
6. environment fingerprint.

The gate prints one final result:

`ATS LOCAL CI: PASS`

or:

`ATS LOCAL CI: FAIL`.

## Fast gate

The fast gate runs repository validation plus Ruff lint/format checks.

It may run with an uncommitted working tree and therefore is not sufficient to close a material program task.

## Local audit report

Each full Python gate writes:

`reports/local_ci/LATEST.json`

The Windows launchers write these shareable reports:

- `reports/local_ci/CURRENT_TASK_REPORT.txt` — final task completion attempt;
- `reports/local_ci/AGENT_PREFLIGHT_REPORT.txt` — pre-merge agent-branch verification;
- `reports/local_ci/CURRENT_TASK_DIAG_REPORT.txt` — targeted runtime diagnostic

The report includes:

- verification mode;
- Git commit SHA;
- dirty/clean working-tree state;
- start/end timestamps;
- commands and return codes;
- environment fingerprint when available;
- overall PASS/FAIL.

`LATEST.json` and `CURRENT_TASK_REPORT.txt` are local runtime evidence and are ignored by Git. Canonical governance does not depend on committing machine-specific verification output.

## Agent remote pre-push checklist

Before any material remote write, agents must apply:

`governance/program/AGENT_PRE_PUSH_CHECKLIST.md`

The checklist makes Python formatting status, canonical-state reconciliation and validator-marker audit explicit before OWNER verification. A remote commit with unverified Python formatting remains `FORMAT_UNVERIFIED_UNTIL_PINNED_RUFF`; task completion remains `PENDING_OWNER_LAUNCHER` until the exact HEAD passes the launcher.

## Failure handling and durable lessons

A FAIL must be diagnosed from the first failing stage before source changes are made.

Reusable failure knowledge is stored in:

`governance/program/LOCAL_CI_TROUBLESHOOTING.md`

The troubleshooting registry records failure class, supported root cause, correct response and preventive rule. It does not store raw local reports.

Infrastructure failures such as `git pull --ff-only` connectivity errors must not trigger speculative code changes. Conversely, a formatter-only failure should be fixed as a formatting issue when tests/lint/validator already establish that no separate logic failure is present.

When an agent or tool writes Python directly to the remote repository and therefore bypasses local hooks, Ruff formatting remains part of the authoring responsibility. Passing tests or Ruff lint alone does not imply `ruff format --check` will pass. Such changes are staged on `agent/*` and receive OWNER `ATS_AGENT_PREFLIGHT.bat` verification before merge to `main`.

For a task-runtime/data failure whose cause is not yet demonstrated, the next step is diagnostic evidence rather than another speculative production patch. Use `ATS_TASK_DIAG.bat` when the current task exposes a targeted diagnostic.

After a merged fix, the authoritative completion evidence is still a new full task launcher run on the new exact `main` HEAD.

## Git hooks

Repository hooks:

- `.githooks/pre-commit` -> fast gate;
- `.githooks/pre-push` -> full gate.

Enable them once in a local clone:

```bash
git config core.hooksPath .githooks
```

Verify:

```bash
git config --get core.hooksPath
```

Normal work should not use `git push --no-verify`. If a hook is intentionally bypassed, the task is not considered complete until the full canonical gate passes on the exact commit.

## Completion rule

A material ATS task is complete only when:

1. deliverable/state/backlog/handoff synchronization is finished;
2. the full local gate passes on the exact commit intended for push;
3. the commit is then pushed to GitHub.

GitHub Actions status is not a completion criterion.

## Environment

The gate uses the reproducible M2 environment:

- CPython 3.13.15;
- supported local hosts: Windows x86_64 and Linux x86_64;
- uv 0.12.13;
- committed `uv.lock`;
- `uv sync --frozen` / `uv run --frozen`.

If the frozen environment cannot be created, verification is blocked rather than silently falling back to another Python or dependency set.


## Fast preflight before the completion check

The Windows launcher runs:

`uv run --frozen python tools/verify_repo.py --fast`

after environment sync and before `tools/current_task_check.py`.

Purpose: recurrent validator/lint/format failures are caught before the expensive full pytest/fingerprint stage. This is an early-failure control only; it does not replace the final full Local CI gate.

If the fast preflight fails, the launcher exits with code `16`.
