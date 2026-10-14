# ATS Gate Checkpoint Protocol

**Status:** RF-039 PROPOSED BASELINE  
**Purpose:** prevent context drift before irreversible or evidence-consuming research actions.

## 1. Core rule

ATS must not rely on conversational memory alone before a material gate.

Immediately before any of the following actions, GPT must re-read the relevant canonical state and produce a compact checkpoint:

- research freeze;
- protected/confirmatory reveal;
- confirmatory trading test;
- independent evidence reveal;
- protocol change after freeze;
- any other action that can irreversibly consume evidence or change the interpretation of a result.

## 2. Required sources

At minimum re-check:

1. `AI_HANDOFF.md`;
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`;
4. relevant Hypothesis / Idea / portfolio item;
5. relevant Data Feasibility, freeze, decision and methodology files;
6. exact runner/code/data identities when applicable.

If canonical sources disagree, record the desynchronization and block the irreversible action until the research meaning is unambiguous.

## 3. Mandatory checkpoint

Before the gate, state explicitly:

- `CLAIM` — what exact claim is being tested;
- `RESEARCH_PURPOSE`;
- `ECONOMIC_ROLE`;
- `MARKET / INSTRUMENT`;
- `DATASET IDENTITY / PERIOD / SOURCE RULES`;
- `CLEANING / GAPS / ELIGIBILITY`;
- `FORMULAS`;
- `PARAMETERS / SEARCH FAMILY`;
- `HORIZONS`;
- `PRIMARY METRICS`;
- `DECISION / FALSIFICATION RULE`;
- `RUNNER / CODE IDENTITY`;
- `COST / EXECUTION ASSUMPTIONS` when economically relevant;
- `PROTECTED-EVIDENCE STATUS`;
- `WHAT IS FROZEN`;
- `WHAT MAY STILL CHANGE`;
- `OWNER EXECUTOR REQUIRED?`;
- `OWNER DECISION AUTHORITY REQUIRED?`.

## 4. Fail-closed rule

Every decision-relevant checkpoint field must be either resolved or explicitly declared not applicable with a reason.

If a field that can change the result is `UNKNOWN`, `UNRESOLVED`, inconsistent with canonical state, or silently inferred from chat memory, do not reveal protected evidence and do not run the confirmatory test.

Resolve the ambiguity first without inspecting the protected outcome.

## 5. Context-window rule

Long conversations do not relax governance.

When a session is long, context is uncertain, or work resumes after interruption, reconstruct the gate from repository source-of-truth files rather than from remembered conversation history.

The checkpoint is a control artifact, not an additional research test and not a new Material Research Attempt unless its resolution changes the research specification.

## 6. Technical gate distinction

Formatting, lint, branch synchronization, hash checks and deterministic CI retries may use LIGHT MODE and do not require the full research checkpoint unless they are immediately authorizing an irreversible reveal.

## 7. Boundary

This protocol does not calculate market outcomes and does not itself authorize a reveal. It verifies that an already-authorized material action still matches the frozen research contract.