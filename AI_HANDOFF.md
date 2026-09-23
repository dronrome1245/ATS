# ATS AI Handoff

## Current program state

- M0–M3: `COMPLETED / PASS`.
- M4 reusable baseline WBS-4.1…4.8: `COMPLETED`; M4.9/M4.10 wait for an eligible S05 PASS Candidate.
- M6: `COMPLETED / PASS`.
- Strategy #1: отклонена на R3.
- Strategy #2: отклонена на R3.
- Candidate count: `0`.
- Current lane: `RESEARCH_FACTORY_CONTINUOUS`.

## Verified RF-004 closure

OWNER launcher PASS was confirmed on exact commit:

`f402469ff3aa52bcd3ae98189f7ad4b92eac7ffc`

Evidence included pinned Ruff lint/format, pytest collection `141 tests`, full pytest `141 passed`, full Local CI, current task PASS and launcher PASS.

Canonical last completed artifact:

`research/hypotheses/HYP-0003.md`

## RF-005 HYP-0003 Data Feasibility

Current task:

`ATS2-RF-005 — HYP-0003 Data Feasibility`

Canonical next artifact:

`research/reviews/HYP-0003-DATA-FEASIBILITY.md`

Decision:

`CONDITIONAL`

The review fixes before any development result:

- G10-ex-USD candidate currencies: `AUD, CAD, CHF, EUR, GBP, JPY, NOK, NZD, SEK`;
- nine mechanical USD-pair candidates;
- minimum feasible cross-section: `6`;
- direct/inverse BID/ASK normalization;
- extreme-basket size: `max(1, ceil(N/6))`;
- deterministic tie break;
- H1 UTC month-boundary timing;
- protected tail: `2021-09-01T00:00:00Z` to `2026-09-01T00:00:00Z`;
- information boundary: `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

Dukascopy is the primary source candidate because its official historical-data service documents multi-instrument historical data and BID/ASK export. Exact availability/common coverage still requires local machine verification.

No HYP-0003 momentum surface has been computed.

Run `ATS_TASK_CHECK.bat` and return `reports/local_ci/CURRENT_TASK_REPORT.txt`.

After exact-head PASS:

`ATS2-RF-006 — HYP-0003 Data Feasibility preparation`.
