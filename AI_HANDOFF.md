# ATS AI Handoff

## Current program state

- M0-M3: COMPLETED / PASS.
- M4 baseline reusable; M4.9/M4.10 blocked pending a future S05 PASS Candidate.
- M6: COMPLETED / PASS.
- Strategies #1–3: REJECTED_AT_R3.
- Strategy #4 IDEA-0004 / HYP-0005: first structural confirmatory
  reveal PASS, review step 5/5 ACTIVE. NOT a trading Candidate.
- Strategy #5 HYP-0006: DEVELOPMENT_REVEALED_EXPLORATORY_ONLY.
- HYP-0007: formation complete, independent data certification PAUSED.
- Candidate count: 0. Live and capital approvals remain OFF.

## Current research and exact source of truth

Current Technical ID: ATS2-RF-038.
Original lineage: IDEA-0004 / HYP-0005 / PROTO-01.
Research plan 5/5 — preserve and interpret first reveal.
No new material research attempt or alternative date/bucket/threshold.

Completed task: ATS2-RF-037.
Exact-main one-time reveal HEAD:
4388ac8aac732f7bd745a4466f8a9b524d543167
OWNER report: ATS CURRENT TASK CHECK PASS and
ATS TASK LAUNCHER PASS, clean exact main, full ATS Local CI,
validator, pinned Ruff lint/format, 278 pytest PASS.
RF-037 OWNER task report SHA-256:
f5fff726d8243d0434364d6bfcff60d4f1614bbe459de4d7494c40b229a46369

Original OWNER authorization on 2026-10-12:
OWNER_AUTHORIZED_HYP0005_FIRST_REVEAL_ONCE_2026_10_12
Status: CONSUMED_BEFORE_OUTCOME then
FIRST_REVEAL_COMPLETED_ONCE. Do not rerun.
Saved original result: CONFIRMATORY_STRUCTURAL_PASS,
decision reason BOTH_PRIMARY_INEQUALITIES_MET,
both primary Boolean comparisons TRUE.

Tracked last completed artifact:
research/reviews/HYP-0005-PROTOTYPE-01-FIRST-REVEAL-EXECUTION.md
Tracked next artifact (staging):
research/reviews/HYP-0005-PROTOTYPE-01-RESULT-REVIEW.md

Five original OWNER-supplied HYP-0005 RF-037 artifacts:

- task report SHA-256:
  f5fff726d8243d0434364d6bfcff60d4f1614bbe459de4d7494c40b229a46369
- result JSON SHA-256:
  cba7f07eebef52b649d2a2b6a7edb1dc0b808c04080fe1ae0d71e6eab25f19dc
- result TXT SHA-256:
  57daab4a0ae2834d338f77785d52ecd3383c026d5df1196648f0b19a86813af9
- consumed marker SHA-256:
  726ffc650a43982b49da998cd2d5ac6a5f33f816bbb0a39434998335296cf359
- receipt SHA-256:
  3a0f29606781c6fadabc3a141439752a60aa8e744760405a584ec005400ab6c1

Frozen HYP-0005 runner Git blob:
814193997768605fe60607d66dfd755a9323f339.
Dataset DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0.
Source bundle SHA-256:
65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2.
Original CSV SHA-256:
b1091c4975665b2b0cd4f58627a10aceaab7aeff5076431abb6abc74c0a054c1.

2010 prepared rows / 1991 eligible:
CORE_ACTIVE 838; OFF_HOURS 837; TRANSITION 316;
LEFT_UNSEEN 1542 / RIGHT_UNSEEN 449.
Three expected LEFT market hours genuinely missing.
The exact source blocks LEFT May-Aug 2003 and RIGHT Sep 2026
were revealed on RF-037 and are now CONSUMED.
The previously consumed intervening history remains consumed.
No HYP-0005 block can be reclassified independent for other ATS lines.

Original primary movement medians:
CORE_ACTIVE 0.0007490105401033453,
OFF_HOURS 0.00038491476276447667 (PASS).
Original median relative spread:
CORE_ACTIVE 0.00008657184257709088,
OFF_HOURS 0.0001246294499390464 (PASS).
The positive decision is nondirectional and structural.
Calendar-year diagnostics (2003/2026) do not upgrade this
result or act as independent tests.

Evidence original label:
CONFIRMATORY_STRUCTURAL_NOT_INDEPENDENT_EXAM.
No formal EXP manifest or frozen directional Strategy Version;
taxonomy qualified class remains EXPLORATORY_PROTOTYPE.
Data Feasibility remains CONDITIONAL /
H1_OPEN_PROXY_AT_EVENT_TIME, exact tick boundary unknown.
2026-09 source provider identity remains
USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER.

The frozen result limitations contain historical RF-024
pre-reveal text, including the outdated assertion that
HYP-0005 outcome has not yet been computed. Do NOT edit
the result JSON to fix this; clarify status in separate review.
No trading P&L, cost model, signal direction, entry/exit,
economic viability, independent examination, Candidate,
live execution or capital approval can be inferred.
Direct R4 admission remains blocked.

RF-038 changes governance/review/checker only.
The original HYP-0005 market runner must NEVER execute again.
Agent preflight does NOT read original quote rows.
OWNER exact-main RF-038 task must verify saved
consumed/result/receipt hashes only, WITHOUT first reveal
or recomputed medians from protected data.

Next action: OWNER exact-head .\ATS_AGENT_PREFLIGHT.bat
on agent/rf038-hyp0005-post-reveal-review once PR is staged,
then sends AGENT_PREFLIGHT_REPORT.txt. GPT merges only after
verified exact-head PASS; OWNER exact-main .\ATS_TASK_CHECK.bat
hash-only PASS then closes RF-038.
The subsequent research action requires lineage/Idea Intake
for any new directional cost-aware trading hypothesis;
NO new ID has been minted and no protected data is reserved.

HYP-0005: REVEALED_CONFIRMATORY_STRUCTURAL_PASS.
RF-038: POST_REVEAL_REVIEW_STAGED_NO_MARKET_RERUN.
HYP-0006: DEVELOPMENT_REVEALED_EXPLORATORY_ONLY.
HYP-0007: NO_CONFIRMATORY_OUTCOME_COMPUTED.

## HYP-0006 fixed research claim

Canonical Hypothesis:

`research/hypotheses/HYP-0006.md`

Frozen before outcome inspection:

- market: `FX_SPOT_OTC`;
- instrument: `EURUSD`;
- event class: scheduled U.S. CPI publication;
- pre-event horizon: previous 60 minutes;
- post-event horizon: next 60 minutes;
- `PRE_RELEASE_ANCHOR` strictly before public release;
- primary structural claim:
  `median(post_abs_60m_return) > median(pre_abs_60m_return)`;
- no directional return sign;
- no trading-P&L claim.

## RF-026 closure

Canonical completed artifact:

`research/reviews/HYP-0006-DATA-FEASIBILITY.md`

Current next artifact:

research/reviews/HYP-0005-PROTOTYPE-01-RESULT-REVIEW.md

RF-026 closed exact-main PASS on:

`5e0ff9e4481e5dc28c14a73adcf32433715973a3`

Data Feasibility decision:

`CONDITIONAL`

Development interval:

`2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z`

Evidence class:

`DEVELOPMENT / EXPLORATORY ONLY`

## Why RF-027 source architecture changed

Two exact-main RF-027 attempts passed Local CI and then failed before event acquisition because live
BLS HTTP access returned 403:

- `a4c6331949e9c71fc68eb1baa870d20a03518d48`;
- `2ce019bb51b0e45e900c0555ed44be5a3433e23a`.

Both are:

`TECHNICAL_SOURCE_ACCESS_FAILURE`

Neither computed a HYP-0006 outcome.

ATS therefore no longer treats live BLS availability as a normal runtime dependency.

## Current RF-027 architecture

Protocol:

`research/reviews/HYP-0006-DATA-FEASIBILITY-PREP.md`

Snapshot intake instructions:

`research/reviews/HYP-0006-BLS-SNAPSHOT-INTAKE.md`

Snapshot manifest:

`data/reference/HYP-0006-BLS-SCHEDULE-SNAPSHOT-MANIFEST.csv`

Required official BLS annual schedule snapshots:

`2003..2021`

Local raw path:

`data/raw/bls/hyp0006/schedules/YYYY.html`

Normal RF-027 live BLS network mode:

`PROHIBITED`

Once the 19 official snapshots exist locally, the runner creates:

`data/derived/HYP-0006-BLS-CPI-CALENDAR-2003-2021.csv`

Source identity:

`BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS`

Timestamp semantics:

`BLS_ANNUAL_SCHEDULE_US_EASTERN`

The calendar is hashed before any EUR/USD outcome is computed.

## Current RF-027 source status

The one-time official BLS snapshot intake is complete locally.

Canonical local bundle:

- years: `2003..2021`;
- count: `19`;
- path: `data/raw/bls/hyp0006/schedules/YYYY.html`;
- content preserved during filename normalization.

An earlier exact-main RF-027 source-preparation run passed governance and full Local CI, then:

- produced the local BLS CPI calendar;
- found `217` CPI events;
- produced BLS calendar SHA-256
  `646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9`;
- stopped on Dukascopy tick acquisition for
  `2004-03-17T12:00:00Z`;
- last proven source error: `HTTP 503`;
- created no geometry CSV and no final RF-027 result JSON.

This is:

`TECHNICAL_SOURCE_ACCESS_FAILURE`

It is not a HYP-0006 result.

Repository-wide source discipline:

`FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF`

After the first proven external HTTP/network/access failure, automatic retries, alternate endpoints and fallbacks stop immediately. A new external attempt requires explicit OWNER authorization after that first failure is reported.


The first-failure policy correction passed exact-head preflight and was squash-merged to `main` at:

`367976fa7510d0fe8c3662d5b33a9889fc824c94`

A later offline inventory of the frozen RF-027 timestamp geometry, using the same BLS calendar
SHA-256, found:

- CPI events: `217`;
- required unique Dukascopy hourly BI5 objects: `1085`;
- local files present at inventory time: `37`;
- missing files at inventory time: `1048`;
- duplicate required hours: `0`;
- first missing hour at inventory time: `2004-03-17T13:00:00Z`.

The previously failing `2004-03-17T12:00:00Z` object now exists locally, but its content has not
yet been decode-validated by the controlled preload. These are source-acquisition observations, not
a HYP-0006 result.

## EUR/USD source geometry

Quote source remains:

`DUKASCOPY_HOURLY_TICK_BI5`

RF-027 requests only bounded tick objects around each frozen CPI timestamp and calculates
timestamp-distance geometry only.

Required invariant:

`protected_hyp0005_source_requests = 0`

RF-027 may not write CPI-event return distributions, the HYP-0006 primary inequality or P&L.

## HYP-0005 boundary

HYP-0005 remains separate and unchanged.

Information boundary:

`NO_CONFIRMATORY_OUTCOME_COMPUTED`

## Historical RF-030 gate (completed, not current)

Historical task:

`ATS2-RF-030`

Current artifact:

`research/reviews/HYP-0006-PROTOTYPE-01-REVEAL-GATE.md`

Last completed artifact:

`research/reviews/HYP-0006-PROTOTYPE-01.md`

Frozen RF-028 boundary limits before first reveal:

- `t-60m` and `t+60m`: nearest tick within `30,000 ms`, ties to previous;
- pre-release: last quote strictly before `t`, staleness <= `30,000 ms`;
- duplicate selected millisecond: last raw record;
- BID/ASK: same raw tick record.

The exact-main controlled Dukascopy execute-run was performed once on:

`f3151d8915b61d1a08e79cf27133764201475e65`

Observed result:

- calendar SHA-256:
  `646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9`;
- CPI events: `217`;
- required unique BI5 objects: `1085`;
- existing before/after: `37`;
- missing before/after: `1048`;
- network requests: `1`;
- downloaded objects: `0`;
- failed hour: `2004-03-17T13:00:00Z`;
- failed canonical URL:
  `https://datafeed.dukascopy.com/datafeed/EURUSD/2004/02/17/13h_ticks.bi5`;
- failure: `HTTP 503`;
- controlled status: `SOURCE_BLOCKED`.

Historical OWNER authorization:

`AUTHORIZED_ONCE_BY_OWNER_2026_10_05`

Current execution status:

`SOURCE_BLOCKED_AUTHORIZATION_CONSUMED`

No retry or alternate endpoint is authorized.

This is a technical source-access failure, not a HYP-0006 outcome.

Normal RF-027 Dukascopy runtime is now:

`PROHIBITED`

for live network access. It must use:

`FROZEN_LOCAL_DUKASCOPY_BI5_SNAPSHOT_BUNDLE`

Missing raw tick inputs are classified:

`OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE`

Source-recovery review:

`research/reviews/HYP-0006-DUKASCOPY-SOURCE-RECOVERY.md`

The source-blocker/offline-runtime correction passed exact-head preflight and was squash-merged to
`main` at:

`953b405a63f8077411c817965f96cb9e3aee5d29`

OWNER then performed a bounded manual browser probe using three canonical Dukascopy BI5 URLs. All
three supplied files passed independent BI5 integrity checks; this was source-access evidence only.

OWNER explicitly authorized one bounded browser-assisted pilot on 2026-10-05:

`OWNER_AUTHORIZED_BROWSER_PILOT_50_2026_10_05`

Frozen pilot limits:

- first `50` currently missing frozen BI5 objects;
- canonical Dukascopy URL only;
- maximum `2` browser-open attempts per object;
- after the second unsuccessful attempt: `SKIPPED_AFTER_2_ATTEMPTS`;
- no alternate hostname, mirror, proxy or provider fallback;
- validate before canonical promotion;
- one-shot local consumed sentinel before the first browser-open;
- no HYP-0006 outcome calculation.

Tool:

`tools/hyp0006_dukascopy_browser_pilot.py`

The browser-pilot implementation passed exact-head preflight and was squash-merged to `main` at:

`52b2f9c0755a4efbda49c86c96ace1763a3d47cf`

The one authorized exact-main browser-pilot was executed on:

`c7a10c8bcd84ca4754db92af4c63f39c02101543`

Result:

- objects selected: `50`;
- objects promoted: `50`;
- objects skipped after two attempts: `0`;
- hypothesis outcome computed: `NO`.

Pilot status:

`PASS_50_OF_50_AUTHORIZATION_CONSUMED`

The zero-network post-pilot inventory recount confirmed:

- required canonical BI5 objects: `1085`;
- existing: `87`;
- missing: `998`;
- network requests: `0`;
- downloaded: `0`;
- semantic missing: `0`;
- hypothesis outcome computed: `NO`.

Post-pilot inventory status:

`CONFIRMED_ZERO_NETWORK`

OWNER explicitly authorized one next bounded browser-assisted batch of `250` currently missing
canonical Dukascopy BI5 objects on 2026-10-05.

Authorization marker:

`OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05`

Frozen batch-250 contract:

- first `250` currently missing objects from the deterministic RF-027 inventory;
- canonical Dukascopy URL only;
- maximum `2` browser-open attempts per object;
- after the second unsuccessful attempt: `SKIPPED_AFTER_2_ATTEMPTS`;
- no alternate hostname, mirror, proxy or provider fallback;
- validate before canonical promotion;
- separate one-shot consumed sentinel;
- no HYP-0006 outcome calculation.

Tool:

`tools/hyp0006_dukascopy_browser_batch_250.py`

The batch-250 implementation passed exact-head preflight and was squash-merged to `main` at:

`94e7a91ec96986dd940f2a13575c9ee436b1a354`

The authorized exact-main batch-250 execution completed on:

`438bc59aa6f2cc81a762914f111017f75a2e46b2`

Result:

- objects selected: `250`;
- objects promoted: `250`;
- objects skipped after two attempts: `0`;
- hypothesis outcome computed: `NO`.

Batch status:

`PASS_250_OF_250_AUTHORIZATION_CONSUMED`

The same batch must not be rerun.

Detailed local evidence review passed for all `250 / 250` rows:

- manifest-vs-JSON row identity: `PASS`;
- attempts=1: `250`;
- attempts=2: `0`;
- record-count range: `341..8535`;
- JSON SHA-256:
  `36e1301d551a69990ca707e7bf33da1ce07e5e88b1e7dc23a379a66b814e6b2c`;
- manifest SHA-256:
  `9aa6d7646c809f7a8fb2caaf421f13553ec30ba26dee5d8d991464e1e6cad2e1`.

A subsequent zero-network inventory recount confirmed:

- required: `1085`;
- existing: `337`;
- missing: `748`;
- network requests: `0`;
- downloaded: `0`;
- semantic missing: `0`.

Post-batch inventory status:

`CONFIRMED_ZERO_NETWORK`

OWNER explicitly authorized one next one-shot browser-assisted acquisition of all confirmed `748`
remaining canonical BI5 objects on 2026-10-05.

Frozen remaining-748 contract:

- exactly all `748` current missing deterministic RF-027 objects;
- execution must block if the current missing count is not exactly `748`;
- canonical Dukascopy URL family only;
- maximum `2` browser-open attempts per object;
- after the second unsuccessful attempt: `SKIPPED_AFTER_2_ATTEMPTS` and continue;
- no alternate hostname, mirror, proxy or provider fallback;
- never overwrite an existing canonical local BI5;
- validate BI5 integrity before byte-preserving promotion;
- separate one-shot consumed sentinel before first browser-open;
- no HYP-0006 outcome calculation.

Tool:

`tools/hyp0006_dukascopy_browser_remaining_748.py`

Authorization marker:

`OWNER_AUTHORIZED_REMAINING_748_2026_10_05`

Execution status:

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
- promoted SHA-256: `747/747` unique;
- JSON SHA-256:
  `ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112`;
- skipped object: ordinal `159`, `2011-11-16T11:00:00Z`;
- skipped URL:
  `https://datafeed.dukascopy.com/datafeed/EURUSD/2011/10/16/11h_ticks.bi5`;
- skipped canonical path:
  `data/raw/dukascopy/hyp0006/EURUSD/2011/11/16/11h_ticks.bi5`;
- final failure: `no_valid_bi5_download_within_45s_attempt_2`;
- skipped canonical file: `ABSENT`;
- consumed sentinel: `VALIDATED_PASS`.

OWNER supplied the final missing BI5 for `2011-11-16T11:00:00Z`. It was independently validated
with the frozen RF-027 decoder and copied byte-for-byte into the canonical local path.

Final-object intake evidence:

- SHA-256:
  `391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7`;
- decoder: `PASS`;
- record count: `6810`;
- destination existed before intake: `NO`;
- destination hash after intake: identical.

A post-intake zero-network recount confirmed:

- required: `1085`;
- existing: `1085`;
- missing: `0`;
- network requests: `0`;
- downloaded: `0`;
- semantic missing: `0`.

Bundle status:

`CONFIRMED_ZERO_NETWORK_COMPLETE`

Bundle completeness: `1085 / 1085`.

Current gate: RF-038 hash-only post-reveal result review,
agent/rf038-hyp0005-post-reveal-review.
RF-037 original result CONFIRMATORY_STRUCTURAL_PASS and
one-shot receipt were independently checked against all five
OWNER-supplied artifact SHA-256 values.
No repeat market outcome, first reveal, protected-data
retuning or direct R4/trading Candidate.
OWNER next: exact-head AGENT_PREFLIGHT_REPORT.txt.
