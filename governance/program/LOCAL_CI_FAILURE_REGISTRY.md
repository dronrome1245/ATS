# ATS Local CI Failure Registry

**Status:** ACTIVE  
**Purpose:** count repeated Local CI failure causes and convert recurrence into mandatory preventive controls.  
**Canonical lessons:** `governance/program/LOCAL_CI_TROUBLESHOOTING.md`

## 1. Escalation policy

Every confirmed failure occurrence is assigned to one stable `LCI-###` cause.

- occurrence 1 → `OBSERVED`: record the cause and correct response;
- occurrence 2 → `RECURRING`: preventive rule becomes mandatory;
- occurrence 3 → `CONTROL_REQUIRED`: prose is insufficient; add a technical/process control;
- occurrence 4+ → `REPEAT_AFTER_CONTROL_THRESHOLD`: do not treat the event as isolated; strengthen or verify the control before normal progression.

A new occurrence increments the existing cause. Do not create a new ID merely because the affected file/task changed.

## 2. Cause summary

| Cause | Class | Confirmed occurrences | State | Current control |
|---|---|---:|---|---|
| `LCI-001` | `SYNC_NETWORK` | 1 | OBSERVED | classify before source changes |
| `LCI-002` | `FORMAT` | 14 | REPEAT_AFTER_CONTROL_THRESHOLD | fast Local CI preflight before full task check; exact Ruff diff is authoritative; remote Python commits remain format-unverified until pinned Ruff runs |
| `LCI-003` | `ENVIRONMENT` | 1 | OBSERVED | pinned uv/Python bootstrap procedure |
| `LCI-004` | `VALIDATOR` | 4 | REPEAT_AFTER_CONTROL_THRESHOLD | extract and audit the complete current marker tuple for every changed validator-targeted file |
| `LCI-005` | `DIRTY_TREE` | 2 | RECURRING | narrow ignore patterns for known `reports/local_ci/` runtime outputs; task-runner outputs must be covered before closure |
| `LCI-006` | `HANDOFF_SYNC` | 1 | OBSERVED | exact canonical `last_completed_artifact`/`next_artifact`/`next_task_id` values must appear in handoff/next-step |
| `LCI-007` | `DATA_SOURCE_NETWORK` | 7 | REPEAT_AFTER_CONTROL_THRESHOLD | cache + current Dukascopy Jetta H1 path + legacy BI5 fallback + metadata fallback + retry batches; normalize direct OSError/socket resets |
| `LCI-008` | `TEST` | 1 | OBSERVED | regression-test serialized event-time rows against typed continuity logic used by task preparation |
| `LCI-009` | `LINT` | 1 | OBSERVED | track Ruff lint and format separately; inspect import grouping for every new/rewritten Python import block |
| `LCI-010` | `TEST_IMPORT` | 1 | OBSERVED | fast pytest collection plus same-context import smoke for new Python tools; avoid script-only sibling imports |
| `LCI-011` | `DATA_SOURCE_DISCOVERY_PROTOCOL` | 1 | OBSERVED | use Dukascopy HistoryStart metadata for first H1 availability; content URLs only verify required boundary data |
| `LCI-012` | `DATA_SOURCE_REQUEST_PROTOCOL` | 1 | OBSERVED | send the provider-required freeserv Referer and regression-test the constructed request |

## 3. Occurrence log

| Date | Cause | Commit/context | Stage | Short symptom |
|---|---|---|---|---|
| 2026-09-18 | `LCI-001` | network context | sync | `git pull --ff-only` could not reach GitHub |
| 2026-09-18 | `LCI-002` | `b3085c26342c52e6ae852962faefcaf347d43a2a` | format | Ruff wanted canonical Python formatting |
| 2026-09-19 | `LCI-003` | new Windows host | environment | `uv` missing from PATH |
| 2026-09-21 | `LCI-004` | `e4f397b4a985be314c75e4385d59030e77fcbfcd` | validator | Markdown/presentation-sensitive marker drift |
| 2026-09-21 | `LCI-002` | `c8a0225acafba15d59dcd35d5bf3aceee716ced3` | format | remote Python edit not Ruff-formatted |
| 2026-09-21 | `LCI-004` | `c8a0225acafba15d59dcd35d5bf3aceee716ced3` | validator | selective marker audit missed declared markers |
| 2026-09-21 | `LCI-004` | `0c9823fe48c1e562d516ac311d956893afdec44f` | validator | transition changed WBS wording but validator expected old marker |
| 2026-09-21 | `LCI-005` | `01603925a5c3d690e5e6cbfbcbaedc40e42a76e8` | clean tree | Windows `.lnk` appeared under local reports |
| 2026-09-21 | `LCI-002` | `cd348024bd907225ea15219786ef5ad54ebdea1d` | format | sensitivity/checker needed Ruff canonical layout |
| 2026-09-21 | `LCI-002` | `9f912b7b5e350d287ed76ce4bffe7a67722faf58` | format | slicing module needed Ruff canonical layout |
| 2026-09-22 | `LCI-002` | `9fb041c51cf93071ca6735b52897cbb2b24e5568` | format | concentration module was stopped by fast preflight before full pytest |
| 2026-09-22 | `LCI-002` | `9134c44d1d3d861124c44e00b4df820ad181cb5d` | format | resampling test was stopped by fast preflight before full pytest |
| 2026-09-22 | `LCI-002` | `f989e6d77c94aaaa93df9bf6fdd994708b570404` | format | independent-exam checker tuple layout was stopped by fast preflight before full pytest |
| 2026-09-22 | `LCI-002` | `2048d3c9cd7162e3e71429331bd2b5979534b1d6` | format | M4-008 checker repeated the same one-element tuple layout failure; fast preflight stopped before full pytest |
| 2026-09-22 | `LCI-006` | `2048d3c9cd7162e3e71429331bd2b5979534b1d6` | validator | AI handoff omitted the exact canonical `last_completed_artifact` path |
| 2026-09-22 | `LCI-002` | `feb146aa0a65b3909b13efabbfe2c9097c0b74c0` | format | Ruff preferred the one-line contiguous-hour comparison in `src/ats/discovery/eurusd_h1.py`; fast preflight stopped before discovery execution |
| 2026-09-22 | `LCI-005` | `4f51123578b7d790fce98ef329da512286fe6649` | clean tree | successful discovery run created two unignored `reports/local_ci/SEARCH-*` runtime files before full gate |
| 2026-09-22 | `LCI-004` | `5beb1e5060e0d92427f7971759215f0916e90b7d` | validator | manual marker audit omitted the existing `Windows shortcut artifact makes Local CI tree dirty` literal after the troubleshooting heading was renamed |
| 2026-09-22 | `LCI-002` | `cf7f97c0263fa6b546911aaadcea748727e8afca` | format | HYP-0002 feasibility tool used multiline forms that Ruff canonicalized to one-line string assignment and compact set comprehensions |
| 2026-09-22 | `LCI-007` | `2545491d35a980e8c375100b9c8f8d99ee44f41e` | data acquisition | Dukascopy ASK 2026-05 returned repeated HTTP 503/connection reset; rerun later progressed past that file |
| 2026-09-22 | `LCI-007` | `2545491d35a980e8c375100b9c8f8d99ee44f41e` | data acquisition | subsequent resume reached BID 2026-06 but again hit repeated HTTP 503/timeout |
| 2026-09-23 | `LCI-007` | `b82e827c0c8510a38aac3179411b3b2a8d455310` | source probe | AUDUSD historical-availability probe hit repeated WinError 10054/10060 after per-URL retries; full CI had already passed |
| 2026-09-23 | `LCI-007` | `0988069a525a7cd0d8acb48a3d9ed34d3ceb0332` | source probe | outer 5/15/30-second retry batches ran, but final Windows connection reset escaped as raw OSError instead of retryable ProbeError |
| 2026-09-23 | `LCI-011` | `338ad44867d9ae68e11eb613a96b92101a5ac853` | source discovery | retry/fallback control worked, but binary-searching old monthly URLs hit persistent HTTP 503 for AUDUSD 1997-11 ASK on both endpoints |
| 2026-09-23 | `LCI-007` | `7dec11ceb34c456a6c2f6b93833eeb02b2f0e804` | metadata acquisition | HistoryStart metadata timed out after all retry batches; the metadata path had no alternate provider-native source |
| 2026-09-23 | `LCI-007` | `1b45022b8d57e8140016f8448a63e0a182697bcc` | metadata acquisition | HistoryStart again failed after bounded endpoint retries before fallback |
| 2026-09-23 | `LCI-007` | `d33e3112c7e6734bba8dfbc664c4c8498ed11650` | development data acquisition | legacy GBPUSD 2003-08 BID paths exhausted bounded retries with datafeed timeout and www HTTP 503; current Dukascopy tooling uses the provider-native Jetta H1 API instead |
| 2026-09-23 | `LCI-012` | `1b45022b8d57e8140016f8448a63e0a182697bcc` | metadata fallback | public instruments fallback returned HTTP 403 because the request omitted the required freeserv Referer |
| 2026-09-22 | `LCI-008` | `04aaa885e5be81f2468b1478423949f0e9e5323b` | task runtime | confirmatory rows stored RFC3339 event-time strings but `valid_window` expected datetime-valued rows, causing string subtraction after acquisition completed |
| 2026-09-22 | `LCI-002` | `7c8e82e7f29b0bc3e09de557f88dd1c14441474f` | format | Ruff compacted generator expressions in `valid_timestamp_window` and confirmatory eligible-count calculation |
| 2026-09-23 | `LCI-002` | `8a8e331f949e8084c17beef23b636e25a5dbf84b` | format | RF-007 checker used multiline parenthesized hash literals that pinned Ruff canonicalized to one-line assignments |
| 2026-09-23 | `LCI-002` | `9665c81bdd6f2a6eb98e69d4b518be6854224966` | format | RF-008 fast preflight requested pinned Ruff canonical layout in the new development-data runner, checker and synthetic tests before acquisition began |
| 2026-09-23 | `LCI-002` | `cd864887ae81c8628042d1f268844d22117a6fb9` | format | second RF-008 fast preflight exposed one remaining multiline exception raise in `tools/hyp0003_development_data.py`; exact Ruff diff requested one-line canonical form |
| 2026-09-22 | `LCI-009` | `213fb1116e7ca2fc866fc7281b57215d3908cb64` | lint | Ruff I001 rejected a blank line between `import yaml` and sibling-tool import `from proto01_eurusd ...`; format itself passed |
| 2026-09-22 | `LCI-010` | `199e81861b6aab5c5844a76cadfb183f4fc693a8` | pytest collection | `tools.hyp0002_proto01` imported a sibling tool with script-only `from proto01_eurusd ...`, causing ModuleNotFoundError when pytest imported it as `tools.*` |

## 4. Rule-conversion discipline

When a cause reaches `RECURRING`, update its lesson with a mandatory preventive rule.

When a cause reaches `CONTROL_REQUIRED`, add a concrete control in code, validator, launcher or workflow. A statement such as "be more careful" is not a control.

After a control is added, the next exact-commit PASS is evidence that the control did not break the workflow; future recurrences determine whether the control must be strengthened.

## 5. Current technical controls

Shared agent-side prevention is defined in `governance/program/AGENT_PRE_PUSH_CHECKLIST.md` and is mandatory before material remote repository writes.

### FORMAT / LCI-002

The Windows launcher runs a fast Local CI preflight before the full current-task check. The fast gate includes repository validation, Ruff lint and Ruff format, but skips full pytest/fingerprint. A format failure therefore stops before the expensive full test suite.

This does not replace the final full gate. Task completion still requires `ATS TASK LAUNCHER: PASS`.

### VALIDATOR / LCI-004

Validator-targeted files require complete marker audit. The audit source is the actual current `CONTENT_MARKERS` tuple in `tools/validate_repo.py`; hand-maintained subsets are not accepted.

### DIRTY_TREE / LCI-005

Known disposable runtime outputs under `reports/local_ci/` use narrow ignore patterns. Existing Windows shortcut handling remains `reports/local_ci/*.lnk`. Bounded discovery uses `reports/local_ci/SEARCH-*-result.json` and `reports/local_ci/SEARCH-*-report.txt`.

These patterns are narrowly scoped; real untracked source files and unknown runtime filenames remain blocking.

Any task runner that writes local output before the full clean-tree gate must have its output pattern covered before the runner is activated in `tools/current_task_check.py`.

### HANDOFF_SYNC / LCI-006

Before remote push, canonical state reconciliation must compare the exact values of `last_completed_artifact`, `next_artifact`, and `next_task_id` against `AI_HANDOFF.md` and `02_СЛЕДУЮЩИЙ_ШАГ.md`. Narrative equivalence is not enough.

### DATA_SOURCE_NETWORK / LCI-007

External historical-data acquisition must be resumable. Successfully downloaded source files remain cached; transient 5xx/timeouts on one month/side receive bounded additional download batches with backoff. At occurrence 3, the control became mandatory in code: source-probe/download operations use an outer per-object retry batch in addition to any per-URL retry loop. Occurrence 4 showed that platform-level socket/OSError exceptions must also be normalized into the retryable source-error class so they cannot bypass fallback endpoints or the outer batch. Occurrence 5 showed that provider metadata discovery also needs a fallback path: HistoryStart uses both Dukascopy historical-data endpoints first, then the public instruments metadata `history_start_60min` field. Occurrence 7 showed that the legacy BI5 content hosts can remain unavailable after bounded retries while current Dukascopy tooling has moved H1 candles to the provider-native `jetta.dukascopy.com/v1` monthly API. RF-008 therefore tries Jetta first and preserves legacy BI5 as cache-compatible fallback. A source-network failure does not change the frozen data period, provider or hypothesis.

### TEST / LCI-008

Task-specific preparation code must test representation boundaries explicitly. Serialized RFC3339 row values and typed datetime row values are separate contracts; continuity helpers must consume the representation they declare. A regression test must cover the same serialized row shape produced by the preparation path.

### LINT / LCI-009

Remote Python preflight must treat Ruff lint and Ruff format as separate gates. The current `pyproject.toml` selects Ruff `I`, so import grouping/order is a blocking invariant even when `ruff format --check` would pass. For new or rewritten files under `tools/`, sibling-tool imports must be grouped exactly as pinned Ruff classifies them; do not insert a first-party separator unless the Ruff configuration explicitly defines that module as first-party.

### TEST_IMPORT / LCI-010

Fast Local CI now runs `pytest --collect-only -q` after validator/Ruff checks. New tools imported by tests must be importable under the same namespace/context used by pytest. Script-only sibling imports under `tools/` are prohibited for modules that tests import as `tools.<module>`; prefer self-contained helpers or a proper package-level dependency.


## 6. Verified control run

The fast-preflight control introduced for recurrent `LCI-002` was verified on exact commit:

`cac82301e61a126919d70ffede595bb7cf671f4b`

Observed sequence:

1. fast Local CI preflight PASS;
2. pinned Ruff format PASS;
3. full pytest: 105 passed;
4. full Local CI PASS;
5. ATS task launcher PASS.

This confirms the control is active and does not replace the final full gate.


## 7. Post-threshold rule for remote Python edits

### FORMAT / LCI-002 — post-threshold rule

The fast preflight is confirmed useful: on the fifth occurrence it stopped the workflow before full pytest. However, detection is not prevention.

Because the remote authoring environment does not have the project-pinned Ruff executable, any commit containing remotely authored Python must be treated as:

`FORMAT_UNVERIFIED_UNTIL_PINNED_RUFF`

until the OWNER fast preflight runs.

Rules:

1. never describe remote Python formatting as verified without pinned Ruff output;
2. if fast preflight returns a Ruff diff, apply that exact diff only and increment this registry;
3. do not run or request the expensive full task check separately after a fast-preflight format failure; fix format first;
4. repeated FORMAT events after this threshold remain the same `LCI-002` cause and must not receive new IDs;
5. if a future environment gains the exact pinned Ruff version, running it before push becomes mandatory and replaces this limitation.


## 8. Resolution evidence — LCI-002 occurrence 5

Failed commit:

`9fb041c51cf93071ca6735b52897cbb2b24e5568`

Failure:

`ruff format --check` requested canonical formatting changes only in:

`src/ats/validation/concentration.py`

Applied resolution:

1. use the exact Ruff-provided layout;
2. do not change concentration-analysis logic;
3. rerun the OWNER launcher on the new exact commit;
4. require both fast-preflight PASS and final full-gate PASS.

Resolved commit:

`3a0dc9af4cc2191cc98c65b190b6f1f1c5cb1ea3`

Verified result:

- fast Local CI preflight: `PASS`;
- pinned Ruff lint: `PASS`;
- pinned Ruff format: `PASS`;
- pytest: `115 passed`;
- environment fingerprint: `PASS`;
- full ATS Local CI: `PASS`;
- current task check: `PASS`;
- ATS task launcher: `PASS`;
- working tree: `CLEAN`.

**Reusable resolution rule:** when `LCI-002` is caused only by Ruff formatting, apply the exact Ruff diff without changing logic, then require a fresh exact-commit launcher PASS. Do not invent an alternative manual layout.


## 9. Resolution evidence — LCI-002 occurrence 6

Failed commit:

`9134c44d1d3d861124c44e00b4df820ad181cb5d`

Failure:

`ruff format --check` requested one canonical formatting change only in:

`tests/test_validation_resampling.py`

Applied resolution:

1. apply the exact Ruff-provided comprehension layout;
2. do not change test semantics or resampling logic;
3. keep `LCI-002` as the same recurring cause;
4. require a fresh OWNER launcher PASS on the corrected exact commit.

Resolved commit:

`6d452c4f340825eaa39b8e28dad3f6691332b217`

Verified result:

- fast Local CI preflight: `PASS`;
- pinned Ruff lint: `PASS`;
- pinned Ruff format: `PASS`;
- pytest: `124 passed`;
- environment fingerprint: `PASS`;
- full ATS Local CI: `PASS`;
- current task check: `PASS`;
- ATS task launcher: `PASS`;
- working tree: `CLEAN`.

**Reusable resolution rule remains unchanged:** exact Ruff diff is authoritative for format-only failures; apply it without logic changes, then verify the corrected exact commit through fast preflight and the full launcher.


## 10. Resolution evidence — LCI-002 occurrence 7

Failed commit:

`f989e6d77c94aaaa93df9bf6fdd994708b570404`

Failure:

`ruff format --check` requested one canonical formatting change only in:

`tools/current_task_check.py`

Applied resolution:

1. apply the exact Ruff-provided one-line tuple layout;
2. do not change checker semantics or task scope;
3. keep `LCI-002` as the same recurring cause;
4. require a fresh OWNER launcher PASS on the corrected exact commit.

Resolved commit:

`4d4f5546c54bc1b8985f37dd63c251b87517245e`

Verified result:

- fast Local CI preflight: `PASS`;
- pinned Ruff lint: `PASS`;
- pinned Ruff format: `PASS`;
- pytest: `124 passed`;
- environment fingerprint: `PASS`;
- full ATS Local CI: `PASS`;
- current task check: `PASS`;
- ATS task launcher: `PASS`;
- working tree: `CLEAN`.

**Reusable resolution rule remains unchanged:** exact Ruff diff is authoritative for format-only failures; apply it without logic changes, then verify the corrected exact commit through fast preflight and the full launcher.
