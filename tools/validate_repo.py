#!/usr/bin/env python3
"""ATS repository validator after M2 reproducible-environment baseline."""

from __future__ import annotations

import csv
import os
import tomllib
from pathlib import Path

import validate_repo_core as core

TAXONOMY = "governance/methodology/EVIDENCE_TAXONOMY.md"
REVIEW_PROTOCOL = "governance/methodology/RESEARCH_REVIEW_PROTOCOL.md"
REVIEW_CHECKS = "governance/methodology/RESEARCH_REVIEW_CHECKS.md"
REVIEW_DECISIONS = "governance/methodology/RESEARCH_REVIEW_DECISIONS.md"
REVIEW_TEMPLATE = "governance/methodology/templates/RESEARCH_REVIEW_TEMPLATE.md"
VALIDATION_FRAMEWORK = "governance/methodology/VALIDATION_FRAMEWORK.md"
MARKET_PATTERN_DISCOVERY = "governance/methodology/MARKET_PATTERN_DISCOVERY.md"
INDEPENDENT_EXAM_PROTOCOL = "governance/methodology/INDEPENDENT_EXAM_PROTOCOL.md"
M1_EXIT = "governance/program/M1_EXIT_REVIEW.md"
M2_EXIT = "governance/program/M2_EXIT_REVIEW.md"
M3_EXIT = "governance/program/M3_EXIT_REVIEW.md"
REFERENCE_STRATEGY_SELECTION = "governance/program/REFERENCE_STRATEGY_1_SELECTION.md"
REFERENCE_STRATEGY_IDEA = "research/ideas/IDEA-0001.md"
REFERENCE_STRATEGY_HYPOTHESIS = "research/hypotheses/HYP-0001.md"
REFERENCE_STRATEGY_DATA_FEASIBILITY = "research/reviews/HYP-0001-DATA_FEASIBILITY.md"
REFERENCE_STRATEGY_PROTOTYPE = "research/reviews/HYP-0001-PROTOTYPE-01.md"
PROTO01_RESULT = "reports/research/HYP-0001-PROTOTYPE-01-result.json"
PROTO01_SCHEMA = "data/manifests/DATA-EURUSD-DUKASCOPY-H1-PROTO01.schema.json"
PROTO01_MANIFEST = "data/manifests/DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml"
PROTO01_TOOL = "tools/proto01_eurusd.py"
CONSUMER_PROFILE = "governance/program/REFERENCE_CONSUMER_PROFILE.md"
RESEARCH_STACK_ADR = "governance/decisions/ADR-0001-RESEARCH-STACK.md"
ENVIRONMENT_SPEC = "governance/program/RESEARCH_ENVIRONMENT_SPEC.md"
LOCAL_CI_GATE = "governance/program/LOCAL_CI_GATE.md"
LOCAL_CI_TROUBLESHOOTING = "governance/program/LOCAL_CI_TROUBLESHOOTING.md"
LOCAL_CI_FAILURE_REGISTRY = "governance/program/LOCAL_CI_FAILURE_REGISTRY.md"
DATASET_MANIFEST_SPEC = "governance/program/DATASET_MANIFEST_SPEC.md"
DATASET_MANIFEST_FILES = (
    "data/manifests/DATASET_TEMPLATE.yaml",
    "src/ats/__init__.py",
    "src/ats/schemas/__init__.py",
    "src/ats/schemas/dataset_manifest.py",
    "tests/test_dataset_manifest.py",
)
BASE_LOADER_FILES = (
    ".gitattributes",
    "src/ats/data/__init__.py",
    "src/ats/data/loader.py",
    "tests/fixtures/datasets/ordered_events.csv",
    "tests/fixtures/datasets/ordered_events.schema.json",
    "tests/fixtures/datasets/ordered_events.manifest.yaml",
    "tests/test_data_loader.py",
)
STRATEGY_INTERFACE_FILES = (
    "src/ats/strategy/__init__.py",
    "src/ats/strategy/interface.py",
    "tests/test_strategy_interface.py",
)
REPLAY_FILES = (
    "src/ats/replay/__init__.py",
    "src/ats/replay/engine.py",
    "tests/test_replay_engine.py",
)
COST_INTERFACE_FILES = (
    "src/ats/costs/__init__.py",
    "src/ats/costs/interface.py",
    "tests/test_cost_interface.py",
)
ANALYTICS_FILES = (
    "src/ats/analytics/__init__.py",
    "src/ats/analytics/standard.py",
    "tests/test_standard_analytics.py",
)
RUNNER_FILES = (
    "src/ats/runner/__init__.py",
    "src/ats/runner/experiment.py",
    "tests/test_experiment_runner.py",
)
PLATFORM_TEST_FILES = (
    "tests/test_research_platform.py",
    "tests/fixtures/platform/reference_consumer_expected.json",
)
LOCAL_CI_FILES = (
    "ATS_TASK_CHECK.bat",
    "tools/verify_repo.py",
    "tools/current_task_check.py",
    ".githooks/pre-commit",
    ".githooks/pre-push",
    "reports/local_ci/README.md",
)
ENVIRONMENT_FILES = (
    "pyproject.toml",
    ".python-version",
    "uv.lock",
    "tools/environment_fingerprint.py",
    "tests/test_environment_baseline.py",
)
VALIDATION_SENSITIVITY_FILES = (
    "src/ats/validation/__init__.py",
    "src/ats/validation/sensitivity.py",
    "tests/test_validation_sensitivity.py",
)
VALIDATION_SLICING_FILES = (
    "src/ats/validation/slicing.py",
    "tests/test_validation_slicing.py",
)
VALIDATION_CONCENTRATION_FILES = (
    "src/ats/validation/concentration.py",
    "tests/test_validation_concentration.py",
)
VALIDATION_RESAMPLING_FILES = (
    "src/ats/validation/resampling.py",
    "tests/test_validation_resampling.py",
)
HEADER = (
    "experiment_id", "status", "research_stage", "evidence_class",
    "qualified_evidence_class", "idea_id", "hypothesis_id", "candidate_id",
    "strategy_id", "strategy_version", "package_path", "manifest_path",
    "registration_revision", "registered_at", "completed_at", "machine_outcome",
    "decision", "supersedes_experiment_id", "superseded_by_experiment_id",
)
QUALIFIED = {
    "EXPLORATORY_OBSERVATION", "EXPLORATORY_PROTOTYPE", "REGISTERED_EXPERIMENT",
    "VALIDATION_EVIDENCE", "INDEPENDENT_EXAMINATION_EVIDENCE", "STRESS_EVIDENCE",
    "DEMO_SHADOW_EVIDENCE", "MINIMAL_LIVE_EVIDENCE", "ACTIVE_LIVE_EVIDENCE",
    "PORTFOLIO_EVIDENCE", "SCALING_EVIDENCE",
}
DIRECT_RUNTIME = {
    "numpy==2.5.3",
    "pydantic==2.13.5",
    "PyYAML==6.0.3",
}
DIRECT_DEV = {
    "pytest==9.1.1",
    "ruff==0.16.7",
}


def configure() -> None:
    core.REQUIRED_FILES = core.REQUIRED_FILES + (
        TAXONOMY, REVIEW_PROTOCOL, REVIEW_CHECKS, REVIEW_DECISIONS, REVIEW_TEMPLATE,
        VALIDATION_FRAMEWORK, MARKET_PATTERN_DISCOVERY, INDEPENDENT_EXAM_PROTOCOL,
        M1_EXIT, M2_EXIT, M3_EXIT, REFERENCE_STRATEGY_SELECTION, REFERENCE_STRATEGY_IDEA,
        REFERENCE_STRATEGY_HYPOTHESIS, REFERENCE_STRATEGY_DATA_FEASIBILITY,
        REFERENCE_STRATEGY_PROTOTYPE, PROTO01_RESULT, PROTO01_SCHEMA, PROTO01_MANIFEST,
        PROTO01_TOOL,
        CONSUMER_PROFILE,
        RESEARCH_STACK_ADR, ENVIRONMENT_SPEC,
        LOCAL_CI_GATE,
        LOCAL_CI_TROUBLESHOOTING, LOCAL_CI_FAILURE_REGISTRY, DATASET_MANIFEST_SPEC,
        *DATASET_MANIFEST_FILES, *BASE_LOADER_FILES,
        *STRATEGY_INTERFACE_FILES, *REPLAY_FILES, *COST_INTERFACE_FILES,
        *ANALYTICS_FILES, *RUNNER_FILES, *PLATFORM_TEST_FILES,
        *LOCAL_CI_FILES, *ENVIRONMENT_FILES, *VALIDATION_SENSITIVITY_FILES,
        *VALIDATION_SLICING_FILES, *VALIDATION_CONCENTRATION_FILES,
        *VALIDATION_RESAMPLING_FILES,
    )
    core.CANONICAL_PATH_KEYS = core.CANONICAL_PATH_KEYS + (
        "evidence_taxonomy", "research_review_protocol", "validation_framework",
        "market_pattern_discovery", "independent_exam_protocol",
        "m1_exit_review",
        "m2_exit_review", "m3_exit_review", "reference_strategy_1_selection", "reference_strategy_1_idea",
        "reference_strategy_1_hypothesis", "reference_strategy_1_data_feasibility",
        "reference_strategy_1_dataset_manifest", "reference_consumer_profile", "research_stack_adr", "research_environment_spec",
        "dataset_manifest_spec", "local_ci_gate", "local_ci_troubleshooting",
        "local_ci_failure_registry",
    )
    core.REGISTRY_HEADER = HEADER
    core.CONTENT_MARKERS[TAXONOMY] = (
        "source_class", "qualified_evidence_class", "VALIDATION_EVIDENCE",
        "INDEPENDENT_EXAMINATION_EVIDENCE", "Negative evidence and class retention",
        "Structural acceptance test",
    )
    core.CONTENT_MARKERS[REVIEW_PROTOCOL] = (
        "event-driven", "RESEARCH_REVIEW_CHECKS.md", "RESEARCH_REVIEW_DECISIONS.md",
        "RESEARCH_REVIEW_TEMPLATE.md", "source_class", "qualified_evidence_class",
        "bounded follow-up", "Structural acceptance",
    )
    core.CONTENT_MARKERS[REVIEW_CHECKS] = (
        "INCOMPLETE_BLOCKING", "LINEAGE_OK", "CLASS_SUFFICIENT",
        "SUFFICIENT_FOR_DECISION", "Experiment integrity",
    )
    core.CONTENT_MARKERS[REVIEW_DECISIONS] = (
        "Preparer", "Reviewer", "Decision authority", "PROMOTE / PARK / REJECT",
        "Bounded return to research", "Immutable record and re-review",
    )
    core.CONTENT_MARKERS[REVIEW_TEMPLATE] = (
        "Prior Review ID", "Package completeness", "Lineage / currency",
        "Evidence class sufficiency", "Negative evidence and dissent", "Stop condition",
    )
    core.CONTENT_MARKERS[VALIDATION_FRAMEWORK] = (
        "Validation tests a **fixed-enough system**",
        "DEVELOPMENT",
        "VALIDATION",
        "INDEPENDENT_EXAMINATION",
        "Validation Profile",
        "Parameter neighbourhood",
        "Observation dependence",
        "effective sample size",
        "overlapping forward windows",
        "block bootstrap",
        "research freedom",
        "`PASS / FAIL / RETURN`",
        "`PASS / FAIL`",
        "no direct tuning on validation data",
        "future eligible Candidates",
        "ATS2-M4-002 — Parameter sensitivity tooling",
    )
    core.CONTENT_MARKERS[MARKET_PATTERN_DISCOVERY] = (
        "Market Pattern Discovery is **hypothesis generation**",
        "Search Manifest",
        "qualified_evidence_class = EXPLORATORY_OBSERVATION",
        "Search-space accounting",
        "Bounded search, not unlimited mining",
        "NO_PATTERN_SHORTLISTED",
        "SHORTLIST_FOR_IDEA_INTAKE",
        "WBS-6.0 — Market Pattern Discovery",
        "M4.1–M4.8 reusable validation capability",
        "HYP-0001 remains `REJECTED_AT_R3`",
    )
    core.CONTENT_MARKERS[INDEPENDENT_EXAM_PROTOCOL] = (
        "one-shot reveal",
        "Independent Exam Freeze Manifest",
        "DRAFT → FROZEN → REVEALED → DECIDED",
        "There is no `RETURN`",
        "default to **consumed**",
        "Technical failure before reveal",
        "Technical failure after reveal",
        "INDEPENDENT_EXAMINATION_EVIDENCE",
        "revealed protected block",
        "HYP-0001 remains `REJECTED_AT_R3`",
    )
    core.CONTENT_MARKERS[M1_EXIT] = (
        "Decision:** `PASS`", "M1_RESEARCH_METHODOLOGY = COMPLETED / PASS",
        "ATS2-M2-000 — Reference Consumer Profile", "Pipeline counters intentionally remain zero",
    )
    core.CONTENT_MARKERS[M2_EXIT] = (
        "Decision:** `PASS`",
        "M2_RESEARCH_PLATFORM_MVP = COMPLETED / PASS",
        "953eac0e88608d782a825d7039c1eb1bf14577c6",
        "complete pytest suite: 83 passed",
        "all 29 artifacts listed as completed under M2 exist",
        "experiments/REGISTRY.csv",
        "ATS2-M3-001 — Select Reference Strategy #1",
        "does **not** authorize",
        "Transition-commit closure",
    )
    core.CONTENT_MARKERS[M3_EXIT] = (
        "Decision:** `PASS`",
        "M3_REFERENCE_STRATEGY_1 = COMPLETED / PASS",
        "REJECTED_AT_R3",
        "1,006",
        "-0.0002301573",
        "aeda05d90994259a22e25d882398218aead968941fe0b1c73eb34894841291c0",
        "complete pytest suite: `86 passed`",
        "WBS-3.5",
        "WBS-3.10",
        "first future promoted Candidate",
        "ATS2-M4-001 — Validation protocol framework",
        "Transition-commit closure",
    )
    core.CONTENT_MARKERS[REFERENCE_STRATEGY_SELECTION] = (
        "Decision:** `SELECT`",
        "SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT",
        "Single-instrument 1H long/flat trend-following / breakout",
        "No numeric lookback, threshold, stop, holding period, position size or cost value",
        "Binance Public Data",
        "`1h` as a supported kline interval",
        "Alpha Vantage",
        "`60min` as a supported intraday interval",
        "Time Series Momentum",
        "selection was made before running a backtest",
        "OWNER changed the selected decision interval from daily bars to 1H bars",
        "ATS2-M3-002 — Idea & rationale",
        "research/ideas/IDEA-0001.md",
    )
    core.CONTENT_MARKERS[REFERENCE_STRATEGY_IDEA] = (
        "Idea ID: `IDEA-0001`",
        "Status: `SCREENING`",
        "EURUSD",
        "FX_SPOT_OTC",
        "POSITIVE_CONTINUATION_AFTER_UPWARD_TREND_OR_BREAKOUT_STATE",
        "same-close execution",
        "Result: `NEW`",
        "Decision: `SCREEN`",
        "research/hypotheses/HYP-0001.md",
    )
    core.CONTENT_MARKERS[REFERENCE_STRATEGY_HYPOTHESIS] = (
        "Hypothesis ID: `HYP-0001`",
        "Parent Idea ID: `IDEA-0001`",
        "Status: `READY_FOR_DATA_FEASIBILITY`",
        "highest BID high of the preceding 24",
        "next eligible 1H bar ASK open",
        "24 eligible 1H bars",
        "mean(signal executable 24-bar return) > 0",
        "same-close execution",
        "Decision: `DATA_FEASIBILITY`",
        "research/reviews/HYP-0001-DATA_FEASIBILITY.md",
    )
    core.CONTENT_MARKERS[REFERENCE_STRATEGY_DATA_FEASIBILITY] = (
        "Review status: `CONDITIONAL`",
        "Dukascopy Historical Data / JForex history",
        "Period.ONE_HOUR",
        "OfferSide.BID",
        "OfferSide.ASK",
        "Canonical research timezone: `UTC`",
        "GAP-DF-001",
        "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
        "Decision: `CONDITIONAL`",
        "research/reviews/HYP-0001-PROTOTYPE-01.md",
    )
    core.CONTENT_MARKERS[REFERENCE_STRATEGY_PROTOTYPE] = (
        "Prototype sequence: `PROTO-01`",
        "Status: `COMPLETED / REJECT`",
        "2021-01-01T00:00:00Z",
        "2026-01-01T00:00:00Z",
        "at least 100 valid breakout observations",
        "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
        "tools/proto01_eurusd.py",
        "Decision: `REJECT`",
        "ONE_OR_BOTH_PRIMARY_HYPOTHESIS_INEQUALITIES_FAILED",
        "EXPLORATORY_PROTOTYPE",
    )
    core.CONTENT_MARKERS[PROTO01_RESULT] = (
        '"decision": "REJECT"',
        '"breakout_signal_count": 1006',
        '"signal_mean_return": -0.00023015725987422884',
        '"unconditional_mean_return": -0.00006471364916215143',
        '"signal_minus_baseline": -0.0001654436107120774',
        '"prepared_csv_sha256": "aeda05d90994259a22e25d882398218aead968941fe0b1c73eb34894841291c0"',
        '"git_commit": "6115b1c7114e942a4f3e76795ce8d25b552cf849"',
    )
    core.CONTENT_MARKERS[PROTO01_SCHEMA] = (
        "HYP-0001 PROTO-01 EURUSD 1H aligned BID/ASK rows",
        "event_time",
        "availability_time",
        "bid_open",
        "ask_open",
        "additionalProperties",
    )
    core.CONTENT_MARKERS[PROTO01_MANIFEST] = (
        'dataset_id: "DATA-DUKASCOPY-EURUSDH1-PROTO01-001"',
        'dataset_version: "1.0.0"',
        "31,296 aligned rows",
        "cf378faaae58424112d289315b2ec076f4100775f2613a5d2d685ec46a02aba4",
        "aeda05d90994259a22e25d882398218aead968941fe0b1c73eb34894841291c0",
        'availability_mode: "EXPLICIT_FIELD"',
        'missing: "ALLOW_DECLARED_GAPS"',
        "tools/proto01_eurusd.py@e3550ae9793416d52c0bc8cca061cf221df2805b",
    )
    core.CONTENT_MARKERS[PROTO01_TOOL] = (
        "HYP-0001 PROTO-01",
        "candles_hour_1.bi5",
        "DOWNLOAD_BASES",
        "PROTO01_DATA_REPORT.txt",
        "PROTO01_RESULT.json",
        "DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml",
        "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "FEWER_THAN_100_VALID_BREAKOUT_OBSERVATIONS",
        "is_fx_market_hour",
        "Closed-market hours excluded",
    )
    core.CONTENT_MARKERS[CONSUMER_PROFILE] = (
        "single research logic instance", "Minimum data contract",
        "Timestamp and ordering semantics", "Minimum research decision interface",
        "Deterministic replay/backtest contract", "Cost-model consumer contract",
        "Experiment integration", "M2 acceptance fixture",
        "tests/test_research_platform.py",
        "tests/fixtures/platform/reference_consumer_expected.json",
        "ATS2-M2-001",
    )
    core.CONTENT_MARKERS[RESEARCH_STACK_ADR] = (
        "Status:** ACCEPTED", "CPython 3.13 series", "uv.lock",
        "Pydantic v2", "PyYAML 6.x", "NumPy 2.x", "M2 is **not DataFrame-first**",
        "Alternatives considered", "ATS2-M2-002 — Reproducible environment",
    )
    core.CONTENT_MARKERS[ENVIRONMENT_SPEC] = (
        "CPython", "3.13.15", "Linux x86_64", "uv == 0.12.13",
        "uv sync --frozen", "tools/verify_repo.py", "Local CI Gate",
        "ATS2-M2-003 — Dataset manifest support",
    )
    core.CONTENT_MARKERS[DATASET_MANIFEST_SPEC] = (
        "dataset_id + dataset_version",
        "information-availability",
        "tie_break_keys",
        "material data change requires a new dataset version",
        "yaml.safe_load",
        "Actual byte verification",
        "ATS2-M2-004 — Base data loader",
    )
    core.CONTENT_MARKERS["data/manifests/DATASET_TEMPLATE.yaml"] = (
        'dataset_id: "DATA-SYNTHETIC-M2-001"',
        'dataset_version: "1.0.0"',
        "availability_mode: \"SAME_AS_EVENT_TIME\"",
        "tie_break_keys:",
        "algorithm: \"NOT_AVAILABLE\"",
        "Synthetic non-market template; not research evidence.",
    )
    core.CONTENT_MARKERS["src/ats/schemas/dataset_manifest.py"] = (
        "class DatasetManifest",
        "yaml.safe_load",
        "ConfigDict(extra=\"forbid\", frozen=True)",
        "coverage timestamps must be timezone-aware",
        "event_time_field must be the first ordering key",
        "SHA256 integrity requires a lowercase 64-hex digest",
        "load_dataset_manifest",
    )
    core.CONTENT_MARKERS["tests/test_dataset_manifest.py"] = (
        "test_canonical_template_loads",
        "test_naive_coverage_timestamp_is_rejected",
        "test_tie_break_is_required",
        "test_invalid_sha256_metadata_is_rejected",
        "test_unsafe_yaml_tag_is_rejected",
    )
    core.CONTENT_MARKERS[".gitattributes"] = (
        "tests/fixtures/datasets/*.csv text eol=lf",
    )
    core.CONTENT_MARKERS["src/ats/data/loader.py"] = (
        "class DatasetLoadError",
        "class MalformedRowError",
        "class LoadedRecord",
        "class LoadedDataset",
        "csv.DictReader",
        "hashlib.sha256",
        "SORT_BY_ORDERING_CONTRACT",
        "dataset SHA256 mismatch",
        "event time outside manifest coverage",
        "source_location=manifest.storage.location",
    )
    core.CONTENT_MARKERS["tests/fixtures/datasets/ordered_events.manifest.yaml"] = (
        'dataset_id: "DATA-SYNTHETIC-LOADER-001"',
        'format: "CSV"',
        'algorithm: "SHA256"',
        "ab8107703361915dde4ba99c6fb03b8d9455afcd2afcbb55a8f63091c53b4172",
        "Synthetic non-market fixture; not research evidence.",
    )
    core.CONTENT_MARKERS["tests/test_data_loader.py"] = (
        "test_reference_fixture_loads_deterministically",
        "test_sha256_mismatch_is_rejected",
        "test_out_of_order_sort_policy_is_deterministic",
        "test_duplicate_keep_policies_are_explicit",
        "test_malformed_drop_policy_counts_dropped_rows",
        "test_explicit_availability_field_is_parsed",
        "test_coverage_violation_is_not_hidden_by_malformed_drop",
        "test_non_rfc3339_timestamp_is_rejected",
    )
    core.CONTENT_MARKERS["src/ats/strategy/interface.py"] = (
        "class ResearchRunContext",
        "class ResearchObservation",
        "class ResearchDecision",
        "class ResearchDiagnostic",
        "class StrategyStep",
        "class ResearchStrategy",
        "observation_from_loaded_record",
        "allow_nan=False",
        "sort_keys=True",
        "decision_time must be timezone-aware",
    )
    core.CONTENT_MARKERS["tests/test_strategy_interface.py"] = (
        "DeterministicFixtureStrategy",
        "test_loaded_record_bridge_preserves_research_times_and_fields",
        "test_repeated_fixture_transitions_are_exactly_deterministic",
        "test_decision_serialization_is_canonical_and_broker_neutral",
        "test_run_context_is_immutable",
        "test_non_finite_decision_payload_is_rejected",
        "test_diagnostic_is_serializable_and_immutable",
    )
    core.CONTENT_MARKERS["src/ats/replay/engine.py"] = (
        "class ReplayContractError",
        "class ReplayFrame",
        "class ReplayResult",
        "def run_replay",
        "availability_time must be nondecreasing",
        "decision_time cannot be earlier",
        "observation_from_loaded_record",
        "computed_sha256=dataset.computed_sha256",
    )
    core.CONTENT_MARKERS["tests/test_replay_engine.py"] = (
        "test_replay_preserves_loaded_order_and_calls_strategy_once_per_record",
        "test_replay_state_trace_is_ordered_and_complete",
        "test_repeated_replay_is_exactly_equal",
        "test_availability_time_regression_is_rejected",
        "test_decision_before_observation_availability_is_rejected",
        "test_manifest_loader_strategy_replay_vertical_slice",
    )
    core.CONTENT_MARKERS["src/ats/costs/interface.py"] = (
        "class CostApplicability",
        "class CostComponentConfig",
        "class CostModelConfig",
        "class CostInput",
        "class CostComponentResult",
        "class CostResult",
        "class CostModel",
        "def apply_cost_model",
        "applicable cost component must declare explicit parameters",
        "cost result components must exactly match configured order",
        "allow_nan=False",
    )
    core.CONTENT_MARKERS["tests/test_cost_interface.py"] = (
        "DeterministicFixtureCostModel",
        "test_applicable_component_requires_explicit_parameters",
        "test_not_applicable_component_is_explicit_and_parameter_free",
        "test_fixture_model_is_exactly_deterministic",
        "test_cost_result_serialization_is_canonical_and_cost_only",
        "test_model_cannot_silently_omit_configured_component",
    )
    core.CONTENT_MARKERS["src/ats/analytics/standard.py"] = (
        "class AnalyticsApplicability",
        "class NotApplicable",
        "class EffectSeries",
        "class ActivityCount",
        "class StandardAnalyticsResult",
        "def build_standard_analytics",
        "gross effect and modeled costs use different units",
        "cost result has no applicable components",
        "research decisions",
        "allow_nan=False",
        "to_markdown",
    )
    core.CONTENT_MARKERS["tests/test_standard_analytics.py"] = (
        "test_standard_analytics_keeps_gross_costs_and_net_separate",
        "test_replay_counts_are_reported_without_treating_decisions_as_trades",
        "test_effect_distribution_and_path_metrics_are_deterministic",
        "test_incompatible_cost_units_keep_total_and_net_not_applicable",
        "test_no_applicable_cost_components_do_not_create_hidden_zero_cost",
        "test_json_and_markdown_outputs_are_deterministic",
    )
    core.CONTENT_MARKERS["src/ats/runner/experiment.py"] = (
        "class ExperimentRunError",
        "class RegisteredExperimentContext",
        "class RuntimeIdentity",
        "class ExperimentRuntime",
        "class ExperimentRunResult",
        "def load_registered_experiment_context",
        "def run_registered_experiment",
        "yaml.safe_load",
        "REGISTERED_CONTEXT_MATCH",
        "registered_manifest_sha256",
        "registered metrics are not available from standard analytics",
        "no dynamic imports from manifest text",
    )
    core.CONTENT_MARKERS["tests/test_experiment_runner.py"] = (
        "test_registered_manifest_runs_end_to_end_without_mutation",
        "test_repeated_registered_run_is_exactly_deterministic",
        "test_draft_manifest_is_rejected_before_execution",
        "test_runtime_identity_must_match_registered_context",
        "test_dataset_identity_and_snapshot_are_frozen",
        "test_registered_metric_must_exist_in_standard_analytics",
        "test_registered_cost_model_requires_runtime_cost_components",
        "test_registered_not_applicable_costs_remain_explicit",
    )
    core.CONTENT_MARKERS["tests/test_research_platform.py"] = (
        "class AcceptanceStrategy",
        "class AcceptanceCostModel",
        "test_reference_consumer_acceptance_matches_committed_regression",
        "test_reference_consumer_acceptance_repeats_exactly",
        "test_reference_consumer_fixture_preserves_cost_applicability",
        "test_reference_consumer_fixture_has_no_formal_research_identity",
        "reference_consumer_expected.json",
        "REGISTRY.csv",
    )
    core.CONTENT_MARKERS["src/ats/validation/sensitivity.py"] = (
        "class SensitivityContractError",
        "class ParameterVariant",
        "class SensitivityPlan",
        "class SensitivityPoint",
        "class SensitivityResult",
        "MappingProxyType",
        "NO_AUTOMATIC_SELECTION",
        "metric set mismatch",
        "evaluate_parameter_sensitivity",
        "without ranking or selection",
    )
    core.CONTENT_MARKERS["tests/test_validation_sensitivity.py"] = (
        "test_full_predeclared_region_is_preserved_in_input_order",
        "test_serialization_is_deterministic_and_has_no_selected_winner",
        "test_metric_order_comes_from_plan_not_evaluator_mapping_order",
        "test_duplicate_variant_ids_are_rejected",
        "test_missing_or_extra_metrics_are_rejected",
        "test_non_finite_values_are_rejected",
        "test_non_scalar_parameter_values_are_rejected",
        "test_plan_and_results_are_immutable",
        "NO_AUTOMATIC_SELECTION",
    )
    core.CONTENT_MARKERS["src/ats/validation/slicing.py"] = (
        "class EmptySlicePolicy",
        "class SliceDefinition",
        "class SlicePlan",
        "class SlicePoint",
        "class SliceResult",
        "ALL_DECLARED_SLICES_REPORTED",
        "require_exhaustive",
        "allow_overlap",
        "unknown slice_ids",
        "evaluate_declared_slices",
        "without selective omission",
    )
    core.CONTENT_MARKERS["tests/test_validation_slicing.py"] = (
        "test_every_declared_slice_is_reported_in_plan_order",
        "test_serialization_is_deterministic_and_declares_reporting_policy",
        "test_unassigned_observation_is_blocking_when_exhaustive",
        "test_overlap_is_blocked_unless_explicitly_allowed",
        "test_unknown_or_duplicate_membership_is_rejected",
        "test_empty_slice_policy_can_reject_declared_empty_slice",
        "test_metric_contract_and_finite_values_fail_closed",
        "test_plan_and_result_are_immutable",
        "ALL_DECLARED_SLICES_REPORTED",
    )
    core.CONTENT_MARKERS["src/ats/validation/concentration.py"] = (
        "class ConcentrationContractError",
        "class Contribution",
        "class ConcentrationPlan",
        "class TopConcentration",
        "class GroupContribution",
        "class ConcentrationResult",
        "ABSOLUTE_MAGNITUDE_DIAGNOSTIC_ONLY",
        "NO_AUTOMATIC_OUTLIER_REMOVAL",
        "analyze_concentration",
        "retaining every input observation",
    )
    core.CONTENT_MARKERS["tests/test_validation_concentration.py"] = (
        "test_all_observations_are_retained_in_input_order",
        "test_top_observation_concentration_uses_absolute_magnitude",
        "test_group_aggregation_retains_every_group_in_first_seen_order",
        "test_top_group_concentration_is_diagnostic_only",
        "test_zero_absolute_effect_has_explicit_null_share",
        "test_duplicate_observation_ids_are_rejected",
        "test_invalid_top_counts_are_rejected",
        "test_plan_and_result_are_immutable",
        "NO_AUTOMATIC_OUTLIER_REMOVAL",
    )
    core.CONTENT_MARKERS["src/ats/validation/resampling.py"] = (
        "class ResamplingContractError",
        "class ResamplingMethod",
        "BLOCK_BOOTSTRAP",
        "class ResamplingBlock",
        "class ResamplingPlan",
        "class ResamplingReplicate",
        "class ResamplingResult",
        "DECLARED_BLOCKS_PRESERVED",
        "run_block_resampling",
        "preserve internal order",
    )
    core.CONTENT_MARKERS["tests/test_validation_resampling.py"] = (
        "test_repeated_block_resampling_is_exactly_deterministic",
        "test_source_block_identity_and_count_are_retained",
        "test_each_selected_block_is_preserved_whole_and_in_order",
        "test_serialization_declares_no_iid_fallback",
        "test_duplicate_block_ids_are_rejected",
        "test_empty_or_non_finite_blocks_are_rejected",
        "test_no_implicit_method_or_empty_block_set",
        "test_plan_and_result_are_immutable",
        "DECLARED_BLOCKS_PRESERVED",
    )
    core.CONTENT_MARKERS["tests/fixtures/platform/reference_consumer_expected.json"] = (
        '"schema_version": "m2-reference-consumer-1"',
        '"dataset_id": "DATA-SYNTHETIC-LOADER-001"',
        '"decision_type": "M2_ACCEPTANCE"',
        '"gross_effect"',
        '"net_effect"',
        '"slippage_proxy"',
        '"NOT_APPLICABLE"',
    )
    core.CONTENT_MARKERS["governance/methodology/templates/experiment/result.json"] = (
        "registered_manifest_sha256",
        "dataset_version",
        "computed_sha256",
        "reproducibility_status",
    )
    core.CONTENT_MARKERS[LOCAL_CI_GATE] = (
        "ATS_TASK_CHECK.bat",
        "CURRENT_TASK_REPORT.txt",
        "uv run --frozen python tools/verify_repo.py",
        "ATS LOCAL CI: PASS",
        "LOCAL_CI_TROUBLESHOOTING.md",
        ".githooks/pre-commit",
        ".githooks/pre-push",
        "GitHub Actions status is not a completion criterion",
        "Fast preflight before the completion check",
        "launcher exits with code `16`",
    )
    core.CONTENT_MARKERS[LOCAL_CI_TROUBLESHOOTING] = (
        "LCI-001",
        "SYNC_NETWORK",
        "Failed to connect to github.com:443",
        "LCI-002",
        "FORMAT",
        "ruff format --check",
        "b3085c26342c52e6ae852962faefcaf347d43a2a",
        "fd09a08de2a234ac1249a9e44ee7e21f32f4a7cd",
        "LCI-003",
        "uv is not available on PATH",
        "exit code `12`",
        "uv 0.12.13",
        "Invoke-WebRequest -UseBasicParsing",
        "powershell -ExecutionPolicy ByPass -File",
        "uv python install 3.13.15",
        "uv refuses to overwrite an executable it does not manage",
        "linked to non-existent Python interpreter",
        "LCI-004",
        "Repository validator marker drift from Markdown formatting",
        "stable semantic phrase",
        "LCI-005",
        "Windows shortcut artifact makes Local CI tree dirty",
        "reports/local_ci/*.lnk",
        "narrowly scoped",
        "do not modify source code for infrastructure/network failures",
        "Raw machine reports are not copied into this file",
        "technical-control threshold",
    )
    core.CONTENT_MARKERS[LOCAL_CI_FAILURE_REGISTRY] = (
        "Escalation policy",
        "LCI-002",
        "Confirmed occurrences",
        "REPEAT_AFTER_CONTROL_THRESHOLD",
        "fast Local CI preflight",
        "9fb041c51cf93071ca6735b52897cbb2b24e5568",
        "9134c44d1d3d861124c44e00b4df820ad181cb5d",
        "6d452c4f340825eaa39b8e28dad3f6691332b217",
        "3a0dc9af4cc2191cc98c65b190b6f1f1c5cb1ea3",
        "124 passed",
        "Reusable resolution rule",
        "Rule-conversion discipline",
    )
    core.CONTENT_MARKERS["ATS_TASK_CHECK.bat"] = (
        "git pull --ff-only",
        "uv sync --frozen",
        "tools/current_task_check.py",
        "CURRENT_TASK_REPORT.txt",
        "Required ATS baseline: uv 0.12.13.",
        "fast local ci preflight",
        "tools/verify_repo.py --fast",
        "exit code %RC%",
        "ATS TASK LAUNCHER: PASS",
        "ATS TASK LAUNCHER: FAIL",
    )
    core.CONTENT_MARKERS["tools/current_task_check.py"] = (
        'TASK_ID = "ATS2-M4-006"',
        "M4-006 independent exam artifacts",
        "governance/methodology/INDEPENDENT_EXAM_PROTOCOL.md",
        "M4-006 independent exam governance validation",
        "tools/verify_repo.py",
        "ATS CURRENT TASK CHECK:",
    )
    core.CONTENT_MARKERS["tools/verify_repo.py"] = (
        "ATS Local CI Gate", "repository validator", "ruff lint", "ruff format",
        "pytest", "environment fingerprint", "ATS LOCAL CI:", "LATEST.json",
    )
    core.CONTENT_MARKERS["reports/local_ci/README.md"] = (
        "ATS_TASK_CHECK.bat",
        "CURRENT_TASK_REPORT.txt",
        "LATEST.json",
        "LOCAL_CI_GATE.md",
        "LOCAL_CI_TROUBLESHOOTING.md",
        "reports/local_ci/*.lnk",
    )
    core.CONTENT_MARKERS["governance/program/PROGRAM_WBS_V2.md"] = (
        "`WBS-2.0`",
        "Reference Consumer Profile",
        "`WBS-2.10`",
        "`WBS-3.1`",
        "`WBS-3.2`",
        "M2 Research Platform MVP — `COMPLETED / PASS`",
        "Reference Strategy #1 research outcome — `REJECTED_AT_R3`",
        "Validate first promoted Candidate",
        "`WBS-6.0`",
        "Market Pattern Discovery",
        "M4.1–M4.8",
    )
    core.CONTENT_MARKERS["data/README.md"] = (
        "Dataset Manifests",
        "DATASET_MANIFEST_SPEC.md",
        "Base data loader",
        "src/ats/data/loader.py",
        "SORT_BY_ORDERING_CONTRACT",
        "missing/gap policy",
        "not research evidence",
    )
    core.CONTENT_MARKERS["src/README.md"] = (
        "ats.data.loader",
        "ats.strategy.interface",
        "ats.replay.engine",
        "ats.costs.interface",
        "ats.analytics.standard",
        "ats.runner.experiment",
        "ReplayFrame",
        "ReplayResult",
        "CostModelConfig",
        "CostResult",
        "StandardAnalyticsResult",
        "RegisteredExperimentContext",
        "ExperimentRunResult",
        "M2 Exit is recorded",
        "SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT",
        "M3 Reference Strategy #1 is recorded as `COMPLETED / PASS`",
        "ATS2-M4-002 — Parameter sensitivity tooling",
        "ATS2-M4-003 — Time/regime slicing",
        "ATS2-M4-004 — Observation concentration analysis",
        "ATS2-M4-005 — Dependence-preserving resampling framework",
        "ats.validation.sensitivity",
        "ats.validation.slicing",
        "ats.validation.concentration",
        "ats.validation.resampling",
    )
    core.CONTENT_MARKERS["tests/README.md"] = (
        "test_environment_baseline.py",
        "test_dataset_manifest.py",
        "test_data_loader.py",
        "test_strategy_interface.py",
        "test_replay_engine.py",
        "test_cost_interface.py",
        "test_standard_analytics.py",
        "test_experiment_runner.py",
        "test_research_platform.py",
        "test_validation_sensitivity.py",
        "test_validation_slicing.py",
        "test_validation_concentration.py",
        "test_validation_resampling.py",
        "reference_consumer_expected.json",
        "vertical integration from Dataset Manifest",
        "explicit cost components",
        "Strategy decisions are not inferred to be trades",
        "synthetic non-market",
    )
    core.CONTENT_MARKERS["reports/README.md"] = (
        "source_class",
        "qualified_evidence_class",
        "ats.analytics.standard",
        "gross effect",
        "manifest-driven Experiment runner",
        "negative prototype remains exploratory evidence",
    )
    core.CONTENT_MARKERS["governance/methodology/templates/CANDIDATE_EVIDENCE_INDEX_TEMPLATE.md"] = (
        "Source class", "Qualified evidence class", "Negative and discarded evidence",
    )
    core.CONTENT_MARKERS["governance/methodology/templates/strategy_version/EVIDENCE_INDEX.md"] = (
        "Source class", "Qualified evidence class", "VALIDATION_EVIDENCE",
        "INDEPENDENT_EXAMINATION_EVIDENCE", "Evidence status",
    )
    core.CONTENT_MARKERS["experiments/README.md"] = (
        "Experiment Registry", "qualified_evidence_class", "registration_revision",
        "ats.runner.experiment", "registered_manifest_sha256",
        "does not become `REGISTERED_EXPERIMENT` evidence",
    )
    core.CONTENT_MARKERS["tools/search_experiments.py"] = (
        "REGISTRY.csv", "qualified_evidence_class", "--contains",
    )
    core.CONTENT_MARKERS["tools/environment_fingerprint.py"] = (
        "platform.python_implementation", "platform.python_version", "uv --version",
    )
    core.CONTENT_MARKERS["tests/test_environment_baseline.py"] = (
        "3, 13, 15", '"numpy": "2.5.3"', '"pydantic": "2.13.5"',
        '"PyYAML": "6.0.3"', '"pytest": "9.1.1"', '"ruff": "0.16.7"',
    )


def validate_environment(repo: Path) -> int:
    blocking = 0

    python_version = (repo / ".python-version").read_text(encoding="utf-8").strip()
    if python_version != "3.13.15":
        core.fail(f".python-version must be exactly 3.13.15, found {python_version!r}")
        blocking += 1

    with (repo / "pyproject.toml").open("rb") as handle:
        project = tomllib.load(handle)

    project_table = project.get("project", {})
    if project_table.get("requires-python") != ">=3.13,<3.14":
        core.fail("pyproject project.requires-python must be >=3.13,<3.14")
        blocking += 1
    if set(project_table.get("dependencies", [])) != DIRECT_RUNTIME:
        core.fail("pyproject runtime dependency pins do not match M2 baseline")
        blocking += 1
    if set(project.get("dependency-groups", {}).get("dev", [])) != DIRECT_DEV:
        core.fail("pyproject dev dependency pins do not match M2 baseline")
        blocking += 1
    pytest_options = project.get("tool", {}).get("pytest", {}).get("ini_options", {})
    if pytest_options.get("pythonpath") != ["src"]:
        core.fail("pytest pythonpath must expose src for ATS package tests")
        blocking += 1
    if pytest_options.get("addopts") != "-p no:cacheprovider":
        core.fail("pytest cacheprovider must remain disabled for the local Windows workflow")
        blocking += 1

    uv_table = project.get("tool", {}).get("uv", {})
    if uv_table.get("package") is not False:
        core.fail("tool.uv.package must remain false for current M2 baseline")
        blocking += 1
    if uv_table.get("required-version") != "==0.12.13":
        core.fail("tool.uv.required-version must be ==0.12.13")
        blocking += 1
    expected_environments = {
        "sys_platform == 'linux' and platform_machine == 'x86_64'",
        "sys_platform == 'win32' and platform_machine == 'AMD64'",
    }
    if set(uv_table.get("environments", [])) != expected_environments:
        core.fail("tool.uv.environments must define Windows x86_64 and Linux x86_64")
        blocking += 1
    if set(uv_table.get("required-environments", [])) != expected_environments:
        core.fail("tool.uv.required-environments must require Windows x86_64 and Linux x86_64")
        blocking += 1

    lock = (repo / "uv.lock").read_text(encoding="utf-8")
    for marker in (
        'requires-python = ">=3.13,<3.14"',
        'name = "numpy"\nversion = "2.5.3"',
        'name = "pydantic"\nversion = "2.13.5"',
        'name = "pydantic-core"\nversion = "2.46.5"',
        'name = "pyyaml"\nversion = "6.0.3"',
        'name = "pytest"\nversion = "9.1.1"',
        'name = "ruff"\nversion = "0.16.7"',
        "numpy-2.5.3-cp313-cp313-manylinux_2_27_x86_64",
        "pydantic_core-2.46.5-cp313-cp313-manylinux_2_17_x86_64",
        "pyyaml-6.0.3-cp313-cp313-manylinux2014_x86_64",
        "ruff-0.16.7-py3-none-manylinux_2_17_x86_64",
        "numpy-2.5.3-cp313-cp313-win_amd64",
        "pydantic_core-2.46.5-cp313-cp313-win_amd64",
        "pyyaml-6.0.3-cp313-cp313-win_amd64",
        "ruff-0.16.7-py3-none-win_amd64",
        'hash = "sha256:',
    ):
        if marker not in lock:
            core.fail(f"uv.lock environment marker missing: {marker}")
            blocking += 1

    if (repo / ".github/workflows/validate.yml").exists():
        core.fail("GitHub Actions workflow must remain disabled; use the Local CI Gate")
        blocking += 1

    gitignore = (repo / ".gitignore").read_text(encoding="utf-8")
    for ignored_report in (
        "reports/local_ci/LATEST.json",
        "reports/local_ci/CURRENT_TASK_REPORT.txt",
        "reports/local_ci/*.lnk",
    ):
        if ignored_report not in gitignore:
            core.fail(f"local CI runtime report must remain ignored by Git: {ignored_report}")
            blocking += 1

    for hook_name in ("pre-commit", "pre-push"):
        hook = repo / ".githooks" / hook_name
        hook_text = hook.read_text(encoding="utf-8")
        if "tools/verify_repo.py" not in hook_text:
            core.fail(f"local CI hook missing verify_repo.py: {hook_name}")
            blocking += 1
        if os.name != "nt" and hook.stat().st_mode & 0o111 == 0:
            core.fail(f"local CI hook must be executable on POSIX hosts: {hook_name}")
            blocking += 1

    for relative in (
        "tools/environment_fingerprint.py",
        "tools/verify_repo.py",
        "tools/proto01_eurusd.py",
        "src/ats/schemas/dataset_manifest.py",
        "src/ats/data/loader.py",
        "src/ats/strategy/interface.py",
        "src/ats/replay/engine.py",
        "src/ats/costs/interface.py",
        "src/ats/analytics/standard.py",
        "src/ats/runner/experiment.py",
        "src/ats/validation/sensitivity.py",
        "src/ats/validation/slicing.py",
        "src/ats/validation/concentration.py",
        "src/ats/validation/resampling.py",
        "tests/test_environment_baseline.py",
        "tests/test_dataset_manifest.py",
        "tests/test_data_loader.py",
        "tests/test_strategy_interface.py",
        "tests/test_replay_engine.py",
        "tests/test_cost_interface.py",
        "tests/test_standard_analytics.py",
        "tests/test_experiment_runner.py",
        "tests/test_research_platform.py",
        "tests/test_validation_sensitivity.py",
        "tests/test_validation_slicing.py",
        "tests/test_validation_concentration.py",
        "tests/test_validation_resampling.py",
    ):
        path = repo / relative
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            core.fail(f"Python syntax error in {relative}: {exc}")
            blocking += 1

    return blocking


def main() -> int:
    configure()
    repo = Path(__file__).resolve().parents[1]
    blocking = 0

    for relative in core.REQUIRED_FILES:
        if not (repo / relative).is_file():
            core.fail(f"missing required file: {relative}")
            blocking += 1
    if (repo / core.TRANSITIONAL_STATE).exists():
        core.fail(f"transitional duplicate state must not exist: {core.TRANSITIONAL_STATE}")
        blocking += 1
    for relative in core.MIGRATED_CURRENT_V2_FILES + core.MIGRATED_LEGACY_SOURCE_FILES:
        if (repo / relative).exists():
            core.fail(f"migrated duplicate/source path must not exist: {relative}")
            blocking += 1

    state = (repo / "03_СОСТОЯНИЕ_ПРОЕКТА.yaml").read_text(encoding="utf-8")
    for marker in (
        'schema_version: "2.0"', "phase: M4_VALIDATION_FRAMEWORK",
        "M0_PROGRAM_REBASELINE: COMPLETED", "M1_RESEARCH_METHODOLOGY: COMPLETED",
        "M2_RESEARCH_PLATFORM_MVP: COMPLETED", "M3_REFERENCE_STRATEGY_1: COMPLETED",
        "M4_VALIDATION_FRAMEWORK: IN_PROGRESS",
        "exit_decision: PASS",
        'm1_exit_review: "governance/program/M1_EXIT_REVIEW.md"',
        'm2_exit_review: "governance/program/M2_EXIT_REVIEW.md"',
        'm3_exit_review: "governance/program/M3_EXIT_REVIEW.md"',
        'validation_framework: "governance/methodology/VALIDATION_FRAMEWORK.md"',
        'market_pattern_discovery: "governance/methodology/MARKET_PATTERN_DISCOVERY.md"',
        'independent_exam_protocol: "governance/methodology/INDEPENDENT_EXAM_PROTOCOL.md"',
        'reference_strategy_1_selection: "governance/program/REFERENCE_STRATEGY_1_SELECTION.md"',
        'reference_strategy_1_idea: "research/ideas/IDEA-0001.md"',
        'reference_strategy_1_hypothesis: "research/hypotheses/HYP-0001.md"',
        'reference_strategy_1_data_feasibility: "research/reviews/HYP-0001-DATA_FEASIBILITY.md"',
        'reference_strategy_1_dataset_manifest: "data/manifests/DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml"',
        'reference_consumer_profile: "governance/program/REFERENCE_CONSUMER_PROFILE.md"',
        'research_stack_adr: "governance/decisions/ADR-0001-RESEARCH-STACK.md"',
        'research_environment_spec: "governance/program/RESEARCH_ENVIRONMENT_SPEC.md"',
        'dataset_manifest_spec: "governance/program/DATASET_MANIFEST_SPEC.md"',
        'local_ci_gate: "governance/program/LOCAL_CI_GATE.md"',
        'local_ci_troubleshooting: "governance/program/LOCAL_CI_TROUBLESHOOTING.md"',
        'local_ci_failure_registry: "governance/program/LOCAL_CI_FAILURE_REGISTRY.md"',
        'last_completed_task_id: "ATS2-M4-006"',
        'current_task: "ATS2-M4-007"', 'current_ready_task: "ATS2-M4-007"',
        'current_wbs: "WBS-4.7"', "reference_strategy_selection_allowed: true",
        'selected_reference_strategy: "SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT"',
        'idea_id: "IDEA-0001"', 'hypothesis_id: "HYP-0001"',
        'data_feasibility_decision: "CONDITIONAL"',
        'prototype_id: "PROTO-01"', 'prototype_status: "REJECTED"',
        'prototype_outcome: "REJECT"', 'research_line_status: "REJECTED_AT_R3"',
        'selected_market_context: "FX_SPOT_OTC"',
        'selected_instrument: "EURUSD"', "ideas_registered: 1",
        'primary_local_host: WINDOWS_X86_64', 'WINDOWS_X86_64', 'LINUX_X86_64',
        'python: "3.13.15"', 'uv: "0.12.13"',
        "mode: LOCAL", "github_actions_required: false",
        'full_command: "uv run --frozen python tools/verify_repo.py"',
        'current_task_launcher: "ATS_TASK_CHECK.bat"',
        'current_task_checker: "tools/current_task_check.py"',
        'shareable_report: "reports/local_ci/CURRENT_TASK_REPORT.txt"',
        "experiments_registered: 0", "physical_migration_complete: true",
        "thirteen_gate_model_is_program_roadmap: false",
    ):
        if marker not in state:
            core.fail(f"canonical state marker missing or changed: {marker}")
            blocking += 1

    for key in core.CANONICAL_PATH_KEYS:
        relative = core.extract_quoted_scalar(state, key)
        if not relative or not (repo / relative).exists():
            core.fail(f"canonical state path invalid for {key}: {relative}")
            blocking += 1

    safety_block = state.split("safety:", 1)[1].split("strategy_pipeline:", 1)[0]
    for line in safety_block.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = [part.strip() for part in line.split(":", 1)]
        if key == "emergency_stop_required_before_live":
            if value != "true":
                core.fail("emergency-stop safety invariant changed")
                blocking += 1
        elif value != "false":
            core.fail(f"safety permission must remain false: {key}")
            blocking += 1

    blocking += core.validate_content_markers(repo)
    blocking += core.validate_registry(repo)
    blocking += validate_environment(repo)

    with (repo / "experiments/REGISTRY.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != HEADER:
            core.fail("Experiment Registry header mismatch")
            blocking += 1
        else:
            for line_no, row in enumerate(reader, start=2):
                value = row["qualified_evidence_class"].strip()
                if value and value not in QUALIFIED:
                    core.fail(f"invalid qualified_evidence_class at line {line_no}: {value}")
                    blocking += 1

    acceptance_fixture = (
        repo / "tests" / "fixtures" / "platform" / "reference_consumer_expected.json"
    ).read_text(encoding="utf-8")
    for forbidden_identity in ("EXP-", "HYP-", "CAND-", "STRAT-"):
        if forbidden_identity in acceptance_fixture:
            core.fail(
                "M2 acceptance fixture must not contain formal research identity: "
                + forbidden_identity
            )
            blocking += 1

    search_tool = repo / "tools/search_experiments.py"
    try:
        compile(search_tool.read_text(encoding="utf-8"), str(search_tool), "exec")
    except SyntaxError as exc:
        core.fail(f"search_experiments.py syntax error: {exc}")
        blocking += 1

    next_artifact = core.extract_quoted_scalar(state, "next_artifact")
    last_completed = core.extract_quoted_scalar(state, "last_completed_artifact")
    next_task = core.extract_quoted_scalar(state, "next_task_id")
    handoff = (repo / "AI_HANDOFF.md").read_text(encoding="utf-8")
    next_step = (repo / "02_СЛЕДУЮЩИЙ_ШАГ.md").read_text(encoding="utf-8")
    backlog = (repo / "governance/backlog/PROGRAM_BACKLOG_V2.md").read_text(encoding="utf-8")

    if core.backlog_status(backlog, "ATS2-M4-006") != "DONE":
        core.fail("M4-006 must be DONE in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-M4-007") != "READY":
        core.fail("M4-007 must be READY in Program Backlog")
        blocking += 1
    if not last_completed or not (repo / last_completed).exists():
        core.fail("canonical last_completed_artifact missing")
        blocking += 1
    for value, label in ((next_artifact, "next_artifact"), (next_task, "next_task_id")):
        if not value or value not in handoff or value not in next_step:
            core.fail(f"handoff/next-step mismatch for {label}: {value}")
            blocking += 1
    if last_completed and last_completed not in handoff:
        core.fail("AI_HANDOFF.md missing last_completed_artifact")
        blocking += 1

    agents = (repo / "AGENTS.md").read_text(encoding="utf-8")
    for marker in (
        "03_СОСТОЯНИЕ_ПРОЕКТА.yaml",
        "governance/backlog/PROGRAM_BACKLOG_V2.md",
        "governance/program/LOCAL_CI_TROUBLESHOOTING.md",
        "legacy/v1/",
    ):
        if marker not in agents:
            core.fail(f"AGENTS.md marker missing: {marker}")
            blocking += 1

    for relative_name in core.OPERATIONAL_FILES:
        path = repo / relative_name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for prefix in core.STALE_V1_PREFIXES:
            if prefix in text:
                core.fail(f"stale pre-migration namespace in {relative_name}: {prefix}")
                blocking += 1

    for path, relative in core.current_text_files(repo):
        text = path.read_text(encoding="utf-8")
        for pattern in core.FORBIDDEN_PLACEHOLDERS:
            if pattern.search(text):
                core.fail(f"forbidden placeholder pattern in {relative}")
                blocking += 1
                break
        blocking += core.validate_local_markdown_links(repo, path, relative)

    if blocking:
        print(f"ATS repository validation: BLOCKING ({blocking})")
        return 1
    print("ATS repository validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
