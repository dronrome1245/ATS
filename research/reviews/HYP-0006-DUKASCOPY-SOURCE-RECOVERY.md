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

Prepare and validate the offline-only RF-027 architecture so that:

- normal RF-027 execution never performs live Dukascopy HTTP access;
- missing BI5 files are classified as source input still required, not as a market result;
- the controlled execute-run remains a historical acquisition record only;
- no HYP-0006 outcome can be revealed while the source bundle is incomplete.

Only after an approved frozen local BI5 bundle is complete enough for RF-027 and exact-main
`ATS CURRENT TASK CHECK: PASS` plus `ATS TASK LAUNCHER: PASS` may
`ATS2-RF-028 — HYP-0006 pre-reveal data/tolerance freeze` begin.
