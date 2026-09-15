# M0 Exit Review — Program Rebaseline v2

**Task:** `ATS2-M0-013`  
**Milestone:** `M0_PROGRAM_REBASELINE`  
**Decision:** `PASS`  
**Date:** 15 September 2026

## 1. Purpose

This review decides whether ATS Program Rebaseline v2 is complete and whether the program may enter M1 Research Factory.

`PASS` here means only that the program governance, research methodology, repository structure, backlog, templates, canonical state, handoff and validation controls are ready for research work. It is not a trading admission decision.

## 2. Exit criteria

The Program WBS defines M0 Exit as:

1. `WBS-0.1` through `WBS-0.12` complete;
2. repository validator passes on `main`;
3. a new agent can determine the next milestone without external conversation context.

All three criteria are satisfied.

## 3. WBS evidence

| Work package | Result | Evidence |
|---|---|---|
| `WBS-0.1` Program Charter | PASS | `governance/program/PROGRAM_CHARTER_V2.md` |
| `WBS-0.2` Operating Model | PASS | `governance/program/OPERATING_MODEL_V2.md` |
| `WBS-0.3` Strategy Lifecycle | PASS | `governance/methodology/STRATEGY_LIFECYCLE_V2.md` |
| `WBS-0.4` Research Methodology | PASS | `governance/methodology/RESEARCH_METHODOLOGY_V1.md` |
| `WBS-0.5` Program WBS | PASS | `governance/program/PROGRAM_WBS_V2.md` |
| `WBS-0.6` Repository Structure | PASS | `governance/program/REPOSITORY_STRUCTURE_V2.md` |
| `WBS-0.7` Program Backlog | PASS | `governance/backlog/PROGRAM_BACKLOG_V2.md` |
| `WBS-0.8` Research entity templates | PASS | `governance/methodology/templates/README.md` |
| `WBS-0.9` Canonical state v2 | PASS | `03_СОСТОЯНИЕ_ПРОЕКТА.yaml` |
| `WBS-0.10` Repository validator v2 | PASS | `tools/validate_repo.py` |
| `WBS-0.11` AI handoff protocol | PASS | `AI_HANDOFF.md`, `AGENTS.md`, AI pointer files |
| `WBS-0.12` Legacy classification | PASS | `legacy/v1/README.md`, `MIGRATION_INDEX.md`, `CARRYOVER.md` |

## 4. Structural and CI evidence

`ATS2-M0-012` completed the final link/validator sweep.

The hardened validator detected two stale AI entrypoints, they were corrected, and GitHub Actions validation run `106` completed successfully on `main`.

The repository now enforces:

- current ATS v2 governance under `governance/`;
- one canonical machine-readable state;
- synchronized state/backlog/handoff/next action;
- archived ATS v1 only under `legacy/v1/`;
- rejection of removed v1/current-v2 paths if they reappear;
- local Markdown link validity in current documentation;
- existing safety invariants.

## 5. Handoff test

A new agent can determine without prior chat history:

- ATS is a Strategy Factory program, not one robot;
- M0 Program Rebaseline is complete;
- the current milestone is M1 Research Factory;
- the next task is `ATS2-M1-001 — Idea intake process`;
- the next artifact is `governance/methodology/IDEA_INTAKE_PROCESS.md`;
- G01–G13 are legacy history/reference, not the current roadmap;
- no real-money, demo, allocation or scaling permission exists.

This satisfies the M0 handoff criterion.

## 6. Safety boundary after M0

M0 Exit does **not** approve or select:

- a concrete Reference Strategy;
- broker or account;
- jurisdiction or tax treatment;
- real capital or allocation;
- Strategy Risk Mandate;
- demo/shadow admission;
- minimal live trading;
- scaling;
- profit withdrawal policy.

All corresponding safety flags remain false. Those decisions remain governed by later lifecycle/program stages and OWNER decision rights.

## 7. Decision

`M0_PROGRAM_REBASELINE = COMPLETED`.

ATS is authorized to enter `M1_RESEARCH_METHODOLOGY` / Research Factory work.

The first program-level task is:

`ATS2-M1-001 — Idea intake process`.

Deliverable:

`governance/methodology/IDEA_INTAKE_PROCESS.md`.

M1 should operationalize the Research Funnel before any Reference Strategy #1 selection or shared platform build beyond demonstrated research needs.
