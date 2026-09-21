# Source code

ATS is in `M4_VALIDATION_FRAMEWORK`; the reusable M2 research-platform baseline and M3 Reference Strategy #1 research cycle are complete.

Canonical stack decision:

`governance/decisions/ADR-0001-RESEARCH-STACK.md`

Canonical materialized environment:

`governance/program/RESEARCH_ENVIRONMENT_SPEC.md`

M2 source code uses:

- CPython `3.13.15` as the exact reproducibility baseline;
- uv `0.12.13` + `pyproject.toml` + committed `uv.lock`;
- Pydantic `2.13.5` + PyYAML `6.0.3` at manifest/config boundaries;
- NumPy `2.5.3` for baseline numerical analytics;
- standard-library CSV/JSON and a typed ordered-record interface for the initial loader/replay path;
- pytest `9.1.1` + Ruff `0.16.7` for the current quality baseline.

Planned package boundary:

```text
src/ats/
├── schemas/
├── data/
├── strategy/
├── replay/
├── costs/
├── analytics/
├── runner/
└── validation/
```

M2 is not DataFrame-first and does not baseline pandas, Polars, PyArrow, DuckDB, an external backtesting framework, Docker, broker adapters or live execution. Such capabilities are added only after a real consumer demonstrates the need.

M3 selected and tested Reference Strategy #1. Its HYP-0001 / PROTO-01 research line was rejected at R3. Deterministic synthetic software fixtures remain software evidence only and are not trading evidence.

The M2 environment, Dataset Manifest, loader, Strategy/Research interface, replay, cost model, analytics/report, manifest-driven runner and end-to-end acceptance/regression baseline are complete. M2 Exit decision is `PASS`; M3 then used the platform on real EUR/USD BID/ASK research data and correctly stopped the first hypothesis at Cheap Prototype.


## Implemented M2 boundary

`ATS2-M2-003` materializes the first typed platform boundary:

- `ats.schemas.dataset_manifest.DatasetManifest`;
- `ats.schemas.dataset_manifest.load_dataset_manifest`;
- safe YAML parsing plus immutable Pydantic validation;
- explicit event-time / information-availability semantics;
- deterministic ordering/tie-break metadata;
- quality, lineage and integrity metadata.

`ATS2-M2-004 — Base data loader` is now materialized in `ats.data.loader`. It consumes the Dataset Manifest contract rather than inventing dataset semantics in code.


## Base loader boundary

Implemented loader behavior:

- immutable `LoadedRecord` / `LoadedDataset`;
- UTF-8 CSV reference format;
- RFC3339 timezone-aware event and availability times;
- deterministic ordering and tie-breaks;
- explicit duplicate/malformed/out-of-order policies;
- SHA-256 integrity verification;
- manifest coverage enforcement;
- stable manifest storage location in output instead of host-specific absolute paths.

Generic missing-event inference is intentionally absent because the Manifest does not define a universal calendar/frequency.

`ATS2-M2-005 — Minimal Strategy research interface` is materialized in `ats.strategy.interface`.


## Strategy / Research interface boundary

Implemented M2-005 contract:

- immutable `ResearchRunContext`;
- immutable `ResearchObservation` bridged from `LoadedRecord`;
- broker-neutral `ResearchDecision` with canonical JSON serialization;
- serializable `ResearchDiagnostic`;
- generic immutable `StrategyStep[state]`;
- `ResearchStrategy[state]` protocol with deterministic `initial_state` and `on_observation` boundaries;
- decision payload restricted to finite JSON scalar values in the M2 baseline.

The interface supplies no wall clock, network, broker, account, portfolio allocation or live-risk object.

`ATS2-M2-006 — Deterministic backtest/replay` is materialized in `ats.replay.engine`.


## Deterministic replay boundary

Implemented M2-006 behavior:

- `run_replay` consumes `LoadedDataset + ResearchRunContext + ResearchStrategy`;
- loader records are bridged into `ResearchObservation` in their existing deterministic order;
- `initial_state` is called once per replay;
- `on_observation` is called exactly once per record;
- immutable `ReplayFrame` records observation, state-before/state-after, decisions and diagnostics;
- `ReplayResult` binds dataset identity/version/hash/context and exposes ordered flattened decisions/diagnostics;
- availability time may not move backward in the single-stream M2 replay;
- a decision may not claim a time earlier than the current observation's availability time;
- no wall clock, network, broker, costs or analytics are injected by the engine.

`ATS2-M2-007 — Cost model interface` is materialized in `ats.costs.interface`.

## Cost model interface boundary

Implemented M2-007 behavior:

- immutable `CostComponentConfig / CostModelConfig` with ordered unique component names;
- applicable components require explicit parameters and receive no numeric defaults;
- `CostApplicability.NOT_APPLICABLE` requires an explicit reason and carries no hidden zero;
- immutable `CostInput` stays outside Strategy logic and contains only declared JSON-scalar attributes;
- `CostComponentResult / CostResult` serialize modeled costs separately from gross/net performance;
- each applicable result has an explicit finite numeric value and unit;
- `CostModel` is a deterministic protocol over explicit input + config only;
- `apply_cost_model` rejects mismatched input identity, omitted/reordered components or changed applicability.

`ATS2-M2-008 — Standard analytics/report` is materialized in `ats.analytics.standard`.

## Standard analytics/report boundary

Implemented M2-008 behavior:

- `build_standard_analytics` binds deterministic replay identity/counts to explicitly declared economic semantics;
- `EffectSeries` requires finite ordered increments, a non-empty semantic definition and an explicit unit;
- gross effect, modeled costs and net effect remain separate fields;
- modeled cost totals exist only when at least one applicable component exists and all applicable component units are compatible;
- net effect exists only when gross effect and modeled cost total use the same unit;
- effect count/mean/min/max and absolute cumulative max drawdown are deterministic when an effect series is applicable;
- `NotApplicable` prevents missing economic/trade semantics from becoming invented zeroes or metrics;
- Strategy decisions remain decisions; trade/event/opportunity count is a separate explicit input;
- `StandardAnalyticsResult.to_json()` produces canonical machine-readable output using result sections compatible with the Experiment result vocabulary;
- `StandardAnalyticsResult.to_markdown()` provides a deterministic minimum human-readable report.

No return percentage, Sharpe, win rate, capital utilization, market-specific P&L or trade semantics are invented by this baseline.

`ATS2-M2-009 — Manifest-driven experiment runner` is materialized in `ats.runner.experiment`.

## Manifest-driven experiment runner boundary

Implemented M2-009 behavior:

- `RegisteredExperimentContext` is the immutable frozen preregistration subset consumed by the runner;
- `ExperimentRunResult` is the deterministic machine-readable result object emitted after execution;
- registered manifest bytes are read using safe YAML and SHA-256 bound without modification;
- only `REGISTERED / REGISTERED_EXPERIMENT` context is executable by the M2 runner;
- code revision, implementation reference and environment ID are matched against explicit resolved runtime identity;
- Dataset ID/source snapshot are matched against the Dataset Manifest before loading;
- registered parameters/configuration/random seed become `ResearchRunContext`;
- registered structured cost components become `CostModelConfig`, while `NOT_APPLICABLE` costs remain explicit;
- the runner composes existing loader → replay → costs → analytics capabilities without duplicating their logic;
- registered primary/secondary metric names must exist in the standard analytics result surface;
- completion timestamp is explicit input; no wall clock is injected;
- result output records registered manifest SHA-256 plus dataset version/hash for reproducibility;
- implementation references are not dynamically imported or executed from manifest text.

`ATS2-M2-010 — Research platform tests` materializes the Reference Consumer Profile acceptance fixture in `tests/test_research_platform.py` plus `tests/fixtures/platform/reference_consumer_expected.json`.

M2 Exit is recorded in `governance/program/M2_EXIT_REVIEW.md`. M3-001 selected `SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT` as the first reference strategy class. M3 Reference Strategy #1 is recorded as `COMPLETED / PASS`, while HYP-0001 itself is `REJECTED_AT_R3`. M4-001 defines the reusable Validation Framework. `ATS2-M4-002 — Parameter sensitivity tooling` materializes `ats.validation.sensitivity`; next is `ATS2-M4-003 — Time/regime slicing`.


## M4 validation tooling

`ats.validation.sensitivity` evaluates a caller-declared ordered parameter neighbourhood.

It preserves every declared variant, requires an exact declared metric set, rejects non-finite values, and emits `selection_policy = NO_AUTOMATIC_SELECTION`. It deliberately has no best/winner/ranking API.

The software fixture is synthetic and creates no Candidate, Strategy Version, Experiment or validation evidence by itself.


## M4 declared slicing

`ats.validation.slicing` evaluates caller-declared time/regime slices without selective omission.

It reports every declared slice in plan order, exposes unassigned and multiply-assigned observation counts, and requires explicit policies for exhaustiveness, overlap and empty slices. Unknown slice IDs and metric-contract violations fail closed.

The synthetic slicing fixture is software-only and creates no validation evidence.


## M4 concentration diagnostics

`ATS2-M4-004 — Observation concentration analysis` materializes this capability.

`ats.validation.concentration` retains every supplied observation and optional group while measuring how much absolute effect is concentrated in predeclared top-count diagnostics.

The result declares `NO_AUTOMATIC_OUTLIER_REMOVAL`. Ranking by absolute magnitude is diagnostic only; it does not delete observations or change the underlying evidence.

The synthetic fixture is software-only and creates no validation evidence.
