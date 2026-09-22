# ATS Multiple-Research Accounting

**Task:** `ATS2-M4-007`  
**Work package:** `WBS-4.7`  
**Status:** BASELINE  
**Purpose:** make material research freedom and selection history visible so a final result cannot be interpreted as if it were the only attempt ever considered.

## 1. Core rule

ATS preserves the **selection path**, not only the selected result.

A clean final Strategy Version, favorable validation report or shortlisted discovery pattern does not erase:

- prior hypotheses;
- rejected prototypes;
- parameter/search families;
- market/instrument searches;
- data-source/period changes;
- discarded alternatives;
- returns to research;
- failed validations;
- consumed independent blocks.

Multiple-research accounting is descriptive governance and evidence context.

It does **not** create a universal numeric penalty, p-value correction or automatic PASS/FAIL threshold.

## 2. Why this exists

Research can generate false confidence when many alternatives are tried and only the attractive result is shown.

ATS therefore distinguishes:

1. the result eventually selected;
2. the number and type of alternatives that could have been selected;
3. the sequence of changes made after observing earlier results;
4. which evidence blocks became known along the way.

The reviewer must see all four.

## 3. Unit of accounting

The canonical unit is a **Material Research Attempt**.

An attempt is material when it can reasonably affect:

- which hypothesis/strategy is selected;
- the measured effect;
- the interpretation of evidence strength;
- the decision rule;
- the apparent independence of later evidence.

Material attempts remain in history even when superseded, rejected, parked or abandoned.

## 4. Attempt types

Canonical attempt types include:

- `DISCOVERY_SEARCH`;
- `IDEA`;
- `HYPOTHESIS`;
- `CHEAP_PROTOTYPE`;
- `PARAMETER_SEARCH`;
- `FEATURE_OR_FILTER_SEARCH`;
- `MARKET_OR_UNIVERSE_SEARCH`;
- `HORIZON_OR_DIRECTION_SEARCH`;
- `DATA_SOURCE_OR_PERIOD_CHANGE`;
- `COST_OR_EXECUTION_CHANGE`;
- `STRATEGY_VERSION`;
- `REGISTERED_EXPERIMENT`;
- `VALIDATION_ATTEMPT`;
- `RETURN_TO_RESEARCH`;
- `INDEPENDENT_EXAM`;
- `PROTECTED_BLOCK_REVEAL`.

New types may be added when a genuinely distinct source of selection freedom appears.

## 5. Minimum Attempt Record

Each material attempt records, as applicable:

- stable `attempt_id`;
- research-line / lineage identifier;
- attempt type;
- sequence/order;
- parent/prior attempt reference(s);
- Idea/Hypothesis/Candidate/Strategy Version IDs;
- Search/Experiment/Exam IDs;
- code revision / implementation reference;
- Dataset ID/version and period/block;
- market/instrument/universe;
- parameter/feature/filter family;
- horizon/direction;
- costs/execution assumptions when materially changed;
- primary question/metric/decision rule when applicable;
- alternatives evaluated count;
- alternatives shortlisted count;
- outcome/decision;
- evidence class;
- status: active/superseded/rejected/parked/failed/consumed;
- result/artifact references;
- whether decision-relevant results were observed before the next attempt;
- material change rationale;
- protected-block status;
- known limitations.

Not-applicable fields remain explicit where needed to avoid ambiguous omissions.

## 6. Search-space accounting

A bounded search may use one attempt record plus a search summary rather than one record per parameter cell.

The summary must preserve the real denominator, including where applicable:

- pattern families;
- parameter combinations;
- features/filters;
- horizons;
- directions;
- markets/instruments;
- regimes;
- metrics inspected;
- total alternatives evaluated;
- negative/failed alternatives;
- shortlisted alternatives.

Reporting only the best alternative is insufficient.

`MARKET_PATTERN_DISCOVERY.md` Search Manifests feed this accounting directly.

## 7. What counts as a new attempt

Create a new material attempt when, after decision-relevant information is known, research changes something that could affect selection or result interpretation.

Examples:

- changing signal logic;
- adding/removing a filter;
- changing lookback or horizon;
- changing direction;
- changing market/universe;
- changing dataset/source/period because of results;
- changing costs/execution assumptions;
- changing primary metric or decision threshold;
- creating a materially changed Strategy Version;
- returning from validation to development;
- running another bounded discovery search;
- opening another protected block.

The history is cumulative.

## 8. What does not need a new research attempt

Purely mechanical work need not inflate research-attempt counts when it cannot affect the research result or selection decision.

Examples:

- formatting-only code changes;
- documentation typo corrections;
- environment/bootstrap repair before any decision-relevant output;
- exact deterministic rerun after a technical failure when inputs/rules are unchanged and no new result-dependent decision is made;
- report rendering repair that reproduces the same frozen computation.

These events may belong in engineering/CI audit trails instead.

## 9. Technical reruns versus research iteration

A rerun is not automatically a new research attempt.

### Same attempt

Keep the same attempt when:

- research inputs/rules are unchanged;
- the rerun is required for technical reproducibility;
- no tuning occurs because of the prior failed execution;
- evidence semantics remain identical.

### New attempt

Create a new attempt when the previous result influences a material change.

A sequence of “small fixes” that collectively changes strategy behavior is research iteration, not merely technical repair.

## 10. Outcome retention

Negative and discarded outcomes remain visible.

Allowed statuses include:

- `ADVANCED`;
- `REJECTED`;
- `PARKED`;
- `SUPERSEDED`;
- `FAILED_CRITERION`;
- `RETURNED_TO_RESEARCH`;
- `NO_PATTERN_SHORTLISTED`;
- `CONSUMED_PROTECTED_BLOCK`.

A later successful version never deletes prior statuses.

## 11. Lineage

Every selected Candidate/Strategy Version must be traceable backward through material parents to the research that created it.

The lineage should make it possible to answer:

- Which discovery/Idea created this hypothesis?
- Which hypotheses were discarded before this one?
- How many material parameter/search alternatives were examined?
- Which data periods/sources were already known?
- Which validation attempts failed or returned to research?
- Which protected blocks were revealed?
- What changed between versions?

Missing lineage is a validation-governance defect.

## 12. Consumed protected blocks

Any independent block reaching `REVEALED` under `INDEPENDENT_EXAM_PROTOCOL.md` is recorded as consumed.

Accounting records:

- exam/block identity;
- Strategy Version exposed;
- reveal status/date/event;
- PASS/FAIL/integrity outcome;
- whether later development used knowledge from the reveal.

A revealed block cannot disappear from history when a later Strategy Version is created.

## 13. Returns to research

Every S06 `RETURN` or other decision-relevant return from a stronger evidence stage to development is a material event.

Record:

- trigger;
- evidence observed before return;
- allowed remediation;
- resulting Strategy Version/attempt;
- which validation/independent blocks became known;
- whether new protected evidence is required.

A return is not a reset of research freedom.

## 14. Data changes

Changing data can create hidden selection freedom.

Material data changes include:

- vendor/source;
- time coverage;
- instrument/universe;
- missing/gap policy;
- transformation logic;
- timestamp semantics;
- quality exclusion rules.

If a change is made after observing an unattractive result, the old result and old data context remain linked in the accounting record.

## 15. Cost/execution changes

Research accounting also records material changes to:

- spread;
- commission;
- financing;
- slippage;
- latency;
- fill model;
- capacity/impact;
- execution timing.

A result is not treated as one continuous attempt if economics are repeatedly changed in response to results without recording those changes.

## 16. Required review summary

Before Candidate promotion, S06 validation decision and S07 independent exam, the reviewer receives a **Research Freedom Summary** containing at least:

- material attempts total;
- discovery searches total;
- hypotheses total;
- prototypes total;
- strategy versions total;
- parameter/feature/search families total;
- alternatives evaluated where known;
- markets/instruments searched;
- material data changes;
- material cost/execution changes;
- failed/rejected/parked attempts;
- validation attempts and returns;
- independent exams;
- consumed protected blocks;
- known missing historical accounting.

Counts must be accompanied by lineage references; a single scalar “research count” is not enough.

## 17. Decision use

Accounting informs how much confidence can reasonably be assigned to later evidence.

More search freedom can justify:

- stronger protected validation;
- more independent evidence;
- more conservative interpretation;
- formal multiple-testing/selection-bias methods where appropriate.

However ATS does not define a universal rule such as:

> N attempts automatically means FAIL.

The applicable statistical treatment belongs to the future class-specific Validation Profile.

## 18. Relationship to Experiment Registry

`experiments/REGISTRY.csv` remains the registry for formal Experiments.

Multiple-research accounting is broader.

It also covers material work that may not be a registered Experiment, such as:

- exploratory discovery searches;
- manual hypothesis changes;
- discarded variants;
- returns to research;
- consumed independent blocks.

Formal Experiments should be linked rather than duplicated.

## 19. Relationship to Market Pattern Discovery

Every bounded Search Manifest contributes:

- one `DISCOVERY_SEARCH` attempt;
- its full evaluated-alternative counts;
- shortlist outcome;
- links to any resulting Idea/Hypothesis.

If a follow-up search changes the family/grid/ranking rule after seeing results, it is a new attempt.

This prevents discovery from becoming invisible search freedom.

## 20. Current historical baseline

Existing ATS history already demonstrates why the accounting layer matters:

- `IDEA-0001 / HYP-0001 / PROTO-01` is retained as a rejected research line;
- HYP-0001 remains `REJECTED_AT_R3`;
- its rejection cannot be erased by later Strategy #2 success;
- no Candidate, validation attempt or independent exam currently exists;
- the first bounded Market Pattern Discovery search has not started.

This document defines future accounting; it does not invent missing past experiments.

## 21. Structural acceptance

This accounting model is acceptable when a future reviewer can answer:

1. How many material research attempts led to this version?
2. What kinds of attempts were they?
3. How many alternatives were evaluated in bounded searches?
4. What negative/discarded results existed?
5. What changed after each observed result?
6. Which datasets/markets were already inspected?
7. Which validation returns occurred?
8. Which protected blocks were consumed?
9. Can the selected version be traced to its material ancestors?
10. What accounting gaps remain?

## 22. Current boundary

This is governance/methodology infrastructure.

No new trading research is run.

No Candidate, Strategy Version, Experiment, validation result or independent exam is created.

HYP-0001 remains `REJECTED_AT_R3`.
