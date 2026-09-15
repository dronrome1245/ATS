# ATS Research Review Checks

**Part of:** `ATS2-M1-010` / `RESEARCH_REVIEW_PROTOCOL.md`

## Input completeness

Classify the package as `COMPLETE`, `COMPLETE_WITH_LIMITATIONS`, or `INCOMPLETE_BLOCKING`.

Required where applicable: target identity/status, Idea/Hypothesis lineage, Candidate/Strategy Version identity, requested decision, Data Feasibility, Prototype/Economic history, formal Experiment IDs and Registry rows, Evidence Index, negative/failed/superseded evidence, material alternatives/search freedom, relevant cost/execution assumptions, unresolved limitations, prior decisions and material changes.

Missing decision-critical input is blocking; it is never replaced by invented assumptions.

## Lineage and currency

Result: `LINEAGE_OK / LINEAGE_BLOCKED`.

Verify that IDs refer to the object actually tested; evidence from another Strategy Version is not silently inherited; superseded/invalidated artifacts are not presented as current; revealed protected data are not still called independent for later tuning.

## Experiment integrity

When formal Experiments are used, verify Registry presence, package/manifest consistency, preregistration where required, result/conclusion completeness, disclosed defects/deviations and inclusion of material negative/failed Experiments.

`REGISTERED_EXPERIMENT` alone is not validation or independent evidence.

## Evidence class

For each material artifact record `source_class`, `qualified_evidence_class`, result/outcome, supported claim, unsupported claims, current evidence status and limitations.

Result: `CLASS_SUFFICIENT / CLASS_INSUFFICIENT`.

A weaker class cannot substitute for a class required by the stage.

## Evidence sufficiency

Result: `SUFFICIENT_FOR_DECISION / SUFFICIENT_WITH_LIMITATIONS / INSUFFICIENT`.

Assess, as relevant: effective sample/independent opportunities, temporal/regime/event diversity, dependence, concentration/outliers, uncertainty, cost sensitivity, research freedom/multiple testing, data timing/quality, reproducibility and contradictory evidence.

No universal trade-count threshold is used.
