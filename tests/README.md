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

## Later M2 tests

As capabilities are implemented, tests will be added for:

- Dataset Manifest validation;
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
