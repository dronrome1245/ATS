# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M1_RESEARCH_METHODOLOGY / IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0: `COMPLETED / PASS`.

## Last completed

`ATS2-M1-009 — Evidence taxonomy operationalization` — `DONE`.

Artifact: `governance/methodology/EVIDENCE_TAXONOMY.md`.

Aligned surfaces:

- `experiments/REGISTRY.csv`;
- `experiments/README.md`;
- `tools/search_experiments.py`;
- Candidate Evidence Index template;
- Strategy Version Evidence Index template.

Core rule: `source_class` records how evidence was produced; `qualified_evidence_class` records the strongest claim class whose protocol prerequisites were actually satisfied. Result attractiveness does not upgrade class. Negative evidence is retained.

Registry indexes both evidence-class fields and still contains zero real Experiment rows.

## Current ready task

`ATS2-M1-010 — Research review protocol`

Next artifact: `governance/methodology/RESEARCH_REVIEW_PROTOCOL.md`.

The protocol must define review triggers, required input package, lineage/current-version checks, data/economic assumptions, formal Experiment completeness, evidence-class/sufficiency checks, reviewer roles, stage-appropriate decisions, bounded return-to-research, negative-evidence/dissent retention, immutable decision records and re-review triggers.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/methodology/EVIDENCE_TAXONOMY.md`.
6. `governance/methodology/RESEARCH_METHODOLOGY_V1.md`.
7. `governance/methodology/EXPERIMENT_REGISTRATION.md`.
8. `experiments/README.md`.

## Recovery check

- Last completed: `ATS2-M1-009`.
- Next task: `ATS2-M1-010`.
- Next artifact: `governance/methodology/RESEARCH_REVIEW_PROTOCOL.md`.
- Positive result upgrades evidence class automatically? — no.
- Can a weaker evidence class substitute for a required one? — no.
