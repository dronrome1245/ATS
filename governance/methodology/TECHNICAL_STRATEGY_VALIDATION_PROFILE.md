# ATS Technical Strategy Validation Profile

**Task:** `ATS2-M4-008`  
**Work package:** `WBS-4.8`  
**Status:** BASELINE  
**Purpose:** turn the general V1–V7 Validation Framework into explicit validation requirements for price-driven technical trading strategies without inventing universal profitability, risk or sample-size thresholds.

## 1. Core rule

This profile applies to **price-driven technical strategies** whose decision logic is materially based on ordered market-price information such as bars, quotes, trades, returns, ranges, volatility states, technical transformations or deterministic combinations of those inputs.

It is a **class baseline**, not a strategy result.

A future Candidate/Strategy Version must instantiate this profile before decision-relevant S06 validation results are observed.

The information boundary is:

`DEVELOPMENT → VALIDATION → INDEPENDENT_EXAMINATION`

Development may select or change the system. Validation tests the fixed-enough system under a predeclared protocol. Independent Examination evaluates the frozen version on protected evidence under `INDEPENDENT_EXAM_PROTOCOL.md`.

ATS defines **no universal Sharpe, trade-count, p-value, return, drawdown, win-rate or profit-factor threshold** for this strategy class.

## 2. Scope

This profile is suitable when the core research claim is driven primarily by price/market-state information available at decision time.

Typical covered structures include, where the concrete strategy specifies them:

- breakout, trend, momentum or reversal rules;
- moving-window or state-transition rules;
- volatility/range conditions;
- session/time-of-day technical rules;
- price-derived filters;
- deterministic combinations of technical conditions;
- bar-, quote- or trade-driven entry/exit logic.

Additional class-specific requirements are needed when the core claim materially depends on information not covered here, for example external events/news, fundamental releases, alternative data, portfolio-level allocation logic or execution-only alpha.

A technical strategy may use statistical or machine-learning components only when the concrete Validation Profile instance declares the decision-time inputs, training/development boundary, parameter/search freedom and all additional failure modes. This baseline does not silently validate an undeclared model-selection process.

## 3. Eligibility

Strategy-specific use of this profile requires the prerequisites from `VALIDATION_FRAMEWORK.md`:

1. a promoted Candidate / concrete Strategy Version or equivalently frozen decision logic;
2. retained research/economic history;
3. S05 Economic Viability `PASS`;
4. identified code, configuration, data and cost context;
5. registered validation questions and decision rules before result observation.

The class profile itself may exist before an eligible Candidate.

The rejected `HYP-0001 / PROTO-01` line remains `REJECTED_AT_R3` and is not reopened by this profile.

## 4. Required strategy-specific profile instance

Before S06, the concrete Candidate/Strategy Version must record at least:

- Candidate ID / Strategy ID / Strategy Version;
- implementation/code revision;
- configuration and parameter set;
- market, instrument or declared universe;
- Dataset ID/version for every development, validation and protected block;
- exact chronological boundaries and timestamp semantics;
- bar/quote/trade construction and price basis;
- feature/lookback/warm-up semantics;
- signal decision time and information-availability rule;
- entry/exit/position-management logic relevant to the validation claim;
- cost and execution assumptions;
- unit of observation/opportunity/trade;
- known overlap/dependence structure;
- primary validation questions;
- primary metrics;
- secondary diagnostics;
- V1–V7 applicability and method;
- exact S06 decision rule;
- Research Freedom Summary reference;
- registered Experiment IDs/packages;
- protected independent-block identity and S07 freeze plan;
- known limitations.

Omission is not equivalent to `N/A`. A field or validation dimension is `N/A` only when the profile gives a concrete reason.

## 5. Data-zone contract

Every strategy-specific profile must define three non-overlapping information roles even when physical files overlap in storage.

### 5.1 DEVELOPMENT

Development data may be used to:

- invent or modify rules;
- choose parameters;
- inspect exploratory diagnostics;
- choose features/filters;
- perform bounded discovery;
- debug result-affecting logic.

Any information used to choose the final version is development-known for that research line.

### 5.2 VALIDATION

Validation data test the chosen version under the registered S06 protocol.

Required:

- validation boundaries fixed before decision-relevant result observation;
- no tuning on validation results;
- no removal of unfavorable periods/observations because they hurt the result;
- every decision-relevant validation run is a registered Experiment;
- negative/failed validation evidence remains attached to the version.

A rolling/anchored validation design is allowed only when its chronology, fitting/selection windows, evaluation windows and aggregation rule are predeclared.

### 5.3 INDEPENDENT_EXAMINATION

The protected block is governed by `INDEPENDENT_EXAM_PROTOCOL.md`.

Before reveal, freeze:

- Strategy Version;
- code/configuration;
- parameters;
- protected Dataset/block;
- costs/execution assumptions;
- primary metrics;
- binary `PASS / FAIL` criteria;
- runner/environment identity.

A revealed block is consumed for the applicable independent claim.

## 6. Chronology and leakage rules

Price-driven validation must preserve decision-time causality.

The concrete profile must declare:

- event/availability timestamp used by the strategy;
- ordering and tie-break rules;
- bar close/open semantics where bars are used;
- lookback/warm-up requirements;
- forward-return/trade outcome horizon;
- whether labels/outcomes cross split boundaries;
- overlap between adjacent observations/trades;
- any purge/embargo or boundary-assignment rule used to prevent information leakage.

Random row shuffling is not accepted as an independence claim for an ordered price process unless the profile gives a defensible reason and demonstrates that chronology/dependence relevant to the claim is preserved.

There is no universal split percentage, embargo width or minimum history length. The concrete values must follow from the strategy/data semantics and be fixed before decision-relevant results.

## 7. Data and market semantics

The concrete profile must make the tested market representation reproducible.

Declare, as applicable:

- market/instrument/universe identity;
- vendor/source and Dataset ID/version;
- coverage start/end;
- timezone/session/calendar rules;
- BID/ASK/MID/trade/settlement price basis;
- bar construction or quote/trade sampling rule;
- adjusted/unadjusted price treatment where applicable;
- corporate-action treatment where applicable;
- missing/gap/duplicate/out-of-order policy;
- transformation lineage;
- data-quality exclusions;
- survivorship/universe-selection semantics where applicable.

Changing these after observing validation output is a material research event unless the change is proven result-irrelevant.

## 8. V1 — Parameter neighbourhood

**Applicability:** REQUIRED when the strategy has any material configurable parameter, threshold, lookback, horizon, filter value or comparable degree of freedom.

`N/A` is allowed only for a genuinely parameterless decision rule or when the purported parameter cannot affect the validated behavior. The reason must be recorded.

Requirements:

- freeze the evaluated Strategy Version before the sensitivity run;
- predeclare the parameter family and neighbourhood/range;
- explain why the neighbourhood is relevant independently of which values look favorable;
- retain the full evaluated surface/region;
- report cliffs, sign changes and isolated favorable cells;
- do not replace the frozen configuration with the best validation cell.

Canonical capability:

`src/ats/validation/sensitivity.py`

A materially improved setting discovered during V1 is new development work and requires the appropriate new Strategy Version/Experiment context.

## 9. V2 — Time / regime slicing

**Applicability:** REQUIRED.

The profile must define deterministic slices relevant to the strategy and available without using validation outcomes to choose them.

Possible dimensions include, when justified:

- chronological periods;
- session/time-of-day;
- volatility/range state;
- trend/range state;
- market/universe grouping;
- other strategy-relevant regime labels whose construction is known before decision-relevant output.

Requirements:

- slicing rules are predeclared or independently defined;
- all declared slices are reported;
- unfavorable slices remain visible;
- post-hoc discovered regimes are diagnostics only unless a new development iteration is created.

Canonical capability:

`src/ats/validation/slicing.py`

## 10. V3 — Observation dependence

**Applicability:** REQUIRED.

Raw count is not automatically effective evidence.

The profile must identify the economically/statistically relevant unit, for example a trade, signal opportunity, non-overlapping event block or another defensible unit.

It must explicitly assess, as applicable:

- overlapping forward windows;
- repeated signals during one market episode;
- overlapping positions;
- serial dependence;
- clustered events;
- correlated instruments/universe members;
- repeated exposure to the same underlying move.

If an effective-sample or uncertainty statement is made, the method must respect the declared dependence structure.

Known dependence must not be treated as IID merely because an IID calculation is convenient.

## 11. V4 — Concentration / outliers

**Applicability:** REQUIRED.

The profile must predeclare concentration diagnostics that can reveal whether the result is dominated by a small part of the evidence.

At minimum, choose diagnostics relevant to the strategy from:

- top observation/trade/event contribution;
- contribution by date/month/year/session/regime;
- clustering of repeated exposure;
- extreme positive/negative outcomes;
- drawdown/loss concentration;
- market/instrument concentration for multi-asset strategies.

Canonical capability:

`src/ats/validation/concentration.py`

Outliers are retained unless a predeclared data-quality/protocol rule requires exclusion. A result-dependent exclusion is not a valid rescue.

## 12. V5 — Cost / execution sensitivity

**Applicability:** REQUIRED for a trading/economic viability claim.

The profile must define a baseline economic execution model and justified adverse scenarios for every material component, as applicable:

- spread;
- commission;
- slippage;
- financing/rollover;
- latency/delay;
- fill assumptions;
- market impact/capacity.

The deterioration range must be justified from available market/execution evidence or a clearly stated conservative scenario, not chosen because it preserves PASS.

The strategy-specific profile must state which components are `N/A` and why.

A favorable gross effect cannot substitute for required net-economic validation.

## 13. V6 — Resampling / path uncertainty

**Applicability:** CONDITIONAL.

Use V6 when a defensible resampling/path-uncertainty question exists for the strategy and data-generating process.

Requirements when used:

- define the resampled unit/block/cluster before decision-relevant output;
- preserve internal order/dependence that matters;
- state seed/method and aggregation;
- do not silently fall back to IID;
- interpret output as uncertainty/sensitivity within the model, not as a guaranteed future probability.

Canonical capability:

`src/ats/validation/resampling.py`

`N/A` is acceptable when no defensible resampling target exists or V6 would add false precision. The profile must record that rationale.

## 14. V7 — Research freedom / multiple-research accounting

**Applicability:** REQUIRED.

Before S06 decision and before S07 freeze, the reviewer receives the `Research Freedom Summary` defined in `MULTIPLE_RESEARCH_ACCOUNTING.md`.

The profile must disclose, as applicable:

- discovery searches;
- hypotheses/prototypes;
- Strategy Versions;
- parameter/feature/filter searches;
- markets/universes/horizons/directions inspected;
- material data changes;
- material cost/execution changes;
- validation attempts and returns to research;
- failed/rejected/parked outcomes;
- consumed protected blocks.

When search freedom is material, the concrete profile must predeclare how that history affects statistical interpretation. This may include formal selection-bias/multiple-testing treatment or a documented reason that a specific correction is not appropriate.

The treatment cannot be selected after seeing which method makes the strategy pass.

ATS imposes no universal numeric penalty solely from attempt count.

## 15. Primary metrics and decision rule

The concrete profile must choose strategy-relevant primary metrics before validation results.

For a price-driven trading strategy, the decision package must cover the economic claim rather than a single attractive headline statistic. As applicable, the registered metrics should expose:

- net economic effect under baseline costs;
- path/risk or adverse-outcome behavior;
- opportunity/trade frequency;
- cost contribution;
- concentration/dependence diagnostics required by V3/V4;
- class-specific robustness metrics required by V1/V2/V5/V6.

This profile does not prescribe numeric values.

S06 uses:

`PASS / FAIL / RETURN`

`PASS` requires every registered blocking criterion and every required validation dimension to be satisfied.

`FAIL` records a valid unfavorable validation outcome.

`RETURN` is only for a bounded remediable issue under the general Validation Framework. It is not permission to rescue a poor result.

S07 uses only:

`PASS / FAIL`

## 16. S06 freeze boundary

Before the first decision-relevant S06 result is observed, freeze or register:

- target Candidate/Strategy Version;
- exact code/configuration/parameters;
- validation Dataset/block identity;
- data-zone boundaries;
- cost/execution model;
- V1–V7 applicability/methods;
- primary metrics;
- decision rule;
- Experiment package(s);
- Research Freedom Summary reference;
- known limitations.

A post-result change to any decision-relevant item is handled under the material-change rule.

## 17. S07 freeze boundary

Before the protected block is revealed, additionally freeze the Independent Exam context required by `INDEPENDENT_EXAM_PROTOCOL.md`.

S07 cannot be used to choose:

- a better parameter;
- a new filter;
- a different market;
- a new cost assumption;
- a weaker criterion;
- a different validation profile.

If the protected result is revealed, the block is consumed even if the strategy later changes.

## 18. Material-change rule

After validation output is known, create a new research/Strategy Version context when a change can affect trades, measured effect, evidence interpretation or independence.

Examples include:

- changing lookback/horizon/threshold;
- adding/removing a filter after a weak slice;
- changing market/instrument/universe;
- changing data source/period/transformation;
- changing entry/exit/position logic;
- changing costs/execution assumptions;
- changing primary metric or threshold;
- changing overlap/dependence treatment.

The old result remains linked to the old version.

A mechanical change that provably cannot affect the result may remain engineering work, with evidence of equivalence retained.

## 19. Tooling/evidence contract

The technical profile uses existing ATS M4 capabilities rather than inventing a second validation stack:

- V1: `src/ats/validation/sensitivity.py`;
- V2: `src/ats/validation/slicing.py`;
- V3/V4 support: dependence declarations plus `src/ats/validation/concentration.py`;
- V6: `src/ats/validation/resampling.py`;
- S07: `governance/methodology/INDEPENDENT_EXAM_PROTOCOL.md`;
- V7: `governance/methodology/MULTIPLE_RESEARCH_ACCOUNTING.md`;
- every decision-relevant S06 run: registered Experiment under `EXPERIMENT_REGISTRATION.md`.

A tool output qualifies as evidence only when the surrounding protocol satisfies the Evidence Taxonomy.

## 20. Review output

The S06 review for a strategy using this profile must make it possible to reconstruct:

- exact validated version;
- exact data-zone boundaries;
- all required V1–V7 results or explicit allowed `N/A` rationales;
- dependence/effective-opportunity interpretation;
- cost/execution sensitivity;
- negative/contradictory evidence;
- Research Freedom Summary;
- registered Experiment lineage;
- final `PASS / FAIL / RETURN` with the registered reason.

A favorable aggregate result cannot override a blocking failure in a required dimension.

## 21. Structural acceptance test

This class profile is structurally acceptable when a future reviewer can answer before S06 result observation:

1. What exact Strategy Version is being validated?
2. What information was development-known?
3. What exact timestamps/data are validation-only?
4. What exact block remains protected for S07?
5. How are lookback/horizon boundary leakage and overlap handled?
6. Is V1 required, and what neighbourhood is frozen?
7. What V2 slices are predeclared?
8. What is the effective observation/opportunity unit for V3?
9. What concentration diagnostics are required by V4?
10. What baseline/adverse cost-execution scenarios are required by V5?
11. Is V6 applicable, and what dependence-preserving method is frozen?
12. What full research/search history is disclosed for V7?
13. What primary metrics and exact S06 rule are fixed?
14. What change forces a new version/Experiment?
15. What exact evidence class may each run support?

## 22. Current program boundary

This artifact creates reusable methodology only.

It does not create:

- a new Idea/Hypothesis;
- a Candidate;
- a Strategy Version;
- a validation Experiment;
- an S06 result;
- an S07 independent-exam result;
- any live/demo/capital permission.

`HYP-0001` remains `REJECTED_AT_R3`.

`WBS-4.9` and `WBS-4.10` remain blocked until a future promoted Candidate reaches S05 `PASS`.

After exact M4-008 closure, `WBS-6.0 — Market Pattern Discovery` may begin to source future research candidates while M5 remains blocked until S07 `PASS`.
