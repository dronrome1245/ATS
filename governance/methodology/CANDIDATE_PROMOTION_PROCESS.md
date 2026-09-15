# ATS Candidate Promotion Process

**Task:** `ATS2-M1-006`  
**Work package:** `WBS-1.6`  
**Status:** BASELINE  
**Purpose:** admit a successful Research Funnel line into Strategy Candidate status only through an explicit review, while preserving lineage, negative history and preliminary-evidence limitations.

## 1. Scope

Candidate Promotion is the control between the Research Funnel and the formal Strategy Lifecycle.

It starts only after Economic Pre-Screen has produced:

`ADVANCE_TO_CANDIDATE_REVIEW`.

The review asks:

> Is the Research Funnel package coherent and economically promising enough to justify a named Strategy Candidate and a larger formal research budget, with its weaknesses and unresolved questions made explicit?

Candidate Promotion does not prove profitability, validation, robustness, production readiness or live suitability.

Flow:

`R0–R4 package → Candidate Promotion Review → PROMOTE / PARK / REJECT`

Only `PROMOTE` creates a `CAND-xxxx` object.

## 2. Required upstream package

A Candidate Promotion Review requires a traceable package containing:

1. a registered Parent Idea with the relevant intake history;
2. the current primary `HYP-xxxx` and its lineage;
3. the applicable Data Feasibility Review;
4. all Cheap Prototype iterations materially relevant to the decision, including negative/unattractive iterations;
5. the Economic Pre-Screen with decision `ADVANCE_TO_CANDIDATE_REVIEW`;
6. known search/research-degrees-of-freedom history;
7. known data, execution, economic and operational limitations;
8. known failure modes and unresolved research questions.

If the package is materially incomplete or contradictory, the review is `BLOCKED` and no promotion decision is issued until the inconsistency is resolved. `BLOCKED` is a workflow state, not a fourth promotion decision.

## 3. Promotion Review artifact

Canonical template:

`governance/methodology/templates/CANDIDATE_PROMOTION_REVIEW_TEMPLATE.md`

For a real research line, each review attempt is stored as:

`research/reviews/HYP-xxxx-CANDIDATE-PROMOTION-nn.md`

Local review sequence:

`CPR-01`, `CPR-02`, and so on.

Rules:

1. A review attempt is never overwritten to hide a prior `PARK` or `REJECT`.
2. A later review receives the next sequence number.
3. The review records all inputs used for its decision.
4. `PARK` and `REJECT` reviews remain searchable even though no Candidate is created.
5. A structural methodology test does not create a real review artifact or Candidate.

## 4. Candidate identity

Candidate IDs use:

`CAND-0001`, `CAND-0002`, and so on.

Canonical location after `PROMOTE`:

`research/candidates/CAND-xxxx/`

Minimum contents:

- `CANDIDATE.md`;
- `EVIDENCE_INDEX.md`.

Rules:

1. Candidate ID is assigned **only after** the promotion decision is `PROMOTE`.
2. `PARK` or `REJECT` does not consume or reserve a Candidate ID.
3. Candidate IDs are unique program-wide and never reused.
4. The next ID is the lowest unused positive sequence number above the highest Candidate ID already registered.
5. Renaming a Candidate does not change its ID.
6. Candidate ID is not a Strategy ID.

## 5. Candidate versus Strategy

A Strategy Candidate is permission to spend more research effort under the formal lifecycle. It is not yet a fully admitted `Strategy` entity.

After `PROMOTE`:

- Candidate status is `READY_FOR_S01`;
- `Strategy ID` remains `null`;
- formal `S01 Candidate Admission` later decides whether to create/admit the `STRAT-...` Strategy identity and continue to S02–S05.

Candidate Promotion therefore does not skip S01 and does not create a Strategy Version.

## 6. Review questions

The promotion reviewer must answer all of the following.

### P1 — Lineage integrity

Are Idea, Hypothesis, Data Feasibility, Prototype and Economic Pre-Screen linked without unexplained jumps or silent reformulation?

### P2 — Preliminary economic case

Does the Economic Pre-Screen support further research without a known fatal economic defect?

### P3 — Evidence honesty

Are exploratory, registered and other evidence classes labelled correctly, with no prototype presented as validation or pre-registered evidence?

### P4 — Negative/search history

Are failed variants, iterations, discarded alternatives and important search degrees of freedom visible enough to assess selection risk?

### P5 — Data/testability

Is the research line testable with the recorded data constraints, and are remaining data gaps explicit rather than assumed away?

### P6 — Known risks and failure modes

Are the major ways the observed effect could be false, unstable, untradeable or economically useless recorded?

### P7 — Bounded research objective

Is there a clear proposed S02–S05 research scope that can convert the Candidate into a defined Strategy Version and test economic viability without unlimited optimization?

### P8 — Resource proportionality

Does the likely research/platform effort remain proportionate to the preliminary opportunity, including strategy-specific versus reusable platform work?

## 7. Evidence classification at promotion

Candidate promotion may use preliminary/exploratory artifacts because its purpose is deciding whether deeper research is worth funding.

The Candidate package must not erase evidence class distinctions.

At minimum, each referenced artifact in `EVIDENCE_INDEX.md` records:

- artifact/reference;
- research stage;
- evidence class;
- question/result supported;
- known limitations;
- whether it was pre-registered;
- whether it is eligible for formal validation claims.

`EXPLORATORY_PROTOTYPE` remains exploratory after promotion.

A positive Candidate review cannot retroactively promote exploratory results into registered or validation evidence.

## 8. Known risks and unresolved questions

Promotion requires explicit disclosure of open weaknesses.

The review records, where applicable:

- data/timestamp uncertainty;
- incomplete cost model;
- concentration/outlier dependence;
- low effective opportunity diversity;
- capacity uncertainty;
- execution sensitivity;
- parameter/search dependence;
- operational/data complexity;
- missing robustness evidence;
- unresolved mechanism questions;
- platform capabilities likely required later.

An unknown is not automatically a rejection, but it must have a plausible research path and must not be silently converted into a favorable assumption.

## 9. Proposed S02–S05 research scope

Before `PROMOTE`, define the initial formal research objective through S05.

The scope states what the Candidate must eventually establish across:

- `S02 Research Specification` — unambiguous trading/research rules;
- `S03 Data & Research Protocol` — controlled datasets, periods, costs and protocol;
- `S04 Baseline Implementation` — reproducible implementation and registered baseline experiments;
- `S05 Economic Viability` — stronger net economics, risk/capital efficiency, evidence quality, capacity and operational viability.

The scope is a research plan, not a promise that S05 will pass.

It should also identify likely platform needs as `NEED`, without prematurely building production infrastructure.

## 10. Decision model

Exactly one decision is issued for a completed promotion review.

### `PROMOTE`

Meaning: the upstream Research Funnel package is coherent and sufficiently promising to justify creating a Strategy Candidate and entering formal Candidate admission work.

Required consequences:

1. assign the next `CAND-xxxx` ID;
2. create `research/candidates/CAND-xxxx/CANDIDATE.md` from the canonical Candidate template;
3. create `research/candidates/CAND-xxxx/EVIDENCE_INDEX.md` from the Candidate Evidence Index template;
4. record the promotion-review reference;
5. set Candidate status `READY_FOR_S01`;
6. leave `Strategy ID` as `null` until S01;
7. preserve all upstream negative/search history by reference.

`PROMOTE` means “worth formal research”, not “edge proven”.

### `PARK`

Meaning: the line may remain promising, but Candidate creation is not justified now because a material resource, data, platform, priority or evidence block remains.

Required consequences:

- no `CAND-xxxx` is created;
- no Candidate ID is reserved;
- the blocking condition and reopening criterion are recorded;
- the review remains in history.

A later review uses a new `CPR-nn` sequence.

### `REJECT`

Meaning: the package does not justify formal Candidate research expenditure.

Typical reasons include:

- fatal lineage/evidence integrity problem;
- preliminary economics already insufficient;
- effect depends on hidden selection/search that makes further spend unjustified;
- data/testability defect cannot be resolved without changing the Hypothesis;
- required complexity/resources are disproportionate;
- known failure mode already defeats the research thesis.

Required consequences:

- no Candidate is created;
- the review and rejection reason are retained;
- a materially changed future claim must return through the appropriate upstream stages rather than reusing this decision.

## 11. No automatic promotion

The following do **not** create a Candidate by themselves:

- Idea `SCREEN`;
- Hypothesis `DATA_FEASIBILITY`;
- Data Feasibility `FEASIBLE`;
- a positive-looking Cheap Prototype;
- Economic Pre-Screen `ADVANCE_TO_CANDIDATE_REVIEW`;
- a high return or attractive chart;
- methodology completion in M1.

A Candidate exists only after an explicit `PROMOTE` review decision and Candidate artifact creation.

## 12. Material change after promotion

A material change to the research claim after promotion must not be hidden inside the existing Candidate.

If the change affects the primary Hypothesis Statement, Mechanism, Market/universe, Conditions, Horizon, expected Direction, information-time premise or Falsification rule:

1. create a new `HYP-xxxx` according to Hypothesis change control;
2. repeat applicable Data Feasibility / Prototype / Economic Pre-Screen work;
3. perform a new Candidate Promotion Review;
4. if promoted, assign a new Candidate ID;
5. retain the old Candidate and mark it `SUPERSEDED` or otherwise closed by the later lifecycle process.

Minor documentation corrections that do not change the research claim may remain under the same Candidate.

## 13. Candidate template usage

Canonical Candidate template:

`governance/methodology/templates/CANDIDATE_TEMPLATE.md`

Canonical Candidate Evidence Index template:

`governance/methodology/templates/CANDIDATE_EVIDENCE_INDEX_TEMPLATE.md`

The Candidate template is copied **only after** `PROMOTE`.

The created Candidate must record:

- Candidate ID;
- Parent Idea ID;
- Parent Hypothesis ID;
- promotion-review reference;
- Data Feasibility / Prototype / Economic Pre-Screen references;
- preliminary economic rationale;
- evidence limitations/search history;
- known risks/failure modes;
- unresolved research questions;
- proposed S02–S05 research scope;
- likely platform/capability needs;
- `Strategy ID: null` until S01;
- status `READY_FOR_S01`.

## 14. Decision authority

Routine Candidate Promotion may be performed by RESEARCH / VALIDATION program-review roles under this methodology because it creates no real market exposure and allocates no live capital.

OWNER approval is not required by the ATS safety boundary for `PROMOTE`, `PARK` or `REJECT` at this stage.

OWNER rights remain reserved for program capital policy, Strategy Risk Mandate, live admission, allocation, scaling and profit withdrawal.

## 15. Structural acceptance test

The Candidate Promotion Review, Candidate and Candidate Evidence Index templates are structurally tested without creating a fictitious Idea, Hypothesis, market, return, Candidate or Strategy.

The structural test verifies that the templates can represent:

- complete R0–R4 lineage;
- promotion-review sequence;
- `PROMOTE / PARK / REJECT`;
- Candidate creation only on `PROMOTE`;
- stable `CAND-xxxx` identity;
- `Strategy ID: null` before S01;
- preliminary evidence classes/limitations;
- negative/search history;
- known risks/failure modes;
- unresolved questions;
- proposed S02–S05 scope;
- platform/capability needs;
- Candidate status `READY_FOR_S01`.

No Candidate ID is allocated by this structural test, so `strategy_pipeline.candidates_active` remains unchanged.

## 16. Definition of Done for a real promotion review

A real Candidate Promotion Review is complete when:

- required upstream R0–R4 artifacts are linked;
- Economic Pre-Screen decision is `ADVANCE_TO_CANDIDATE_REVIEW`;
- evidence classes and limitations are explicit;
- negative/search history is visible;
- known risks/failure modes and unresolved questions are recorded;
- a bounded S02–S05 research scope is defined;
- exactly one decision among `PROMOTE / PARK / REJECT` is recorded with reason;
- `PARK`/`REJECT` create no Candidate;
- `PROMOTE` creates one uniquely identified `CAND-xxxx` package with status `READY_FOR_S01` and no Strategy ID yet.

## 17. M1-006 completion result

This process plus the aligned Candidate Promotion Review, Candidate and Candidate Evidence Index templates satisfies `WBS-1.6`.

Next program-level work:

`ATS2-M1-007 — Experiment registration schema`.

That step operationalizes how a formal experiment is registered **before** its result can be used as registered evidence.