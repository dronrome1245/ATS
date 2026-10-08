# HYP-0005 RF-023 — Official Frozen Snapshot Intake (Offline Repair)

Task: `ATS2-RF-032` — source-access repair within **existing** `ATS2-RF-023`
Research gate: `HYP-0005 1/5` (source-preparation; **not** a new research step)
Status: `SOURCE_INPUT_REQUIRED_2026_09`
Information boundary: `NO_CONFIRMATORY_OUTCOME_COMPUTED`

## Reason for repair / known evidence

Original frozen preparation contract:
`research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md`.
Original RF-023 source/geometry runner:
`tools/hyp0005_data_feasibility.py`.

The 2026-09 source access failure on 2026-09-28 was **Jetta BID and
ASK HTTP 400 "From time is too late"**, with BI5 HTTP 503 under the
separate diagnostic. These are external failures, not a market result.

OWNER's subsequent 2026-10-08 offline file-only inventory reported:
- complete nonempty same-format Jetta JSON BID/ASK files for 2003-05,
  2003-06, 2003-07 and 2003-08;
- an additional nonempty BI5 pair for 2003-08;
- **neither JSON nor BI5 side exists for 2026-09**;
- no RF-023 preparation JSON, TXT or derived CSV yet;
- git `main@1ff81954fa1918975a9d19ce94c3f8c926fecb96` CLEAN.
File presence and matched file format are **not** decoded BID/ASK
coherence or certified provider provenance. No protected price content
was opened and no hypothesis outcome was computed.

RF-032 hardens the same source architecture for deterministic **local-only**
intake and blocks all HTTP requests, automatic retry/backoff and
network fallback from ordinary RF-023. This is infrastructure/source-access
repair; it does not change the frozen source family, dates, sample,
bucket mapping, formulas, or hypothesis/decision criteria.
`HYP-0005` remains `SOURCE_INPUT_REQUIRED` until an official,
verifiable source pair is available.

## Exact source identity — do not alter

Instrument: `EURUSD`, Dukascopy H1 paired `BID` + `ASK` candles.

Frozen `LEFT_UNSEEN`:
`[2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)`.

Frozen `RIGHT_UNSEEN`:
`[2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)`.

Frozen consumed interval (not independent for HYP-0005):
`[2003-08-03T21:00:00Z, 2026-09-01T00:00:00Z)`.

The required source months remain exactly
`2003-05, 2003-06, 2003-07, 2003-08, 2026-09`.
For each month select **one complete BID+ASK source format**. Prefer
an existing complete official Jetta JSON pair, then an existing
complete official legacy Dukascopy BI5 pair. Never combine different
formats for BID and ASK. Partial/corrupt pairs block preparation
rather than silently being repaired by a network request.

## Official source URL and canonical filename: missing month only

No external request is authorized by RF-032.

**Option A — canonical Jetta JSON (preferred if official raw bytes can
be obtained):**

| Side | Official source URL | Byte-preserved canonical local path |
|---|---|---|
| BID | `https://jetta.dukascopy.com/v1/candles/hour/EUR-USD/BID/2026/9` | `data/external/dukascopy/EURUSD/H1/2026/09/BID_candles_hour_1.json` |
| ASK | `https://jetta.dukascopy.com/v1/candles/hour/EUR-USD/ASK/2026/9` | `data/external/dukascopy/EURUSD/H1/2026/09/ASK_candles_hour_1.json` |

**Option B — already permitted official legacy BI5 source architecture,
only if separately selected after observing an actual official access
blocker:**

| Side | Official source URL | Byte-preserved canonical local path |
|---|---|---|
| BID | `https://datafeed.dukascopy.com/datafeed/EURUSD/2026/08/BID_candles_hour_1.bi5` | `data/external/dukascopy/EURUSD/H1/2026/09/BID_candles_hour_1.bi5` |
| ASK | `https://datafeed.dukascopy.com/datafeed/EURUSD/2026/08/ASK_candles_hour_1.bi5` | `data/external/dukascopy/EURUSD/H1/2026/09/ASK_candles_hour_1.bi5` |

For legacy BI5 the URL uses Dukascopy's **zero-based month**
(`08` means September). Do not confuse that provider URL with the
canonical `2026/09` local directory.

These URLs are derived from existing ATS frozen provider-native
source functions. **Availability as of 2026-10-08 has not been
verified; DO NOT assume the 2026-09 pair is downloadable.**

## Required provenance at future intake

Only after a separate explicit OWNER source-access decision:
1. If an official pair becomes genuinely available, capture raw BID and
   ASK response bytes without editing/reformatting/recompressing them.
2. Preserve the original official URL for each side; capture UTC
   acquisition time, byte size, SHA-256, response content type and
   Last-Modified/ETag if supplied, and access/license notes.
3. Write the two raw files atomically to the exact paths for **one**
   selected format; never overwrite any preexisting file or the
   existing 2003 snapshots. Reject partial or mixed-format intake.
4. Check provider-native format and BID/ASK timestamp/record geometry
   **only in a later separately gated offline RF-023 preparation**.
   No outcome columns or price-performance statistics before freeze.
5. Retain immutable source hashes for RF-024 formal dataset freeze.

Do not substitute the source with a third-party vendor or select a
favorable alternative interval. If official acquisition fails, record
exact HTTP/OS failure once; stop and request an architecture decision.
Do not launch repeated probes, automatically cycle hosts, or
present source failure as `INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY`.

## RF-032 completion boundary

RF-032 can complete its *technical offline architecture* on exact main
even while September is missing, returning
`SOURCE_INPUT_REQUIRED_2026_09` for the research gate.

Its exact-main checker may validate existing file presence/size/SHA-256,
governance, and synthetic code tests. It **must not** run RF-023
preparation, open/decode protected price rows, request the network,
compute HYP-0005 outcomes, or write the derived confirmatory CSV.

Source provisioning and the frozen RF-023 data preparation remain
separate gates after this technical repair.
HYP-0006 first reveal and HYP-0007 must not consume the HYP-0005
protected files.

No confirmatory dataset is frozen, no Hypothesis is rejected, and no
Candidate/R4/Strategy Version or trading P&L result exists here.
