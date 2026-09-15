# ATS Evidence Taxonomy

**Task:** `ATS2-M1-009`  
**Work package:** `WBS-1.9`  
**Status:** BASELINE  
**Purpose:** make evidence classification operational by binding each evidence class to its provenance, prerequisites, permitted claims, prohibited claims and lifecycle decisions.

## 1. Core rule

ATS does not classify evidence by whether the result is attractive.

Evidence class is determined by **how the evidence was produced and what protocol constraints were satisfied**, not by whether P&L, return, drawdown or any other metric looks good.

A negative independent examination remains `INDEPENDENT_EXAMINATION_EVIDENCE`. A positive Cheap Prototype remains `EXPLORATORY_PROTOTYPE`.

Therefore:

> result direction changes the conclusion; protocol quality changes the evidence class.

No artifact may be upgraded to a stronger class solely because its result is favorable.

## 2. Two-axis model: source class and qualified evidence class

ATS separates two concepts that must not be conflated.

### 2.1 `source_class`

`source_class` describes the structural origin of the artifact and is immutable for that artifact.

Examples:

- `EXPLORATORY_OBSERVATION`;
- `EXPLORATORY_PROTOTYPE`;
- `REGISTERED_EXPERIMENT`;
- `DEMO_SHADOW_EVIDENCE`;
- `MINIMAL_LIVE_EVIDENCE`;
- `ACTIVE_LIVE_EVIDENCE`.

For formal `EXP-...` objects the manifest source class remains `REGISTERED_EXPERIMENT` because preregistration is a property of origin/provenance.

### 2.2 `qualified_evidence_class`

`qualified_evidence_class` expresses the strongest claim class the artifact is currently allowed to support after checking the relevant protocol prerequisites.

Canonical values:

- `EXPLORATORY_OBSERVATION`;
- `EXPLORATORY_PROTOTYPE`;
- `REGISTERED_EXPERIMENT`;
- `VALIDATION_EVIDENCE`;
- `INDEPENDENT_EXAMINATION_EVIDENCE`;
- `STRESS_EVIDENCE`;
- `DEMO_SHADOW_EVIDENCE`;
- `MINIMAL_LIVE_EVIDENCE`;
- `ACTIVE_LIVE_EVIDENCE`;
- `PORTFOLIO_EVIDENCE`;
- `SCALING_EVIDENCE`.

A registered Experiment may have:

- `source_class = REGISTERED_EXPERIMENT`;
- `research_stage = VALIDATION`;
- `qualified_evidence_class = VALIDATION_EVIDENCE` only after the validation prerequisites in this taxonomy are actually satisfied.

`research_stage = VALIDATION` alone does **not** make an Experiment validation evidence.

## 3. Evidence hierarchy is not a universal numeric ladder

The taxonomy has an approximate progression of evidentiary strength:

`Exploratory → Registered Research → Validation → Independent Examination → Demo/Shadow → Minimal Live → Active Live → Scaling/Portfolio evidence`

But different classes answer different questions.

For example:

- `INDEPENDENT_EXAMINATION_EVIDENCE` is stronger than demo evidence for historical/model generalization;
- `DEMO_SHADOW_EVIDENCE` is stronger than backtest evidence for production implementation behavior;
- `MINIMAL_LIVE_EVIDENCE` is stronger than demo evidence for actual fills/costs under observed live conditions;
- `STRESS_EVIDENCE` answers sensitivity/tail questions and does not replace independent evidence.

No single score converts all evidence classes into one number.

## 4. Canonical class matrix

| Qualified evidence class | Main question answered | May support | Must not be used to claim |
|---|---|---|---|
| `EXPLORATORY_OBSERVATION` | Is there an observation worth formulating? | Idea/Hypothesis generation | edge exists; economics work; validation; live readiness |
| `EXPLORATORY_PROTOTYPE` | Is there a preliminary effect worth more research? | R4 Economic Pre-Screen; bounded Candidate-review input | validated/stable edge; formal statistical proof; live execution; profitability proof |
| `REGISTERED_EXPERIMENT` | What happened under a preregistered research context? | exact registered question; baseline research decisions | validation merely because it was registered; independence; live proof |
| `VALIDATION_EVIDENCE` | Does a sufficiently fixed Strategy Version survive the registered validation protocol? | S06 robustness/validation decisions; evidence of out-of-development stability | independent/final confirmation; live execution quality; guaranteed future profitability |
| `INDEPENDENT_EXAMINATION_EVIDENCE` | Does the frozen version pass the protected independent exam? | S07 `PASS/FAIL`; strongest protected historical/model confirmation for that version | live fills/costs; permanent edge; future-profit guarantee; reuse of revealed block as independent |
| `STRESS_EVIDENCE` | How does the system behave under defined deterioration/scenarios/resampling? | sensitivity, tail, sequence, operational resilience and S08 readiness analysis | probability of exact future loss unless justified; live execution proof; standalone profitability proof |
| `DEMO_SHADOW_EVIDENCE` | Does production-like implementation behave correctly in real infrastructure without meaningful financial exposure? | S09 operational acceptance; runtime-vs-expected decision alignment; recovery/reconciliation evidence | profitability; true live slippage/cost profile at financial exposure; scalable capacity |
| `MINIMAL_LIVE_EVIDENCE` | How does the system execute with real but minimal financial exposure? | S10 execution/fill/cost/reconciliation decisions under observed conditions | long-run profitability; broad regime robustness; unlimited scaling; portfolio usefulness by itself |
| `ACTIVE_LIVE_EVIDENCE` | How is the admitted Strategy Version actually behaving at current allocation? | continue/reduce/pause/revalidate decisions; realized execution and performance monitoring | unlimited future scaling; evidence for materially different version; guaranteed persistence of edge |
| `PORTFOLIO_EVIDENCE` | What does the strategy contribute inside the current portfolio? | S11 admission/allocation context, correlation/exposure/marginal contribution | standalone edge proof; unrelated portfolio regimes; strategy-level validation replacement |
| `SCALING_EVIDENCE` | Does new live evidence justify the next controlled allocation step? | one incremental `INCREASE/HOLD/REDUCE/PAUSE` decision | arbitrary future scale; skipping intermediate live evidence; capacity beyond observed/analysed range |

## 5. `EXPLORATORY_OBSERVATION`

### Definition

An observation, chart pattern, descriptive statistic, qualitative market mechanism, ad-hoc query or other unregistered finding used to generate an Idea or Hypothesis.

### Allowed claims

- an observation exists in the inspected material;
- the observation suggests a possible mechanism worth formulating;
- a specific Hypothesis may be worth a bounded test.

### Prohibited claims

- persistent edge exists;
- expected profitability has been established;
- the finding survived costs, validation or independent examination;
- the finding supports live capital.

### Promotion prerequisite

It does not get relabelled. A stronger claim requires a new artifact produced under the stronger protocol.

## 6. `EXPLORATORY_PROTOTYPE`

### Definition

A Cheap Prototype produced under `CHEAP_PROTOTYPE_PROTOCOL.md` to answer one early quantitative question at low cost.

### Allowed claims

- under the stated prototype assumptions, the preliminary effect had the observed direction/magnitude;
- the research line deserves `ADVANCE_TO_ECONOMIC_SCREEN`, `ITERATE`, `PARK` or `REJECT` according to the prototype rule;
- the artifact is valid preliminary input to Economic Pre-Screen/Candidate review with its limitations visible.

### Prohibited claims

- formal validation;
- preregistered evidence if the prototype was not registered beforehand;
- proof of profitability;
- independent evidence;
- live execution evidence.

### Promotion prerequisite

The prototype itself remains `EXPLORATORY_PROTOTYPE`. If the finding needs formal evidence, register a new `EXP-...` before rerunning the corresponding question.

## 7. `REGISTERED_EXPERIMENT`

### Definition

A formal Experiment satisfying `EXPERIMENT_REGISTRATION.md`: the decision-relevant manifest was `REGISTERED` and committed before corresponding result observation.

### Allowed claims

- the predeclared question was tested under the recorded code/data/config/cost/decision context;
- the observed result may be used as formal registered research evidence for the scope actually tested;
- negative/failed results count as evidence and remain in the Experiment Registry.

### Prohibited claims

Registration alone does not prove:

- robustness;
- validation;
- independence;
- economic usefulness;
- live execution;
- future profitability.

### Qualification rule

`REGISTERED_EXPERIMENT` is the base formal source class. It may later qualify as `VALIDATION_EVIDENCE`, `INDEPENDENT_EXAMINATION_EVIDENCE` or `STRESS_EVIDENCE` only when the relevant additional protocol prerequisites below are satisfied. The manifest source class is not rewritten.

## 8. `VALIDATION_EVIDENCE`

### Required prerequisites

All applicable conditions must hold:

1. A concrete Strategy Version or equivalently frozen decision logic is identified.
2. The material rules being tested were fixed before the validation result.
3. The Experiment was preregistered.
4. Validation data/blocks were not used for direct tuning of the decisions being evaluated.
5. Data provenance, timestamps, costs and execution assumptions are sufficient for the registered question.
6. The validation protocol defines relevant robustness/holdout logic and decision criteria before result observation.
7. Material result-affecting changes create a new Strategy Version/Experiment as required.
8. The run is reproducible enough for review and material defects are disclosed.

### Allowed claims

- the fixed version passed/failed the specified validation checks;
- the observed effect is or is not robust across the registered validation axes/blocks;
- S06 decisions may rely on the evidence within its stated scope.

### Prohibited claims

- independent final confirmation unless the protected independent protocol was used;
- real execution quality;
- production readiness;
- guaranteed future profitability.

## 9. `INDEPENDENT_EXAMINATION_EVIDENCE`

### Required prerequisites

1. Strategy Version, code/configuration, parameters, dataset block, costs and pass/fail rule were frozen before reveal.
2. The independent block was protected from tuning for this Strategy Version/research line as required by protocol.
3. The exam was preregistered with an immutable exam context.
4. The protected block is used once for the applicable independent decision.
5. Decision is `PASS` or `FAIL`; no post-result conditional pass.
6. After reveal, the block is marked known and cannot silently remain independent for a modified version.

### Allowed claims

- the frozen version passed or failed the specified independent examination;
- the result is independent historical/model evidence within the protected block and protocol scope.

### Prohibited claims

- future profit is guaranteed;
- live fills/costs match the model;
- the revealed block remains independent after tuning on it;
- a materially changed version inherits the exam automatically.

## 10. `STRESS_EVIDENCE`

### Definition

Evidence from predefined adverse scenarios, perturbations, execution degradation, resampling, Monte Carlo/block bootstrap or operational failure scenarios appropriate to the strategy/data-generating process.

### Required prerequisites

- stress question/scenario is explicit;
- assumptions and perturbation mechanics are recorded;
- dependencies that matter are preserved rather than destroyed by naive resampling;
- outputs are interpreted as sensitivity/plausible scenario behavior, not false precision.

### Allowed claims

- the system is sensitive/resilient to the registered deterioration within the tested range;
- tail/sequence/operational vulnerabilities were observed or bounded under the modeled scenarios;
- stress findings may support S08 readiness and risk design.

### Prohibited claims

- exact probability of a future loss unless independently justified;
- actual broker/fill behavior;
- standalone evidence of persistent profitability.

## 11. `DEMO_SHADOW_EVIDENCE`

### Required prerequisites

- production-like Strategy Version/runtime is identified;
- live market/infrastructure path is exercised without meaningful financial exposure;
- clocks/data/connectivity/state/recovery/reconciliation/duplicate prevention are observable;
- expected decision ↔ runtime decision comparison is available where applicable.

### Allowed claims

- implementation behaves correctly/incorrectly in the observed production-like environment;
- runtime decisions, state recovery, monitoring and reconciliation satisfy/fail the S09 protocol;
- infrastructure issues are exposed before meaningful financial risk.

### Prohibited claims

- profitability proof;
- complete live cost/slippage proof;
- capacity/scaling proof;
- replacement for validation/independent examination.

## 12. `MINIMAL_LIVE_EVIDENCE`

### Required prerequisites

This class is future-facing and does not grant permission by existing as taxonomy.

Before it can exist:

- OWNER live admission is approved;
- Strategy Risk Mandate is approved;
- deployment/risk/reconciliation/emergency controls required by S08/S09 are operational;
- actual exposure is intentionally minimal and auditable;
- fills/costs/runtime decisions are reconciled against model expectations.

### Allowed claims

- actual execution/fill/cost/runtime behavior under the observed minimal-live conditions;
- model ↔ expected execution ↔ actual execution divergences;
- S10 `PASS/PAUSE/FAIL/RETURN_TO_S08` evidence.

### Prohibited claims

- long-run profitability from a short/minimal sample;
- scalability beyond tested conditions;
- portfolio benefit without portfolio analysis;
- permission to increase allocation automatically.

## 13. `ACTIVE_LIVE_EVIDENCE`

### Definition

Evidence accumulated from an admitted Strategy Version operating with a controlled active allocation.

### Allowed claims

- realized performance/execution/risk behavior for that version, allocation and observed environment;
- evidence for `CONTINUE/REDUCE/PAUSE/REVALIDATE/RETIRE` or equivalent health decisions;
- observed execution degradation, cost drift, regime behavior and edge drift.

### Prohibited claims

- unlimited persistence of edge;
- unlimited capacity;
- inheritance by a materially changed Strategy Version;
- automatic scaling without new evidence.

## 14. `PORTFOLIO_EVIDENCE`

### Definition

Evidence about the strategy's interaction with the actual/current portfolio: correlation, exposure overlap, risk contribution, capital competition, diversification and marginal contribution.

### Allowed claims

- portfolio admission/allocation usefulness within the analysed portfolio context;
- concentration/correlation/interaction observations relevant to S11/M7.

### Prohibited claims

- standalone edge proof;
- replacement for strategy validation;
- universal portfolio usefulness across materially different portfolio compositions.

## 15. `SCALING_EVIDENCE`

### Definition

New live evidence collected after a specific allocation level, used to decide the next controlled allocation step.

### Allowed claims

- whether observed behavior at the current step supports `INCREASE/HOLD/REDUCE/PAUSE` for the next defined step;
- observed capacity/execution degradation at or near tested scale.

### Prohibited claims

- arbitrary future scaling;
- skipping evidence blocks between materially different allocation levels;
- using old backtest evidence as the sole scaling basis.

## 16. Negative evidence and class retention

Evidence class is independent from result favorability.

Examples:

- failed registered experiment → still `REGISTERED_EXPERIMENT`;
- failed validation → still `VALIDATION_EVIDENCE` with outcome `FAIL`;
- failed independent exam → still `INDEPENDENT_EXAMINATION_EVIDENCE` with outcome `FAIL`;
- demo defect → still `DEMO_SHADOW_EVIDENCE` showing failure;
- adverse minimal-live execution → still `MINIMAL_LIVE_EVIDENCE`.

Negative evidence must remain discoverable and linked to the same Strategy/Hypothesis/Experiment context.

Deleting or downgrading negative evidence because it is inconvenient is prohibited.

## 17. No automatic inheritance across Strategy Versions

Evidence belongs to the exact context it tested.

Material Strategy Version change does not automatically inherit validation, independent, stress, demo or live evidence.

Review must determine which evidence remains relevant, which becomes historical context and which stages must be repeated.

Minor non-trade-affecting changes may retain evidence only when documented change control shows they cannot affect the claims being relied upon.

## 18. Qualification is protocol-based, not result-based

To assign a stronger `qualified_evidence_class`, the reviewer checks prerequisites.

A favorable result with unmet prerequisites remains at its lower class.

A negative result with fully met prerequisites receives the stronger class and a negative outcome.

Examples:

- positive registered backtest on a tuned development period → `REGISTERED_EXPERIMENT`, not `VALIDATION_EVIDENCE`;
- negative held-out validation under a frozen protocol → `VALIDATION_EVIDENCE` with `FAIL`;
- positive demo/shadow execution → `DEMO_SHADOW_EVIDENCE`, not profitability proof;
- positive minimal-live fills → `MINIMAL_LIVE_EVIDENCE`, not `SCALING_EVIDENCE`.

## 19. Evidence classification record

Any Evidence Index entry relied upon for a material decision should record at minimum:

- artifact/reference;
- Strategy/Hypothesis/Experiment linkage;
- `source_class`;
- `qualified_evidence_class`;
- research/lifecycle stage;
- result/outcome polarity when applicable;
- claim supported;
- claims explicitly not supported;
- key limitations;
- qualification basis/reviewer;
- status (`CURRENT / SUPERSEDED / INVALIDATED / HISTORICAL` as applicable).

The classification record summarizes claim eligibility; it does not replace the underlying Experiment/report/log.

## 20. Relationship to Experiment Registry

`experiments/REGISTRY.csv` remains the canonical searchable index of formal Experiment identities.

For registered Experiments:

- `evidence_class` records the immutable source/provenance class, normally `REGISTERED_EXPERIMENT`;
- `research_stage` records intended stage;
- `qualified_evidence_class` records the strongest reviewed claim class when one has been assigned.

Important:

`research_stage = VALIDATION` with blank or base `qualified_evidence_class` does not mean the experiment passed validation qualification.

Registry remains an index. Qualification details belong in the applicable Evidence Index/review and underlying package.

## 21. Relationship to Candidate Evidence Index

Candidate Evidence Index may contain mostly preliminary material.

It must distinguish:

- exploratory artifacts;
- registered Experiments;
- qualified evidence class, if any;
- negative/discarded research history;
- what each artifact may and may not claim.

Candidate promotion never upgrades evidence class by itself.

## 22. Relationship to Strategy Version Evidence Index

Strategy Version Evidence Index is the canonical view of which evidence classes currently support that exact version.

It must not merely list reports; it must make visible:

- source class;
- qualified class;
- result/status;
- claim supported;
- important limitations;
- whether the evidence is current, superseded or invalidated by material change.

Independent blocks already revealed are explicitly marked as no longer protected/independent for subsequent tuning.

## 23. Evidence and decisions

Evidence class constrains which decision it may support.

Typical mapping:

- Idea/Hypothesis decisions: exploratory evidence is sufficient.
- Economic Pre-Screen/Candidate review: exploratory + registered preliminary evidence may be sufficient, with limitations.
- S05 Economic Viability: registered research evidence and economic analysis are required; later validation classes are not yet assumed.
- S06 Validation decision: `VALIDATION_EVIDENCE` required.
- S07 Independent Examination: `INDEPENDENT_EXAMINATION_EVIDENCE` required.
- S08 risk/live readiness: prior validation/independent evidence plus `STRESS_EVIDENCE` and production-readiness artifacts.
- S09 Demo/Shadow acceptance: `DEMO_SHADOW_EVIDENCE` required.
- S10 Minimal Live decision: `MINIMAL_LIVE_EVIDENCE` required.
- S11 Active/Portfolio admission: live + `PORTFOLIO_EVIDENCE` as applicable.
- S12 Controlled Scaling: new `SCALING_EVIDENCE` required for each material step.

A stronger-looking result from a weaker class cannot substitute for a required class.

## 24. Safety and authorization boundary

This taxonomy classifies evidence. It does not authorize actions.

In particular, defining `DEMO_SHADOW_EVIDENCE`, `MINIMAL_LIVE_EVIDENCE`, `ACTIVE_LIVE_EVIDENCE` or `SCALING_EVIDENCE` does not change current program safety flags.

OWNER decisions remain required for program capital policy, Strategy Risk Mandate, live admission, allocation, scaling and profit withdrawal.

## 25. Structural acceptance test

The taxonomy is structurally tested without creating a fictitious market result, Experiment, Strategy, Candidate, demo session or live trade.

Acceptance requires that the taxonomy unambiguously answers, for each canonical class:

1. what protocol/source produced it;
2. what claims it may support;
3. what claims it may not support;
4. what prerequisites are required for a stronger qualified class;
5. how negative evidence is retained;
6. how it is represented in Experiment Registry and Evidence Indexes;
7. why an attractive result alone cannot upgrade the class.

No synthetic return, P&L, drawdown, capital amount, broker or risk limit is introduced by this structural test.

## 26. M1-009 completion result

This taxonomy satisfies `WBS-1.9` when the Experiment Registry and Candidate/Strategy Evidence Index templates are aligned to the two-axis model and repository validation confirms the canonical markers.

Next dependent work:

`ATS2-M1-010 — Research review protocol`.

That step will define the repeatable review procedure that consumes the classified evidence and records `PROMOTE / PARK / REJECT` or other stage-appropriate decisions without changing evidence class post hoc.
