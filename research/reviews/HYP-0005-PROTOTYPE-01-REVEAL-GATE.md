# HYP-0005 / PROTO-01 — First Confirmatory Reveal Gate (Preparation Only)

Technical task: `ATS2-RF-036`.
Parent lineage: `IDEA-0004 / HYP-0005 / PROTO-01`.
Research plan: **4.1/5 — preparation of gate 4/5, not its market reveal**.
Date: `2026-10-12`.
Status: `STAGED_PREPARATION_ONLY_REVEAL_NOT_AUTHORIZED`.
Information boundary: `NO_CONFIRMATORY_OUTCOME_COMPUTED`.

## 1. Previous completed gates and evidence

1/5: RF-023 source/geometry preparation PASSED (offline, zero outcome).
2/5: RF-024 frozen `CONDITIONAL` dataset PASSED on
`dd014ef6a1014edcfaa26f7d735478aee0cc94ef`.
3/5: RF-035 runner/decision freeze PASSED exact-main on
`9da36dba228d4fa55c3068a01cabc7f215aa7e02`.
OWNER exact-main report SHA-256:
`d7833785bee462c7b122479de22eae041329f42e24d38a1e7481ae4286aeff1b`.
Reported: clean `main`, validator PASS, Ruff lint/format PASS,
267 pytest PASS, full ATS Local CI PASS,
`ATS CURRENT TASK CHECK: PASS` and `ATS TASK LAUNCHER: PASS`.
No reveal artifacts before or after that run.

This RF-036 task is a **technical source-of-truth and authorization-gate preparation**.
It does not complete the major research step 4/5. It does not create a new
Idea, Hypothesis, material research attempt, Candidate, Strategy Version or Experiment.

## 2. Unchanged, already frozen inputs

The canonical pre-outcome contract is
`research/reviews/HYP-0005-PROTOTYPE-01.md`.
The identical and immutable first-reveal implementation is
`tools/hyp0005_proto01.py`, Git blob
`814193997768605fe60607d66dfd755a9323f339`.
Inherited HYP-0004 arithmetic code Git blob:
`cbc9a46bf5e5296615f51c0ea564153968bc2a55`.
Original RF-023 frozen preparation tool Git blob:
`b8d72d858d5c2691de7dec9a709f6e4d7ccb2808`.
Original HYP-0005 hypothesis card Git blob:
`ebbbc89187c911485c1568dc11f5f2f9e703718a`.
Frozen RF-024 manifest Git blob:
`03dccee9c7f21fff77ade9347b9730b79d6c62c7`.

Dataset:
`DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0`
(Dukascopy H1 EURUSD BID/ASK, 10 local source objects).
Frozen source-bundle SHA-256:
`65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2`.
Frozen prepared CSV:
`data/derived/HYP-0005-CONF-01-EURUSD-H1.csv`.
CSV SHA-256:
`b1091c4975665b2b0cd4f58627a10aceaab7aeff5076431abb6abc74c0a054c1`.
Frozen RF-023 result JSON SHA-256:
`d2eadd9a64da74ae79e2a0008426147953f24beb8c23f66557a721a7b8a65381`.

2010 rows / 1991 eligible exact-next-hour starts:
CORE_ACTIVE 838; OFF_HOURS 837; TRANSITION 316;
LEFT_UNSEEN 1542; RIGHT_UNSEEN 449.
LEFT interval `[2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)`;
RIGHT interval `[2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)`.
Previously consumed interval is prohibited.
Three expected LEFT market hours are genuinely missing (no fills).
Fixed UTC buckets, same-segment exact `t+1h`, source and cleaning
rules, mathematical formulas and primary comparisons cannot change.
Do not shift buckets for daylight-saving time or select favorable years.

Source limitations are not cured by a positive result:
`CONDITIONAL / H1_OPEN_PROXY_AT_EVENT_TIME`,
`exact_tick_boundary_time_known=false`,
`USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER`.
No tick-level, executable, trading P&L or independent-examination claim.

## 3. The two previously frozen primary rules

Compute midpoint at the current and next exact hourly boundary,
relative quoted spread at the current boundary, and absolute next-hour return
using the untouched inherited HYP-0004 implementation.

1. `median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)`
2. `median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)`

Both must be TRUE for `CONFIRMATORY_STRUCTURAL_PASS`
and `BOTH_PRIMARY_INEQUALITIES_MET`.
If either is FALSE: `CONFIRMATORY_STRUCTURAL_FAIL`,
`ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED` and retain all negative evidence.
`TRANSITION`, LEFT/RIGHT and calendar-year slices remain
diagnostic only and may not rescue a failed primary comparison.
Positive routing:
`REVIEW_CONFIRMATORY_STRUCTURAL_EVIDENCE_NO_DIRECT_R4`.
Negative routing:
`RETAIN_NEGATIVE_CONFIRMATORY_EVIDENCE_NO_RETUNING`.
No minimum effect size, significance cutoff, costs/trades or
economic/profitability promotion is introduced here.

## 4. Preparation-only quality gate (RF-036)

1. GPT stages this gate record, syncs canonical state and
   strengthens the metadata-only exact-main task checker.
2. OWNER runs `.\ATS_AGENT_PREFLIGHT.bat` on the exact
   `agent/rf036-hyp0005-first-reveal-gate-prep` HEAD.
   Preflight runs synthetic tests, validator, Ruff and pytest, **not reveal**.
3. On verified exact-head PASS, GPT squash-merges to `main`.
4. OWNER runs `.\ATS_TASK_CHECK.bat` on exact-clean
   merged `main`. It checks source/runner identity by hashes and
   historical preparation geometry only; it MUST reject any existing
   HYP-0005 first-reveal result artifacts. It MUST NOT invoke
   `run_first_reveal_once`.
5. Only exact-main `CURRENT TASK CHECK PASS` and
   `TASK LAUNCHER PASS` close **RF-036 technical preparation**.
   They do **not** satisfy the research gate 4/5.

RF-036 does not add an active command-line reveal path.
The frozen runner's direct CLI continues to exit 2.
Authorization for merely preparing this gate does not authorize
reading protected quote values to compute hypothesis outcomes.

## 5. Future separately authorized first reveal (not RF-036)

Before any execution, OWNER must explicitly authorize
**one** HYP-0005 confirmatory first reveal for the fixed dataset
and immutable runner. The future execution gate must be separately
implemented/verified on `agent/*`, pass exact-head preflight,
squash-merge, then run only on exact-clean `main`.

The future execution gate, still NOT authorized, must:

1. Check explicit OWNER one-shot authorization, exact commit/branch,
   clean worktree, `origin/main` identity and RF-024/RF-035 ancestry.
2. Check exact runner Git blob in HEAD and worktree, all frozen
   manifest/source/preparation/CSV hashes and absence of all result
   and consumed-sentinel artifacts **before any price-value parsing**.
3. Record a durable one-shot consumed sentinel before the first
   outcome computation; no silent replay after a partial failure.
4. Invoke only unchanged `run_first_reveal_once(authorized=True)`,
   reconstruct exact geometry before computing metrics, then write
   both canonical artifacts with original positive or negative result:
   - `reports/local_ci/HYP0005_PROTO01_RESULT.json`;
   - `reports/local_ci/HYP0005_PROTO01_RESULT_REPORT.txt`.
5. Preserve complete results, SHA-256, exact main commit,
   error classification and an immutable review. Already existing
   complete matching results may be verified **hash-only**;
   existing partial/inconsistent artifacts are blockers,
   never a reason to delete, modify or rerun.
6. Distinguish `TECHNICAL_BLOCKER` (source, hash, geometry,
   environment) from genuine `CONFIRMATORY_STRUCTURAL_FAIL`.
   Neither is upgraded to trading evidence.

Stage 5/5 is subsequent result interpretation and routing;
no post-reveal selection, reparameterization, independent evidence
claim, R4 bypass or hidden discarded failures is permitted.

## 6. Current mandatory stop

`HYP-0005: NO_CONFIRMATORY_OUTCOME_COMPUTED`.
`FIRST_REVEAL: NOT_AUTHORIZED / NOT_EXECUTED`.
`RF-036: PREPARATION_ONLY`.
`HYP-0006: DEVELOPMENT_REVEALED_EXPLORATORY_ONLY`.
`HYP-0007: NO_CONFIRMATORY_OUTCOME_COMPUTED`.

Next action for OWNER **after** the RF-036 agent PR exists:
run exact-head `.\ATS_AGENT_PREFLIGHT.bat` and provide
`reports/local_ci/AGENT_PREFLIGHT_REPORT.txt`.
Do not run first reveal, RF-023 preparation or any network source request.
