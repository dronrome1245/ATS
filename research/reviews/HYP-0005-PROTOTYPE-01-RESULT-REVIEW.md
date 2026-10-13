# HYP-0005 / PROTO-01 — Preserved Confirmatory Structural First-Reveal Review

Technical task: ATS2-RF-038
Parent Idea: IDEA-0004
Hypothesis: HYP-0005
Original Prototype ID: PROTO-01
Research plan: 5/5 — post-reveal interpretation and route decision
Review date: 2026-10-13
Stage at PR staging: STAGED_PENDING_EXACT_MAIN_PASS
Research result: CONFIRMATORY_STRUCTURAL_PASS (already revealed once)
Original result label: CONFIRMATORY_STRUCTURAL_NOT_INDEPENDENT_EXAM
Review source_class: EXPLORATORY_PROTOTYPE
Review qualified_evidence_class: EXPLORATORY_PROTOTYPE
Formal Experiment ID: NONE
Independent Examination: NOT PERFORMED

## 1. Trigger and decision authority

The first, and only authorized, HYP-0005 confirmatory structural reveal
was performed by OWNER under task ATS2-RF-037 on exact-clean main.
Review trigger: successful saved result/receipt and ATS current-task
completion report uploaded by OWNER on 2026-10-13.

Preparer/reviewer: ATS research GPT, based only on the five preserved
OWNER-supplied result/gate artifacts and prior frozen protocol.
Review authority: Research Factory for the narrow prototype
interpretation and next research question, NOT capital/live authority.
OWNER remains the sole authority for live admission and allocation.

The existing five-step HYP-0005 plan does not change:
1/5 source/data preparation PASS; 2/5 CONDITIONAL dataset freeze PASS;
3/5 original code/rule freeze PASS; 4/5 reveal EXECUTED_ONCE and PASS;
5/5 result review (this RF-038 task), pending exact-main task closure.
This is NOT a new Hypothesis or additional material research attempt.

## 2. Evidence identification, exact-main and no-rerun boundary

Original one-shot execution commit:
4388ac8aac732f7bd745a4466f8a9b524d543167

Immutable original HYP-0005 runner Git blob:
814193997768605fe60607d66dfd755a9323f339

Authorization marker:
OWNER_AUTHORIZED_HYP0005_FIRST_REVEAL_ONCE_2026_10_12

Canonical preserved local files (do not edit, replace or rerun):

| Artifact | SHA-256 |
|---|---|
| reports/local_ci/CURRENT_TASK_REPORT.txt | f5fff726d8243d0434364d6bfcff60d4f1614bbe459de4d7494c40b229a46369 |
| reports/local_ci/HYP0005_PROTO01_RESULT.json | cba7f07eebef52b649d2a2b6a7edb1dc0b808c04080fe1ae0d71e6eab25f19dc |
| reports/local_ci/HYP0005_PROTO01_RESULT_REPORT.txt | 57daab4a0ae2834d338f77785d52ecd3383c026d5df1196648f0b19a86813af9 |
| reports/local_ci/HYP0005_PROTO01_FIRST_REVEAL_CONSUMED.json | 726ffc650a43982b49da998cd2d5ac6a5f33f816bbb0a39434998335296cf359 |
| reports/local_ci/HYP0005_PROTO01_FIRST_REVEAL_RECEIPT.json | 3a0f29606781c6fadabc3a141439752a60aa8e744760405a584ec005400ab6c1 |

The original receipt records the result JSON and TXT SHA-256, exact
execution commit, frozen dataset CSV SHA-256 and runner Git blob.
Those checksums match the supplied original file bytes.
The consumed marker was written at 2026-10-12T18:24:13.934095Z,
before result completion at 2026-10-12T18:24:15.565495Z and
receipt completion at 2026-10-12T18:24:15.612340Z.
Consumed state: CONSUMED_BEFORE_OUTCOME.
Receipt state: FIRST_REVEAL_COMPLETED_ONCE.

The OWNER report records First reveal: EXECUTED_ONCE,
ATS CURRENT TASK CHECK: PASS and ATS TASK LAUNCHER: PASS on
exact-clean main. Full ATS Local CI PASS, repository validator,
pinned Ruff lint/format, 278 pytest and environment fingerprint
all PASS. Frozen source/data/code identities and 10 local H1
BID/ASK objects passed hash-only checks. The review performed
26/26 additional consistency checks on the uploaded preserved
artifacts; NO protected raw quote data were loaded or recomputed.
RF-037 technical execution therefore qualifies for CLOSED / EXACT-MAIN PASS.

This review is observational and archival. NEVER call the frozen
first-reveal function again. There is no remaining one-shot authorization.

## 3. Preregistered sample and immutable primary decisions

Dataset:
DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0
Market and instrument: FX_SPOT_OTC / EURUSD.
Source: Dukascopy H1 BID/ASK opening quotes, local frozen snapshot.
Data Feasibility: CONDITIONAL / H1_OPEN_PROXY_AT_EVENT_TIME.
Provider provenance: USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER.

Source-bundle SHA-256:
65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2
Prepared CSV SHA-256:
b1091c4975665b2b0cd4f58627a10aceaab7aeff5076431abb6abc74c0a054c1

LEFT_UNSEEN:
[2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)
RIGHT_UNSEEN:
[2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)
The intervening development interval is already consumed.
After RF-037 first reveal, BOTH LEFT and RIGHT are revealed and
CONSUMED for future ATS independence assessments.

Original 2010 prepared hourly rows produced 1991 eligible exact
next-hour observations: CORE_ACTIVE 838, OFF_HOURS 837, TRANSITION
316, LEFT 1542 and RIGHT 449. All three missing expected LEFT
market hours and 16 closed-market next-hour boundaries remained
excluded under predeclared policy; no filling or selected subperiods.

Original inequality 1:
median(abs_next_1h_return | CORE_ACTIVE) >
median(abs_next_1h_return | OFF_HOURS)

Saved values:
CORE_ACTIVE 0.0007490105401033453
OFF_HOURS 0.00038491476276447667
Original movement_inequality_pass: TRUE
Observed ratio (descriptive): 1.9459127385084296.

Original inequality 2:
median(relative_spread | CORE_ACTIVE) <=
median(relative_spread | OFF_HOURS)

Saved values:
CORE_ACTIVE 0.00008657184257709088
OFF_HOURS 0.0001246294499390464
Original spread_inequality_pass: TRUE
Observed relative spread reduction (descriptive): approximately 30.5%.

The original Boolean:
both_primary_inequalities_pass = TRUE.
Frozen first-reveal decision: CONFIRMATORY_STRUCTURAL_PASS.
Decision reason: BOTH_PRIMARY_INEQUALITIES_MET.
Original runner next action:
REVIEW_CONFIRMATORY_STRUCTURAL_EVIDENCE_NO_DIRECT_R4.

This positive result is limited to structural, nondirectional
quote statistics. It is NOT positive trade expectancy or profit.
No new p-value, effect cutoff, alternative bucket or selected period
was applied to determine PASS.

## 4. Preserved diagnostics — NOT independent decision gates

Two calendar-year groupings are present in the saved result.
The positive direction appears in both years, descriptively:

| Calendar year | CORE_ACTIVE median absolute NEXT_1H | OFF_HOURS median absolute NEXT_1H | CORE_ACTIVE median relative spread | OFF_HOURS median relative spread |
|---|---:|---:|---:|---:|
| 2003 | 0.0008841477278916932 | 0.0004421161204717361 | 0.00008744392658875595 | 0.0001363146670094568 |
| 2026 | 0.00038346475538275637 | 0.0002364543879485037 | 0.00001758411803015241 | 0.00003438227937324543 |

For CORE_ACTIVE, 648/838 = 77.3% of eligible observations
are from 2003, and 190/838 = 22.7% from 2026.
For OFF_HOURS, 650/837 = 77.7% are from 2003,
and 187/837 = 22.3% from 2026.
The near-23-year gap and concentration materially limit
regime representativeness, effective-sample inference and
the strength of out-of-time generalization claims.

These year-level figures are predeclared reporting diagnostics.
They CANNOT rescue, modify, strengthen or redefine the
original full-sample primary decision.
TRANSITION observations were also reporting-only.

## 5. Evidence classification and limitations

Review input completeness: COMPLETE_WITH_LIMITATIONS.
Frozen lineage: LINEAGE_OK.
Integrity: SHA256_MATCHED / EXACT_MAIN_CHECK_PASS.
Evidence sufficiency: SUFFICIENT_WITH_LIMITATIONS for the
narrow, preregistered structural comparison only.
Evidence class: CLASS_INSUFFICIENT for profitability,
R4 admission, formal validation or independent examination.

This is a pre-registered/frozen first reveal inside a Cheap
Prototype lineage (PROTO-01); there is no separately registered
EXP-YYYYMMDD-nnn formal Experiment manifest and no frozen
directional Strategy Version. Accordingly the canonical ATS
taxonomy source_class and qualified_evidence_class remain
EXPLORATORY_PROTOTYPE, with an additional original structural
result label CONFIRMATORY_STRUCTURAL_NOT_INDEPENDENT_EXAM.
A favorable result does not automatically upgrade evidence class.

Material limitations to retain:

- H1_OPEN_PROXY_AT_EVENT_TIME: the H1 opening quote is a proxy
  for an available/executable event-time price; exact tick-level
  boundary time is unknown.
- September 2026 source provenance remains OWNER/USER ATTESTED,
  not independently verified against official provider metadata.
- Only two short, disjoint time blocks; 2003 dominates hourly counts;
  no broad FX-regime or provider-revision representativeness proof.
- Hourly observations need not be independent economic
  opportunities; no effective sample size, confidence interval
  or predeclared significance test was established here.
- No directional trading rule, entry, exit, hold management,
  costs, slippage, financing, risk limits, drawdown or P&L.
- HYP-0004 was prior exploratory development; HYP-0005 shows
  a frozen positive structural contrast on two separate blocks.
  This does not substitute for an Independent Examination.
- All HYP-0005 reveal blocks are now consumed across ATS lines.
  The HYP-0007 independent-source feasibility question remains
  OPEN; none of these revealed periods is automatically independent
  for HYP-0007 or any future tuning.
- The JSON result's limitations array embeds immutable historical
  RF-024 manifest text, including STAGED_PENDING_EXACT_MAIN_PASS
  and "No HYP-0005 hypothesis outcome has been computed or revealed".
  These statements describe historical pre-reveal manifest metadata,
  not CURRENT research status. The result JSON must NOT be edited.
  Current first-reveal status is established by the preserved receipt,
  exact-main task report and this separate review.

No material negative market result was suppressed: both primary
inequalities are positive under their original decision contract.
Recorded limitations and failed technical preflights remain
historical evidence, not overwritten by the positive finding.

## 6. Review decision and next boundary

Stage-appropriate original decision:
CONFIRMATORY_STRUCTURAL_PASS

Review routing:
REVIEW_CONFIRMATORY_STRUCTURAL_EVIDENCE_NO_DIRECT_R4

Interpretation: the fixed session-linked structural quote
contrast was observed in the authorized first confirmatory
dataset, with the above limitations preserved. This is
not an executable or validated profitable trading system.

HYP-0005 research plan step 5/5 is satisfied on preserved
source evidence as the post-reveal interpretation. RF-038 task
CANNOT be called CLOSED until its separate exact-main task gate
passes. Do not reopen step 4/5 or rerun the first reveal.
No direct R4 Economic Pre-Screen or Candidate promotion
may be treated as passed.

The next research question, outside the completed HYP-0005
structural test, is whether the time-of-day effect can be
converted into a falsifiable, economically meaningful
DIRECTIONAL entry, exit and cost-aware trading hypothesis.
This is NOT answered by the current positive structural
comparison. BEFORE assigning a new Idea/HYP ID or seeing more
outcomes, perform a lineage/Idea Intake decision:
- if mechanism, market, condition, horizon and proposed test
  materially match an existing Idea, make a new, separately
  registered Hypothesis under that Idea;
- if materially distinct, require a new Idea Intake first.
No proposed trading rule or parameter has yet been selected
or granted a protected test block.

No new market outcome is computed or revealed in RF-038.
No existing source data are retuned and no independent
dataset is certified. OWNER has no capital/live action.
