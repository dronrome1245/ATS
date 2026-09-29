# HYP-0006 BLS Schedule Snapshot Intake

Task: `ATS2-RF-027`  
Hypothesis: `HYP-0006`  
Purpose: one-time capture of official BLS annual release schedules so later RF-027 runs do not depend on live BLS HTTP access.

## Why this exists

Two exact-main RF-027 attempts reached the official BLS source and received HTTP 403 before event acquisition.

This is a technical source-access problem, not a HYP-0006 result.

The repair is to snapshot the official annual BLS schedule pages once, hash them, derive the CPI event calendar locally, and never require live BLS access during normal RF-027 runtime.

## Required inputs

Canonical manifest:

`data/reference/HYP-0006-BLS-SCHEDULE-SNAPSHOT-MANIFEST.csv`

It lists 19 official pages for calendar years 2003 through 2021.

Each page must be saved unedited to exactly:

`data/raw/bls/hyp0006/schedules/YYYY.html`

Example:

`data/raw/bls/hyp0006/schedules/2003.html`

comes from:

`https://www.bls.gov/schedule/2003/home.htm`

Raw snapshot files are intentionally ignored by Git.

## OWNER procedure

Do this only when GPT explicitly says the RF-027 code has passed exact-head preflight and the snapshot bundle is now required.

For each year 2003 through 2021:

1. open the URL from the manifest in a normal browser;
2. save the page as HTML only;
3. rename the saved file to exactly `YYYY.html` if the browser used another name;
4. place it under `data/raw/bls/hyp0006/schedules/`;
5. do not edit, clean, reformat or copy/paste the page contents.

After all 19 files are present, run:

`.\ATS_TASK_CHECK.bat`

The runner will verify that every required snapshot exists, compute SHA-256 for every source file, parse only official CPI schedule rows, create a local CPI calendar, hash that calendar, and then proceed to Dukascopy tick geometry.

## Generated local calendar

RF-027 will generate:

`data/derived/HYP-0006-BLS-CPI-CALENDAR-2003-2021.csv`

This calendar contains only event identity/time/provenance fields. It contains no EUR/USD prices, returns or P&L.

The calendar is a preparation artifact. RF-028 will later decide whether to freeze its exact SHA-256 and admissibility rules before any HYP-0006 reveal.

## Failure semantics

Missing snapshot file:

`OWNER_INPUT_REQUIRED_BLS_SCHEDULE_SNAPSHOTS`

This is not a HYP-0006 negative result.

Malformed/unparseable official snapshot:

technical/data-source blocker.

Live BLS network access during RF-027 runtime:

prohibited.

## Information boundary

`NO_HYPOTHESIS_OUTCOME_COMPUTED`
