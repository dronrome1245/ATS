# Candidate Evidence Index

## Identity

- Candidate ID: `null`
- Parent Idea ID: `null`
- Parent Hypothesis ID: `null`
- Candidate Promotion Review reference: `null`
- Created on: `null`

## Purpose

This index lists the evidence and exploratory research context available when the Candidate was promoted. It does not upgrade the evidence class of any referenced artifact.

Canonical classification rules:

`governance/methodology/EVIDENCE_TAXONOMY.md`

## Evidence entries

For each material artifact record:

- Artifact / reference: `null`
- Experiment ID when applicable: `null`
- Research / lifecycle stage: `null`
- Source class: `null`
- Qualified evidence class: `null`
- Result / outcome: `null`
- Claim supported: `null`
- Claims explicitly not supported: `null`
- Known limitations: `null`
- Qualification basis / reviewer: `null`
- Evidence status: `CURRENT`

Allowed evidence status values:

`CURRENT / SUPERSEDED / INVALIDATED / HISTORICAL`

Repeat the entry block for every material artifact.

## Required classification discipline

- `EXPLORATORY_OBSERVATION` supports hypothesis generation only.
- Cheap Prototype remains source class `EXPLORATORY_PROTOTYPE`.
- Economic Pre-Screen remains a preliminary research-budget review.
- A formal Experiment has source class `REGISTERED_EXPERIMENT` only when its `EXP-...` context was registered before corresponding result observation.
- `research_stage = VALIDATION` does not by itself create `VALIDATION_EVIDENCE`.
- `VALIDATION_EVIDENCE`, `INDEPENDENT_EXAMINATION_EVIDENCE` and stronger classes require the prerequisites in `EVIDENCE_TAXONOMY.md`.
- Candidate promotion never upgrades evidence class.
- Positive result does not upgrade class; negative evidence retains the class earned by its protocol.

## Negative and discarded evidence

- Negative prototype / experiment references: `null`
- Discarded variants / alternatives: `null`
- Search degrees of freedom summary: `null`

Negative evidence is retained with the same source/qualified class it earned. It is not deleted or reclassified downward because its conclusion is unfavorable.

## Data and economic limitations

- Data Feasibility constraints: `null`
- Cost / execution limitations: `null`
- Concentration / sample limitations: `null`
- Capacity / operational limitations: `null`

## Open evidence requirements for S02–S05

- Research specification evidence needed: `null`
- Data / protocol evidence needed: `null`
- Baseline implementation evidence needed: `null`
- Economic viability evidence needed: `null`

Candidate promotion does not close these requirements and does not establish validated edge.
