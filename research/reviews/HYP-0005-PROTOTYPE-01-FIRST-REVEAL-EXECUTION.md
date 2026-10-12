# HYP-0005 / PROTO-01 — Authorized First Confirmatory Reveal Execution Gate

Technical task: ATS2-RF-037
Existing lineage: IDEA-0004 / HYP-0005 / PROTO-01
Research step: 4/5 — ONE FIRST CONFIRMATORY REVEAL
Technical workflow: RF-036 preparation exact-main PASS; RF-037 execute once.
Date: 2026-10-12
Status at staging: OWNER_AUTHORIZED_ONCE_EXECUTION_NOT_YET_PERFORMED
Information boundary: NO_CONFIRMATORY_OUTCOME_COMPUTED

## 1. One explicit OWNER authorization

OWNER explicitly authorized ONE first confirmatory HYP-0005 reveal in the
project conversation on 2026-10-12, in direct response to the separate
authorization request after exact-main RF-036 completion.

Authorization: OWNER_AUTHORIZED_HYP0005_FIRST_REVEAL_ONCE_2026_10_12

The scope is strictly the EXISTING, frozen HYP-0005 structural replication.
No second test, source acquisition, source substitution, favorable-period
selection, formula adjustment, HYP-0006/HYP-0007 computation, economic claim
or live use is authorized. Agent preflight never computes HYP-0005 outcomes.

RF-036 completed on exact main
1facc2604e701cc05b34118e8c3295070bfd9eaa.
Exact-main OWNER completion report SHA-256:
48924993149cdd11ba489ab0dc2c22e14a551669a7bdd28d7b3f987442e97ee2.
The report passed validator, Ruff, 269 pytest, full Local CI,
CURRENT TASK CHECK and TASK LAUNCHER. No HYP-0005 reveal occurred.

## 2. Unchanged research and source freeze

Dataset: DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0;
FX_SPOT_OTC / EURUSD; Dukascopy H1 BID/ASK.
LEFT_UNSEEN [2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z);
RIGHT_UNSEEN [2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z).
Already consumed interval is ineligible.
Frozen UTC CORE_ACTIVE 07..16; TRANSITION 17..20; OFF_HOURS 21..06.
Exact NEXT_1H same-segment only, original gap/closure/cleaning rules,
no interpolation or cross-segment bridging.

2010 prepared rows; 1991 eligible hourly starts:
CORE_ACTIVE 838, OFF_HOURS 837, TRANSITION 316;
LEFT_UNSEEN 1542, RIGHT_UNSEEN 449.
Three genuine missing LEFT expected market hours remain excluded.

Source bundle SHA-256:
65a782b3fcc05bd7868f17429f478cd9613bca11be4fd859ae0ed1096be7f5e2
Prepared CSV SHA-256:
b1091c4975665b2b0cd4f58627a10aceaab7aeff5076431abb6abc74c0a054c1
RF-023 preparation JSON SHA-256:
d2eadd9a64da74ae79e2a0008426147953f24beb8c23f66557a721a7b8a65381

Original HYP-0005 runner:
tools/hyp0005_proto01.py
Git blob: 814193997768605fe60607d66dfd755a9323f339
HYP-0004 arithmetic Git blob:
cbc9a46bf5e5296615f51c0ea564153968bc2a55
RF-023 geometry source code Git blob:
b8d72d858d5c2691de7dec9a709f6e4d7ccb2808
HYP-0005 hypothesis card Git blob:
ebbbc89187c911485c1568dc11f5f2f9e703718a
RF-024 manifest Git blob:
03dccee9c7f21fff77ade9347b9730b79d6c62c7

Both predeclared primary comparisons are required:
1. median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)
2. median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)

Both true: CONFIRMATORY_STRUCTURAL_PASS.
Either false: CONFIRMATORY_STRUCTURAL_FAIL, negative evidence RETAINED.
TRANSITION and calendar-year values are diagnostic only, never rescuing FAIL.

Data Feasibility remains CONDITIONAL / H1_OPEN_PROXY_AT_EVENT_TIME;
exact_tick_boundary_time_known=false.
September provider provenance:
USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER.
No trading P&L, economic viability, independent examination or Candidate.

## 3. Gate order: no reveal before exact main

1. GPT stages the authorization, source-of-truth update, gate module,
   narrow output ignore rules and synthetic-only tests in branch
   agent/rf037-hyp0005-authorized-one-shot-reveal.
2. OWNER executes .\ATS_AGENT_PREFLIGHT.bat at the exact agent HEAD.
   Preflight runs validator, Ruff, pytest and environment, NO REVEAL.
3. GPT verifies the exact-head PASS before squash-merging the PR.
4. OWNER switches to main, git pull --ff-only, checks exact merged HEAD,
   and executes .\ATS_TASK_CHECK.bat ONCE.
5. Exact-main checker verifies HEAD/origin/CLEAN, RF-024/035/036 ancestry,
   all frozen Git blobs, original ten source hashes and 2010/1991
   preparation geometry, manifest/schema, RF-023 JSON/TXT/CSV identity,
   preserved HYP-0006 evidence, positive/negative criteria,
   one explicit OWNER authorization and FULL ATS Local CI.
6. Only after ALL prechecks PASS, the one-shot module
   tools/hyp0005_first_reveal_gate.py rechecks exact main, frozen
   runner and original data hashes and absence of prior output.
7. BEFORE the first market computation, write the exclusive consumed
   marker (open in x mode, flush and os.fsync). Then invoke exactly
   the frozen run_first_reveal_once(authorized=True) once.
8. Preserve result JSON, TXT and one exclusive receipt binding original
   output SHA-256, exact commit, dataset identity and original decision.
   Every negative result remains preserved, no tuning or rescue.
9. Repeated task checker calls may validate an existing complete
   marker/result/receipt set HASH-ONLY. They NEVER recompute the result.
   Missing, partial or mismatched files mean TECHNICAL_BLOCKER, and
   prohibit automatic retry or deletion.
10. Only exact-main CURRENT TASK CHECK PASS and TASK LAUNCHER PASS,
    plus review of the saved receipt, can close RF-037.
    Step 5/5 remains a separate post-reveal review.

## 4. Local output identities

These four files must be absent BEFORE the one-shot first reveal,
and specifically ignored by .gitignore:

reports/local_ci/HYP0005_PROTO01_FIRST_REVEAL_CONSUMED.json
reports/local_ci/HYP0005_PROTO01_RESULT.json
reports/local_ci/HYP0005_PROTO01_RESULT_REPORT.txt
reports/local_ci/HYP0005_PROTO01_FIRST_REVEAL_RECEIPT.json

The consumed marker is durable BEFORE any outcome computation.
Failure after marker creation consumes the authorization until
independent technical review. No silent retry.

After exact-main execution OWNER must send:
reports/local_ci/CURRENT_TASK_REPORT.txt
and the four original local HYP-0005 first-reveal files.
Do not edit, overwrite, rename or rerun the output.

## 5. Research information boundary

Before authorized exact-main first reveal:
HYP-0005: NO_CONFIRMATORY_OUTCOME_COMPUTED
FIRST REVEAL: AUTHORIZED_ONCE / NOT_EXECUTED

After it, record its original positive or negative result and proceed
to research step 5/5 for interpretation and routing. A structural PASS
does not create a directional Strategy, prove profit or automatically
authorize R4, validation, live execution or capital allocation.
