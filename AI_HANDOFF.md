# ATS AI Handoff

## Current state

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- Instrument: EUR/USD 1H.
- Idea: `IDEA-0001`.
- Hypothesis: `HYP-0001`.
- Data Feasibility: `CONDITIONAL`.
- Current task: `ATS2-M3-004 — Cheap prototype`.
- Prototype: `PROTO-01`.
- Prototype status: `PRE_RUN_DATA_REQUIRED`.

## PROTO-01 is fixed before result

Canonical record:

`research/reviews/HYP-0001-PROTOTYPE-01.md`

Fixed period: full years 2021–2025.

Fixed decision rule is already written. Result has not been viewed.

## Data preparation

Tool:

`tools/proto01_eurusd.py`

Run only:

`uv run --frozen python tools/proto01_eurusd.py prepare`

Share:

`reports/local_ci/PROTO01_DATA_REPORT.txt`

Do not run `tools/proto01_eurusd.py run` until the canonical Dataset Manifest is committed:

`data/manifests/DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml`

Raw/downloaded data stay outside Git.

## Safety

No Candidate, Strategy ID, formal Experiment, demo/live permission or capital allocation exists.
