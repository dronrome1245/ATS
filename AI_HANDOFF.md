# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline complete; full M4.9/M4.10 awaits S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategies #1–3: `REJECTED_AT_R3`.
- Strategy #4: `IDEA-0004 / HYP-0005` **CURRENT PRIORITY**.
- Strategy #5: HYP-0006 development structural reveal preserved
  as `DEVELOPMENT_REVEALED_EXPLORATORY_ONLY`; HYP-0007 confirmatory
  data independence remains pending.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Current executable stage

`Research Factory → HYP-0005 → RF-036 gate 4/5 preparation ONLY`

Research plan: `4/5` major step is OPEN and NOT REVEALED;
technical substep `4.1/5` stages the authorization and
pre-result verification protocol. Earlier 1/5 and 2/5 PASSED.

Latest completed Technical ID: `ATS2-RF-035`.
Its exact-main OWNER PASS:
`9da36dba228d4fa55c3068a01cabc7f215aa7e02`.
Verified 267 pytest PASS, validator, Ruff lint/format, full
Local CI, exact CLEAN HEAD, frozen inputs, task and launcher PASS.
OWNER report SHA-256:
`d7833785bee462c7b122479de22eae041329f42e24d38a1e7481ae4286aeff1b`.

Current Technical ID: `ATS2-RF-036`.
OWNER approved **preparation only**, not a first reveal.
New gate artifact:
`research/reviews/HYP-0005-PROTOTYPE-01-REVEAL-GATE.md`.
Last completed tracked artifact:
`research/reviews/HYP-0005-PROTOTYPE-01.md`.
This remains the original HYP-0005 research attempt;
no new Hypothesis/Idea or search over rules.

Data frozen by RF-024 on
`dd014ef6a1014edcfaa26f7d735478aee0cc94ef`:
`DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0`.
Manifest:
`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001.yaml`.
Source-bundle SHA-256:
`65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2`.
CSV:
`data/derived/HYP-0005-CONF-01-EURUSD-H1.csv`;
SHA-256:
`b1091c4975665b2b0cd4f58627a10aceaab7aeff5076431abb6abc74c0a054c1`.
2010 rows, 1991 exact-next-hour eligible;
CORE_ACTIVE 838 / OFF_HOURS 837 / TRANSITION 316;
LEFT_UNSEEN 1542 / RIGHT_UNSEEN 449; three LEFT market-hour gaps.
Frozen periods:
LEFT `[2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)`;
RIGHT `[2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)`.
Original HYP-0004 development interval fully consumed,
never eligible for HYP-0005.

Frozen runner:
`tools/hyp0005_proto01.py`
Git blob `814193997768605fe60607d66dfd755a9323f339`.
Inherited arithmetic code Git blob
`cbc9a46bf5e5296615f51c0ea564153968bc2a55`.
Two frozen primary comparisons:
`median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)`;
`median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)`.
TRANSITION and year slices diagnostic only, no tuning.
The decision is structural, nondirectional, not trading P&L;
a positive result creates no Candidate, R4 or independent status.
Data semantics remain `CONDITIONAL / H1_OPEN_PROXY_AT_EVENT_TIME`,
`exact_tick_boundary_time_known=false`.
September vendor origin still
`USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER`.

RF-036 stages only protocol, state sync, synthetic tests and
a no-reveal metadata-only current-task gate.
Agent preflight and merged exact-main task checker must NOT
call `run_first_reveal_once` or compute median/returns/spreads;
first reveal needs a distinct future OWNER one-shot authorization,
technical launch gate and result preservation.
Direct frozen runner CLI exits 2.

Information boundaries:
- HYP-0005: `NO_CONFIRMATORY_OUTCOME_COMPUTED`;
- first reveal: `NOT_AUTHORIZED / NOT_EXECUTED`;
- HYP-0006: `DEVELOPMENT_REVEALED_EXPLORATORY_ONLY`;
- HYP-0007: `NO_CONFIRMATORY_OUTCOME_COMPUTED`.

OWNER next **after RF-036 PR is created**:
run `.\\ATS_AGENT_PREFLIGHT.bat` at exact agent HEAD,
send `reports/local_ci/AGENT_PREFLIGHT_REPORT.txt`.
GPT squash-merges only after validated exact-head PASS;
then OWNER runs `.\\ATS_TASK_CHECK.bat` on merged exact main.
Those gates close preparation only and never reveal HYP-0005.

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

`research/reviews/HYP-0005-PROTOTYPE-01-REVEAL-GATE.md`

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

Current gate: RF-036 `agent/rf036-hyp0005-first-reveal-gate-prep`
exact-head OWNER preflight, synthetic and metadata-only, followed
by GPT squash merge and exact-main task check. RF-035 was
CLOSED exact-main OWNER PASS at
`9da36dba228d4fa55c3068a01cabc7f215aa7e02`.
No first confirmatory reveal authorization exists.
No change to original HYP-0005 formulas, 2010-row data,
1991 eligible observations, frozen code/hash or source
provenance. `NO_CONFIRMATORY_OUTCOME_COMPUTED`.
