# ATS Program Backlog v2

**Программа:** ATS — Algorithmic Trading Systems  
**Версия:** 2.0  
**Статус:** BASELINE  
**Дата:** 18 сентября 2026 года  
**WBS:** `governance/program/PROGRAM_WBS_V2.md`  
**Repository Structure:** `governance/program/REPOSITORY_STRUCTURE_V2.md`

## 1. Назначение

Backlog превращает Program WBS в исполнимую очередь работ. Material program task не считается завершённой до синхронизации state/status/next-step/handoff и полного локального quality gate. На Windows стандартный OWNER workflow — `ATS_TASK_CHECK.bat`, который формирует `reports/local_ci/CURRENT_TASK_REPORT.txt`. GitHub Actions не является completion gate.

## 2. Текущая execution queue

1. `ATS2-M0-013` — M0 Exit Review — `DONE`.
2. `ATS2-M1-001…011` — M1 Research Methodology — `DONE / PASS`.
3. `ATS2-M2-000` — Reference Consumer Profile — `DONE`.
4. `ATS2-M2-001` — Research stack ADR — `DONE`.
5. `ATS2-M2-002` — Reproducible environment — `DONE`.
6. `ATS2-M2-003` — Dataset manifest support — `DONE`.
7. `ATS2-M2-004` — Base data loader — `DONE`.
8. `ATS2-M2-005` — Minimal Strategy research interface — `DONE`.
9. `ATS2-M2-006` — Deterministic backtest/replay — `DONE`.
10. `ATS2-M2-007` — Cost model interface — `DONE`.
11. `ATS2-M2-008` — Standard analytics/report — `DONE`.
12. `ATS2-M2-009` — Manifest-driven experiment runner — `DONE`.
13. `ATS2-M2-010` — Research platform tests — `DONE`.
14. `ATS2-M2-011` — M2 Exit — `DONE / PASS`.
15. `ATS2-M3-001` — Select Reference Strategy #1 — `DONE`.
16. `ATS2-M3-002` — Idea & rationale — `DONE`.
17. `ATS2-M3-003` — Data feasibility — `DONE / CONDITIONAL`.
18. `ATS2-M3-004` — Cheap prototype — `DONE / REJECT`.
19. `ATS2-M3-005` — M3 early-rejection closeout / platform learning review — `DONE / PASS`.
20. `ATS2-M4-001` — Validation protocol framework — `DONE`.
21. `ATS2-M4-002` — Parameter sensitivity tooling — `DONE`.
22. `ATS2-M4-003` — Time/regime slicing — `DONE`.
23. `ATS2-M4-004` — Observation concentration analysis — `DONE`.
24. `ATS2-M4-005` — Dependence-preserving resampling framework — `DONE`.
25. `ATS2-M4-006` — Independent exam protocol — `DONE`.
26. `ATS2-M4-007` — Multiple-research accounting — `DONE`.
27. `ATS2-M4-008` — Technical strategy validation profile — `DONE`.
28. `ATS2-M6-000` — Market Pattern Discovery capability — `DONE`.
29. `ATS2-M6-001` — First bounded discovery run — `DONE`.
30. `ATS2-M6-002` — Strategy #2 class selection and Idea intake — `DONE`.
31. `ATS2-M6-003` — HYP-0002 formation — `DONE`.
32. `ATS2-M6-004` — HYP-0002 Data Feasibility preparation — `DONE`.
33. `ATS2-M6-005` — HYP-0002 Data Feasibility freeze — `DONE`.
34. `ATS2-M6-006` — HYP-0002 PROTO-01 freeze — `DONE`.
35. `ATS2-M6-007` — HYP-0002 PROTO-01 reveal — `DONE`.
36. `ATS2-M6-008` — Reference Strategy #2 early-rejection closeout — `DONE`.
37. `ATS2-M6-009` — M6 Exit Review — `DONE / PASS`.
38. `ATS2-RF-001` — Strategy #3 sourcing rebaseline — `DONE`.
39. `ATS2-RF-002` — Strategy #3 idea sourcing — `DONE`.
40. `ATS2-RF-003` — Strategy #3 family selection and Idea intake — `DONE`.
41. `ATS2-RF-004` — HYP-0003 formation — `DONE`.
42. `ATS2-RF-005` — HYP-0003 Data Feasibility — `DONE`.
43. `ATS2-RF-006` — HYP-0003 Data Feasibility preparation — `DONE`.
44. `ATS2-RF-007` — HYP-0003 Data Feasibility freeze — `DONE`.
45. `ATS2-RF-008` — HYP-0003 development data preparation — `DONE / PASS`.
46. `ATS2-RF-009` — HYP-0003 development data freeze — `DONE / PASS`.
47. `ATS2-RF-010` — HYP-0003 PROTO-01 freeze — `DONE / PASS`.
48. `ATS2-RF-011` — HYP-0003 PROTO-01 reveal — `DONE / PASS`.
49. `ATS2-RF-012` — Strategy #3 early-rejection closeout — `DONE / PASS`.
50. `ATS2-RF-013` — Strategy #4 idea sourcing — `DONE / PASS`.
51. `ATS2-RF-014` — Strategy #4 family selection and Idea intake — `DONE / PASS`.
52. `ATS2-RF-015` — HYP-0004 formation — `DONE / PASS`.
53. `ATS2-RF-016` — HYP-0004 Data Feasibility — `DONE / PASS`.
54. `ATS2-RF-017` — HYP-0004 development data preparation — `DONE / PASS`.
55. `ATS2-RF-018` — HYP-0004 development data freeze — `DONE / PASS`.
56. `ATS2-RF-019` — HYP-0004 PROTO-01 freeze — `DONE / PASS`.
57. `ATS2-RF-020` — HYP-0004 PROTO-01 reveal — `DONE / PASS`.
58. `ATS2-RF-021` — HYP-0004 PROTO-01 result canonicalization and routing — `DONE / PASS`.
59. `ATS2-RF-022` — HYP-0005 confirmatory hypothesis formation — `DONE / PASS`.
60. `ATS2-RF-023` — HYP-0005 confirmatory Data Feasibility preparation — `DONE / PASS`.
61. `ATS2-RF-024` — HYP-0005 confirmatory Data Feasibility freeze — `READY` after RF-023 exact-main PASS; conditional freeze staged pending exact-main gate.
62. `ATS2-RF-025` — Parallel Strategy #5 Idea Intake + HYP-0006 formation — `DONE / PASS`.
63. `ATS2-RF-026` — HYP-0006 Data Feasibility — `DONE / PASS`.
64. `ATS2-RF-027` — HYP-0006 Data Feasibility preparation with frozen local BLS + Dukascopy snapshots — `DONE / PASS`.
65. `ATS2-RF-028` — HYP-0006 pre-reveal data/tolerance freeze — `DONE / PASS`.
66. `ATS2-RF-029` — HYP-0006 PROTO-01 pre-reveal runner/decision freeze — `DONE / PASS`.
67. `ATS2-RF-030` — HYP-0006 PROTO-01 first development reveal gate — `DONE / PASS`.
68. `ATS2-RF-031` — HYP-0006 reveal canonicalization and HYP-0007 confirmatory structural hypothesis formation — `DONE / PASS`.
69. `ATS2-RF-032` — HYP-0005 RF-023 offline-only official snapshot source-input repair — `DONE / PASS`.
70. `ATS2-RF-033` — HYP-0005 September 2026 provenance Git hygiene and file-only intake identity check — `DONE / PASS`.
71. `ATS2-RF-034` — controlled offline RF-023 source/geometry preparation on frozen local BID/ASK — `DONE / PASS`.

Program-level current next task — `ATS2-RF-024` (HYP-0005 conditional confirmatory Data Feasibility dataset freeze; no hypothesis outcome).


RF-027 source architecture is now frozen to local official BLS schedule snapshots rather than live
BLS HTTP access.

Canonical inputs:

- `data/reference/HYP-0006-BLS-SCHEDULE-SNAPSHOT-MANIFEST.csv`;
- `data/raw/bls/hyp0006/schedules/YYYY.html` for 2003–2021.

Generated local event calendar:

`data/derived/HYP-0006-BLS-CPI-CALENDAR-2003-2021.csv`

Normal runtime live BLS access is prohibited.

Missing snapshot input is classified:

`OWNER_INPUT_REQUIRED_BLS_SCHEDULE_SNAPSHOTS`

and is not a HYP-0006 result.

The corrective offline-BLS architecture passed exact-head preflight and was merged to `main` at
`79a01623c3fef4deb3757e4d2940b8cd16b9bff3`.

OWNER snapshot intake is complete locally: all 19 canonical files for 2003–2021 are present under
`data/raw/bls/hyp0006/schedules/YYYY.html`, with content preserved during filename normalization.
Extra 2022–2025 pages are retained outside the canonical schedule directory.

An earlier exact-main RF-027 source-preparation run passed governance and full Local CI, built the local BLS CPI
calendar with `217` events and calendar SHA-256
`646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9`, then stopped on
Dukascopy tick acquisition for `2004-03-17T12:00:00Z` with HTTP 503.

This is `TECHNICAL_SOURCE_ACCESS_FAILURE`, not a HYP-0006 result. No geometry CSV or final RF-027
result JSON was emitted.

Repository-wide policy:

`FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF`

The policy correction passed exact-head preflight and was squash-merged to `main` at
`367976fa7510d0fe8c3662d5b33a9889fc824c94`.

After the first proven external HTTP/network/access failure, ATS must stop automatic retries,
alternate endpoints and fallbacks and report the blocker to OWNER. A new external attempt requires
explicit OWNER authorization.

A later offline inventory using the same calendar SHA-256 found `1085` unique required Dukascopy
hourly BI5 objects: `37` existed locally, `1048` were missing, duplicate required hours were
`0`, and the first inventory-time missing hour was `2004-03-17T13:00:00Z`.

OWNER authorized preparation, but not network execution, of a controlled preload tool:

`tools/hyp0006_dukascopy_controlled_download.py`

Merged preparation branch:

`agent/rf027-dukascopy-controlled-downloader`

The tool must default to zero-network inventory, require `--execute --owner-authorized` for a later
network run, use only the canonical `datafeed.dukascopy.com` endpoint, never overwrite existing
objects, validate new BI5 content before atomic promotion, and stop on the first HTTP/network/access
failure without retry or fallback.

The controlled downloader passed exact-head preflight, was squash-merged to `main`, and an
exact-main offline dry-run completed on:

`a638e49108e05e9618208ca577c6ebd0c74aa4e1`

Dry-run status:

`DRY_RUN_READY`

Observed values remained `217` events / `1085` required BI5 objects / `37` existing /
`1048` missing / `0` network requests, with the same BLS calendar SHA-256.

OWNER explicitly authorized one controlled execute-run on 2026-10-05.

Historical authorization:

`AUTHORIZED_ONCE_BY_OWNER_2026_10_05`

The exact-main run on
`f3151d8915b61d1a08e79cf27133764201475e65`
made exactly one canonical request, downloaded zero objects and stopped on HTTP 503 for
`2004-03-17T13:00:00Z`.

Controlled execution status:

`SOURCE_BLOCKED_AUTHORIZATION_CONSUMED`

Observed inventory remained `37` existing / `1048` missing after the run.

No retry or automatic alternate endpoint is authorized.

RF-027 now stages the preferred same-source recovery architecture:

`FROZEN_LOCAL_DUKASCOPY_BI5_SNAPSHOT_BUNDLE`

Normal RF-027 live Dukascopy network mode becomes:

`PROHIBITED`

Missing local BI5 inputs are classified:

`OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE`

Recovery review:

`research/reviews/HYP-0006-DUKASCOPY-SOURCE-RECOVERY.md`

The source-blocker/offline-runtime correction passed exact-head preflight and was squash-merged to
`main` at:

`953b405a63f8077411c817965f96cb9e3aee5d29`

Current gate is exact-main `.\ATS_TASK_CHECK.bat`. With the local BI5 bundle still incomplete,
normal RF-027 must remain offline and hand off
`OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE`.

This preserves `DUKASCOPY_HOURLY_TICK_BI5` semantics and does not compute a HYP-0006 outcome.

A bounded manual browser probe subsequently produced three supplied canonical BI5 files; all three
passed independent raw BI5 integrity checks.

OWNER then authorized one bounded browser-assisted intake pilot:

`OWNER_AUTHORIZED_BROWSER_PILOT_50_2026_10_05`

Frozen pilot scope:

- first `50` currently missing deterministic RF-027 BI5 objects;
- canonical Dukascopy URL only;
- at most `2` attempts per object;
- `SKIPPED_AFTER_2_ATTEMPTS` after the second unsuccessful attempt;
- no alternate hostname/mirror/proxy/provider fallback;
- one-shot execution;
- no HYP-0006 outcome calculation.

Pilot tool:

`tools/hyp0006_dukascopy_browser_pilot.py`

The browser-pilot implementation passed exact-head preflight and was squash-merged to `main` at
`52b2f9c0755a4efbda49c86c96ace1763a3d47cf`.

The exact-main bounded browser pilot ran once on
`c7a10c8bcd84ca4754db92af4c63f39c02101543` and returned
`50` selected / `50` promoted / `0` skipped with
`NO_HYPOTHESIS_OUTCOME_COMPUTED`.

Pilot status:

`PASS_50_OF_50_AUTHORIZATION_CONSUMED`

A zero-network inventory recount confirmed `87 / 1085` canonical objects present and `998`
missing, with `0` network requests, `0` downloaded and `0` semantic missing.

Post-pilot inventory status:

`CONFIRMED_ZERO_NETWORK`

OWNER explicitly authorized one next bounded browser-assisted batch of `250` currently missing
canonical BI5 objects.

Frozen batch-250 scope:

- first `250` current missing deterministic RF-027 objects;
- canonical Dukascopy source only;
- at most `2` attempts per object;
- `SKIPPED_AFTER_2_ATTEMPTS` after the second unsuccessful attempt;
- no alternate hostname/mirror/proxy/provider fallback;
- one-shot execution;
- no HYP-0006 outcome calculation.

Batch tool:

`tools/hyp0006_dukascopy_browser_batch_250.py`

The batch-250 implementation passed exact-head preflight and was squash-merged to `main` at
`94e7a91ec96986dd940f2a13575c9ee436b1a354`.

The authorized exact-main batch-250 execution completed on
`438bc59aa6f2cc81a762914f111017f75a2e46b2` with
`250` selected / `250` promoted / `0` skipped and
`NO_HYPOTHESIS_OUTCOME_COMPUTED`.

Batch status:

`PASS_250_OF_250_AUTHORIZATION_CONSUMED`

Detailed batch-250 JSON/manifest evidence review passed for all `250 / 250` rows. All objects
were completed on the first browser-open attempt (`250` attempts=1 / `0` attempts=2), with
record-count range `341..8535`.

Evidence hashes:

- JSON:
  `36e1301d551a69990ca707e7bf33da1ce07e5e88b1e7dc23a379a66b814e6b2c`;
- manifest:
  `9aa6d7646c809f7a8fb2caaf421f13553ec30ba26dee5d8d991464e1e6cad2e1`.

A zero-network recount confirmed `337 / 1085` canonical objects present and `748` missing, with
`0` network requests, `0` downloaded and `0` semantic missing.

Post-batch inventory status:

`CONFIRMED_ZERO_NETWORK`

OWNER explicitly authorized one next one-shot browser-assisted acquisition of all confirmed `748`
remaining canonical BI5 objects.

Authorization marker:

`OWNER_AUTHORIZED_REMAINING_748_2026_10_05`

Frozen remaining-748 scope:

- exactly all `748` current missing deterministic RF-027 objects;
- execution blocks on any missing-count drift;
- canonical Dukascopy only;
- maximum `2` attempts per object;
- `SKIPPED_AFTER_2_ATTEMPTS` after the second unsuccessful attempt;
- no alternate hostname/mirror/proxy/provider fallback;
- no overwrite; validate before promotion;
- one-shot execution;
- no HYP-0006 outcome calculation.

Tool:

`tools/hyp0006_dukascopy_browser_remaining_748.py`

Status:

`PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED`

Exact-main execution: `0131dd82d286814adaa76ff6e2524e0d000ca13c`.
Manifest SHA-256: `a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4`.
Result: `748` selected / `747` promoted / `1` skipped.

Repeat execution is prohibited.

Detailed evidence review status:

`FULL_JSON_MANIFEST_REVIEW_PASS`

Detailed evidence review passed for all `748 / 748` rows:

- attempts=1: `746`;
- attempts=2: `2`;
- promoted record-count range: `419..31693`;
- promoted SHA-256 uniqueness: `747 / 747`;
- JSON SHA-256:
  `ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112`;
- skipped ordinal/hour: `159 / 2011-11-16T11:00:00Z`;
- final skipped failure: `no_valid_bi5_download_within_45s_attempt_2`;
- skipped canonical file: `ABSENT`.

OWNER supplied the final missing BI5 for `2011-11-16T11:00:00Z`. Frozen decoder validation passed;
the byte-preserving canonical intake has SHA-256
`391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7`
and `6810` records.

Post-intake zero-network recount confirmed `1085 / 1085` required objects present and `0`
missing, with `0` network requests, `0` downloaded and `0` semantic missing.

Bundle status:

`CONFIRMED_ZERO_NETWORK_COMPLETE`

Current gate: exact-main `ATS_TASK_CHECK.bat` for RF-027. Any new browser/source request still
requires a new explicit OWNER decision.
Information boundary remains:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`


RF-027 second exact-main attempt on `2ce019bb51b0e45e900c0555ed44be5a3433e23a` again hit
official BLS archive-index HTTP 403 before event acquisition. The same RF-027 line now stages an
official annual-schedule inventory fallback with archive-header timestamp preferred and no
third-party event source.


RF-027 exact-main attempt on `a4c6331949e9c71fc68eb1baa870d20a03518d48` passed Local CI but was
technically blocked before event acquisition by official BLS HTTP 403. This is not a HYP-0006
result. The same RF-027 line is correcting only BLS automated-access mechanics under the unchanged
official source/event-denominator contract.

RF-023 remains separately open under Strategy #4 and retains its frozen HYP-0005 contract. Its external source-availability blocker is not treated as a negative HYP-0005 result and is not bypassed by RF-025.

## 3. M0 / M1

`M0_PROGRAM_REBASELINE = COMPLETED / PASS`.

`M1_RESEARCH_METHODOLOGY = COMPLETED / PASS`.

Canonical exits:

- `governance/program/M0_EXIT_REVIEW.md`;
- `governance/program/M1_EXIT_REVIEW.md`.

## 4. M2 — Shared Research Platform MVP

| Task ID | WBS | Priority | Status | Dependencies | Deliverable | Definition of Done |
|---|---|---:|---|---|---|---|
| `ATS2-M2-000` | `WBS-2.0` | P1 | DONE | M1 Exit PASS | `governance/program/REFERENCE_CONSUMER_PROFILE.md` | Minimum abstract ordered-data research consumer is defined without choosing a concrete market/instrument/strategy/live environment; WBS-2.0 exists and WBS-2.1 is driven by this profile |
| `ATS2-M2-001` | `WBS-2.1` | P1 | DONE | M2-000 | `governance/decisions/ADR-0001-RESEARCH-STACK.md` | Accepted stack is CPython 3.13 + uv/pyproject/uv.lock, Pydantic v2 + PyYAML boundary validation, NumPy 2.x analytics, typed ordered-record replay semantics, pytest + Ruff; heavier data/live frameworks are deferred until a real consumer needs them |
| `ATS2-M2-002` | `WBS-2.2` | P1 | DONE | M2-001 | `governance/program/RESEARCH_ENVIRONMENT_SPEC.md` + `pyproject.toml` + `.python-version` + `uv.lock` + environment fingerprint/test | Canonical environment supports Windows x86_64 and Linux x86_64 with CPython 3.13.15 + uv 0.12.13; direct/transitive dependencies and install artifacts are locked; `uv sync --frozen` / `uv run --frozen` workflow, fingerprint and environment test are defined |
| `ATS2-M2-003` | `WBS-2.3` | P1 | DONE | M2-001, M2-002 | `governance/program/DATASET_MANIFEST_SPEC.md` + `data/manifests/DATASET_TEMPLATE.yaml` + `src/ats/schemas/dataset_manifest.py` + tests | Stable dataset ID/version, source/snapshot, coverage, event/availability time, deterministic ordering/tie-break, explicit quality policy, transformation lineage, integrity metadata and known limitations are typed and validated with safe YAML/Pydantic using synthetic non-market fixtures |
| `ATS2-M2-004` | `WBS-2.4` | P1 | DONE | M2-003 | `src/ats/data/loader.py` + deterministic loader fixtures/tests | UTF-8 CSV reference data load deterministically from a validated Dataset Manifest with explicit RFC3339 time semantics, ordering/tie-break, duplicate/malformed/out-of-order policies, coverage enforcement and optional SHA-256 verification |
| `ATS2-M2-005` | `WBS-2.5` | P1 | DONE | M2-001, M2-004 | `src/ats/strategy/interface.py` + `tests/test_strategy_interface.py` | Immutable run/observation inputs, generic deterministic state transition, broker-neutral serializable decisions/diagnostics and loader-record bridge are defined without wall-clock/network/broker dependencies |
| `ATS2-M2-006` | `WBS-2.6` | P1 | DONE | M2-004, M2-005 | `src/ats/replay/engine.py` + `tests/test_replay_engine.py` | Same frozen loader output + run context + research strategy produces reproducible ordered observation/state/decision/diagnostic trace with availability-time causality checks and no hidden wall-clock/network inputs |
| `ATS2-M2-007` | `WBS-2.7` | P1 | DONE | M2-006 | `src/ats/costs/interface.py` + tests | Costs are explicit deterministic inputs applied outside strategy logic and kept separate from gross effects/results |
| `ATS2-M2-008` | `WBS-2.8` | P1 | DONE | M2-006, M2-007 | `src/ats/analytics/standard.py` + `tests/test_standard_analytics.py` | Baseline output exposes effect/P&L, risk/path, events/trades and costs as applicable |
| `ATS2-M2-009` | `WBS-2.9` | P1 | DONE | M2-002…008 | `src/ats/runner/experiment.py` + `tests/test_experiment_runner.py` | Registered experiment context can be replayed by a documented procedure without rewriting preregistration |
| `ATS2-M2-010` | `WBS-2.10` | P1 | DONE | M2-004…009 | `tests/test_research_platform.py` + `tests/fixtures/platform/reference_consumer_expected.json` | Critical calculations have deterministic non-market fixtures/regression checks |
| `ATS2-M2-011` | M2 Exit | P1 | DONE / PASS | M2-000…010 | `governance/program/M2_EXIT_REVIEW.md` | Minimal reusable vertical research stack can reproduce an end-to-end baseline registered experiment workflow |

M2 Exit decision: `PASS`. The platform milestone is complete; this does not create research evidence for a trading strategy.

## 5. M3 — Reference Strategy #1

| Task ID | WBS | Priority | Status | Dependencies | Deliverable | Definition of Done |
|---|---|---:|---|---|---|---|
| `ATS2-M3-001` | `WBS-3.1` | P1 | DONE | M1 PASS, M2 PASS | `governance/program/REFERENCE_STRATEGY_1_SELECTION.md` | Selected `SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT` as the first reference strategy class without selecting parameters, instrument, vendor or claiming profitability |
| `ATS2-M3-002` | `WBS-3.2` | P1 | DONE | M3-001 | `research/ideas/IDEA-0001.md` + `research/hypotheses/HYP-0001.md` | `IDEA-0001` is screened and `HYP-0001` fixes a 24-bar breakout condition, 24-bar primary horizon, BID/ASK execution premise and falsification path before prototype results |
| `ATS2-M3-003` | `WBS-3.3` | P1 | DONE / CONDITIONAL | M3-002 | `research/reviews/HYP-0001-DATA_FEASIBILITY.md` | Dukascopy EUR/USD 1H BID/ASK path is structurally suitable; actual snapshot/coverage must be frozen before prototype execution, and PROTO-01 economic claims remain before-financing unless rollover/commission inputs are added |
| `ATS2-M3-004` | `WBS-3.4` | P1 | DONE / REJECT | M3-002, M3-003 CONDITIONAL | `research/reviews/HYP-0001-PROTOTYPE-01.md` + dataset manifest + `reports/research/HYP-0001-PROTOTYPE-01-result.json` | 1006 fixed-rule signals were observed; signal mean return was negative and below baseline, so the preregistered rule produced `REJECT` and the line stops before Economic Pre-Screen |
| `ATS2-M3-005` | `WBS-3.11 (early-rejection path)` | P1 | DONE / PASS | M3-004 REJECT | `governance/program/M3_EXIT_REVIEW.md` | R3 rejection is preserved; WBS-3.5–3.10 are not entered; real-data/platform learnings are recorded; M3 Exit = PASS without tuning HYP-0001 |

Because PROTO-01 returned `REJECT`, WBS-3.5–3.10 are not entered for this research line. The remaining M3 work is the early-rejection platform-learning/exit path under WBS-3.11.

Reference Strategy #1 class and EUR/USD research instrument are selected, and `HYP-0001` fixes the initial 24-bar research parameters; no Candidate, Strategy ID or Experiment has yet been created.

Carryover from ATS v1 remains governed by `legacy/v1/CARRYOVER.md`.

## 6. M4 — Validation Framework

| Task ID | WBS | Priority | Status | Dependencies | Deliverable | Definition of Done |
|---|---|---:|---|---|---|---|
| `ATS2-M4-001` | `WBS-4.1` | P1 | DONE | M3 PASS, M1 methodology | `governance/methodology/VALIDATION_FRAMEWORK.md` | Development/validation/independent boundaries, mandatory validation dimensions, dependence/overlap treatment, decision rules and tooling contracts are defined without inventing a Candidate or reopening HYP-0001 |
| `ATS2-M4-002` | `WBS-4.2` | P1 | DONE | M4-001, M2 platform | `src/ats/validation/sensitivity.py` + `tests/test_validation_sensitivity.py` | Ordered predefined variants are all evaluated and serialized; missing/extra/non-finite metrics fail closed; the result exposes `NO_AUTOMATIC_SELECTION` and no best/winner ranking |
| `ATS2-M4-003` | `WBS-4.3` | P1 | DONE | M4-001, M4-002 | `src/ats/validation/slicing.py` + `tests/test_validation_slicing.py` | Every declared slice is reported in plan order; exhaustive/overlap/empty-slice policies are explicit; unknown membership and metric-contract violations fail closed |
| `ATS2-M4-004` | `WBS-4.4` | P1 | DONE | M4-001, M4-003 | `src/ats/validation/concentration.py` + `tests/test_validation_concentration.py` | Full observation/group set is retained; predeclared top-count diagnostics quantify absolute concentration; zero-denominator cases are explicit; no outlier is removed automatically |
| `ATS2-M4-005` | `WBS-4.5` | P1 | DONE | M4-001, M4-004 | `src/ats/validation/resampling.py` + `tests/test_validation_resampling.py` | Whole declared blocks are resampled with replacement under an explicit seed/method; internal block order and full selection trace are preserved; no IID fallback exists in the API |
| `ATS2-M4-006` | `WBS-4.6` | P1 | DONE | M4-001, M4-005 | `governance/methodology/INDEPENDENT_EXAM_PROTOCOL.md` | Freeze manifest fixes version/code/config/data/costs/metrics/rule before reveal; reveal is irreversible; only PASS/FAIL exists; post-reveal repair cannot restore independence |
| `ATS2-M4-007` | `WBS-4.7` | P1 | DONE | M4-001, M4-006, experiment/discovery history | `governance/methodology/MULTIPLE_RESEARCH_ACCOUNTING.md` | Material Research Attempts, bounded-search denominators, negative/discarded outcomes, data/cost changes, returns to research and consumed protected blocks remain traceable to the selected version |
| `ATS2-M4-008` | `WBS-4.8` | P1 | DONE | M4-001…007 | `governance/methodology/TECHNICAL_STRATEGY_VALIDATION_PROFILE.md` | Technical price-driven strategy profile makes V1–V7 concrete, declares applicability/required evidence and specifies what must be frozen before S06/S07 |
| `ATS2-M6-000` | `WBS-6.0` | P1 | DONE | M2, M3 learnings, M4-008 | `governance/methodology/MARKET_PATTERN_DISCOVERY.md` + reusable bounded-search tooling | Search Manifest contract, deterministic full-denominator engine and synthetic contract tests are available without creating market evidence |
| `ATS2-M6-001` | `WBS-6.0` | P1 | DONE | M6-000 | `research/discovery/SEARCH-EURUSD-H1-2021-2025-001.yaml` + `reports/research/SEARCH-EURUSD-H1-2021-2025-001-summary.md` | Exact-head run evaluated all 16 alternatives, retained full denominator and returned `SHORTLIST_FOR_IDEA_INTAKE` with five reversal variants |
| `ATS2-M6-002` | `WBS-6.1` | P1 | DONE | M6-001 | `governance/program/REFERENCE_STRATEGY_2_SELECTION.md` + `research/ideas/IDEA-0002.md` | Selected the two-sided return-tail reversal class and screened IDEA-0002 without promoting one discovery cell as a winner |
| `ATS2-M6-003` | `WBS-6.2` | P1 | DONE | M6-002 | `research/hypotheses/HYP-0002.md` | Froze the post-discovery two-sided 24H reversal formulation and required development-only thresholds plus unseen confirmatory data |
| `ATS2-M6-004` | `WBS-6.2` | P1 | DONE | M6-003 | `research/reviews/HYP-0002-DATA-FEASIBILITY-PREP.md` + local preparation report | Froze Q10_DEV/Q90_DEV and the disjoint 2026-01 through 2026-08 Dukascopy BID/ASK block with no HYP-0002 outcome calculation |
| `ATS2-M6-005` | `WBS-6.2` | P1 | DONE | M6-004 | `research/reviews/HYP-0002-DATA-FEASIBILITY.md` + confirmatory Dataset Manifest | Recorded CONDITIONAL feasibility and froze thresholds, confirmatory data identity, timing and cost limitations before outcome reveal |
| `ATS2-M6-006` | `WBS-6.2` | P1 | DONE | M6-005 | `research/reviews/HYP-0002-PROTOTYPE-01.md` + frozen runner/tests | Froze the two-sided prototype question, four-inequality decision rule and deterministic implementation before reveal |
| `ATS2-M6-007` | `WBS-6.2` | P1 | DONE | M6-006 | `reports/research/HYP-0002-PROTOTYPE-01-result.json` | Exact frozen reveal returned `REJECT`: high-tail/DOWN passed both inequalities while low-tail/UP failed both; no rerun or post-result rescue |
| `ATS2-M6-008` | `WBS-6.7` | P1 | DONE | M6-007 REJECT | `governance/program/REFERENCE_STRATEGY_2_CLOSEOUT.md` | Preserved terminal negative evidence, recorded reuse/generalization learnings and kept downstream strategy work unentered |
| `ATS2-M6-009` | M6 Exit | P1 | DONE / PASS | M6-008 | `governance/program/M6_EXIT_REVIEW.md` | M6 closed against its two-profile Research Factory/platform-generalization exit criterion; both strategy lines remain rejected at R3 and candidate count remains zero |

## 7. Continuous Research Factory after M6

| Task ID | WBS | Priority | Status | Dependencies | Deliverable | Definition of Done |
|---|---|---:|---|---|---|---|
| `ATS2-RF-001` | `WBS-RF.0` | P1 | DONE | M6 Exit PASS | `governance/program/STRATEGY_3_SOURCING_REBASELINE.md` | Continuous Research Factory lane defined without inventing Strategy #3 facts; development tuning before confirmatory freeze is allowed only with complete search accounting |
| `ATS2-RF-002` | `WBS-RF.1` | P1 | DONE | RF-001 PASS | `governance/program/STRATEGY_3_IDEA_SOURCING.md` | Retained four reviewed families, shortlisted three and selected no winner |
| `ATS2-RF-003` | `WBS-RF.1` | P1 | DONE | RF-002 PASS | `governance/program/STRATEGY_3_FAMILY_SELECTION.md` + `research/ideas/IDEA-0003.md` | Selected cross-sectional currency momentum and registered IDEA-0003 without fixing a parameter set |
| `ATS2-RF-004` | `WBS-RF.2` | P1 | DONE | RF-003 PASS | `research/hypotheses/HYP-0003.md` | Froze the 25-cell development grid, broad-region rule and separate future confirmatory-Hypothesis boundary |
| `ATS2-RF-005` | `WBS-RF.2` | P1 | DONE | RF-004 PASS | `research/reviews/HYP-0003-DATA-FEASIBILITY.md` | Recorded CONDITIONAL source feasibility, non-performance G10-ex-USD candidate universe, timing and protected-tail rules |
| `ATS2-RF-006` | `WBS-RF.2` | P1 | DONE | RF-005 PASS | `research/reviews/HYP-0003-DATA-FEASIBILITY-PREP.md` + probe tool/tests + local feasibility report | Exact-head OWNER launcher PASS recorded 9/9 source-qualified currencies, common possible development start and probe hashes without computing momentum |
| `ATS2-RF-007` | `WBS-RF.2` | P1 | DONE | RF-006 PASS | `reports/research/HYP-0003-DATA-FEASIBILITY-PREP-result.json` + updated `research/reviews/HYP-0003-DATA-FEASIBILITY.md` | Exact-head OWNER launcher PASS froze the 9-currency source universe, common possible coverage and full development-data acquisition contract without revealing the protected tail |
| `ATS2-RF-008` | `WBS-RF.2` | P1 | DONE / PASS | RF-007 PASS | `research/reviews/HYP-0003-DEVELOPMENT-DATA-PREP.md` + `tools/hyp0003_development_data.py` + tests + local preparation report | Exact-head OWNER launcher PASS on `63e1bc9c7e1ba2e001ecdd9918244d83db0e58c3` acquired `3906 / 3906` source objects, prepared `1,014,509` rows, emitted frozen source/data hashes and requested zero protected-tail source objects without computing a HYP-0003 momentum cell |
| `ATS2-RF-009` | `WBS-RF.2` | P1 | DONE / PASS | RF-008 PASS | canonical RF-008 result + development Dataset Manifest/schema + updated Data Feasibility freeze | Exact-main OWNER launcher PASS on `74057ebcb6d43fbb66a275c74fbd2081b148f9a2` froze the prepared dataset identity, schema, source/data hashes and quality facts with `NO_HYPOTHESIS_OUTCOME_COMPUTED` |
| `ATS2-RF-010` | `WBS-RF.2` | P1 | DONE / PASS | RF-009 PASS | `research/reviews/HYP-0003-PROTOTYPE-01.md` + frozen runner + synthetic tests | Exact-main OWNER launcher PASS on `dbb93b2510334561c7c38aa14b859aa42a420bbc` froze the complete 25-cell runner/decision contract with `NO_HYPOTHESIS_OUTCOME_COMPUTED` |
| `ATS2-RF-011` | `WBS-RF.2` | P1 | DONE / PASS | RF-010 PASS | `reports/research/HYP-0003-PROTOTYPE-01-result.json` + updated prototype evidence | Exact-main OWNER reveal on `f974b9bb60a6cc295cb8aaba4a263499c14769c0` retained all 25 cells and returned `REJECT / STOP_HYP0003`: median cell mean `-0.0013404354655954772`, positive cells `8/25`, formation span `4/5`, holding span `4/5` |
| `ATS2-RF-012` | `WBS-RF.2` | P1 | DONE / PASS | RF-011 REJECT | `governance/program/STRATEGY_3_CLOSEOUT.md` + updated prototype/state/backlog | Exact-main OWNER launcher PASS on `90d8f4f44f84d6116fa7ee1e815ecc827b213bcf` preserved the complete HYP-0003 negative result and closed Strategy #3 as `REJECTED_AT_R3` without rescue |
| `ATS2-RF-013` | `WBS-RF.1` | P1 | DONE / PASS | RF-012 PASS | `governance/program/STRATEGY_4_IDEA_SOURCING.md` | Exact-main OWNER launcher PASS on `d8ba5544111ff05fc48c59939acccb337b220e99` retained five reviewed families and a four-family shortlist without ranking, selection or IDEA-0004 |
| `ATS2-RF-014` | `WBS-RF.1` | P1 | DONE / PASS | RF-013 PASS | `governance/program/STRATEGY_4_FAMILY_SELECTION.md` + `research/ideas/IDEA-0004.md` | Exact-main OWNER launcher PASS on `b1392ad843c57bf0ca4c2d0575f4095957b80e82` selected S4-FAM-03 for Idea Intake and screened IDEA-0004 without performance-selected parameter fixation |
| `ATS2-RF-015` | `WBS-RF.2` | P1 | DONE / PASS | RF-014 PASS | `research/hypotheses/HYP-0004.md` | Exact-main OWNER launcher PASS on `79d83a5fb900e00f510c4348cc6dcb8a5489c5c0` registered the bounded fixed-UTC EUR/USD structural claim before outcome inspection |
| `ATS2-RF-016` | `WBS-RF.2` | P1 | DONE / PASS | RF-015 PASS | `research/reviews/HYP-0004-DATA-FEASIBILITY.md` | Exact-main OWNER launcher PASS on `3628010fc04045de040794c482e57ccd2639f99b` recorded CONDITIONAL feasibility without computing a HYP-0004 outcome |
| `ATS2-RF-017` | `WBS-RF.2` | P1 | DONE / PASS | RF-016 PASS | `research/reviews/HYP-0004-DEVELOPMENT-DATA-PREP.md` + `tools/hyp0004_development_data.py` + synthetic tests + local preparation result | Exact-main OWNER launcher PASS on `ae9767a71b3860e55d345afb34b2f9c18b5dd063` verified the frozen parent, prepared `112900` EUR/USD rows, emitted derived SHA-256 `3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6` and retained `NO_HYPOTHESIS_OUTCOME_COMPUTED` |
| `ATS2-RF-018` | `WBS-RF.2` | P1 | DONE / PASS | RF-017 PASS | canonical RF-017 result + `data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001.yaml` + schema + Data Feasibility freeze update | Exact-main OWNER launcher PASS on `6d388c500d2c5e1671e11700966b713b95a395b8` froze the exact `112900`-row dataset identity, `111938` exact-next-hour denominator, bucket geometry and `H1_OPEN_PROXY_AT_EVENT_TIME` limitation without outcome calculation |
| `ATS2-RF-019` | `WBS-RF.2` | P1 | DONE / PASS | RF-018 PASS | `research/reviews/HYP-0004-PROTOTYPE-01.md` + `tools/hyp0004_proto01.py` + synthetic tests | Exact-main OWNER launcher PASS on `95174c2922fd5882c995ff14b3031d690ecc80bf` froze the exact structural calculations, calendar-year diagnostics, both primary inequalities, decision routing and runner blob `cbc9a46bf5e5296615f51c0ea564153968bc2a55` without revealing a development outcome |
| `ATS2-RF-020` | `WBS-RF.2` | P1 | DONE / PASS | RF-019 PASS | exact local `HYP0004_PROTO01_RESULT.json` + shareable report | Exact-main OWNER reveal on `60371d16b71c1e7d1fb0ccd83c5104984e4b740a` executed the exact frozen runner once after full Local CI PASS and returned `ADVANCE_TO_ECONOMIC_SCREEN / BOTH_PRIMARY_INEQUALITIES_MET`; both primary inequalities passed and the result SHA-256 is `1c9b2cb1a1628599e935ee61fd8c9b152d7bd3447969b065c920c8d13e3e5230` |
| `ATS2-RF-021` | `WBS-RF.2` | P1 | DONE / PASS | RF-020 PASS | `reports/research/HYP-0004-PROTOTYPE-01-result.json` + updated prototype/state/backlog | Exact-main OWNER launcher PASS on `79cb1d36bd544cc14db49ea5f6e85ef138a579eb` preserved the exact RF-020 result and selected the confirmatory structural branch; direct R4 remains blocked |
| `ATS2-RF-022` | `WBS-RF.2` | P1 | DONE / PASS | RF-021 PASS | `research/hypotheses/HYP-0005.md` | Exact-main OWNER launcher PASS on `136b62b52922abc1556396377c6cd6fca88fba75` registered HYP-0005 with EURUSD/fixed UTC buckets/NEXT_1H/two primary inequalities and retained `NO_CONFIRMATORY_OUTCOME_COMPUTED` |
| `ATS2-RF-023` | `WBS-RF.2` | P1 | DONE / PASS | RF-022 PASS; exact-main RF-034 PASS | `research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md` + immutable `tools/hyp0005_data_feasibility.py` + original 10 source hashes + local 2010-row CSV / JSON / TXT | Exact-main one-shot offline preparation on `14531698c87fd3a0d87e1ec54c6713f11b7cbb60` returned READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE, 1991 eligible exact-next-hour, fixed bucket/segment geometry, 3 unfilled expected market hours, zero HYP-0005 primary outcomes; original source bundle/derived CSV hashes retained |

RF-023 exact-main preparation PASS is preserved as RF-034 on `14531698c87fd3a0d87e1ec54c6713f11b7cbb60`: 2010 rows, 1991 eligible exact-next-hour, 10 source objects and 3 unfilled missing expected market hours. RF-024 now stages a CONDITIONAL data-feasibility review and exact dataset identity; **not frozen until RF-024 exact-main PASS**. No independent provider-byte certification, source replacement, HYP-0005 spread/return metrics, primary inequality or P&L has occurred.

| `ATS2-RF-024` | `WBS-RF.2` | P1 | READY | RF-023 exact-main preparation PASS; RF-034 exact-main PASS | `research/reviews/HYP-0005-DATA-FEASIBILITY.md` + versioned `data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001.yaml` + `.schema.json` + synchronized SoT/checker | Stage CONDITIONAL feasibility with H1_OPEN_PROXY_AT_EVENT_TIME limitation, two disjoint predeclared protected intervals, 10 original hashes, source bundle/2010 row CSV SHA-256, 1991 eligible geometry; dataset freeze only after exact-head/merge/exact-main PASS, no spread, next-hour return or primary inequality |
| `ATS2-RF-025` | `WBS-RF.2` | P1 | DONE / PASS | RF-022 PASS; retained `S4-FAM-02` sourcing provenance; RF-023 may remain externally blocked | `research/ideas/IDEA-0005.md` + `research/hypotheses/HYP-0006.md` + synchronized state/backlog/handoff/current-task gate | Exact-main OWNER launcher PASS on `9b0a6c8898a7ebf9b03167a871ad02af96ca2807` registered IDEA-0005/HYP-0006 as two Material Research Attempts while preserving HYP-0005 and `NO_HYPOTHESIS_OUTCOME_COMPUTED` |
| `ATS2-RF-026` | `WBS-RF.2` | P1 | DONE / PASS | RF-025 exact-main PASS | `research/reviews/HYP-0006-DATA-FEASIBILITY.md` + synchronized state/backlog/handoff/current-task gate | Exact-main OWNER launcher PASS on `5e0ff9e4481e5dc28c14a73adcf32433715973a3` recorded `CONDITIONAL` feasibility, frozen the development interval and source/timing constraints, and retained `NO_HYPOTHESIS_OUTCOME_COMPUTED` |
| `ATS2-RF-027` | `WBS-RF.2` | P1 | DONE / PASS | RF-026 exact-main PASS | `research/reviews/HYP-0006-DATA-FEASIBILITY-PREP.md` + `tools/hyp0006_data_feasibility.py` + synthetic tests + local machine result | Exact-main PASS on `bbbdbd301b610dfc61316c9ff82015fb0e039a47` returned `READY_FOR_DATA_FEASIBILITY_FREEZE`, `217/217` complete timestamp-geometry events, `1085/1085` required BI5 objects, zero protected HYP-0005 requests and `NO_HYPOTHESIS_OUTCOME_COMPUTED` |
| `ATS2-RF-028` | `WBS-RF.2` | P1 | DONE / PASS | RF-027 exact-main PASS | `research/reviews/HYP-0006-DATA-TOLERANCE-FREEZE.md` + `tools/hyp0006_data_tolerance_freeze.py` + synthetic tests + local freeze result | Exact-main owner launcher PASS on `e7f05a0d237c4d78a8a0edb93710619e6ad2ba00` froze 216/217 eligible events, 1 gap-based exclusion, 30000 ms anchor tolerances and unchanged RF-027 hashes with `NO_HYPOTHESIS_OUTCOME_COMPUTED` |
| `ATS2-RF-029` | `WBS-RF.2` | P1 | DONE / PASS | RF-028 exact-main PASS | `research/reviews/HYP-0006-PROTOTYPE-01.md` + `tools/hyp0006_proto01.py` + synthetic tests + synchronized SoT/current-task gate | Exact-main PASS on `94df9ede91522f473872b25a6d8023fd64182878` froze the 216-event structural question, equations, source/anchor reconstruction, diagnostics, single median inequality, decision routing and runner blob `6afb870c035bc5ae76f773784a5fa3db15d680fd` with `NO_HYPOTHESIS_OUTCOME_COMPUTED` |
| `ATS2-RF-030` | `WBS-RF.2` | P1 | DONE / PASS | RF-029 exact-main PASS | `research/reviews/HYP-0006-PROTOTYPE-01-REVEAL-GATE.md` + canonical local `HYP0006_PROTO01_RESULT.json` + shareable report | Exact-main OWNER launcher PASS on `d1135bb2486009ebb358bf4b508c06303ab77f74` verified 1085/1085 BI5 SHA-256, ran frozen runner once, preserved 216/217 event results and `ADVANCE_TO_ECONOMIC_SCREEN` under preregistered median inequality; JSON SHA-256 `484575ceb2b6c12df651697d50559e70c7cba8a8f52fc4508d28943e8c5447e9`; exploratory only, no trading/independent claim |
| `ATS2-RF-031` | `WBS-RF.2` | P1 | DONE / PASS | RF-030 exact-main PASS; OWNER approved new confirmatory structural hypothesis preparation | `research/reviews/HYP-0006-PROTOTYPE-01-RESULT-REVIEW.md` + `research/hypotheses/HYP-0007.md` + synchronized SoT | Exact-main OWNER launcher PASS on `1ff81954fa1918975a9d19ce94c3f8c926fecb96` retained exact HYP-0006 reveal SHA-256 `484575ceb2b6c12df651697d50559e70c7cba8a8f52fc4508d28943e8c5447e9` and registered distinct HYP-0007 8-gate confirmatory structural plan without outcome or independent dataset |
| `ATS2-RF-032` | `WBS-RF.2` | P1 | DONE / PASS | RF-031 exact-main PASS; OWNER switched priority to HYP-0005 | `research/reviews/HYP-0005-OFFLINE-SOURCE-INTAKE.md` + offline-only RF-023 source tool + tests + tracked state | Exact-main OWNER launcher PASS on `8b7492f0f17a549f51a967a9bc9dfdbf2fdd0ce9` confirmed frozen HYP-0005 source architecture, no external network/market outcome and source-input requirement; a later 9 October OWNER file-only intake is separate technical evidence |
| `ATS2-RF-033` | `WBS-RF.2` | P1 | DONE / PASS | RF-032 exact-main PASS and OWNER byte-preserving source intake | `.gitignore` narrow provenance ignore + `research/reviews/HYP-0005-LOCAL-SOURCE-INTAKE-EVIDENCE.md` + tracked state | Exact-main OWNER launcher PASS on `5ea7a923c59c44d6b733f8c7c6db352fd846d434` verified all 10 local BID/ASK objects, exact 2026-09 provenance hash, Git CLEAN, 254 tests, and no hypothesis outcome |
| `ATS2-RF-034` | `WBS-RF.2` | P1 | DONE / PASS | RF-033 exact-main PASS; OWNER authorized offline RF-023 preparation | `research/reviews/HYP-0005-RF023-OFFLINE-PREPARATION-GATE.md` + original frozen data tool + source/result hash-only checker + exact-main 2010-row result | Exact-main `14531698c87fd3a0d87e1ec54c6713f11b7cbb60`, 257 pytest, Ruff/validator/local CI PASS; one-shot RF-023 runner produced 1991 exact-next-hour eligible, READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE, no hypothesis outcome or source HTTP |

## 8. Следующий шаг

Current task: `ATS2-RF-024` — HYP-0005 confirmatory
Data Feasibility review and conditional dataset freeze. This is
research step **2/5** after RF-023 preparation exact-main PASS.

RF-034 / RF-023 source geometry preparation:
`14531698c87fd3a0d87e1ec54c6713f11b7cbb60`,
2010 prepared rows, 1991 exact-next-hour eligible
(838 CORE_ACTIVE, 837 OFF_HOURS, 316 TRANSITION);
LEFT_UNSEEN 1542 eligible, RIGHT_UNSEEN 449 eligible;
3 left expected-market-hour gaps and 0 right gaps.
Precomputed source-bundle SHA-256:
`65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2`.
Prepared CSV SHA-256:
`b1091c4975665b2b0cd4f58627a10aceaab7aeff5076431abb6abc74c0a054c1`.

Tracked review:
`research/reviews/HYP-0005-DATA-FEASIBILITY.md`.

Staged dataset version:
`DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0`.
Manifest/schema under `data/manifests/`.
Decision: `CONDITIONAL` due to
`H1_OPEN_PROXY_AT_EVENT_TIME`, three unfilled gaps and
`USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER`.
Do not claim vendor or tick timing independently verified.

Execution sequence: GPT stages agent branch/PR; OWNER
`.\\ATS_AGENT_PREFLIGHT.bat` exact-head PASS; GPT squash merge;
OWNER `.\\ATS_TASK_CHECK.bat` exact-main PASS.
**Only then** RF-024 dataset identity is formally frozen.
The RF-024 checker must verify old local RF-023 result
hashes without rerunning RF-023, decoding quotes or
calculating primary movement/spread inequalities.

Next research step **3/5** pre-reveal runner freeze
is not yet authorized. HYP-0005 outcome:
`NO_CONFIRMATORY_OUTCOME_COMPUTED`.
