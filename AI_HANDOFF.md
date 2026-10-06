# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: `REJECTED_AT_R3`.
- Strategy #2: `REJECTED_AT_R3`.
- Strategy #3 / HYP-0003: `REJECTED_AT_R3`.
- Strategy #4 / HYP-0005: active confirmatory line; RF-023 remains externally source-blocked.
- Strategy #5 / HYP-0006: active Data Feasibility preparation.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Current executable stage

`Research Factory → Strategy #5 → HYP-0006 → RF-027 Data Feasibility preparation`

RF-027 verifies only official CPI event identity/timing and EUR/USD tick timestamp geometry.

It does **not** compute a HYP-0006 market outcome.

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

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

`research/reviews/HYP-0006-DATA-FEASIBILITY-PREP.md`

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

## Next gate

Current task:

`ATS2-RF-027`

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

`NOT_YET_EXECUTED`

The remaining-748 implementation passed exact-head preflight and was squash-merged to `main` at:

`a8f111ebefe1defa35c201a61253c4ba5c5174d4`

Current gate: run only the exact-main zero-network remaining-748 manifest and review the deterministic
748-object selection. Browser execution must not start before that manifest review. The existing
OWNER authorization remains active and does not need to be reissued.

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

Only after the frozen local BI5 bundle is complete enough for RF-027 and exact-main
`ATS CURRENT TASK CHECK: PASS` plus `ATS TASK LAUNCHER: PASS`:

`ATS2-RF-028 — HYP-0006 pre-reveal data/tolerance freeze`

may begin.
