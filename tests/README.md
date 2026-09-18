# Tests

ATS is in `M2_RESEARCH_PLATFORM_MVP`.

Canonical environment baseline:

- `governance/program/RESEARCH_ENVIRONMENT_SPEC.md`;
- `pyproject.toml`;
- `.python-version`;
- `uv.lock`.

## Current M2 test baseline

`tests/test_environment_baseline.py` verifies that the frozen environment uses the exact supported CPython patch and direct dependency versions.

Canonical command:

```bash
uv run --frozen pytest tests/test_environment_baseline.py
```

This test is infrastructure verification only. It does not create an Idea, Hypothesis, Candidate, Experiment or trading evidence.

## Dataset Manifest tests

`tests/test_dataset_manifest.py` validates the canonical synthetic Manifest, safe YAML loading, immutable typed parsing, timestamp/availability rules, deterministic ordering/tie-break rules, version syntax and integrity metadata.

These remain software/schema tests only and are not research evidence.

## Later M2 tests

As capabilities are implemented, tests will be added for:

- deterministic ordering and tie-breaking;
- base loader error/missing/duplicate handling;
- Strategy/Research interface semantics;
- deterministic replay transitions;
- explicit cost calculations;
- analytics/result schemas;
- manifest-driven runner behavior;
- repeated-run equality/tolerance using synthetic non-market fixtures.

Broker execution, order idempotency, reconciliation, live risk controls and shadow/live behavior belong to later milestones and are not M2 test requirements.

## Quality commands

Fast developer gate:

```bash
uv run --frozen python tools/verify_repo.py --fast
```

Full completion gate:

```bash
uv run --frozen python tools/verify_repo.py
```

The full gate runs repository validation, the complete pytest suite, Ruff lint/format checks and the environment fingerprint. Policy: `governance/program/LOCAL_CI_GATE.md`.


## Base data loader tests

`tests/test_data_loader.py` verifies:

- deterministic repeat loading of the canonical synthetic CSV fixture;
- SHA-256 mismatch rejection;
- out-of-order reject/sort behavior;
- duplicate reject/keep-first/keep-last behavior;
- malformed reject/drop behavior;
- explicit information-availability timestamp parsing;
- coverage enforcement;
- required ordering/tie-break columns;
- unsupported format rejection;
- coverage violations remaining blocking even when malformed rows may be dropped.

Fixture bytes are deterministic non-market software inputs and do not create research evidence.
