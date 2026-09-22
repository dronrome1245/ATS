# Reference Strategy #2 Selection

**Task:** `ATS2-M6-002`  
**Work package:** `WBS-6.1`  
**Decision:** `SELECT`  
**Date:** 22 September 2026

## Selected strategy class

`SINGLE_INSTRUMENT_1H_TWO_SIDED_RETURN_TAIL_REVERSAL`

This is a single-instrument 1H reversal/mean-reversion class after an extreme prior return state.

It may research DOWN reversal after an extreme positive move and UP reversal after an extreme negative move. Signals use completed-bar information and modeled action occurs no earlier than the next information-available point.

No exact lookback, tail threshold, effect horizon, sizing, leverage, stop, capital or live policy is selected here.

## Discovery provenance

Canonical summary:

`reports/research/SEARCH-EURUSD-H1-2021-2025-001-summary.md`

The bounded search evaluated all 16 alternatives:

- continuation: `0 / 8` shortlisted;
- reversal: `5 / 8` shortlisted;
- all four 24H-effect reversal combinations were shortlisted.

The result remains `EXPLORATORY_OBSERVATION`.

## No post-result winner ranking

The Search Manifest preregistered only `shortlist_score >= 0`.

No ranking or tie-break rule among shortlisted alternatives was preregistered.

Therefore M6-002 does not promote `alt-06`, `alt-08`, `alt-14`, `alt-15` or `alt-16` as a privileged winner. A future Hypothesis must make a new explicit fixed formulation and preserve the full 16-alternative selection history.

## Distinction from Reference Strategy #1

Reference Strategy #1 was `SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT`.

Reference Strategy #2 asks whether an extreme directional move reverses rather than continues and is two-sided rather than long/flat. This materially changes the strategy-logic profile without claiming an edge.

## Data boundary

The first discovery used `DATA-DUKASCOPY-EURUSDH1-PROTO01-001@1.0.0` for 2021–2025 EURUSD H1.

That block is development-known and cannot be relabeled as protected unseen evidence for the new line.

## Research integrity

The path is cumulative: 16 alternatives inspected, five shortlisted, all five reversal, no post-result winner ranking. This history must appear in future Research Freedom Summary accounting.

## Safety boundary

This selection does not authorize demo/shadow trading, real-money trading, capital allocation, leverage, Strategy Risk Mandate, broker/account selection or scaling.

## Next step

The first Idea instance is `research/ideas/IDEA-0002.md`.

After M6-002 exact-head closure, create a separately frozen falsifiable HYP-0002 before any new confirmatory result is viewed.
