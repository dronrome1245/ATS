# ADR-0001 — M2 Research Stack

**Task:** `ATS2-M2-001`  
**Work package:** `WBS-2.1`  
**Status:** ACCEPTED  
**Date:** 16 September 2026  
**Consumer contract:** `governance/program/REFERENCE_CONSUMER_PROFILE.md`

## 1. Context

M2 must build the minimum reproducible Research Platform MVP before a concrete Reference Strategy #1 is selected.

The stack therefore must support the abstract M2 consumer:

`ordered dataset → typed research logic → deterministic replay → explicit costs → analytics/result → reproducible rerun`.

The decision must optimize for research correctness, auditability, reproducibility and low implementation burden. It must not optimize prematurely for live execution, distributed scale, ultra-low latency, news ingestion or a specific market/data vendor.

## 2. Decision

ATS M2 uses the following baseline stack.

### Runtime

- **CPython 3.13 series** as the supported M2 runtime line.
- Standard GIL-enabled interpreter; free-threaded/experimental runtime modes are out of scope for M2.
- Exact patch version is pinned by `WBS-2.2 Reproducible environment` rather than this ADR.

### Project and environment management

- **`pyproject.toml`** is the canonical project/dependency/tool configuration.
- **uv** is the package/environment/lock tool.
- **`uv.lock`** is committed and is the canonical resolved dependency lock for M2.
- A repository-local virtual environment is the normal development model.
- Conda/Poetry/pip-tools are not part of the baseline toolchain.

### Runtime dependencies

Keep the dependency surface intentionally small:

1. **Pydantic v2** — typed validation/serialization of Dataset Manifest, run configuration and other machine contracts.
2. **PyYAML 6.x** — safe YAML loading for existing ATS manifests; loaded structures are validated by typed models.
3. **NumPy 2.x** — baseline numerical arrays/statistics/analytics where the standard library is insufficient.

Exact package versions are resolved and pinned during `WBS-2.2`.

### Development dependencies

- **pytest** — unit, deterministic fixture and regression tests.
- **Ruff** — linting and formatting.

Additional type-checker/static-analysis tools are deferred until they solve an observed development problem.

## 3. Data representation decision

M2 is **not DataFrame-first**.

The core loader/replay contract is a typed ordered iterator/sequence of records. Strategy/research logic consumes one deterministic observation/event at a time through the research interface.

Initial supported fixture/reference storage may use:

- CSV for deterministic small tabular fixtures;
- JSON for machine-readable results;
- YAML for manifests/configuration.

The loader architecture must isolate storage format behind a data interface so Parquet/Arrow or another format can be added without changing Strategy/Replay semantics.

Parquet, pandas, Polars, PyArrow and DuckDB are not baseline dependencies. They may be introduced when a real dataset/consumer shows that the benefit exceeds the additional dependency and semantic surface.

## 4. Time and ordering model

- Python timezone-aware `datetime` plus standard `zoneinfo` are the baseline time representation.
- Internal normalized timestamps may use UTC, but source/event/availability semantics remain explicit in Dataset Manifest metadata.
- Equal-timestamp records require an explicit deterministic tie-break key.
- Replay order is determined by dataset semantics, never by filesystem iteration, dictionary order assumptions or wall-clock time.

## 5. Typed contract model

Pydantic models are used only at boundaries where external configuration/artifacts enter or leave the platform.

Examples:

- Dataset Manifest;
- run/experiment configuration;
- cost-model configuration;
- machine-readable result schema.

Hot replay loops should use small Python dataclasses/immutable typed records where appropriate rather than repeatedly invoking runtime validation.

This keeps boundary validation strong without coupling every internal operation to a validation framework.

## 6. Minimal package layout

The planned Python source layout is:

```text
src/ats/
├── schemas/      # machine contracts / validated boundary models
├── data/         # dataset manifests, readers, ordered records
├── strategy/     # broker-independent research interface
├── replay/       # deterministic replay/backtest core
├── costs/        # explicit cost-model interface
├── analytics/    # baseline metrics/result builders
└── runner/       # manifest/config-driven orchestration
```

Test fixtures live under `tests/` and must not be placed in Research Factory registries.

Exact module/class/function names are implementation details for WBS-2.3 through WBS-2.9.

## 7. Determinism rules imposed by the ADR

M2 code must avoid hidden inputs.

A replay result may depend only on declared inputs such as:

`code revision + runtime/environment + dataset version + config + seed/protocol + cost assumptions`.

Consequences:

- no live network calls in deterministic fixture/replay tests;
- no dependency on current wall-clock time for research decisions;
- randomness must use an explicit seed/protocol;
- ordering must be explicit and stable;
- numerical comparisons use a documented tolerance where exact bit equality is not a valid cross-environment requirement;
- derived output never silently mutates the preregistered Experiment manifest.

## 8. Cost model architecture

Costs are injected through an interface/configuration and are never global hidden constants.

Baseline representation must allow applicable components such as:

- commission/fees;
- spread;
- slippage/proxy.

The architecture permits later cost components, but M2 does not invent borrow, funding, market impact or venue-specific models without a real consumer.

## 9. Analytics architecture

The baseline analytics layer consumes replay outputs and produces serializable results. It is not the place for strategy decisions.

It must support, when meaningful:

- gross versus net effect/P&L;
- modeled costs;
- opportunity/event/trade counts;
- equity/path and drawdown measures when monetary semantics exist;
- diagnostics/anomalies;
- deterministic machine-readable output compatible with ATS Experiment result artifacts.

Metrics that are not meaningful remain explicit `NOT_APPLICABLE`/absent by schema rule rather than fabricated zeros.

## 10. Experiment integration

M2 runner reads the registered pre-result context but does not own research interpretation.

Boundary:

`manifest.yaml → resolve frozen inputs → execute deterministic run → result.json-compatible facts → conclusion.md remains review/interpretation`.

The Experiment Registry remains an index only.

Infrastructure software fixtures do not receive `EXP-...` IDs and are not evidence.

## 11. Testing approach

M2 quality gates use:

- unit tests for manifest validation, ordering, replay transitions, cost calculations and analytics;
- deterministic synthetic non-market fixtures;
- golden/regression outputs where stable semantics are intentional;
- repeated-run equality/tolerance checks;
- repository validator plus platform tests in CI.

CI may continue to run governance validation independently of the research environment. WBS-2.2 will define the Python/runtime matrix and platform test commands.

## 12. Alternatives considered

### Python 3.14 as immediate baseline

Not selected for M2 baseline. The project prioritizes a mature scientific/research compatibility line over adopting the newest feature series immediately. Upgrade remains possible by ADR amendment after reproducibility tests pass.

### pandas-first platform

Rejected as a baseline architectural dependency. DataFrames are useful for exploratory analysis, but a DataFrame-first replay contract can hide ordering/index/mutation semantics that ATS must make explicit. pandas can be added at the analysis edge later without becoming the Strategy API.

### Polars / Arrow / DuckDB / Parquet-first stack

Deferred. These are useful for larger real datasets, but M2 has no confirmed volume/performance consumer yet. The data interface must allow adding them later.

### Existing backtesting framework as the core engine

Rejected for M2. Framework-specific execution/order semantics would become implicit platform policy before ATS has selected Reference Strategy #1. ATS needs a small explicit replay model whose assumptions are owned by its Experiment/Data contracts.

### Rust/C++ core

Rejected for M2. There is no demonstrated latency/throughput need that justifies cross-language build/tooling complexity.

### Mandatory Docker/containers

Deferred. Reproducibility first uses pinned CPython + uv lock + deterministic fixtures. Containerization can be added if machine-level differences become material or production deployment later requires it.

### Notebook as execution source of truth

Rejected. Notebooks remain valid exploratory tools, but formal M2 runs are package/runner driven and versionable.

## 13. Consequences

### Positive

- small dependency surface;
- deterministic event semantics remain visible;
- no premature broker/live coupling;
- easy unit/regression testing;
- clean fit with M1 Experiment/Data contracts;
- room to add higher-performance storage/data tools later behind interfaces.

### Costs / limitations

- initial loader may be less convenient than DataFrame-first research;
- high-volume tick datasets may later require Arrow/Parquet/Polars/DuckDB or optimized readers;
- Python replay performance may eventually require profiling-driven optimization;
- exact cross-platform floating-point bit equality is not promised unless the relevant algorithm permits it.

These are accepted because M2 is a correctness/reproducibility MVP, not the final production engine.

## 14. Constraints for WBS-2.2 onward

`ATS2-M2-002 — Reproducible environment` must materialize this ADR through at least:

- exact supported CPython patch selection;
- `pyproject.toml`;
- committed `uv.lock`;
- documented `uv sync` / `uv run` workflow;
- pinned runtime/dev dependencies;
- CI command for platform tests;
- environment fingerprint/version reporting.

Later M2 work must preserve the architecture boundary that Strategy/Research logic does not call broker/live services.

## 15. Decision status

**ACCEPTED.**

This ADR is sufficient to start `WBS-2.2` and `WBS-2.3` design work. Under current WIP discipline the next program-level ready task is `ATS2-M2-002 — Reproducible environment`.
