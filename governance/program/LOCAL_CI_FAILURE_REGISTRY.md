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
| `LCI-002` | `FORMAT` | 9 | REPEAT_AFTER_CONTROL_THRESHOLD | fast Local CI preflight before full task check; exact Ruff diff is authoritative; remote Python commits remain format-unverified until pinned Ruff runs |
| `LCI-003` | `ENVIRONMENT` | 1 | OBSERVED | pinned uv/Python bootstrap procedure |
| `LCI-004` | `VALIDATOR` | 3 | CONTROL_REQUIRED | marker audit rule for every changed validator-targeted file |
| `LCI-005` | `DIRTY_TREE` | 1 | OBSERVED | narrowly ignore `reports/local_ci/*.lnk` |
| `LCI-006` | `HANDOFF_SYNC` | 1 | OBSERVED | exact canonical `last_completed_artifact`/`next_artifact`/`next_task_id` values must appear in handoff/next-step |

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

Validator-targeted files require complete marker audit, not a selected subset.

### DIRTY_TREE / LCI-005

Only `reports/local_ci/*.lnk` is ignored for Windows shell shortcuts; real untracked source files remain blocking.

### HANDOFF_SYNC / LCI-006

Before remote push, canonical state reconciliation must compare the exact values of `last_completed_artifact`, `next_artifact`, and `next_task_id` against `AI_HANDOFF.md` and `02_СЛЕДУЮЩИЙ_ШАГ.md`. Narrative equivalence is not enough.


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
