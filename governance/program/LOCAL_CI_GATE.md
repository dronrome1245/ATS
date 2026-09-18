# ATS Local CI Gate

**Status:** BASELINE  
**Scope:** repository-wide quality gate  
**Replaces:** GitHub Actions as the mandatory completion gate

## Purpose

ATS uses a local verification gate because hosted GitHub Actions is no longer part of the operating workflow.

GitHub remains the remote source-control repository. Repository correctness is verified on the canonical local environment before push.

## Canonical Windows owner workflow

The normal Windows workflow is one launcher from repository root:

```bat
ATS_CHECK.bat
```

The launcher performs `git pull --ff-only`, `uv sync --frozen` and the full Local CI Gate, then writes `reports/local_ci/LATEST_REPORT.txt`.

The OWNER should normally send that TXT report to ChatGPT instead of manually copying console commands/output.

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

The Windows launcher writes a shareable combined report:

`reports/local_ci/LATEST_REPORT.txt`

The report includes:

- verification mode;
- Git commit SHA;
- dirty/clean working-tree state;
- start/end timestamps;
- commands and return codes;
- environment fingerprint when available;
- overall PASS/FAIL.

`LATEST.json` and `LATEST_REPORT.txt` are local runtime evidence and are ignored by Git. Canonical governance does not depend on committing machine-specific verification output.

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
