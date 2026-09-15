# M1 Exit Review — Research Methodology / Research Factory

**Task:** `ATS2-M1-011`  
**Milestone:** `M1_RESEARCH_METHODOLOGY`  
**Decision:** `PASS`  
**Date:** 15 September 2026

## 1. Purpose

This review decides whether ATS has operationalized the Research Factory sufficiently to enter M2 Research Platform MVP.

`PASS` means the research process is structurally reproducible and governed. It does **not** mean that any trading strategy has been shown profitable, validated or admitted to live trading.

## 2. Exit criterion

Program WBS defines M1 Exit as the ability to:

1. register a new Idea;
2. formulate a falsifiable Hypothesis;
3. review Data Feasibility;
4. run a bounded Cheap Prototype;
5. perform Economic Pre-Screen;
6. decide Candidate promotion;
7. preregister and retain formal Experiments;
8. classify evidence and its permissible claims;
9. conduct a repeatable research review producing an auditable decision.

The structural workflow is now complete.

## 3. WBS evidence

| Work package | Result | Canonical evidence |
|---|---|---|
| `WBS-1.1` Idea intake | PASS | `governance/methodology/IDEA_INTAKE_PROCESS.md` |
| `WBS-1.2` Hypothesis | PASS | `governance/methodology/HYPOTHESIS_MODEL.md` |
| `WBS-1.3` Data Feasibility | PASS | `governance/methodology/DATA_FEASIBILITY_REVIEW.md` |
| `WBS-1.4` Cheap Prototype | PASS | `governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md` |
| `WBS-1.5` Economic Pre-Screen | PASS | `governance/methodology/ECONOMIC_PRE_SCREEN.md` |
| `WBS-1.6` Candidate promotion | PASS | `governance/methodology/CANDIDATE_PROMOTION_PROCESS.md` |
| `WBS-1.7` Experiment registration | PASS | `governance/methodology/EXPERIMENT_REGISTRATION.md` |
| `WBS-1.8` Experiment registry | PASS | `experiments/REGISTRY.csv`, `experiments/README.md` |
| `WBS-1.9` Evidence classification | PASS | `governance/methodology/EVIDENCE_TAXONOMY.md` |
| `WBS-1.10` Research review | PASS | `governance/methodology/RESEARCH_REVIEW_PROTOCOL.md` package |

## 4. End-to-end structural walkthrough

A new research line can now follow:

`Observation → IDEA → HYP → Data Feasibility → PROTO → Economic Pre-Screen → Candidate Review → CAND (only on PROMOTE) → preregistered EXP → Registry → Evidence classification → Research Review`

At each step ATS defines:

- stable identity and lineage;
- allowed unknowns and blocking gaps;
- negative-result retention;
- no post-hoc upgrade of exploratory evidence;
- explicit costs/data/execution assumptions where relevant;
- bounded return-to-research rather than unlimited rescue optimization;
- immutable historical decision records.

No fictitious Idea, Hypothesis, Candidate, Experiment or market result was created to prove this workflow. Pipeline counters intentionally remain zero.

## 5. Evidence and review integrity

The M1 baseline now enforces:

- exploratory work cannot masquerade as preregistered evidence;
- an `EXP-...` must be registered before its result is observed;
- positive and negative Experiments remain discoverable;
- `source_class` is separated from `qualified_evidence_class`;
- attractive results do not upgrade evidence class;
- negative evidence retains the class earned by its protocol;
- Research Review cannot use a weaker class as a substitute for a required class;
- review decisions are retained and reconsideration creates a new review record.

## 6. M2 entry clarification

M2 builds the minimal reusable Research Platform MVP before selecting a concrete Reference Strategy #1.

To avoid premature strategy selection, M2 starts with:

`ATS2-M2-000 — Reference Consumer Profile`.

This profile describes the minimum consumer requirements needed to design the first vertical research stack without selecting a specific market, instrument, trading rule or expected return.

Only after that profile is fixed may `WBS-2.1 — Research stack ADR` choose the minimum technology stack.

Concrete Reference Strategy #1 selection remains an M3 decision.

## 7. Safety boundary

M1 Exit does not authorize:

- demo/shadow trading;
- real-money trading;
- capital allocation;
- Strategy Risk Mandate;
- broker/jurisdiction choice;
- scaling;
- profit withdrawal.

All corresponding safety permissions remain false. `reference_strategy_selection_allowed` also remains false during M2.

## 8. Decision

`M1_RESEARCH_METHODOLOGY = COMPLETED / PASS`.

ATS may enter:

`M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.

First M2 task:

`ATS2-M2-000 — Reference Consumer Profile`.

The next step is to define the minimum research-platform consumer profile, not to choose or test a concrete trading strategy.
