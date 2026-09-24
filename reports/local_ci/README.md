# Local CI reports

Normal Windows task-completion workflow uses:

`ATS_TASK_CHECK.bat`

Agent-authored changes now use a separate staging workflow before they are merged to `main`:

`ATS_AGENT_PREFLIGHT.bat`

Runtime data failures that need evidence before a code change use:

`ATS_TASK_DIAG.bat`

The completion BAT remains task-agnostic. It automatically performs:

1. `git pull --ff-only`;
2. `uv sync --frozen`;
3. `tools/current_task_check.py`.

`ATS_AGENT_PREFLIGHT.bat` runs only on an `agent/*` branch. It refreshes `origin/main`, synchronizes the frozen environment, then runs the full normal Local CI gate on the exact agent commit. It does not run task-specific acquisition. The agent may merge the branch to `main` only after this preflight returns PASS.

`ATS_TASK_DIAG.bat` runs `tools/current_task_diag.py`. For RF-008 it reads only already cached source objects and does not request market data from the network. Its default diagnostic target is the latest confirmed failing candle, and optional command-line arguments can select another target.

`tools/current_task_check.py` and `tools/current_task_diag.py` are task-specific surfaces and are updated by the agent when the active work package changes.

Shareable reports are:

- `reports/local_ci/CURRENT_TASK_REPORT.txt` — final task launcher;
- `reports/local_ci/AGENT_PREFLIGHT_REPORT.txt` — agent-branch pre-merge verification;
- `reports/local_ci/CURRENT_TASK_DIAG_REPORT.txt` — targeted runtime diagnostic.

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
- `reports/local_ci/HYP0002_PROTO01_RESULT.json` — HYP-0002 PROTO-01 local machine result after reveal;
- `reports/local_ci/HYP0002_PROTO01_RESULT_REPORT.txt` — HYP-0002 PROTO-01 local result summary after reveal;
- `reports/local_ci/HYP0003_DEVELOPMENT_DATA.json` — RF-008 HYP-0003 development-data machine preparation result;
- `reports/local_ci/HYP0003_DEVELOPMENT_DATA_REPORT.txt` — RF-008 shareable development-data preparation summary;
- `reports/local_ci/*.lnk` — disposable Windows Explorer shortcuts.

The rules are deliberately directory-scoped and filename-scoped so unrelated untracked files still make the full clean-tree gate fail.

A task runner that creates a new local runtime filename must add an appropriate narrow ignore rule before the runner is used inside a completion check.
