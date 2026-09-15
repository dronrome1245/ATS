# ATS Cheap Prototype Protocol

**Task:** `ATS2-M1-004`  
**Work package:** `WBS-1.4`  
**Status:** BASELINE  
**Purpose:** obtain one early quantitative answer at minimum reasonable cost without confusing exploratory prototype output with formal research or validation evidence.

## 1. Scope

Cheap Prototype is Research Funnel stage `R3`.

It starts only after:

- a registered `HYP-xxxx` exists;
- the Hypothesis is sufficiently specified and falsifiable;
- Data Feasibility is `FEASIBLE`, or `CONDITIONAL` with every prototype-relevant condition explicitly resolved or encoded as a limitation.

Flow:

`Hypothesis + Data Feasibility → one prototype question → minimal implementation → result → ADVANCE_TO_ECONOMIC_SCREEN / ITERATE / PARK / REJECT`

The prototype answers a narrow question such as whether an observable effect appears in the expected direction under the stated data/timing/cost assumptions.

It does not prove profitability, robustness, statistical validity, production readiness or live executability.

## 2. Core rule: one prototype, one question

Each prototype begins with one pre-written question.

Good examples of question shape:

- Does the effect appear in the expected direction under the stated condition?
- Does a simple baseline retain positive gross or net effect after the early conservative cost approximation?
- Is the event response materially different from the relevant baseline window?
- Is the relationship large enough to justify an Economic Pre-Screen?

Bad question shape:

- Find the most profitable parameters.
- Search every market until something works.
- Optimize the strategy.
- Prove that the idea is profitable.

If a second materially different question is needed, create another prototype iteration rather than silently expanding the original scope.

## 3. Prototype identity and canonical artifact

Cheap Prototype is intentionally lighter than a formal `Experiment` and does not receive an `EXP-...` ID merely for existing.

A prototype is identified by:

- parent `Hypothesis ID`;
- prototype sequence within that Hypothesis: `PROTO-01`, `PROTO-02`, and so on.

Canonical human-readable artifact:

`research/reviews/HYP-xxxx-PROTOTYPE-nn.md`

Canonical template:

`governance/methodology/templates/CHEAP_PROTOTYPE_TEMPLATE.md`

Rules:

1. Prototype sequence is not reused within the Hypothesis.
2. A new material question or materially changed implementation assumption creates a new prototype iteration.
3. Prototype implementation may be a notebook, script, query, event study, spreadsheet calculation or other minimal reproducible-enough artifact appropriate to the question.
4. Implementation/output references are recorded in the prototype artifact.
5. Prototype identity is not a substitute for formal Experiment registration.

## 4. Eligibility

Prototype work may start only when all of the following are true:

1. Parent Hypothesis is identified.
2. Hypothesis has a recorded transition to Data Feasibility.
3. Data Feasibility decision permits the planned prototype.
4. Any `CONDITIONAL` limitations relevant to the prototype are explicitly listed.
5. The prototype question is written before viewing its result.
6. The minimum data/timing/cost assumptions are recorded.
7. The intended conclusion path is defined before the run.

A prototype must not start merely because data are convenient or because a chart appears interesting.

## 5. Minimum prototype record

Before execution, the prototype artifact records:

- Hypothesis ID;
- Data Feasibility review reference;
- prototype sequence;
- created date;
- one prototype question;
- expected direction/form inherited from the Hypothesis;
- data source/snapshot reference sufficient for the stage;
- relevant Data Feasibility constraints;
- time period or observation scope;
- transformation/feature summary;
- minimal baseline definition;
- cost/execution approximation where economically relevant;
- planned output metrics;
- known limitations;
- stop/decision rule for the prototype.

After execution it records:

- implementation reference;
- result summary;
- primary metric/result values needed to answer the question;
- obvious anomalies or data-quality issues;
- interpretation limited to the prototype question;
- outcome decision and reason;
- follow-up, if any.

Unknown facts remain explicit unknowns. They are not replaced with invented values.

## 6. Minimum implementation principle

Prototype implementation should be the smallest implementation capable of answering the question honestly.

Acceptable examples include:

- one notebook;
- one Python/R script;
- one SQL/query workflow;
- a simple event study;
- a minimal baseline backtest;
- a small deterministic calculation.

Not required at R3:

- production architecture;
- shared Strategy SDK;
- broker integration;
- deployment system;
- monitoring/recovery;
- portfolio engine;
- generalized optimization framework;
- large parameter-search infrastructure.

If prototype work starts requiring these, stop and ask whether the research question can be answered more cheaply.

## 7. Baseline before optimization

The first prototype should prefer a simple baseline.

The purpose is to determine whether an effect exists without depending on fine tuning.

Default rules:

1. Do not begin with a large parameter grid.
2. Do not search many markets/instruments merely to find one winner unless cross-sectional search is itself the declared question.
3. Do not add filters sequentially until the result turns positive.
4. Do not select the best horizon after inspecting many horizons and present it as if it were preselected.
5. If multiple variants are necessary to understand the question, record how many were inspected and why.

A prototype that only becomes attractive after broad search has increased research risk and must carry that fact into later screening.

## 8. Data discipline

Prototype data must obey the completed Data Feasibility review.

The prototype records the actual source/snapshot used and any deviations from the review.

No prototype may silently:

- replace an unfavorable dataset with another source;
- change timestamp interpretation;
- use revised values instead of point-in-time values;
- switch to current constituents for historical universe claims;
- fill missing data in a way not declared in the review;
- alter the period because another interval looks better.

A material data change requires re-review of Data Feasibility before using the result to advance the research line.

## 9. Information-time and leakage controls

At minimum, prototype implementation must prevent obvious future information leakage identified by Hypothesis/Data Feasibility.

Examples include:

- future bars/features at signal time;
- revised macro data used before revision time;
- final event labels unavailable at event time;
- centered rolling windows;
- future universe membership;
- normalization using future observations;
- overlap that directly leaks target information into features.

R3 does not require the full later validation protocol, but known leakage is a blocking defect, not an acceptable prototype shortcut.

## 10. Cost and execution approximations

If the Hypothesis implies trading or an economically sensitive action, the prototype should include the simplest reasonable early cost approximation supported by Data Feasibility.

Depending on the question this may include:

- spread;
- commission;
- slippage proxy;
- financing;
- event/execution delay;
- contract/tick economics.

Exact live execution is not required.

The approximation must be explicit and conservative enough that a tiny gross effect is not presented as economically meaningful merely because costs were omitted.

If costs cannot yet be estimated, the prototype conclusion must remain gross-only and carry that limitation into Economic Pre-Screen.

## 11. Metrics

Prototype metrics are chosen to answer the one question, not to maximize dashboard size.

Possible metrics include:

- mean/median response;
- gross/net expectancy estimate;
- hit rate when relevant;
- effect size;
- event-window response;
- trade/opportunity count;
- distribution/quantiles;
- simple drawdown/path diagnostic;
- cost sensitivity at a few declared assumptions;
- concentration in time/instruments/events.

A prototype may show uncertainty or confidence intervals when useful, but R3 does not impose one universal significance threshold.

The result must expose enough context to avoid a single headline metric hiding obvious concentration or sample weakness.

## 12. Allowed exploratory freedom

Prototype is exploratory research, so limited iteration is allowed.

Allowed:

- fixing implementation bugs;
- checking data alignment;
- a small number of clearly documented sensitivity checks;
- comparing a simple baseline to one or a few pre-motivated alternatives;
- debugging assumptions from the Data Feasibility review.

Not allowed as a clean single prototype result:

- unrecorded broad parameter search;
- repeated reformulation until a positive result appears;
- hiding failed variants;
- moving the sample period after seeing results;
- changing the Hypothesis while keeping the same prototype identity;
- presenting the best exploratory run as if it were pre-registered evidence.

When exploratory freedom materially expands, record it and treat the result as weaker preliminary evidence.

## 13. Hypothesis change boundary

If prototype work reveals that the research claim itself should change materially, stop the current prototype line.

Material changes include changes to:

- Statement;
- Mechanism;
- Market/universe;
- Conditions;
- Horizon;
- expected Direction/form;
- decision-time information premise;
- Falsification rule.

The changed claim requires a new `HYP-xxxx` according to `HYPOTHESIS_MODEL.md`, followed by Data Feasibility for that new Hypothesis.

Do not rewrite the old Hypothesis to fit prototype output.

## 14. Prototype outcome model

### `ADVANCE_TO_ECONOMIC_SCREEN`

Meaning: the narrow prototype question produced enough preliminary signal or information to justify R4 Economic Pre-Screen.

This is not a statement that edge is proven or that the strategy is profitable.

### `ITERATE`

Meaning: another cheap prototype is justified without materially changing the Hypothesis.

Valid reasons include implementation correction, one pre-motivated sensitivity question or resolution of a non-material uncertainty.

Each iteration receives a new prototype sequence.

`ITERATE` must not become indefinite optimization. If the research line repeatedly needs new filters/parameters/questions to survive, that itself is negative evidence to carry forward.

### `PARK`

Meaning: the question remains potentially useful, but another external/data/resource condition currently makes the next cheap step low-value or impossible.

No active prototype work continues until the block changes.

### `REJECT`

Meaning: the prototype provides enough negative preliminary information to stop this research line before Economic Pre-Screen, or exposes a fatal defect in the current Hypothesis/data premise.

The prototype and rejection reason are retained.

## 15. Decision discipline

Prototype outcome should be based on the pre-written question and declared decision rule.

The decision rule at R3 can be qualitative or quantitative, but it must be understandable before the result is inspected.

Examples:

- advance only if the effect has the expected sign and is not concentrated in one obvious bad-data episode;
- reject if enforcing decision-time timestamps removes the claimed response;
- park if usable cost inputs cannot be obtained;
- iterate once if the only unresolved issue is one declared data-alignment ambiguity.

Do not retrofit a new decision rule after seeing an unattractive result and then present the run as if it passed the original rule.

## 16. Prototype versus formal Experiment

Cheap Prototype is exploratory/preliminary research.

It is not automatically a registered `Experiment` and must not be cited as registered research, validation evidence or independent evidence.

If a prototype result needs to become formal evidence later:

1. define the formal question/decision rule under the Experiment process;
2. register the `EXP-YYYYMMDD-nnn` manifest before observing that experiment result;
3. rerun under the registered context;
4. preserve the earlier prototype as exploratory history.

Do not retroactively assign an Experiment ID to a completed exploratory run and call it pre-registered evidence.

## 17. Negative history and search accounting

Prototype failures and unattractive variants are retained or referenced.

Record, where applicable:

- number of prototype iterations;
- number of variants/parameters inspected;
- markets/instruments inspected;
- data-source changes;
- hypothesis changes that forced a new ID;
- discarded variants.

This search history becomes an input to later validation strength and selection-bias assessment.

## 18. Decision authority

Routine prototype execution and outcome classification may be performed by RESEARCH under this protocol because no real market exposure is created.

OWNER approval is not required for `ADVANCE_TO_ECONOMIC_SCREEN`, `ITERATE`, `PARK` or `REJECT` at R3.

OWNER rights remain reserved for capital policy, Strategy Risk Mandate, live admission, allocation, scaling and profit withdrawal.

## 19. Structural acceptance test

`CHEAP_PROTOTYPE_TEMPLATE.md` is tested against this protocol without creating a fictitious Hypothesis, dataset, instrument or prototype result.

The template must represent:

- Hypothesis and Data Feasibility linkage;
- prototype sequence;
- one pre-written question;
- expected direction;
- data/scope/period;
- assumptions and constraints;
- baseline implementation;
- cost/execution approximation;
- planned metrics;
- known limitations;
- decision rule;
- implementation/output references;
- result summary;
- search/iteration accounting;
- one outcome and reason.

No market result, return, cost number or synthetic research finding is invented by this structural test.

## 20. Definition of Done for an individual Cheap Prototype

A real prototype iteration is complete when:

- parent Hypothesis and Data Feasibility review are identified;
- one research question was written before execution;
- data/timing/cost assumptions are recorded;
- implementation scope is minimal and traceable;
- result answers the declared question as far as available evidence permits;
- exploratory search/iterations are recorded;
- one outcome among `ADVANCE_TO_ECONOMIC_SCREEN / ITERATE / PARK / REJECT` is recorded with reason;
- no prototype output is mislabeled as formal validation evidence;
- negative history is retained.

## 21. M1-004 completion result

This protocol plus `CHEAP_PROTOTYPE_TEMPLATE.md` satisfies `WBS-1.4`.

Next dependent work:

`ATS2-M1-005 — Economic Pre-Screen`.

R4 must decide whether the preliminary effect is economically worth further research after considering magnitude, likely costs, opportunities, capital use, risk characteristics, capacity and operational complexity.