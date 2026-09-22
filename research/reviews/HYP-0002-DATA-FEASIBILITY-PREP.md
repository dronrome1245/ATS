# HYP-0002 Data Feasibility Preparation

Task: ATS2-M6-004
Work package: WBS-6.2
Status: PREPARATION
Date: 22 September 2026

## Purpose

Prepare the inputs for the formal HYP-0002 Data Feasibility decision without evaluating the HYP-0002 outcome.

The preparation must verify the existing development snapshot, calculate development-only Q10_DEV and Q90_DEV, acquire a disjoint confirmatory BID/ASK block, and report coverage and hashes.

## Development calibration block

Canonical dataset: DATA-DUKASCOPY-EURUSDH1-PROTO01-001@1.0.0
Coverage: 2021-01-01T00:00:00Z through 2025-12-31T23:00:00Z
Expected SHA-256: aeda05d90994259a22e25d882398218aead968941fe0b1c73eb34894841291c0

For each eligible timestamp:

R24(t) = MID_CLOSE(t) / MID_CLOSE(t-24) - 1

MID_CLOSE = (BID_CLOSE + ASK_CLOSE) / 2

The preparation tool calculates linear-interpolation 10th and 90th percentiles: Q10_DEV and Q90_DEV.

## Confirmatory block frozen before outcome observation

Provider/source family: Dukascopy EURUSD 1H BID + ASK historical candles.

Frozen period:
2026-01-01T00:00:00Z <= event_time < 2026-09-01T00:00:00Z

This is eight fully completed calendar months after the development/discovery period.

Official source references:
https://www.dukascopy.com/api/data/get/historical-data-export
https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/history-bars/

## Preparation outputs

Tool: tools/hyp0002_data_feasibility.py

Local-only outputs:
data/derived/HYP-0002-CONFIRM-01-EURUSD-H1.csv
reports/local_ci/HYP0002_DATA_FEASIBILITY.json
reports/local_ci/HYP0002_DATA_FEASIBILITY_REPORT.txt

The report exposes threshold count, Q10_DEV, Q90_DEV, confirmatory coverage, aligned rows, gaps, eligible windows, prepared CSV SHA-256, source-bundle SHA-256 and source-file count.

## Information boundary

The preparation tool is prohibited from calculating HYP-0002 signal returns, baselines, pass/fail results or any other outcome metric.

NO_HYPOTHESIS_OUTCOME_COMPUTED

After review, commit the formal Data Feasibility review and confirmatory Dataset Manifest before any HYP-0002 outcome is revealed.
