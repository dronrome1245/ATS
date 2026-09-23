# M6 Exit Review — Reference Strategy #2 & Platform Generalization

**Task:** `ATS2-M6-009`  
**Milestone:** `M6_REFERENCE_STRATEGY_2`  
**Decision:** `PASS`  
**Date:** 23 September 2026

## 1. Purpose

This review decides whether M6 achieved its program objective:

> test whether the ATS Research Factory and Shared Platform can support a second materially different strategy profile, preserve negative evidence honestly, and identify what is genuinely reusable versus still unproven.

A `PASS` here does **not** mean Reference Strategy #2 succeeded.

Reference Strategy #2 was rejected at the Cheap Prototype stage:

`HYP-0002 / PROTO-01 = REJECTED_AT_R3`

M6 passes because ATS applied the research process to a second distinct profile, froze and revealed a separate confirmatory block without post-result rescue, preserved the negative result, and recorded reusable platform/process learnings.

## 2. M6 exit criterion

Canonical WBS exit criterion:

> ATS proves that the Research Factory and Shared Platform are applicable to at least two different strategy profiles, or identifies concrete architectural limitations with preserved evidence.

This criterion is satisfied.

The two exercised profiles are materially different:

1. Reference Strategy #1 — single-instrument 1H long/flat trend breakout;
2. Reference Strategy #2 — single-instrument 1H two-sided return-tail reversal.

Both passed through Idea/Hypothesis/Data Feasibility/Cheap Prototype with real EUR/USD BID/ASK data and reproducible dataset identity.

Both were stopped at R3 by rules fixed before their terminal prototype results.

## 3. M6 work-package result

| Work package | Result | Evidence / consequence |
|---|---|---|
| `WBS-6.0` Market Pattern Discovery | DONE | bounded discovery methodology/tooling plus full 16-alternative history |
| `WBS-6.1` Select Strategy #2 | DONE | two-sided return-tail reversal class selected without promoting one discovery cell as winner |
| `WBS-6.2` Run Research Funnel | DONE / terminal early rejection | HYP-0002 Data Feasibility and frozen PROTO-01 ended with `REJECTED_AT_R3` |
| `WBS-6.3` Identify new data needs | NOT ENTERED | R3 rejection removed the need for deeper strategy-specific data capability |
| `WBS-6.4` Extend Strategy API | NOT ENTERED | no Candidate/baseline implementation justified API expansion |
| `WBS-6.5` Event/news support | NOT ENTERED | Strategy #2 did not require event/news data |
| `WBS-6.6` Baseline & Economic Viability #2 | NOT ENTERED | no advance to Economic Pre-Screen/Candidate path |
| `WBS-6.7` Platform reuse review | PASS via early-rejection path | `governance/program/REFERENCE_STRATEGY_2_CLOSEOUT.md` |
| `WBS-6.8` Validation handoff #2 | NOT ENTERED | no S05 PASS Candidate exists |

M6 does not fabricate completion of work packages whose dependencies were never reached.

## 4. Reference Strategy #2 terminal result

Canonical result:

`reports/research/HYP-0002-PROTOTYPE-01-result.json`

Result SHA-256:

`cf89ae89680aad25d24944dc737c4092f995327dca022a7c6a19d7ea102e552e`

Reveal commit:

`96d7b90ac908cacccfefbccbe8daa06867b2f18c`

Decision:

`REJECT — ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED`

Observed frozen result:

- high-tail/DOWN: `201` events, positive mean and positive excess versus same-direction baseline;
- low-tail/UP: `122` events, negative mean and negative excess versus same-direction baseline;
- high-tail/DOWN overlapping-window share: `0.9203980099502488`;
- low-tail/UP overlapping-window share: `0.9016393442622951`.

The passing high-tail/DOWN side was not allowed to replace the failed two-sided HYP-0002 after reveal.

## 5. What proved reusable

### Research governance

The same lifecycle discipline worked for both profiles:

- Idea and falsifiable Hypothesis before material testing;
- Data Feasibility before prototype execution;
- frozen data identity and timing semantics;
- pre-written prototype question and decision rule;
- negative outcome retention;
- no post-result rescue inside the same Hypothesis.

### Data identity and integrity

Both lines used explicit:

- BID/ASK field semantics;
- UTC timestamps and availability semantics;
- gap policy;
- dataset manifests/hashes;
- local/external licensed market bytes rather than committing raw data.

### Local quality gate

The second line strengthened reusable engineering controls:

- repository validator;
- Ruff lint and format as separate gates;
- fast pytest collection/import verification;
- full pytest;
- exact state/handoff/backlog reconciliation;
- complete validator-marker audit;
- narrow runtime-output ignore rules.

### Discovery accounting

M6 added bounded market-pattern discovery with a retained full search denominator and negative alternatives. That capability remains reusable for future development-data searches.

## 6. What remains unproven

M6 does **not** prove:

- that a Strategy Candidate can reach S05;
- that the shared Strategy API supports two deep Candidate implementations;
- that M4.9/M4.10 validation works on a real promoted Candidate;
- that any strategy is economically viable;
- that any strategy is ready for demo, live execution or capital allocation.

Because both reference lines stopped at R3, deep platform generalization beyond the Research Funnel remains untested.

This is a concrete architectural/evidence boundary, not a reason to invent downstream work.

## 7. Program consequence

Current candidate count:

`0`

Therefore:

- M4.9 remains `BLOCKED_PENDING_S05_CANDIDATE`;
- M4.10 remains blocked behind M4.9;
- M5 remains `NOT_STARTED`;
- M7/M8 remain unavailable;
- no broker/account/risk mandate/live allocation decision is appropriate.

The critical path to a meaningful live candidate still requires a future research line to survive R3/R4 and reach S05.

## 8. Strategy sourcing consequence

Reference Strategy #1 and Reference Strategy #2 are both closed at R3.

Neither line may be reopened by silently changing its failed hypothesis.

If research continues, the next strategy must enter as a new Idea/Hypothesis/research line with its own search accounting and Data Feasibility.

A separate program rebaseline should define that Strategy #3 sourcing lane rather than stretching the `Reference Strategy #2` milestone indefinitely.

## 9. Safety boundary

M6 Exit does not authorize:

- Candidate or Strategy creation for HYP-0001 or HYP-0002;
- demo/shadow trading;
- real-money trading;
- broker/account selection;
- Strategy Risk Mandate;
- capital allocation;
- leverage;
- scaling.

All live/capital permissions remain false.

## 10. Decision

`M6_REFERENCE_STRATEGY_2 = COMPLETED / PASS`

Reference Strategy #2 research outcome remains:

`REJECTED_AT_R3`

Reference Strategy #1 research outcome remains:

`REJECTED_AT_R3`

M4 reusable framework remains available but strategy-specific validation stays blocked pending a future S05 PASS Candidate.

## 11. Transition-commit closure

This review records the M6 exit decision, but operational closure still requires the normal exact-commit Local CI Gate.

M6 is operationally closed only after `ATS_TASK_CHECK.bat` passes on the final commit containing:

- this M6 Exit Review;
- synchronized canonical state/backlog/status/next-step/handoff;
- validator/task-check updates.

After that exact-head PASS, the program should create a separate roadmap rebaseline for Strategy #3 sourcing.
