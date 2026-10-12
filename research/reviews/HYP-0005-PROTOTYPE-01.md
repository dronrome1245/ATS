# HYP-0005 / PROTO-01 — Pre-Reveal Confirmatory Structural Runner Freeze

Technical task: `ATS2-RF-035`. Parent Idea: `IDEA-0004`.
Hypothesis: `HYP-0005` (formed and frozen under `ATS2-RF-022`).
Research plan: **3/5 — exact pre-reveal runner/protocol freeze**.
Stage: `STAGED_PENDING_EXACT_MAIN_PASS`.
Evidence status: `NO_CONFIRMATORY_OUTCOME_COMPUTED`.
Date: 2026-10-12.

## 1. Frozen falsifiable claim and mechanism

Inherit original **structural, nondirectional** HYP-0005 claim:
for all eligible start boundaries `t` in the two unchanged, independent-from-ATS-development HYP-0005 blocks:

- `mid_t = (bid_open_t + ask_open_t) / 2`
- `relative_spread_t = (ask_open_t - bid_open_t) / mid_t`
- `abs_next_1h_return_t = abs(mid_(t+1h) / mid_t - 1)`

Both predeclared conditions must hold:

1. `median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)`
2. `median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)`.

`TRANSITION` is reporting-only. No directional sign, profit target,
minimum effect threshold, p-value threshold, alternate source/period,
subset selection or additional hypothesis may be introduced after
result inspection.

Exact definitions are **inherited** from frozen development code
`tools/hyp0004_proto01.py` (Git blob
`cbc9a46bf5e5296615f51c0ea564153968bc2a55`).
The confirmatory runner imports that same frozen implementation
of `abs_next_1h_return`, `relative_spread`, `bucket_metrics`,
`primary_summary`, `calendar_year_diagnostics`; its frozen
source/geometry preparation code is
`tools/hyp0005_data_feasibility.py` Git blob
`b8d72d858d5c2691de7dec9a709f6e4d7ccb2808`.
Any Git blob/worktree drift causes a technical STOP.

## 2. Frozen dataset and timestamp contract

The exact CONDITIONAL confirmatory dataset was frozen
at RF-024 exact-main OWNER PASS on
`dd014ef6a1014edcfaa26f7d735478aee0cc94ef`.
No HYP-0005 result was computed.

Dataset: `DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0`.
Manifest:
`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001.yaml`.
Schema:
`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF.schema.json`.
The manifest/schema are immutable and will **not** be edited
post-freeze, including their historical staging status text.

Raw source: Dukascopy EURUSD H1 BID+ASK Jetta JSON,
ten hash-identified local source objects for
`2003-05`, `2003-06`, `2003-07`, `2003-08`, `2026-09`.
The September official provider attribution remains
`USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER`.

Source-bundle SHA-256:
`65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2`.

Local prepared CSV:
`data/derived/HYP-0005-CONF-01-EURUSD-H1.csv`,
SHA-256:
`b1091c4975665b2b0cd4f58627a10aceaab7aeff5076431abb6abc74c0a054c1`.
Exactly `2010` rows. RF-023 preserved JSON SHA-256:
`d2eadd9a64da74ae79e2a0008426147953f24beb8c23f66557a721a7b8a65381`.
Original RF-023 frozen code SHA:
`b8d72d858d5c2691de7dec9a709f6e4d7ccb2808`.

LEFT_UNSEEN:
`[2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)`;
RIGHT_UNSEEN:
`[2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)`;
already consumed and **never selected**:
`[2003-08-03T21:00:00Z, 2026-09-01T00:00:00Z)`.

UTC CORE_ACTIVE `07:00..16:00`, TRANSITION `17:00..20:00`,
OFF_HOURS `21:00..06:00`. Never apply DST bucket shifts.
Only events in frozen segments, with exactly `t+1h` in
the **same segment** and an expected FX-market hour,
are eligible. No weekend/missing-hour interpolation, stale
replacement, cross-segment bridging, or post-outcome exclusion.

Frozen geometry checked **before outcome computations**:

| Geometry | Value |
|---|---:|
| total rows | 2010 |
| exact-next-hour eligible | 1991 |
| CORE_ACTIVE eligible | 838 |
| OFF_HOURS eligible | 837 |
| TRANSITION eligible | 316 |
| LEFT_UNSEEN eligible | 1542 |
| RIGHT_UNSEEN eligible | 449 |
| expected LEFT / RIGHT FX market hours | 1560 / 453 |
| retained LEFT / RIGHT rows | 1557 / 453 |
| missing LEFT / RIGHT expected market hours | 3 / 0 |
| ineligible due to closed next-hour | 16 |
| ineligible due to missing next-hour | 3 |
| ineligible due to segment end | 0 |

The source-bar opens are represented with
`H1_OPEN_PROXY_AT_EVENT_TIME`:
`availability_time = event_time` and
`source_bar_completion_time = event_time + 1 hour`.
`exact_tick_boundary_time_known=false`.
This is neither executable tick evidence nor live price evidence.

## 3. Exact runner and decision freeze

Confirmatory runner:
`tools/hyp0005_proto01.py`.
Expected frozen runner Git blob:
`814193997768605fe60607d66dfd755a9323f339`.
This blob must equal both `HEAD:tools/hyp0005_proto01.py`
and `git hash-object tools/hyp0005_proto01.py` on
OWNER's exact-head and exact-main checks.

On reveal, perform in precisely this order:
1. Authorization + exact-clean-main and RF-024 ancestor check.
2. Require first-reveal result paths absent; no overwrite or rerun.
3. Verify frozen manifest, prepared CSV, RF-023 JSON and code blobs.
4. Parse all 2010 rows only then; validate source quote,
   UTC event/availability/completion times, exact segment,
   row sequence, buckets and gap policy.
5. Reconstruct original RF-023 geometry mechanically and
   require exact `1991` eligible starts and every predeclared
   segment/bucket/exclusion count, **before computing metrics**.
6. For each eligible `t`, evaluate the fixed four arithmetic
   equations from Section 1, on BID/ASK open at exactly
   `t` and `t+1h`. Use no future values for bucket
   assignment or determining eligibility.
7. Produce for each bucket: eligible count,
   mean and median absolute next-1h return,
   median relative spread; retain TRANSITION reporting.
8. Produce predeclared calendar-year per-bucket observation
   counts, shares, medians and maximum single-year share,
   **diagnostic only**, not a sample-selection rule.
9. Compare two fixed primary inequalities and preserve
   the three Boolean fields:
   `movement_inequality_pass`, `spread_inequality_pass`,
   `both_primary_inequalities_pass`.
10. Serialize original result JSON and TXT **once**;
    retain every negative as well as positive outcome.
    This consumes HYP-0005 confirmatory evidence for this
    one material research attempt.

Frozen routing (regardless of statistical significance):

- Both conditions TRUE:
  `CONFIRMATORY_STRUCTURAL_PASS`;
  `BOTH_PRIMARY_INEQUALITIES_MET`;
  `REVIEW_CONFIRMATORY_STRUCTURAL_EVIDENCE_NO_DIRECT_R4`.
- Either condition FALSE:
  `CONFIRMATORY_STRUCTURAL_FAIL`;
  `ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED`;
  `RETAIN_NEGATIVE_CONFIRMATORY_EVIDENCE_NO_RETUNING`.
- Inconsistent/missing file, CSV digest drift,
  missing source, malformed row, geometry mismatch, code blob
  drift, missing authorization or runtime error:
  `TECHNICAL_BLOCKER` and no valid Hypothesis result.
  Do **not** relabel a source failure as a negative
  confirmatory market result.

No new return-sign prediction, economic threshold,
trial/performance selection or favorable-year rescue.
A structural PASS does NOT create a Candidate or authorize R4,
capital, live orders, or an Independent Examination.

## 4. Outcome boundary and gates

**Stage 3/5 (current):** create/freeze only this protocol,
runner Git blob and synthetic tests. OWNER's
`.\\ATS_AGENT_PREFLIGHT.bat` verifies exact HEAD and
full Local CI; GPT squash-merges, then OWNER exact-main
`.\\ATS_TASK_CHECK.bat` must PASS. **Do not execute**
`run_first_reveal_once` or open the prepared CSV for
market outcomes in either Stage-3 gate.

The runner's direct CLI exits with code 2.
Its one-shot reveal function requires
`authorized=True`, an exact clean `main` and
ancestry from the frozen RF-024 commit.
A separate Stage-4 approval, frozen exact-head
first-reveal execution checker/launcher and identity gate
are required before calling that function.
The authorization is not granted by freezing this file.

Planned first-reveal local outputs (all absent at stage 3):
- `reports/local_ci/HYP0005_PROTO01_RESULT.json`.
- `reports/local_ci/HYP0005_PROTO01_RESULT_REPORT.txt`.

No prototype result file is created by RF-035.
Do not touch HYP-0006, HYP-0007, source download,
source geometry preparation or any protected EURUSD block.

## 5. Research classification

Hypothesis class: confirmatory structural replication
with predeclared source periods not used for HYP-0004
development. It is **not** a strategy P&L test,
full independent-examination gate, proof of a
causal liquidity mechanism or validation of live execution.

Dataset Data Feasibility remains `CONDITIONAL`.
The entire RF-023 prepared dataset and original
2010-row CSV are frozen as bytes at RF-024 exact-main
`dd014ef6a1014edcfaa26f7d735478aee0cc94ef`.
No post-outcome rerun, period/date/parameter adjustment,
relabeling, source selection or reuse of these blocks as
independent ATS evidence for another Hypothesis is allowed.

Next research step **4/5** only after RF-035
technical **exact-main PASS**, with separately granted
OWNER first-reveal authorization. HYP-0005
`NO_CONFIRMATORY_OUTCOME_COMPUTED` until that stage.
