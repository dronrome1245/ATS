# HYP-0003 Data Feasibility Preparation

Task: `ATS2-RF-006`  
Hypothesis ID: `HYP-0003`  
Status: `PREPARATION_PROTOCOL_FROZEN`  
Date: 23 September 2026

## Purpose

This task machine-verifies the predeclared nine-symbol Dukascopy source universe before ATS downloads the full HYP-0003 development dataset.

It computes **no momentum feature, ranking, basket return or 25-cell development result**.

## Candidate universe

The source candidates remain fixed from RF-005:

`AUDUSD, USDCAD, USDCHF, EURUSD, GBPUSD, USDJPY, USDNOK, NZDUSD, USDSEK`

Currency inclusion/exclusion is allowed only for source/data feasibility, never for strategy performance.

Minimum source-qualified currency count:

`6`

## Protected evidence boundary

The HYP-0003 development preparation must not read or download source months at or after:

`2021-09-01T00:00:00Z`

The reserved tail remains:

`2021-09-01T00:00:00Z <= time < 2026-09-01T00:00:00Z`

The availability search ceiling is therefore August 2021.

## Probe method

Canonical tool:

`tools/hyp0003_data_feasibility.py`

For each candidate symbol the tool:

1. downloads or reuses Dukascopy `metadata/HistoryStart.bi5`;
2. parses the big-endian history-start table and reads the H1 start timestamp for the symbol;
3. verifies August 2021 BID and ASK monthly H1 availability;
4. decompresses each August 2021 probe object and validates the BI5 record structure;
5. records record count, first/last source timestamps and SHA-256;
6. derives the common possible development start from the latest H1 metadata start among source-qualified currencies;
7. hashes the HistoryStart identity plus boundary probe identities into one `probe_bundle_sha256`.

This replaces the earlier binary search across arbitrary old monthly URLs. Repeated HTTP 503 responses on a 1997 availability probe showed that historical content URLs are not a reliable protocol for discovering provider inception. Dukascopy's dedicated history-start metadata is the appropriate source-discovery mechanism.

The metadata/probe path never calculates strategy returns.

## Important hash boundary

`probe_bundle_sha256` identifies only the RF-006 availability/integrity probes.

It includes the Dukascopy `HistoryStart.bi5` SHA-256 plus the August 2021 BID/ASK boundary probes. It is **not** the future HYP-0003 development dataset hash and is **not** the full source-bundle hash for the future development dataset.

Those identities require the later full-data preparation task.

## Valid preparation outcomes

`READY_FOR_FREEZE_REVIEW`

At least six candidate currencies have both-sided source availability through the development boundary and a common development start can be established.

`INSUFFICIENT_SOURCE_UNIVERSE`

Fewer than six candidates satisfy the availability probe. This is a valid negative Data Feasibility preparation result, not a software failure.

Technical network/decompression/consistency failures block the task and must not be reclassified as missing source data.

## Local outputs

The tool writes:

- `reports/local_ci/HYP0003_DATA_FEASIBILITY.json`
- `reports/local_ci/HYP0003_DATA_FEASIBILITY_REPORT.txt`

Both outputs are disposable local runtime evidence and remain ignored by Git.

## Information boundary

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

No HYP-0003 parameter cell is evaluated in RF-006.

## Next step

After exact-head OWNER launcher PASS and review of the machine preparation report:

`ATS2-RF-007 — HYP-0003 Data Feasibility freeze`

RF-007 will canonically record the source-qualified universe/common coverage decision. Full historical development bytes will be acquired only under the subsequently frozen dataset-preparation contract.
