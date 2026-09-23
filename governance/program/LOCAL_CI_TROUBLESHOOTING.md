# ATS Local CI Troubleshooting & Lessons

**Status:** BASELINE  
**Scope:** reusable failure knowledge for `ATS_TASK_CHECK.bat` and the Local CI Gate  
**Canonical gate:** `governance/program/LOCAL_CI_GATE.md`

## 1. Purpose

This document is the durable repository memory for recurring or reusable Local CI failures.

Runtime files such as:

- `reports/local_ci/CURRENT_TASK_REPORT.txt`;
- `reports/local_ci/LATEST.json`;

remain local evidence and are intentionally ignored by Git. Raw machine reports are not copied into this file.

A failure is recorded here only after its class and root cause are understood well enough to produce a preventive rule.

## 2. Failure-handling rule

When `ATS_TASK_CHECK.bat` returns FAIL:

1. identify the first failing stage;
2. classify the failure before changing code;
3. do not modify source code for infrastructure/network failures;
4. fix the narrowest confirmed cause;
5. if the failure reveals a reusable lesson, add or update an entry in this document;
6. rerun the full launcher on the new exact HEAD;
7. do not declare the task closed until `ATS TASK LAUNCHER: PASS`.

Known failure classes:

- `SYNC_NETWORK` — repository synchronization/connectivity failed before code verification;
- `ENVIRONMENT` — frozen environment cannot be created or fingerprinted;
- `FORMAT` — formatter check fails while logic/tests may still pass;
- `LINT` — static lint rule fails;
- `TEST` — targeted or full pytest failure;
- `VALIDATOR` — repository/governance invariant failure;
- `DIRTY_TREE` — exact-commit verification is impossible because the worktree is modified;
- `UNKNOWN` — no code change until the failure is narrowed further.

## 3. Durable lesson format

Each reusable entry must include:

- **ID** — stable `LCI-###`;
- **First observed** — date and, when relevant, commit;
- **Class**;
- **Symptom**;
- **Root cause**;
- **Correct response**;
- **Preventive rule**;
- **Scope** — whether the rule applies to OWNER workflow, agents, or both.

Do not store secrets, credentials, private paths, raw full logs or machine-specific personal information here.

## 4. Known lessons

### LCI-001 — GitHub connectivity failure during pull

**First observed:** 2026-09-18  
**Class:** `SYNC_NETWORK`

**Symptom**

`ATS_TASK_CHECK.bat` stops at `git pull --ff-only` with an error such as:

`Failed to connect to github.com:443`

The task-specific tests, validator, Ruff and full Local CI have not run yet.

**Root cause**

The launcher cannot confirm/update the local clone because GitHub is temporarily unreachable from the OWNER machine or network path.

**Correct response**

Do not change ATS source code. Restore/wait for network access and rerun the same launcher. The failure is infrastructure-level unless a separate Git configuration/authentication problem is proven.

**Preventive rule**

Always distinguish a pre-verification synchronization failure from a code failure. A `SYNC_NETWORK` failure must never trigger speculative source changes.

**Scope:** OWNER workflow and agents.

### LCI-002 — Ruff format failure after direct remote Python edit

**First observed:** 2026-09-18 on `b3085c26342c52e6ae852962faefcaf347d43a2a`  
**Repeat observed:** 2026-09-21 on `c8a0225acafba15d59dcd35d5bf3aceee716ced3` in `src/ats/runner/experiment.py`  
**Repeat observed:** 2026-09-21 on `cd348024bd907225ea15219786ef5ad54ebdea1d` in `src/ats/validation/sensitivity.py` and `tools/current_task_check.py` after a manual line-length preflight incorrectly implied formatting readiness  
**Repeat observed:** 2026-09-21 on `9f912b7b5e350d287ed76ce4bffe7a67722faf58` in `src/ats/validation/slicing.py` after remote authoring without pinned Ruff execution  
**Repeat observed:** 2026-09-22 on `9fb041c51cf93071ca6735b52897cbb2b24e5568` in `src/ats/validation/concentration.py`; fast preflight correctly stopped before full pytest  
**Repeat observed:** 2026-09-22 on `9134c44d1d3d861124c44e00b4df820ad181cb5d` in `tests/test_validation_resampling.py`; fast preflight again stopped before full pytest  
**Repeat observed:** 2026-09-22 on `f989e6d77c94aaaa93df9bf6fdd994708b570404` in `tools/current_task_check.py`; fast preflight again stopped before full pytest  
**Repeat observed:** 2026-09-22 on `2048d3c9cd7162e3e71429331bd2b5979534b1d6` in `tools/current_task_check.py`; the same one-element tuple layout recurred and fast preflight again stopped before full pytest  
**Repeat observed:** 2026-09-22 on `feb146aa0a65b3909b13efabbfe2c9097c0b74c0` in `src/ats/discovery/eurusd_h1.py`; Ruff preferred a one-line boolean comparison even though the manual line-length/syntax preflight found no defect  
**Repeat observed:** 2026-09-22 on `cf7f97c0263fa6b546911aaadcea748727e8afca` in `tools/hyp0002_data_feasibility.py`; Ruff canonicalized a one-value string assignment and simple set comprehensions into compact one-line forms  
**Repeat observed:** 2026-09-22 on `7c8e82e7f29b0bc3e09de557f88dd1c14441474f` in `tools/hyp0002_data_feasibility.py`; Ruff compacted two generator expressions into its canonical single-line body form  
**Fixed first occurrence by:** `fd09a08de2a234ac1249a9e44ee7e21f32f4a7cd`  
**Class:** `FORMAT`

**Symptom**

Targeted tests, full pytest, repository validator and Ruff lint pass, but `ruff format --check` reports that a maintained Python file would be reformatted.

Observed example: a multiline conditional expression in `tests/test_cost_interface.py` was logically correct but not in Ruff's canonical layout.

**Root cause**

A Python file was written directly through the remote repository path, so local Git hooks did not get a chance to run before the remote commit existed.

**Correct response**

Apply only the formatter-prescribed style change when no logic failure is present, keep it in a style-only commit when practical, then rerun the full launcher on the new exact HEAD.

Confirmed latest resolution: `3a0dc9af4cc2191cc98c65b190b6f1f1c5cb1ea3` — exact Ruff diff applied to `src/ats/validation/concentration.py`, followed by fast-preflight PASS, pinned Ruff PASS, `115 passed`, full Local CI PASS and launcher PASS.

Confirmed sixth resolution: `6d452c4f340825eaa39b8e28dad3f6691332b217` — exact Ruff diff applied to `tests/test_validation_resampling.py`, followed by fast-preflight PASS, pinned Ruff PASS, `124 passed`, full Local CI PASS and launcher PASS.

Confirmed seventh resolution: `4d4f5546c54bc1b8985f37dd63c251b87517245e` — exact Ruff diff applied to `tools/current_task_check.py`, followed by fast-preflight PASS, pinned Ruff PASS, `124 passed`, full Local CI PASS and launcher PASS.

**Preventive rule**

For agent-created or programmatic Python edits that bypass the repository hooks:

1. treat Ruff-compatible formatting as part of authoring, not as optional cleanup;
2. when an execution environment with the pinned Ruff version is available, run the formatter/check on the exact changed file before presenting a candidate HEAD;
3. if pinned Ruff was not actually executed, do not describe formatting as preflight-passed; syntax inspection is not a substitute for `ruff format --check`;
4. never infer that passing tests + lint means format also passes;
5. if Local CI supplies an exact formatter diff, apply that canonical layout rather than hand-inventing another equivalent layout;
6. manual line-length checks, syntax compilation and visual style inspection are **not** Ruff-format preflight and must never be described as such;
7. before asking OWNER to run the launcher after remote Python edits, state formatting as either `VERIFIED_BY_PINNED_RUFF` or `NOT_YET_VERIFIED_BY_RUFF`; there is no intermediate "looks formatted" state;
8. when pinned Ruff is unavailable, still normalize previously observed canonical shapes before push: single-value parenthesized assignments and simple comprehensions should use Ruff's compact form when they fit the configured line width. This reduces recurrence but does not count as Ruff verification.

**Escalation**

This failure class is now recurring at the technical-control threshold. Documentation alone is insufficient. `ATS_TASK_CHECK.bat` must run the fast Local CI gate before the full task check so format/lint/validator failures stop the workflow before the expensive full pytest stage.

The fast preflight is now proven as an early-stop control, but it cannot verify format before push because the remote authoring environment does not have the pinned Ruff executable. Therefore remote Python commits remain explicitly format-unverified until OWNER fast preflight supplies pinned Ruff output.

**Scope:** agents and any tooling that writes directly to the remote repository.

### LCI-003 — uv missing from PATH on a new Windows host

**First observed:** 2026-09-19  
**Class:** `ENVIRONMENT`

**Symptom**

`ATS_TASK_CHECK.bat` stops before repository sync/environment sync with:

`ERROR: uv is not available on PATH.`

and returns launcher exit code `12`.

**Root cause**

The Windows host has not completed the ATS environment bootstrap, or `uv` is installed but its executable directory is not visible in the process `PATH`.

This is not a Strategy/replay/cost/analytics code failure. No pytest, validator, Ruff or environment fingerprint stage has run.

**Correct response**

Install the project-pinned `uv 0.12.13` using the official uv installer, open a new terminal/session so the updated PATH is visible, verify `uv --version`, install the pinned Python baseline, then rerun the launcher.

Canonical Windows bootstrap:

```powershell
$installer = Join-Path $env:TEMP "uv-0.12.13-install.ps1"
Invoke-WebRequest -UseBasicParsing "https://astral.sh/uv/0.12.13/install.ps1" -OutFile $installer
powershell -ExecutionPolicy ByPass -File $installer
```

The download-to-file form is the ATS-preferred Windows bootstrap because it avoids shell/pipeline parsing problems observed with nested `irm ... | iex` execution.

Then open a new PowerShell session and run:

```powershell
where.exe uv
uv --version
uv python install 3.13.15
uv sync --frozen
```

Expected uv version prefix:

`uv 0.12.13`

If `uv --version` still fails after installation, diagnose PATH visibility before changing ATS source code.

A later `uv python install 3.13.15` warning such as:

`Executable already exists ... python3.13.exe but is not managed by uv; use --force`

does not by itself mean the ATS project is blocked. uv refuses to overwrite an executable it does not manage unless `--force` is supplied. Do **not** use `--force` merely to silence this warning. First continue with `uv sync --frozen`; uv can use a compatible CPython 3.13.15 discovered on the host or a managed installation without replacing the unrelated launcher executable.

On a migrated/copied working directory, `uv sync --frozen` may also report:

`Ignoring existing virtual environment linked to non-existent Python interpreter`

This means the repository-local `.venv` points to an interpreter path that existed on the previous computer. The environment is disposable. Let `uv sync --frozen` recreate/synchronize it. If sync cannot recover it automatically, remove only the repository-local `.venv` and rerun `uv sync --frozen`; do not edit project code or `uv.lock`.

**Preventive rule**

A newly provisioned ATS host must complete the pinned tool bootstrap before the task launcher is expected to pass. Treat launcher exit code `12` as an environment/bootstrap failure and never as evidence of a code defect.

**Scope:** OWNER workflow and agents.

### LCI-004 — Repository validator marker drift from Markdown formatting

**First observed:** 2026-09-21 on `e4f397b4a985be314c75e4385d59030e77fcbfcd`  
**Repeat observed:** 2026-09-21 on `c8a0225acafba15d59dcd35d5bf3aceee716ced3` after a selective marker preflight missed three newly declared README markers  
**Repeat observed:** 2026-09-21 on `0c9823fe48c1e562d516ac311d956893afdec44f` after the M2→M3 transition changed `PROGRAM_WBS_V2.md` while an unchanged validator marker still expected the old M2 wording  
**Class:** `VALIDATOR`

**Symptom**

Targeted tests, full pytest, Ruff lint/format and environment fingerprint pass, but the repository validator reports a missing content marker for text that is visibly present in the target governance file with different capitalization or Markdown emphasis.

Observed example: the troubleshooting file contained `Do **not** use --force ...` while the validator expected the literal lower-case/plain-Markdown wording.

**Root cause**

The validator marker was coupled to presentation details instead of a stable semantic fragment. Markdown emphasis or capitalization changed the raw text while the required rule remained present.

**Correct response**

Do not change product/runtime logic. Fix the validator to search for a stable semantic phrase already present in the canonical document, then rerun the full launcher on the new exact HEAD.

**Preventive rule**

Repository content markers should validate durable invariants, identifiers or semantic phrases and should avoid dependence on capitalization, Markdown emphasis or prose punctuation when those details are not themselves governance requirements.

Whenever `CONTENT_MARKERS` is changed, preflight must audit **every newly added or modified marker against its exact target file**. In addition, whenever a validator-targeted file is changed, preflight must extract and audit **the complete current marker tuple for that target directly from `tools/validate_repo.py`**, even if validator code itself was not edited. A hand-maintained or selected subset is not sufficient and must never be reported as a complete marker preflight.

**Scope:** agents and repository-maintenance tooling.


### LCI-007 — Historical data source transient network failure

**First observed:** 2026-09-22 on `2545491d35a980e8c375100b9c8f8d99ee44f41e` while acquiring HYP-0002 confirmatory data  
**Repeat observed:** 2026-09-22 on the same exact commit after resume progressed to a later month/side  
**Repeat observed:** 2026-09-23 on `b82e827c0c8510a38aac3179411b3b2a8d455310` during HYP-0003 source availability probing  
**Repeat after control:** 2026-09-23 on `0988069a525a7cd0d8acb48a3d9ed34d3ceb0332` after outer retry batches were added  
**Repeat after control:** 2026-09-23 on `7dec11ceb34c456a6c2f6b93833eeb02b2f0e804` when HistoryStart metadata timed out after all batches  
**Repeat after control:** 2026-09-23 on `1b45022b8d57e8140016f8448a63e0a182697bcc` when HistoryStart again failed before the fallback reached a separate request-protocol defect  
**Class:** `DATA_SOURCE_NETWORK`

**Symptom**

Repository validator, pinned Ruff, pytest and full Local CI pass, but the task-specific data preparation step receives repeated upstream `HTTP 503 Service Unavailable`, read timeout or connection reset errors from the frozen historical-data provider.

**Root cause**

The external data source is intermittently unavailable during acquisition. Successful month/side files are already persisted locally, so later runs resume from the first missing source file rather than restarting the whole acquisition.

The third occurrence exposed a control gap in the new HYP-0003 availability probe: it had short per-URL retries, but no outer per-object retry batches with increasing backoff. A transient reset while classifying an old month therefore aborted the task before the existing cache/resume design could accumulate further progress.

The fourth occurrence showed a second boundary bug: `urllib.request.urlopen()` can raise a direct Windows `OSError` / `ConnectionResetError`, not only `URLError`. The final reset therefore escaped `ProbeError`, bypassed the remaining fallback/retry taxonomy and surfaced as raw `WinError 10054`.

The fifth occurrence showed that the dedicated metadata path itself was still a single point of failure: `HistoryStart.bi5` timed out after all bounded batches. The source provider also exposes H1 inception through the public instruments metadata field `history_start_60min`, so source discovery now has a provider-native fallback rather than changing provider or research period.

The sixth occurrence repeated the same upstream HistoryStart unavailability. Its subsequent fallback `HTTP 403` is classified separately as `LCI-012` because that failure is caused by the request contract, not by source-network availability.

The seventh occurrence happened during RF-008 full development acquisition after all local quality gates passed. The legacy monthly BI5 hosts could not deliver `GBPUSD 2003-08 BID`: `datafeed.dukascopy.com` timed out and `www.dukascopy.com/datafeed` returned `HTTP 503` through all bounded batches. Current Dukascopy ecosystem tooling now uses the provider-native `https://jetta.dukascopy.com/v1` compact candle API for H1 monthly buckets, so the acquisition request path—not the frozen provider or period—needed a provider-native fallback update.

**Correct response**

Do not change the Hypothesis, data period or provider merely because of a transient source-network failure. Keep the existing local cache and retry only the missing month/side. Use bounded additional download/probe batches with increasing backoff; if the source remains unavailable after the bound, fail closed without computing any research outcome.

For HYP-0003 probes, the control is `probe_side_resilient()` with `PROBE_BATCH_BACKOFF_SECONDS = (5.0, 15.0, 30.0)`. Each new batch reuses any source object already cached by a previous attempt. `fetch_bytes()` must normalize both `URLError` and direct `OSError` socket failures into `ProbeError` so fallback endpoints and outer retry batches remain active.

For RF-008 full H1 acquisition, use the current Dukascopy Jetta monthly candle API as the first provider-native content path and keep already cached / legacy BI5 as fallback. Jetta compact JSON is decoded without creating synthetic flat bars for omitted hours; missing expected market hours remain explicit quality statistics.

**Preventive rule**

1. External-source research preparation must be resumable and idempotent at a source-file boundary.
2. Confirmed successful files must be reused from the local frozen cache.
3. Transient 5xx/timeouts may receive bounded retry batches with backoff.
4. Exhausted retries remain a blocking source-network failure; they must not trigger post-hoc source/period changes.
5. The preparation step must preserve the declared information boundary while retrying.
6. Per-URL retries alone do not satisfy this control for a long-running source task; a file/probe operation must also have bounded outer retry batches.
7. The retry control must have regression coverage that simulates transient failure followed by recovery without real network access.
8. When the provider has migrated its current public historical-data path, use that provider-native path before repeatedly hammering a degraded legacy host; preserve legacy cache compatibility and the same provider/source class.
9. Compact provider responses must not introduce synthetic bars when the frozen research contract forbids forward fill or interpolation.

**Escalation**

Occurrence 3 reached `CONTROL_REQUIRED`. HYP-0003 therefore added a concrete per-object retry-batch control and deterministic unit test. Occurrence 4 strengthened the control with explicit OS/socket exception normalization. Occurrence 5 keeps `REPEAT_AFTER_CONTROL_THRESHOLD` and removes the metadata single point of failure with two HistoryStart endpoints plus the provider-native instruments metadata fallback. Occurrence 6 confirms the upstream network class remains recurring; the fallback `403` is tracked under `LCI-012`. Occurrence 7 strengthens full development acquisition with the current Dukascopy Jetta H1 monthly path plus legacy BI5 cache/fallback, without changing provider, period, universe or information boundary.

**Scope:** OWNER research workflow and agents.

### LCI-011 — Monthly content URLs are unsuitable for discovering history inception

**First observed:** 2026-09-23 on `338ad44867d9ae68e11eb613a96b92101a5ac853`  
**Class:** `DATA_SOURCE_DISCOVERY_PROTOCOL`

**Symptom**

Repository validator, pinned Ruff, 146/146 pytest and full Local CI all pass. The RF-006 source probe then repeatedly receives `HTTP 503` from both Dukascopy content endpoints for the same old monthly object while trying to binary-search the first available H1 month.

**Root cause**

The retry/network control is functioning, but the discovery protocol is wrong for this question. A historical content URL is optimized for retrieving a known source object, not for proving the provider's first-ever H1 month. Persistent 5xx responses on an arbitrary pre-inception/old month are not a reliable `available / unavailable` signal.

Dukascopy exposes dedicated history-start metadata and the JForex `IDataService.getTimeOfFirstCandle` concept for first-available history.

**Correct response**

Do not increase retry counts and do not change the strategy/data provider. Replace binary search across old content URLs with the dedicated `metadata/HistoryStart.bi5` source for H1 start timestamps. Keep actual monthly BID/ASK content probes only for the required development boundary and later full-data acquisition.

**Preventive rule**

1. Use metadata/catalog endpoints for source-discovery questions when the provider exposes them.
2. Use content URLs to retrieve known required objects, not to infer provider inception through repeated missing/old requests.
3. Cache the metadata object and bind it by SHA-256.
4. Preserve the existing retry/backoff control for real metadata/content network failures.
5. A discovery-protocol correction before any strategy result does not authorize changing HYP-0003 parameters or protected evidence boundaries.

**Scope:** research/development tooling and agents.

### LCI-012 — Dukascopy freeserv metadata requires request Referer

**First observed:** 2026-09-23 on `1b45022b8d57e8140016f8448a63e0a182697bcc`  
**Class:** `DATA_SOURCE_REQUEST_PROTOCOL`

**Symptom**

Repository validator, pinned Ruff, 148/148 pytest and full Local CI pass. Both HistoryStart endpoints are unavailable, then the provider-native `common/instruments` fallback returns `HTTP 403` on every bounded retry.

**Root cause**

The public Dukascopy freeserv instruments endpoint requires the request context used by its chart client: `Referer: https://freeserv.dukascopy.com/`. RF-006 sent only `User-Agent` and `Accept`, so the valid fallback request was rejected before its JSONP payload could be parsed.

**Correct response**

Keep the same provider, candidate universe and protected period. Send the required Referer only for freeserv requests, preserve all existing timeout/retry behavior, and regression-test the exact header passed through `fetch_bytes()`.

**Preventive rule**

1. Provider-native fallback endpoints must reproduce required public client request headers when those headers are part of the endpoint contract.
2. A deterministic authorization/context response such as `403` must not be interpreted as source absence.
3. Header fixes must be endpoint-scoped; do not add unrelated browser headers to all historical-data requests.
4. The fallback request contract must have a network-free regression test that inspects the constructed request.
5. A request-protocol correction does not authorize changing the frozen provider, universe, development period or information boundary.

**Scope:** research/development tooling and agents.

### LCI-009 — Ruff import-order lint failure after remote Python authoring

**First observed:** 2026-09-22 on `213fb1116e7ca2fc866fc7281b57215d3908cb64` in `tools/hyp0002_proto01.py`  
**Class:** `LINT`

**Symptom**

Repository validator and `ruff format --check` pass, but pinned Ruff lint fails with `I001 Import block is un-sorted or un-formatted`.

The observed exact diff removed the blank line between:

`import yaml`

and:

`from proto01_eurusd import ...`

**Root cause**

The remote authoring preflight tracked formatting risk but did not independently track lint/import-order risk. Under the current `pyproject.toml`, Ruff selects `I` and no explicit first-party classification is configured for sibling modules under `tools/`. Ruff therefore classified the observed sibling-tool import in the same import section as the installed dependency import.

**Correct response**

Apply the exact pinned-Ruff import diff and do not change runtime/research logic. Rerun the launcher on the corrected exact HEAD.

**Preventive rule**

1. Ruff lint and Ruff format are separate pre-launch statuses.
2. If pinned Ruff has not run on exact proposed Python content, both statuses remain unverified.
3. Every new or materially rewritten Python import block receives an explicit import-grouping audit when Ruff `I` rules are enabled.
4. Under the current configuration, do not invent a first-party separator for sibling `tools/` modules unless Ruff configuration explicitly defines that classification.
5. An import-only lint failure must never trigger research-logic changes.

**Scope:** agents and any tooling that writes Python through remote repository APIs.

### LCI-010 — Tool imports under script context but not pytest package context

**First observed:** 2026-09-22 on `199e81861b6aab5c5844a76cadfb183f4fc693a8`  
**Class:** `TEST_IMPORT`

**Symptom**

Fast validator, Ruff lint and Ruff format all pass. Full pytest then fails during collection before any test runs:

`ModuleNotFoundError: No module named 'proto01_eurusd'`

The test imports `tools.hyp0002_proto01`, while that module used a script-context sibling import:

`from proto01_eurusd import ...`

**Root cause**

A Python tool was authored to run correctly as `python tools/file.py` but was not import-safe under the namespace used by pytest. Syntax compilation and Ruff do not execute imports, so the defect escaped the previous pre-push checks.

**Correct response**

Do not change the frozen research protocol. Remove the script-only sibling import from the runner and make the trivial file/time helpers self-contained. Verify the module can be imported as `tools.hyp0002_proto01`.

**Preventive rule**

1. New Python tools that tests import must be importable in the exact pytest namespace/context.
2. Do not rely on script-directory-only imports for such tools.
3. Fast Local CI must run `pytest --collect-only -q` so collection/import failures stop before the full suite.
4. Agent pre-push checks for new Python tools must include an actual import smoke, not only syntax compilation.
5. Import-context fixes must not alter frozen research parameters or outcome rules.

**Scope:** agents and research/development tooling.

### LCI-008 — Serialized row passed to typed continuity helper

**First observed:** 2026-09-22 on `04aaa885e5be81f2468b1478423949f0e9e5323b` during HYP-0002 Data Feasibility preparation  
**Class:** `TEST`

**Symptom**

Fast/full Local CI, pinned Ruff and the existing pytest suite pass, but the task-specific preparation step fails after data acquisition with:

`TypeError: unsupported operand type(s) for -: 'str' and 'str'`

The failure occurs while counting eligible 24-before/24-after windows.

**Root cause**

The first occurrence: the confirmatory preparation path stores `event_time` as RFC3339 strings for deterministic CSV/report serialization. It then reused `valid_window()` from PROTO-01, whose contract assumes already parsed rows where `event_time` is a `datetime`. The shared algorithm was compatible, but the row representation was not.

The second occurrence: an RF-008 network-free Jetta-preference test called cache-aware production code without replacing its real cache-path helpers. Because the OWNER host already had a valid legacy BI5 object from earlier probes, the code correctly chose the frozen local cache before the mocked Jetta network path. The test therefore depended on external filesystem state and asserted the wrong branch for that environment.

**Correct response**

Do not change the frozen dataset, Hypothesis, provider, cache-first production behavior or information boundary. For representation failures, parse event timestamps once and apply continuity checks to the parsed timestamp sequence. For cache-aware unit tests, replace both Jetta and legacy cache-path helpers with isolated `tmp_path` locations so the test explicitly controls whether cache files exist.

**Preventive rule**

1. Treat serialized rows and typed in-memory rows as distinct contracts.
2. A helper reused across those boundaries must receive explicitly converted inputs or expose a representation-neutral primitive.
3. Task-runtime paths that transform representation must have a direct regression test; broad platform tests are not sufficient.
4. Network-free tests for cache-aware code must isolate filesystem/cache paths under `tmp_path`; they must not inherit the OWNER's real `data/external/` cache.
5. A test for "network/provider preference when cache is absent" must make both candidate cache paths explicitly absent before asserting which provider function runs.
6. Do not repair a test-contract bug by changing research parameters, provider selection or production cache-first semantics.

**Scope:** research/development tooling.

### LCI-006 — Canonical state/handoff reconciliation drift

**First observed:** 2026-09-22 on `2048d3c9cd7162e3e71429331bd2b5979534b1d6`  
**Class:** `HANDOFF_SYNC`

**Symptom**

Repository validator reports:

`AI_HANDOFF.md missing last_completed_artifact`

even though the handoff narratively describes the previous completed task.

**Root cause**

The canonical state contained:

`last_completed_artifact: "governance/methodology/MULTIPLE_RESEARCH_ACCOUNTING.md"`

but the synchronized handoff rewrite removed that exact artifact path. ATS reconciliation is intentionally literal for canonical identities; a prose summary is not a substitute for the canonical reference.

**Correct response**

Restore the exact canonical artifact reference in `AI_HANDOFF.md` without changing task scope, then rerun the launcher on the corrected exact commit.

**Preventive rule**

Before every remote program-state commit, mechanically compare these exact canonical-state values against both handoff surfaces:

1. `last_completed_artifact` must appear in `AI_HANDOFF.md`;
2. `next_artifact` must appear in `AI_HANDOFF.md` and `02_СЛЕДУЮЩИЙ_ШАГ.md`;
3. `next_task_id` must appear in `AI_HANDOFF.md` and `02_СЛЕДУЮЩИЙ_ШАГ.md`.

Do not accept semantic or narrative equivalence for stable IDs/paths.

**Scope:** agents performing program-state/handoff synchronization.

### LCI-005 — Runtime artifact makes Local CI tree dirty

Historical validator marker retained for compatibility: `Windows shortcut artifact makes Local CI tree dirty`.

**First observed:** 2026-09-21 on `01603925a5c3d690e5e6cbfbcbaedc40e42a76e8`  
**Repeat observed:** 2026-09-22 on `4f51123578b7d790fce98ef329da512286fe6649`, when the successful first discovery run wrote two unignored `SEARCH-*` files before the full gate  
**Class:** `DIRTY_TREE`

**Symptom**

Repository validation passes, but Full Local CI stops before Ruff/pytest because `git status --porcelain` reports an untracked Windows shortcut such as:

`reports/local_ci/ATS_TASK_CHECK.bat - ... .lnk`

The shortcut is not ATS source, research evidence or a required runtime report.

**Root cause**

`reports/local_ci/` intentionally contains disposable runtime outputs, but the ignore policy was enumerated file-by-file. The first occurrence was a Windows shortcut; the second was caused by the M6 discovery runner creating its machine result and text report before the full clean-tree gate. Those new generated filenames were not yet covered by `.gitignore`.

**Correct response**

Do not change research logic. Add only narrow ignore patterns for the confirmed disposable runtime artifact class:

- `reports/local_ci/SEARCH-*-result.json`;
- `reports/local_ci/SEARCH-*-report.txt`;
- existing Windows shortcut handling remains `reports/local_ci/*.lnk`.

Do not ignore all of `reports/local_ci/` and do not globally ignore broad file types. The ignore rules remain narrowly scoped.

**Preventive rule**

1. Every task runner that writes local files before the full gate must declare its output paths during implementation.
2. Before activating that runner in `tools/current_task_check.py`, ensure each disposable output has a narrow `.gitignore` pattern.
3. Unknown/unexpected untracked files must remain blocking.
4. Runtime-output documentation must list the intended ignored patterns.
5. When a dirty-tree failure occurs, inspect the exact `git status --porcelain` entries before deleting files or changing source code.

**Scope:** OWNER Windows workflow and agents.


## 5. Adding future lessons

Add a new entry only when all are true:

1. the failure class is known;
2. the root cause is supported by the report or reproduction;
3. the corrective action is known;
4. there is a concrete rule that can reduce recurrence or misdiagnosis.

If the same failure class repeats without a new lesson, update the existing entry only when the preventive rule itself improves.

## 6. Relationship to completion

This troubleshooting registry does not replace the Local CI Gate.

The completion evidence remains a fresh `ATS_TASK_CHECK.bat` PASS on the exact HEAD being closed. A documented lesson explains how to handle failures; it does not waive any gate.
