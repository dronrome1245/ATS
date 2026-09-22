# Local CI reports

Normal Windows owner workflow uses one stable launcher:

`ATS_TASK_CHECK.bat`

The BAT itself is task-agnostic. It automatically performs:

1. `git pull --ff-only`;
2. `uv sync --frozen`;
3. `tools/current_task_check.py`.

`tools/current_task_check.py` is the task-specific verification package and is updated by the agent when the current work package changes.

The shareable report for the current task is always:

`reports/local_ci/CURRENT_TASK_REPORT.txt`

The Python Local CI runner additionally writes:

`reports/local_ci/LATEST.json`

All runtime reports are intentionally ignored by Git.

Reusable failure lessons are committed separately in:

`governance/program/LOCAL_CI_TROUBLESHOOTING.md`

Do not commit raw `CURRENT_TASK_REPORT.txt` or `LATEST.json`. After a FAIL, the agent should classify the first failing stage and preserve only durable root-cause/prevention knowledge in the troubleshooting registry.

OWNER workflow:

1. double-click `ATS_TASK_CHECK.bat`;
2. wait for PASS or FAIL;
3. send `CURRENT_TASK_REPORT.txt` to ChatGPT.

Canonical policy: `governance/program/LOCAL_CI_GATE.md`.


## Runtime-output ignore policy

`reports/local_ci/` is a runtime-output directory. Generated files must be ignored by narrow, purpose-specific patterns rather than by ignoring the whole directory.

Current patterns include:

- `reports/local_ci/SEARCH-*-result.json` — machine-readable bounded-discovery runtime results;
- `reports/local_ci/SEARCH-*-report.txt` — bounded-discovery shareable summaries;
- `reports/local_ci/HYP0002_DATA_FEASIBILITY.json` — local HYP-0002 threshold/data-preparation evidence;
- `reports/local_ci/HYP0002_DATA_FEASIBILITY_REPORT.txt` — HYP-0002 preparation summary;
- `reports/local_ci/*.lnk` — disposable Windows Explorer shortcuts.

The rules are deliberately directory-scoped and filename-scoped so unrelated untracked files still make the full clean-tree gate fail.

A task runner that creates a new local runtime filename must add an appropriate narrow ignore rule before the runner is used inside a completion check.
