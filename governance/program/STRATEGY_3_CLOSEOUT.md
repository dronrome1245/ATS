# Strategy #3 Early-Rejection Closeout

**Task:** `ATS2-RF-012`  
**Work package:** `WBS-RF.2 (Research Funnel closeout)`  
**Strategy line:** Strategy #3 / `HYP-0003`  
**Research outcome:** `REJECTED_AT_R3`  
**Status:** READY_FOR_OWNER_CLOSURE  
**Date:** 25 September 2026

## 1. Purpose

This closeout preserves the terminal HYP-0003 Cheap Prototype result, records reusable Research Factory learnings, and prevents the rejected broad-region claim from being rescued by selecting only favorable cells after reveal.

The continuous Research Factory remains active because no S05 PASS Candidate exists.

## 2. Frozen research path

Strategy #3 followed:

`family sourcing → IDEA-0003 → HYP-0003 → Data Feasibility → frozen development dataset → frozen PROTO-01 → one development reveal`

Prototype identity:

`HYP-0003 / PROTO-01`

Canonical machine result:

`reports/research/HYP-0003-PROTOTYPE-01-result.json`

Machine result SHA-256:

`a1feee3d6495afdcc46f81ce0ee8e137896a77a3bd52de8baf6cbf53da1a7620`

Reveal commit:

`f974b9bb60a6cc295cb8aaba4a263499c14769c0`

Frozen runner Git blob:

`d65746f39476ba3fee8cf59acfd0b2f82af9c663`

No runner, dataset, grid or decision-rule change occurred between RF-010 freeze and RF-011 reveal.

## 3. Result

Decision:

`REJECT — ONE_OR_MORE_BROAD_REGION_CRITERIA_FAILED`

The frozen broad-region rule required all three conditions to pass.

| Criterion | Result | Decision |
|---|---:|---|
| median of 25 cell mean returns > 0 | `-0.0013404354655954772` | FAIL |
| positive-mean cells >= 13 / 25 | `8 / 25` | FAIL |
| positive formation span >= 3 / 5 | `4 / 5` | PASS |
| positive holding span >= 3 / 5 | `4 / 5` | PASS |

All `25 / 25` declared cells were retained and had valid observations.

The two failed breadth conditions are sufficient to reject HYP-0003. Passing span conditions and individual positive cells do not rescue the claim.

## 4. Surface facts retained without winner selection

The result contains positive-mean cells across four formation periods and four holding periods, but only eight cells are positive in total.

The full surface is retained rather than selecting a post-hoc best cell.

The 12-month formation row is negative across all five holding periods.

Observation counts range from `166` to `180` per cell.

For holding periods above one month, overlapping forward windows are generally extreme, commonly near `99%`. Those dependent observations remain visible rather than being treated as independent evidence.

## 5. Evidence classification and economic boundary

Evidence class:

`EXPLORATORY_PROTOTYPE`

Economic label:

`QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING`

Known limitations remain:

- commission is not modeled;
- financing/rollover is not modeled and is material for multi-month holds;
- H1 quote opens are not guaranteed live fills;
- multi-month forward windows are strongly overlapping;
- development evidence is not validation or independent-examination evidence.

The rejection is therefore a Research Funnel stop decision, not a claim about every possible implementation of currency momentum.

## 6. Search and iteration accounting

For this research line:

- declared development variants: `25`;
- variants retained in terminal result: `25 / 25`;
- prototype reveals used for the decision: `1`;
- development dataset changes after RF-009 freeze: `0`;
- runner changes after RF-010 freeze: `0`;
- post-reveal parameter/grid changes: `0`;
- reveal reruns used for decision: `0`;
- protected-tail reveal inside HYP-0003: `0`.

The negative result remains part of the program research-freedom history.

## 7. Research decision

Cheap Prototype protocol defines `REJECT` as sufficient negative preliminary evidence to stop a line before Economic Pre-Screen.

Therefore HYP-0003 does **not** enter:

- R4 Economic Pre-Screen;
- Candidate Promotion;
- S01–S05 Candidate research;
- M4.9/M4.10 strategy-specific validation;
- M5 execution/live engineering.

No Candidate, Strategy Version, formal Experiment or live permission is created from HYP-0003.

The pre-written positive-route action `CREATE_NEW_CONFIRMATORY_HYPOTHESIS_BEFORE_R4` is not reached.

## 8. Reuse and methodology learnings

### L1 — The Research Factory handled a cross-sectional multi-asset profile

Strategy #3 required synchronized point-in-time multi-currency data, direct/inverse quote normalization, deterministic universe eligibility, basket construction and side-aware execution.

The platform and governance flow supported that materially different profile through R3 without requiring live/execution architecture.

### L2 — Breadth rules prevented best-cell rescue

Eight cells had positive mean returns, but the pre-written claim required at least 13 positive cells plus a positive median surface.

The methodology therefore prevented a few favorable cells from being promoted as if the broad-region hypothesis had passed.

### L3 — Full-denominator retention matters

All `25 / 25` declared variants are preserved in the canonical result.

No unfavorable cell was hidden, removed or relabeled after reveal.

### L4 — Dependence is material for multi-month horizons

Most holding periods beyond one month have approximately 98–99% overlap between consecutive forward windows.

Raw monthly observation counts therefore cannot be interpreted as independent sample sizes.

### L5 — Economic interpretation remains limited

Spread is represented through BID/ASK sides, but financing/rollover and commission are not modeled.

Even the favorable cells are not full-net profitability evidence.

### L6 — Protected data remained protected

HYP-0003 ended on the development block. The reserved tail beginning `2021-09-01T00:00:00Z` was not used to rescue the rejected claim.

## 9. Next Research Factory step

Strategy #3 terminates at R3.

The next research task is:

`ATS2-RF-013 — Strategy #4 idea sourcing`

Strategy #4 must be sourced as a new research line. It must not:

- rename one of the eight positive HYP-0003 cells as a successful strategy;
- retune HYP-0003 and present the retuned version as the original result;
- use the protected HYP-0003 tail to rescue the rejected claim;
- reuse `HYP-0003` for a materially changed formulation.

A materially new claim requires a new Idea/Hypothesis identity and normal Research Factory accounting.

## 10. Safety boundary

This closeout does not authorize:

- demo/shadow trading;
- real-money trading;
- broker/account selection;
- capital allocation;
- leverage;
- scaling.

All live/capital permissions remain false.

## 11. Closeout decision

Strategy #3 / HYP-0003:

`REJECTED_AT_R3`

Closeout decision:

`PASS — NEGATIVE_EVIDENCE_PRESERVED_WITHOUT_RESCUE`

After exact-head OWNER launcher PASS, `ATS2-RF-013 — Strategy #4 idea sourcing` becomes the active Research Factory task.
