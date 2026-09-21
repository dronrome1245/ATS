# Tests

ATS is in `M4_VALIDATION_FRAMEWORK`; the M2 platform test baseline remains the shared regression gate.

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

## M2 acceptance baseline

The final M2 platform acceptance layer is `tests/test_research_platform.py` with committed expected output in `tests/fixtures/platform/reference_consumer_expected.json`.

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


## Research platform acceptance tests

`tests/test_research_platform.py` verifies:

- the Reference Consumer Profile synthetic fixture end to end from Dataset Manifest through loader, Strategy interface, replay, explicit costs and standard analytics/result;
- exact comparison with a committed expected regression result;
- exact repeated-run canonical JSON equality;
- preservation of explicit cost applicability, including a non-applicable component;
- absence of `EXP-/HYP-/CAND-/STRAT-` identities from the committed acceptance fixture;
- zero Experiment Registry rows while the fixture remains software-only.

M2-010 targeted closure also reruns `tests/test_experiment_runner.py`, so registered-manifest orchestration remains covered without assigning a formal Experiment identity to the acceptance fixture.


## M4 parameter sensitivity tests

`tests/test_validation_sensitivity.py` verifies:

- every predefined variant is preserved in caller order;
- repeated evaluation serializes identically;
- metric output order follows the predeclared plan;
- duplicate variant IDs and malformed parameter shapes are rejected;
- missing or extra metrics fail closed;
- non-scalar/non-finite parameters and non-finite metrics are rejected;
- plan/results are immutable;
- output declares `NO_AUTOMATIC_SELECTION` and contains no automatic rank/selected winner.

The fixture is synthetic software-only input and is not validation evidence.


## M4 time/regime slicing tests

`tests/test_validation_slicing.py` verifies:

- every declared slice is reported in plan order;
- deterministic serialization declares `ALL_DECLARED_SLICES_REPORTED`;
- exhaustive plans reject unassigned observations;
- non-exhaustive plans count unassigned observations explicitly;
- overlap is blocked unless explicitly allowed and is counted when allowed;
- unknown/duplicate memberships fail closed;
- empty-slice handling is explicit;
- metric contracts and finite values are enforced;
- slicing plan/results are immutable.

The fixture is synthetic software-only input and is not validation evidence.


## M4 concentration tests

`tests/test_validation_concentration.py` verifies:

- all observations remain in input order;
- top-count concentration uses absolute magnitude deterministically;
- every declared group remains visible in first-seen order;
- ranking is marked diagnostic-only;
- no automatic outlier removal is exposed;
- zero absolute effect produces an explicit null share;
- duplicate IDs, non-finite values and invalid top-count plans fail closed;
- plan/results are immutable.

The fixture is synthetic software-only input and is not validation evidence.
