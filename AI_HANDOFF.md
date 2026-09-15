# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M2_RESEARCH_PLATFORM_MVP / IN_PROGRESS`.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- M0: `COMPLETED / PASS`.
- M1: `COMPLETED / PASS`.
- Real trading, demo, allocation and scaling remain disallowed.

## Last completed

`ATS2-M2-000 — Reference Consumer Profile` — `DONE`.

Canonical artifact:

`governance/program/REFERENCE_CONSUMER_PROFILE.md`

Reference consumer contract:

- one finite deterministic ordered research/event stream per run;
- stable Dataset Manifest and explicit timestamp/order semantics;
- broker-independent Strategy/Research decision interface;
- deterministic replay/backtest;
- explicit cost inputs with no invented universal defaults;
- machine-readable standard results/analytics;
- integration with registered Experiment manifest/result/conclusion;
- reproducible binding of code/environment/data/config/costs/result;
- deterministic synthetic software fixture for platform testing only.

The fixture is not a research entity or evidence.

WBS now contains `WBS-2.0`; `WBS-2.1` depends on the Consumer Profile rather than an unselected Reference Strategy #1.

M2-facing `data/`, `src/` and `reports/` policies are aligned with ATS v2.

## Current ready task

`ATS2-M2-001 — Research stack ADR`

Canonical next artifact:

`governance/decisions/ADR-0001-RESEARCH-STACK.md`

Goal: choose the smallest viable research technology stack that satisfies the Reference Consumer Profile.

## M2-001 must decide

- research language/runtime;
- environment/package/lock approach;
- data representation/loading baseline;
- config/manifest parsing;
- package/module boundaries;
- test framework and deterministic fixture approach;
- only the numerical/data dependencies actually justified;
- local/CI reproducibility;
- external dataset storage/manifests policy;
- rejected heavier alternatives and trade-offs;
- explicit exclusion of broker/live/portfolio/news/distributed/GUI requirements unless separately justified later.

## Read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. `governance/program/REFERENCE_CONSUMER_PROFILE.md`.
6. `governance/program/PROGRAM_WBS_V2.md`.
7. `governance/program/OPERATING_MODEL_V2.md`.
8. current Experiment/Data/Repository structure docs as needed.

## Boundary

M2 builds research infrastructure only. Do not select Reference Strategy #1, market, instrument, broker, jurisdiction, capital allocation, risk limits or live environment.

## Recovery check

- Current milestone: `M2_RESEARCH_PLATFORM_MVP`.
- Last completed: `ATS2-M2-000`.
- Next task: `ATS2-M2-001`.
- Next artifact: `governance/decisions/ADR-0001-RESEARCH-STACK.md`.
- Reference Strategy #1 selection allowed now? — no.
- Pipeline counts remain zero? — yes.
