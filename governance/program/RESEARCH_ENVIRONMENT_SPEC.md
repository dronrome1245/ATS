# ATS M2 Research Environment Specification

**Task:** `ATS2-M2-002`  
**Work package:** `WBS-2.2`  
**Status:** BASELINE  
**Architecture source:** `governance/decisions/ADR-0001-RESEARCH-STACK.md`

## 1. Purpose

This specification materializes the accepted M2 research-stack ADR into one reproducible local environment baseline.

It fixes the runtime/tool/dependency versions and the canonical install/run commands needed before Dataset Manifest, loader, Strategy API or replay implementation begins.

This is research infrastructure only. It does not select Reference Strategy #1 and does not create a broker/live path.

## 2. Supported runtime and host

The exact M2 reproducibility baseline is:

- implementation: `CPython`;
- exact patch: `3.13.15`;
- supported hosts: `Windows x86_64` and `Linux x86_64`;
- operational Python pin: root `.python-version`;
- project Python compatibility range: `>=3.13,<3.14` in `pyproject.toml`;
- uv resolution environments: `sys_platform == 'win32' and platform_machine == 'AMD64'` and `sys_platform == 'linux' and platform_machine == 'x86_64'`.

The compatibility range describes source/package compatibility across the 3.13 line. Reproducibility claims for M2 are made against the exact Python patch on the supported Windows x86_64 and Linux x86_64 hosts above.

Other operating systems/architectures are not declared reproducibility targets by M2-002. Windows x86_64 is the primary local workstation target; Linux x86_64 remains a supported reproducibility target.

Free-threaded/experimental Python builds are out of scope for M2.

## 3. uv baseline

Canonical project/environment tool:

- `uv == 0.12.13`.

`pyproject.toml` sets:

`[tool.uv] required-version = "==0.12.13"`

A different uv version must fail the project command instead of silently changing lock/resolution behavior.

## 4. Direct dependency pins

Runtime dependencies are exact-pinned:

- `pydantic == 2.13.5`;
- `PyYAML == 6.0.3`;
- `numpy == 2.5.3`.

Development dependencies are exact-pinned:

- `pytest == 9.1.1`;
- `ruff == 0.16.7`.

No dependency is added merely because it is common in data-science projects.

## 5. Locked transitive baseline

The committed `uv.lock` fixes the dependency graph used by the current direct pins, including:

- `annotated-types == 0.8.0`;
- `pydantic-core == 2.46.5`;
- `typing-extensions == 4.16.0`;
- `typing-inspection == 0.4.4`;
- `iniconfig == 2.3.0`;
- `packaging == 26.3`;
- `pluggy == 1.6.0`;
- `Pygments == 2.21.0`.

`colorama == 0.4.6` is retained in the lock because pytest declares it under the Windows marker, but it is not installed in the canonical Linux environment.

For packages with platform-specific binaries, the lock includes Windows x86_64 and Linux x86_64 wheel URLs and SHA-256 hashes. Pure-Python dependencies use universal wheels.

The lock is the canonical resolution. Direct/transitive versions must not be upgraded opportunistically during another M2 work package.

## 6. Canonical setup

Prerequisite: install the project-required uv version using the official uv distribution mechanism.

Canonical Windows PowerShell bootstrap for the pinned baseline:

```powershell
$installer = Join-Path $env:TEMP "uv-0.12.13-install.ps1"
Invoke-WebRequest -UseBasicParsing "https://astral.sh/uv/0.12.13/install.ps1" -OutFile $installer
powershell -ExecutionPolicy ByPass -File $installer
```

ATS prefers the download-to-file form on Windows because nested `irm ... | iex` execution can be affected by shell/pipeline parsing on some PowerShell environments.

After installation, open a new terminal/session if necessary and verify:

```powershell
where.exe uv
uv --version
```

The version must begin with:

`uv 0.12.13`

Then from repository root on the supported host:

```bash
uv python install 3.13.15
uv sync --frozen
```

If `ATS_TASK_CHECK.bat` reports `ERROR: uv is not available on PATH.` with exit code `12`, the host bootstrap is incomplete or the new process does not see uv on PATH. Diagnose/install the environment; do not change ATS source code.

If `uv python install 3.13.15` warns that a `python3.13.exe` already exists but is not managed by uv, do not use `--force` automatically. The warning concerns the convenience executable in the user bin directory, not necessarily the project interpreter. Continue with `uv sync --frozen` and confirm the environment fingerprint. uv only overwrites unmanaged Python executables when explicitly forced.

When moving/copying an ATS working directory between computers, an existing repository-local `.venv` may reference a Python interpreter that does not exist on the new host. `uv sync --frozen` may report that the old environment is being ignored and can recreate it. If it cannot, deleting only `.venv` and rerunning frozen sync is permitted because `.venv` is disposable and ignored by Git.

`--frozen` is mandatory for reproducibility checks and the Local CI Gate. It prevents environment setup from silently changing `uv.lock`.

The normal environment is repository-local `.venv/`, which remains ignored by Git.

## 7. Canonical commands

Fast developer gate:

```bash
uv run --frozen python tools/verify_repo.py --fast
```

Full completion gate:

```bash
uv run --frozen python tools/verify_repo.py
```

The full gate runs repository/governance validation, the complete pytest suite, Ruff lint/format checks and the environment fingerprint. Individual commands remain available for diagnosis, but the full gate is the completion criterion. Full platform tests will grow under later M2 work packages.

## 8. Environment fingerprint

`tools/environment_fingerprint.py` emits machine-readable JSON containing at least:

- Python implementation/version;
- operating-system/platform description;
- uv version visible on PATH;
- exact installed versions of direct and test dependencies.

The fingerprint is diagnostic/reproducibility metadata. It is not market evidence and does not receive an Experiment ID.

## 9. Local quality gate contract

Canonical policy: `governance/program/LOCAL_CI_GATE.md`.

The supported local verification path is:

1. use CPython `3.13.15` and uv `0.12.13` on Windows x86_64 or Linux x86_64;
2. `uv sync --frozen`;
3. enable hooks once with `git config core.hooksPath .githooks`;
4. use the fast gate during development;
5. run the full gate on a clean exact commit before push;
6. require `ATS LOCAL CI: PASS` for material-task completion.

GitHub Actions is not a completion criterion.

## 10. Lock verification and update procedure

The lock declares compatible binary artifacts for both supported hosts. Windows x86_64 support includes locked wheels for NumPy, Pydantic Core, PyYAML and Ruff in addition to the Linux x86_64 wheels.

An intentional dependency/runtime change requires:

1. record the reason and affected M2 capability;
2. update exact direct pins or Python/uv pin;
3. regenerate `uv.lock` with the approved uv version and network access;
4. run frozen sync from a clean supported environment;
5. run the full Local CI Gate;
6. commit `pyproject.toml`, `.python-version`, `uv.lock` and affected governance together.

Never edit a completed Experiment's historical environment field to pretend that a later dependency upgrade was used originally.

## 11. Explicit exclusions

M2-002 does not add:

- pandas/Polars/PyArrow/DuckDB;
- notebook runtime as source of truth;
- Docker as a mandatory baseline;
- broker SDKs or live market-data clients;
- portfolio/risk/execution infrastructure;
- cloud/VPS dependencies;
- a concrete strategy implementation.

Those require a later demonstrated consumer need.

## 12. Definition of Done

`ATS2-M2-002` is complete when:

- exact CPython, uv and supported host platforms are fixed;
- `pyproject.toml`, `.python-version` and an installable-artifact `uv.lock` are committed;
- direct and transitive environment versions are locked;
- frozen setup/run commands are documented;
- an environment fingerprint command exists;
- a non-market environment test verifies the pinned baseline;
- Local CI Gate and git hooks use the frozen environment;
- state/backlog/status/next/handoff/validator are synchronized;
- `ATS2-M2-003 — Dataset manifest support` becomes the single next ready task.
