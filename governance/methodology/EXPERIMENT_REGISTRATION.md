# ATS Experiment Registration

**Task:** `ATS2-M1-007`  
**Work package:** `WBS-1.7`  
**Status:** BASELINE  
**Purpose:** define when and how an ATS experiment becomes a preregistered formal experiment whose later result may qualify as registered evidence.

## 1. Scope

This methodology governs formal `Experiment` registration across ATS research and later lifecycle stages.

A registered experiment answers a predeclared question under a frozen-enough context:

`Question + Hypothesis + Code + Data + Configuration + Costs + Metrics + Decision Rule → Result → Conclusion`

The central boundary is temporal:

> The decision-relevant experiment context must be registered before the corresponding result is observed.

Registration does not make the result true, significant, profitable, validated or independent. It only establishes that the experiment was specified before its result was known.

Cheap Prototype remains `EXPLORATORY_PROTOTYPE`. A completed prototype cannot receive an `EXP-...` ID afterward and be represented as preregistered evidence.

## 2. Canonical experiment package

A formal experiment lives under:

`experiments/EXP-YYYYMMDD-nnn/`

Minimum package:

- `manifest.yaml` — pre-result registered context;
- `result.json` — machine-readable observed result;
- `conclusion.md` — human interpretation and decision;
- optional `artifacts/` — plots, tables or other experiment outputs appropriate for Git/reference policy.

Canonical templates:

- `governance/methodology/templates/experiment/manifest.yaml`;
- `governance/methodology/templates/experiment/result.json`;
- `governance/methodology/templates/experiment/conclusion.md`.

The package becomes complete evidence only after manifest, result and conclusion exist and refer to the same Experiment ID.

## 3. Experiment identity

ID format:

`EXP-YYYYMMDD-nnn`

Example shape:

`EXP-20260915-001`

Rules:

1. Date component is the registration date in the program record, not the date a historical dataset begins.
2. Sequence is unique for that date across ATS.
3. An Experiment ID is never reused after cancellation, failure, rejection, supersede or deletion request.
4. One Experiment ID represents one registered question/context and one corresponding result observation.
5. A materially changed question, dataset/period, implementation, parameters, cost model or decision rule requires a new Experiment ID once the original experiment has been registered.
6. Structural template testing does not allocate an Experiment ID.

## 4. Registration states

Allowed registration states:

`DRAFT → REGISTERED → RUNNING → COMPLETED`

Alternative terminal states:

`DRAFT → CANCELLED`  
`REGISTERED → CANCELLED`  
`REGISTERED → SUPERSEDED`

Meaning:

- `DRAFT` — context may still be edited; no result may be represented as preregistered evidence from this draft.
- `REGISTERED` — preregistration boundary is frozen and committed before result observation.
- `RUNNING` — execution has begun under the registered context.
- `COMPLETED` — result and conclusion are recorded.
- `CANCELLED` — no valid result is claimed under this registration.
- `SUPERSEDED` — a replacement Experiment ID was registered before a result was used from the superseded context.

A result observed while the manifest is still `DRAFT` is exploratory, not preregistered formal evidence.

## 5. Registration eligibility

A formal experiment must have a real research purpose and an identifiable parent claim.

Minimum eligibility:

- a real `HYP-xxxx` exists;
- the experiment question is specific enough to evaluate;
- required data/implementation can be identified;
- the intended research stage is known;
- primary metrics and decision rule can be stated before observing the result.

Candidate ID and Strategy/Strategy Version linkage are required only when those entities already exist and the experiment operates on them.

A pre-Candidate registered experiment may therefore have:

- `hypothesis_id` populated;
- `candidate_id = NOT_APPLICABLE` with reason;
- `strategy_id = NOT_APPLICABLE` with reason;
- `strategy_version = NOT_APPLICABLE` with reason.

## 6. Evidence class and research stage

Every registered experiment records:

`evidence_class: REGISTERED_EXPERIMENT`

This class means only that preregistration requirements were satisfied.

The manifest separately records `research_stage`, for example:

- `RESEARCH`;
- `VALIDATION`;
- `INDEPENDENT_EXAMINATION`;
- `STRESS`;
- `EXECUTION`;
- another explicitly defined future stage.

`REGISTERED_EXPERIMENT` does not automatically mean validation evidence. Claim strength is constrained by research stage, data independence, protocol quality and the later Evidence Taxonomy.

## 7. Required pre-result identity and lineage

Before status becomes `REGISTERED`, the manifest must record:

- Experiment ID;
- status `REGISTERED`;
- created date/time;
- registered date/time;
- registration actor/role;
- evidence class;
- research stage;
- Idea ID when relevant;
- Hypothesis ID;
- Candidate ID when available;
- Strategy ID / Strategy Version when available;
- superseded Experiment ID when this registration replaces an earlier unused/superseded registration.

Unknown lineage that should already exist is blocking. Truly inapplicable downstream identities use `NOT_APPLICABLE` plus explanation.

## 8. Code and implementation identity

The manifest must identify what implementation will be executed.

Required as applicable:

- `code_revision` — immutable Git commit/revision when code is in Git;
- `implementation_reference` — script/notebook/query/module path or external immutable reference;
- `environment_id` — environment/lockfile/container reference where relevant;
- implementation notes for any material runtime dependency not represented by the code revision.

If code is changed in a way that can change the result after registration, the registered experiment is no longer the same experiment and a new Experiment ID is required before observing the changed run's result.

Non-result-affecting operational fixes may be documented as an amendment only if they cannot change the computed experiment outcome.

## 9. Data identity and period

The preregistration must identify the data information set sufficiently to prevent silent sample switching.

Record:

- Dataset ID when canonical dataset tooling exists;
- otherwise source/snapshot reference sufficient to identify the intended input;
- data period / event scope;
- universe/sampling scope where relevant;
- timezone/timestamp semantics when relevant;
- transformation reference or data-preparation code revision;
- known data limitations inherited from Data Feasibility.

A post-registration switch to a materially different source, period, universe or timestamp interpretation requires a new Experiment ID.

Protected validation/independent blocks must never be opened merely to decide how to rewrite the registration.

## 10. Parameters and configuration

The manifest records all decision-relevant configuration needed to reproduce the registered run, including as applicable:

- strategy/research parameters;
- feature parameters;
- entry/exit or event-window configuration;
- filters;
- sampling rules;
- data-cleaning choices not fixed by the Dataset identity;
- execution assumptions;
- any allowed parameter region when the registered question itself is a predefined search procedure.

An empty parameter object is acceptable only when the experiment truly has no tunable/configurable parameters affecting the result.

Unregistered parameter search cannot later be summarized only by its best result and presented as one preregistered experiment.

## 11. Randomness and seeds

If the experiment contains stochastic behavior, the preregistration records the random seed or a fully specified seed-generation/repetition protocol.

If no stochastic component exists:

`random_seed: NOT_APPLICABLE`

and the applicability notes state why.

Changing a seed after inspecting an unfavorable result is a new experiment unless the registered protocol explicitly required multiple seeds and defined how their results would be aggregated.

## 12. Cost and execution assumptions

Where economically relevant, the manifest freezes the cost/execution context before result observation.

Record as applicable:

- spread model;
- commission;
- slippage model/proxy;
- financing/swap;
- latency/delay;
- fill/partial-fill assumptions;
- market-impact/capacity assumption when material;
- other economic deductions relevant to the question.

A gross-only experiment is allowed only when the question is explicitly gross-only and the conclusion does not make a net-profitability claim.

## 13. Predefined question

Every formal experiment has one primary predefined research question.

It must be answerable by the registered data, metrics and decision rule.

Good structure:

- Does the predefined effect retain the expected direction under the specified dataset, period and costs?
- Does the fixed Strategy Version satisfy the registered validation criterion on the protected block?
- Does execution degradation within the registered stress scenario breach the predefined acceptance rule?

Bad structure:

- Find something profitable.
- Optimize until performance improves.
- Decide later which metric matters.

Additional exploratory findings may be recorded after the experiment, but they are secondary observations and do not rewrite the primary registered question.

## 14. Primary and secondary metrics

Primary metrics are named before result observation and are the metrics used by the predefined decision rule.

Secondary metrics are diagnostics whose purpose is interpretation, risk/context or anomaly detection.

Rules:

1. At least one primary metric is required unless the research class has a clearly documented non-numeric binary/event outcome.
2. Metric definitions must be unambiguous enough to reproduce.
3. A favorable secondary metric cannot replace an unfavorable primary metric after the result is observed.
4. A newly discovered useful metric may motivate a new Experiment ID; it does not become retroactively primary for the old experiment.

## 15. Predefined decision rule

The manifest records the decision rule before result observation.

The rule may be quantitative, categorical or composite, but must state what result maps to the stage-appropriate decision.

Examples of decision structure:

- `PASS` only if predefined primary criteria are satisfied and no registered blocking defect occurs;
- `FAIL` if the primary effect has the wrong direction;
- `RETURN_TO_RESEARCH` if a specifically predefined ambiguity is triggered;
- stage-specific `PROMOTE / PARK / REJECT` where that is the governing decision model.

The experiment conclusion may explain why the rule cannot be evaluated because of a data/runtime defect, but it may not invent a more convenient success rule after seeing the result.

## 16. Registration boundary in Git

Registration is considered complete only when the `REGISTERED` manifest exists in repository history before the corresponding result is observed.

The Git commit containing the registered manifest is the immutable historical anchor. The manifest does not store its own commit SHA because that would create a self-reference problem.

`ATS2-M1-008 — Experiment registry` will make that anchor discoverable by recording Experiment ID, manifest path and registration revision/commit reference.

Until registry tooling exists, the Git history plus canonical experiment directory is sufficient for M1-007 preregistration semantics.

## 17. Amendments before result observation

### Draft edits

While status is `DRAFT` and no result has been observed, any field may be edited.

### After `REGISTERED`

Decision-relevant fields are frozen.

A material change to any of the following requires a new Experiment ID:

- predefined question;
- Hypothesis or Strategy Version;
- dataset/source/period/universe;
- result-affecting code revision;
- parameters/configuration;
- cost/execution assumptions;
- primary metrics;
- decision rule;
- research stage/evidence claim;
- randomness protocol.

The old registration is marked `SUPERSEDED` or `CANCELLED` without attaching the replacement result to it.

Administrative, non-semantic corrections may be appended to `registration.amendments` only when they cannot change the experiment result or decision. Each amendment records timestamp, actor, reason and changed field/text.

Examples: spelling correction in a note or repaired non-semantic reference. Changing a period or cost assumption is not administrative.

## 18. Post-result changes

Once any result from the registered context is observed by the research process, the preregistration context is historically fixed.

Prohibited:

- changing primary metrics and pretending they were original;
- changing pass/fail criteria after seeing the result;
- changing sample period and reusing the same Experiment ID;
- changing costs/parameters to rescue the experiment under the same registration;
- deleting an unfavorable experiment from the evidence history;
- assigning an old exploratory run an `EXP-...` ID and calling it preregistered.

Corrections to result calculation caused by a genuine implementation defect require explicit defect documentation. If the defect could materially affect the result, the corrected run receives a new Experiment ID unless a later stage-specific protocol explicitly defines another auditable correction procedure.

## 19. Result file

`result.json` is populated only after execution/observation.

It records machine-readable facts, not interpretation.

Minimum relationship to manifest:

- same Experiment ID;
- completion timestamp;
- observed primary metrics;
- observed secondary metrics;
- opportunity/trade/event count when applicable;
- realized/modelled costs where applicable;
- risk diagnostics where applicable;
- output artifact references;
- machine outcome if deterministically derivable from the registered rule;
- execution/reproducibility metadata needed to identify the actual run.

A missing metric remains explicitly unavailable; it is not fabricated.

## 20. Conclusion file

`conclusion.md` evaluates the registered question against the registered decision rule.

It records:

- identity and research stage;
- registered question;
- registered primary rule;
- observed result summary;
- decision-rule evaluation;
- evidence/data/reproducibility limitations;
- interpretation: what the experiment supports and does not support;
- stage-appropriate decision;
- follow-up question if needed.

A follow-up question is a new future experiment where preregistration is required; it does not modify the completed experiment.

## 21. Failed, negative and cancelled experiments

Negative evidence is retained.

- A `FAIL` result remains discoverable.
- A registered experiment cancelled before execution remains discoverable as `CANCELLED`.
- A registration replaced before result use remains discoverable as `SUPERSEDED` and links to the replacement Experiment ID.
- A runtime/data failure is recorded honestly; it is not silently rerun under modified assumptions using the same historical claim.

This prevents the registry from becoming a collection of winners only.

## 22. Relationship to Cheap Prototype

Cheap Prototype and formal Experiment serve different purposes.

Cheap Prototype:

- cheap/exploratory;
- local `PROTO-nn` identity;
- allows limited documented iteration;
- evidence class `EXPLORATORY_PROTOTYPE`.

Formal Experiment:

- stable `EXP-YYYYMMDD-nnn` identity;
- registered before result observation;
- frozen question/context/primary decision rule;
- evidence class `REGISTERED_EXPERIMENT`.

If a prototype finding is important enough to become formal evidence, register a new formal experiment and rerun it. The prototype remains visible as prior exploratory history.

## 23. Decision authority

Routine experiment registration may be performed by RESEARCH / VALIDATION roles under the applicable protocol because registration itself creates no financial exposure.

OWNER approval is not required merely to register or run a non-live research experiment.

OWNER decision rights remain reserved for program capital policy, Strategy Risk Mandate, live admission, allocation, scaling and profit withdrawal.

## 24. Structural acceptance test

The experiment templates are tested structurally without creating a fictitious Experiment ID, market result, return, dataset, Strategy or Candidate.

The schema must be able to represent:

- stable Experiment identity;
- `DRAFT/REGISTERED/RUNNING/COMPLETED/CANCELLED/SUPERSEDED` state;
- `REGISTERED_EXPERIMENT` evidence class;
- Hypothesis and optional Candidate/Strategy lineage;
- code/implementation/environment identity;
- dataset/source snapshot and period;
- parameters/configuration;
- random seed/applicability;
- cost/execution assumptions;
- predefined question;
- primary/secondary metrics;
- predefined decision rule;
- registration timestamp/actor;
- administrative amendment history;
- result and conclusion file references;
- observed result fields separated from preregistration.

The structural test fills no fictitious result and allocates no `EXP-...` ID.

## 25. Definition of Done for a real registered Experiment

Registration is complete before result observation when:

- a unique Experiment ID is allocated;
- parent Hypothesis and other applicable lineage are recorded;
- code/implementation and data context are identifiable;
- decision-relevant configuration is fixed;
- applicable cost/execution assumptions are fixed;
- primary question/metrics/decision rule are defined;
- research stage and evidence class are explicit;
- randomness is fixed or explicitly not applicable;
- status is `REGISTERED`;
- registration metadata are recorded;
- the registered manifest is committed before the corresponding result is observed.

The experiment becomes a complete registered evidence package only after its result and conclusion are recorded without rewriting the preregistration history.

## 26. M1-007 completion result

This methodology plus the aligned experiment templates satisfies `WBS-1.7`.

Next dependent work:

`ATS2-M1-008 — Experiment registry`.

That step must make positive, negative, cancelled and superseded experiments discoverable by stable ID and bind each registry entry to its registered manifest/context.