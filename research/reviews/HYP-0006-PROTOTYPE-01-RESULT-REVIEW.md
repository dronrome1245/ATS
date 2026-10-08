# HYP-0006 PROTO-01 — Preserved First-Reveal Result Review

Task: `ATS2-RF-031`
Reviewed on: `2026-10-08`
Research step: `18/22`
Provenance: `IDEA-0005 / HYP-0006 / PROTO-01`
Source class: `EXPLORATORY_PROTOTYPE`
Qualified evidence: `DEVELOPMENT_EXPLORATORY_ONLY`
Stage: `POST_REVEAL_GOVERNANCE_REVIEW`
Status: `REVIEWED_POSITIVE_STRUCTURAL_ONLY`

## Exact result identity and no-rerun boundary

RF-030 first reveal completed under exact `main` commit:

`d1135bb2486009ebb358bf4b508c06303ab77f74`

Frozen RF-029 runner Git blob, unchanged on reveal:

`6afb870c035bc5ae76f773784a5fa3db15d680fd`

Canonical saved LOCAL artifacts (never replace or delete):

| Artifact | Frozen SHA-256 |
|---|---|
| `reports/local_ci/CURRENT_TASK_REPORT.txt` | `34b67f3fe3888310c74fff2cc14a5db65aca819219709aaf376abcbe51c7fc53` |
| `reports/local_ci/HYP0006_PROTO01_RESULT.json` | `484575ceb2b6c12df651697d50559e70c7cba8a8f52fc4508d28943e8c5447e9` |
| `reports/local_ci/HYP0006_PROTO01_RESULT_REPORT.txt` | `2f547f6866f13367cb1cdc4f7c31dfec8a7ff12c9fc4e1391d9124b50ba3f213` |

Machine report: `ATS CURRENT TASK CHECK: PASS`; `ATS TASK LAUNCHER: PASS`.
Repository validator, pinned Ruff lint, Ruff format, pytest (246 tests),
environment fingerprint and full ATS Local CI: all PASS. Local frozen
`1085/1085` BI5 objects passed their SHA-256 checks immediately before
the first reveal. No live BLS/Dukascopy request or downloader was used.

The runner was invoked exactly once under the registered frozen first-reveal
path. The saved report supplies the historical outcome; RF-031 **does not**
rerun the runner, touch BID/ASK source data for returns, or reclassify the
revealed development block as confirmatory or independent.

The original HYP-0006 development interval was
`[2003-08-03T21:00:00Z, 2021-09-01T00:00:00Z)`.

## Frozen denominator and first result

- `217` scheduled U.S. CPI candidates.
- `216` eligible events.
- One preregistered timestamp-gap exclusion: `BLS-CPI-20030815`.
- `216` paired before/after absolute-return observations.
- `median_pre_abs_60m_return = 0.0005589654536042321`.
- `median_post_abs_60m_return = 0.0012930417305135888`.
- Frozen single inequality `median(post_abs_60m_return) > median(pre_abs_60m_return)`: `TRUE`.
- Frozen prototype decision: `ADVANCE_TO_ECONOMIC_SCREEN`.
- Mandatory next routing: `CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4`.

This decision is about **median absolute movement**, not a signed
directional trading return. It neither establishes an executable entry nor
authorizes direct R4 admission, economic profitability, Candidate promotion,
Strategy Version or capital allocation.

## Preserved non-decision diagnostics

The saved 19 calendar-year groups contain 16 with post-year median greater
than pre-year median and three exceptions: `2003`, `2008`, `2011`.
The maximum single-year share is `0.05555555555555555` (12/216).
The 2003 group has four events; 2021 has eight.

All `216` eligible CPI timestamps are flagged for a simultaneous official BLS
`Real Earnings` release, so the observed effect cannot be attributed
exclusively to CPI. The event cluster must remain visible without
post-result exclusions.

Saved spread diagnostics:
- Median strictly-pre-release relative quoted spread:
  `0.00009947885660692423`.
- Median first-post-release relative quoted spread:
  `0.00008393020387456029`.

These are quote diagnostics, not executable round-trip cost estimates
or profit figures. They cannot rescue or upgrade the frozen primary decision.

## Research accounting and cross-line boundary

The original `IDEA-0005 / HYP-0006` is retained as a successful **exploratory
structural attempt**, not superseded by editing its prior result/contract.

OWNER authorized preparation of a new **confirmatory structural** continuation
on `2026-10-08` after first-reveal review. Its new material hypothesis attempt
must be registered separately, with a new HYP ID and the same parent
`IDEA-0005` only if lineage review confirms unchanged
mechanism/market/event condition/horizon/test semantics.

The consumed HYP-0006 development block is never independent for its
confirmatory successor. The HYP-0004 consumed/inspected EURUSD coverage
`[2003-08-03T21:00:00Z, 2026-09-01T00:00:00Z)` is not automatically
independent for the successor either. The two still-protected HYP-0005
segments `[2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)` and
`[2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)` are strictly off limits.
A potential new confirmatory block is **NOT CERTIFIED** at this stage.
Future Data Feasibility must audit every other ATS exposure, establish exact
non-overlap, coverage, public-release timestamp semantics, BI5 source
identity and preserved point-in-time availability.

This review does **not** create independent examination evidence, does
not approve data acquisition/reveal, and must retain negative/limiting facts.

## Review decision

`RF030_REVEALED_EXPLORATORY_ADVANCE_TO_NEW_HYPOTHESIS_FORMATION`.

`HYP0006_RESULT_PRESERVED_NO_RERUN`.

RF-031 is governance and Hypothesis formation only. No HYP-0007
confirmatory outcome, dataset or experimental result is calculated here.
