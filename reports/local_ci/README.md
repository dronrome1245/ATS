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
