# ATS Market Pattern Discovery

**Capability:** reusable exploratory discovery of candidate price-dynamics patterns  
**Status:** BASELINE  
**Purpose:** allow ATS to systematically search for candidate market patterns while preserving search history and preventing exploratory mining from being mislabeled as validated evidence.

## 1. Core rule

Market Pattern Discovery is **hypothesis generation**, not strategy validation.

Its output may create:

- an `EXPLORATORY_OBSERVATION`;
- a new Idea;
- a falsifiable Hypothesis worth entering the normal Research Funnel.

It must not directly create:

- a Candidate;
- a Strategy Version;
- `VALIDATION_EVIDENCE`;
- `INDEPENDENT_EXAMINATION_EVIDENCE`;
- a live/capital decision.

The canonical path is:

`bounded discovery → observation → Idea → Hypothesis → Data Feasibility → Cheap Prototype → Economic Screen → Candidate`

## 2. Why this capability exists

ATS must not depend only on manually invented trading ideas.

It should also be able to inspect market data for repeatable conditional behavior such as:

- continuation after an impulse or breakout state;
- reversal after an extreme move;
- volatility expansion/contraction effects;
- session/time-of-day effects;
- serial dependence;
- range/trend state transitions;
- conditional future-return distributions;
- other explicitly bounded price-dynamics questions.

The discovery process must remain reproducible and auditable because a large search space can manufacture attractive-looking accidents.

## 3. Discovery is exploratory evidence

Every discovery result has:

`qualified_evidence_class = EXPLORATORY_OBSERVATION`

unless a later, separately registered artifact earns a stronger class under the Evidence Taxonomy.

A positive discovery result does not become a preregistered experiment retroactively.

A negative discovery result remains part of the search history.

## 4. Search Manifest

Before a bounded discovery run begins, record a **Search Manifest**.

Minimum fields:

- discovery/search ID;
- Dataset ID/version and development-period scope;
- market/instrument/universe;
- timestamp semantics;
- pattern families;
- feature/condition families;
- horizons;
- directions;
- filters/regimes allowed in the search;
- parameter/value grids where applicable;
- primary descriptive/effect metrics;
- search budget / maximum combinations;
- ranking or shortlist rule, if any;
- random seed/protocol if stochastic;
- cost/execution applicability label;
- excluded protected validation/independent blocks;
- code revision and implementation reference.

The Search Manifest fixes what was searched. It does not preregister a hypothesis result.

## 5. Development-data boundary

Pattern Discovery uses development/exploratory information only.

Protected validation or independent-examination blocks must not be opened merely to discover a pattern or choose a promising formulation.

If a block is used for discovery, it is development-known for that research line and cannot later be called independent.

## 6. Search-space accounting

Every run must preserve the actual search space.

Record, as applicable:

- number of pattern families;
- number of markets/instruments;
- number of horizons;
- number of parameter combinations;
- number of filters/regimes;
- number of directional variants;
- number of metrics inspected;
- number of total evaluated alternatives;
- failed/negative alternatives;
- shortlisted alternatives.

The final report must not show only the best result without the denominator of how many alternatives were inspected.

This directly feeds `WBS-4.7 — Multiple-research accounting`.

## 7. Bounded search, not unlimited mining

A discovery run requires a finite search budget.

Bad:

> Search every possible transformation until something profitable appears.

Acceptable:

> Evaluate these declared pattern families, horizons and condition grids on this development dataset, retain every result, and shortlist according to this fixed exploratory rule.

If a new search family is invented after inspecting the run, that is a new Search Manifest/run.

## 8. No hidden rescue

After a result is seen:

- changing the horizon;
- adding a filter;
- changing the market;
- changing the direction;
- changing the ranking metric;
- changing the sample period;

creates additional search freedom and must be recorded as a new discovery attempt or manifest revision before the new result is treated as a distinct search.

The history is cumulative; failed variants are not erased.

## 9. Discovery metrics

Discovery metrics are descriptive/exploratory and strategy-class dependent.

Possible examples include:

- conditional mean/median future return;
- difference from unconditional baseline;
- positive-outcome share;
- volatility/range change;
- conditional distribution quantiles;
- event/opportunity count;
- dependence/overlap diagnostics;
- effect stability across broad development slices.

No one metric creates a universal PASS.

## 10. Dependence and overlap

Raw observation count is not automatically independent evidence.

Discovery reports should expose, where relevant:

- overlapping forward windows;
- clustered observations;
- repeated signals from one market episode;
- correlated instruments/events;
- effective-opportunity concerns.

This is especially important because M3 PROTO-01 showed that a large raw signal count can coexist with substantial window overlap.

## 11. Multiple testing and selection bias

Discovery is expected to inspect multiple alternatives.

Therefore:

- attractive findings are hypotheses to test, not proof;
- search count/history must remain visible;
- later validation must be stronger when search freedom was large;
- independent blocks remain protected;
- the same final block must not be repeatedly used to rescue discovered patterns.

Formal corrections, if needed, belong to the later Statistical Validation Profile; discovery itself must at least preserve the complete selection history.

## 12. Shortlist outcomes

A discovery run may assign exploratory outcomes such as:

- `NO_PATTERN_SHORTLISTED`;
- `SHORTLIST_FOR_IDEA_INTAKE`;
- `FOLLOW_UP_DISCOVERY_REQUIRED`.

These are workflow outcomes only.

They do not equal:

- `PROMOTE`;
- S05 `PASS`;
- S06 validation `PASS`;
- S07 independent-exam `PASS`.

## 13. Idea/Hypothesis conversion

A shortlisted pattern enters the standard ATS methodology only after a separate Idea/Hypothesis artifact states:

- the concrete statement;
- plausible mechanism/rationale;
- market/condition;
- horizon;
- expected direction;
- falsification condition;
- required data;
- known biases;
- link back to the discovery/search ID.

The discovery result itself remains exploratory history.

## 14. Reproducibility

A discovery run should be reproducible from:

`Search Manifest + code revision + Dataset identity + environment + seed/protocol → full result table + shortlist`

Full result tables may live outside Git if too large, but their immutable location/hash and summary counts must be recorded.

## 15. Anti-patterns

Forbidden representations:

- presenting the best of many searched variants as if it were one preselected hypothesis;
- hiding the number of alternatives searched;
- deleting failed variants;
- searching protected independent data;
- converting a discovery result directly into validation evidence;
- changing the shortlist rule after seeing results without recording a new attempt;
- using profitability alone as the discovery objective without explicit market-state/horizon semantics.

## 16. Program integration

This capability is introduced as:

`WBS-6.0 — Market Pattern Discovery`

It is intended to help source Reference Strategy #2 after the reusable validation infrastructure is built.

The program dependency is deliberately changed so Strategy #2 research can begin **before M5 execution engineering**.

Canonical bridge:

`M4.1–M4.8 reusable validation capability → WBS-6.0 discovery / Strategy #2 research → S05 PASS Candidate → M4.9/M4.10 validation + independent exam → M5 execution platform`

This prevents the rejected Strategy #1 line from creating a roadmap deadlock.

## 17. Current boundary

Creating this methodology does not run a market scan.

No new Idea, Hypothesis, Candidate, Strategy, Experiment or evidence result is created by this document.

HYP-0001 remains `REJECTED_AT_R3`.
