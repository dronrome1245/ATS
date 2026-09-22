# ATS Validation Framework

**Task:** `ATS2-M4-001`  
**Work package:** `WBS-4.1`  
**Status:** BASELINE  
**Purpose:** define how ATS tests a sufficiently fixed future Candidate/Strategy Version for robustness without turning validation into another parameter search.

## 1. Core rule

Validation tests a **fixed-enough system**.

It does not search for a new profitable system.

The central boundary is:

> Development may choose or change the system. Validation evaluates the chosen system under a predeclared protocol. Independent Examination evaluates a frozen version on a protected block that has not been used for tuning.

A favorable result does not upgrade evidence class by itself. Evidence strength follows the protocol that produced it.

## 2. Relationship to existing ATS methodology

This framework operationalizes the validation part of:

- `STRATEGY_LIFECYCLE_V2.md` — S06 Robustness & Validation and S07 Independent Examination;
- `EXPERIMENT_REGISTRATION.md` — pre-result registration boundary;
- `EVIDENCE_TAXONOMY.md` — `VALIDATION_EVIDENCE` and `INDEPENDENT_EXAMINATION_EVIDENCE`;
- `RESEARCH_REVIEW_PROTOCOL.md` — completeness, lineage, evidence-class and sufficiency review;
- `RESEARCH_REVIEW_CHECKS.md` — effective sample, dependence, concentration, uncertainty and research freedom;
- `MULTIPLE_RESEARCH_ACCOUNTING.md` — material research attempts, selection lineage, negative alternatives and consumed protected blocks.

This document does not weaken any prerequisite in those methodologies.

## 3. Scope

The framework applies to future research lines that have earned validation eligibility.

Strategy-specific S06 validation requires, at minimum:

1. a promoted Candidate / concrete Strategy Version or equivalently frozen decision logic;
2. the relevant research and economic history retained;
3. S05 Economic Viability `PASS`;
4. identified code/configuration/data/cost context;
5. a registered validation question and decision rule before validation results are observed.

Program-level M4 tooling may be built before such a Candidate exists.

The rejected `HYP-0001 / PROTO-01` line is **not eligible** for M4 strategy-specific validation and must not be reopened by this framework.

## 4. Three information zones

### 4.1 DEVELOPMENT

Purpose: formulate, debug and choose a Strategy Version.

Allowed:

- feature/rule development;
- parameter choice;
- implementation debugging;
- exploratory diagnostics;
- declared research iteration.

Results from data used directly for tuning are development information. They are not validation merely because they are out-of-sample from some earlier prototype.

### 4.2 VALIDATION

Purpose: test whether the fixed version survives predefined robustness checks.

Required:

- validation protocol fixed before result observation;
- registered Experiment(s);
- no direct tuning on validation data;
- explicit validation axes, metrics and decision criteria;
- preserved negative/failed evidence;
- sufficient data/timing/cost semantics for the registered question.

A registered Experiment qualifies as `VALIDATION_EVIDENCE` only when the Evidence Taxonomy prerequisites are satisfied.

### 4.3 INDEPENDENT_EXAMINATION

Purpose: one protected final historical/model examination of a frozen version.

Required:

- code, parameters, configuration, data block, costs and pass/fail rule frozen before reveal;
- protected block not used for tuning the applicable version/research line;
- immutable registered exam context;
- protected block used once for the applicable independent decision;
- decision only `PASS / FAIL`.

After reveal, the block is known and may not silently remain independent for a modified version.

## 5. Validation Profile

Before strategy-specific validation begins, the Candidate/Strategy Version must have a **Validation Profile**.

The profile is the binding strategy-class-specific selection from this framework. It records:

- target Candidate / Strategy Version;
- research class and main failure modes;
- development, validation and protected-independent data boundaries;
- primary validation questions;
- required validation axes;
- data/time/event unit of analysis;
- dependence/overlap treatment;
- parameter-neighbourhood definition where applicable;
- time/regime slicing rules;
- concentration/outlier checks;
- cost/execution sensitivity assumptions;
- resampling method when applicable;
- primary metrics;
- secondary diagnostics;
- pass/fail/return decision rule;
- registered Experiment package(s);
- search/multiple-research accounting;
- known limitations.

ATS defines **no universal Sharpe, trade-count, p-value, return or drawdown threshold** for every strategy class.

The profile must state thresholds/criteria appropriate to the concrete strategy before seeing validation results.

## 6. Mandatory validation dimensions

A Validation Profile must either include each dimension below or explicitly state why it is not applicable.

### V1 — Parameter neighbourhood

Question:

> Does the result survive a reasonable neighbourhood around the frozen configuration, or does it depend on one isolated point?

Rules:

- the neighbourhood/range is motivated and recorded before results;
- validation does not report only the best cell;
- the frozen configuration remains the evaluated version;
- a materially changed "better" configuration becomes new development work / a new Strategy Version and new validation context;
- parameter sensitivity output must make cliffs, sign changes and isolated optima visible.

### V2 — Time / regime slicing

Question:

> Is the result distributed across relevant time periods/regimes rather than concentrated in one convenient interval?

Rules:

- slicing logic is predeclared or based on information independent of validation outcomes;
- post-hoc discovered regimes are diagnostics and cannot retroactively become primary pass criteria;
- the report shows unfavorable slices as well as favorable ones;
- no period is silently removed because it hurts the result.

### V3 — Observation dependence

Question:

> How many genuinely separate pieces of evidence exist after accounting for overlap, clustering or serial/event dependence?

Rules:

- raw observation count is not automatically the effective sample size;
- overlapping forward windows, clustered events, repeated positions or correlated instruments must be identified;
- the Validation Profile declares the unit of independent opportunity or a defensible dependence-adjusted analysis;
- known dependence must not be treated as IID merely because an IID calculation is convenient;
- uncertainty claims must respect the dependence structure.

The M3 PROTO-01 result, where `71.8688%` of signal forward windows overlapped another signal window, is the concrete program lesson behind this requirement. That rejected result is an example of the issue, not validation evidence.

### V4 — Concentration / outliers

Question:

> Does the result depend on a small number of observations, events, dates, regimes or extreme outcomes?

The profile defines relevant concentration diagnostics, for example:

- contribution by top observations/trades/events;
- concentration by month/year/session/regime;
- contribution with/without declared extreme observations;
- event clustering or repeated exposure;
- drawdown/loss concentration.

Outliers are not silently deleted. Any exclusion rule must be data-quality or protocol-driven and fixed before the decision-relevant result.

### V5 — Cost / execution sensitivity

Question:

> Does the result survive plausible deterioration in economically relevant costs/execution assumptions?

As applicable, test declared ranges/scenarios for:

- spread;
- commission;
- slippage;
- latency/delay;
- financing/rollover;
- fill assumptions;
- market impact/capacity.

Sensitivity ranges must be justified independently of which values make the strategy pass.

Stress findings may qualify as `STRESS_EVIDENCE`; they do not substitute for independent examination.

### V6 — Resampling / path uncertainty

Use only when appropriate to the data-generating process and registered question.

Possible methods include:

- block bootstrap;
- clustered/event resampling;
- stationary/time-series resampling;
- Monte Carlo over explicitly modeled sequence/execution assumptions.

Rules:

- dependence that matters is preserved;
- IID bootstrap is used only when IID is defensible;
- block/cluster choices are declared before seeing the decision-relevant output;
- resampling is interpreted as uncertainty/sensitivity, not as false precision about future probabilities.

### V7 — Research freedom / multiple-research accounting

Validation Review must see the history that led to the version:

- material hypotheses/versions inspected;
- parameter/search families inspected;
- markets/instruments searched where relevant;
- failed/negative Experiments;
- discarded alternatives;
- data-source changes;
- prior returns to research.

A clean final chart does not erase earlier search freedom.

## 7. Registered validation package

Every decision-relevant validation run is a registered Experiment under `EXPERIMENT_REGISTRATION.md`.

Before result observation it records, as applicable:

- `research_stage: VALIDATION`;
- parent Hypothesis/Candidate/Strategy Version;
- code revision and implementation reference;
- Dataset ID/version and validation block;
- frozen parameters/configuration;
- cost/execution assumptions;
- dependence/overlap handling;
- primary question;
- primary metrics;
- secondary diagnostics;
- decision rule;
- expected `qualified_evidence_class` if all prerequisites are satisfied.

Registration is necessary but not sufficient for `VALIDATION_EVIDENCE`.

## 8. Validation decisions

S06 uses:

`PASS / FAIL / RETURN`

### PASS

Requires all of the following:

- registered primary criteria satisfied;
- no blocking integrity/lineage/data defect;
- required validation axes completed;
- evidence class qualifies as required;
- negative and contradictory evidence is included;
- result is not dependent on an undeclared post-hoc rescue.

PASS means the fixed version survived the registered validation protocol within its scope. It does not mean future profitability is guaranteed.

### FAIL

Use when a required validation criterion fails or the fixed version demonstrates unacceptable fragility under the registered protocol.

FAIL is retained as validation evidence when protocol prerequisites were satisfied.

### RETURN

Allowed only for a specific remediable issue whose correction does not reinterpret an unfavorable valid result.

RETURN must state:

- the exact defect/question;
- why it blocks the decision;
- allowed correction;
- whether a new Strategy Version or Experiment is required;
- stop condition.

A poor result is not an implementation defect. RETURN must not become rescue optimization.

## 9. Material-change boundary

After validation result observation, any material change to the trading logic, parameters, data definition, cost model or decision-relevant implementation creates a new research/Strategy Version context as required.

The old validation result remains attached to the old version.

Examples of material change:

- changing the signal/lookback/horizon;
- adding a filter because a validation slice failed;
- choosing a different parameter after seeing sensitivity output;
- changing the tested market/universe;
- switching validation period/source because the result was unattractive;
- weakening the pass rule after result observation.

Bug fixes that cannot affect the computed result may be documented without changing the research claim. Result-affecting fixes require a new registered run/context.

## 10. Independent Examination boundary

S07 is separate from S06.

Validation data may be inspected according to its registered protocol. The protected independent block may not be used to choose parameters, features, thresholds, filters or the validation profile.

The independent exam freezes:

- Strategy Version;
- code/configuration;
- parameters;
- protected dataset block;
- costs/execution assumptions;
- primary metrics;
- `PASS / FAIL` criteria.

There is no conditional pass.

A failed independent exam is not repaired on the same protected block and then re-described as independent evidence.

Detailed freeze/exam mechanics are implemented in `WBS-4.6`.

## 11. Evidence and Review

The final S06 Research Review must record:

- package completeness;
- lineage/current Strategy Version;
- all material Experiment IDs;
- `source_class`;
- `qualified_evidence_class`;
- effective independent opportunities;
- dependence/overlap limitations;
- concentration/outlier findings;
- time/regime findings;
- cost/execution sensitivity;
- research freedom/multiple testing;
- contradictory/negative evidence;
- final `PASS / FAIL / RETURN` and reason.

A favorable headline metric cannot override a blocking failure.

## 12. Tooling contract for M4

The framework intentionally separates rules from implementation.

### `WBS-4.2 — Parameter sensitivity tooling`

Must support predefined parameter neighbourhoods and report the full evaluated surface/region rather than only a winner.

### `WBS-4.3 — Time/regime slicing`

Must evaluate deterministic declared slices without selective reporting.

### `WBS-4.4 — Trade/observation concentration`

Must expose concentration and overlap rather than relying only on raw counts.

### `WBS-4.5 — Resampling framework`

Must support dependence-preserving methods where appropriate and make assumptions explicit.

### `WBS-4.6 — Independent exam protocol`

Must define protected-block freeze, one-shot reveal and immutable `PASS / FAIL`.

### `WBS-4.7 — Multiple-research accounting`

Must make material research attempts/search freedom visible to review.

### `WBS-4.8 — Class-specific profiles`

Must turn this general framework into explicit requirements for each strategy/data class that ATS actually needs.

Initial class profile:

`governance/methodology/TECHNICAL_STRATEGY_VALIDATION_PROFILE.md`

No tool may silently choose a validation method solely because it produces a better result.

## 13. Current M4 boundary

At completion of `ATS2-M4-001`:

- no promoted Candidate exists;
- no strategy-specific validation Experiment is created;
- `experiments/REGISTRY.csv` remains unchanged;
- HYP-0001 remains `REJECTED_AT_R3`;
- no validation result is invented;
- live/demo/capital permissions remain false.

The framework is infrastructure/methodology for future eligible Candidates.

## 14. Structural acceptance

This framework is structurally acceptable when a future agent can answer, before validation result observation:

1. What exact version is being validated?
2. What information was used for development?
3. What data are validation data?
4. What block is protected for independent examination?
5. What validation axes are mandatory for this strategy class?
6. How are overlapping/dependent observations treated?
7. What primary metrics and decision rule are fixed?
8. What search/multiple-research history must be disclosed?
9. What change requires a new version/Experiment?
10. What exact evidence class may the result support?

## 15. Completion and next work

`ATS2-M4-001 — Validation protocol framework` is complete when:

- this framework is committed;
- state/backlog/status/handoff/validator are synchronized;
- no fictitious Candidate or validation result is created;
- the exact final commit passes the full Local CI Gate.

Next work:

`ATS2-M4-002 — Parameter sensitivity tooling`

Work package:

`WBS-4.2`

Initial implementation target:

`src/ats/validation/sensitivity.py`
