# Source code

ATS is in `M3_REFERENCE_STRATEGY_1`; the reusable M2 research-platform baseline is complete.

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
└── runner/
```

M2 is not DataFrame-first and does not baseline pandas, Polars, PyArrow, DuckDB, an external backtesting framework, Docker, broker adapters or live execution. Such capabilities are added only after a real consumer demonstrates the need.

A concrete Reference Strategy #1 is not selected until M3. Deterministic synthetic software fixtures used for platform tests are not research entities or trading evidence.

The M2 environment, Dataset Manifest, loader, Strategy/Research interface, replay, cost model, analytics/report, manifest-driven runner and end-to-end acceptance/regression baseline are complete. M2 Exit decision is `PASS`; M3 now uses this platform against a real Reference Strategy selection process.


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

M2 Exit is recorded in `governance/program/M2_EXIT_REVIEW.md`. M3-001 selected `SINGLE_INSTRUMENT_DAILY_LONG_FLAT_TREND_BREAKOUT` as the first reference strategy class. The next step is `ATS2-M3-002 — Idea & rationale`; no shared source-code capability is added until the real research consumer demonstrates a need.
