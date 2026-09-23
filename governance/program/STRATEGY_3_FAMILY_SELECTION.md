# Strategy #3 Family Selection

**Task:** `ATS2-RF-003`  
**Program lane:** `RESEARCH_FACTORY_CONTINUOUS / WBS-RF.1`  
**Decision:** `SELECT`  
**Date:** 23 September 2026

## 1. Selected family

`S3-FAM-02 — CROSS_SECTIONAL_CURRENCY_MOMENTUM`

The selected family asks whether currencies with stronger past relative performance continue to outperform weaker peers over a later horizon under executable cost assumptions.

This task selects a research family only. It does not claim that the effect is profitable or validated.

## 2. Why this family is admitted

The selection is based on research-process value rather than reported headline returns.

### Distinct mechanism

Strategy #1 was a single-instrument trend/breakout line.

Strategy #2 was a single-instrument two-sided reversal line.

Strategy #3 uses a cross-sectional relative-performance mechanism across a currency universe. It therefore tests a materially different research profile.

### Plausible data path

Historical FX BID/ASK data are available for multiple instruments from established market-data sources.

The exact source, currency universe, coverage and synchronization policy are **not** selected here. They must be reviewed under HYP-0003 Data Feasibility before any confirmatory evidence is used.

### Cheap falsification path

A development-stage prototype can rank a bounded currency universe by past relative return and test subsequent winner-minus-loser or side-specific executable returns under explicit costs.

This can be done before portfolio/live infrastructure is built.

### Platform value

The family tests whether ATS research tooling can move from a single ordered price stream to synchronized multi-instrument observations and cross-sectional ranking.

Any platform extension must remain demand-driven and minimal.

## 3. Literature provenance

The family is motivated by the empirical currency-momentum literature, including Menkhoff, Sarno, Schmeling & Schrimpf, *Currency Momentum Strategies*.

The literature reports cross-sectional momentum effects and also emphasizes transaction costs and limits to arbitrage.

The publication is provenance for a testable research family, not evidence that an ATS implementation has edge.

## 4. Why the other shortlisted families are not selected now

### S3-FAM-01 — Macroeconomic announcement response

Retained for future sourcing.

It is materially distinct and research-relevant, but honest directional surprise research requires reliable publication-time data and, where surprise is used, an expectations/consensus path with explicit timestamp and revision semantics.

That data path is less certain than the selected family at current program maturity.

### S3-FAM-03 — Intraday time/session effect

Retained for future sourcing.

It has a relatively cheap data path, but it exercises less new platform behavior because it remains a single-stream price/clock conditioning problem. It may also produce statistically visible effects that are economically weak after spread and costs.

No claim is made that either unselected family is inferior or unprofitable.

## 5. Research-freedom boundary

The selected family has substantial degrees of freedom:

- currency-universe construction;
- return normalization;
- lookback horizon;
- holding/rebalance horizon;
- ranking or bucket rule;
- long/short or side-specific construction;
- cost/execution treatment.

Therefore RF-003 deliberately selects **none** of those parameters.

HYP-0003 must define a bounded development search or a pre-motivated fixed formulation before material testing.

Development parameter tuning is allowed, but all materially inspected variants must remain visible in research accounting.

## 6. Evidence boundary

No prior Strategy #1 or Strategy #2 result is reused as proof for this family.

No previously revealed block becomes independent evidence merely because a new Idea ID is created.

Any future confirmatory block must be frozen before it is used for the corresponding decision.

## 7. Idea intake

Canonical Idea:

`research/ideas/IDEA-0003.md`

Intake decision:

`SCREEN`

Resulting status:

`SCREENING`

The next research step is HYP-0003 formation. That Hypothesis must specify the measurable cross-sectional claim and the bounded development-parameter policy without selecting parameters post hoc from confirmatory data.

## 8. Safety boundary

This selection does not authorize demo/shadow trading, real-money trading, broker/account selection, capital allocation, leverage, Strategy Risk Mandate or scaling.
