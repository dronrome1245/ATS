# Data Feasibility Review — HYP-0001 EUR/USD 1H Breakout

## Identity

- Hypothesis ID: `HYP-0001`
- Review status: `CONDITIONAL`
- Reviewed on: `2026-09-21`
- Reviewer role: `DATA / RESEARCH`

## Hypothesis summary

- Statement summary: after a completed EUR/USD 1H BID close breaks strictly above the maximum BID high of the previous 24 completed eligible 1H bars, the executable long return from the next eligible ASK open to the BID open 24 eligible 1H bars later is expected to have a positive mean and exceed the unconditional 24-bar executable-return baseline.
- Market / universe context: `FX_SPOT_OTC / EURUSD`
- Decision/effect horizon: signal on completed 1H bar; primary effect horizon `24 eligible 1H bars`
- Decision-time information premise: signal uses completed BID bars only; same-close execution is prohibited; entry measurement starts at the next eligible ASK open.

## Required information and source candidates

### Primary candidate — Dukascopy Historical Data / JForex history

Official Dukascopy documentation supports:

- `Instrument.EURUSD`;
- `Period.ONE_HOUR`;
- separate `OfferSide.BID` and `OfferSide.ASK`;
- historical retrieval by shift, candle interval and time interval;
- the distinction between shift `0` current/incomplete candle and shift `1` latest fully formed candle;
- 1H Historical Tester candle data with Bid/Ask selection;
- a free Historical Data Export tool with CSV download.

Canonical source references reviewed on 21 September 2026:

- https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/history-bars/
- https://www.dukascopy.com/wiki/en/forex-cfds/jforex/historical-tester/
- https://www.dukascopy.com/swiss/english/marketwatch/historical/
- https://www.dukascopy.com/wiki/en/forex-cfds/jforex/customizing-platform/
- https://www.dukascopy.com/wiki/en/forex-cfds/account-management/rollovers/
- https://www.dukascopy.com/swiss/sk/legal-pages/terms-of-use/

### Secondary candidate — Alpha Vantage

Alpha Vantage documents `FX_INTRADAY` for `EUR` / `USD` with `60min` interval, but the endpoint is currently Premium and its standard OHLC output does not by itself establish separate BID/ASK execution semantics required by `HYP-0001`.

Reference:

- https://www.alphavantage.co/documentation/

Disposition: **not the primary source for HYP-0001** unless paired with an independently justified BID/ASK/spread source, which would add unnecessary source-alignment complexity.

## Access and licensing assessment

- Required data categories: EUR/USD 1H BID OHLC, aligned ASK OHLC, timestamps, session/weekend gaps, source identity, spread implicit in BID/ASK, and rollover information where an economic claim requires it.
- Candidate source: Dukascopy Historical Data Export / JForex historical service.
- Access verified: `DOCUMENTED_BUT_NOT_YET_FROZEN_LOCALLY`.
- Public export path: Dukascopy states that historical forex data can be exported for free in CSV through its Historical Data Export tool.
- Licensing / redistribution constraints: Dukascopy terms restrict redistribution/publication and database use in some contexts. ATS therefore **does not assume redistribution rights** for raw source data.
- Repository policy for this research line: raw Dukascopy market files remain local/external; Git stores only Dataset Manifest metadata, acquisition method, source references, transformation code, coverage summary and cryptographic hashes unless redistribution rights are separately confirmed.

The XML Data license is not treated as a blanket license for all JForex/Historical Export data. Source-specific terms must be respected.

## Coverage

- Earliest usable timestamp: `NOT_YET_LOCALLY_VERIFIED`.
- Latest usable timestamp: `NOT_YET_LOCALLY_VERIFIED`.
- Official-support indication: Dukascopy support stated in 2022 that its hourly major-FX database begins around 2003; this is a coverage clue, not the frozen dataset boundary.
- Continuity / known gaps: regular FX weekend closures and possible feed gaps are expected; exact missing-bar statistics must be measured after export.
- Instrument breadth: one instrument only, EUR/USD.
- Historical constituent membership: `NOT_APPLICABLE`.
- Regime diversity: potentially long history exists, but actual selected period is not chosen in this review.

A prototype may not start until exact first/last usable timestamps and row counts are recorded from the actual downloaded snapshot.

## Granularity and field semantics

- Required granularity: `1H`.
- Available granularity: Dukascopy explicitly supports `Period.ONE_HOUR` and 1 Hour Historical Tester candles.
- Required fields: timestamp, BID O/H/L/C, ASK O/H/L/C.
- Field semantics: signal uses BID bars; modeled long entry uses ASK open; primary exit/valuation uses BID open.
- Aggregation limitations: aggregated hourly bars do not reproduce intra-hour path or actual order fills. HYP-0001 only requires completed-bar signal formation and next-bar/open quote measurement, so 1H bars are sufficient for the primary continuation question.

## Time semantics

- Source timestamp representation: JForex history methods use millisecond timestamps and time intervals aligned to the requested bar period.
- Canonical research timezone: `UTC`.
- Timestamp meaning: Dataset Manifest must store bar-open time in UTC and derive bar-close/availability as one hour later for a fully formed 1H bar, subject to verification against exported source semantics.
- 1H boundaries: Dukascopy documentation states Day Start Time affects periods longer than 1 hour; `ONE_HOUR` is therefore not shifted by the daily-candle EET/GMT setting.
- Market calendar / session rules: FX has a scheduled weekend closure. Dukascopy documents reopening around 21:00 GMT in summer or 22:00 GMT in winter and corresponding settlement timing.
- Daylight-saving handling: do not derive bar eligibility from local wall-clock assumptions; canonicalize source timestamps to UTC.
- Decision-time availability: signal bar becomes usable only after it is fully formed. JForex shift `1` is the latest fully formed bar; shift `0` is incomplete and is prohibited for signal computation.

### Canonical HYP-0001 gap policy

For `PROTO-01`:

1. do not synthesize missing 1H bars;
2. do not forward-fill BID or ASK prices;
3. BID and ASK bar timestamps must match exactly;
4. a 24-bar lookback/forward window must consist of consecutive hourly timestamps;
5. scheduled weekend/session closures break continuity;
6. any signal whose required 24-before or 24-after window crosses such a break is excluded from the primary test;
7. unscheduled gaps also break continuity and are reported.

This policy keeps the primary `24 eligible 1H bars` claim close to a 24-hour active-market interval rather than silently turning it into a multi-day weekend horizon.

## Revisions and corrections

- Data revised/restated after first publication: `POSSIBLE / NOT GUARANTEED IMMUTABLE`.
- Point-in-time vintages available: `NOT ESTABLISHED`.
- First-release versus corrected historical files distinguishable: `NOT ESTABLISHED`.
- Correction/update timestamps available: `NOT ESTABLISHED`.
- Prototype handling rule: freeze the actual downloaded files before analysis, compute SHA-256 for every raw file, record acquisition timestamp and source method, and never silently replace the snapshot after results are observed.

A corrected or replaced source snapshot is a material data change and requires a new Dataset Manifest version and review of whether the prototype must be rerun.

## Instrument lifecycle

- Corporate actions: `NOT_APPLICABLE`.
- Split/dividend adjustment: `NOT_APPLICABLE`.
- Delisting/expiry: `NOT_APPLICABLE` to a spot FX pair in the equity sense.
- Contract roll: `NOT_APPLICABLE`.
- Relevant lifecycle risk: vendor/feed convention changes and market-session convention changes must remain visible in the dataset metadata.

## Missing and bad data

- Missing observation policy: `FAIL_WINDOW`; do not impute.
- Duplicate timestamp policy: `BLOCK_UNTIL_RESOLVED`.
- Out-of-order records: sort only by canonical UTC timestamp after uniqueness validation; record this transformation.
- BID/ASK alignment: exact timestamp join required; unmatched side breaks the window.
- Bad/impossible value policy:
  - OHLC internal consistency must hold;
  - non-finite/non-positive prices are rejected;
  - aligned ASK open should not be below BID open; violations are flagged for source review.
- Stale data: repeated prices are not automatically errors, but long suspicious runs must be diagnosed.
- Feed/outage notes: all detected gaps and excluded windows are counted and reported.

## Universe and selection risks

- Survivorship risk: low/not applicable for one current major FX pair, but this does not generalize to other instruments.
- Historical universe membership risk: `NOT_APPLICABLE`.
- Selection bias risk: EUR/USD was deliberately selected as Reference Strategy #1 instrument before any HYP-0001 prototype result; this is recorded research selection and limits generalization.
- Delisted/failed entity coverage: `NOT_APPLICABLE`.
- Mitigation: no cross-instrument claims; retain the selection history.

## Leakage and overlap risks

- Future-looking transformation: rolling breakout window must exclude the signal bar and all future bars.
- Execution leakage: same-close fill is prohibited.
- BID/ASK leakage: entry ASK open becomes known only at the next eligible bar; it is an outcome/execution measurement, not a signal input.
- Window overlap: 24-bar forward windows may overlap across nearby signals, creating dependent observations.
- Future-known normalization: prohibited for the primary test.
- Event-window leakage: not applicable beyond overlapping forward windows.
- Mitigation: report signal count, overlapping-window count/share and dependence limitation; do not present naive independence-based significance as validation evidence.

## Transformation trace and dataset identity

Before `PROTO-01` runs, materialize a Dataset Manifest that records:

- provider: `Dukascopy`;
- instrument: `EURUSD`;
- period: `ONE_HOUR / 1H`;
- offer sides: `BID + ASK`;
- exact acquisition method;
- acquisition timestamp;
- source file names/objects;
- exact coverage;
- raw SHA-256 identities;
- canonical UTC transformation;
- BID/ASK alignment step;
- gap/window eligibility rules;
- transformation code revision.

Dataset ID: `NOT_ASSIGNED_UNTIL_ACTUAL_SNAPSHOT_EXISTS`.

Raw data must not be committed merely for convenience. The manifest and hashes are the repository evidence of the local/external snapshot.

## Cost and execution inputs

### Spread

`AVAILABLE_FROM_DATA`.

HYP-0001 uses ASK open for entry and BID open for exit/valuation, so quoted spread is incorporated directly in the primary executable-return definition.

### Commission

`NOT_YET_SELECTED / BROKER_ACCOUNT_SPECIFIC`.

No broker/account is selected at this research stage. Commission is not intrinsic to the signal-continuation claim. PROTO-01 may not describe its result as fully net/live economics without an explicit commission premise.

### Financing / rollover

`MATERIAL_BUT_NOT_YET_FROZEN`.

Dukascopy documents that positions open at settlement are rolled and receive swap charges/credits; EUR/USD may receive multiple swap applications around value-date/weekend/holiday transitions.

Because the primary 24-bar horizon can cross settlement, historical rollover must be included before any claim of full economic viability.

For the first Cheap Prototype, rollover may remain unmodeled only if the result is explicitly labeled:

`QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING`.

### Slippage / latency

`NOT_AVAILABLE_FROM_1H_BAR_DATA`.

Next-bar ASK open / BID exit are deterministic quote measurements, not promises of real fills. Any execution/live claim is prohibited.

## Known gaps

### GAP-DF-001 — Actual snapshot not yet frozen

- Affected component: all prototype calculations.
- Bias risk: untracked source replacement or revised history.
- Blocks Cheap Prototype: `YES UNTIL RESOLVED`.
- Required mitigation: download actual BID and ASK files, record acquisition metadata and SHA-256 in a Dataset Manifest.

### GAP-DF-002 — Exact coverage and continuity not yet measured

- Affected component: signal count, regime breadth and gap exclusions.
- Bias risk: sparse or concentrated sample.
- Blocks Cheap Prototype: `YES UNTIL RESOLVED`.
- Required mitigation: record first/last timestamp, row counts, duplicate/missing counts and contiguous-window eligibility before run.

### GAP-DF-003 — Historical rollover series not frozen

- Affected component: full economic interpretation for 24-hour/multi-day positions.
- Bias risk: overstated net expectancy.
- Blocks Cheap Prototype: `NO` for the narrow continuation question; `YES` for economic-viability claims.
- Required mitigation: keep PROTO-01 before-financing or add reproducible historical rollover inputs.

### GAP-DF-004 — Broker/account commission not selected

- Affected component: full net trading economics.
- Bias risk: overstated net expectancy.
- Blocks Cheap Prototype: `NO` for HYP-0001 primary quote-continuation test.
- Required mitigation: prohibit full-net claims and add explicit commission premise before Economic Pre-Screen.

### GAP-DF-005 — Raw-data redistribution rights not assumed

- Affected component: repository storage/sharing.
- Bias risk: none to the numerical claim; legal/operational distribution risk.
- Blocks Cheap Prototype: `NO` for local research.
- Required mitigation: keep raw source data local/external; commit metadata/hashes only unless rights are confirmed.

## Feasibility decision

- Decision: `CONDITIONAL`
- Decision reason: the required EUR/USD 1H BID/ASK fields, completed-bar semantics and historical access paths are documented and structurally sufficient for HYP-0001. However, ATS has not yet frozen and inspected the actual BID/ASK snapshot, measured exact coverage/continuity or acquired historical rollover inputs.
- Prototype constraints / limitations:
  1. `PROTO-01` may execute only after GAP-DF-001 and GAP-DF-002 are resolved in the actual Dataset Manifest.
  2. Use only exact aligned BID/ASK timestamps and the no-imputation contiguous-window policy above.
  3. Keep the frozen HYP-0001 24-bar breakout and 24-bar primary horizon unchanged.
  4. Primary result is limited to `QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING` unless rollover and commission inputs are explicitly added.
  5. No live-fill, slippage, profitability, validation or capital claim is permitted.
- Hypothesis reformulation required: `NO`.

This `CONDITIONAL` decision permits preparation of Cheap Prototype `PROTO-01`. It does not permit executing the prototype until the actual snapshot and coverage conditions are satisfied.

## External-source evidence reviewed

Dukascopy:

- Historical Data Export: https://www.dukascopy.com/swiss/english/marketwatch/historical/
- History Bars API: https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/history-bars/
- Historical Tester: https://www.dukascopy.com/wiki/en/forex-cfds/jforex/historical-tester/
- Time settings / market reopen behavior: https://www.dukascopy.com/wiki/en/forex-cfds/jforex/customizing-platform/
- Rollover: https://www.dukascopy.com/wiki/en/forex-cfds/account-management/rollovers/
- Terms of Use: https://www.dukascopy.com/swiss/sk/legal-pages/terms-of-use/

Secondary source candidate:

- Alpha Vantage API documentation: https://www.alphavantage.co/documentation/

## Next research artifact

`research/reviews/HYP-0001-PROTOTYPE-01.md`

Before any result is generated, PROTO-01 must record its data snapshot/manifest, fixed question, fixed metrics and pre-run decision rule.
