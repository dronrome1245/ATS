# ATS Hypothesis Model

**Task:** `ATS2-M1-002`  
**Work package:** `WBS-1.2`  
**Status:** BASELINE  
**Purpose:** convert a screened Idea into a falsifiable research claim before data selection or quantitative testing.

## 1. Scope

The Hypothesis Model covers the transition from an Idea with intake decision `SCREEN` to a registered Hypothesis that is precise enough to enter Data Feasibility review.

It does not establish that an edge exists. It does not authorize backtesting, prototype work, validation, live execution or capital allocation by itself.

Flow:

`Idea SCREEN → Hypothesis DRAFT → Falsifiability check → DATA_FEASIBILITY / PARK / REJECT`

## 2. Idea and Hypothesis are different objects

An Idea says that a market behaviour or potential source of edge may be worth investigating.

A Hypothesis states what should be observable, why it may occur, where and when it should occur, what information is assumed available at decision time, and what observation would count against the claim.

One screened Idea may produce more than one Hypothesis when materially different mechanisms, conditions, horizons or expected effects need separate tests. These Hypotheses receive separate IDs and remain linked to the same parent Idea.

Idea screening is not evidence for a Hypothesis.

## 3. Canonical location and identity

Registered Hypotheses live under:

`research/hypotheses/HYP-xxxx.md`

ID format:

`HYP-0001`, `HYP-0002`, and so on.

Rules:

1. Hypothesis ID is unique program-wide.
2. An ID is never reused after rejection, parking or supersede.
3. The next ID is the lowest unused positive sequence number above the highest ID already registered in `research/hypotheses/`.
4. Every Hypothesis must reference a real parent `Idea ID`.
5. Renaming a Hypothesis does not change its ID.
6. A material reformulation after the Hypothesis has left `DRAFT` creates a new Hypothesis ID and records the superseded ID.

The repository does not pre-create empty files to reserve IDs.

## 4. Eligibility to create a Hypothesis

A Hypothesis may be created only when the parent Idea:

- exists in `research/ideas/`;
- has intake decision `SCREEN`;
- has enough context to state an observable effect;
- is not merely a duplicate of an existing active research line without a material distinction.

A parked or rejected Idea does not automatically produce a Hypothesis. It must first return through the Idea intake process and receive a new recorded `SCREEN` decision.

## 5. Minimum Hypothesis fields

Before a Hypothesis can receive a decision, it must contain or explicitly mark unknown where allowed:

- stable Hypothesis ID;
- Parent Idea ID;
- creation date;
- status;
- supersedes/lineage reference when applicable;
- falsifiable Statement;
- proposed Mechanism;
- Market / asset class and instrument or universe if known;
- Conditions under which the claim applies;
- decision/effect Horizon;
- expected Direction or form of effect;
- decision-time information premise;
- explicit Falsification criteria;
- Required data categories;
- timestamp/information-timing requirements;
- cost/execution inputs that may matter;
- Known biases and leakage risks;
- one planned cheap research question;
- decision and decision reason.

Unknown facts remain `null` or are stated as unknown. Unknown data vendor, exact history length, exact cost value or exact sample size is acceptable before Data Feasibility. The kind of data and timing semantics needed to test the claim must still be identifiable.

## 6. Falsifiability admission rule

A Hypothesis is falsifiable enough to proceed only when all of the following are true:

1. **Observable claim:** the statement predicts an observable difference, relationship, response or distributional property.
2. **Defined context:** the market, condition and horizon are specific enough that observations can later be classified as relevant or not relevant.
3. **Direction or shape:** the expected effect has a direction, sign, ordering or other testable form.
4. **Information-time premise:** the claim does not silently use information unavailable at the historical decision timestamp.
5. **Failure path:** the card states what result would count as evidence against the claim or force a new Hypothesis.
6. **Non-tautology:** the statement is not true by definition and is not merely a restatement of a future-selected profitable parameter set.
7. **Research question:** the planned cheap test asks a limited question about the claim rather than “find the best parameters”.

A Hypothesis does not need a universal numeric significance threshold at this stage. Statistical decision rules belong to the later registered experiment/validation protocol appropriate to the research class.

## 7. Mechanism discipline

The Mechanism explains why the effect might exist. It may be economic, behavioural, structural, event-driven or microstructure-based.

The mechanism may be uncertain, but it must be distinguishable from the observed result itself. “The backtest is profitable” is not a mechanism.

If the same Idea supports two materially different mechanisms, create separate Hypotheses rather than combining them into one unfalsifiable claim.

## 8. Conditions, horizon and information set

The Hypothesis must state:

- when the claim is expected to apply;
- when it explicitly makes no prediction;
- the decision horizon;
- the expected effect or holding horizon;
- what information is assumed available at the decision timestamp.

This prevents later Data Feasibility or prototype work from changing the market regime, timing or horizon only because a different formulation produces a better historical result.

## 9. Falsification

Falsification criteria should be written before the relevant quantitative result is known.

They may describe:

- no observable effect in the stated direction;
- effect disappears once decision-time timing is enforced;
- effect exists only under data leakage or an unavailable information state;
- effect is dominated by required transaction costs under the stated premise;
- mechanism predicts one condition but the observed relationship systematically appears elsewhere;
- evidence is too sparse or dependent to answer the claim with the available data.

A failed Hypothesis is retained. It is not rewritten after the fact into the claim that would have matched the result.

## 10. Decision model

### `DATA_FEASIBILITY`

Meaning: the Hypothesis is sufficiently falsifiable and specified to evaluate whether the required data can honestly test it.

Resulting status: `READY_FOR_DATA_FEASIBILITY`.

This decision is not evidence of edge and does not authorize a prototype until Data Feasibility is completed.

### `PARK`

Meaning: the Hypothesis is coherent but should not consume the next unit of research effort.

Typical reasons include unresolved context, unavailable prerequisite information, low priority or an external dependency.

Resulting status: `PARKED`.

### `REJECT`

Meaning: the Hypothesis should not proceed in its current form.

Typical reasons include non-falsifiability, circular statement, dependence on unavailable future information, contradiction with the parent Idea premise, or inability to define an observable failure condition.

Resulting status: `REJECTED`.

Rejected and parked Hypotheses are retained.

## 11. Status model

Allowed statuses at this stage:

`DRAFT → READY_FOR_DATA_FEASIBILITY`

or holding/terminal branches:

`DRAFT → PARKED`  
`DRAFT → REJECTED`

A Hypothesis that is replaced after leaving `DRAFT` may be marked `SUPERSEDED` while the replacement receives a new `HYP-xxxx` ID.

## 12. Material reformulation and change control

While status is `DRAFT` and no downstream review or experiment has relied on the card, wording may be clarified in place.

After the Hypothesis has received `DATA_FEASIBILITY`, or after downstream work has used it, a change is material if it changes any of:

- core Statement;
- Mechanism;
- Market/universe;
- Conditions;
- Horizon;
- expected Direction/form;
- information-time premise;
- Falsification rule.

A material change creates a new Hypothesis ID. The old object remains in history and the new object records `Supersedes Hypothesis ID`.

Corrections that do not change the research claim, such as spelling or link repair, may remain under the same ID.

## 13. Required data is a question, not a vendor choice

At Hypothesis stage, required data identifies what information must exist to test the claim, for example price/quote data, event timestamps, fundamentals, cross-sectional membership or cost inputs.

The Hypothesis does not need to select a vendor or prove coverage. Those questions belong to `ATS2-M1-003 — Data Feasibility review`.

Timestamp semantics and information availability must nevertheless be stated whenever they could change the truth of the claim.

## 14. Cheap-test handoff

The `Planned cheap test` field defines one limited research question that could weaken or support continuing the research line.

It is not yet an experiment authorization. Data Feasibility must first establish that the needed information can be represented without obvious leakage or missing-timestamp problems.

Prototype rules are defined later by `ATS2-M1-004`.

## 15. Decision authority

Routine Hypothesis formation and classification may be performed by RESEARCH under this methodology.

OWNER approval is not required because no capital or real exposure is created.

OWNER rights remain reserved for program capital policy, Strategy Risk Mandate, live admission, allocation, scaling and profit withdrawal.

## 16. Template usage

Canonical template:

`governance/methodology/templates/HYPOTHESIS_TEMPLATE.md`

Procedure:

1. Confirm that the parent Idea exists and has a recorded `SCREEN` decision.
2. Check whether an existing Hypothesis already represents the same claim.
3. Assign the next stable `HYP-xxxx` ID only for a real research claim.
4. Record Parent Idea ID and lineage.
5. Write Statement and Mechanism separately.
6. Define market context, conditions, horizons, expected direction and decision-time information premise.
7. Write Falsification before downstream quantitative evidence is observed.
8. Identify required data categories, timing semantics, relevant cost/execution inputs and known bias risks.
9. Define one limited cheap research question.
10. Record exactly one decision: `DATA_FEASIBILITY`, `PARK` or `REJECT`.
11. Set status consistently with the decision.
12. If `DATA_FEASIBILITY`, hand off to M1 Data Feasibility review.

## 17. Negative history

- `PARK`, `REJECT` and `SUPERSEDED` records are retained.
- A failed formulation is not deleted when a new formulation is created.
- Multiple Hypotheses from one Idea are acceptable when they are materially distinct and separately identifiable.
- External claims and source reputation remain provenance, not evidence of edge.

## 18. Structural acceptance test

`HYPOTHESIS_TEMPLATE.md` is tested against this model without creating a fictitious Hypothesis.

| Requirement | Template field | Result |
|---|---|---|
| stable identity | `Hypothesis ID`, `Created on`, `Status` | PASS |
| parent linkage | `Parent Idea ID` | PASS |
| lineage | `Supersedes Hypothesis ID` | PASS |
| falsifiable claim | `Statement` | PASS |
| mechanism | `Mechanism` | PASS |
| context | `Market`, `Conditions` | PASS |
| horizon | `Horizon` | PASS |
| expected effect | `Expected direction` | PASS |
| information timing | `Decision-time information premise` | PASS |
| falsification | `Falsification` | PASS |
| data need | `Required data` | PASS |
| bias risks | `Known biases and leakage risks` | PASS |
| cheap question | `Planned cheap test` | PASS |
| decision | `Status decision` | PASS |

No market, instrument, return, broker, capital value or fictitious Hypothesis is created by this acceptance test.

## 19. Definition of Done for an individual Hypothesis

An individual Hypothesis formation is complete when:

- stable identity and parent Idea linkage exist;
- the claim passes the falsifiability admission rule or is explicitly parked/rejected;
- Statement and Mechanism are separated;
- context, horizons, expected direction and information-time premise are recorded;
- Falsification is explicit;
- required data and known biases are recorded;
- one decision and reason are recorded;
- status matches the decision;
- negative or superseded history is retained.

## 20. M1-002 completion result

This model plus the aligned `HYPOTHESIS_TEMPLATE.md` satisfies `WBS-1.2`.

Next dependent work:

`ATS2-M1-003 — Data Feasibility review`.

That step must determine whether the required data actually exist with usable coverage, timestamp semantics and bias controls before prototype work begins.