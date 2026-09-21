# Tests

ATS is in `M2_RESEARCH_PLATFORM_MVP`.

Canonical environment baseline:

- `governance/program/RESEARCH_ENVIRONMENT_SPEC.md`;
- `pyproject.toml`;
- `.python-version`;
- `uv.lock`.

## Current M2 test baseline

`tests/test_environment_baseline.py` verifies that the frozen environment uses the exact supported CPython patch and direct dependency versions.

Canonical command:

```bash
uv run --frozen pytest tests/test_environment_baseline.py
```

This test is infrastructure verification only. It does not create an Idea, Hypothesis, Candidate, Experiment or trading evidence.

## Dataset Manifest tests

`tests/test_dataset_manifest.py` validates the canonical synthetic Manifest, safe YAML loading, immutable typed parsing, timestamp/availability rules, deterministic ordering/tie-break rules, version syntax and integrity metadata.

These remain software/schema tests only and are not research evidence.

## Later M2 tests

As capabilities are implemented, tests will be added for:

- end-to-end research-platform regression/acceptance behavior.

Broker execution, order idempotency, reconciliation, live risk controls and shadow/live behavior belong to later milestones and are not M2 test requirements.

## Quality commands

Fast developer gate:

```bash
uv run --frozen python tools/verify_repo.py --fast
```

Full completion gate:

```bash
uv run --frozen python tools/verify_repo.py
```

The full gate runs repository validation, the complete pytest suite, Ruff lint/format checks and the environment fingerprint. Policy: `governance/program/LOCAL_CI_GATE.md`.


## Base data loader tests

`tests/test_data_loader.py` verifies:

- deterministic repeat loading of the canonical synthetic CSV fixture;
- SHA-256 mismatch rejection;
- out-of-order reject/sort behavior;
- duplicate reject/keep-first/keep-last behavior;
- malformed reject/drop behavior;
- explicit information-availability timestamp parsing;
- coverage enforcement;
- required ordering/tie-break columns;
- unsupported format rejection;
- coverage violations remaining blocking even when malformed rows may be dropped.

Fixture bytes are deterministic non-market software inputs and do not create research evidence.


## Strategy / Research interface tests

`tests/test_strategy_interface.py` verifies:

- loader-record to research-observation bridging;
- exact repeated deterministic state transitions;
- canonical decision JSON serialization;
- broker-neutral decision surface;
- immutable run context and observations;
- duplicate context-key rejection;
- non-finite payload rejection;
- timezone-aware decision times;
- unique observation fields;
- serializable immutable diagnostics.

The fixture strategy is synthetic non-market software logic and is not research evidence.


## Deterministic replay tests

`tests/test_replay_engine.py` verifies:

- one initialization and exactly one strategy step per loaded record;
- preservation of loaded-record order and stable sequence indices;
- ordered state-before/state-after trace;
- exact repeated-run equality;
- decision/diagnostic flattening in emission order;
- dataset identity/hash binding;
- empty-dataset behavior;
- nondecreasing information-availability enforcement;
- rejection of decisions timestamped before observation availability;
- vertical integration from Dataset Manifest through loader, Strategy interface and replay.

The replay fixture remains synthetic non-market software logic and is not research evidence.


## Cost model interface tests

`tests/test_cost_interface.py` verifies:

- applicable cost components require explicit parameters;
- not-applicable components are explicit, reasoned and parameter-free;
- component names are unique;
- non-finite inputs/results are rejected;
- immutable cost contracts;
- exact repeated deterministic fixture results;
- canonical cost-only serialization;
- configured components cannot be silently omitted or reordered;
- result identity and applicability must match the declared input/config.

The fixture uses synthetic non-market units and explicit cost components only. It is not research evidence.


## Standard analytics/report tests

`tests/test_standard_analytics.py` verifies:

- gross effect, modeled costs and net effect remain separate;
- replay observation/decision/diagnostic counts are preserved;
- Strategy decisions are not inferred to be trades;
- deterministic effect count/mean/min/max and absolute max drawdown;
- empty but explicitly applicable effect series behavior;
- incompatible cost units keep total/net explicitly not applicable;
- all-not-applicable cost components do not become a hidden zero;
- non-finite or semantically undeclared effects are rejected;
- trade/event count requires explicit non-negative semantics;
- canonical JSON and deterministic Markdown output.

The analytics fixture uses synthetic non-market units only and is not research evidence.


## Manifest-driven experiment runner tests

`tests/test_experiment_runner.py` verifies:

- registered manifest execution without modifying manifest bytes;
- exact repeated deterministic result JSON;
- DRAFT manifest rejection;
- code/environment/implementation runtime identity matching;
- Dataset ID and source-snapshot freeze enforcement;
- registered metric availability enforcement;
- required runtime cost components for registered costs;
- explicit NOT_APPLICABLE costs without hidden zero;
- explicit timezone-aware completion timestamp.

Tests create transient software-only manifest files under pytest temporary directories. They do not commit a fictitious Experiment package or Registry row and are not research evidence.
