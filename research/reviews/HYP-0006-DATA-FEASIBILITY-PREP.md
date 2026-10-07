# HYP-0006 Data Feasibility Preparation

Task: `ATS2-RF-027`  
Hypothesis ID: `HYP-0006`  
Status: `PREPARATION_PROTOCOL_FROZEN_OFFLINE_BLS_SNAPSHOTS`  
Date: 29 September 2026

## Purpose

RF-027 machine-verifies the official U.S. CPI event denominator and granular EUR/USD BID/ASK
timestamp geometry required by HYP-0006.

RF-027 computes **no HYP-0006 return, pre/post distribution, primary inequality or trading P&L**.

## Why the source architecture changed

Two exact-main RF-027 attempts passed Local CI and then failed before event acquisition because the
official BLS website returned HTTP 403 to the automated client:

- `a4c6331949e9c71fc68eb1baa870d20a03518d48`;
- `2ce019bb51b0e45e900c0555ed44be5a3433e23a`.

Both failures are classified:

`TECHNICAL_SOURCE_ACCESS_FAILURE`

They are not HYP-0006 negative results.

The repeated access failure proves that normal RF-027 execution must not depend on live BLS HTTP
availability.

## Frozen development interval

Only CPI events with official BLS scheduled release timestamp inside:

`2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z`

may enter this preparation.

Evidence classification:

`DEVELOPMENT / EXPLORATORY ONLY`

## Canonical BLS source architecture

The official source class remains the U.S. Bureau of Labor Statistics.

Live BLS network access during normal RF-027 runtime is:

`PROHIBITED`

Canonical source intake is a one-time set of official annual BLS schedule snapshots.

Manifest:

`data/reference/HYP-0006-BLS-SCHEDULE-SNAPSHOT-MANIFEST.csv`

Required years:

`2003..2021`

Required raw snapshot location:

`data/raw/bls/hyp0006/schedules/YYYY.html`

OWNER intake instructions:

`research/reviews/HYP-0006-BLS-SNAPSHOT-INTAKE.md`

Raw snapshots are not committed to Git.

For every snapshot RF-027 records:

- official source URL;
- local raw snapshot path;
- SHA-256;
- calendar year.

## Frozen local CPI calendar

RF-027 derives a local event calendar from the 19 official schedule snapshots:

`data/derived/HYP-0006-BLS-CPI-CALENDAR-2003-2021.csv`

The calendar contains only:

- event identity;
- local release date;
- local release clock time;
- UTC release timestamp;
- historical U.S. Eastern timezone semantics;
- official BLS schedule label;
- same-time BLS release labels;
- source year;
- official source URL;
- raw snapshot identity and SHA-256.

It contains no market price, return or P&L field.

Result source identity:

`BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS`

Timestamp semantics:

`BLS_ANNUAL_SCHEDULE_US_EASTERN`

## Historical U.S. Eastern conversion

Annual BLS schedule clock times are interpreted as U.S. Eastern Time.

Historical DST rule:

- through 2006: first Sunday in April through last Sunday in October;
- from 2007 onward: second Sunday in March through first Sunday in November.

UTC conversion is deterministic and is performed before any EUR/USD observation is selected.

## Event denominator

The denominator is every official BLS schedule row identifying the Consumer Price Index whose
converted release timestamp lies inside the frozen development interval.

No event may be removed because of future EUR/USD behavior.

Duplicate CPI rows for the same date are allowed only if their official release clock is identical.
Conflicting official clock times are blocking.

Same-time BLS event policy:

`FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION`

## Missing source inputs

If one or more required BLS annual snapshot files are absent, RF-027 must stop with:

`OWNER_INPUT_REQUIRED_BLS_SCHEDULE_SNAPSHOTS`

This is an OWNER input requirement, not a Hypothesis result and not a data-feasibility rejection.

Malformed/unparseable official snapshot content is a technical/source-integrity blocker.

RF-027 must never silently fall back to:

- a third-party economic calendar;
- inferred monthly dates;
- current BLS pages substituted for missing historical snapshots;
- manually typed event dates;
- live BLS HTTP retrieval.

## Granular EUR/USD source

Quote source remains:

`DUKASCOPY_HOURLY_TICK_BI5`

Candidate endpoints recorded for architecture review:

1. `https://datafeed.dukascopy.com/datafeed`
2. `https://www.dukascopy.com/datafeed`

Runtime source-access rule:

`FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF`

After the controlled execute-run blocker recorded on 2026-10-05, normal RF-027 execution is
offline-only for Dukascopy tick objects.

Normal RF-027 Dukascopy network mode:

`PROHIBITED`

Missing local BI5 objects must stop the normal preparation path as:

`OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE`

The second candidate endpoint is **not** an automatic fallback. A later external acquisition attempt,
alternate hostname, official alternate interface, mirror, proxy or provider substitution requires a
separate explicit source-architecture decision and any required OWNER authorization.

## OWNER-authorized controlled Dukascopy preload

The latest offline inventory was derived from the locally generated BLS calendar with SHA-256:

`646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9`

Observed inventory:

- CPI events: `217`;
- required unique hourly BI5 objects: `1085`;
- locally existing at inventory time: `37`;
- missing at inventory time: `1048`;
- duplicate required hours: `0`;
- first missing hour after the inventory: `2004-03-17T13:00:00Z`.

These counts are source-acquisition observations only. They do not freeze the later RF-028 data
admission decision and they do not evaluate the HYP-0006 primary claim.

OWNER authorized **preparation of a controlled downloader** on 2026-10-02. This authorization does
not authorize network execution.

Controlled tool:

`tools/hyp0006_dukascopy_controlled_download.py`

Offline/default invocation:

`uv run --frozen python -m tools.hyp0006_dukascopy_controlled_download`

A later network execution, only after separate explicit OWNER authorization, uses:

`uv run --frozen python -m tools.hyp0006_dukascopy_controlled_download --execute --owner-authorized`

Its contract is:

1. default mode is offline inventory only and performs zero network requests;
2. execute mode requires both `--execute` and `--owner-authorized`;
3. inventory must match the observed BLS calendar SHA-256, 217 CPI events and 1085 unique required
   hourly objects before any network request;
4. only `https://datafeed.dukascopy.com/datafeed` is used in one execution;
5. existing local BI5 objects are never overwritten;
6. every newly downloaded object is decoded and source-integrity checked before atomic promotion
   from a temporary file;
7. HTTP/network/access failure stops the run immediately under
   `FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF`;
8. there is no retry, second endpoint, mirror, proxy or provider fallback;
9. protocol-defined 404/410 missing objects are recorded as source-availability observations and
   are not retried;
10. the tool may write only acquisition/inventory metadata and may not compute returns, the primary
    HYP-0006 inequality or P&L.

Historical network authorization:

`AUTHORIZED_ONCE_BY_OWNER_2026_10_05`

The exact authorized execute-run was consumed on exact-main commit
`f3151d8915b61d1a08e79cf27133764201475e65`.

Observed result:

- status: `SOURCE_BLOCKED`;
- network requests: `1`;
- downloaded objects: `0`;
- existing after run: `37`;
- missing after run: `1048`;
- failed hour: `2004-03-17T13:00:00Z`;
- failed canonical URL:
  `https://datafeed.dukascopy.com/datafeed/EURUSD/2004/02/17/13h_ticks.bi5`;
- failure: `HTTP 503`.

Current controlled-execution status:

`SOURCE_BLOCKED_AUTHORIZATION_CONSUMED`

Any later execute-run requires a new explicit OWNER authorization. No retry is currently authorized.

Source-recovery architecture:

`FROZEN_LOCAL_DUKASCOPY_BI5_SNAPSHOT_BUNDLE`

Canonical recovery review:

`research/reviews/HYP-0006-DUKASCOPY-SOURCE-RECOVERY.md`

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

## Bounded browser-assisted source-intake pilot

A manual browser probe established that three canonical Dukascopy BI5 files supplied by OWNER pass
the frozen raw BI5 integrity rules.

OWNER then authorized one bounded pilot:

`OWNER_AUTHORIZED_BROWSER_PILOT_50_2026_10_05`

Frozen pilot parameters before execution:

- selected set: first `50` currently missing objects from the deterministic RF-027 inventory;
- source URL family: canonical `https://datafeed.dukascopy.com/datafeed` only;
- browser-open attempts per selected object: maximum `2`;
- success criterion: a valid BI5 for the exact expected hour appears in the configured Downloads
  directory and passes the existing RF-027 integrity decoder;
- after the second unsuccessful attempt:
  `SKIPPED_AFTER_2_ATTEMPTS`;
- no alternate hostname, mirror, proxy or provider fallback;
- no overwrite of an existing canonical local BI5;
- byte-preserving promotion only after integrity validation;
- one-shot local consumed sentinel is written before the first browser-open;
- the pilot writes source-acquisition metadata/hashes only;
- no returns, HYP-0006 primary inequality or P&L.

Tool:

`tools/hyp0006_dukascopy_browser_pilot.py`

Synthetic tests:

`tests/test_hyp0006_dukascopy_browser_pilot.py`

The pilot does not attempt to infer browser DOM state. An attempt is operationally unsuccessful when
no valid expected BI5 appears within the configured wait window.

Pilot execution status before exact-main execution:

`NOT_YET_EXECUTED`

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

## Authorized bounded browser batch 250

After the 50-object pilot passed `50/50` and a zero-network recount confirmed
`87 / 1085` canonical BI5 objects present with `998` missing, OWNER authorized one next bounded
browser-assisted batch:

`OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05`

Frozen before execution:

- first `250` current missing RF-027 BI5 objects;
- canonical Dukascopy URL only;
- maximum `2` attempts per object;
- `SKIPPED_AFTER_2_ATTEMPTS` after the second unsuccessful attempt;
- no alternate endpoint/provider fallback;
- validate before promotion;
- separate one-shot consumed sentinel;
- no returns, primary inequality or P&L.

Tool:

`tools/hyp0006_dukascopy_browser_batch_250.py`

Exact-main execution:

- git commit: `438bc59aa6f2cc81a762914f111017f75a2e46b2`;
- selected: `250`;
- promoted: `250`;
- skipped after two attempts: `0`;
- hypothesis outcome computed: `NO`.

Execution status:

`PASS_250_OF_250_AUTHORIZATION_CONSUMED`

Detailed JSON/manifest evidence review status:

`FULL_JSON_MANIFEST_REVIEW_PASS`

Observed evidence:

- rows checked: `250 / 250`;
- attempts=1: `250`;
- attempts=2: `0`;
- record-count range: `341..8535`;
- JSON SHA-256:
  `36e1301d551a69990ca707e7bf33da1ce07e5e88b1e7dc23a379a66b814e6b2c`;
- manifest SHA-256:
  `9aa6d7646c809f7a8fb2caaf421f13553ec30ba26dee5d8d991464e1e6cad2e1`.

Zero-network recount confirmed `337 / 1085` present and `748` missing, with `0` network
requests, `0` downloaded and `0` semantic missing.

Post-batch inventory status:

`CONFIRMED_ZERO_NETWORK`

OWNER then authorized exactly one source-acquisition batch covering all `748` confirmed remaining
canonical BI5 objects.

Authorization:

`OWNER_AUTHORIZED_REMAINING_748_2026_10_05`

Inventory rule:

`REQUIRE_EXACTLY_748_CURRENT_MISSING`

The remaining-748 runner must require exactly `748` current missing objects, use canonical
Dukascopy only, permit at most `2` attempts per object, continue with
`SKIPPED_AFTER_2_ATTEMPTS`, never overwrite an existing object, use no alternate provider/endpoint
fallback, consume its authorization before the first browser-open and compute no HYP-0006 outcome.

Tool:

`tools/hyp0006_dukascopy_browser_remaining_748.py`

Implementation merge:

`a8f111ebefe1defa35c201a61253c4ba5c5174d4`

Manifest status: `MANIFEST_REVIEW_PASS_748_OF_748`.
Manifest SHA-256: `a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4`.

Exact-main execution: `0131dd82d286814adaa76ff6e2524e0d000ca13c`.
Result: `748` selected / `747` promoted / `1` skipped.
Execution status: `PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED`.

Repeat execution is prohibited.

Detailed evidence review status:

`FULL_JSON_MANIFEST_REVIEW_PASS`

Observed evidence:

- rows checked: `748 / 748`;
- attempts=1: `746`;
- attempts=2: `2`;
- promoted record-count range: `419..31693`;
- promoted SHA-256 rows: `747`;
- promoted unique SHA-256: `747`;
- duplicate promoted SHA-256: `0`;
- JSON SHA-256:
  `ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112`;
- skipped ordinal: `159`;
- skipped hour: `2011-11-16T11:00:00Z`;
- skipped final failure: `no_valid_bi5_download_within_45s_attempt_2`;
- skipped canonical file: `ABSENT`;
- consumed sentinel validation: `PASS`.

OWNER supplied the final missing BI5 for `2011-11-16T11:00:00Z`.

Final manual intake evidence:

- SHA-256:
  `391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7`;
- frozen decoder: `PASS`;
- record count: `6810`;
- destination existed before: `NO`;
- byte-preserving canonical copy: `PASS`.

Post-intake zero-network recount:

- required objects: `1085`;
- existing: `1085`;
- missing: `0`;
- network requests: `0`;
- downloaded: `0`;
- semantic missing: `0`;
- HYP-0006 outcome computed: `NO`.

Bundle status:

`CONFIRMED_ZERO_NETWORK_COMPLETE`

Bundle completeness: `1085 / 1085`.

## Exact-main RF-027 completion

Exact-main commit:

`bbbdbd301b610dfc61316c9ff82015fb0e039a47`

Completion gates:

- `ATS CURRENT TASK CHECK: PASS`;
- `ATS TASK LAUNCHER: PASS`;
- Local CI: `PASS`;
- preparation decision: `READY_FOR_DATA_FEASIBILITY_FREEZE`.

Final preparation evidence:

- BLS snapshots: `19`;
- candidate/resolved CPI events: `217 / 217`;
- complete timestamp-geometry events: `217 / 217`;
- required/acquired BI5 objects: `1085 / 1085`;
- missing BI5 objects: `0`;
- protected HYP-0005 source requests: `0`;
- BLS snapshot manifest SHA-256:
  `3837c463b36914c2276e9985a8a70a8ead13ca0e4b16901a22cb4fd2dece6ee4`;
- BLS snapshot bundle SHA-256:
  `5306799d4c4196941d701e661df2fa4255682783b966e7bcfd69f702a1ead341`;
- BLS calendar SHA-256:
  `646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9`;
- source bundle SHA-256:
  `5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425`;
- geometry CSV SHA-256:
  `e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034`.

RF-027 outcome metrics computed: `NO`.
RF-027 primary claim evaluated: `NO`.

Current gate:

`ATS2-RF-028 — HYP-0006 pre-reveal data/tolerance freeze`.

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

Object path:

`EURUSD/{YEAR}/{ZERO_BASED_MONTH}/{DAY}/{HOUR}h_ticks.bi5`

Each object is LZMA-compressed and must decode into 20-byte big-endian records:

`>IIIff`

RF-027 validates:

- ordered millisecond timestamps;
- finite positive BID/ASK;
- `ASK >= BID`;
- finite non-negative volume fields.

Quote prices are inspected only for source integrity and are not written to the BLS calendar or
geometry dataset.

## Bounded tick-object rule

For each frozen CPI timestamp `t`, RF-027 requests only hourly objects spanning:

`floor(t - 60m) - 1h` through `floor(t + 60m) + 1h`

inclusive.

This permits timestamp-only geometry around:

- `t - 60m`;
- strictly before `t`;
- `t + 60m`.

RF-027 must reject any request outside the development interval or inside either frozen HYP-0005
unseen segment.

Required invariant:

`protected_hyp0005_source_requests = 0`

## Geometry only

RF-027 may calculate only timestamp/source geometry:

- nearest previous/next tick distance around `t - 60m`;
- last tick distance strictly before `t`;
- nearest previous/next tick distance around `t + 60m`;
- missing tick-object count;
- duplicate tick-timestamp count;
- source object hashes;
- event counts;
- same-time BLS flags.

RF-027 does not freeze the final numeric anchor tolerance. That is RF-028 work.

## Local outputs

Machine result:

`reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP.json`

Shareable summary:

`reports/local_ci/HYP0006_DATA_FEASIBILITY_PREP_REPORT.txt`

Frozen-calendar candidate:

`data/derived/HYP-0006-BLS-CPI-CALENDAR-2003-2021.csv`

Tick geometry:

`data/derived/HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv`

## Valid preparation decisions

`READY_FOR_DATA_FEASIBILITY_FREEZE`

Meaning: all required official BLS snapshots are present and parseable, the CPI denominator is
non-empty, event times are deterministic, HYP-0005 protected requests are zero, and at least one
event has complete granular tick timestamp geometry.

`UNRESOLVED_OFFICIAL_EVENT_TIMES`

Meaning: official snapshot content cannot produce an unambiguous CPI release timestamp.

`INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY`

Meaning: BLS calendar preparation succeeds but the bounded Dukascopy pass produces no event with
complete timestamp geometry.

These are Data Feasibility preparation decisions, not HYP-0006 market outcomes.

## Explicitly prohibited RF-027 output

RF-027 must not calculate or write:

- `pre_abs_60m_return`;
- `post_abs_60m_return`;
- return mean/median/quantile/distribution;
- the primary HYP-0006 inequality;
- directional event returns;
- trading P&L.

Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

## Next step

After exact-main RF-027 PASS and review of the preparation JSON:

`ATS2-RF-028 — HYP-0006 pre-reveal data/tolerance freeze`

must freeze the exact BLS calendar SHA-256, source snapshot bundle SHA-256, eligible-event rules,
Dukascopy source identity and numeric anchor tolerances before any HYP-0006 outcome calculation.
