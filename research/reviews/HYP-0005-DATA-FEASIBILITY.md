# HYP-0005 — Confirmatory Data Feasibility Review and Dataset Freeze

Task: `ATS2-RF-024`  
Parent preparation: `ATS2-RF-023` via `ATS2-RF-034`  
Hypothesis: `HYP-0005`; parent Idea: `IDEA-0004`  
Research stage: `2/5 — DATA_FEASIBILITY_FREEZE`  
Review decision: `CONDITIONAL`  
Technical freeze status: `STAGED_PENDING_EXACT_MAIN_PASS`  
Evidence classification: `CONFIRMATORY_DATA_PREPARATION_ONLY`  
Information boundary: `NO_CONFIRMATORY_OUTCOME_COMPUTED`  
Review date: 2026-10-12

## 1. Decision question

Can the preselected disjoint EURUSD H1 BID+ASK source observations support the
**unchanged structural HYP-0005** test without selecting dates, modifying
UTC buckets or inspecting either primary inequality, and can the exact
preparation bytes be deterministically frozen?

**Answer: CONDITIONAL**, with the already-declared H1 bar-open timing proxy,
three missing expected market hours retained as gaps, source-provider
authenticity limitation, and no trading/execution claims.
The RF-023 preparation decision was
`READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE`.
It is a data geometry outcome, **not** a PASS of HYP-0005's two claims.

This document and the manifest/schema are **staged** on `agent/*`.
Formal dataset freeze and technical RF-024 closure require OWNER exact-head
preflight, GPT squash merge and OWNER exact-main `ATS_TASK_CHECK.bat` PASS.
Until exact-main PASS, do not label this dataset frozen or execute the
confirmatory market/primary-outcome runner.

## 2. Preserved research contract and evidence boundaries

- Market/instrument: `FX_SPOT_OTC / EURUSD`.
- Provider family: `Dukascopy EURUSD H1 BID+ASK`; selected existing complete
  `JETTA_JSON` pair for each of five frozen months.
- Source months: `2003-05`, `2003-06`, `2003-07`, `2003-08`, `2026-09`.
  Ten BID/ASK source objects, hash-matched in RF-034 exact main.
- LEFT_UNSEEN: `[2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)`.
- RIGHT_UNSEEN: `[2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)`.
- Previously consumed ATS EURUSD block excluded:
  `[2003-08-03T21:00:00Z, 2026-09-01T00:00:00Z)`.
- Fixed UTC buckets: `CORE_ACTIVE=07..16`, `TRANSITION=17..20`,
  `OFF_HOURS=21..06`. Transition is reporting-only.
- Horizon: `NEXT_1H` with **exact** same-segment `t+1h`;
  no gap, closure, missing hour or segment boundary may be bridged.
- Frozen formulas, parameters, source/cleaning/continuity rules,
  the two primary inequalities and future one-shot reveal boundaries
  remain as in `research/hypotheses/HYP-0005.md`.
- HYP-0005: `NO_CONFIRMATORY_OUTCOME_COMPUTED`.
  HYP-0006 original development outcome is preserved and not rerun.
  HYP-0007 remains unexamined/paused; these source blocks do not
  automatically become independent for any other ATS line.

## 3. Exact RF-023 preparation evidence (already executed once)

Exact preparation/verification commit:
`14531698c87fd3a0d87e1ec54c6713f11b7cbb60`.

Frozen source preparation protocol Git blob:
`c15b2b67700dd46fc592f1208731ce6b42f6905c`.

Frozen offline runner Git blob:
`b8d72d858d5c2691de7dec9a709f6e4d7ccb2808`.

Local source bundle SHA-256:
`65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2`.

Raw source metadata:
`reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP.json`;
SHA-256 of this exact report:
`d2eadd9a64da74ae79e2a0008426147953f24beb8c23f66557a721a7b8a65381`.

Shareable preparation report:
`reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP_REPORT.txt`;
SHA-256:
`fe9f26d15a99294cff17d2f94f3f58dcd41bbb22ffde60bdaf815aedb93d4618`.

Derived local dataset:
`data/derived/HYP-0005-CONF-01-EURUSD-H1.csv`;
SHA-256:
`b1091c4975665b2b0cd4f58627a10aceaab7aeff5076431abb6abc74c0a054c1`.
Dataset ID/version:
`DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0`.

The complete owner-supplied `CURRENT_TASK_REPORT.txt` (RF-034)
is SHA-256
`849a8254c727730b1ccee9a81f521f8aec4c998badc2340ffb66060644f96345`
and attests `ATS CURRENT TASK CHECK: PASS`, `ATS TASK LAUNCHER: PASS`,
257 tests PASS, source/provenance hashes PASS, no HTTP,
`outcome_metrics_computed=false` and
`primary_claim_evaluated=false`.

## 4. Source and geometry, without price outcomes

| Geometry field | LEFT_UNSEEN | RIGHT_UNSEEN | Total |
|---|---:|---:|---:|
| Expected market hours | 1560 | 453 | 2013 |
| Prepared rows | 1557 | 453 | 2010 |
| Missing expected market hours | 3 | 0 | 3 |
| Exact next-hour eligible | 1542 | 449 | 1991 |

Eligible by fixed UTC bucket: `CORE_ACTIVE=838`,
`OFF_HOURS=837`, `TRANSITION=316`.
Total by bucket: `CORE_ACTIVE=839`, `OFF_HOURS=837`,
`TRANSITION=334`.

Ineligible start boundaries partition exactly:
`16` next hour market-closed; `3` next hour missing;
`0` segment-end; `2010 - 1991 = 19`.
No interpolation, time shifting or selective weekday/year exclusions
have been introduced to increase geometry.

All required frozen preparation decision inequalities **about row counts**
pass: both disjoint segments and both primary time buckets have
strictly positive exact-next-hour eligibility. These are
**not** the HYP-0005 movement and spread inequalities.

## 5. Timestamps, quote semantics and data transformation

- Observation: historical EURUSD H1 `bid_open` and `ask_open` for
  same UTC hour; paired timestamps must coincide in the frozen segments.
- Quote integrity (frozen RF-023): finite positive opening quotes,
  `ask_open >= bid_open`; invalid/missing/duplicate timestamps and
  closed-market rows fail the preparation as prescribed.
- `event_time`: UTC hourly bar-open timestamp.
- `availability_time`: `event_time` under the declared
  `H1_OPEN_PROXY_AT_EVENT_TIME` approximation.
- `source_bar_completion_time`: `event_time + 1 hour`.
- `exact_tick_boundary_time_known = false`; the proxy
  **does not certify executable real-time quote availability**.
- Frozen output field order:
  `event_time,availability_time,source_bar_completion_time,sequence,confirmatory_segment,source_symbol,bid_open,ask_open,utc_bucket`.
  No midpoint, spread, return, median, performance or primary
  inequality field is present.
- Deterministic row ordering by `event_time` then `sequence`,
  unique disjoint segment/timestamp identity; gaps stay gaps.

The manifest's top-level coverage start/end form an **outer bound of two
disjoint segments**, not continuous coverage from 2003 through 2026.
All selection and timing boundaries are in this review and the original
frozen preparation contract.

## 6. Bias/leakage and data-feasibility limitations

1. **Source attribution:** September 2026 Jetta original URL and
   BID/ASK side were attested by OWNER; no independent provider-byte
   certification, response ETag or Last-Modified evidence exists.
   Classification remains
   `USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER`.
   The JSON source bundle SHA identifies exact local bytes, not
   independent vendor attestation. No post-outcome vendor swap allowed.
2. **Historical information availability:** H1 bar open is a
   *proxy*, not verified exact boundary tick; a trading or actionable
   execution claim is disallowed under this evidence alone.
3. **Coverage:** three expected market hours absent in LEFT_UNSEEN.
   The exact-next-hour rule excludes affected starts. Data are
   not repaired, forward-filled or selected by favorable outcome.
4. **Sample structure:** only two predeclared disjoint segments;
   calendar years are not chosen after observing market results.
   No assumption of full-regime representativeness or
   automatic cross-ATS independence follows.
5. **FX OTC market:** quote-derived broker/vendor history;
   multi-venue representativeness, point-in-time executable prices
   and exact data-vendor licensing/retention conditions remain
   unknown/not independently verified. Raw and derived bytes
   remain local and Git-ignored.
6. **Costs/economic feasibility:** primary HYP-0005 statement is
   structural and direction-free, not a profitability claim.
   Commission, financing, slippage, market impact, live costs
   and P&L are not assessed at RF-024.
7. **Revision and survivorship:** source Jetta month objects are frozen
   by local SHA; historical vendor corrections/revisions cannot be
   ruled out. Instrument is fixed single EURUSD (not a universe
   screen); no corporate actions adjustment applies to spot FX
   in this measurement.

These limitations constrain interpretation but do not change
mechanism, market, fixed UTC buckets, NEXT_1H, frozen two
primary inequalities or the preselected segments.

## 7. Frozen dataset identity and schema

Staged versioned manifest:
`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001.yaml`.

Staged row schema:
`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF.schema.json`.

The manifest binds the only permitted CSV digest, source bundle,
the exact source/protocol/runner identity and temporal limitations.
The CSV remains local under `data/derived/` and never enters Git.

The source bundle digest was independently reconstructed from the ten
source records in the submitted RF-023 JSON using the frozen
source-object hashing contract; reconstruction matched
`65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2`.
This verifies **metadata consistency**, not remote provider authenticity.

Any future source/snapshot, schema, CSV bytes, cleaning, coverage or
timestamp-semantic change requires a separately versioned dataset and
prior research authorization; it cannot silently replace this
confirmatory version after first reveal.

## 8. RF-024 review decision and routing

Data Feasibility review decision: `CONDITIONAL`.

Conditional interpretation:
`H1_OPEN_PROXY_AT_EVENT_TIME` only; no exact-tick execution claim,
no retrospective period/sample selection, retain three missing-hour
gaps, preserve owner-attested provider limitation, use only the
two frozen source segments and exact-next-hour rule.

**Research route after RF-024 exact-main PASS:**
freeze `DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0`
for *structural confirmatory testing only*, then separately
stage the pre-reveal runner and both decision inequalities.
No HYP-0005 outcome calculation is approved at RF-024.

If immutable source/CSV hashes, row schema, prior consumption
boundary or local CI fails, RF-024 must STOP as a technical/data
blocker, not retroactively PARK or reject HYP-0005 merely to
keep the process moving.

Task closure requires both exact-head OWNER preflight PASS and
exact-main OWNER task-check PASS. Until then:
`STAGED_PENDING_EXACT_MAIN_PASS`.

Information boundary: `NO_CONFIRMATORY_OUTCOME_COMPUTED`.
