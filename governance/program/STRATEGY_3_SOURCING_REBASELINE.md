# Strategy #3 Sourcing Rebaseline

**Task:** `ATS2-RF-001`  
**Program lane:** `RESEARCH_FACTORY_CONTINUOUS`  
**Status:** BASELINE_PENDING_OWNER_CLOSURE  
**Date:** 23 September 2026

## 1. Purpose

M6 proved that ATS can apply the same Research Factory discipline to two materially different price-driven strategy profiles and preserve negative evidence honestly.

Both reference strategy lines were rejected at R3:

- Reference Strategy #1 — trend/breakout;
- Reference Strategy #2 — two-sided return-tail reversal.

No S05 PASS Candidate exists.

This rebaseline converts strategy sourcing from a one-off reference milestone into a continuous Research Factory lane and defines the next search as Strategy #3 without inventing its market, instrument, timeframe, provider, parameters or expected return.

## 2. Boundary after M6

M6 is closed as:

`M6_REFERENCE_STRATEGY_2 = COMPLETED / PASS`

This means the two-profile Research Factory/platform-generalization objective was met.

It does **not** mean:

- either reference strategy succeeded;
- a Candidate exists;
- M4.9/M4.10 may start;
- M5 may start;
- any live/capital permission exists.

Candidate count remains:

`0`

## 3. Continuous Research Factory lane

After M6, ATS uses a repeatable sourcing lane rather than creating a new milestone for every rejected idea.

### `WBS-RF.0 — Sourcing rebaseline`

Purpose: define sourcing scope, evidence boundaries and task sequence before Strategy #3 selection.

### `WBS-RF.1 — Strategy #3 idea sourcing`

Purpose: source one or more bounded candidate ideas through explicit Idea Intake and/or bounded development-data discovery.

Rules:

- retain the complete search denominator when systematic discovery is used;
- retain negative/discarded alternatives;
- do not call a discovered pattern a strategy edge;
- do not reuse HYP-0001 or HYP-0002 IDs;
- do not select a market/instrument/timeframe merely because data are already convenient.

### `WBS-RF.2 — Research Funnel`

Purpose: take one admitted new Idea through a new Hypothesis, Data Feasibility and Cheap Prototype under the existing M1 methodology.

A materially new claim receives a new `HYP-xxxx`.

### `WBS-RF.3 — Economic screen / Candidate path`

Purpose: only a prototype that advances under its pre-written rule may enter Economic Pre-Screen and Candidate promotion.

No Candidate is created merely because Strategy #1 and #2 were rejected.

### `WBS-RF.4 — S05 and validation handoff`

Purpose: when a future promoted Candidate honestly reaches S05 PASS, hand it to the already-built M4.9/M4.10 validation path.

Until then:

`M4.9 = BLOCKED_PENDING_S05_CANDIDATE`

## 4. Strategy #3 sourcing principles

Strategy #3 should test a credible new source of edge rather than tune either rejected Hypothesis.

Preferred sourcing properties:

- materially distinct mechanism or condition from the two rejected lines;
- a falsifiable claim;
- data/timestamp semantics that can be represented honestly;
- a cheap R3 test before expensive implementation;
- explicit search accounting.

A different strategy class is useful when evidence supports it, but diversity is not a reason to invent data needs or choose a class without a research basis.

## 5. Data/evidence boundary

Known historical blocks may be used only according to their declared evidence status.

Rules:

1. no previously revealed block is silently relabeled as independent evidence;
2. future discovery use of known data must be declared development/exploratory use;
3. a new Hypothesis must define its own Data Feasibility and evidence partition before confirmatory use;
4. protected validation/independent evidence remains protected when such a block is later defined;
5. search history from Strategy #1 and Strategy #2 remains part of program-level multiple-research accounting.

## 6. Platform boundary

No new shared capability is built merely in anticipation of Strategy #3.

The demand-driven rule remains:

`Strategy need → Minimum capability → Reuse opportunity → Shared capability → Hardening`

Existing capabilities are reused where they fit. New data feeds, Strategy API extensions, event/news support or execution assumptions require a concrete Strategy #3 need.

## 7. Safety boundary

This rebaseline does not authorize:

- demo/shadow trading;
- real-money trading;
- broker/account selection;
- Strategy Risk Mandate;
- capital allocation;
- leverage;
- scaling.

All live/capital permissions remain false.

## 8. Next task after closure

After exact-head OWNER launcher PASS for this rebaseline:

`ATS2-RF-002 — Strategy #3 idea sourcing`

That task may use bounded discovery and/or explicit Idea Intake, but it must not preselect the result in this rebaseline.
