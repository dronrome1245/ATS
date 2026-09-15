# ATS Economic Pre-Screen

**Task:** `ATS2-M1-005`  
**Work package:** `WBS-1.5`  
**Status:** BASELINE  
**Purpose:** decide whether a research line appears economically valuable enough to justify Candidate review and a larger research budget after Cheap Prototype work.

## 1. Scope

Economic Pre-Screen is Research Funnel stage `R4`.

It starts only after a Cheap Prototype has produced outcome `ADVANCE_TO_ECONOMIC_SCREEN`. The review must include the relevant Data Feasibility constraints and the complete known prototype/search history, including negative or unattractive variants.

The question is:

> Is the preliminary effect potentially valuable enough, after realistic costs, capital use, risk, uncertainty and operational burden, to justify more expensive formal research?

Economic Pre-Screen does not prove profitability, statistical validity, robustness or live suitability.

Flow:

`Cheap Prototype → Economic Pre-Screen → ADVANCE_TO_CANDIDATE_REVIEW / RETURN_TO_RESEARCH / PARK / REJECT`

`ADVANCE_TO_CANDIDATE_REVIEW` does not itself create a Strategy Candidate. Candidate creation and formal `PROMOTE / PARK / REJECT` admission are defined by `ATS2-M1-006`.

## 2. Canonical artifact and template

Reusable template:

`governance/methodology/templates/ECONOMIC_PRE_SCREEN_TEMPLATE.md`

For a real research line, the review instance is stored under:

`research/reviews/HYP-xxxx-ECONOMIC_PRE_SCREEN.md`

The review references:

- Parent `Idea ID`;
- primary `Hypothesis ID`;
- Data Feasibility review;
- all Cheap Prototype iterations materially relevant to the decision;
- known failed/negative variants that affect interpretation.

## 3. No universal profitability threshold

ATS does not define one program-wide:

- annual return target;
- Sharpe threshold;
- minimum trade count;
- minimum profit factor;
- maximum drawdown threshold;
- minimum capacity number;
- capital allocation amount.

Different strategy classes have different horizons, opportunity frequencies, capital usage, execution constraints and evidence structures.

The Pre-Screen therefore evaluates whether the preliminary economics are **plausibly useful relative to costs, uncertainty, capital, risk and complexity**, not whether a universal number is exceeded.

Concrete strategy-specific thresholds may be defined later in the Strategy Economic Profile and registered research protocol.

## 4. Inputs required before decision

A Pre-Screen must contain or explicitly mark unknown for:

- Parent Idea ID;
- Hypothesis ID;
- Data Feasibility review reference and decision;
- Prototype references and outcomes;
- preliminary effect magnitude;
- gross economic estimate if applicable;
- applicable early cost assumptions;
- preliminary net economic estimate or reason it cannot yet be estimated;
- opportunity frequency and diversity;
- capital usage characteristics;
- preliminary risk/path characteristics;
- concentration warnings;
- capacity/scalability considerations;
- data, execution and operational complexity;
- evidence weaknesses;
- research degrees of freedom/search history;
- sensitivity/margin-of-safety observations;
- unresolved questions;
- final Pre-Screen decision and reason.

Unknown values remain unknown. They are not replaced with invented return, capital, cost or risk numbers.

## 5. Economic dimensions

The review assesses the following dimensions. They are a structured scorecard, not a mechanically weighted formula.

Allowed dimension assessments:

`FAVORABLE / UNCERTAIN / UNFAVORABLE / NOT_APPLICABLE`

Every assessment requires a short reason and supporting preliminary artifact/reference.

### E1 — Effect Magnitude

Question:

> Is the observed effect large enough to be distinguishable from data resolution, measurement noise and obvious implementation approximations?

Consider:

- effect size in units appropriate to the research class;
- stability of sign/direction across the limited prototype scope;
- whether the result is driven by one extreme observation;
- whether magnitude is meaningful relative to the stated hypothesis and baseline.

A statistically interesting but economically microscopic effect may be `UNFAVORABLE`.

### E2 — Gross/Net Economics and Cost Sensitivity

Question:

> Is there plausible economic value after the costs that matter for this research class?

Use the simplest defensible early model available from Data Feasibility and the prototype.

Potential inputs include:

- spread;
- commission;
- slippage proxy;
- financing;
- execution delay;
- market impact/capacity warning;
- data/infrastructure expense when materially relevant.

If only gross economics are available, this dimension cannot be marked fully favorable without explaining why costs are unlikely to dominate the effect.

### E3 — Opportunity Frequency and Effective Diversity

Question:

> Are there enough economically relevant opportunities, and enough diversity among them, to make further research worthwhile and eventually support useful evidence?

Consider:

- raw opportunity count;
- temporal distribution;
- event/regime diversity;
- cross-sectional diversity;
- clustering/dependence;
- long inactive periods;
- whether one market episode generates most observations.

There is no universal minimum count. A rare strategy may still be attractive, but evidence may be expensive or practically impossible to accumulate.

### E4 — Capital Use and Capital Efficiency

Question:

> What kind of capital commitment would the strategy concept require relative to its potential economic contribution?

At Pre-Screen stage evaluate qualitatively or with available preliminary measures:

- time capital is tied up;
- margin/collateral intensity if applicable;
- turnover and cash usage;
- idle-capital implications;
- whether the economic effect appears too small relative to required capital commitment.

This is not a capital-allocation decision. No program capital amount is assigned here.

### E5 — Risk, Path and Concentration

Question:

> Does the preliminary payoff path suggest a risk burden that could make the effect economically unattractive even if the aggregate return is positive?

Consider what the prototype can reasonably reveal:

- drawdown/path shape;
- loss clustering;
- tail-like losses;
- payoff asymmetry;
- concentration in top observations/events;
- dependence on gaps/outliers;
- time/regime concentration.

R3 data are preliminary; this dimension identifies warnings rather than pretending to be full validation.

### E6 — Capacity and Scalability

Question:

> Is there a plausible path to economically useful scale, or is the opportunity structurally too small/fragile?

Consider where applicable:

- liquidity;
- turnover;
- market depth;
- event crowding;
- execution sensitivity;
- opportunity size;
- likely degradation as notional increases.

No precise capacity estimate is required before the necessary data exist. Unknown capacity is recorded as uncertainty, not assumed infinite.

### E7 — Operational, Data and Execution Burden

Question:

> Is the likely implementation burden proportionate to the potential value?

Consider:

- special/expensive data feeds;
- latency requirements;
- complex timestamp/revision handling;
- custom execution;
- manual operations;
- monitoring burden;
- failure/reconciliation risk;
- strategy-specific infrastructure unlikely to be reusable.

A small edge requiring a disproportionately expensive stack is economically weak even if the prototype looks positive.

### E8 — Evidence Quality and Research Freedom

Question:

> How much confidence should ATS place in the preliminary result given the amount of search that produced it?

Consider:

- prototype iteration count;
- parameter variants inspected;
- markets/instruments inspected;
- horizons/conditions tried;
- discarded variants;
- data-source changes;
- hypothesis changes;
- sample dependence/concentration;
- known unresolved data limitations.

A selected best result after broad exploratory search receives weaker economic weight than a simple baseline result from a narrow pre-motivated test.

### E9 — Economic Margin of Safety

Question:

> Does the preliminary economic case survive small realistic deterioration, or does the edge disappear immediately?

Use only simple, explainable sensitivity checks appropriate to the stage, such as:

- moderately worse costs;
- modest execution delay/degradation;
- removal of one dominant observation/episode;
- nearby reasonable baseline assumptions;
- conservative rounding of uncertain inputs.

No universal stress multiplier is imposed.

If a small realistic deterioration destroys all apparent value, the research line normally should not advance without a specific reason for `RETURN_TO_RESEARCH`.

## 6. Margin of safety versus precision

Pre-Screen should be conservative but not falsely precise.

It is acceptable to say:

- cost estimate is approximate but likely much smaller than the observed effect;
- capacity is unknown and therefore remains a Candidate-review risk;
- opportunity diversity is insufficient and requires more research;
- capital efficiency cannot yet be quantified but appears structurally problematic.

It is not acceptable to fabricate decimals, annualized returns or capital requirements from evidence that cannot support them.

The goal is to detect clear economic weakness early, not to produce a production-grade valuation model.

## 7. Net economics rule

When the research concept implies trading, an economically positive claim should not rely only on gross P&L/effect if transaction/execution costs are material.

The review records:

1. gross preliminary effect;
2. cost components included;
3. net preliminary effect where estimable;
4. omitted cost components;
5. sensitivity to plausible worsening;
6. whether omitted costs could plausibly reverse the conclusion.

If omitted material costs could reasonably eliminate the effect, `ADVANCE_TO_CANDIDATE_REVIEW` requires a clearly stated justification or the line should return to research/park.

## 8. Opportunity frequency is not trade-count worship

A strategy is not rejected merely because it trades rarely.

The Pre-Screen asks instead:

- how many independent or partly independent opportunities exist;
- whether they span enough time/regimes/events to justify further work;
- whether an evidence program is realistically possible;
- whether the economic contribution per opportunity compensates for rarity.

A high raw trade count generated by one repeated market episode does not automatically improve the assessment.

## 9. Risk is a constraint, not the objective

The Pre-Screen does not prefer the lowest-risk idea regardless of economics.

A very low-risk effect can still be economically useless.

A high-return effect can still be unacceptable if preliminary tail/path characteristics or capital burden are disproportionate.

The decision considers the joint profile:

`Potential Return × Costs × Risk × Capital × Evidence × Capacity × Complexity`

The purpose is not to maximize one component but to decide whether the research line deserves more resources.

## 10. Complexity budget

Complexity is an economic cost.

When two research lines appear economically similar, the line requiring less unique infrastructure, fewer fragile data assumptions and lower operational burden is generally more attractive.

Complexity may be justified by a materially larger or more diversifying opportunity, but the justification must be explicit.

Pre-Screen must identify whether major future work is likely to be:

- reusable platform capability;
- strategy-specific engineering;
- external data/access cost;
- execution-specific complexity;
- operational/manual burden.

## 11. Research degrees of freedom penalty

Economic attractiveness is discounted qualitatively when the preliminary result emerged after extensive search.

Examples of increased research risk:

- many parameter combinations;
- many markets with only one winner reported;
- repeated changes to horizon/condition;
- multiple data sources tried after failures;
- repeated prototype iterations without a stable reason;
- selective exclusion of bad periods/observations.

Pre-Screen does not attempt to solve multiple testing statistically at R4. It records the burden and may require stronger later evidence or reject/return the line if the result is too selection-dependent.

## 12. Decision model

### `ADVANCE_TO_CANDIDATE_REVIEW`

Meaning: the preliminary economic case is sufficiently promising to justify formal Candidate admission review and a possible larger research budget.

Minimum interpretation:

- no known fatal economic defect;
- plausible value remains after relevant early costs;
- capital/risk/complexity do not obviously dominate the opportunity;
- evidence weaknesses are known and appear addressable by formal research;
- economic margin of safety is not obviously absent.

This decision is **not** Candidate promotion and does not create a Strategy ID.

### `RETURN_TO_RESEARCH`

Meaning: one or more specific uncertainties prevent Candidate review, but they can be answered with a bounded additional research step without changing success criteria after the fact.

The review must state:

- exact unresolved question;
- why it matters economically;
- permitted next research action;
- what result would resolve the question;
- maximum intended scope/iteration before another decision.

`RETURN_TO_RESEARCH` must not become unlimited optimization.

If resolving the issue materially changes the Hypothesis, create a new `HYP-xxxx` and repeat applicable upstream stages.

### `PARK`

Meaning: the research line may be economically interesting but should not consume active research budget now because a material external/resource/data/platform dependency is unresolved or opportunity cost is too high.

The blocking condition is recorded. Reopening requires evidence that the block changed.

### `REJECT`

Meaning: the preliminary economics do not justify further material research expenditure.

Typical reasons include:

- effect too small relative to realistic costs;
- no plausible economic margin of safety;
- capital use disproportionate to expected contribution;
- risk/path characteristics dominate the apparent return;
- opportunity/evidence structure is practically too weak;
- capacity appears structurally negligible;
- operational/data/execution burden is disproportionate;
- apparent economics depend mainly on broad search/selection and cannot justify further spend.

Rejection and its reason are retained.

## 13. Scorecard discipline

A Pre-Screen must not collapse all dimensions into a single universal numeric score.

The canonical template records each E1–E9 assessment plus rationale.

Decision guidance:

- `ADVANCE_TO_CANDIDATE_REVIEW` normally requires no dimension with a known fatal `UNFAVORABLE` condition and a coherent overall economic case;
- `RETURN_TO_RESEARCH` is used when a bounded question could materially change one or more `UNCERTAIN` dimensions;
- `PARK` is used when the main barrier is external/timing/resource dependency rather than a negative economic conclusion;
- `REJECT` is used when the economic case is already insufficient or structurally fragile.

A favorable majority does not override one fatal defect automatically.

## 14. Relationship to Candidate promotion

Economic Pre-Screen and Candidate promotion are separate controls.

M1-005 produces a review recommendation.

M1-006 will determine the formal Candidate admission process and how `ADVANCE_TO_CANDIDATE_REVIEW` becomes one input to `PROMOTE / PARK / REJECT`.

Candidate review must be able to see:

- Idea and Hypothesis lineage;
- Data Feasibility;
- prototype/search history;
- Pre-Screen scorecard;
- unresolved economic/evidence risks.

No Candidate is created merely because M1-005 methodology exists or because a prototype looks attractive.

## 15. Relationship to later S05 Economic Viability

R4 Economic Pre-Screen is deliberately cheaper and weaker than formal `S05 Economic Viability`.

R4 asks whether deeper research is worth funding.

S05 later asks whether a defined Strategy Version has sufficient net edge, risk efficiency, capital efficiency, evidence quality, capacity and operational viability to justify expensive validation.

Passing R4 does not imply passing S05.

## 16. Decision authority

Routine Economic Pre-Screen may be performed by RESEARCH / VALIDATION roles under the canonical rubric because no real capital is allocated and no live exposure is created.

OWNER approval is not required for `ADVANCE_TO_CANDIDATE_REVIEW`, `RETURN_TO_RESEARCH`, `PARK` or `REJECT` at R4.

OWNER rights remain reserved for program capital policy, Strategy Risk Mandate, live admission, allocation, scaling and profit withdrawal.

## 17. Structural acceptance test

`ECONOMIC_PRE_SCREEN_TEMPLATE.md` is tested against this methodology without creating a fictitious strategy, return, capital requirement, risk limit, cost assumption or market result.

The template must represent:

- Idea/Hypothesis lineage;
- Data Feasibility linkage;
- all material Prototype references;
- preliminary magnitude;
- gross/net/cost sensitivity;
- opportunity frequency/diversity;
- capital use;
- risk/path/concentration;
- capacity;
- operational/data/execution complexity;
- evidence weakness/search history;
- margin of safety;
- E1–E9 scorecard;
- unresolved questions;
- one decision and reason.

The structural test verifies fields only. It does not populate invented economics.

## 18. Definition of Done for a real Economic Pre-Screen

A real Pre-Screen is complete when:

- all required lineage/review/prototype references are recorded;
- material negative prototype/search history is visible;
- E1–E9 are assessed with rationale or explicit `NOT_APPLICABLE`;
- realistic early costs are included or missing costs are explicitly treated as uncertainty;
- capital/risk/capacity/complexity implications are addressed at the level supported by evidence;
- margin of safety is considered;
- evidence weakness and research freedom are recorded;
- one decision among `ADVANCE_TO_CANDIDATE_REVIEW / RETURN_TO_RESEARCH / PARK / REJECT` is recorded with reason;
- the decision does not claim profitability or validation;
- negative decisions remain retained.

## 19. M1-005 completion result

This methodology plus `ECONOMIC_PRE_SCREEN_TEMPLATE.md` satisfies `WBS-1.5`.

Next dependent work:

`ATS2-M1-006 — Candidate promotion process`.

That step must formalize admission from a successful Research Funnel into a Strategy Candidate without treating preliminary/exploratory evidence as validated edge.