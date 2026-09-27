# HYP-0004 Data Feasibility Review

Task: `ATS2-RF-016`  
Hypothesis ID: `HYP-0004`  
Review status: `CONDITIONAL`  
Date: 26 September 2026

## 1. Decision question

Can ATS represent the fixed-UTC EUR/USD HYP-0004 structural claim with reproducible H1 BID/ASK data, exact one-hour continuity and an honest boundary-spread proxy before any HYP-0004 outcome is computed?

Current decision:

`CONDITIONAL`

ATS already has a frozen, hash-identified Dukascopy H1 BID/ASK development dataset that contains EUR/USD rows over a long pre-protected interval. That parent dataset is sufficient to justify a bounded preparation step, but HYP-0004 still requires a machine check that paired `bid_open/ask_open` fields are usable as a coherent boundary proxy and that only exact next-hour pairs enter the later structural test.

No HYP-0004 movement or spread comparison is calculated in this review.

## 2. HYP-0004 requirements carried into the review

HYP-0004 fixes:

- market: `FX_SPOT_OTC`;
- instrument: `EURUSD`;
- canonical timezone: `UTC`;
- `CORE_ACTIVE`: UTC hours 07 through 16 inclusive;
- `TRANSITION`: UTC hours 17 through 20 inclusive;
- `OFF_HOURS`: UTC hours 21 through 23 and 00 through 06 inclusive;
- decision boundary: hourly boundary;
- effect horizon: next exact one-hour boundary;
- movement outcome: absolute midpoint return;
- friction diagnostic: relative BID/ASK spread at the decision boundary;
- primary claim requires both predeclared inequalities to hold;
- no post-result clock-window search is allowed inside HYP-0004.

The Data Feasibility task must preserve all of those choices.

## 3. Reusable parent dataset

Primary development-data candidate:

`DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001`

Canonical manifest:

`data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001.yaml`

Canonical schema:

`data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV.schema.json`

Frozen prepared-data SHA-256:

`8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2`

Frozen source-bundle SHA-256:

`9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a`

Parent coverage:

`2003-08-03T21:00:00Z <= event_time <= 2021-08-31T23:00:00Z`

The parent dataset contains normalized H1 BID/ASK rows for nine G10-ex-USD currencies. For HYP-0004 only rows with:

- `currency = EUR`;
- `source_symbol = EURUSD`;
- `source_orientation = DIRECT`

may be retained.

This reuse is admitted because EUR/USD was fixed by HYP-0004 before this Data Feasibility review and no HYP-0004 result is used to select the parent dataset.

## 4. Source and access status

Source class:

Dukascopy historical H1 BID/ASK candles, as already frozen by the HYP-0003 development-data lineage.

Access status:

`PREVIOUSLY_ACQUIRED_AND_HASH_FROZEN_PARENT_DATASET`

RF-016 does not assume that the local parent CSV is present on every host. RF-017 must verify either:

1. the local prepared parent file exists and matches the frozen SHA-256; or
2. the parent dataset is reproduced under the already frozen HYP-0003 acquisition contract before deriving HYP-0004 data.

Failure to verify the parent identity is a technical/data block, not permission to substitute another vendor or an untracked CSV.

Licensing / redistribution:

raw provider bytes and prepared market data remain local/external and are not committed to Git. Git stores manifests, schemas, hashes, preparation code and research records.

## 5. Development coverage

HYP-0004 development reuse is limited to the parent dataset interval:

`2003-08-03T21:00:00Z <= event_time <= 2021-08-31T23:00:00Z`

This interval is development evidence only.

The existing HYP-0003 protected tail beginning `2021-09-01T00:00:00Z` is not automatically promoted into a HYP-0004 confirmatory block. Any later confirmatory or trading formulation must establish its own unseen-data boundary before reveal and account for any data already consumed by other ATS research lines.

RF-016 does not authorize acquisition or inspection of a later HYP-0004 outcome block.

## 6. Granularity and required fields

Required granularity:

`1H`

Required parent fields:

- `event_time`;
- `availability_time`;
- `currency`;
- `source_symbol`;
- `source_orientation`;
- `sequence`;
- `bid_open`;
- `ask_open`.

HYP-0004 does not require H1 high/low/close fields for its primary structural test.

Candidate boundary definitions for RF-017:

- `bid_t = bid_open`;
- `ask_t = ask_open`;
- `mid_t = (bid_t + ask_t) / 2`;
- next boundary is the row at exactly `event_time + 1 hour`.

No stale previous bar may substitute for a missing next-hour row.

## 7. Boundary BID/ASK coherence condition

The parent HYP-0003 record establishes that separately aggregated BID/ASK H1 extrema are not necessarily synchronous and therefore high/low fields must not be treated as executable paired quotes.

HYP-0004 uses only paired bar-open fields as a candidate boundary proxy.

Before any HYP-0004 outcome is calculated, RF-017 must verify for every retained EUR/USD boundary row used by the future prototype:

- BID and ASK originate from the same frozen parent row/event timestamp;
- both are finite and positive;
- `ask_open >= bid_open`;
- the source-format lineage is coherent under the frozen parent preparation;
- no synthetic spread repair, interpolation or side mixing is applied.

If these conditions cannot be satisfied reproducibly, HYP-0004 remains blocked and the bar-open proxy may not be silently replaced after seeing HYP-0004 results.

This Data Feasibility review does not claim that a paired H1 open is tick-exact. It admits it only as a declared bar-boundary development proxy subject to the RF-017 coherence check.

## 8. Time and continuity semantics

Canonical timezone:

`UTC`

Parent event time:

`H1 bar open`

Parent availability time:

`event_time + 1 hour`

HYP-0004 classification uses `event_time.hour` only. No DST transformation is applied to the fixed-UTC buckets.

A future HYP-0004 observation is eligible only when:

1. the boundary row at `t` passes the frozen quality rules;
2. the row at exactly `t + 1 hour` exists;
3. both rows are expected Dukascopy FX market hours under the existing market-hour calendar;
4. the pair does not bridge a weekend, holiday/closure or missing expected tradable-hour gap.

RF-017 may count eligible geometry by bucket and year. It may not calculate absolute-return medians, spread medians or the HYP-0004 decision.

## 9. Missing and bad data policy

- duplicate timestamp for EUR/USD: blocking;
- out-of-order row: blocking;
- malformed/non-positive `bid_open` or `ask_open`: blocking;
- `ask_open < bid_open`: blocking for the HYP-0004 boundary proxy;
- missing exact `t + 1h` row: observation excluded as non-contiguous and counted;
- expected closed-market gap: declared and never filled;
- missing expected tradable-hour row: counted explicitly and never interpolated;
- forward fill: prohibited;
- synthetic spread repair: prohibited;
- alternative-hour substitution: prohibited.

The future preparation result must expose all exclusions and the full denominator.

## 10. Information-time premise

At historical boundary `t`, only the timestamp and paired boundary BID/ASK proxy are treated as available for classification/diagnostic purposes.

The `t + 1h` boundary is an outcome.

RF-017 may create time/bucket labels and data-quality geometry, but it may not use the future boundary to:

- change the clock bucket;
- choose a different boundary lag;
- drop an otherwise valid date because its HYP-0004 result is unattractive;
- search alternate session definitions.

## 11. Revisions, corporate actions and universe risks

Revisions/restatements:

`NOT_APPLICABLE_TO_FROZEN_MARKET_QUOTE_SNAPSHOT`

Corporate actions:

`NOT_APPLICABLE_TO_SPOT_EURUSD`

Universe/survivorship:

`SINGLE_FIXED_INSTRUMENT`

Selection-bias risk remains relevant at the research-program level because EUR/USD and the fixed UTC windows were selected during hypothesis formation. That research choice is retained in history and is not erased by this review.

## 12. Transformation trace and future HYP-0004 dataset identity

RF-017 should derive a dedicated HYP-0004 development dataset from the frozen parent rather than mutate the parent file.

Planned dataset ID:

`DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001`

Planned local data path:

`data/derived/HYP-0004-DEV-01-EURUSD-H1.csv`

Planned manifest:

`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001.yaml`

Planned schema:

`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV.schema.json`

The derived dataset should retain only source/boundary fields needed for later HYP-0004 testing plus deterministic identity/order fields.

RF-017 must emit:

- verified parent dataset SHA-256;
- derived row count;
- derived dataset SHA-256;
- first/last retained timestamps;
- duplicate/out-of-order/malformed counts;
- boundary open-crossing count;
- exact-next-hour eligible/ineligible counts;
- eligible counts by `CORE_ACTIVE`, `TRANSITION`, `OFF_HOURS`;
- eligible counts by calendar year;
- information boundary `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

Counts of data geometry are allowed. Return/spread distribution summaries are not.

## 13. Cost and execution applicability

The RF-016/RF-017 path is a structural development test, not trading P&L.

Spread:

`REPRESENTED_AS_BOUNDARY_BID_ASK_PROXY`

Commission:

`NOT_APPLICABLE_TO_THE_PRIMARY_STRUCTURAL_CLAIM`

Financing / rollover:

`NOT_APPLICABLE_TO_THE_PRIMARY_NEXT_1H_STRUCTURAL_CLAIM`

Slippage / fill realism:

`NOT_MODELED`

A later directional trading rule would require a new economic/execution assessment. Passing HYP-0004 would not by itself establish a tradable edge.

## 14. Known gaps

Blocking before any HYP-0004 outcome:

1. current-host availability and exact SHA-256 identity of the frozen parent CSV must be verified;
2. the EUR/USD subset must be derived deterministically from the frozen parent identity;
3. paired `bid_open/ask_open` boundary coherence must be checked;
4. exact-next-hour continuity counts must be measured without filling gaps;
5. a dedicated HYP-0004 derived dataset hash and manifest/schema must be frozen.

Not blocking for RF-017 preparation:

- commission schedule;
- financing/swap schedule;
- live slippage model;
- later confirmatory-block definition.

Those items constrain later trading interpretation, not the present structural data question.

## 15. Information boundary

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

RF-016 has not calculated:

- any `abs_next_1h_return`;
- any `relative_spread` distribution summary;
- any bucket mean or median;
- either primary HYP-0004 inequality;
- any trading P&L.

## 16. Feasibility decision

Decision:

`CONDITIONAL`

Decision reason:

The frozen HYP-0003 development dataset provides a reproducible, hash-identified EUR/USD H1 BID/ASK parent with UTC bar-open semantics and long development coverage. This is sufficient to justify a dedicated HYP-0004 preparation step without selecting data from HYP-0004 performance. The remaining blocking conditions are mechanical: verify the exact parent identity on the OWNER host, derive the EUR/USD subset, enforce paired boundary-open coherence, and freeze exact-next-hour geometry before any HYP-0004 outcome is calculated.

Prototype authorization:

`NOT_YET_AUTHORIZED`

Hypothesis reformulation required:

`NO`

## 17. Next task

After exact-head OWNER launcher PASS:

`ATS2-RF-017 — HYP-0004 development data preparation`

RF-017 must materialize/freeze the HYP-0004 development-data candidate and report only identity, quality and geometry facts under:

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

A later task must review/freeze that prepared dataset before the HYP-0004 structural prototype can be revealed.

## 18. RF-018 development data freeze update

Task: `ATS2-RF-018`

This update canonicalizes the exact RF-017 OWNER PASS result before any HYP-0004 outcome is calculated. It supersedes the unresolved development-data facts in Sections 12, 14, 16 and 17 while preserving the historical `CONDITIONAL` review decision and its limitations.

### 18.1 Canonical RF-017 preparation result

Exact-main OWNER launcher PASS was obtained on:

`ae9767a71b3860e55d345afb34b2f9c18b5dd063`

Canonical result:

`reports/research/HYP-0004-DEVELOPMENT-DATA-PREP-result.json`

RF-017 recorded:

- preparation decision: `READY_FOR_DEVELOPMENT_DATA_FREEZE`;
- parent dataset: `DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001`;
- verified parent dataset SHA-256: `8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2`;
- parent source-bundle SHA-256: `9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a`;
- derived dataset: `DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001@1.0.0`;
- derived rows: `112900`;
- derived CSV SHA-256: `3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6`;
- first event time: `2003-08-03T21:00:00Z`;
- last event time: `2021-08-31T23:00:00Z`;
- exact-next-hour eligible rows: `111938`;
- boundary-open crossings: `0`;
- duplicate timestamps: `0`;
- out-of-order timestamps: `0`;
- malformed boundary rows: `0`;
- information boundary: `NO_HYPOTHESIS_OUTCOME_COMPUTED`.

No HYP-0004 primary claim was evaluated.

### 18.2 Frozen exact-next-hour geometry

Total retained rows by UTC bucket:

| Bucket | Total rows | Exact-next-hour eligible |
|---|---:|---:|
| `CORE_ACTIVE` | 47021 | 47012 |
| `TRANSITION` | 18806 | 18189 |
| `OFF_HOURS` | 47073 | 46737 |

Ineligible denominator:

- declared closed-market next hour: `940`;
- missing expected tradable next hour: `21`;
- right-edge dataset boundary: `1`.

The totals reconcile exactly:

`111938 + 940 + 21 + 1 = 112900`

No ineligible row is shifted to another horizon or filled synthetically.

### 18.3 Frozen development dataset identity

Dataset:

`DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001@1.0.0`

Canonical manifest:

`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001.yaml`

Canonical row schema:

`data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV.schema.json`

Prepared local bytes:

`data/derived/HYP-0004-DEV-01-EURUSD-H1.csv`

A change to the parent dataset identity, derived digest, coverage, UTC bucket mapping, exact-next-hour eligibility rule, boundary availability mode or row schema is a material dataset change and may not silently replace this version.

### 18.4 Frozen boundary timing limitation

Boundary availability mode:

`H1_OPEN_PROXY_AT_EVENT_TIME`

Exact tick boundary time known:

`false`

The parent completed-H1 lineage still records parent-row availability at `event_time + 1 hour`, while the derived development dataset treats the H1 open as a boundary proxy available at `event_time`.

This is an explicit approximation, not a claim that the first executable tick is known to occur exactly at the hourly boundary.

Any HYP-0004 prototype conclusion must therefore be limited to the frozen H1 bar-open proxy. A later trading/execution claim would require a separate timing/execution assessment and may require finer-grained data.

### 18.5 RF-018 freeze decision

Freeze decision:

`FREEZE_DEVELOPMENT_DATASET`

Reason:

RF-017 verified the exact frozen parent identity, deterministically retained the preselected EUR/USD rows, found no duplicate/out-of-order/malformed/boundary-crossing violations, exposed the full exact-next-hour denominator and produced a stable derived-data digest with substantial eligible geometry in both primary HYP-0004 buckets.

The Data Feasibility decision remains:

`CONDITIONAL`

The condition is now encoded as a frozen limitation rather than an unresolved preparation blocker: HYP-0004 development uses `H1_OPEN_PROXY_AT_EVENT_TIME`, while exact tick boundary timing remains unknown.

Prototype protocol freeze is authorized on this exact dataset and timing approximation.

Prototype outcome calculation is **not** authorized during RF-018.

Hypothesis reformulation required:

`NO`

### 18.6 Information boundary

`NO_HYPOTHESIS_OUTCOME_COMPUTED`

RF-018 freezes metadata, bytes identity, quality counts and time/bucket geometry only.

It does not calculate:

- `abs_next_1h_return`;
- `relative_spread`;
- any return/spread mean, median or quantile by bucket;
- either primary HYP-0004 inequality;
- any trading P&L.

### 18.7 Next task

After exact-main OWNER launcher PASS for RF-018:

`ATS2-RF-019 — HYP-0004 PROTO-01 freeze`

RF-019 must freeze one pre-written structural prototype question, exact metrics and the two primary HYP-0004 inequalities before the first development reveal.

