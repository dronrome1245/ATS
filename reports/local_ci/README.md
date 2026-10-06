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

`ATS_TASK_DIAG.bat` runs the task-specific `tools/current_task_diag.py`. Diagnostic behavior must match the active failure class. For RF-023 it performs bounded provider-access probes only, comparing the failing September 2026 EUR/USD source paths with August 2026 controls; it does not compute any HYP-0005 outcome.

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

For an unmerged agent change:

1. switch to the requested `agent/*` branch;
2. double-click `ATS_AGENT_PREFLIGHT.bat`;
3. send `AGENT_PREFLIGHT_REPORT.txt` to ChatGPT;
4. do not run the full task launcher until the agent branch has passed and been merged.

For an unresolved task-runtime/data failure:

1. stay on the exact failing commit;
2. double-click `ATS_TASK_DIAG.bat`;
3. send `CURRENT_TASK_DIAG_REPORT.txt` to ChatGPT.

For final task completion after merge:

1. switch back to `main` and pull the merged commit;
2. double-click `ATS_TASK_CHECK.bat`;
3. send `CURRENT_TASK_REPORT.txt` to ChatGPT.

Canonical policy: `governance/program/LOCAL_CI_GATE.md`.


## Runtime-output ignore policy

`reports/local_ci/` is a runtime-output directory. Generated files must be ignored by narrow, purpose-specific patterns rather than by ignoring the whole directory.

Current patterns include:

- `reports/local_ci/AGENT_PREFLIGHT_REPORT.txt` — pre-merge agent-branch OWNER verification report;
- `reports/local_ci/CURRENT_TASK_DIAG_REPORT.txt` — targeted task-runtime diagnostic report;
- `reports/local_ci/SEARCH-*-result.json` — machine-readable bounded-discovery runtime results;
- `reports/local_ci/SEARCH-*-report.txt` — bounded-discovery shareable summaries;
- `reports/local_ci/HYP0002_DATA_FEASIBILITY.json` — local HYP-0002 threshold/data-preparation evidence;
- `reports/local_ci/HYP0002_DATA_FEASIBILITY_REPORT.txt` — HYP-0002 preparation summary;
- `reports/local_ci/HYP0002_PROTO01_RESULT.json` — HYP-0002 PROTO-01 local machine result after reveal;
- `reports/local_ci/HYP0002_PROTO01_RESULT_REPORT.txt` — HYP-0002 PROTO-01 local result summary after reveal;
- `reports/local_ci/HYP0003_DEVELOPMENT_DATA.json` — RF-008 HYP-0003 development-data machine preparation result;
- `reports/local_ci/HYP0003_DEVELOPMENT_DATA_REPORT.txt` — RF-008 shareable development-data preparation summary;
- `reports/local_ci/HYP0003_PROTO01_RESULT.json` — HYP-0003 PROTO-01 local machine result after RF-011 reveal;
- `reports/local_ci/HYP0003_PROTO01_RESULT_REPORT.txt` — HYP-0003 PROTO-01 local result summary after RF-011 reveal;
- `reports/local_ci/HYP0004_DEVELOPMENT_DATA.json` — RF-017 HYP-0004 local development-data preparation result;
- `reports/local_ci/HYP0004_DEVELOPMENT_DATA_REPORT.txt` — RF-017 HYP-0004 preparation summary;
- `reports/local_ci/HYP0004_PROTO01_RESULT.json` — HYP-0004 PROTO-01 local machine result after RF-020 reveal;
- `reports/local_ci/HYP0004_PROTO01_RESULT_REPORT.txt` — HYP-0004 PROTO-01 local result summary after RF-020 reveal;
- `reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP.json` — RF-023 HYP-0005 local confirmatory data-feasibility preparation result;
- `reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP_REPORT.txt` — RF-023 shareable confirmatory data-feasibility preparation summary;
- `reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP.json` — RF-027 HYP-0006 event/tick geometry preparation result;
- `reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP_REPORT.txt` — RF-027 shareable event/tick geometry preparation summary;
- `reports/local_ci/HYP0006_DUKASCOPY_CONTROLLED_DOWNLOAD.json` — RF-027 controlled Dukascopy preload machine report;
- `reports/local_ci/HYP0006_DUKASCOPY_CONTROLLED_DOWNLOAD_REPORT.txt` — RF-027 controlled preload shareable summary;
- `reports/local_ci/HYP0006_DUKASCOPY_CONTROLLED_DOWNLOAD_INVENTORY.csv` — deterministic 1,085-object local/network inventory with no price or outcome fields;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_PILOT_50.json` — bounded 50-object browser-pilot machine report;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_PILOT_50_REPORT.txt` — bounded browser-pilot shareable summary;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_PILOT_50_MANIFEST.csv` — deterministic selected-object dry-run manifest;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_PILOT_50_CONSUMED.json` — local one-shot authorization-consumption sentinel;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_BATCH_250.json` — bounded 250-object browser-batch machine report;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_BATCH_250_REPORT.txt` — bounded 250-object browser-batch shareable summary;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_BATCH_250_MANIFEST.csv` — deterministic selected-object dry-run manifest;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_BATCH_250_CONSUMED.json` — local one-shot 250-object authorization-consumption sentinel;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_REMAINING_748.json` — one-shot all-remaining 748-object browser batch machine report;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_REMAINING_748_REPORT.txt` — remaining-748 shareable summary;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_REMAINING_748_MANIFEST.csv` — deterministic all-remaining dry-run manifest;
- `reports/local_ci/HYP0006_DUKASCOPY_BROWSER_REMAINING_748_CONSUMED.json` — local one-shot remaining-748 authorization-consumption sentinel;
- `reports/local_ci/*.lnk` — disposable Windows Explorer shortcuts.

The rules are deliberately directory-scoped and filename-scoped so unrelated untracked files still make the full clean-tree gate fail.

A task runner that creates a new local runtime filename must add an appropriate narrow ignore rule before the runner is used inside a completion check.
