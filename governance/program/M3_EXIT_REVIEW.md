# M3 Exit Review — Reference Strategy #1

**Task:** `ATS2-M3-005`  
**Milestone:** `M3_REFERENCE_STRATEGY_1`  
**Decision:** `PASS`  
**Date:** 21 September 2026

## 1. Purpose

This review decides whether M3 achieved its program goal: exercise the ATS research process on a real strategy line, preserve the evidence honestly, and learn what the shared platform actually needs.

A `PASS` here does **not** mean Reference Strategy #1 was successful.

Reference Strategy #1 was rejected at the Cheap Prototype stage:

`HYP-0001 / PROTO-01 = REJECT`.

M3 passes because ATS correctly stopped a weak research line using rules fixed before the result, retained the negative evidence, and converted the first real-data run into reusable platform/program learnings.

## 2. M3 exit criterion

M3 is complete when Reference Strategy #1 either reaches the later research gates or is correctly rejected earlier, while preserving reproducible evidence and platform learnings.

For this review the exit requires:

1. one Reference Strategy class selected deliberately;
2. a real Idea and falsifiable Hypothesis registered;
3. Data Feasibility reviewed before quantitative testing;
4. a real market dataset identified, cleaned, versioned and hashed;
5. one Cheap Prototype question and decision rule fixed before result observation;
6. the prototype result retained without parameter rescue;
7. the terminal research decision recorded;
8. reusable data/platform learnings separated from strategy-specific logic;
9. exact-commit Local CI closure of the prototype implementation.

All criteria are satisfied.

## 3. Research path

| Work package | Result | Evidence |
|---|---|---|
| `WBS-3.1` Select Reference Strategy #1 | PASS | `governance/program/REFERENCE_STRATEGY_1_SELECTION.md` |
| `WBS-3.2` Idea & rationale | PASS | `research/ideas/IDEA-0001.md`, `research/hypotheses/HYP-0001.md` |
| `WBS-3.3` Data feasibility | `CONDITIONAL` | `research/reviews/HYP-0001-DATA_FEASIBILITY.md` |
| `WBS-3.4` Cheap prototype | `REJECT` research outcome | `research/reviews/HYP-0001-PROTOTYPE-01.md`, `reports/research/HYP-0001-PROTOTYPE-01-result.json` |
| `WBS-3.5` Economic pre-screen | NOT ENTERED | Prototype did not produce `ADVANCE_TO_ECONOMIC_SCREEN` |
| `WBS-3.6`–`WBS-3.10` formal Candidate / Strategy work | NOT ENTERED | No Candidate or Strategy ID was created |
| `WBS-3.11` Platform learning review | PASS via early-rejection path | this M3 Exit Review |

The rejected line stops at R3. No Economic Pre-Screen, Candidate admission, formal Experiment, Strategy Version, validation or live engineering is created for HYP-0001.

## 4. Prototype result

The prototype tested one preregistered question on EUR/USD 1H data for full calendar years 2021–2025.

Frozen rule:

- signal: completed BID close above the maximum BID high of the previous 24 completed contiguous tradable hours;
- modeled entry: next-hour ASK open;
- modeled evaluation: BID open 24 contiguous tradable hours later;
- primary requirements: signal mean return > 0 and signal mean return > unconditional baseline.

Observed result:

- aligned tradable H1 bars: `31,296`;
- eligible baseline observations: `18,485`;
- breakout signals: `1,006`;
- mean signal return: `-0.0002301573` (about `-0.0230%`);
- unconditional mean return: `-0.0000647136` (about `-0.0065%`);
- signal minus baseline: `-0.0001654436` (about `-0.0165%`);
- signal positive share: `45.8250%`;
- overlapping signal-window share: `71.8688%`.

Both primary inequalities failed, so the preregistered decision was:

`REJECT — ONE_OR_BOTH_PRIMARY_HYPOTHESIS_INEQUALITIES_FAILED`.

This is negative `EXPLORATORY_PROTOTYPE` evidence. It is not formal validation evidence.

## 5. Data reproducibility

Canonical Dataset Manifest:

`data/manifests/DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml`

Dataset identity:

`DATA-DUKASCOPY-EURUSDH1-PROTO01-001 / 1.0.0`

Prepared CSV SHA-256:

`aeda05d90994259a22e25d882398218aead968941fe0b1c73eb34894841291c0`

Source-bundle SHA-256:

`cf378faaae58424112d289315b2ec076f4100775f2613a5d2d685ec46a02aba4`

The prepared dataset contains exactly `31,296` expected tradable hours and zero missing expected tradable hours.

Raw Dukascopy files remain local/external rather than being copied into Git.

## 6. Reproducibility and Local CI evidence

Prototype result run commit:

`6115b1c7114e942a4f3e76795ce8d25b552cf849`

M3-004 accepted closure commit:

`b2da28bdb53ed3e7606c15a04351aca55888ae4a`

OWNER Local CI report on 21 September 2026 confirmed:

- complete pytest suite: `86 passed`;
- working tree: `CLEAN`;
- repository validator: PASS;
- Ruff lint: PASS;
- Ruff format: PASS;
- environment fingerprint: PASS;
- CPython: `3.13.15`;
- uv: `0.12.13`;
- `ATS LOCAL CI: PASS`;
- `ATS CURRENT TASK CHECK: PASS`;
- `ATS TASK LAUNCHER: PASS`.

## 7. Platform and methodology learnings

### L1 — Market calendar semantics must be explicit

The first raw preparation initially exposed that Dukascopy monthly H1 cache files contain calendar-hour candles during closed FX weekend hours.

ATS therefore needed explicit market-session filtering plus daylight-saving boundary tests before the dataset could be used honestly.

Reusable lesson:

> a generic "hourly" frequency is not enough to infer whether an observation is tradable; market-calendar/session semantics belong to data preparation or a future reusable calendar capability when another consumer proves the need.

### L2 — BID/ASK semantics materially change the question

HYP-0001 could not be evaluated honestly from a single idealized price series.

The prototype therefore used:

`ASK entry → BID exit`

so quoted spread was represented directly.

Reusable lesson: execution-side semantics must stay explicit in data and research protocols.

### L3 — Dataset identity worked on real licensed data

The existing Dataset Manifest model successfully bound:

- source identity;
- fixed period;
- event and availability time;
- quality policy;
- transformation lineage;
- prepared-data SHA-256.

The source consisted of 120 monthly BID/ASK files, so a separate source-bundle SHA-256 was also recorded.

Potential future improvement: if multiple future consumers need it, Dataset Manifest may gain first-class multi-object/source-bundle integrity metadata. Do not generalize it yet from one consumer.

### L4 — Dependence must be visible in validation

`71.8688%` of breakout signal windows overlapped another signal window.

Reusable lesson: a later Validation Framework must distinguish raw observation count from effective independent evidence and explicitly address overlap/dependence.

### L5 — Cheap rejection prevented unnecessary engineering

Because R3 returned `REJECT`, ATS correctly did **not** build:

- commission/rollover infrastructure for this strategy;
- Candidate/Strategy entities;
- formal experiment packages;
- broker/live adapters;
- risk mandate or capital logic.

This is expected behavior of the Strategy Factory: expensive work follows evidence rather than preceding it.

### L6 — Exact Local CI caught non-research drift

The first M3-004 closure attempt passed tests and validator but failed Ruff format on `tools/proto01_eurusd.py`.

The formatting-only correction was made without changing the prototype result, and the exact corrected commit then passed the complete gate.

Reusable lesson: completion requires exact-commit repository quality, not only correct research logic.

## 8. Program-roadmap learning

The original M4 strategy-specific wording targeted "Reference Strategy #1" directly.

That is invalid after a legitimate early rejection: ATS must not validate a strategy that the Research Funnel already stopped.

Therefore WBS-4.9/WBS-4.10 are generalized to the **first future promoted Candidate**. Reference Strategy #1 would have filled that role only if it had survived research.

Program-level M4 framework work may start now. Strategy-specific validation remains blocked until a future research line earns Candidate/S05 eligibility.

## 9. Safety boundary after M3

M3 Exit does not authorize:

- demo/shadow trading;
- real-money trading;
- Candidate or Strategy creation for HYP-0001;
- capital allocation;
- leverage;
- Strategy Risk Mandate;
- broker/account selection;
- scaling.

All current live/capital safety permissions remain false.

## 10. Decision

`M3_REFERENCE_STRATEGY_1 = COMPLETED / PASS`.

Reference Strategy #1 research outcome remains:

`REJECTED_AT_R3`.

ATS may enter:

`M4_VALIDATION_FRAMEWORK / IN_PROGRESS`.

First M4 task:

`ATS2-M4-001 — Validation protocol framework`

Work package:

`WBS-4.1`

Canonical next artifact:

`governance/methodology/VALIDATION_FRAMEWORK.md`

The framework must be reusable for a future promoted Candidate and must not retroactively validate or rescue HYP-0001.

## 11. Transition-commit closure

This review records the M3 Exit decision based on the accepted prototype evidence and platform learnings above.

The `ATS2-M3-005` repository transition remains subject to the normal exact-commit Local CI Gate. M3 is operationally closed only after `ATS_TASK_CHECK.bat` passes on the final commit containing this review, synchronized state/backlog/status/handoff and validator changes.
