# RF-039 Existing Hypothesis Disposition

**Status:** PROPOSED GOVERNANCE DECISION  
**Scope:** `HYP-0001` through `HYP-0007`  
**Purpose:** map existing research lines into the new portfolio / signal-to-strategy methodology without rewriting historical evidence.

## 1. Non-retroactivity rule

RF-039 does not alter any historical result, frozen rule, consumed evidence block or prior decision.

Existing Hypothesis cards and result artifacts remain historical source records even when their old status field is stale relative to later reviews.

This document only defines the recommended **next action** under the revised methodology.

No market outcome is computed by RF-039.

## 2. HYP-0001 — EUR/USD 1H 24-Bar Upward Breakout Continuation

Historical outcome:

- `PROTO-01 = REJECT`;
- 1006 valid signals;
- both primary mean-return inequalities failed;
- no blocking implementation anomaly.

Disposition:

`CLOSE_NEGATIVE / DO_NOT_RETEST_IN_PLACE`

Rules:

- do not change the 24-bar lookback/horizon inside HYP-0001;
- do not rerun HYP-0001 on another period as a rescue attempt;
- any materially different breakout concept must enter the preliminary portfolio as a new PH proposal and cite HYP-0001 as prior negative lineage.

## 3. HYP-0002 — EUR/USD Two-Sided 24H Return-Tail Reversal

Historical outcome:

- `PROTO-01 = REJECT`;
- high-tail/DOWN side passed;
- low-tail/UP side failed;
- the registered two-sided claim therefore failed;
- prior 16-alternative discovery is part of selection history.

Disposition:

`CLOSE_NEGATIVE / RETAIN_POST_SELECTION_INFORMATION`

Rules:

- do not rewrite HYP-0002 into the passing one-sided tail;
- a future one-sided extreme-return proposal is allowed only as a new PH item with explicit post-selection lineage and elevated multiplicity/selection burden;
- no direct Candidate path from the favorable high-tail subset.

## 4. HYP-0003 — Cross-Sectional Currency Momentum Development Region

Historical outcome:

- complete `25 / 25` bounded grid was evaluated;
- broad positive-region claim failed;
- only `8 / 25` cells had positive mean return;
- the median cell mean was negative.

Disposition:

`CLOSE_NEGATIVE / RETAIN_AS_RESEARCH_FAMILY_HISTORY`

Rules:

- do not select one favorable cell from the rejected grid and treat it as prespecified evidence;
- HYP-0003 becomes an explicit example of one bounded parameter family in Multiple Research Accounting;
- materially different momentum research must enter the future portfolio with its own family definition.

## 5. HYP-0004 — Fixed-UTC Intraday Activity Contrast

Historical outcome:

- structural development PASS;
- CORE_ACTIVE had higher median next-hour absolute movement than OFF_HOURS;
- CORE_ACTIVE had no wider median quoted relative spread;
- no directional trading rule or P&L was defined.

Disposition:

`STRUCTURAL_REFERENCE / POSSIBLE_REGIME_FILTER`

Rules:

- HYP-0004 itself is complete;
- do not perform further HYP-0004 structural replication;
- its result may be cited as development provenance for a new directional trading proposal;
- using session/activity as a regime filter in a new strategy creates a new PH/Hypothesis lineage and does not convert HYP-0004 into alpha.

## 6. HYP-0005 — Confirmatory Fixed-UTC Activity Contrast

Main-branch boundary at RF-039 branch creation:

- `main` contains RF-037 one-shot reveal authorization;
- post-reveal preservation/review is being handled separately by open RF-038 / PR #57;
- RF-039 must not execute, repeat or reconstruct the HYP-0005 reveal.

Disposition:

`DO_NOT_RERUN / WAIT_FOR_RF038_CANONICALIZATION`

After RF-038 is canonically closed, use this routing regardless of the technical preservation task:

- if the preserved valid first reveal is the documented structural PASS, classify HYP-0005 as `CONFIRMATORY_STRUCTURAL_REFERENCE` and stop structural replication;
- if RF-038 discovers an integrity defect, resolve the integrity state without performing a second first reveal.

No direct R4/Candidate path is authorized from a non-directional activity contrast.

## 7. HYP-0006 — U.S. CPI Release Immediate Activity Contrast

Historical outcome already revealed in ATS lineage:

- structural post-release absolute movement exceeded pre-release movement on the development event inventory;
- result is non-directional;
- coincident official releases limit CPI-specific causal attribution;
- quoted spread diagnostics are not executable round-trip cost.

Disposition:

`STRUCTURAL_REFERENCE / NO_DIRECT_TRADING_ROLE`

Rules:

- do not interpret greater post-release volatility as directional alpha;
- do not calculate strategy P&L from HYP-0006 itself;
- trading use requires a separate directional information source or a separately defined post-release observable market-state rule.

## 8. HYP-0007 — Confirmatory CPI 60m Activity Contrast

Current role:

- confirmatory structural replication of HYP-0006;
- no directional sign;
- no profitability claim;
- requires a new genuinely unseen event block.

RF-039 value-of-information assessment:

A positive or negative HYP-0007 structural result does not currently determine a concrete trading action because no directional/executable trading rule has been defined.

Disposition:

`PARK_BEFORE_CONFIRMATORY_DATA_CONSUMPTION`

Rules:

- do not acquire/reveal a protected independent block for HYP-0007 merely to continue the structural chain;
- retain the registered card and all provenance;
- reactivation requires a new portfolio decision documenting the concrete downstream decision that HYP-0007 would change;
- if reactivated, its frozen structural claim remains unchanged; no result-driven reformulation is allowed.

## 9. Portfolio consequences

Existing HYP-0001 through HYP-0007 do not automatically occupy slots in the new preliminary portfolio because they already exist as historical research objects.

Their legacy information affects new proposal ranking:

- avoid retesting HYP-0001/HYP-0002/HYP-0003 formulations;
- HYP-0004/HYP-0005 may support a session/regime-filter proposal, not direct alpha;
- HYP-0006 may support CPI/event research context, not direction;
- HYP-0007 should remain parked unless its confirmatory answer becomes decision-relevant.

## 10. Effective next research action

After RF-039 methodology is accepted, ATS should **not immediately start HYP-0007 or invent HYP-0008**.

The next research action is:

`REVIEW_AND_APPROVE_PRELIMINARY_HYPOTHESIS_PORTFOLIO`

Only approved PH proposals may subsequently proceed through lineage / Idea Intake / Hypothesis formation and Data Feasibility.
