# ATS Data Feasibility Review

**Task:** `ATS2-M1-003`  
**Work package:** `WBS-1.3`  
**Status:** BASELINE  
**Purpose:** decide whether available or obtainable data can honestly test a concrete Hypothesis before Cheap Prototype work begins.

## 1. Scope

Data Feasibility Review starts only for a registered Hypothesis whose decision is `DATA_FEASIBILITY` and whose status is `READY_FOR_DATA_FEASIBILITY`.

The review answers a narrower question than research or validation:

> Can ATS represent the information state, observations, timing, coverage and cost inputs required to test this Hypothesis without known fatal bias or leakage?

It does not establish that the Hypothesis is true. It does not authorize formal validation, live execution or capital allocation.

Flow:

`Hypothesis READY_FOR_DATA_FEASIBILITY → Data review → FEASIBLE / CONDITIONAL / PARK / REJECT → Cheap Prototype only when permitted`

## 2. Canonical review artifact

Reusable template:

`governance/methodology/templates/DATA_FEASIBILITY_TEMPLATE.md`

For a real Hypothesis, the review instance is stored under:

`research/reviews/HYP-xxxx-DATA_FEASIBILITY.md`

Rules:

1. The review references exactly one primary `HYP-xxxx`.
2. A review may reference several source candidates or dataset snapshots.
3. Unknown provider, exact history length or exact cost value is recorded as unknown until verified; it is not invented.
4. The review is a research record and remains in history after `PARK` or `REJECT`.
5. A later material change to the Hypothesis requires a new review for the new Hypothesis ID.

## 3. Minimum review inputs

Before a decision, the review must contain or explicitly mark unknown for:

- Hypothesis ID;
- Hypothesis statement summary;
- required information/data categories;
- candidate source types or actual sources if known;
- accessibility and licensing constraints;
- temporal coverage;
- cross-sectional/universe coverage where relevant;
- granularity and required fields;
- timezone and market-calendar assumptions;
- timestamp semantics;
- decision-time information availability;
- revision/restatement/correction behaviour;
- corporate-action handling where relevant;
- missing/bad data behaviour;
- universe membership and survivorship risks;
- selection and sampling risks;
- leakage/overlap risks;
- transformation and dataset-identity plan;
- cost/execution inputs needed for the early test;
- known gaps;
- impact of each material gap;
- feasibility decision and reason.

## 4. Source availability

A source is usable only if ATS can explain what information it provides and how that information can be obtained reproducibly enough for the proposed research stage.

Possible source categories include exchange/vendor feeds, broker history, public data, event feeds, filings, reference data, internally derived data or another explicit source class.

The program does not select one universal vendor in M1.

For a real review, `FEASIBLE` requires evidence that the needed source actually exists and is accessible under the intended research conditions. A source that is merely assumed to exist cannot support `FEASIBLE`.

If access is plausible but not yet verified, the review may be `CONDITIONAL` or `PARK` depending on whether the uncertainty blocks the next cheap test.

## 5. Coverage

Coverage is evaluated against the concrete Hypothesis, not against a universal number of years or observations.

The review records, as applicable:

- first/last available timestamp;
- continuity and known gaps;
- event or observation count;
- relevant market regimes;
- instrument/universe breadth;
- historical constituent membership;
- delisted/expired instruments;
- known changes in data-generation methodology.

Insufficient coverage may lead to `CONDITIONAL`, `PARK` or `REJECT` depending on whether the claim can still be answered honestly.

Raw observation count alone is not enough; dependence and effective diversity matter later in research/validation.

## 6. Granularity and field semantics

Data must be at least as precise as the Hypothesis requires.

The review records:

- bar/tick/event/reference-data granularity;
- price or quote field semantics;
- bid/ask versus midpoint/last where relevant;
- volume/open-interest semantics where relevant;
- event fields and identifiers;
- whether aggregation could destroy or fabricate the claimed timing/effect.

A Hypothesis requiring sub-minute reaction cannot be declared feasible using daily bars merely because daily data are easy to obtain.

## 7. Timestamp semantics and timezone

Every time-sensitive source must have explicit timestamp semantics.

The review distinguishes where applicable:

- event occurrence time;
- publication/release time;
- first machine-available time;
- exchange timestamp;
- broker/vendor receive timestamp;
- bar open/close/end timestamp;
- revision/correction timestamp;
- local timezone versus UTC;
- daylight-saving transitions;
- trading-session/calendar boundaries.

A timestamp whose meaning is unknown is a material gap, not a cosmetic metadata issue.

## 8. Decision-time information availability

The review must answer:

> Could the strategy or research decision have known this value at the historical decision timestamp?

Point-in-time availability is required whenever later revisions, delayed publication, finalized constituents, corrected events or retrospective labels could leak future information.

Examples of unacceptable hidden future information include:

- revised macroeconomic values used as if they were the first release;
- today’s index constituents projected backward;
- adjusted fundamentals before their publication date;
- event classifications assigned using later information;
- future bar values included in features at the decision timestamp.

If the historical information state cannot be reconstructed sufficiently for the claim, the review must narrow the claim through a new Hypothesis or reject the line; it cannot silently assume point-in-time correctness.

## 9. Revisions, restatements and corrections

For revisable data, record:

- whether vintages exist;
- whether the source overwrites history;
- whether first-release and final values can be distinguished;
- restatement/correction frequency if known;
- how a prototype will avoid using later revisions unintentionally.

For event/news research, publication, update and correction timestamps are separate concepts when the source exposes them.

For corporate/fundamental data, effective date and publication date are not interchangeable.

## 10. Corporate actions and instrument lifecycle

Where applicable, record treatment of:

- splits;
- dividends;
- symbol changes;
- contract rolls;
- delistings;
- mergers;
- expired instruments;
- trading halts;
- changes in tick size or contract specification.

Adjusted price history may be useful, but the adjustment method must not introduce information unavailable at the historical timestamp for the intended test.

## 11. Missing and bad data

The review defines how the prototype will recognize and handle:

- missing observations;
- duplicate timestamps;
- out-of-order records;
- impossible/obviously bad values;
- stale quotes or stale reference values;
- feed outages;
- missing events;
- partial universe coverage.

The default rule is not to fill missing values silently.

Forward filling, interpolation, deletion or substitution is permitted only when the transformation is explicit and does not manufacture information or alter the Hypothesis unnoticed.

## 12. Universe, survivorship and selection bias

For cross-sectional or multi-instrument research, the review asks whether the historical universe is known as of each timestamp.

Risks include:

- using only instruments that survive to the present;
- excluding delisted or failed entities;
- selecting markets after observing performance;
- filtering securities with future-known liquidity/capitalization;
- historical membership reconstructed from current membership.

If the Hypothesis claims a universe-level effect, current-universe-only data normally cannot support an unrestricted historical claim.

## 13. Leakage and overlap

The review identifies ways future or neighbouring information could leak into the early test, including:

- forward-looking transformations;
- centered windows;
- labels overlapping feature windows;
- future-known normalization statistics;
- event windows that cross evaluation boundaries;
- cross-sectional data built from future constituent knowledge;
- duplicated information from the same underlying event.

Detailed purging/embargo rules belong to later protocol when applicable, but obvious leakage must be blocked before prototype work.

## 14. Transformation trace and dataset identity

Prototype data must be traceable from source to research input.

The review defines the minimum identity plan appropriate to the stage, which may include:

- source name/type;
- acquisition date;
- source query/export parameters;
- coverage;
- timezone/timestamp semantics;
- transformation steps;
- code revision used for transformation;
- file/object identity or checksum where available;
- future `DATA-...` Dataset ID once dataset-manifest tooling exists.

M1 does not require the full M2 data platform, but it does require enough traceability that a positive prototype cannot depend on an unidentifiable data snapshot.

## 15. Cost and execution inputs

Data feasibility includes the information needed to estimate economically relevant costs for the cheap test.

Depending on the Hypothesis this may include:

- spread or bid/ask data;
- commission schedule;
- financing/swap assumptions;
- slippage proxy;
- contract size/tick value;
- trading-session restrictions;
- event latency or execution delay assumptions.

Exact live costs are not required at this stage. An early conservative approximation may be acceptable if the review records its limitation.

If the claimed effect is smaller than data resolution or cannot be distinguished from likely costs even approximately, this is a material feasibility/economic warning.

## 16. Licensing, access and retention

The review records known constraints that affect reproducibility:

- redistribution restrictions;
- API/export limits;
- retention windows;
- paid access requirements;
- whether raw data may be stored in Git;
- whether only a manifest/reference can be committed.

Secrets, credentials and non-redistributable raw data are not committed to the repository.

## 17. Known gaps

Every material uncertainty is listed explicitly with:

- gap description;
- affected part of the Hypothesis/test;
- whether it can bias direction or magnitude;
- whether it blocks the cheap test;
- proposed mitigation or required evidence.

A review with unknown material timestamp semantics, unknown survivorship state or another potentially fatal gap cannot be marked `FEASIBLE` merely to keep the research line moving.

## 18. Decision model

### `FEASIBLE`

Meaning: the required information can be represented with sufficient honesty for the planned cheap test, and no known unresolved gap invalidates the information-time premise.

Effect: `ATS2-M1-004` Cheap Prototype may use the review constraints.

### `CONDITIONAL`

Meaning: a cheap test is possible only under explicit constraints or approximations that are recorded in the review.

Effect: Cheap Prototype may proceed only if every blocking condition for that prototype is resolved or encoded as a declared limitation. The prototype conclusion must not generalize beyond those constraints.

If satisfying the condition materially changes Statement, Market, Condition, Horizon, Direction or information-time premise, create a new Hypothesis instead of silently changing the existing one.

### `PARK`

Meaning: the Hypothesis remains coherent, but an external/data-access gap currently prevents an honest useful test.

Effect: no prototype until the block changes and the review is updated/reperformed.

### `REJECT`

Meaning: the required historical information state cannot be represented well enough to test the Hypothesis as stated, or the available data necessarily introduce a fatal bias that cannot be mitigated without changing the Hypothesis.

Effect: no prototype for this Hypothesis. The review is retained with the rejection reason.

## 19. Review status model

Allowed review statuses:

`DRAFT → FEASIBLE`  
`DRAFT → CONDITIONAL`  
`DRAFT → PARKED`  
`DRAFT → REJECTED`

A later re-review does not erase the earlier decision. If source availability changes without changing the Hypothesis, the review may be updated with dated decision history or a new review artifact according to future registry rules.

## 20. Decision authority

Routine Data Feasibility decisions may be made by DATA / RESEARCH under this methodology because they create no real market exposure.

OWNER approval is not required for `FEASIBLE`, `CONDITIONAL`, `PARK` or `REJECT` at this stage.

OWNER rights remain reserved for capital policy, Strategy Risk Mandate, live admission, allocation, scaling and profit withdrawal.

## 21. Structural acceptance test

`DATA_FEASIBILITY_TEMPLATE.md` is tested against this model without selecting a fictitious vendor, instrument, dataset or Hypothesis.

The template must represent:

- Hypothesis linkage;
- source/access review;
- coverage/granularity;
- timestamp and information-time semantics;
- revisions/corrections;
- corporate-action/instrument lifecycle where applicable;
- missing/bad data policy;
- universe/survivorship/selection risks;
- leakage/overlap risks;
- transformation trace/dataset identity;
- cost/execution inputs;
- licensing/access constraints;
- known gaps;
- one explicit feasibility decision and reason.

No source availability, coverage, vendor, cost value or market fact is invented by this structural test.

## 22. Definition of Done for an individual Data Feasibility Review

A real review is complete when:

- the reviewed Hypothesis is identified;
- required data categories are mapped to actual or verified-plausible sources;
- coverage/granularity and timestamp semantics are recorded;
- decision-time information availability is evaluated;
- revision, missing/bad-data, universe/survivorship and leakage risks are assessed where applicable;
- transformation/dataset identity plan is explicit;
- relevant cost/execution inputs are identified;
- material gaps and their effect are recorded;
- one decision among `FEASIBLE / CONDITIONAL / PARK / REJECT` is recorded with reason;
- the decision does not silently alter the Hypothesis.

## 23. M1-003 completion result

This process plus `DATA_FEASIBILITY_TEMPLATE.md` satisfies `WBS-1.3`.

Next dependent work:

`ATS2-M1-004 — Cheap Prototype protocol`.

That step defines how to answer one early quantitative question at minimum cost without confusing exploratory/prototype output with formal validation evidence.