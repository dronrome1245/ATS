# ATS M2 Reference Consumer Profile

**Task:** `ATS2-M2-000`  
**Work package:** `WBS-2.0`  
**Status:** BASELINE  
**Purpose:** define the minimum abstract consumer contract for the first reusable Research Platform MVP without selecting Reference Strategy #1.

## 1. Boundary

This profile describes what the M2 platform must be able to consume and produce. It is **not** a trading strategy specification.

M2-000 does not choose:

- market, venue or instrument;
- bar/tick/news strategy class;
- entry/exit rules or expected return;
- broker, account, jurisdiction or live environment;
- capital, leverage or risk limits;
- Reference Strategy #1.

Concrete Reference Strategy #1 remains an M3 decision.

## 2. Reference consumer

The minimum consumer is a **single research logic instance operating on a finite, deterministically ordered historical/research event stream**.

The consumer must be able to:

1. load a dataset identified by a stable dataset manifest;
2. receive observations/events in deterministic order;
3. use only information declared available at the current historical decision point;
4. maintain deterministic research state;
5. emit serializable research decisions/intents and diagnostics without broker-specific calls;
6. run through a deterministic replay/backtest context;
7. apply explicit cost assumptions when the question is economic;
8. produce machine-readable results and standard research artifacts linked to the registered Experiment context.

This shape is intentionally generic enough for a later simple bar/tick-like or other ordered-data strategy, while not requiring event/news ingestion or production execution in M2.

## 3. Minimum data contract

M2 must support at least one primary finite ordered dataset per run.

A dataset must have a manifest that identifies, as applicable:

- stable dataset ID/version;
- source or source snapshot reference;
- schema/reference format;
- coverage/period;
- timezone and timestamp semantics;
- ordering key and tie-breaking rule;
- duplicate/missing/bad-data policy;
- transformation/preparation reference;
- checksum/hash where practical;
- known limitations.

Each research record/event must be orderable deterministically. The platform contract must distinguish the event/observation time from the time at which information becomes available when those differ. If the two are equivalent for a dataset, that equivalence must be explicit rather than assumed silently.

The consumer does not require M2 to implement live feeds, vendor APIs, news ingestion or arbitrary multi-stream joins.

## 4. Timestamp and ordering semantics

The first stack must guarantee:

- unambiguous timezone-aware timestamps or an explicitly documented equivalent representation;
- deterministic ordering for equal timestamps;
- no use of later records to compute an earlier decision unless the registered protocol explicitly permits that information;
- deterministic handling of duplicates and missing records according to the Dataset Manifest;
- stable iteration order across repeated runs from the same input dataset/version.

Exact storage format and in-memory representation are technology decisions for `WBS-2.1` and later implementation tasks.

## 5. Minimum research decision interface

M2 requires a technology-neutral Strategy/Research interface, not a broker API.

The semantic contract is:

**Inputs**

- immutable run/configuration context;
- current ordered observation/event;
- current strategy/research state;
- declared parameters/features available to that run.

**Outputs**

- zero or more deterministic, serializable decision/intent records;
- optional state update;
- optional diagnostics needed for audit/replay.

The M2 interface must not require broker order IDs, account balance, live margin, portfolio allocation or live risk controls.

Exact method names, object model and programming language are decided by `ATS2-M2-001` / `WBS-2.5`.

## 6. Deterministic replay/backtest contract

Given the same:

`code revision + environment + dataset version + configuration + seed/protocol + cost assumptions`,

the platform must reproduce the same ordered decisions and result within exact equality or an explicitly documented numerical/randomness tolerance.

Minimum replay requirements:

- finite historical/research run;
- deterministic event ordering;
- no hidden dependency on wall-clock time or live broker/network state;
- explicit seed/protocol for stochastic components;
- decision trace sufficient to inspect a sample manually;
- explicit separation between research logic and replay/execution simulation;
- repeatable result artifact generation.

M2 does not need production-grade exchange queue simulation, broker recovery or live reconciliation.

## 7. Cost-model consumer contract

Economic experiments must not receive hidden cost constants.

The platform must accept explicit cost/execution assumptions as run inputs and report their contribution separately from gross effect/performance.

The cost interface must be able to represent applicable components such as fees/commission, spread and slippage/proxy, while allowing additional components to be added later when a real consumer requires them.

No universal numeric defaults are defined by this profile. A component that is genuinely not applicable must be explicit rather than silently omitted.

## 8. Minimum outputs

A completed M2 run must be able to produce, as applicable:

- run/Experiment identity and input references;
- ordered decision/intent trace;
- trade/event/effect output generated by the replay model;
- gross effect/P&L where applicable;
- explicit modeled costs and net effect/P&L where applicable;
- event/trade/opportunity count where meaningful;
- baseline risk/path information such as drawdown when monetary/equity semantics exist;
- diagnostics for data/order/runtime anomalies;
- machine-readable result compatible with the ATS Experiment result contract;
- standard human-readable research report or report input.

Metrics that are not meaningful for a given research question remain not applicable; the platform must not fabricate them.

## 9. Experiment integration

The Research Platform must integrate with the M1 Experiment model.

For a formal registered Experiment:

1. `manifest.yaml` supplies the frozen pre-result context;
2. runner/platform resolves the referenced code/data/config/environment/cost inputs;
3. execution does not rewrite the registered decision rule or primary metrics;
4. observed machine facts are written to `result.json` or an equivalent result object that can populate it;
5. `conclusion.md` remains the human/stage interpretation artifact;
6. Experiment Registry remains an index, not a second source of run truth.

A software fixture run used to test M2 infrastructure is not a formal `EXP-...` and is not market evidence.

## 10. Reproducibility requirements

The first vertical stack must support:

- version-controlled research code;
- reproducible/pinned environment specification;
- stable Dataset Manifest/version;
- explicit configuration/parameters;
- explicit randomness seed/protocol when applicable;
- explicit cost assumptions;
- machine-readable result;
- traceable binding of `code + environment + data + config + costs + result`.

A clean supported environment must be able to execute a deterministic fixture without broker/live services.

## 11. Required M2 capabilities

The profile requires these M2 capabilities:

1. `WBS-2.1` Research stack ADR;
2. `WBS-2.2` reproducible environment;
3. `WBS-2.3` Dataset Manifest support;
4. `WBS-2.4` deterministic base loader;
5. `WBS-2.5` minimal Strategy/Research interface;
6. `WBS-2.6` deterministic replay/backtest core;
7. `WBS-2.7` explicit cost-model interface;
8. `WBS-2.8` baseline analytics/report output;
9. `WBS-2.9` manifest-driven experiment runner;
10. `WBS-2.10` automated deterministic fixtures/regression checks.

## 12. Explicit M2 out of scope

M2 does not require:

- live market-data streaming or broker connectivity;
- order routing, live risk controller, reconciliation or recovery;
- portfolio/multi-strategy allocation engine;
- event/news ingestion unless later justified by a real consumer;
- distributed/HPC infrastructure;
- GUI/dashboard as a prerequisite for research correctness;
- universal optimizer/AutoML platform;
- cloud/VPS dependency;
- production monitoring/incident system;
- strategy-specific validation framework beyond M1 evidence discipline.

These capabilities are added demand-driven in later milestones.

## 13. M2 acceptance fixture

M2 may use a deterministic software fixture consisting of:

- synthetic non-market ordered records;
- a trivial deterministic research-logic fixture;
- explicit fixed configuration and cost inputs;
- expected decisions/results committed as test fixtures.

The fixture exists only to test platform correctness/reproducibility. It must not receive an Idea/Hypothesis/Candidate/Experiment ID and must not be presented as trading evidence.

A minimum end-to-end M2 acceptance run must demonstrate:

`fixture dataset → loader → research interface → replay → costs → analytics/result → reproducible rerun`.

Two runs from the same frozen inputs must agree within the declared deterministic/numerical tolerance.

Materialized M2-010 acceptance artifacts:

- `tests/test_research_platform.py`;
- `tests/fixtures/platform/reference_consumer_expected.json`.

The committed acceptance fixture covers Dataset Manifest → loader → Strategy/Research interface → replay → explicit costs → standard analytics/result and exact rerun equality. The separate M2-009 runner suite covers registered-manifest orchestration. The acceptance fixture itself carries no Idea/Hypothesis/Candidate/Strategy/Experiment identity and creates no Registry row.

## 14. Constraint for Research stack ADR

`ATS2-M2-001 — Research stack ADR` must choose the minimum technology stack against this profile, not against an invented Reference Strategy #1.

The ADR must explain how the selected stack supports:

- deterministic ordered-data processing;
- reproducible environments;
- Dataset Manifest/versioning;
- testable Strategy/Research interface;
- deterministic replay;
- explicit costs;
- machine-readable analytics/result;
- manifest-driven experiments;
- automated tests.

It must also state why materially heavier alternatives are not needed for the current consumer.

## 15. Definition of Done

`ATS2-M2-000` is complete when:

- this consumer contract is canonical;
- `PROGRAM_WBS_V2.md` contains `WBS-2.0` and makes `WBS-2.1` depend on the Consumer Profile rather than an unselected M3 strategy;
- no market/instrument/strategy/live assumptions were invented;
- state/backlog/status/next/handoff and validator are synchronized;
- `ATS2-M2-001 — Research stack ADR` is the single next ready task.
