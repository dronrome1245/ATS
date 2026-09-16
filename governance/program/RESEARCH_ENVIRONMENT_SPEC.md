# ATS M2 Research Environment Specification

**Task:** `ATS2-M2-002`  
**Work package:** `WBS-2.2`  
**Status:** BASELINE  
**Architecture source:** `governance/decisions/ADR-0001-RESEARCH-STACK.md`

## 1. Purpose

This specification materializes the accepted M2 research-stack ADR into one reproducible local/CI environment baseline.

It fixes the runtime/tool/dependency versions and the canonical install/run commands needed before Dataset Manifest, loader, Strategy API or replay implementation begins.

This is research infrastructure only. It does not select Reference Strategy #1 and does not create a broker/live path.

## 2. Supported runtime

The exact M2 baseline runtime is:

- implementation: `CPython`;
- exact patch: `3.13.15`;
- operational pin: root `.python-version`;
- project compatibility range: `>=3.13,<3.14` in `pyproject.toml`.

The compatibility range intentionally describes source/package compatibility across the 3.13 line. The supported reproducibility baseline is the exact patch in `.python-version`.

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

The committed `uv.lock` fixes the full dependency graph used by the current direct pins, including:

- `annotated-types == 0.8.0`;
- `pydantic-core == 2.46.5`;
- `typing-extensions == 4.16.0`;
- `typing-inspection == 0.4.4`;
- `iniconfig == 2.3.0`;
- `packaging == 26.3`;
- `pluggy == 1.6.0`;
- `Pygments == 2.21.0`;
- `colorama == 0.4.6` on Windows through pytest's platform marker.

The lock is the canonical resolution. Direct/transitive versions must not be upgraded opportunistically during another M2 work package.

## 6. Canonical setup

Prerequisite: install the project-required uv version using the official uv distribution mechanism.

Then from repository root:

```bash
uv python install 3.13.15
uv sync --frozen
```

`--frozen` is mandatory for reproducibility checks and CI. It prevents environment setup from silently changing `uv.lock`.

The normal environment is repository-local `.venv/`, which remains ignored by Git.

## 7. Canonical commands

Repository/governance validation:

```bash
uv run --frozen python tools/validate_repo.py
```

Environment verification:

```bash
uv run --frozen pytest tests/test_environment_baseline.py
uv run --frozen python tools/environment_fingerprint.py
```

Lint baseline:

```bash
uv run --frozen ruff check tools/environment_fingerprint.py tests/test_environment_baseline.py
```

Full platform tests will grow under later M2 work packages. M2-002 does not invent loader/replay tests before those components exist.

## 8. Environment fingerprint

`tools/environment_fingerprint.py` emits machine-readable JSON containing at least:

- Python implementation/version;
- operating-system/platform description;
- uv version visible on PATH;
- exact installed versions of direct and test dependencies.

The fingerprint is diagnostic/reproducibility metadata. It is not market evidence and does not receive an Experiment ID.

## 9. CI contract

The repository workflow must be able to perform the same frozen environment steps:

1. checkout repository;
2. activate/install CPython `3.13.15`;
3. install uv `0.12.13`;
4. `uv sync --frozen`;
5. run repository validator;
6. emit environment fingerprint;
7. run the M2 environment test baseline;
8. run the configured Ruff check.

A CI scheduling/runner failure before steps execute is infrastructure failure, not a passing or failing repository validation result.

## 10. Lock update procedure

A dependency/runtime change requires an intentional environment update:

1. record the reason and affected M2 capability;
2. update exact direct pins or Python/uv pin;
3. regenerate `uv.lock` with the approved uv version;
4. run frozen sync from a clean environment;
5. run validator, tests, lint and fingerprint;
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

- exact CPython and uv versions are fixed;
- `pyproject.toml`, `.python-version` and `uv.lock` are committed;
- direct and transitive environment versions are locked;
- frozen setup/run commands are documented;
- an environment fingerprint command exists;
- a non-market environment test verifies the pinned baseline;
- CI is configured to use the frozen environment when a runner is available;
- state/backlog/status/next/handoff/validator are synchronized;
- `ATS2-M2-003 — Dataset manifest support` becomes the single next ready task.
