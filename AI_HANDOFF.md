# ATS AI Handoff

## Current state

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- Instrument: EUR/USD 1H.
- Current task: `ATS2-M3-004 — Cheap prototype`.
- Prototype: `PROTO-01`.
- Prototype status: `READY_TO_RUN`.
- Result has not been viewed.

## Frozen rules

Canonical prototype record:

`research/reviews/HYP-0001-PROTOTYPE-01.md`

Period: full years 2021–2025.

Rule: existing HYP-0001 24-bar upward breakout, next-hour ASK entry, BID valuation 24 contiguous hours later.

## Frozen data

Manifest:

`data/manifests/DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml`

Dataset:

`DATA-DUKASCOPY-EURUSDH1-PROTO01-001 / 1.0.0`

Prepared CSV SHA-256:

`aeda05d90994259a22e25d882398218aead968941fe0b1c73eb34894841291c0`

Source bundle SHA-256:

`cf378faaae58424112d289315b2ec076f4100775f2613a5d2d685ec46a02aba4`

Data checks:

- 31,296 aligned tradable H1 rows;
- 0 missing expected tradable hours;
- 261 declared market/session gaps;
- 18,485 timestamps with complete 24-before/24-after windows.

## Next action

OWNER:

`git pull --ff-only`

then:

`uv run --frozen python tools/proto01_eurusd.py run`

Share:

- `reports/local_ci/PROTO01_RESULT_REPORT.txt`
- `reports/local_ci/PROTO01_RESULT.json`

Do not rerun with altered parameters or another period after seeing the result.
