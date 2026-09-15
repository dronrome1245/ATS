# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- Real trading, demo, allocation and scaling remain disallowed current actions.

## Last completed

`ATS2-M1-011 — M1 Exit Review` — `DONE / PASS`.

Canonical exit artifact:

`governance/program/M1_EXIT_REVIEW.md`.

M1 provides the structural Research Factory path:

`Idea → Hypothesis → Data Feasibility → Cheap Prototype → Economic Pre-Screen → Candidate Review → preregistered Experiment → Registry → Evidence Classification → Research Review`.

Important M1 invariants:

- exploratory work is not retroactively formal evidence;
- Experiment preregistration precedes result observation;
- negative evidence is retained;
- `source_class` and `qualified_evidence_class` are distinct;
- attractive results do not upgrade evidence class;
- Research Review is event-driven and stage-aware;
- review history is immutable and bounded return-to-research prevents unlimited rescue tuning.

Structural testing created no fictitious Idea/Hypothesis/Candidate/Experiment/market result. Pipeline counters remain zero intentionally.

## Current ready task

`ATS2-M2-000 — Reference Consumer Profile`

Canonical next artifact:

`governance/program/REFERENCE_CONSUMER_PROFILE.md`

Goal: define the minimum abstract consumer contract that is sufficient to choose/build the first M2 vertical research stack without selecting a concrete Reference Strategy #1.

## What M2-000 must define

- minimum ordered research/market data contract;
- timestamp/order semantics needed by the first stack;
- minimal strategy/research decision interface;
- deterministic replay/backtest expectations;
- explicit cost-model inputs;
- minimum analytics/result outputs;
- integration with registered Experiment manifest/result/conclusion;
- reproducibility requirements;
- required M2 capabilities versus explicit out-of-scope capabilities;
- enough constraints for `ATS2-M2-001 — Research stack ADR`;
- alignment of WBS-2.1 so stack choice depends on Consumer Profile rather than an M3 strategy that has not yet been selected.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/M1_EXIT_REVIEW.md`.
6. `governance/program/PROGRAM_WBS_V2.md`.
7. `governance/program/PROGRAM_CHARTER_V2.md`.
8. M1 Experiment/Data/Evidence methodology as needed.

## Boundary

M2 builds safe research infrastructure only. Do not select a concrete Reference Strategy #1, market, instrument, broker, jurisdiction, capital allocation, risk limits or live environment.

Concrete Reference Strategy #1 selection remains M3 work after M2 Exit.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last completed: `ATS2-M1-011`.
- Next task: `ATS2-M2-000`.
- Next artifact: `governance/program/REFERENCE_CONSUMER_PROFILE.md`.
- M1 exit decision: `PASS`.
- Reference Strategy #1 selection allowed now? — no.
- Real Experiment rows registered: `0`.
