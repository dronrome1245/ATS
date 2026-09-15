# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M1_RESEARCH_METHODOLOGY / IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0: `COMPLETED / PASS`.
- Real trading, demo, allocation and scaling remain disallowed current actions.

## Last completed

`ATS2-M1-010 — Research review protocol` — `DONE`.

Canonical package:

- `governance/methodology/RESEARCH_REVIEW_PROTOCOL.md`;
- `governance/methodology/RESEARCH_REVIEW_CHECKS.md`;
- `governance/methodology/RESEARCH_REVIEW_DECISIONS.md`;
- `governance/methodology/templates/RESEARCH_REVIEW_TEMPLATE.md`.

Core review rules:

- review is event-driven, not tied to an invented calendar cadence;
- package completeness and lineage/current-context are checked before interpretation;
- formal Experiment integrity and Registry consistency are checked when formal evidence is used;
- `source_class` and `qualified_evidence_class` constrain allowed claims;
- evidence sufficiency is stage-relative and has no universal trade-count threshold;
- negative/failed/contradictory evidence and reviewer dissent remain visible;
- positive progression cannot override blocking data/evidence/integrity defects;
- return-to-research is bounded by an explicit question and stop condition;
- issued reviews are immutable history; reconsideration creates a new Review ID.

Structural testing created no fictitious research or evidence objects.

## Current ready task

`ATS2-M1-011 — M1 Exit Review`

Canonical next artifact:

`governance/program/M1_EXIT_REVIEW.md`

Goal: verify end-to-end integrity of M1 and issue one explicit `PASS / FAIL` decision.

## M1 Exit checks

- `ATS2-M1-001…010` are DONE;
- Research Funnel decisions are unambiguous;
- Experiment preregistration/Registry are coherent;
- evidence classification and negative-evidence retention are operational;
- Research Review is repeatable and stage-aware;
- state/backlog/status/next/handoff/entrypoints agree;
- validator is green on main;
- structural tests did not create fake Idea/Candidate/Experiment/market evidence;
- safety permissions remain unchanged;
- a new agent can recover the process without conversation history.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/methodology/RESEARCH_REVIEW_PROTOCOL.md`.
6. `governance/methodology/EVIDENCE_TAXONOMY.md`.
7. `governance/methodology/EXPERIMENT_REGISTRATION.md`.
8. `experiments/README.md` and `experiments/REGISTRY.csv`.
9. M1 methodology artifacts as needed for exit verification.

## Boundary

M1 Exit does not select Reference Strategy #1, broker, jurisdiction, capital allocation or risk limits. A `PASS` only authorizes program transition to M2 Research Platform MVP, whose first task is `ATS2-M2-000 — Reference Consumer Profile`.

## Recovery check

- Last completed: `ATS2-M1-010`.
- Next task: `ATS2-M1-011`.
- Next artifact: `governance/program/M1_EXIT_REVIEW.md`.
- M1 status before exit decision: `IN_PROGRESS`.
- Real Experiment rows currently registered: `0`.
