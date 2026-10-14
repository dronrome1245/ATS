# ATS Research Portfolio Protocol

**Status:** PROPOSED BASELINE FOR RF-039  
**Applies to:** new research proposals after this protocol becomes effective  
**Purpose:** reduce sequential idea chasing, make the research denominator visible before testing, and require explicit prioritization before any new Hypothesis consumes data or protected evidence.

## 1. Core rule

ATS must prepare and approve a preliminary research portfolio before starting quantitative testing of new research proposals.

Flow:

`Research proposals → Preliminary portfolio → OWNER portfolio approval → Idea/Hypothesis formation → Data Feasibility → research execution`

A proposal in the preliminary portfolio is **not** a registered Hypothesis and must not receive an `HYP-xxxx` ID merely to reserve sequence numbers.

Before portfolio approval ATS may:

- formulate candidate research questions;
- document mechanism and expected economic role;
- estimate data/execution requirements;
- identify overlap with prior ATS research;
- estimate cost, complexity and information value;
- rank candidates;
- reject duplicates or low-value proposals.

Before portfolio approval ATS must **not**:

- calculate a market outcome for a proposed item;
- run a backtest or signal test for that item;
- inspect protected/unseen data for that item;
- tune parameters using market results;
- create a registered Hypothesis as if the proposal were already admitted;
- consume an independent/protected evidence block.

## 2. Why the portfolio gate exists

Testing hypotheses one at a time and inventing the next one after observing each result creates hidden program-wide selection freedom.

The portfolio gate makes visible, before new results are observed:

- what ATS intends to test;
- what alternatives were considered;
- why some proposals have higher priority;
- which proposals share the same research family;
- what data and execution burden each proposal creates;
- what result would actually change a decision.

The approved portfolio is not immutable forever. Changes are allowed, but material additions/removals after research outcomes are known must be recorded as new selection history under `MULTIPLE_RESEARCH_ACCOUNTING.md`.

## 3. Portfolio proposal identity

Before approval, proposals use temporary labels only:

`PH-01`, `PH-02`, ...

`PH` means `Portfolio Hypothesis Proposal`.

A PH label is not an Idea ID or Hypothesis ID and has no evidentiary status.

After approval, a proposal may be routed to:

- an existing Idea;
- a new Idea Intake;
- a new Hypothesis under an existing Idea;
- `PARK`;
- `REJECT`;
- `REFERENCE_ONLY`.

Only then may normal permanent IDs be assigned under the applicable methodology.

## 4. Required fields for every portfolio proposal

Each PH item must contain:

- temporary proposal ID;
- concise statement;
- proposed mechanism;
- market/instrument/universe;
- `RESEARCH_PURPOSE`;
- `ECONOMIC_ROLE`;
- directional or non-directional classification;
- information available at decision time;
- candidate development question;
- likely data class;
- likely execution-data requirement;
- likely material costs;
- nearest existing ATS lineage / duplicate risk;
- preliminary research family;
- expected information value;
- estimated research burden;
- result-dependent decision: what changes if positive / negative;
- priority recommendation.

No exact optimized parameter value is required at portfolio stage.

## 5. Research purpose

Use one primary value:

- `PLATFORM_QUALIFICATION`
- `MARKET_STRUCTURE`
- `REGIME_FILTER`
- `ALPHA_DISCOVERY`
- `EXECUTION_RESEARCH`
- `CONFIRMATORY_REPLICATION`

A proposal that only checks a known market-structure fact should normally be low priority unless it is needed for platform qualification, a regime filter or a specific downstream decision.

## 6. Economic role

Use one primary value:

- `NO_DIRECT_TRADING_ROLE`
- `REGIME_FILTER`
- `ENTRY_SIGNAL`
- `EXIT_SIGNAL`
- `POSITION_SIZING`
- `EXECUTION_RULE`
- `RISK_FILTER`

A structural result with `NO_DIRECT_TRADING_ROLE` does not automatically justify confirmatory replication.

## 7. Value-of-information screen

Before recommending approval, answer:

1. What decision changes if the proposal is positive?
2. What decision changes if it is negative?
3. Is the claimed effect already a well-known structural fact?
4. Is there a cheaper test that answers the same decision question?
5. Does the proposal require protected evidence before a trading mechanism exists?
6. Is the likely effect large enough to matter after plausible costs?
7. Will this item add information distinct from other portfolio items?

If neither positive nor negative outcome would change the next action, recommend `PARK`, `REJECT` or `REFERENCE_ONLY`.

## 8. Portfolio approval

OWNER approves the portfolio as a program-priority decision, not as approval of market truth.

Approval records:

- portfolio version;
- included PH items;
- excluded/parked items;
- priority order or priority bands;
- permitted parallelism;
- any data-budget or protected-evidence constraints;
- approval date/reference.

Approval does **not** authorize live trading, capital use or result-based parameter tuning.

## 9. Changes after approval

### Non-material

Clarification that does not alter mechanism, market, condition, direction, research family or expected test can be edited in place before permanent Hypothesis formation.

### Material

Adding a new mechanism, market, direction, event class, horizon family or proposal after results from the approved portfolio are known is a new material selection event.

Record:

- why it was added;
- what prior outcomes were already known;
- whether the addition was result-motivated;
- its research family;
- updated portfolio version.

Do not silently treat later additions as if they were part of the original denominator.

## 10. Relationship to Hypothesis Model

For new research after this protocol becomes effective, portfolio approval becomes an admission prerequisite before creating a new registered Hypothesis for quantitative work.

The sequence is:

`PH proposal → approved portfolio item → Idea/lineage decision → HYP registration → Data Feasibility`

Existing historical `HYP-0001` through `HYP-0007` are not retroactively invalidated and are handled by the dedicated RF-039 disposition decision.

## 11. Relationship to multiple-research accounting

The portfolio itself becomes part of the search denominator.

At minimum preserve:

- total PH proposals considered;
- approved count;
- parked/rejected count;
- research families represented;
- later additions/removals;
- result-motivated changes;
- promotion from PH to Idea/HYP.

A future successful strategy must not be presented as if no alternative portfolio proposals existed.

## 12. Execution order

Default priority:

1. high information value / low burden;
2. direct potential trading role;
3. realistic data and execution observability;
4. clear falsification;
5. limited overlap with already-tested ATS claims.

Do not prioritize confirmatory structural replication over a trading hypothesis merely because the structural path already exists.

## 13. Completion condition

The portfolio stage is complete only when:

- the preliminary list exists;
- each item has the required fields;
- duplicates/lineage are reviewed;
- priority is proposed;
- OWNER records `APPROVE`, `APPROVE_WITH_CHANGES`, or `REJECT_PORTFOLIO`;
- no proposed item has been quantitatively tested before approval.

Until then, status is:

`PORTFOLIO_DRAFT_NO_MARKET_TESTING`.
