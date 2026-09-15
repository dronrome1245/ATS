# ATS Idea Intake Process

**Task:** `ATS2-M1-001`  
**Work package:** `WBS-1.1`  
**Status:** BASELINE  
**Purpose:** operationalize entry into the ATS Research Funnel without inventing a strategy, market, broker or capital assumption.

## 1. Scope

Idea Intake covers the transition from an informal observation to a registered `Idea` that can enter structured screening and, if retained, proceed to Hypothesis formation.

It does not establish that an edge exists. It does not authorize prototype, validation, live execution or capital allocation by itself.

Flow:

`Observation → Idea DRAFT → Intake check → SCREEN / PARK / REJECT → Hypothesis formation if SCREEN`

## 2. Observation, Idea and Hypothesis

### Observation

An unregistered note, pattern, question, external claim or market behaviour. It may be incomplete and has no program status.

### Idea

A registered research object with a stable ID, enough context to understand what is being proposed, the minimum data need, a plausible rationale, a cheapest useful test and known false-inference risks.

An Idea may still be wrong, vague in mechanism or impossible to test economically. Registration preserves the proposal; it does not endorse it.

### Hypothesis

A later object created only after Idea screening. It converts the retained Idea into a falsifiable statement with mechanism, conditions, expected effect and falsification path. Hypothesis rules are defined by `ATS2-M1-002`.

## 3. Canonical location and ID

Registered Ideas live under:

`research/ideas/IDEA-xxxx.md`

ID format:

`IDEA-0001`, `IDEA-0002`, and so on.

Rules:

1. ID is unique program-wide.
2. An ID is never reused after rejection, parking, deletion request or supersede.
3. The next ID is the lowest unused positive sequence number above the highest ID already registered in `research/ideas/`.
4. Renaming an Idea does not change its ID.
5. A duplicate proposal receives its own ID only if there is a material difference in market, mechanism, condition, horizon or proposed test. Otherwise the new observation is linked to the existing Idea.

The repository does not pre-create empty Idea files to reserve numbers.

## 4. Who may submit an Idea

An Idea may originate from OWNER, RESEARCH, DATA, DEVELOPMENT, VALIDATION, an external publication, market observation or prior experiment.

The registered card records provenance but does not treat source reputation as evidence of edge.

An AI agent may structure an Idea supplied by a user or derived from an explicit research source. It must not invent a trading idea merely to populate the pipeline or satisfy a process test.

## 5. Minimum intake fields

Before an Idea can receive an intake decision, the card must contain or explicitly mark unknown for:

- stable Idea ID;
- creation date;
- origin/provenance;
- observation;
- proposed market or asset-class context;
- proposed instrument/universe if known;
- horizon if known;
- preliminary rationale;
- expected observable effect;
- required data;
- cheapest useful test;
- known false-inference risks;
- duplicate/overlap check;
- intake decision and decision reason.

Unknown facts remain `null` or are stated as unknown. Missing market, instrument or horizon is not automatically rejection if the observation is still worth formalizing, but excessive ambiguity may result in `PARK` until the missing context can be supplied.

## 6. Intake quality rules

An Idea is suitable for screening only when all of the following are true:

1. **Research scope:** it concerns a potentially testable source of market behaviour, execution effect, relative relationship, event response or another mechanism relevant to ATS.
2. **Non-circular rationale:** rationale is more than “the backtest made money” or “the chart looks good”.
3. **Observable consequence:** there is some outcome that could later be measured.
4. **Data path:** required data can at least be named, even if availability is not yet confirmed.
5. **Cheap falsification path:** there is a plausible early test that could kill or materially weaken the Idea without production engineering.
6. **Known obvious biases:** the card identifies obvious risks such as leakage, survivorship, timestamp ambiguity, selection bias, multiple testing, sparse events or costs when relevant.
7. **No forbidden assumption:** intake does not require invented capital, broker, jurisdiction, risk limit or live infrastructure choice.

Intake deliberately does not require proof of profitability, statistical significance, complete data, production architecture or a finalized strategy specification.

## 7. Duplicate and overlap check

Before assigning a new ID, compare the proposed Idea against existing `research/ideas/` objects.

Possible result:

- `NEW` — materially distinct Idea;
- `RELATED` — create a new Idea and link related IDs because a meaningful dimension differs;
- `DUPLICATE` — do not create a second Idea; append provenance/reference to the existing Idea through normal change control.

Similarity of indicator names alone does not make two Ideas duplicates. The relevant comparison is mechanism + condition + market + horizon + proposed test.

## 8. Screening decisions

### `SCREEN`

Meaning: the Idea is sufficiently specified to proceed to Hypothesis formation.

`SCREEN` is not a PASS on edge or economics. It means only “worth spending the next small unit of research effort”.

Resulting Idea status: `SCREENING`.

### `PARK`

Meaning: the Idea is preserved but should not consume active research capacity now.

Typical reasons:

- data requirement is currently impractical;
- observation lacks enough context to formulate a useful Hypothesis;
- similar active work has higher priority;
- expected operational complexity appears disproportionate but is not yet enough for rejection;
- external dependency is unavailable.

Resulting Idea status: `PARKED`.

A parked Idea may return to screening when the recorded block changes. The prior decision remains in history.

### `REJECT`

Meaning: there is already a sufficient reason not to continue this research line.

Typical reasons:

- claim is not falsifiable even after reasonable clarification;
- mechanism depends on information unavailable at decision time;
- effect is obviously non-executable under its own premise;
- proposal duplicates an existing Idea without a material distinction;
- required data cannot in principle represent the claimed information state;
- proposed mechanism violates program safety rules such as martingale/rescue logic.

Resulting Idea status: `REJECTED`.

Rejected Ideas are retained and remain searchable. Rejection reason must not be deleted to make a later similar proposal look new.

## 9. Status model

Allowed Idea statuses in M1 intake:

`DRAFT → SCREENING`

or terminal/holding branches:

`DRAFT → PARKED`  
`DRAFT → REJECTED`

A future process may add later lifecycle states, but M1-001 does not overload the Idea object with Prototype or Candidate status.

## 10. Decision authority

Routine intake classification may be performed by RESEARCH under the canonical methodology.

OWNER approval is not required to register, screen, park or reject a research Idea because no real exposure is created.

OWNER decision rights remain required for capital policy, Strategy Risk Mandate, live admission, allocation and scaling.

## 11. Template usage

Canonical template:

`governance/methodology/templates/IDEA_TEMPLATE.md`

Procedure:

1. Check for duplicates/related Ideas.
2. Copy the template into `research/ideas/IDEA-xxxx.md` only for a real submitted Idea.
3. Assign the stable ID and creation date.
4. Record provenance.
5. Fill known facts; retain `null` for facts not yet known.
6. Complete observation, rationale, expected effect, data need, cheapest useful test and false-inference risks.
7. Record duplicate-check result.
8. Record exactly one intake decision: `SCREEN`, `PARK` or `REJECT`.
9. Record the reason and resulting status.
10. If `SCREEN`, proceed to the Hypothesis process once `ATS2-M1-002` is available.

## 12. Negative evidence and history

Idea files are research records.

- `PARK` and `REJECT` are not deleted.
- Later reconsideration does not erase the earlier decision.
- A materially changed proposal may become a new Idea with a new ID and explicit relation to the old one.
- Source claims, screenshots or external articles are provenance, not formal evidence by themselves.

## 13. Work-in-progress discipline

Idea Intake is intentionally cheap. Registration should not trigger platform development, data acquisition contracts, optimization or production implementation.

The next expensive action is permitted only when the current research stage requires it and its dependencies are satisfied.

## 14. Structural acceptance test of the template

`IDEA_TEMPLATE.md` was tested against this process without creating a fictitious Idea.

The acceptance test checks whether one template instance can represent all required intake information:

| Requirement | Template field | Result |
|---|---|---|
| stable identity | `Idea ID`, `Created on`, `Status` | PASS |
| provenance | `Origin / provenance` | PASS |
| observation | `Observation` | PASS |
| market/horizon context | `Proposed market context` | PASS |
| rationale | `Preliminary rationale` | PASS |
| observable effect | `Expected effect` | PASS |
| data need | `Required data` | PASS |
| cheap early test | `Cheapest useful test` | PASS |
| false-inference risks | `Known risks of false inference` | PASS |
| duplicate check | `Duplicate / overlap check` | PASS |
| screening decision | `Initial decision` | PASS |

No market, instrument, return, broker or capital value was invented for this test.

## 15. Definition of Done for an individual Idea intake

An individual Idea intake is complete when:

- a unique ID exists;
- provenance is recorded;
- minimum intake fields are populated or explicitly unknown;
- duplicate/overlap review is recorded;
- one decision among `SCREEN / PARK / REJECT` is recorded with reason;
- status matches the decision;
- the file is retained regardless of a negative outcome.

## 16. M1-001 completion result

This process plus the aligned `IDEA_TEMPLATE.md` satisfies `WBS-1.1`.

Next dependent work:

`ATS2-M1-002 — Hypothesis model`

The next step must define how a screened Idea becomes a falsifiable Hypothesis. It must not assume that `SCREEN` is evidence of edge.