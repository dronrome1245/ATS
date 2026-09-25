# Strategy #4 Family Selection

**Task:** `ATS2-RF-014`  
**Program lane:** `RESEARCH_FACTORY_CONTINUOUS / WBS-RF.1`  
**Decision:** `SELECT`  
**Date:** 25 September 2026

## 1. Selected family

`S4-FAM-03 — INTRADAY_TIME_SESSION_EFFECT`

This family asks whether a predeclared UTC/session condition changes subsequent quote-executable FX return or volatility distributions relative to a matching unconditional baseline.

This task selects a research family for Idea Intake only. It does not claim that an intraday/session effect is profitable, persistent, economically material or validated.

## 2. Why this family is admitted now

The selection is based on mechanism clarity, falsifiability, data-path readiness and cheapest useful test value rather than reported historical headline returns.

### Distinct mechanism

Strategies #1–#3 tested trend/breakout, return-tail reversal and cross-sectional currency momentum.

Strategy #4 instead tests recurring clock-time liquidity/activity structure. The explanatory mechanism is therefore materially different from the previously rejected research lines.

### Reproducible data path

ATS already has experience acquiring and normalizing granular FX BID/ASK histories with explicit timestamps and gap handling.

The exact instrument or universe, provider snapshot, bar granularity, UTC/session definition, DST policy and coverage are **not** selected here. They must be fixed later under HYP-0004 and Data Feasibility.

Unlike announcement-surprise research, this family does not require a point-in-time consensus-history dataset for the first useful test. Unlike carry and PPP/value research, the first useful test does not require a new rate/forward or macro-vintage data stack.

### Cheap falsification path

A bounded prototype can compare a small predeclared set of clock/session conditions with a matching unconditional baseline using side-aware quotes, spread diagnostics and explicit dependence handling.

The prototype can fail quickly if any apparent clock pattern is unstable, non-directional, spread-dominated or concentrated in a few periods.

### Research-freedom burden

Clock/session research can create many degrees of freedom if arbitrary buckets are inspected. For that reason RF-014 selects no session boundary, weekday filter, instrument, horizon, threshold or directional rule.

HYP-0004 must bound those choices before material performance inspection.

### Platform value

The family exercises timestamp, UTC/session, DST, holiday/weekend and liquidity/spread semantics while reusing the existing research stack. Any additional capability must remain demand-driven and minimal.

## 3. Why the other immediate-shortlist families are not selected now

### S4-FAM-01 — Currency carry / interest-rate differential

Retained for future sourcing.

The mechanism is distinct and falsifiable, but an honest first test requires point-in-time rate/forward or swap inputs, tenor/settlement conventions and explicit financing economics that ATS has not yet established as a reproducible acquisition path.

### S4-FAM-02 — Macroeconomic announcement response

Retained for future sourcing.

The mechanism is research-relevant, but directional surprise testing requires exact release timestamps and, where surprise is used, reliable point-in-time expectation/consensus history with revision and vintage semantics.

### S4-FAM-04 — Currency value / PPP / REER

Retained for future sourcing.

The mechanism is distinct, but point-in-time macro vintages, long horizons and a low number of effectively independent observations make the cheapest useful first test materially heavier.

No claim is made that any unselected family is inferior, unprofitable or permanently rejected.

## 4. Research-freedom boundary

RF-014 deliberately does **not** select:

- instrument or currency universe;
- provider or dataset snapshot;
- bar granularity;
- UTC/session boundaries;
- DST or holiday policy;
- weekday filters;
- return versus volatility target;
- directional sign;
- holding/evaluation horizon;
- spread/liquidity threshold;
- cost assumptions beyond requiring explicit applicability;
- development grid or pass/fail rule.

Those choices belong to HYP-0004 formation and later Data Feasibility.

Materially inspected alternatives must remain visible in research accounting.

## 5. Evidence boundary

The RF-013 literature record motivates a testable family only.

No published return, previously revealed ATS dataset, positive HYP-0003 cell or prior rejected strategy is evidence that S4-FAM-03 has edge.

A later Hypothesis must preserve a new Idea/Hypothesis lineage and must freeze its material claim before prototype outcome reveal.

## 6. Idea Intake

Canonical Idea:

`research/ideas/IDEA-0004.md`

Intake decision:

`SCREEN`

Resulting status:

`SCREENING`

The SCREEN decision means only that one bounded next research step is justified.

## 7. Next research step

`ATS2-RF-015 — HYP-0004 formation`

HYP-0004 must turn the intraday/session family into one falsifiable claim and explicitly bound the clock/session definition, target variable, horizon, market/instrument scope, information time and development-search policy before material testing.

## 8. Safety boundary

This selection does not authorize demo/shadow trading, real-money trading, broker/account selection, capital allocation, leverage, Strategy Risk Mandate or scaling.
