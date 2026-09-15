# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Current phase: `M0_PROGRAM_REBASELINE`.
- Status: `IN_PROGRESS`.
- Program model: ATS v2 / Strategy Factory.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Current governance: `governance/program/` и `governance/methodology/`.
- ATS v1: `legacy/v1/`, history/reference only.
- Real trading, allocation and scaling are not permitted current actions.

## 2. Last completed

`ATS2-M0-012 — Final link/validator sweep` завершена.

Last completed artifact:

`governance/program/M0_FINAL_SWEEP.md`

Sweep hardened `tools/validate_repo.py`, found two stale AI pointers, corrected `.github/copilot-instructions.md` and `CLAUDE.md`, and finished with successful GitHub Actions validation run `105`.

## 3. Next task

`ATS2-M0-013 — M0 Exit Review`

Next artifact:

`governance/program/M0_EXIT_REVIEW.md`

The Exit Review decides only whether Program Rebaseline is complete and M1 Research Factory may start.

It must not select Strategy #1, broker, jurisdiction, capital allocation or live risk limits.

## 4. Canonical ATS v2 documents

Program:

- `governance/program/PROGRAM_CHARTER_V2.md`;
- `governance/program/OPERATING_MODEL_V2.md`;
- `governance/program/PROGRAM_WBS_V2.md`;
- `governance/program/REPOSITORY_STRUCTURE_V2.md`;
- `governance/program/M0_FINAL_SWEEP.md`.

Methodology:

- `governance/methodology/STRATEGY_LIFECYCLE_V2.md`;
- `governance/methodology/RESEARCH_METHODOLOGY_V1.md`;
- `governance/methodology/templates/README.md`.

Execution queue:

- `governance/backlog/PROGRAM_BACKLOG_V2.md`.

Legacy:

- `legacy/v1/README.md`;
- `legacy/v1/MIGRATION_INDEX.md`;
- `legacy/v1/CARRYOVER.md`.

## 5. Required read order

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. relevant current governance/methodology.
6. legacy only when historical/carryover context is needed.

## 6. M0 Exit Review checklist

The reviewer must verify:

- WBS-0.1…0.12 deliverables exist;
- validator is green on `main`;
- no old source paths are operational;
- current AI entrypoints point to current state/backlog;
- legacy is isolated and marked superseded;
- state/backlog/handoff/next-step agree;
- safety invariants remain false for live/scaling permissions;
- new context can recover current state without chat history.

## 7. Non-negotiable safety/governance

Without OWNER decision, do not:

- allocate real capital;
- approve Strategy Risk Mandate;
- permit live admission;
- change allocation/scaling;
- invent broker/jurisdiction/instrument/return/risk values;
- weaken independent evidence rules;
- introduce martingale, unlimited averaging or rescue funding.

## 8. Recovery check

A new agent should answer:

- Current phase? — `M0_PROGRAM_REBASELINE`.
- Last completed task? — `ATS2-M0-012`.
- Last artifact? — `governance/program/M0_FINAL_SWEEP.md`.
- Next task? — `ATS2-M0-013`.
- Next artifact? — `governance/program/M0_EXIT_REVIEW.md`.
- Is live trading permitted? — no.
- Are G01–G13 current roadmap? — no; they are legacy ATS v1.
