# HYP-0006 Dukascopy source recovery

**Task:** `ATS2-RF-027`  
**Hypothesis:** `HYP-0006`  
**Status:** `SOURCE_BLOCKED_NO_OUTCOME`  
**Information boundary:** `NO_HYPOTHESIS_OUTCOME_COMPUTED`

## Proven controlled execute-run blocker

OWNER authorized exactly one controlled Dukascopy execute-run on 2026-10-05.

Exact-main commit:

`f3151d8915b61d1a08e79cf27133764201475e65`

Frozen BLS calendar SHA-256:

`646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9`

Observed controlled-run facts:

- CPI events: `217`;
- required unique Dukascopy hourly BI5 objects: `1085`;
- existing before run: `37`;
- missing before run: `1048`;
- network requests: `1`;
- downloaded objects: `0`;
- semantic missing objects: `0`;
- first attempted missing hour: `2004-03-17T13:00:00Z`;
- canonical URL:
  `https://datafeed.dukascopy.com/datafeed/EURUSD/2004/02/17/13h_ticks.bi5`;
- result: `HTTP 503`;
- downloader status: `SOURCE_BLOCKED`.

The one-shot authorization is consumed. No retry, alternate hostname, mirror, proxy or provider
fallback is authorized.

This is:

`TECHNICAL_SOURCE_ACCESS_FAILURE`

It is not a negative HYP-0006 market result.

## Frozen research contract remains unchanged

The blocker does not change:

- market: `FX_SPOT_OTC`;
- instrument: `EURUSD`;
- event class: scheduled U.S. CPI publication;
- development interval:
  `2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z`;
- pre-event horizon: previous 60 minutes;
- post-event horizon: next 60 minutes;
- `PRE_RELEASE_ANCHOR` strictly before public release;
- primary structural claim:
  `median(post_abs_60m_return) > median(pre_abs_60m_return)`;
- HYP-0005 protected-source requests: `0`;
- quote-source semantics:
  `DUKASCOPY_HOURLY_TICK_BI5`.

No HYP-0006 return distribution, primary inequality or trading P&L has been computed.

## Source-recovery decision

Repeated direct runtime access to the canonical Dukascopy BI5 endpoint is no longer treated as a
normal RF-027 dependency.

Preferred recovery architecture:

`FROZEN_LOCAL_DUKASCOPY_BI5_SNAPSHOT_BUNDLE`

The research runtime must consume only local frozen raw BI5 objects and must not automatically fetch
a missing Dukascopy object.

Missing required local objects are classified exactly as:

`OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE`

This preserves the original source semantics because accepted source files remain the exact
Dukascopy hourly `.bi5` objects expected by the frozen RF-027 geometry contract.

The acquisition environment is deliberately separated from the research runtime.

## Required local snapshot contract

Canonical local path:

`data/raw/dukascopy/hyp0006/EURUSD/YYYY/MM/DD/HHh_ticks.bi5`

The required object set remains exactly the mechanically generated `1085` unique hours derived
from the frozen BLS calendar.

For every supplied BI5 object RF-027 must verify before use:

1. the object occupies an expected frozen hour/path;
2. the object decompresses as LZMA;
3. decoded length is a positive multiple of the 20-byte `>IIIff` record;
4. millisecond offsets are ordered and inside the hour;
5. BID and ASK are finite and positive;
6. `ASK >= BID`;
7. volumes are finite and non-negative;
8. raw object SHA-256 is recorded.

Existing valid local objects are not overwritten.

The eventual complete source bundle receives a deterministic SHA-256 before any HYP-0006 outcome
calculation.

## Manual browser probe

OWNER manually requested three canonical Dukascopy BI5 objects for:

- `2004-03-17T13:00:00Z`;
- `2004-03-17T14:00:00Z`;
- `2004-03-17T15:00:00Z`.

All three supplied raw files independently passed the frozen RF-027 BI5 integrity rules:

- valid LZMA payload;
- positive record count;
- decoded length divisible by the 20-byte `>IIIff` record;
- ordered millisecond offsets inside the hour;
- finite positive BID/ASK;
- `ASK >= BID`;
- finite non-negative volumes.

This is source-access/integrity evidence only and is not a HYP-0006 market result.

## Bounded 50-object browser pilot

OWNER authorized one bounded browser-assisted source-intake pilot on 2026-10-05:

`OWNER_AUTHORIZED_BROWSER_PILOT_50_2026_10_05`

Tool:

`tools/hyp0006_dukascopy_browser_pilot.py`

Synthetic tests:

`tests/test_hyp0006_dukascopy_browser_pilot.py`

The pilot contract is:

1. select the first `50` currently missing objects from the deterministic frozen RF-027 inventory;
2. use only the canonical `https://datafeed.dukascopy.com/datafeed` URL already frozen for each hour;
3. open one local browser tab for the exact object URL;
4. treat the attempt as successful only when a valid BI5 for that exact hour appears in the configured Downloads directory;
5. if no valid BI5 appears within the configured wait window, open the same exact URL once more;
6. after the second unsuccessful attempt, record `SKIPPED_AFTER_2_ATTEMPTS` and continue to the next frozen object;
7. maximum attempts per object: `2`;
8. maximum pilot objects: `50`;
9. no alternate hostname, mirror, proxy, provider or third-party fallback;
10. never overwrite an existing canonical local BI5;
11. validate BI5 integrity before byte-preserving promotion into the canonical local path;
12. create a local consumed sentinel before the first browser-open so the whole pilot cannot be accidentally rerun without a new OWNER authorization;
13. write only source-acquisition metadata and hashes;
14. do not compute HYP-0006 returns, the primary inequality or P&L.

The measurable failure criterion is absence of a valid expected BI5 download within the wait window;
the tool does not infer browser DOM/network state.

Exact-main pilot execution:

- git commit: `c7a10c8bcd84ca4754db92af4c63f39c02101543`;
- objects selected: `50`;
- objects promoted after BI5 integrity validation: `50`;
- objects skipped after two attempts: `0`;
- maximum attempts per object: `2`;
- hypothesis outcome computed: `NO`.

Pilot result:

`PASS_50_OF_50_AUTHORIZATION_CONSUMED`

The one-shot browser-pilot authorization is consumed. The same pilot must not be rerun.

A subsequent zero-network controlled inventory recount confirmed the post-pilot local state:

- required unique canonical BI5 objects: `1085`;
- existing: `87`;
- missing: `998`;
- network requests: `0`;
- downloaded: `0`;
- semantic missing: `0`;
- hypothesis outcome computed: `NO`.

Inventory status:

`CONFIRMED_ZERO_NETWORK`

OWNER subsequently authorized one next bounded browser-assisted acquisition batch on 2026-10-05:

`OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05`

Frozen batch-250 contract:

1. select the first `250` currently missing objects from the deterministic RF-027 inventory;
2. use only the same canonical `https://datafeed.dukascopy.com/datafeed` URL family;
3. maximum browser-open attempts per object: `2`;
4. after the second unsuccessful attempt, record `SKIPPED_AFTER_2_ATTEMPTS` and continue;
5. no alternate hostname, mirror, proxy, provider or third-party fallback;
6. never overwrite an existing canonical local BI5;
7. validate BI5 integrity before byte-preserving promotion;
8. write a distinct consumed sentinel before the first browser-open;
9. write source-acquisition metadata and hashes only;
10. do not compute HYP-0006 returns, the primary inequality or P&L.

Tool:

`tools/hyp0006_dukascopy_browser_batch_250.py`

Synthetic tests:

`tests/test_hyp0006_dukascopy_browser_batch_250.py`

Exact-main batch-250 execution:

- git commit: `438bc59aa6f2cc81a762914f111017f75a2e46b2`;
- objects selected: `250`;
- objects promoted after BI5 integrity validation: `250`;
- objects skipped after two attempts: `0`;
- maximum attempts per object: `2`;
- hypothesis outcome computed: `NO`.

Batch result:

`PASS_250_OF_250_AUTHORIZATION_CONSUMED`

The one-shot batch-250 authorization is consumed. The same batch must not be rerun.

Detailed local batch-250 evidence review subsequently passed for all `250 / 250` rows:

Evidence review status:

`FULL_JSON_MANIFEST_REVIEW_PASS`

- JSON top-level contract: `PASS`;
- per-row validation: `PASS`;
- manifest-vs-JSON identity: `PASS`;
- attempts=1: `250`;
- attempts=2: `0`;
- minimum record count: `341`;
- maximum record count: `8535`;
- JSON SHA-256:
  `36e1301d551a69990ca707e7bf33da1ce07e5e88b1e7dc23a379a66b814e6b2c`;
- manifest SHA-256:
  `9aa6d7646c809f7a8fb2caaf421f13553ec30ba26dee5d8d991464e1e6cad2e1`.

The subsequent zero-network inventory recount confirmed:

- required unique canonical BI5 objects: `1085`;
- existing: `337`;
- missing: `748`;
- network requests: `0`;
- downloaded: `0`;
- semantic missing: `0`;
- hypothesis outcome computed: `NO`.

Post-batch inventory status:

`CONFIRMED_ZERO_NETWORK`

OWNER subsequently authorized exactly one browser-assisted acquisition of all `748` confirmed
remaining objects:

`OWNER_AUTHORIZED_REMAINING_748_2026_10_05`

Inventory rule:

`REQUIRE_EXACTLY_748_CURRENT_MISSING`

Frozen remaining-748 contract:

1. the deterministic inventory must report exactly `748` current missing objects or execution blocks;
2. select all of those `748` missing objects, not a subset;
3. use only the canonical `https://datafeed.dukascopy.com/datafeed` URL family;
4. maximum browser-open attempts per object: `2`;
5. after the second unsuccessful attempt, record `SKIPPED_AFTER_2_ATTEMPTS` and continue;
6. no alternate hostname, mirror, proxy, provider or third-party fallback;
7. never overwrite an existing canonical local BI5;
8. validate BI5 integrity before byte-preserving promotion;
9. write a distinct consumed sentinel before the first browser-open;
10. write source-acquisition metadata and hashes only;
11. do not compute HYP-0006 returns, the primary inequality or P&L.

Tool:

`tools/hyp0006_dukascopy_browser_remaining_748.py`

Synthetic tests:

`tests/test_hyp0006_dukascopy_browser_remaining_748.py`

Manifest status: `MANIFEST_REVIEW_PASS_748_OF_748`.
Manifest SHA-256: `a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4`.

Exact-main execution: `0131dd82d286814adaa76ff6e2524e0d000ca13c`.
Result: `748` selected / `747` promoted / `1` skipped.
Execution status: `PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED`.

The one-shot authorization is consumed and the same batch must not be rerun.
Expected inventory is `1084 / 1085` present and `1` missing pending detailed JSON review and
zero-network recount.
Information boundary:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

## Acquisition architectures considered

### A. Frozen canonical BI5 snapshot bundle — preferred

Acquire the exact required raw BI5 bytes from Dukascopy in a separate explicitly authorized
source-acquisition environment, preserve their canonical hour identities, then move the immutable
bundle into the local raw path.

Advantages:

- preserves `DUKASCOPY_HOURLY_TICK_BI5` exactly;
- no provider substitution;
- no price transformation;
- deterministic local runtime after intake;
- raw bytes and SHA-256 remain auditable.

Any external acquisition attempt still requires a new explicit OWNER authorization. This document
does not authorize one.

### B. Official Dukascopy Historical Data / JForex tick export — candidate only

Dukascopy documents official historical tick retrieval through its Historical Data Feed and JForex
historical-data interfaces.

This is the same provider, but it is a different acquisition interface and may transform the raw
representation. It is therefore not automatically equivalent to the frozen BI5 contract.

Before this route could be accepted it would require a Data Feasibility equivalence gate against
locally existing BI5 objects, including timestamp/BID/ASK equality on predefined overlap hours.
No performance metric may be used in that equivalence decision.

Official references for architecture review:

- `https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/history-ticks/`
- `https://www.dukascopy.com/swiss/english/marketwatch/historical/`

### C. Another direct BI5 retry — not current gate

A later retry of the canonical endpoint would preserve source semantics, but the same source family
has now produced repeated HTTP 503 blockers and the one-shot authorization is consumed.

No retry is authorized.

### D. Third-party market-data provider — not permitted as fallback

A third-party provider is not an automatic source replacement.

Using one would require an explicit Data Feasibility/source-identity decision and would no longer be
the frozen `DUKASCOPY_HOURLY_TICK_BI5` source contract.

## Current gate

The one authorized remaining-748 execution is complete with `747 / 748` promoted and `1` skipped.
Its authorization is consumed.

Current action: review all `748` detailed JSON rows, identify the skipped object and its failure
metadata, then perform a zero-network inventory recount.

No repeat execution or new source request is authorized. The frozen source identity and research
rules remain unchanged.

Only after an approved frozen local BI5 bundle is complete enough for RF-027 and exact-main
`ATS CURRENT TASK CHECK: PASS` plus `ATS TASK LAUNCHER: PASS` may
`ATS2-RF-028 — HYP-0006 pre-reveal data/tolerance freeze` begin.
