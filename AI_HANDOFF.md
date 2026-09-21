# ATS AI Handoff

**Назначение:** восстановление текущего контекста ATS v2.

## Current state

- Phase: `M3_REFERENCE_STRATEGY_1 / IN_PROGRESS`.
- Reference class: `SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT`.
- Instrument: `EURUSD`.
- Idea: `IDEA-0001`.
- Hypothesis: `HYP-0001`.
- Data Feasibility decision: `CONDITIONAL`.
- Live/demo/allocation/scaling remain disallowed.

## Frozen HYP-0001 claim

- signal: completed EUR/USD BID close > max BID high of prior 24 completed contiguous eligible 1H bars;
- entry measurement: next eligible ASK open;
- primary effect horizon: 24 contiguous eligible 1H bars;
- exit/valuation measurement: BID open 24 bars after entry;
- expected: signal mean > 0 and > unconditional 24-bar executable baseline;
- same-close execution prohibited.

## Data Feasibility

Canonical review:

`research/reviews/HYP-0001-DATA_FEASIBILITY.md`

Decision:

`CONDITIONAL`

Primary candidate source: Dukascopy Historical Data Export / JForex history.

Structurally supported:

- `Instrument.EURUSD`;
- `Period.ONE_HOUR`;
- separate `OfferSide.BID` / `OfferSide.ASK`;
- free Historical Data Export in CSV;
- fully formed bar semantics.

Prototype-blocking conditions still unresolved:

- actual BID/ASK files not yet frozen;
- exact local coverage/continuity not measured;
- raw snapshot hashes not yet recorded.

Non-blocking but claim-limiting gaps:

- historical rollover not frozen;
- broker/account commission not selected;
- 1H bars do not supply live-fill slippage.

Therefore PROTO-01 may be prepared but cannot execute until the snapshot/coverage conditions are resolved.

Primary prototype economic label, unless additional costs are added:

`QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING`

Raw Dukascopy data remains local/external; Git should store only manifest metadata/hashes unless redistribution rights are confirmed.

## Current closure check

Current checker:

`ATS2-M3-003 — Data feasibility`

Run:

`ATS_TASK_CHECK.bat`

## Next task after PASS

`ATS2-M3-004 — Cheap prototype`

Next artifact:

`research/reviews/HYP-0001-PROTOTYPE-01.md`

Cheap Prototype must follow `governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md` and record one question, frozen data snapshot, cost/execution limitations, planned metrics and pre-run decision rule before result observation.

## Recovery check

- Last implemented task: `ATS2-M3-003`.
- Closure checker: `ATS2-M3-003`.
- Next ready task after PASS: `ATS2-M3-004`.
- Current WBS after PASS: `WBS-3.4`.
- Candidate/Strategy/Experiment created? — no.
- Live/demo/allocation/scaling allowed? — no.
