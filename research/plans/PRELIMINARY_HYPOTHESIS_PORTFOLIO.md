# ATS Preliminary Hypothesis Portfolio

**Portfolio version:** `PH-PORTFOLIO-2026-10-DRAFT-01`  
**Status:** `PORTFOLIO_DRAFT_NO_MARKET_TESTING`  
**Purpose:** define the candidate research queue before any new Hypothesis is registered or tested.

## 1. Hard boundary

This document contains **proposals**, not registered Hypotheses.

No item below has an `HYP-xxxx` ID.

Before OWNER approves this portfolio ATS must not:

- run a market test for any item;
- inspect a new protected/unseen block for any item;
- tune horizons, thresholds or barriers from results;
- promote any item to Candidate;
- infer that inclusion in this list means the effect exists.

After approval, each selected item still requires lineage/Idea decision, Hypothesis formation and Data Feasibility before quantitative testing.

## 2. Proposed priority bands

- `A` — first research queue; high expected information value relative to burden.
- `B` — useful but more data/execution/selection burden.
- `C` — retain only with explicit reason; substantial prior-selection or low incremental-value concern.

Proposed default execution is sequential inside priority A unless independent data/workstreams make parallelism clearly cheaper without increasing leakage risk.

---

## PH-01 — CPI surprise directional EUR/USD response

- Priority: `A`
- Recommendation: `APPROVE_IF_POINT_IN_TIME_CONSENSUS_DATA_FEASIBLE`
- Research purpose: `ALPHA_DISCOVERY`
- Economic role: `ENTRY_SIGNAL`
- Directional: `YES`
- Preliminary family: `FAM-CPI-DIRECTIONAL`
- Market: `EURUSD spot FX`
- Decision-time information: official first-release CPI value plus point-in-time market consensus/expectation that was available before release; only after the release becomes public.
- Proposed mechanism: a positive/negative inflation surprise changes relative U.S. rate expectations and can create a signed EUR/USD repricing response.
- Development question: does a predeclared signed/standardized CPI surprise variable predict a signed executable EUR/USD forward return after publication?
- Data class: official release history, point-in-time consensus history, granular synchronized BID/ASK quotes.
- Execution requirement: sub-minute/top-of-book at minimum; stronger depth/latency modeling if intended execution is inside the first seconds.
- Material costs: event spread widening, latency, slippage/adverse selection.
- Existing ATS lineage: uses HYP-0006 event infrastructure as structural provenance only; it is a materially new directional claim.
- Positive decision consequence: proceed to bounded alpha-path characterization and freeze a trading rule.
- Negative decision consequence: stop CPI-surprise directional family rather than rescue with post-hoc sign/horizon changes.
- Information value: `HIGH`.
- Research burden: `HIGH`, mainly because honest historical consensus data may be difficult or costly.

## PH-02 — Post-CPI early-move continuation versus reversal

- Priority: `A`
- Recommendation: `APPROVE`
- Research purpose: `ALPHA_DISCOVERY`
- Economic role: `ENTRY_SIGNAL`
- Directional: `YES`
- Preliminary family: `FAM-CPI-POSTRELEASE-STATE`
- Market: `EURUSD spot FX`
- Decision-time information: only price/quote information observed after the public CPI timestamp; no consensus data required.
- Proposed mechanism: the first observable post-release price move may contain information about temporary overshoot or continuing price discovery.
- Development question: after a predeclared short observation window following release, does the sign/magnitude of the already-observed move predict subsequent signed return over a separately defined forward window?
- Data class: official event timestamps plus granular synchronized BID/ASK ticks.
- Execution requirement: granular top-of-book; latency/fill semantics must be frozen before profitability evaluation.
- Material costs: event spread, latency, slippage, adverse selection.
- Existing ATS lineage: HYP-0006 supplies only structural evidence that CPI-scheduled periods have larger post-event movement; no directional inference is inherited.
- Positive decision consequence: characterize decay/path, then freeze continuation or reversal strategy logic.
- Negative decision consequence: stop this market-state family; do not switch from continuation to reversal after observing the same result without a new accounted attempt.
- Information value: `HIGH`.
- Research burden: `MEDIUM-HIGH`.

## PH-03 — Active-session conditioned directional breakout

- Priority: `A`
- Recommendation: `APPROVE`
- Research purpose: `ALPHA_DISCOVERY`
- Economic role: `ENTRY_SIGNAL` with `REGIME_FILTER`
- Directional: `YES`
- Preliminary family: `FAM-SESSION-BREAKOUT`
- Market: `EURUSD spot FX`
- Decision-time information: completed price bars and UTC time only.
- Proposed mechanism: directional breakouts may have better continuation when participation/activity is structurally higher; HYP-0004/HYP-0005 session evidence may be used only as regime provenance.
- Development question: does a predeclared breakout signal have stronger signed forward return inside the retained active-session regime than its unconditional counterpart after BID/ASK spread?
- Data class: synchronized EUR/USD BID/ASK bars or finer quotes.
- Execution requirement: next-observable quote/open semantics; Level 2 not initially required for hourly-style execution.
- Material costs: spread, slippage, possible rollover if horizon crosses day boundary.
- Existing ATS lineage: materially distinct from rejected HYP-0001 because the mechanism/conditions include an explicit active-session regime; HYP-0001 negative history must remain in the family record.
- Positive decision consequence: run path/horizon characterization before freezing final exit.
- Negative decision consequence: stop the session-conditioned breakout family; do not search alternate clock windows as rescue.
- Information value: `HIGH`.
- Research burden: `LOW-MEDIUM` because existing EUR/USD BID/ASK infrastructure is reusable.

## PH-04 — Volatility-compression breakout continuation

- Priority: `A`
- Recommendation: `APPROVE`
- Research purpose: `ALPHA_DISCOVERY`
- Economic role: `ENTRY_SIGNAL`
- Directional: `YES`
- Preliminary family: `FAM-COMPRESSION-BREAKOUT`
- Market: `EURUSD spot FX`
- Decision-time information: completed historical bars/quotes only.
- Proposed mechanism: a low-realized-volatility/compressed range regime followed by an observable range break may represent delayed information release or order-flow imbalance with short-lived continuation.
- Development question: does a predeclared compression state plus directional breakout predict positive signed forward return relative to an unconditional executable baseline?
- Data class: EUR/USD BID/ASK bars; finer quotes if short horizons are later selected.
- Execution requirement: explicit post-signal entry semantics and side-aware BID/ASK.
- Material costs: spread/slippage; execution sensitivity increases as horizon shortens.
- Existing ATS lineage: distinct mechanism from HYP-0001 plain 24-bar breakout; HYP-0001 remains negative prior family information.
- Positive decision consequence: bounded alpha-decay/path characterization and frozen strategy formulation.
- Negative decision consequence: stop; no unconstrained compression/lookback search.
- Information value: `MEDIUM-HIGH`.
- Research burden: `LOW-MEDIUM`.

## PH-05 — G10 time-series FX momentum

- Priority: `B`
- Recommendation: `APPROVE_AFTER_FINANCING_DATA_FEASIBILITY`
- Research purpose: `ALPHA_DISCOVERY`
- Economic role: `ENTRY_SIGNAL`
- Directional: `YES`
- Preliminary family: `FAM-G10-TIME-SERIES-MOMENTUM`
- Market: point-in-time eligible G10 FX spot universe.
- Decision-time information: each instrument's own completed historical return, not cross-sectional ranking.
- Proposed mechanism: slow information incorporation and persistent macro/order-flow regimes can create own-series continuation.
- Development question: does a small predeclared formation/holding family produce a broad positive own-series directional region after quote spread and realistic financing treatment?
- Data class: multi-pair synchronized BID/ASK plus financing/rollover inputs or a defensible proxy before economic interpretation.
- Execution requirement: monthly/daily style top-of-book is likely sufficient for initial research; exact semantics to be frozen later.
- Material costs: spread and especially financing/rollover for longer holds.
- Existing ATS lineage: distinct from rejected HYP-0003 cross-sectional momentum, but HYP-0003 remains related negative momentum-family history.
- Positive decision consequence: select/freeze one rule under full family accounting, then test on unseen data.
- Negative decision consequence: close the family rather than select a single favorable cell.
- Information value: `MEDIUM-HIGH`.
- Research burden: `HIGH` due multi-pair and financing data.

## PH-06 — Post-London-fix short-horizon reversal after extreme pre-fix move

- Priority: `B`
- Recommendation: `APPROVE_IF_EVENT/EXECUTION_SEMANTICS_FEASIBLE`
- Research purpose: `ALPHA_DISCOVERY`
- Economic role: `ENTRY_SIGNAL`
- Directional: `YES`
- Preliminary family: `FAM-FIX-MICROSTRUCTURE`
- Market: `EURUSD spot FX`
- Decision-time information: signed price move before the scheduled London 16:00 fix boundary and quotes observable only after the decision point.
- Proposed mechanism: concentrated benchmark-related flow may temporarily push price in one direction around the fix and partially reverse after flow pressure dissipates.
- Development question: conditional on a predeclared extreme pre-fix signed move, is subsequent signed return in the opposite direction positive after executable spread/cost assumptions?
- Data class: accurate fix calendar/semantics plus granular BID/ASK ticks.
- Execution requirement: high; exact event-time latency, spread and slippage matter.
- Material costs: spread widening, latency, adverse selection; Level 2 may become required if passive/very-fast execution is proposed.
- Existing ATS lineage: new event/microstructure family.
- Positive decision consequence: path characterization then frozen execution-aware strategy.
- Negative decision consequence: close without searching alternate fix windows.
- Information value: `MEDIUM`.
- Research burden: `MEDIUM-HIGH`.

## PH-07 — One-sided high-tail 24H reversal follow-up

- Priority: `C`
- Recommendation: `PARK_BY_DEFAULT`
- Research purpose: `ALPHA_DISCOVERY`
- Economic role: `ENTRY_SIGNAL`
- Directional: `YES`
- Preliminary family: `FAM-RETURN-TAIL-REVERSAL`
- Market: `EURUSD spot FX`
- Decision-time information: completed trailing return and frozen threshold only.
- Proposed mechanism: unusually large upward moves may overshoot and partially mean-revert.
- Development question: a future formulation could test only the high-tail/DOWN side, but the exact reason this proposal exists is that this side passed inside rejected HYP-0002.
- Data class: EUR/USD BID/ASK bars.
- Execution requirement: explicit next-bar entry and side-aware exit.
- Material costs: spread, financing for multi-day exposure, overlap/dependence.
- Existing ATS lineage: **strong post-selection dependency on HYP-0002 and the earlier 16-alternative discovery**.
- Positive decision consequence: would still require strong unseen evidence because the side was selected after observing HYP-0002.
- Negative decision consequence: close permanently.
- Information value: `LOW-MEDIUM` after selection penalty.
- Research burden: `MEDIUM` because genuinely fresh evidence is required.

## 3. Proposed approval set

Recommended initial OWNER decision:

- approve for future formation: `PH-01`, `PH-02`, `PH-03`, `PH-04`;
- approve conditionally / second wave: `PH-05`, `PH-06`;
- park: `PH-07`.

This recommendation is based on conceptual information value, lineage and expected data/execution burden only. No new market outcome was calculated to rank the proposals.

## 4. Proposed first execution order after approval

Subject to Data Feasibility:

1. `PH-03` — high information value with reusable existing data infrastructure;
2. `PH-04` — similar low/medium data burden and genuinely directional claim;
3. `PH-02` — stronger event/execution burden but reuses CPI/tick infrastructure;
4. `PH-01` — potentially high value, gated by honest point-in-time consensus availability;
5. `PH-05` — broader universe plus financing burden;
6. `PH-06` — execution-sensitive microstructure research;
7. `PH-07` — remains parked absent explicit OWNER reprioritization.

Execution order is a portfolio decision, not evidence ranking.

## 5. OWNER approval record

Current status:

`NOT_APPROVED`

Allowed next decision:

- `APPROVE`
- `APPROVE_WITH_CHANGES`
- `REJECT_PORTFOLIO`

Until one of these is recorded, no PH item may progress to quantitative testing.
