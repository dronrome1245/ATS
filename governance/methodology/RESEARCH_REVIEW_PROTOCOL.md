# ATS Research Review Protocol

**Task:** `ATS2-M1-010`  
**Work package:** `WBS-1.10`  
**Status:** BASELINE

## Purpose

Provide one repeatable review procedure that consumes current ATS research artifacts and produces an auditable stage-appropriate decision without weakening stage-specific methodology or evidence requirements.

## Core rules

1. Review is event-driven; ATS does not invent a universal weekly/monthly cadence.
2. The applicable stage-specific methodology supplies the decision model.
3. Evidence class is checked before claims are accepted.
4. Negative, failed, contradictory and superseded evidence remains visible.
5. Missing required inputs are not filled with invented assumptions.
6. A favorable metric cannot override a blocking data, lineage, integrity or evidence-class defect.
7. Return-to-research is bounded by one explicit unresolved question and a stop condition.
8. Issued review records are historical and are not rewritten after new evidence arrives.

## Canonical review artifact

Template: `governance/methodology/templates/RESEARCH_REVIEW_TEMPLATE.md`

Real review: `research/reviews/RR-YYYYMMDD-nnn.md`

A later reconsideration receives a new Review ID and links the previous review.

## Required checks

Every review records:

- target, stable IDs and requested decision;
- review trigger;
- preparer, reviewer and decision authority;
- input artifact package;
- completeness result;
- lineage/current-context result;
- formal Experiment integrity when applicable;
- `source_class` / `qualified_evidence_class` for material evidence;
- evidence sufficiency and limitations;
- economic/data/execution assumptions relevant to the decision;
- negative evidence and dissent;
- one stage-appropriate decision and reason;
- bounded follow-up when applicable;
- prior Review ID for reconsideration.

## Completion

`ATS2-M1-010` is complete when the detailed review procedure and reusable template are synchronized with state/backlog/handoff/validator. Next task: `ATS2-M1-011 — M1 Exit Review`.
