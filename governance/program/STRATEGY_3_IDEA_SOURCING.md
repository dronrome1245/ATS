# Strategy #3 Idea Sourcing

**Task:** `ATS2-RF-002`  
**Program lane:** `RESEARCH_FACTORY_CONTINUOUS / WBS-RF.1`  
**Status:** SOURCING_SHORTLIST_READY  
**Date:** 23 September 2026

## 1. Purpose

This task builds a bounded shortlist of materially different research directions for Strategy #3.

It does **not** select a winning strategy, create `IDEA-0003`, choose an instrument/timeframe/provider, or claim profitability.

The next task will compare the shortlisted families against mechanism clarity, data feasibility, cheap-test feasibility, research freedom and platform value before one Idea is admitted.

## 2. Boundary from prior research

Closed lines:

- Strategy #1: trend/breakout family — rejected at R3;
- Strategy #2: two-sided return-tail reversal family — rejected at R3.

Strategy #3 sourcing must not rescue either failed Hypothesis by changing parameters after the fact.

A new material claim requires a new Idea/Hypothesis lineage.

## 3. Development optimization rule

Parameter tuning is allowed **before** confirmatory freeze.

For Strategy #3 research, development work may include:

- a bounded parameter grid;
- multiple reasonable feature definitions;
- alternative horizons;
- alternative thresholds;
- explicit sensitivity checks;
- elimination of clearly weak variants.

But all materially inspected variants must be retained in research/search accounting.

The development phase must not report only the best configuration as though it were the only one tested.

Before any confirmatory run, ATS must freeze:

- the selected formulation;
- parameter values or selection rule;
- dataset/evidence boundary;
- cost/execution approximation;
- primary metrics;
- decision rule.

After a confirmatory block is revealed, that block is known evidence. It may later be used as development data for a **new** Hypothesis, but it cannot remain independent evidence for the same claim after tuning to it.

## 4. Sourcing method

The shortlist is literature-informed and architecture-aware.

Selection is not based on headline historical returns from papers.

Each family is evaluated only for:

- whether there is a falsifiable mechanism;
- whether ATS can plausibly obtain honest data;
- whether a cheap prototype is possible;
- whether it adds a materially different research profile;
- whether research freedom can be bounded.

No family is ranked or selected in this task.

## 5. Shortlisted research families

### S3-FAM-01 — Macroeconomic announcement response

**Mechanism class:** event-driven information arrival.

Research basis:

- Andersen & Bollerslev documented strong intraday FX activity patterns and macroeconomic announcement effects.
- Hashimoto & Ito found that several Japanese macroeconomic releases had measurable short-horizon effects on USD/JPY returns, activity and volatility.

Potential research question class:

> Does a predeclared category of scheduled macroeconomic surprise produce a directional or volatility response that survives realistic timestamp and spread handling?

Distinctive requirements:

- official publication timestamp;
- release value and, if used, expectation/consensus timestamp;
- revision policy;
- timezone/DST handling;
- high-resolution market data around events;
- event clustering rules.

Why it is materially different:

This is event-driven rather than a pure rolling-price pattern. It would test ATS event timestamp semantics and potentially justify new data capabilities only if Data Feasibility passes.

Main risk:

Consensus/surprise data may be difficult or expensive to source reproducibly. No feasibility assumption is made yet.

### S3-FAM-02 — Cross-sectional currency momentum

**Mechanism class:** relative performance across a currency universe.

Research basis:

- Menkhoff, Sarno, Schmeling & Schrimpf documented cross-sectional currency momentum and emphasized transaction-cost and limits-to-arbitrage considerations.
- Later research has continued to examine currency momentum through dispersion, factor and order-flow lenses.

Potential research question class:

> Do currencies with stronger past relative returns continue to outperform weaker peers over a predeclared future horizon after executable cost assumptions?

Distinctive requirements:

- multi-instrument universe;
- synchronized timestamps;
- return comparability across currencies;
- explicit base-currency and excess-return conventions;
- cross-sectional ranking rules;
- portfolio/rebalancing semantics;
- transaction-cost treatment.

Why it is materially different:

This is a multi-instrument relative-value profile, unlike both prior single-instrument hypotheses. It would test whether the existing research platform generalizes beyond one price stream.

Main risk:

Universe construction and many parameter choices create substantial research freedom and selection bias if not tightly bounded.

### S3-FAM-03 — Intraday time/session effect

**Mechanism class:** recurring time-of-day liquidity/activity structure.

Research basis:

- high-frequency FX research documents pronounced intraday activity/volatility patterns and systematic timing around market activity and announcements.

Potential research question class:

> Does a predeclared time-of-day/session condition change the distribution of subsequent executable returns or volatility relative to an unconditional baseline?

Distinctive requirements:

- precise timezone/DST/session semantics;
- sufficiently granular quote data;
- stable market-hour definition;
- explicit handling of weekends/holidays;
- multiple-year regime coverage.

Why it is materially different:

The conditioning variable is clock/session state rather than prior return direction. It is still price/quote-driven but tests time semantics more directly.

Main risk:

A time-of-day pattern may be statistically visible but not economically exploitable after spread, costs and dependence.

## 6. Research-relevant family not shortlisted for immediate Idea intake

### Order-flow prediction

BIS research shows that customer/order flow can contain information about future exchange rates.

This family is research-relevant, but ATS does not currently have a reproducible order-flow dataset or a confirmed acquisition path.

Therefore it is retained as a future sourcing possibility rather than entering the immediate Strategy #3 shortlist.

This is a data-feasibility boundary, not a claim that order-flow strategies do or do not work.

## 7. Source record

Primary literature used for sourcing:

1. Andersen, T. G. & Bollerslev, T. — *DM-Dollar Volatility: Intraday Activity Patterns, Macroeconomic Announcements, and Longer Run Dependencies*, NBER Working Paper 5783 / Journal of Finance.
2. Hashimoto, Y. & Ito, T. — *Effects of Japanese Macroeconomic Announcements on the Dollar/Yen Exchange Rate: High-Resolution Picture*, NBER Working Paper 15020.
3. Menkhoff, L., Sarno, L., Schmeling, M. & Schrimpf, A. — *Currency Momentum Strategies*, CEPR/BIS working-paper lineage.
4. Menkhoff, L., Sarno, L., Schmeling, M. & Schrimpf, A. — *Information flows in foreign exchange markets: dissecting customer currency trades*, BIS Working Paper 405.

These sources motivate research families only. They are not evidence that an ATS implementation has edge.

## 8. Shortlist accounting

Families reviewed for this task: `4`.

Immediate shortlist for Strategy #3 Idea selection: `3`.

Retained but not immediately shortlisted due unresolved data acquisition:

`1` — order-flow prediction.

No family is ranked.

No strategy parameter has been selected.

No market/instrument/timeframe/provider has been selected.

## 9. Next decision

After exact-head OWNER launcher PASS:

`ATS2-RF-003 — Strategy #3 family selection and Idea intake`

RF-003 must choose at most one family for `IDEA-0003`, or explicitly park all three if data/mechanism review does not justify admission.

The selection must state why the chosen family is worth a new Research Funnel attempt without claiming that it is profitable.
