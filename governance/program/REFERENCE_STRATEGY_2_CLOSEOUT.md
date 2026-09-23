# Reference Strategy #2 Early-Rejection Closeout

**Task:** `ATS2-M6-008`  
**Work package:** `WBS-6.7 (early-rejection reuse-review path)`  
**Strategy line:** Reference Strategy #2 / `HYP-0002`  
**Research outcome:** `REJECTED_AT_R3`  
**Status:** READY_FOR_OWNER_CLOSURE  
**Date:** 23 September 2026

## 1. Purpose

This closeout preserves the terminal Cheap Prototype result for Reference Strategy #2, records reusable Research Factory/platform learnings, and prevents an unfavorable two-sided result from being rescued by post-result parameter changes.

This is **not** an M6 milestone exit decision. M6 remains `IN_PROGRESS` until the program makes a separate continuation/exit decision after this line is closed.

## 2. Frozen research path

Reference Strategy #2 followed:

`bounded discovery → IDEA-0002 → HYP-0002 → Data Feasibility → frozen PROTO-01 → one confirmatory reveal`

Discovery history:

- 16 declared alternatives were evaluated;
- 5 reversal alternatives were shortlisted;
- no exact discovery cell was declared a winner;
- HYP-0002 was formulated post-discovery;
- development thresholds and a disjoint 2026 confirmatory block were frozen before reveal.

Prototype identity:

`HYP-0002 / PROTO-01`

Canonical machine result:

`reports/research/HYP-0002-PROTOTYPE-01-result.json`

Machine result SHA-256:

`cf89ae89680aad25d24944dc737c4092f995327dca022a7c6a19d7ea102e552e`

Reveal commit:

`96d7b90ac908cacccfefbccbe8daa06867b2f18c`

## 3. Result

Decision:

`REJECT — ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED`

The frozen two-sided claim required both tail directions to satisfy both primary inequalities.

### High-tail / DOWN side

- events: `201`;
- mean signed return: `0.0004902837195506912`;
- unconditional DOWN mean: `0.00008491191847673248`;
- mean minus baseline: `0.00040537180107395865`;
- median signed return: `0.00042826912095672576`;
- positive share: `0.5472636815920398`;
- overlapping windows: `185 / 201`;
- overlap share: `0.9203980099502488`.

This side satisfied both primary inequalities.

### Low-tail / UP side

- events: `122`;
- mean signed return: `-0.0002984301044940726`;
- unconditional UP mean: `-0.00015076510581675065`;
- mean minus baseline: `-0.00014766499867732195`;
- median signed return: `0.00002652818004655888`;
- positive share: `0.5`;
- overlapping windows: `110 / 122`;
- overlap share: `0.9016393442622951`.

This side failed both primary inequalities.

Because HYP-0002 is explicitly two-sided, the passing high-tail/DOWN side cannot silently replace the failed low-tail/UP side.

## 4. Evidence classification and economic boundary

Evidence class:

`EXPLORATORY_PROTOTYPE`

Economic label:

`QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING`

Known limitations remain:

- commission is not modeled;
- financing/rollover is not modeled;
- 1H quote opens are not guaranteed live fills;
- forward windows are highly overlapping and dependent;
- this result is not validation or independent-examination evidence.

The rejection is therefore a Research Funnel stop decision, not a statement about live trading performance.

## 5. Search and iteration accounting

For this research line:

- bounded discovery alternatives inspected before HYP-0002: `16`;
- shortlisted discovery alternatives: `5`;
- HYP-0002 confirmatory prototype iterations executed: `1`;
- confirmatory dataset changes after freeze: `0`;
- threshold/horizon/direction changes after reveal: `0`;
- confirmatory reruns used for decision: `0`.

The negative result remains visible in history.

## 6. Research decision

Cheap Prototype protocol defines `REJECT` as sufficient negative preliminary information to stop the line before Economic Pre-Screen.

Therefore Reference Strategy #2 does **not** enter:

- R4 Economic Pre-Screen;
- Candidate Promotion;
- S01–S05 Candidate research;
- M4.9/M4.10 strategy-specific validation;
- M5 execution/live engineering.

No Candidate, Strategy Version, formal Experiment or live permission is created from HYP-0002.

## 7. Reuse and platform learnings

### L1 — Research Factory rejected a second distinct profile without rescue

Strategy #1 was a long/flat trend-breakout profile. Strategy #2 was a two-sided return-tail reversal profile.

Both were stopped at R3 under rules fixed before their terminal prototype results. The shared Research Funnel therefore supports at least two materially different price-driven profiles through early falsification without requiring strategy-specific production architecture.

### L2 — Discovery and confirmatory evidence remained separated

The 2021–2025 development/discovery block was not reused as the confirmatory block. Development thresholds were frozen before the 2026 reveal.

This is a reusable control for future post-discovery hypotheses.

### L3 — Two-sided claims must remain genuinely two-sided

One side passed while the other failed. The methodology correctly prevented the passing side from becoming a post-hoc replacement hypothesis.

Any future one-sided claim requires a new Hypothesis ID and new Data Feasibility/research accounting.

### L4 — Observation dependence is material

Overlap was approximately 92% for high-tail/DOWN events and 90% for low-tail/UP events.

Raw event counts therefore materially overstate independent information. The reusable M4 dependence/concentration tooling remains relevant if a future line reaches formal validation.

### L5 — Local CI controls improved during the line

The line exposed recurrent formatting, lint and import-context failures. Durable controls now include:

- pinned Ruff lint and format as separate gates;
- fast pytest collection/import verification;
- complete validator marker audits;
- narrow runtime-output ignore patterns;
- exact state/handoff/backlog reconciliation.

These are platform/process learnings, not evidence for HYP-0002.

## 8. WBS consequence

Reference Strategy #2 terminated inside `WBS-6.2 — Run Research Funnel`.

Therefore for this line:

- `WBS-6.3`–`WBS-6.6`: NOT ENTERED;
- `WBS-6.8`: NOT ENTERED;
- `WBS-6.7`: executed through an explicit early-rejection reuse-review path to retain generalization learnings.

The WBS-6.7 dependency is updated to allow either a completed WBS-6.6 path or a terminal Research Funnel rejection.

## 9. Safety boundary

This closeout does not authorize:

- demo/shadow trading;
- real-money trading;
- Candidate or Strategy creation for HYP-0002;
- broker/account selection;
- capital allocation;
- leverage;
- scaling.

All live/capital permissions remain false.

## 10. Closeout decision

Reference Strategy #2 research line:

`REJECTED_AT_R3`

Closeout decision:

`PASS — NEGATIVE_EVIDENCE_PRESERVED_WITHOUT_RESCUE`

M6 milestone status remains:

`IN_PROGRESS`

After exact-head OWNER launcher PASS, the next program decision should determine whether M6 exits on its two-profile generalization objective or is rebaselined to source another strategy because no S05 PASS Candidate yet exists.
