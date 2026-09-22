# ATS Independent Examination Protocol

**Task:** `ATS2-M4-006`  
**Work package:** `WBS-4.6`  
**Status:** BASELINE  
**Purpose:** define a one-shot protected examination for a frozen future Strategy Version after S06 validation PASS.

## 1. Core rule

Independent Examination is a **one-shot reveal** of a protected evidence block.

Before reveal, ATS freezes:

- Candidate / Strategy ID and exact Strategy Version;
- code revision and implementation reference;
- parameters/configuration;
- Dataset ID/version and exact protected block boundaries;
- data transformation lineage and integrity identifiers;
- cost/execution assumptions;
- primary metrics;
- binary `PASS / FAIL` decision rule;
- exam runner/environment identity;
- any allowed deterministic preprocessing;
- exam manifest revision/hash.

After the protected result is revealed, that block is consumed for the applicable research line/version.

There is no `RETURN`, conditional pass, rescue retuning or second independent attempt on the same revealed block.

## 2. Eligibility

A strategy-specific independent exam requires:

1. a promoted Candidate / concrete Strategy Version;
2. S05 Economic Viability `PASS`;
3. S06 Validation `PASS`;
4. a complete Validation Profile;
5. preserved research/search history;
6. an identified protected block not used for development or validation tuning;
7. an immutable Independent Exam Freeze Manifest created before reveal.

Program-level protocol/tooling may exist before such a Candidate exists.

HYP-0001 remains `REJECTED_AT_R3` and is not eligible.

## 3. Information boundary

The protected block must not have been used to choose:

- signal rules;
- features;
- parameters;
- filters;
- market/universe;
- horizon;
- execution assumptions;
- cost assumptions;
- validation profile;
- primary metrics;
- PASS/FAIL thresholds;
- data-cleaning rules that can affect the decision.

Knowledge of metadata needed to define the block is allowed only to the extent that it does not reveal decision-relevant outcomes.

If decision-relevant protected results are inspected during development or validation, the block is no longer independent for that research line.

## 4. Freeze Manifest

Before reveal, create an **Independent Exam Freeze Manifest**.

Minimum fields:

- `exam_id`;
- Candidate / Strategy ID;
- Strategy Version;
- parent S05 and S06 decision references;
- code revision;
- implementation reference;
- configuration/parameter identity or hash;
- Dataset ID/version;
- protected block start/end or equivalent event/universe boundary;
- dataset/block integrity identifier where possible;
- transformation/preprocessing identity;
- cost model identity and assumptions;
- execution model identity and assumptions;
- primary metric names;
- exact binary `PASS / FAIL` rule;
- environment identity;
- deterministic seed/protocol if applicable;
- expected evidence class;
- freeze timestamp;
- manifest revision/hash;
- authorized reveal procedure/reviewer.

A field may be marked not applicable only when the reason is explicit.

## 5. Freeze states

Canonical states:

`DRAFT → FROZEN → REVEALED → DECIDED`

### DRAFT

The manifest can still change. Protected results must not be accessed.

### FROZEN

The manifest is immutable for the exam. Any decision-relevant change cancels this exam before reveal and requires a new freeze manifest.

### REVEALED

Decision-relevant protected data/result has become available. The block is consumed for the applicable independent claim.

### DECIDED

A binary `PASS` or `FAIL` is recorded with the frozen inputs and revealed result.

There is no state that returns a revealed exam to `FROZEN`.

## 6. Reveal rule

A reveal occurs when any authorized or unauthorized process/person gains access to decision-relevant protected output sufficient to inform strategy decisions.

Examples:

- viewing the primary metric;
- viewing the equity/P&L path;
- viewing outcome labels used by the decision;
- inspecting protected observations in a way that can influence tuning;
- receiving a generated PASS/FAIL before the official review.

The reveal timestamp/event must be recorded.

## 7. Technical failure before reveal

A technical failure does **not automatically consume** the protected block if all are true:

1. failure occurred before decision-relevant protected content/result became accessible;
2. logs prove no protected result was emitted or inspected;
3. strategy/version/config/criteria remain frozen;
4. rerun only corrects infrastructure mechanics that cannot change the research decision;
5. the incident and rerun reason are recorded.

Examples may include inability to start the runner or missing runtime dependency before protected data is opened.

If it is unclear whether protected results were exposed, default to **consumed**.

## 8. Technical failure after reveal

If protected output was exposed and then the runner/reporting pipeline failed:

- the block is consumed;
- repair may reproduce/report the same frozen computation;
- repair must not change rules/configuration/criteria;
- the block cannot be presented as a fresh independent exam for a modified version.

A reporting repair does not erase the first reveal.

## 9. Decision rule

Independent Examination decision is only:

`PASS / FAIL`

### PASS

Use only when the frozen rule is satisfied and exam integrity is intact.

### FAIL

Use when the frozen rule is not satisfied or when a valid frozen run reveals an unfavorable result.

A valid unfavorable result is evidence. It is not an implementation defect.

There is no `RETURN` from S07 to alter the same version while preserving the same block as independent.

## 10. Integrity failure

If exam integrity is broken before a trustworthy decision can be made, record an exam integrity failure separately from strategy `FAIL`.

Examples:

- wrong Strategy Version executed;
- wrong protected block;
- corrupted data;
- mismatched code/config hash;
- decision rule changed after freeze;
- unauthorized protected-data exposure before the official run.

The block's future status depends on whether decision-relevant contents were exposed.

If exposed, it is consumed.

If provably not exposed, a corrected new freeze manifest may reuse the still-protected block.

## 11. Material changes after FAIL

After independent `FAIL`, future research may create a materially changed Strategy Version.

However:

- the failed result remains attached to the old version;
- the revealed protected block is development-known;
- that block cannot serve as independent evidence for the modified line;
- a new independent claim requires genuinely protected evidence not used for the redesign.

No wording such as “retest”, “confirmation”, or “second chance” restores independence.

## 12. PASS does not authorize live trading

Independent `PASS` means the frozen version passed the registered protected historical/model examination within scope.

It does not itself authorize:

- demo trading;
- live trading;
- capital allocation;
- scaling.

Those remain governed by later milestones and OWNER decisions.

## 13. Evidence class

A successful protocol-compliant exam may qualify as:

`INDEPENDENT_EXAMINATION_EVIDENCE`

only if the Evidence Taxonomy prerequisites are satisfied.

Registration/freeze alone is not enough.

An integrity-broken or previously revealed block cannot be upgraded by relabeling it.

## 14. Audit trail

The exam package must preserve:

- freeze manifest;
- exact manifest hash/revision;
- code/config/data identities;
- reveal event;
- runner logs;
- result artifact;
- PASS/FAIL decision;
- integrity incidents;
- reviewer/decision authority;
- evidence classification;
- links to prior validation and research history.

Negative evidence is retained.

## 15. Relationship to multiple-research accounting

Independent Examination does not erase prior search freedom.

The reviewer must be able to see:

- prior hypotheses/versions;
- discovery/search attempts;
- parameter searches;
- failed experiments;
- validation returns/failures;
- previously consumed protected blocks.

That history is formalized further by `WBS-4.7 — Multiple-research accounting`.

## 16. Structural acceptance

This protocol is structurally acceptable when a future reviewer can answer before reveal:

1. What exact Strategy Version is frozen?
2. What exact code/configuration will run?
3. What exact protected block is being consumed?
4. Why is that block still independent?
5. What costs/execution assumptions are frozen?
6. What are the primary metrics?
7. What exact binary rule maps result to PASS/FAIL?
8. What event counts as reveal?
9. What happens if infrastructure fails before reveal?
10. What happens if output is exposed before a technical failure?
11. Where is the immutable audit trail?
12. What evidence class can the result support?

## 17. Current boundary

This document creates protocol infrastructure only.

No Candidate currently exists, no protected block is selected, and no independent exam is run.

HYP-0001 remains `REJECTED_AT_R3`.

No demo/live/capital permission is created.
