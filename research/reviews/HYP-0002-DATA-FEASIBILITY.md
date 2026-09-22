# Data Feasibility Review — HYP-0002 EUR/USD 1H Two-Sided Return-Tail Reversal

## Identity

- Hypothesis ID: `HYP-0002`
- Review status: `CONDITIONAL`
- Reviewed on: `2026-09-22`
- Reviewer role: `DATA / RESEARCH`

## Hypothesis summary

- Statement summary: after an extreme development-calibrated 24H EUR/USD move, both upper-tail/DOWN and lower-tail/UP 24H executable reversal returns must have positive means and exceed their same-direction unconditional baselines on a previously unseen block.
- Market / universe context: `FX_SPOT_OTC / EURUSD`
- Decision/effect horizon: completed `1H` decision bars, `24H` prior-return lookback, `24H` effect horizon.
- Decision-time information premise: signal uses completed BID/ASK closes only; thresholds are frozen from development data; confirmatory thresholds may not be recalibrated; execution measurement starts at the next eligible open.

## Development threshold freeze

Development dataset:

`DATA-DUKASCOPY-EURUSDH1-PROTO01-001@1.0.0`

Development prepared CSV SHA-256:

`aeda05d90994259a22e25d882398218aead968941fe0b1c73eb34894841291c0`

Eligible development threshold observations:

`18,485`

Frozen thresholds:

- `Q10_DEV = -0.005141454111`
- `Q90_DEV = 0.005394148971`

These values are fixed before any HYP-0002 confirmatory outcome is observed.

## Required information and actual source

Required data categories:

- EUR/USD 1H BID/ASK OHLC;
- explicit ordered event and availability timestamps;
- session/weekend gap semantics;
- next-open quote values for two-sided executable-return measurement;
- dataset/source identity and integrity hashes.

Actual confirmatory source:

`Dukascopy EURUSD 1H BID + ASK historical candles`

Acquisition/freeze date:

`2026-09-22`

Acquisition path:

`tools/hyp0002_data_feasibility.py`

Access was verified by successful acquisition and preparation of all 16 required monthly side files.

Raw Dukascopy files remain local/external. Redistribution rights are not assumed.

## Confirmatory dataset identity

Dataset ID:

`DATA-DUKASCOPY-EURUSDH1-HYP0002-001@1.0.0`

Canonical manifest:

`data/manifests/DATA-DUKASCOPY-EURUSDH1-HYP0002-001.yaml`

Prepared CSV SHA-256:

`d62a7103478da2a79a0992310005bcd0afc8dc0010088dccd2ed0e54e2ec112f`

Source bundle SHA-256:

`ccbf5ceff1ee1a5a1cb62dead3af531ce05ae4f71e4da32140b526326e686392`

Source files:

`16`

Preparation commit:

`8b1e2dbc0e604c7fb3ca8297e0f61f252147619a`

## Coverage

- Earliest usable timestamp: `2026-01-01T00:00:00Z`
- Latest usable timestamp: `2026-08-31T23:00:00Z`
- Aligned BID/ASK rows: `4,153`
- Missing tradable hours: `0`
- Detected session/data gaps: `35`
- Maximum gap: `49 hours`
- Eligible 24-before/24-after timestamps: `2,414`
- Instrument breadth: one instrument, `EURUSD`
- Historical constituent membership: `NOT_APPLICABLE`

The 35 gaps remain explicit and break continuity. No gap is filled.

## Granularity and field semantics

- Required granularity: `1H`
- Available granularity: `1H`
- Required fields: BID/ASK OHLC, event time, availability time, deterministic sequence.
- Signal feature: `MID_CLOSE = (BID_CLOSE + ASK_CLOSE) / 2`
- UP execution measurement: next eligible ASK open to BID open 24 eligible hours later.
- DOWN execution measurement: next eligible BID open to ASK open 24 eligible hours later.
- Aggregation limitation: 1H bars cannot establish intra-hour path or actual live fills.

## Time semantics

- Source/canonical research timezone: `UTC`
- Timestamp representation: RFC3339.
- Event time: bar-open timestamp.
- Availability time: one hour after event time for the fully formed 1H bar.
- Session handling: closed-market hours are excluded using the same declared FX calendar rule as the development preparation.
- DST handling: UTC plus the declared market-hour calendar; no local-wall-clock feature logic.
- Decision-time availability: only completed bars and frozen thresholds may create a signal.

## Revisions and corrections

- Source history may be corrected or replaced by the provider.
- Point-in-time correction vintages are not established.
- Prototype handling rule: the exact prepared CSV and source-bundle hashes above are frozen. A changed source snapshot is a material data change and may not silently replace this dataset version.

## Corporate actions / instrument lifecycle

- Corporate actions: `NOT_APPLICABLE`
- Split/dividend adjustments: `NOT_APPLICABLE`
- Delisting/expiry: `NOT_APPLICABLE` in the equity/futures sense.
- Relevant lifecycle risk: source/feed and market-session convention changes.

## Missing and bad data

- Missing observation policy: `ALLOW_DECLARED_GAPS / FAIL_WINDOW`
- Duplicate timestamp policy: `REJECT`
- Out-of-order policy: `REJECT`
- Bad/impossible values: reject non-positive or inconsistent OHLC and ASK-open-below-BID-open observations.
- BID/ASK alignment: exact timestamp match required.
- Stale data: repeated prices are not automatically removed.
- Feed outages: remain visible as gaps; no interpolation or forward fill.

## Universe and selection risks

- Survivorship risk: low/not applicable to a single current major FX pair.
- Historical universe membership risk: `NOT_APPLICABLE`
- Selection bias risk: material. HYP-0002 was formulated after a 16-alternative discovery search on EUR/USD 2021–2025.
- Mitigation: retain the full discovery denominator and never represent the 2026 block as independent examination evidence.

## Leakage and overlap risks

- The 2021–2025 block is development-only and cannot become confirmatory evidence.
- `Q10_DEV` and `Q90_DEV` are frozen from development and cannot be recalculated on the 2026 block.
- Same-close execution is prohibited.
- 24H forward windows may overlap and create dependent observations.
- Future-known normalization is prohibited.
- The confirmatory block was frozen before outcome calculation.
- Information boundary at preparation: `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

## Transformation trace and dataset identity

- Source identity: Dukascopy monthly EURUSD H1 BID/ASK candle files.
- Source bundle: 16 files, SHA-256 `ccbf5ceff1ee1a5a1cb62dead3af531ce05ae4f71e4da32140b526326e686392`.
- Preparation code: `tools/hyp0002_data_feasibility.py@8b1e2dbc0e604c7fb3ca8297e0f61f252147619a`
- Prepared dataset: `data/derived/HYP-0002-CONFIRM-01-EURUSD-H1.csv`
- Prepared CSV SHA-256: `d62a7103478da2a79a0992310005bcd0afc8dc0010088dccd2ed0e54e2ec112f`
- Dataset Manifest: `data/manifests/DATA-DUKASCOPY-EURUSDH1-HYP0002-001.yaml`

## Cost and execution inputs

### Spread

`AVAILABLE_FROM_DATA`

The UP/DOWN executable-return definitions cross the appropriate ASK/BID sides, so quoted spread is represented directly.

### Commission

`NOT_SELECTED / BROKER_ACCOUNT_SPECIFIC`

No broker/account is selected. The cheap prototype may not claim fully net economics.

### Financing / rollover

`MATERIAL_BUT_NOT_FROZEN`

A 24H window can cross settlement. Financing is not represented in the prepared dataset.

### Slippage / latency

`NOT_AVAILABLE_FROM_1H_BAR_DATA`

Next-open quote measurements are not guarantees of live fills.

## Known gaps

### GAP-DF2-001 — Commission not frozen

- Affected component: full net trading economics.
- Bias risk: may overstate economically realizable return.
- Blocks cheap test: `NO` for the narrow HYP-0002 quote-return claim.
- Required mitigation: label the prototype before-commission and prohibit full-net claims.

### GAP-DF2-002 — Financing/rollover not frozen

- Affected component: full economic interpretation of 24H holding windows.
- Bias risk: may overstate or understate net economics.
- Blocks cheap test: `NO` for the narrow directional/effect claim; `YES` for full economic viability.
- Required mitigation: use the label `QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING` and freeze financing before Economic Pre-Screen.

### GAP-DF2-003 — 1H bars are quote measurements, not live fills

- Affected component: execution realism.
- Bias risk: unknown slippage/latency.
- Blocks cheap test: `NO`.
- Required mitigation: prohibit live-fill claims.

### GAP-DF2-004 — Dependence and overlap

- Affected component: inference from 2,414 eligible windows.
- Bias risk: raw counts overstate independent information.
- Blocks cheap test: `NO`.
- Required mitigation: report event counts and overlap/dependence; do not use naive IID significance as validation evidence.

### GAP-DF2-005 — Raw-data redistribution rights not assumed

- Affected component: repository storage/sharing.
- Bias risk: none to the numerical claim.
- Blocks cheap test: `NO`.
- Required mitigation: keep source files and prepared market bytes local/external; commit manifest metadata/hashes only.

## Feasibility decision

- Decision: `CONDITIONAL`
- Decision reason: the frozen development thresholds, disjoint confirmatory BID/ASK dataset, explicit UTC/timing semantics, complete tradable-hour coverage and integrity hashes are sufficient to execute one honest HYP-0002 cheap confirmatory test. Commission, financing and live-fill realism remain unresolved, so the result cannot support full-net economic or execution claims.
- Prototype constraints / limitations:
  1. use exactly `Q10_DEV=-0.005141454111` and `Q90_DEV=0.005394148971`;
  2. use only `DATA-DUKASCOPY-EURUSDH1-HYP0002-001@1.0.0`;
  3. evaluate both reversal sides and all four HYP-0002 inequalities;
  4. do not recalibrate thresholds, horizons or directions on the confirmatory block;
  5. label the result `QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING`;
  6. preserve overlap/dependence diagnostics;
  7. do not describe the result as validation, independent evidence, live execution or profitability proof.
- Hypothesis reformulation required: `NO`

This decision permits a Cheap Prototype only under the constraints above.

## Next research artifact

`research/reviews/HYP-0002-PROTOTYPE-01.md`

The prototype protocol must be frozen before the first HYP-0002 outcome calculation.
