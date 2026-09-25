# Strategy #4 Idea Sourcing

**Task:** `ATS2-RF-013`  
**Program lane:** `RESEARCH_FACTORY_CONTINUOUS / WBS-RF.1`  
**Status:** `SOURCING_SHORTLIST_READY`  
**Date:** 25 September 2026

## 1. Purpose

This task builds a bounded shortlist of materially different research families for Strategy #4 after three independent Research Funnel lines were rejected at R3.

It does **not** select a winning family, create `IDEA-0004`, choose a final market/instrument/timeframe/provider, set strategy parameters, or claim profitability.

RF-014 will compare the immediate shortlist and may select at most one family for Idea Intake, or park all of them.

## 2. Boundary from prior research

Closed lines:

- Strategy #1 — single-instrument trend/breakout — `SREJECTED_AT_R3`;
- Strategy #2 — two-sided return-tail reversal — `SREJECTED_AT_R3`;
- Strategy #3 — cross-sectional currency momentum — `SREJECTED_AT_R3`.

Strategy #4 sourcing must not rescue any rejected line by changing parameters or by selecting only favorable historical cells after the fact.

In particular, the eight positive HYP-0003 development cells remain negative-history context and are not Strategy #4 candidates.

A materially new claim requires a new Idea/Hypothesis lineage.

## 3. Sourcing method

The shortlist is literature-informed and data-path-aware.

Families are reviewed for:

- mechanism clarity;
- falsifiability;
- point-in-time data representability;
- cheapest useful R3 test;
- research-freedom burden;
- dependence/cost risks;
- incremental platform value.

Reported historical returns from publications are not used as ATS evidence.

No family is ranked.

No family is selected.

## 4. Immediate shortlist

### S4-FAM-01 — Currency carry / interest-rate differential

**Mechanism class:** compensation associated with cross-currency interest-rate / forward differentials and their risk premia.

Research basis:

- classic carry-trade research studies borrowing lower-yield currencies and holding higher-yield currencies;
- the literature also documents crash/liquidity risk and sensitivity to volatility;
- recent BIS work continues to treat leveraged carry positions as economically relevant to exchange-rate responses around monetary-policy changes.

Potential research question class:

> Does a predeclared cross-currency carry signal predict subsequent quote-executable excess returns strongly enough to justify a new Hypothesis after explicitly representing financing, forward points and crash-risk diagnostics?

Distinctive data requirements:

- point-in-time short-rate, deposit, OIS or forward-point information;
- synchronized FX spot/forward or swap observations;
- explicit tenor and settlement conventions;
- financing/rollover treatment;
- availability timestamps for rate/forward inputs;
- cross-currency quote normalization.

X�y materially different:

The conditioning variable is an interest-rate/forward differential rather than prior price trend, return tails or momentum rank.

Main risks:

- carry returns can be exposed to crash/unwind states;
- policy-rate proxies may not equal executable funding/forward economics;
- cross-currency basis and tenor conventions can make naive rate-differential implementations economically misleading.

### S4-FAM-02 — Macroeconomic announcement response

**Mechanism class:** scheduled information arrival / price discovery.

Research basis:

High-frequency FX studies document pronounced responses around scheduled macroeconomic news, including conditional mean jumps when released values differ from expectations.

Potential research question class:

> Does one predeclared category of scheduled macroeconomic surprise produce a directional or volatility response that survives exact release-time, revision and spread handling?

Distinctive data requirements:

- official release timestamp;
- released value;
- point-in-time expectation/consensus if surprise is used;
- revision/vintage policy;
- timezone and DST handling;
- high-resolution quote data around events;
- event-clustering rules.

Why materially different:

The signal is external scheduled information rather than an endogenous rolling-price feature.

Main risks:

Reliable point-in-time consensus/expectation histories may be expensive or difficult to source reproducibly. A release-only design may test volatility response but cannot silently substitute for a directional surprise claim.

### S4-FAM-03 — Intraday time/session effect

**Mechanism class:** recurring clock-time liquidity/activity structure.

Research basis:

High-frequency FX literature documents strong intraday activity and volatility patterns that coexist with announcement effects and longer-run volatility dependence.

Potential research question class:

> Does a predeclared UTC/session condition change subsequent quote-executable return or volatility distributions relative to a matching unconditional baseline?

Distinctive data requirements:

- precise UTC/session definition;
- DST policy;
- weekend/holiday handling;
- granular BID/ASK quotes;
- multi-year regime coverage;
- explicit spread/liquidity diagnostics.

Why materially different:

The conditioning variable is time/session state rather than trend, reversal, relative rank or macro valuation.

Main risks:

A stable volatility pattern may exist without a tradable directional edge. Multiple clock buckets and session definitions create selection risk if not bounded before testing.

### S4-FAM-04 — Currency value / PPP / real-exchange-rate deviation

**Mechanism class:** slow mean reversion toward a macroeconomic valuation anchor.

Research basis:

Purchasing-power-parity and real-exchange-rate research treats deviations from relative price fundamentals as persistent but potentially mean-reverting over long horizons. BIS real effective exchange-rate datasets provide a standardized macro valuation context.

Potential research question class:

> Do currencies that are predeclared as materially cheap or expensive relative to a point-in-time real-value anchor subsequently mean-revert after realistic carry/financing and horizon treatment?

Distinctive data requirements:

- point-in-time CPI/price-level or REER data;
- publication/vintage timestamps;
- exchange rates;
- consistent country/currency mappings;
- long historical coverage;
- financing/carry treatment across long holding periods.

Why materially different:

The signal is a slow macro valuation gap rather than short-horizon technical price behavior.

Main risks:

PPP deviations can persist for long periods, leaving few independent observations. Revised macro data can create leakage unless vintages are represented honestly.

## 5. Research-relevant family not immediately shortlisted

### S4-FAM-05 — Customer/order-flow prediction

**Mechanism class:** heterogeneous information and dealer/customer flow.

Research basis:

BIS research using customer FX order-flow data reports that flows contain information about future exchange rates and that predictive content differs materially across customer groups.

Potential research question class:

> Does a point-in-time order-flow imbalance from a predeclared participant class predict subsequent executable FX returns?

Why not immediately shortlisted:

ATS does not currently have a reproducible customer/dealer order-flow dataset or a confirmed acquisition path with the required participant classification and timestamps.

This is a data-access block, not a claim that the mechanism is weak.

## 6. Source record

Research-family provenance used for RF-013:

1. Banerjee, Boneva, Pinter & Sushko — (Monetary policy transmission to exchange rates: the role of currency carry trades*, BIS Bulletin 124, 2026.
2. Burnside, Eichenbaum, Kleshchelski & Rebelo — *Do Peso Problems Explain the Returns to the Carry Trade?*, NBER Working Paper 14054.
3. Brunnermeier, Nagel & Pedersen — *Carry Trades and Currency Crashes*, NBER Working Paper 14473.
4. Andersen & Bollerslev — *DM-Dollar Volatility: Intraday Activity Patterns, Macroeconomic Announcements, and Longer Run Dependencies*, NBER Working Paper 5783.
5. Andersen, Bollerslev, Diebold & Vega — *Micro Effects of Macro Announcements: Real-Time Price Discovery in Foreign Exchange*, NBER Working Paper 8959.
6. Chernov & Creal — *Multihorizon Currency Returns and Purchasing Power Parity*, NBER Working Paper 24563.
7. Menkhoff, Sarno, Schmeling & Schrimpf — *Information flows in foreign exchange markets: dissecting customer currency trades*, BIS Working Paper 405.
8. BIS Data Portal — Bilateral exchange rates and effective-exchange-rate methodology/data context.

These publications motivate falsifiable research families only. They are not evidence that an ATS implementation has edge.

## 7. Shortlist accounting

Families reviewed: `5.

Immediate shortlist for RF-014 family selection: `4`.

Immediate shortlisted families:

- `S4-FAM-01 — CURRENCY_CARRY_INTEREST_RATE_DIFFERENTIAL`;
- `S4-FAM-02 — MACROECONOMIC_ANNOUNCEMENT_RESPONSE`;
- `S4-FAM-03 — INTRADY_TIME_SESSION_EFFECT`;
- `S4-FAM-04 — CURRENCY_VALUE_PPP_REER`.

Retained but not immediately shortlisted due unresolved data acquisition:

- `S4-FAM-05 — CUSTOMER_ORDER_FLOW_PREDICTION`.

No family is ranked.

No family is selected.

No strategy parameter is selected.

No market/instrument/timeframe/provider is selected for an admitted Idea.

## 8. Research-freedom boundary

RF-014 must not select a family because one publication reports the largest historical return.

For any selected family, the next Idea/Hypothesis stages must explicitly bound the material degrees of freedom, including where relevant:

- universe/instrument;
- signal definition;
- lookback or economic tenor;
- holding horizon;
- threshold/bucket definition;
- event category;
- session/time bucket;
- valuation anchor;
- cost/financing convention;
- data vintage and information time.

All materially inspected alternatives remain part of program research accounting.

## 9. Next decision

After exact-head OWNER launcher PASS:

`ATS2-RF-014 — Strategy #4 family selection and Idea intake`

RF-014 may select at most one immediate-shortlist family for `IDEA-0004`, or explicitly park all four if mechanism/data review does not justify admission.

A `SCREEN` decision at Idea Intake will mean only that the next small research step is justified. It will not be evidence of edge.

## 10. Safety boundary

RF-013 does not authorize demo/shadow trading, real-money trading, broker/account selection, capital allocation, leverage, Strategy Risk Mandate or scaling.
