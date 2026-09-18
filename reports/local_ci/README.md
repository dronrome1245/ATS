# Local CI reports

The canonical ATS local quality gate writes its latest machine-local result to:

`reports/local_ci/LATEST.json`

`LATEST.json` is intentionally ignored by Git because it contains runtime-local verification metadata.

Canonical command:

```bash
uv run --frozen python tools/verify_repo.py
```

Policy: `governance/program/LOCAL_CI_GATE.md`.
