# Candidate Promotion Review

## Identity

- Parent Idea ID: `null`
- Parent Hypothesis ID: `null`
- Review sequence: `null`
- Review status: `DRAFT`
- Created on: `null`
- Reviewer role: `null`

For a real review, sequence uses `CPR-01`, `CPR-02`, and so on within the same Hypothesis lineage.

## Entry condition

- Economic Pre-Screen reference: `null`
- Economic Pre-Screen decision: `null`

A completed promotion decision requires Economic Pre-Screen decision `ADVANCE_TO_CANDIDATE_REVIEW`.

## Upstream Research Funnel package

- Idea reference: `null`
- Hypothesis reference: `null`
- Data Feasibility Review reference: `null`
- Cheap Prototype references: `null`
- Economic Pre-Screen reference: `null`
- Negative / discarded prototype or search references: `null`

## P1 — Lineage integrity

- Assessment: `null`
- Rationale: `null`

Confirm that Idea → Hypothesis → Data Feasibility → Prototype → Economic Pre-Screen is traceable without silent material reformulation.

## P2 — Preliminary economic case

- Assessment: `null`
- Rationale: `null`

Summarize why the preliminary economics do or do not justify a larger formal research budget.

## P3 — Evidence honesty

- Assessment: `null`
- Rationale: `null`

Confirm that exploratory, registered and validation evidence classes are not conflated.

## P4 — Negative and search history

- Assessment: `null`
- Prototype iterations inspected: `null`
- Parameter / variant search summary: `null`
- Markets / instruments / horizons inspected: `null`
- Discarded alternatives: `null`
- Rationale: `null`

## P5 — Data and testability

- Assessment: `null`
- Remaining data gaps: `null`
- Timestamp / revision / leakage constraints: `null`
- Rationale: `null`

## P6 — Known risks and failure modes

List the main ways the preliminary effect could be false, unstable, untradeable or economically useless.

## P7 — Unresolved research questions

List open questions that S02–S05 must answer. Unknowns remain explicit; do not invent favorable assumptions.

## P8 — Proposed S02–S05 research scope

### S02 Research Specification

- Required outcome: `null`

### S03 Data & Research Protocol

- Required outcome: `null`

### S04 Baseline Implementation

- Required outcome: `null`

### S05 Economic Viability

- Required outcome: `null`

## Platform / capability needs

- Reusable platform needs: `null`
- Strategy-specific needs: `null`
- External data/access needs: `null`

These are needs, not pre-approved implementation scope.

## Promotion decision

- Decision: `null`
- Decision reason: `null`
- Decision date: `null`
- Reopening criterion if `PARK`: `null`
- Candidate ID created: `null`

Allowed completed decisions: `PROMOTE`, `PARK`, `REJECT`.

Rules:

- `PROMOTE` creates one new `CAND-xxxx` and records it above.
- `PARK` creates no Candidate; set Candidate ID created to `NOT_APPLICABLE`.
- `REJECT` creates no Candidate; set Candidate ID created to `NOT_APPLICABLE`.
- `PROMOTE` is permission for deeper research, not validated edge or live permission.
