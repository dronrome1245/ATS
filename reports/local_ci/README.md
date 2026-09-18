# Local CI reports

Windows owner workflow uses one launcher:

`ATS_CHECK.bat`

It automatically performs:

1. `git pull --ff-only`;
2. `uv sync --frozen`;
3. full `tools/verify_repo.py`.

The shareable human-readable report is:

`reports/local_ci/LATEST_REPORT.txt`

The machine-readable report remains:

`reports/local_ci/LATEST.json`

Both files are intentionally ignored by Git because they contain machine-local runtime verification output.

When a local check passes or fails, send `LATEST_REPORT.txt` to ChatGPT. The report is designed to contain enough command output to diagnose the next blocker without manually copying commands or console text.

Canonical policy: `governance/program/LOCAL_CI_GATE.md`.
