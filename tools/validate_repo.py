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
MULTIPLE_RESEARCH_ACCOUNTING = "governance/methodology/MULTIPLE_RESEARCH_ACCOUNTING.md"
TECHNICAL_STRATEGY_VALIDATION_PROFILE = (
    "governance/methodology/TECHNICAL_STRATEGY_VALIDATION_PROFILE.md"
)
DISCOVERY_SEARCH_MANIFEST_TEMPLATE = (
    "governance/methodology/templates/discovery/SEARCH_MANIFEST_TEMPLATE.yaml"
)
BOUNDED_DISCOVERY_ENGINE = "src/ats/discovery/bounded.py"
BOUNDED_DISCOVERY_INIT = "src/ats/discovery/__init__.py"
BOUNDED_DISCOVERY_TEST = "tests/test_discovery_bounded.py"
FIRST_DISCOVERY_SEARCH_MANIFEST = "research/discovery/SEARCH-EURUSD-H1-2021-2025-001.yaml"
EURUSD_H1_DISCOVERY = "src/ats/discovery/eurusd_h1.py"
EURUSD_H1_DISCOVERY_TOOL = "tools/discover_eurusd_h1.py"
EURUSD_H1_DISCOVERY_TEST = "tests/test_discovery_eurusd_h1.py"
FIRST_DISCOVERY_RESULT_SUMMARY = "reports/research/SEARCH-EURUSD-H1-2021-2025-001-summary.md"
REFERENCE_STRATEGY_2_SELECTION = "governance/program/REFERENCE_STRATEGY_2_SELECTION.md"
REFERENCE_STRATEGY_2_IDEA = "research/ideas/IDEA-0002.md"
REFERENCE_STRATEGY_2_HYPOTHESIS = "research/hypotheses/HYP-0002.md"
REFERENCE_STRATEGY_2_DATA_FEASIBILITY_PREP = "research/reviews/HYP-0002-DATA-FEASIBILITY-PREP.md"
REFERENCE_STRATEGY_2_DATA_FEASIBILITY = "research/reviews/HYP-0002-DATA-FEASIBILITY.md"
HYP0002_CONFIRMATORY_MANIFEST = "data/manifests/DATA-DUKASCOPY-EURUSDH1-HYP0002-001.yaml"
HYP0002_CONFIRMATORY_SCHEMA = "data/manifests/DATA-EURUSD-DUKASCOPY-H1-HYP0002.schema.json"
HYP0002_PROTOTYPE = "research/reviews/HYP-0002-PROTOTYPE-01.md"
HYP0002_PROTOTYPE_TOOL = "tools/hyp0002_proto01.py"
HYP0002_PROTOTYPE_TEST = "tests/test_hyp0002_proto01.py"
HYP0002_PROTOTYPE_RESULT = "reports/research/HYP-0002-PROTOTYPE-01-result.json"
REFERENCE_STRATEGY_2_CLOSEOUT = "governance/program/REFERENCE_STRATEGY_2_CLOSEOUT.md"
STRATEGY_3_SOURCING_REBASELINE = "governance/program/STRATEGY_3_SOURCING_REBASELINE.md"
STRATEGY_3_IDEA_SOURCING = "governance/program/STRATEGY_3_IDEA_SOURCING.md"
STRATEGY_3_FAMILY_SELECTION = "governance/program/STRATEGY_3_FAMILY_SELECTION.md"
STRATEGY_3_IDEA = "research/ideas/IDEA-0003.md"
STRATEGY_3_HYPOTHESIS = "research/hypotheses/HYP-0003.md"
STRATEGY_3_DATA_FEASIBILITY = "research/reviews/HYP-0003-DATA-FEASIBILITY.md"
STRATEGY_3_DATA_FEASIBILITY_PREP = "research/reviews/HYP-0003-DATA-FEASIBILITY-PREP.md"
HYP0003_DATA_FEASIBILITY_PREP_RESULT = (
    "reports/research/HYP-0003-DATA-FEASIBILITY-PREP-result.json"
)
HYP0003_DATA_FEASIBILITY_TOOL = "tools/hyp0003_data_feasibility.py"
HYP0003_DATA_FEASIBILITY_TEST = "tests/test_hyp0003_data_feasibility.py"
STRATEGY_3_DEVELOPMENT_DATA_PREP = (
    "research/reviews/HYP-0003-DEVELOPMENT-DATA-PREP.md"
)
HYP0003_DEVELOPMENT_DATA_TOOL = "tools/hyp0003_development_data.py"
HYP0003_DEVELOPMENT_DATA_TEST = "tests/test_hyp0003_development_data.py"
HYP0003_DEVELOPMENT_DATA_PREP_RESULT = (
    "reports/research/HYP-0003-DEVELOPMENT-DATA-PREP-result.json"
)
HYP0003_DEVELOPMENT_MANIFEST = (
    "data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001.yaml"
)
HYP0003_DEVELOPMENT_SCHEMA = (
    "data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV.schema.json"
)
HYP0003_PROTOTYPE = "research/reviews/HYP-0003-PROTOTYPE-01.md"
HYP0003_PROTOTYPE_TOOL = "tools/hyp0003_proto01.py"
HYP0003_PROTOTYPE_TEST = "tests/test_hyp0003_proto01.py"
HYP0003_PROTOTYPE_RESULT = "reports/research/HYP-0003-PROTOTYPE-01-result.json"
STRATEGY_3_CLOSEOUT = "governance/program/STRATEGY_3_CLOSEOUT.md"
STRATEGY_4_IDEA_SOURCING = "governance/program/STRATEGY_4_IDEA_SOURCING.md"
STRATEGY_4_FAMILY_SELECTION = "governance/program/STRATEGY_4_FAMILY_SELECTION.md"
STRATEGY_4_IDEA = "research/ideas/IDEA-0004.md"
STRATEGY_4_HYPOTHESIS = "research/hypotheses/HYP-0004.md"
STRATEGY_4_DATA_FEASIBILITY = "research/reviews/HYP-0004-DATA-FEASIBILITY.md"
STRATEGY_4_DEVELOPMENT_DATA_PREP = "research/reviews/HYP-0004-DEVELOPMENT-DATA-PREP.md"
HYP0004_DEVELOPMENT_DATA_TOOL = "tools/hyp0004_development_data.py"
HYP0004_DEVELOPMENT_DATA_TEST = "tests/test_hyp0004_development_data.py"
HYP0004_DEVELOPMENT_DATA_PREP_RESULT = (
    "reports/research/HYP-0004-DEVELOPMENT-DATA-PREP-result.json"
)
HYP0004_DEVELOPMENT_MANIFEST = (
    "data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001.yaml"
)
HYP0004_DEVELOPMENT_SCHEMA = (
    "data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV.schema.json"
)
HYP0004_PROTOTYPE = "research/reviews/HYP-0004-PROTOTYPE-01.md"
HYP0004_PROTOTYPE_TOOL = "tools/hyp0004_proto01.py"
HYP0004_PROTOTYPE_TEST = "tests/test_hyp0004_proto01.py"
HYP0004_PROTOTYPE_RESULT = "reports/research/HYP-0004-PROTOTYPE-01-result.json"
HYP0005_HYPOTHESIS = "research/hypotheses/HYP-0005.md"
HYP0005_DATA_FEASIBILITY_PREP = "research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md"
HYP0005_DATA_FEASIBILITY_TOOL = "tools/hyp0005_data_feasibility.py"
HYP0005_DATA_FEASIBILITY_TEST = "tests/test_hyp0005_data_feasibility.py"
STRATEGY_5_IDEA = "research/ideas/IDEA-0005.md"
HYP0006_HYPOTHESIS = "research/hypotheses/HYP-0006.md"
HYP0006_DATA_FEASIBILITY = "research/reviews/HYP-0006-DATA-FEASIBILITY.md"
HYP0006_DATA_FEASIBILITY_PREP = "research/reviews/HYP-0006-DATA-FEASIBILITY-PREP.md"
HYP0006_DATA_FEASIBILITY_TOOL = "tools/hyp0006_data_feasibility.py"
HYP0006_DATA_FEASIBILITY_TEST = "tests/test_hyp0006_data_feasibility.py"
HYP0006_CONTROLLED_DOWNLOAD_TOOL = "tools/hyp0006_dukascopy_controlled_download.py"
HYP0006_CONTROLLED_DOWNLOAD_TEST = "tests/test_hyp0006_dukascopy_controlled_download.py"
HYP0006_BROWSER_PILOT_TOOL = "tools/hyp0006_dukascopy_browser_pilot.py"
HYP0006_BROWSER_PILOT_TEST = "tests/test_hyp0006_dukascopy_browser_pilot.py"
HYP0006_BROWSER_BATCH_250_TOOL = "tools/hyp0006_dukascopy_browser_batch_250.py"
HYP0006_BROWSER_BATCH_250_TEST = "tests/test_hyp0006_dukascopy_browser_batch_250.py"
HYP0006_BROWSER_REMAINING_748_TOOL = "tools/hyp0006_dukascopy_browser_remaining_748.py"
HYP0006_BROWSER_REMAINING_748_TEST = "tests/test_hyp0006_dukascopy_browser_remaining_748.py"
HYP0006_BLS_SNAPSHOT_MANIFEST = "data/reference/HYP-0006-BLS-SCHEDULE-SNAPSHOT-MANIFEST.csv"
HYP0006_BLS_SNAPSHOT_INTAKE = "research/reviews/HYP-0006-BLS-SNAPSHOT-INTAKE.md"
HYP0006_DUKASCOPY_SOURCE_RECOVERY = "research/reviews/HYP-0006-DUKASCOPY-SOURCE-RECOVERY.md"
HYP0006_DATA_TOLERANCE_FREEZE = "research/reviews/HYP-0006-DATA-TOLERANCE-FREEZE.md"
HYP0006_DATA_TOLERANCE_FREEZE_TOOL = "tools/hyp0006_data_tolerance_freeze.py"
HYP0006_DATA_TOLERANCE_FREEZE_TEST = "tests/test_hyp0006_data_tolerance_freeze.py"
HYP0002_DATA_FEASIBILITY_TOOL = "tools/hyp0002_data_feasibility.py"
M1_EXIT = "governance/program/M1_EXIT_REVIEW.md"
M2_EXIT = "governance/program/M2_EXIT_REVIEW.md"
M3_EXIT = "governance/program/M3_EXIT_REVIEW.md"
M6_EXIT = "governance/program/M6_EXIT_REVIEW.md"
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
PROJECT_GPT_SYSTEM_INSTRUCTION = "governance/program/PROJECT_GPT_SYSTEM_INSTRUCTION.md"
AGENT_PRE_PUSH_CHECKLIST = "governance/program/AGENT_PRE_PUSH_CHECKLIST.md"
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
    "ATS_AGENT_PREFLIGHT.bat",
    "ATS_TASK_DIAG.bat",
    "tools/verify_repo.py",
    "tools/current_task_check.py",
    "tools/agent_preflight.py",
    "tools/current_task_diag.py",
    "tools/run_and_tee.py",
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
        MULTIPLE_RESEARCH_ACCOUNTING,
        TECHNICAL_STRATEGY_VALIDATION_PROFILE,
        DISCOVERY_SEARCH_MANIFEST_TEMPLATE, BOUNDED_DISCOVERY_ENGINE,
        BOUNDED_DISCOVERY_INIT, BOUNDED_DISCOVERY_TEST,
        FIRST_DISCOVERY_SEARCH_MANIFEST, EURUSD_H1_DISCOVERY,
        EURUSD_H1_DISCOVERY_TOOL, EURUSD_H1_DISCOVERY_TEST,
        FIRST_DISCOVERY_RESULT_SUMMARY, REFERENCE_STRATEGY_2_SELECTION,
        REFERENCE_STRATEGY_2_IDEA, REFERENCE_STRATEGY_2_HYPOTHESIS,
        REFERENCE_STRATEGY_2_DATA_FEASIBILITY_PREP,
        REFERENCE_STRATEGY_2_DATA_FEASIBILITY,
        HYP0002_CONFIRMATORY_MANIFEST,
        HYP0002_CONFIRMATORY_SCHEMA,
        HYP0002_PROTOTYPE,
        HYP0002_PROTOTYPE_TOOL,
        HYP0002_PROTOTYPE_TEST,
        HYP0002_PROTOTYPE_RESULT,
        REFERENCE_STRATEGY_2_CLOSEOUT,
        STRATEGY_3_SOURCING_REBASELINE,
        STRATEGY_3_IDEA_SOURCING,
        STRATEGY_3_FAMILY_SELECTION,
        STRATEGY_3_IDEA,
        STRATEGY_3_HYPOTHESIS,
        STRATEGY_3_DATA_FEASIBILITY,
        STRATEGY_3_DATA_FEASIBILITY_PREP,
        HYP0003_DATA_FEASIBILITY_PREP_RESULT,
        HYP0003_DATA_FEASIBILITY_TOOL,
        HYP0003_DATA_FEASIBILITY_TEST,
        STRATEGY_3_DEVELOPMENT_DATA_PREP,
        HYP0003_DEVELOPMENT_DATA_TOOL,
        HYP0003_DEVELOPMENT_DATA_TEST,
        HYP0003_DEVELOPMENT_DATA_PREP_RESULT,
        HYP0003_DEVELOPMENT_MANIFEST,
        HYP0003_DEVELOPMENT_SCHEMA,
        HYP0003_PROTOTYPE,
        HYP0003_PROTOTYPE_TOOL,
        HYP0003_PROTOTYPE_TEST,
        HYP0003_PROTOTYPE_RESULT,
        STRATEGY_3_CLOSEOUT,
        STRATEGY_4_IDEA_SOURCING,
        STRATEGY_4_FAMILY_SELECTION,
        STRATEGY_4_IDEA,
        STRATEGY_4_HYPOTHESIS,
        STRATEGY_4_DATA_FEASIBILITY,
        STRATEGY_4_DEVELOPMENT_DATA_PREP,
        HYP0004_DEVELOPMENT_DATA_TOOL,
        HYP0004_DEVELOPMENT_DATA_TEST,
        HYP0004_DEVELOPMENT_DATA_PREP_RESULT,
        HYP0004_DEVELOPMENT_MANIFEST,
        HYP0004_DEVELOPMENT_SCHEMA,
        HYP0004_PROTOTYPE,
        HYP0004_PROTOTYPE_TOOL,
        HYP0004_PROTOTYPE_TEST,
        HYP0004_PROTOTYPE_RESULT,
        HYP0005_HYPOTHESIS,
        HYP0005_DATA_FEASIBILITY_PREP,
        HYP0005_DATA_FEASIBILITY_TOOL,
        HYP0005_DATA_FEASIBILITY_TEST,
        STRATEGY_5_IDEA,
        HYP0006_HYPOTHESIS,
        HYP0006_DATA_FEASIBILITY,
        HYP0006_DATA_FEASIBILITY_PREP,
        HYP0006_DATA_FEASIBILITY_TOOL,
        HYP0006_DATA_FEASIBILITY_TEST,
        HYP0006_CONTROLLED_DOWNLOAD_TOOL,
        HYP0006_CONTROLLED_DOWNLOAD_TEST,
        HYP0006_BROWSER_PILOT_TOOL,
        HYP0006_BROWSER_PILOT_TEST,
        HYP0006_BROWSER_BATCH_250_TOOL,
        HYP0006_BROWSER_BATCH_250_TEST,
        HYP0006_BROWSER_REMAINING_748_TOOL,
        HYP0006_BROWSER_REMAINING_748_TEST,
        HYP0006_BLS_SNAPSHOT_MANIFEST,
        HYP0006_BLS_SNAPSHOT_INTAKE,
        HYP0006_DUKASCOPY_SOURCE_RECOVERY,
        HYP0006_DATA_TOLERANCE_FREEZE,
        HYP0006_DATA_TOLERANCE_FREEZE_TOOL,
        HYP0006_DATA_TOLERANCE_FREEZE_TEST,
        HYP0002_DATA_FEASIBILITY_TOOL,
        M1_EXIT, M2_EXIT, M3_EXIT, M6_EXIT, REFERENCE_STRATEGY_SELECTION, REFERENCE_STRATEGY_IDEA,
        REFERENCE_STRATEGY_HYPOTHESIS, REFERENCE_STRATEGY_DATA_FEASIBILITY,
        REFERENCE_STRATEGY_PROTOTYPE, PROTO01_RESULT, PROTO01_SCHEMA, PROTO01_MANIFEST,
        PROTO01_TOOL,
        CONSUMER_PROFILE,
        RESEARCH_STACK_ADR, ENVIRONMENT_SPEC,
        LOCAL_CI_GATE,
        LOCAL_CI_TROUBLESHOOTING, LOCAL_CI_FAILURE_REGISTRY, PROJECT_GPT_SYSTEM_INSTRUCTION,
        AGENT_PRE_PUSH_CHECKLIST,
        DATASET_MANIFEST_SPEC,
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
        "multiple_research_accounting",
        "technical_strategy_validation_profile",
        "discovery_search_manifest_template", "bounded_discovery_engine",
        "first_discovery_search_manifest", "first_discovery_runner",
        "first_discovery_result_summary", "reference_strategy_2_selection",
        "reference_strategy_2_idea", "reference_strategy_2_hypothesis",
        "reference_strategy_2_data_feasibility_prep",
        "reference_strategy_2_data_feasibility",
        "reference_strategy_2_confirmatory_manifest",
        "reference_strategy_2_confirmatory_schema",
        "reference_strategy_2_prototype",
        "reference_strategy_2_prototype_runner",
        "reference_strategy_2_prototype_result",
        "reference_strategy_2_closeout",
        "strategy_3_sourcing_rebaseline",
        "strategy_3_idea_sourcing",
        "strategy_3_family_selection",
        "strategy_3_idea",
        "strategy_3_hypothesis",
        "strategy_3_data_feasibility",
        "strategy_3_data_feasibility_prep",
        "strategy_3_data_feasibility_tool",
        "strategy_3_development_data_prep",
        "strategy_3_development_data_tool",
        "strategy_3_prototype",
        "strategy_3_prototype_runner",
        "strategy_3_prototype_test",
        "strategy_3_prototype_result",
        "strategy_3_closeout",
        "strategy_4_idea_sourcing",
        "strategy_4_family_selection",
        "strategy_4_idea",
        "strategy_4_hypothesis",
        "strategy_4_data_feasibility",
        "strategy_4_development_data_prep",
        "strategy_4_development_data_tool",
        "strategy_4_development_data_test",
        "strategy_4_development_data_prep_result",
        "strategy_4_development_dataset_manifest",
        "strategy_4_development_dataset_schema",
        "strategy_4_prototype",
        "strategy_4_prototype_runner",
        "strategy_4_prototype_test",
        "strategy_4_prototype_result",
        "strategy_4_confirmatory_hypothesis",
        "strategy_4_confirmatory_data_feasibility_prep",
        "strategy_4_confirmatory_data_feasibility_tool",
        "strategy_4_confirmatory_data_feasibility_test",
        "strategy_5_idea",
        "strategy_5_hypothesis",
        "strategy_5_data_feasibility",
        "strategy_5_data_feasibility_prep",
        "strategy_5_data_feasibility_tool",
        "strategy_5_data_feasibility_test",
        "strategy_5_bls_snapshot_manifest",
        "strategy_5_bls_snapshot_intake",
        "strategy_5_dukascopy_source_recovery",
        "strategy_5_dukascopy_controlled_downloader",
        "strategy_5_dukascopy_controlled_downloader_test",
        "strategy_5_dukascopy_browser_pilot",
        "strategy_5_dukascopy_browser_pilot_test",
        "strategy_5_dukascopy_browser_batch_250",
        "strategy_5_dukascopy_browser_batch_250_test",
        "strategy_5_dukascopy_browser_remaining_748",
        "strategy_5_dukascopy_browser_remaining_748_test",
        "strategy_5_data_tolerance_freeze",
        "strategy_5_data_tolerance_freeze_tool",
        "strategy_5_data_tolerance_freeze_test",
        "m1_exit_review",
        "m2_exit_review", "m3_exit_review", "m6_exit_review", "reference_strategy_1_selection", "reference_strategy_1_idea",
        "reference_strategy_1_hypothesis", "reference_strategy_1_data_feasibility",
        "reference_strategy_1_dataset_manifest", "reference_consumer_profile", "research_stack_adr", "research_environment_spec",
        "dataset_manifest_spec", "local_ci_gate", "local_ci_troubleshooting",
        "local_ci_failure_registry",
        "project_gpt_system_instruction",
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
    core.CONTENT_MARKERS[MULTIPLE_RESEARCH_ACCOUNTING] = (
        "preserves the **selection path**",
        "Material Research Attempt",
        "DISCOVERY_SEARCH",
        "PROTECTED_BLOCK_REVEAL",
        "Search-space accounting",
        "What does not need a new research attempt",
        "Research Freedom Summary",
        "CONSUMED_PROTECTED_BLOCK",
        "Experiment Registry",
        "HYP-0001 remains `REJECTED_AT_R3`",
    )
    core.CONTENT_MARKERS[TECHNICAL_STRATEGY_VALIDATION_PROFILE] = (
        "price-driven technical strategies",
        "DEVELOPMENT → VALIDATION → INDEPENDENT_EXAMINATION",
        "V1 — Parameter neighbourhood",
        "V2 — Time / regime slicing",
        "V3 — Observation dependence",
        "V4 — Concentration / outliers",
        "V5 — Cost / execution sensitivity",
        "V6 — Resampling / path uncertainty",
        "V7 — Research freedom / multiple-research accounting",
        "Research Freedom Summary",
        "S06 freeze boundary",
        "S07 freeze boundary",
        "HYP-0001 / PROTO-01",
    )
    core.CONTENT_MARKERS[DISCOVERY_SEARCH_MANIFEST_TEMPLATE] = (
        "SEARCH-SYNTHETIC-M6-001",
        "Synthetic non-market",
        "max_combinations: 3",
        "ALL_VALIDATION_AND_INDEPENDENT_BLOCKS",
        "SYNTHETIC_TEMPLATE",
        "src/ats/discovery/bounded.py",
    )
    core.CONTENT_MARKERS[BOUNDED_DISCOVERY_ENGINE] = (
        "DISCOVERY_SEARCH",
        "EXPLORATORY_OBSERVATION",
        "PREDECLARED_SHORTLIST_RULE_ONLY",
        "declared alternatives exceed max_combinations",
        "metric set mismatch",
        "SHORTLIST_FOR_IDEA_INTAKE",
        "NO_PATTERN_SHORTLISTED",
        "random_seed and stochastic_protocol must be declared together",
    )
    core.CONTENT_MARKERS[BOUNDED_DISCOVERY_TEST] = (
        "test_template_loads_and_full_search_space_is_retained",
        "qualified_evidence_class",
        "NO_PATTERN_SHORTLISTED",
        "test_search_budget_blocks_undeclared_expansion",
        "metric set mismatch",
    )
    core.CONTENT_MARKERS[FIRST_DISCOVERY_SEARCH_MANIFEST] = (
        "SEARCH-EURUSD-H1-2021-2025-001",
        "DATA-DUKASCOPY-EURUSDH1-PROTO01-001",
        "RETURN_TAIL_CONTINUATION",
        "RETURN_TAIL_REVERSAL",
        "PRIOR_MID_CLOSE_RETURN_QUANTILE",
        "max_combinations: 16",
        "shortlist_score",
        "ALL_FUTURE_VALIDATION_AND_INDEPENDENT_BLOCKS",
        "tools/discover_eurusd_h1.py",
    )
    core.CONTENT_MARKERS[EURUSD_H1_DISCOVERY] = (
        "EurusdH1Evaluator",
        "PRIOR_MID_CLOSE_RETURN_QUANTILE",
        "RETURN_TAIL_CONTINUATION",
        "RETURN_TAIL_REVERSAL",
        "lookback_hours",
        "tail_quantile",
        "shortlist_score",
    )
    core.CONTENT_MARKERS[EURUSD_H1_DISCOVERY_TOOL] = (
        "SEARCH-EURUSD-H1-2021-2025-001",
        "verify_implementation_revision",
        "Search Manifest code_revision",
        "EXPLORATORY_OBSERVATION",
        "PREDECLARED_SHORTLIST_RULE_ONLY",
        "Shortlisted alternatives",
    )
    core.CONTENT_MARKERS[EURUSD_H1_DISCOVERY_TEST] = (
        "test_evaluator_returns_finite_metrics_and_events",
        "test_reversal_direction_contract_is_enforced",
        "test_gaps_are_not_crossed",
        "test_parameter_set_is_closed",
    )
    core.CONTENT_MARKERS[FIRST_DISCOVERY_RESULT_SUMMARY] = (
        "SHORTLIST_FOR_IDEA_INTAKE",
        "Evaluated alternatives: `16 / 16`",
        "continuation: `0 / 8` shortlisted",
        "reversal: `5 / 8` shortlisted",
        "24H-effect reversal: `4 / 4` shortlisted",
        "2f363b3fcdc3f80600bf1f488197f9f848ad8b286248c611ff2aa8d71ac6a318",
        "No exact lookback, tail threshold or effect/holding horizon is selected",
    )
    core.CONTENT_MARKERS[REFERENCE_STRATEGY_2_SELECTION] = (
        "SINGLE_INSTRUMENT_1H_TWO_SIDED_RETURN_TAIL_REVERSAL",
        "0 / 8",
        "5 / 8",
        "No ranking or tie-break rule among shortlisted alternatives was preregistered.",
        "Research Freedom Summary",
        "IDEA-0002",
        "does not authorize",
    )
    core.CONTENT_MARKERS[REFERENCE_STRATEGY_2_IDEA] = (
        "Idea ID: `IDEA-0002`",
        "BOUNDED_MARKET_PATTERN_DISCOVERY",
        "TWO_SIDED_REVERSAL_AFTER_EXTREME_PRIOR_RETURN",
        "selection bias",
        "84%–90%",
        "Result: `RELATED`",
        "Decision: `SCREEN`",
        "HYP-0002",
    )
    core.CONTENT_MARKERS[REFERENCE_STRATEGY_2_HYPOTHESIS] = (
        "Hypothesis ID: `HYP-0002`",
        "Parent Idea ID: `IDEA-0002`",
        "post-discovery",
        "R24(t)",
        "Q10_DEV",
        "Q90_DEV",
        "both tails must satisfy both inequalities",
        "previously unseen",
        "Decision: `DATA_FEASIBILITY`",
        "READY_FOR_DATA_FEASIBILITY",
    )
    core.CONTENT_MARKERS[REFERENCE_STRATEGY_2_DATA_FEASIBILITY_PREP] = (
        "ATS2-M6-004",
        "Q10_DEV",
        "Q90_DEV",
        "2026-01-01T00:00:00Z",
        "2026-09-01T00:00:00Z",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "tools/hyp0002_data_feasibility.py",
    )
    core.CONTENT_MARKERS[HYP0002_DATA_FEASIBILITY_TOOL] = (
        "CONFIRM_START = datetime(2026, 1, 1",
        "CONFIRM_END = datetime(2026, 9, 1",
        "EXPECTED_DEVELOPMENT_SHA256",
        "linear_quantile",
        "Q10_DEV",
        "Q90_DEV",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "HYP0002_DATA_FEASIBILITY_REPORT.txt",
    )
    core.CONTENT_MARKERS[REFERENCE_STRATEGY_2_DATA_FEASIBILITY] = (
        "Hypothesis ID: `HYP-0002`",
        "Review status: `CONDITIONAL`",
        "Q10_DEV = -0.005141454111",
        "Q90_DEV = 0.005394148971",
        "DATA-DUKASCOPY-EURUSDH1-HYP0002-001@1.0.0",
        "d62a7103478da2a79a0992310005bcd0afc8dc0010088dccd2ed0e54e2ec112f",
        "ccbf5ceff1ee1a5a1cb62dead3af531ce05ae4f71e4da32140b526326e686392",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
        "Decision: `CONDITIONAL`",
        "HYP-0002-PROTOTYPE-01.md",
    )
    core.CONTENT_MARKERS[HYP0002_CONFIRMATORY_MANIFEST] = (
        'dataset_id: "DATA-DUKASCOPY-EURUSDH1-HYP0002-001"',
        'dataset_version: "1.0.0"',
        "4,153 aligned rows",
        "ccbf5ceff1ee1a5a1cb62dead3af531ce05ae4f71e4da32140b526326e686392",
        "d62a7103478da2a79a0992310005bcd0afc8dc0010088dccd2ed0e54e2ec112f",
        'availability_mode: "EXPLICIT_FIELD"',
        'missing: "ALLOW_DECLARED_GAPS"',
        "tools/hyp0002_data_feasibility.py@8b1e2dbc0e604c7fb3ca8297e0f61f252147619a",
    )
    core.CONTENT_MARKERS[HYP0002_CONFIRMATORY_SCHEMA] = (
        "HYP-0002 confirmatory EURUSD 1H aligned BID/ASK rows",
        "event_time",
        "availability_time",
        "bid_open",
        "ask_open",
        "additionalProperties",
    )
    core.CONTENT_MARKERS[HYP0002_PROTOTYPE] = (
        "Prototype sequence: `PROTO-01`",
        "Status: `COMPLETED / REJECT`",
        "Q10_DEV = -0.005141454111",
        "Q90_DEV = 0.005394148971",
        "all four primary inequalities",
        "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
        "201",
        "122",
        "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED",
        "tools/hyp0002_proto01.py",
        "Decision: `REJECT`",
    )
    core.CONTENT_MARKERS[HYP0002_PROTOTYPE_TOOL] = (
        "EXPECTED_DATASET_SHA256",
        "Q10_DEV = -0.005141454111",
        "Q90_DEV = 0.005394148971",
        "up_signed_return",
        "down_signed_return",
        "ALL_FOUR_PRIMARY_INEQUALITIES_MET",
        "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED",
        "ONE_OR_BOTH_TAILS_HAVE_ZERO_EVENTS",
        "HYP0002_PROTO01_RESULT.json",
    )
    core.CONTENT_MARKERS[HYP0002_PROTOTYPE_TEST] = (
        "test_signed_return_side_conventions",
        "test_two_sided_decision_contract",
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED",
        "ONE_OR_BOTH_TAILS_HAVE_ZERO_EVENTS",
    )
    core.CONTENT_MARKERS[HYP0002_PROTOTYPE_RESULT] = (
        '"decision": "REJECT"',
        '"decision_reason": "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED"',
        '"event_count": 201',
        '"event_count": 122',
        '"mean_signed_return": 0.0004902837195506912',
        '"mean_signed_return": -0.0002984301044940726',
        '"git_commit": "96d7b90ac908cacccfefbccbe8daa06867b2f18c"',
        '"prepared_csv_sha256": "d62a7103478da2a79a0992310005bcd0afc8dc0010088dccd2ed0e54e2ec112f"',
    )
    core.CONTENT_MARKERS[REFERENCE_STRATEGY_2_CLOSEOUT] = (
        "ATS2-M6-008",
        "REJECTED_AT_R3",
        "cf89ae89680aad25d24944dc737c4092f995327dca022a7c6a19d7ea102e552e",
        "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED",
        "201",
        "122",
        "WBS-6.3",
        "WBS-6.7",
        "PASS — NEGATIVE_EVIDENCE_PRESERVED_WITHOUT_RESCUE",
        "M6 milestone status remains",
    )
    core.CONTENT_MARKERS[STRATEGY_3_SOURCING_REBASELINE] = (
        "ATS2-RF-001",
        "RESEARCH_FACTORY_CONTINUOUS",
        "M6_REFERENCE_STRATEGY_2 = COMPLETED / PASS",
        "Candidate count remains",
        "WBS-RF.0",
        "WBS-RF.1",
        "WBS-RF.4",
        "M4.9 = BLOCKED_PENDING_S05_CANDIDATE",
        "Strategy #3 idea sourcing",
        "All live/capital permissions remain false",
    )
    core.CONTENT_MARKERS[STRATEGY_3_IDEA_SOURCING] = (
        "ATS2-RF-002",
        "Development optimization rule",
        "S3-FAM-01",
        "S3-FAM-02",
        "S3-FAM-03",
        "Order-flow prediction",
        "Families reviewed for this task: `4`",
        "Immediate shortlist for Strategy #3 Idea selection: `3`",
        "No family is ranked",
        "ATS2-RF-003",
    )
    core.CONTENT_MARKERS[STRATEGY_3_FAMILY_SELECTION] = (
        "ATS2-RF-003",
        "S3-FAM-02",
        "CROSS_SECTIONAL_CURRENCY_MOMENTUM",
        "Plausible data path",
        "Cheap falsification path",
        "Research-freedom boundary",
        "research/ideas/IDEA-0003.md",
        "Decision:",
        "SCREEN",
        "HYP-0003",
    )
    core.CONTENT_MARKERS[STRATEGY_3_IDEA] = (
        "Idea ID: `IDEA-0003`",
        "Status: `SCREENING`",
        "LITERATURE_INFORMED_RESEARCH_FACTORY_SOURCING",
        "CROSS_SECTIONAL_CONTINUATION_OF_RELATIVE_CURRENCY_PERFORMANCE",
        "multi-currency FX universe",
        "bounded development policy",
        "multiple testing",
        "Result: `RELATED`",
        "Decision: `SCREEN`",
        "research/hypotheses/HYP-0003.md",
    )
    core.CONTENT_MARKERS[STRATEGY_3_HYPOTHESIS] = (
        "Hypothesis ID: `HYP-0003`",
        "Parent Idea ID: `IDEA-0003`",
        "development-stage",
        "formation periods `1, 3, 6, 9, 12` months",
        "exactly `25`",
        "at least `13 / 25`",
        "one-sixth",
        "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
        "new Hypothesis ID",
        "READY_FOR_DATA_FEASIBILITY",
    )
    core.CONTENT_MARKERS[STRATEGY_3_DATA_FEASIBILITY] = (
        "Hypothesis ID: `HYP-0003`",
        "Review status: `CONDITIONAL`",
        "AUD, CAD, CHF, EUR, GBP, JPY, NOK, NZD, SEK",
        "basket_size = max(1, ceil(eligible_currency_count / 6))",
        "1 / source ASK",
        "1 / source BID",
        "2021-09-01T00:00:00Z",
        "2026-09-01T00:00:00Z",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "ATS2-RF-006",
        "RF-007 freeze update",
        "RF-008 diagnostic correction (2026-09-24)",
        "separately aggregated BID/ASK OHLC extrema",
        "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001",
        "a88add123fd42e83396ba17de13cf65fedf18d8e0a5e1eca476ed6338c91b45e",
        "ATS2-RF-008",
        "RF-009 development data freeze update",
        "FREEZE_DEVELOPMENT_DATASET",
        "63e1bc9c7e1ba2e001ecdd9918244d83db0e58c3",
        "9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a",
        "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2",
        "1,014,509",
        "207",
        "184",
        "ATS2-RF-009",
    )
    core.CONTENT_MARKERS[HYP0003_DATA_FEASIBILITY_PREP_RESULT] = (
        '"task_id": "ATS2-RF-006"',
        '"preparation_commit": "acf197d5774116c7d9a8b742eab77c6ee3447214"',
        '"preparation_decision": "READY_FOR_FREEZE_REVIEW"',
        '"retained_currency_count": 9',
        '"common_possible_development_start": "2003-08-03T21:00:00Z"',
        '"history_metadata_sha256": "215ad432126018f4f871a1e10bc3f315524b84ae29d83fc3fd3adc188107417d"',
        '"probe_bundle_sha256": "a88add123fd42e83396ba17de13cf65fedf18d8e0a5e1eca476ed6338c91b45e"',
        '"information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED"',
    )
    core.CONTENT_MARKERS[STRATEGY_3_DATA_FEASIBILITY_PREP] = (
        "ATS2-RF-006",
        "PREPARATION_PROTOCOL_FROZEN",
        "AUDUSD, USDCAD, USDCHF, EURUSD, GBPUSD, USDJPY, USDNOK, NZDUSD, USDSEK",
        "2021-09-01T00:00:00Z",
        "probe_bundle_sha256",
        "READY_FOR_FREEZE_REVIEW",
        "INSUFFICIENT_SOURCE_UNIVERSE",
        "HYP0003_DATA_FEASIBILITY.json",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "ATS2-RF-007",
    )
    core.CONTENT_MARKERS[HYP0003_DATA_FEASIBILITY_TOOL] = (
        "HYP-0003",
        "PROTECTED_START = datetime(2021, 9, 1",
        "MINIMUM_FEASIBLE_CURRENCIES = 6",
        "CANDIDATES",
        "HISTORY_START_URLS",
        "INSTRUMENTS_URL",
        "H1_PERIOD_MS = 3_600_000",
        "parse_history_start",
        "parse_instruments_jsonp",
        "load_history_metadata",
        "history_start_datetime",
        "PROBE_BATCH_BACKOFF_SECONDS",
        "probe_side_resilient",
        "urllib.error.URLError, OSError",
        "normalized_bid_ask",
        "probe_bundle_hash",
        "READY_FOR_FREEZE_REVIEW",
        "INSUFFICIENT_SOURCE_UNIVERSE",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "HYP0003_DATA_FEASIBILITY_REPORT.txt",
    )
    core.CONTENT_MARKERS[HYP0003_DATA_FEASIBILITY_TEST] = (
        "test_source_url_uses_zero_based_dukascopy_month",
        "test_parse_history_start_h1_metadata",
        "test_parse_instruments_jsonp_h1_fallback",
        "test_load_history_metadata_falls_back_to_instruments_jsonp",
        "test_fetch_bytes_normalizes_direct_oserror",
        "test_probe_side_resilient_retries_transient_network_error",
        "test_normalized_bid_ask_preserves_executable_order",
        "INVERSE",
    )
    core.CONTENT_MARKERS[STRATEGY_3_DEVELOPMENT_DATA_PREP] = (
        "ATS2-RF-008",
        "PREPARATION_PROTOCOL_FROZEN",
        "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001",
        "3906",
        "jetta.dukascopy.com/v1",
        "no-forward-fill/no-interpolation",
        "side-specific aggregates",
        "Component-wise `ASK >= BID`",
        "JETTA_JSON",
        "provider-native Jetta consumer",
        "diagnostic-only",
        "never be clipped, reordered, spread-repaired, interpolated or forward-filled",
        "Legacy `BI5` OHLC geometry validation remains strict",
        "normalization is limited to DIRECT/INVERSE mapping plus finite/positive output checks",
        "BID and ASK are an atomic source pair",
        "Mixed `JETTA_JSON + BI5` BID/ASK pairs are prohibited",
        "USDJPY = 1000",
        "READY_FOR_DEVELOPMENT_DATA_FREEZE",
        "INSUFFICIENT_DEVELOPMENT_DATA",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "ATS2-RF-009",
    )
    core.CONTENT_MARKERS[HYP0003_DEVELOPMENT_DATA_TOOL] = (
        "HYP-0003",
        "DATA_START = datetime(2003, 8, 3, 21",
        "DATA_END = datetime(2021, 9, 1",
        "JETTA_API_ROOT",
        "jetta.dukascopy.com/v1",
        "SOURCE_FORMAT_JETTA_JSON",
        "invalid Jetta price",
        "POINT_DIVISORS",
        '"USDJPY": 1_000',
        "development_months",
        "jetta_source_url",
        "download_jetta_source_once",
        "download_legacy_source_once",
        "download_source_resilient",
        "download_source_pair_from_format",
        "download_source_pair_once",
        "download_source_pair_resilient",
        "mixed source formats",
        "decode_jetta_month",
        "decode_source_object",
        "normalize_pair_ohlc",
        "source_bundle_hash",
        "supports_longest_12_12_geometry",
        "READY_FOR_DEVELOPMENT_DATA_FREEZE",
        "INSUFFICIENT_DEVELOPMENT_DATA",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "HYP0003_DEVELOPMENT_DATA_REPORT.txt",
    )
    core.CONTENT_MARKERS[HYP0003_DEVELOPMENT_DATA_TEST] = (
        "test_development_months_are_frozen_before_protected_tail",
        "test_point_divisors_are_explicit_and_jpy_specific",
        "test_jetta_source_url_uses_current_h1_month_bucket",
        "test_decode_jetta_month_preserves_real_gaps_without_flat_fill",
        "test_decode_jetta_month_preserves_provider_geometry_discrepancy",
        "test_download_source_prefers_jetta_provider_path",
        "test_download_source_reuses_legacy_cache_before_jetta_network",
        "test_source_pair_falls_back_to_coherent_jetta_after_partial_legacy",
        "test_decode_month_uses_frozen_point_divisor",
        "test_decode_month_rejects_out_of_order_records",
        "test_normalize_pair_ohlc_preserves_side_semantics",
        "test_normalize_pair_ohlc_accepts_independently_aggregated_extrema",
        "test_normalize_pair_ohlc_preserves_prevalidated_one_unit_jetta_geometry",
        "test_source_bundle_hash_is_order_independent",
        "test_monthly_cutoff_uses_last_expected_fx_market_hour",
        "test_longest_12_12_geometry_respects_boundaries",
        "test_download_source_rejects_protected_tail_before_network",
        "test_download_source_resilient_retries_transient_error",
    )
    core.CONTENT_MARKERS[HYP0003_DEVELOPMENT_DATA_PREP_RESULT] = (
        '"task_id": "ATS2-RF-008"',
        '"preparation_commit": "63e1bc9c7e1ba2e001ecdd9918244d83db0e58c3"',
        '"launcher_status": "PASS"',
        '"preparation_decision": "READY_FOR_DEVELOPMENT_DATA_FREEZE"',
        '"source_objects_acquired": 3906',
        '"source_objects_missing": 0',
        '"source_bundle_sha256": "9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a"',
        '"prepared_csv_sha256": "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2"',
        '"prepared_rows": 1014509',
        '"eligible_monthly_ranking_points_ge6": 207',
        '"eligible_longest_12_12_geometry_points": 184',
        '"protected_tail_source_objects_requested": 0',
        '"information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED"',
    )
    core.CONTENT_MARKERS[HYP0003_DEVELOPMENT_MANIFEST] = (
        'dataset_id: "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001"',
        'dataset_version: "1.0.0"',
        "source-bundle-sha256:9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a",
        'location: "data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv"',
        'schema_reference: "data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV.schema.json"',
        'start: "2003-08-03T21:00:00Z"',
        'end: "2021-08-31T23:00:00Z"',
        'availability_mode: "EXPLICIT_FIELD"',
        'digest: "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2"',
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    )
    core.CONTENT_MARKERS[HYP0003_DEVELOPMENT_SCHEMA] = (
        '"event_time"',
        '"availability_time"',
        '"currency"',
        '"source_symbol"',
        '"source_orientation"',
        '"sequence"',
        '"bid_open"',
        '"ask_close"',
        '"additionalProperties": false',
    )
    core.CONTENT_MARKERS[HYP0003_PROTOTYPE] = (
        "HYP-0003",
        "PROTO-01",
        "COMPLETED / REJECT",
        "25 / 25",
        "basket_size = max(1, ceil(eligible_currency_count / 6))",
        "winner_long_returns",
        "loser_short_returns",
        "QUOTE_EXECUTABLE_AFTER_SPREAD_BEFORE_FINANCING",
        "ONE_OR_MORE_BROAD_REGION_CRITERIA_FAILED",
        "DEVELOPMENT_REVEALED_PROTOTYPE_REJECTED",
        "a1feee3d6495afdcc46f81ce0ee8e137896a77a3bd52de8baf6cbf53da1a7620",
        "STOP_HYP0003",
    )
    core.CONTENT_MARKERS[HYP0003_PROTOTYPE_RESULT] = (
        '"schema_version": "hyp0003-proto01-result-1"',
        '"hypothesis_id": "HYP-0003"',
        '"prototype_sequence": "PROTO-01"',
        '"declared_cell_count": 25',
        '"all_cells_observed": true',
        '"median_cell_mean": -0.0013404354655954772',
        '"positive_mean_cell_count": 8',
        '"positive_formation_period_count": 4',
        '"positive_holding_period_count": 4',
        '"decision": "REJECT"',
        '"decision_reason": "ONE_OR_MORE_BROAD_REGION_CRITERIA_FAILED"',
        '"next_action": "STOP_HYP0003"',
        '"git_commit": "f974b9bb60a6cc295cb8aaba4a263499c14769c0"',
    )
    core.CONTENT_MARKERS[STRATEGY_3_CLOSEOUT] = (
        "ATS2-RF-012",
        "REJECTED_AT_R3",
        "reports/research/HYP-0003-PROTOTYPE-01-result.json",
        "a1feee3d6495afdcc46f81ce0ee8e137896a77a3bd52de8baf6cbf53da1a7620",
        "8 / 25",
        "4 / 5",
        "NEGATIVE_EVIDENCE_PRESERVED_WITHOUT_RESCUE",
        "ATS2-RF-013 — Strategy #4 idea sourcing",
    )
    core.CONTENT_MARKERS[STRATEGY_4_IDEA_SOURCING] = (
        "ATS2-RF-013",
        "SOURCING_SHORTLIST_READY",
        "S4-FAM-01 - Currency carry / interest-rate differential",
        "S4-FAM-02 - Macroeconomic announcement response",
        "S4-FAM-03 - Intraday time/session effect",
        "S4-FAM-04 - Currency value / PPP / real-exchange-rate deviation",
        "S4-FAM-05 - Customer/order-flow prediction",
        "BIS Bulletin 124",
        "NBER Working Paper 8959",
        "BIS Working Paper 405",
        "Families reviewed: `5`",
        "Immediate shortlist for RF-014 family selection: `4`",
        "No family is ranked.",
        "No family is selected.",
        "ATS2-RF-014 - Strategy #4 family selection and Idea intake",
    )
    core.CONTENT_MARKERS[STRATEGY_4_FAMILY_SELECTION] = (
        "ATS2-RF-014",
        "S4-FAM-03 — INTRADAY_TIME_SESSION_EFFECT",
        "Distinct mechanism",
        "Reproducible data path",
        "Cheap falsification path",
        "Research-freedom boundary",
        "research/ideas/IDEA-0004.md",
        "`SCREEN`",
        "ATS2-RF-015 — HYP-0004 formation",
        "No claim is made that any unselected family is inferior",
    )
    core.CONTENT_MARKERS[STRATEGY_4_IDEA] = (
        "Idea ID: `IDEA-0004`",
        "Status: `SCREENING`",
        "LITERATURE_INFORMED_RESEARCH_FACTORY_SOURCING",
        "CLOCK_SESSION_CONDITIONAL_FX_DISTRIBUTION_SHIFT",
        "FX_SPOT_OTC",
        "Decision: `SCREEN`",
        "research/hypotheses/HYP-0004.md",
        "No directional sign, session boundary, instrument, bucket width, threshold or target magnitude is fixed by this Idea.",
    )
    core.CONTENT_MARKERS[STRATEGY_4_HYPOTHESIS] = (
        "Hypothesis ID: `HYP-0004`",
        "Parent Idea ID: `IDEA-0004`",
        "READY_FOR_DATA_FEASIBILITY",
        "CORE_ACTIVE",
        "TRANSITION",
        "OFF_HOURS",
        "EURUSD",
        "median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)",
        "median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)",
        "DATA_FEASIBILITY",
        "No HYP-0004 outcome may be computed before the Data Feasibility review permits it.",
    )
    core.CONTENT_MARKERS[STRATEGY_4_DATA_FEASIBILITY] = (
        "ATS2-RF-016",
        "Hypothesis ID: `HYP-0004`",
        "Review status: `CONDITIONAL`",
        "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001",
        "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2",
        "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001",
        "ask_open >= bid_open",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "Prototype authorization:",
        "`NOT_YET_AUTHORIZED`",
        "ATS2-RF-017 — HYP-0004 development data preparation",
        "RF-018 development data freeze update",
        "FREEZE_DEVELOPMENT_DATASET",
        "3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6",
        "111938 + 940 + 21 + 1 = 112900",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "ATS2-RF-019 — HYP-0004 PROTO-01 freeze",
    )
    core.CONTENT_MARKERS[STRATEGY_4_DEVELOPMENT_DATA_PREP] = (
        "ATS2-RF-017",
        "PREPARATION_PROTOCOL_FROZEN",
        "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001",
        "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2",
        "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001",
        "ask_open >= bid_open",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "exact-next-hour",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "ATS2-RF-018 — HYP-0004 development data freeze",
    )
    core.CONTENT_MARKERS[HYP0004_DEVELOPMENT_DATA_TOOL] = (
        'TASK_ID = "ATS2-RF-017"',
        "EXPECTED_PARENT_SHA256",
        "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001",
        "bucket_for_hour",
        "ask_open < bid_open",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "eligible_exact_next_hour_count",
        "outcome_metrics_computed",
        "primary_claim_evaluated",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "READY_FOR_DEVELOPMENT_DATA_FREEZE",
    )
    core.CONTENT_MARKERS[HYP0004_DEVELOPMENT_DATA_TEST] = (
        "test_bucket_mapping_is_frozen",
        "test_geometry_summary_counts_exact_next_hour_without_outcomes",
        "test_geometry_summary_distinguishes_closed_and_missing_hours",
        "test_load_eurusd_rows_verifies_parent_identity_and_filters",
        "test_load_eurusd_rows_rejects_boundary_crossing",
        "test_derived_csv_contains_no_hypothesis_outcome_columns",
    )
    core.CONTENT_MARKERS[HYP0004_DEVELOPMENT_DATA_PREP_RESULT] = (
        '"boundary_availability_mode": "H1_OPEN_PROXY_AT_EVENT_TIME"',
        '"derived_row_count": 112900',
        '"eligible_exact_next_hour_count": 111938',
        '"CORE_ACTIVE": 47012',
        '"OFF_HOURS": 46737',
        '"TRANSITION": 18189',
        '"derived_csv_sha256": "3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6"',
        '"git_commit": "ae9767a71b3860e55d345afb34b2f9c18b5dd063"',
        '"information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED"',
        '"preparation_decision": "READY_FOR_DEVELOPMENT_DATA_FREEZE"',
        '"primary_claim_evaluated": false',
    )
    core.CONTENT_MARKERS[HYP0004_DEVELOPMENT_MANIFEST] = (
        'dataset_id: "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001"',
        'dataset_version: "1.0.0"',
        "112,900",
        "111,938",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "parent_row_availability_time",
        "3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    )
    core.CONTENT_MARKERS[HYP0004_DEVELOPMENT_SCHEMA] = (
        "HYP-0004 frozen EUR/USD H1 bar-open development rows",
        '"parent_row_availability_time"',
        '"source_symbol"',
        '"const": "EURUSD"',
        '"bid_open"',
        '"ask_open"',
        '"utc_bucket"',
        '"CORE_ACTIVE"',
        '"TRANSITION"',
        '"OFF_HOURS"',
    )
    core.CONTENT_MARKERS[HYP0004_PROTOTYPE] = (
        "HYP-0004 / PROTO-01",
        "COMPLETED / DEVELOPMENT_PASS",
        "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001@1.0.0",
        "111938 + 940 + 21 + 1 = 112900",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "cbc9a46bf5e5296615f51c0ea564153968bc2a55",
        "1c9b2cb1a1628599e935ee61fd8c9b152d7bd3447969b065c920c8d13e3e5230",
        "60371d16b71c1e7d1fb0ccd83c5104984e4b740a",
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "BOTH_PRIMARY_INEQUALITIES_MET",
        "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
        "HYP-0005 — EUR/USD Fixed-UTC Intraday Activity Contrast Confirmatory Replication",
        "DEVELOPMENT_REVEALED_STRUCTURAL_PASS_CONFIRMATION_REQUIRED",
        "ATS2-RF-022 — HYP-0005 confirmatory hypothesis formation",
    )
    core.CONTENT_MARKERS[HYP0004_PROTOTYPE_TOOL] = (
        "HYP-0004 PROTO-01",
        "EXPECTED_DATASET_SHA256",
        "EXPECTED_ELIGIBLE = 111_938",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "abs_next_1h_return",
        "relative_spread",
        "bucket_metrics",
        "calendar_year_diagnostics",
        "movement_inequality_pass",
        "spread_inequality_pass",
        "both_primary_inequalities_pass",
        "BOTH_PRIMARY_INEQUALITIES_MET",
        "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED",
        "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
        "HYP0004_PROTO01_RESULT.json",
    )
    core.CONTENT_MARKERS[HYP0004_PROTOTYPE_TEST] = (
        "test_midpoint_spread_and_absolute_return_contract",
        "test_bucket_metrics_use_median_primary_statistics",
        "test_primary_decision_requires_both_inequalities",
        "test_primary_decision_parks_when_primary_bucket_is_empty",
        "test_calendar_year_diagnostics_are_reporting_only",
        "test_exact_next_hour_geometry_does_not_bridge_closed_or_missing_hours",
        "test_adjacent_exact_hour_rows_form_one_observation_per_start_boundary",
    )
    core.CONTENT_MARKERS[HYP0004_PROTOTYPE_RESULT] = (
        '"decision": "ADVANCE_TO_ECONOMIC_SCREEN"',
        '"decision_reason": "BOTH_PRIMARY_INEQUALITIES_MET"',
        '"evidence_class": "EXPLORATORY_PROTOTYPE"',
        '"measurement_label": "STRUCTURAL_H1_OPEN_PROXY_NO_TRADING_PNL"',
        '"next_action": "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4"',
        '"both_primary_inequalities_pass": true',
        '"movement_inequality_pass": true',
        '"spread_inequality_pass": true',
        '"median_abs_next_1h_return": 0.0006982268977376305',
        '"median_abs_next_1h_return": 0.0003493061509638462',
        '"median_relative_spread": 4.018781312113313e-05',
        '"median_relative_spread": 6.690913261869393e-05',
        '"git_commit": "60371d16b71c1e7d1fb0ccd83c5104984e4b740a"',
    )
    core.CONTENT_MARKERS[HYP0005_HYPOTHESIS] = (
        "Hypothesis ID: `HYP-0005`",
        "Parent Idea ID: `IDEA-0004`",
        "Development predecessor: `HYP-0004`",
        "Status: `READY_FOR_DATA_FEASIBILITY`",
        "`CORE_ACTIVE`: UTC hours `07` through `16` inclusive",
        "`TRANSITION`: UTC hours `17` through `20` inclusive",
        "`OFF_HOURS`: UTC hours `21`, `22`, `23`, and `00` through `06` inclusive",
        "median(abs_next_1h_return | CORE_ACTIVE) > median(abs_next_1h_return | OFF_HOURS)",
        "median(relative_spread | CORE_ACTIVE) <= median(relative_spread | OFF_HOURS)",
        "No minimum effect-size threshold is added after the HYP-0004 reveal.",
        "Confirmatory datasets inspected by RF-022: `0`",
        "Confirmatory outcomes inspected by RF-022: `0`",
        "If a genuinely unseen confirmatory block cannot be established",
        "ATS2-RF-023 — HYP-0005 confirmatory Data Feasibility preparation",
        "ATS2-RF-024 — HYP-0005 confirmatory Data Feasibility freeze",
        "Direct R4 entry remains blocked",
    )
    core.CONTENT_MARKERS[HYP0005_DATA_FEASIBILITY_PREP] = (
        "PREPARATION_PROTOCOL_FROZEN",
        "2003-05-04T21:00:00Z <= event_time < 2003-08-03T21:00:00Z",
        "2026-09-01T00:00:00Z <= event_time < 2026-09-26T00:00:00Z",
        "2003-08-03T21:00:00Z <= event_time < 2026-09-01T00:00:00Z",
        "DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001@1.0.0",
        "5 months × 2 sides = 10 objects",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "NO_CONFIRMATORY_OUTCOME_COMPUTED",
        "READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE",
        "INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY",
        "ATS2-RF-024 — HYP-0005 confirmatory Data Feasibility freeze",
    )
    core.CONTENT_MARKERS[HYP0005_DATA_FEASIBILITY_TOOL] = (
        'TASK_ID = "ATS2-RF-023"',
        'HYPOTHESIS_ID = "HYP-0005"',
        'DATASET_ID = "DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001"',
        "LEFT_UNSEEN",
        "RIGHT_UNSEEN",
        "H1_OPEN_PROXY_AT_EVENT_TIME",
        "NO_CONFIRMATORY_OUTCOME_COMPUTED",
        "outcome_metrics_computed",
        "primary_claim_evaluated",
        "READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE",
        "INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY",
        "HYP0005_DATA_FEASIBILITY_PREP.json",
    )
    core.CONTENT_MARKERS[HYP0005_DATA_FEASIBILITY_TEST] = (
        "test_frozen_segments_do_not_overlap_consumed_project_interval",
        "test_source_months_are_exactly_predeclared",
        "test_bucket_mapping_is_inherited_without_change",
        "test_geometry_counts_each_segment_without_bridging_gap",
        "test_preparation_decision_requires_both_segments_and_primary_buckets",
        "test_derived_csv_contains_no_hypothesis_outcome_columns",
    )
    core.CONTENT_MARKERS[STRATEGY_5_IDEA] = (
        "Idea ID: `IDEA-0005`",
        "Status: `SCREENING`",
        "RETAINED_RESEARCH_FACTORY_FAMILY",
        "S4-FAM-02 - Macroeconomic announcement response",
        "EVENT_CONDITIONAL_ABSOLUTE_RETURN_SHIFT",
        "FX_SPOT_OTC",
        "Instrument or universe: `EURUSD`",
        "Decision: `SCREEN`",
        "two new Material Research Attempts",
        "The frozen HYP-0005 unseen segments are unavailable",
        "research/hypotheses/HYP-0006.md",
    )
    core.CONTENT_MARKERS[HYP0006_HYPOTHESIS] = (
        "Hypothesis ID: `HYP-0006`",
        "Parent Idea ID: `IDEA-0005`",
        "Status: `READY_FOR_DATA_FEASIBILITY`",
        "scheduled U.S. Consumer Price Index",
        "pre_abs_60m_return",
        "post_abs_60m_return",
        "median(post_abs_60m_return) > median(pre_abs_60m_return)",
        "No quote timestamp at or after `t` may serve as `PRE_RELEASE_ANCHOR`",
        "PREVIOUS_60_MINUTES",
        "NEXT_60_MINUTES",
        "HYP-0005 frozen unseen segments used by HYP-0006 formation: `0`",
        "HYP-0006 market outcomes inspected before formation: `0`",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "ATS2-RF-026 — HYP-0006 Data Feasibility",
    )
    core.CONTENT_MARKERS[HYP0006_DATA_FEASIBILITY] = (
        "Task: `ATS2-RF-026`",
        "Hypothesis ID: `HYP-0006`",
        "Review status: `CONDITIONAL`",
        "U.S. Bureau of Labor Statistics",
        "Dukascopy historical EUR/USD tick data",
        "2003-08-03T21:00:00Z <= release_time < 2021-09-01T00:00:00Z",
        "DEVELOPMENT / EXPLORATORY ONLY",
        "FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION",
        "DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001@1.0.0",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "Prototype authorization:",
        "`NOT_YET_AUTHORIZED`",
        "ATS2-RF-027 — HYP-0006 Data Feasibility preparation",
    )
    core.CONTENT_MARKERS[HYP0006_DATA_FEASIBILITY_PREP] = (
        "Task: `ATS2-RF-027`",
        "PREPARATION_PROTOCOL_FROZEN_OFFLINE_BLS_SNAPSHOTS",
        "OWNER_INPUT_REQUIRED_BLS_SCHEDULE_SNAPSHOTS",
        "BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS",
        "BLS_ANNUAL_SCHEDULE_US_EASTERN",
        "Live BLS network access during normal RF-027 runtime is:",
        "`PROHIBITED`",
        "DUKASCOPY_HOURLY_TICK_BI5",
        "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF",
        "OWNER-authorized controlled Dukascopy preload",
        "1085",
        "AUTHORIZED_ONCE_BY_OWNER_2026_10_05",
        "SOURCE_BLOCKED_AUTHORIZATION_CONSUMED",
        "OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
        "OWNER_AUTHORIZED_BROWSER_PILOT_50_2026_10_05",
        "SKIPPED_AFTER_2_ATTEMPTS",
        "tools/hyp0006_dukascopy_browser_pilot.py",
        "OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05",
        "tools/hyp0006_dukascopy_browser_batch_250.py",
        "PASS_250_OF_250_AUTHORIZATION_CONSUMED",
        "OWNER_AUTHORIZED_REMAINING_748_2026_10_05",
        "tools/hyp0006_dukascopy_browser_remaining_748.py",
        "PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED",
        "0131dd82d286814adaa76ff6e2524e0d000ca13c",
        "a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4",
        "391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7",
        "6810",
        "CONFIRMED_ZERO_NETWORK_COMPLETE",
        "1085 / 1085",
        "ATS_TASK_CHECK.bat",
        "ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112",
        "2011-11-16T11:00:00Z",
        "no_valid_bi5_download_within_45s_attempt_2",
        "FULL_JSON_MANIFEST_REVIEW_PASS",
        "438bc59aa6f2cc81a762914f111017f75a2e46b2",
        "FULL_JSON_MANIFEST_REVIEW_PASS",
        "36e1301d551a69990ca707e7bf33da1ce07e5e88b1e7dc23a379a66b814e6b2c",
        "9aa6d7646c809f7a8fb2caaf421f13553ec30ba26dee5d8d991464e1e6cad2e1",
        "FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION",
        "READY_FOR_DATA_FEASIBILITY_FREEZE",
        "UNRESOLVED_OFFICIAL_EVENT_TIMES",
        "INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "ATS2-RF-028 — HYP-0006 pre-reveal data/tolerance freeze",
    )
    core.CONTENT_MARKERS[HYP0006_DATA_FEASIBILITY_TOOL] = (
        'TASK_ID = "ATS2-RF-027"',
        'HYPOTHESIS_ID = "HYP-0006"',
        "BLS_SNAPSHOT_MANIFEST",
        "BLS_CALENDAR_CSV",
        "OwnerInputRequiredError",
        "load_bls_snapshot_manifest",
        "load_bls_schedule_snapshots",
        "bls_snapshot_bundle_hash",
        "write_bls_calendar_csv",
        "live BLS network access is disabled",
        "cpi_schedule_candidates",
        'SOURCE_SYMBOL = "EURUSD"',
        "EXTERNAL_SOURCE_FAILURE_POLICY",
        "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF",
        "HYP0005_LEFT_START",
        "HYP0005_RIGHT_START",
        "required_tick_hours",
        "DUKASCOPY_NORMAL_RUNTIME_NETWORK_MODE",
        "require_local_dukascopy_snapshot",
        "load_local_tick_hour",
        "decode_tick_object",
        "event_geometry",
        "BLS_FROZEN_LOCAL_ANNUAL_SCHEDULE_SNAPSHOTS",
        "BLS_ANNUAL_SCHEDULE_US_EASTERN",
        "READY_FOR_DATA_FEASIBILITY_FREEZE",
        "UNRESOLVED_OFFICIAL_EVENT_TIMES",
        "INSUFFICIENT_GRANULAR_SOURCE_GEOMETRY",
        '"outcome_metrics_computed": False',
        '"primary_claim_evaluated": False',
        '"information_boundary": "NO_HYPOTHESIS_OUTCOME_COMPUTED"',
    )
    core.CONTENT_MARKERS[HYP0006_DATA_FEASIBILITY_TEST] = (
        "test_live_bls_network_access_is_prohibited",
        "test_external_source_failure_hands_off_after_first_attempt",
        "test_normal_rf027_dukascopy_runtime_is_offline_only",
        "test_snapshot_manifest_requires_exact_2003_2021_contract",
        "test_missing_snapshot_bundle_is_owner_input_not_hypothesis_failure",
        "test_legacy_schedule_text_parses_cpi_and_same_time_release",
        "test_et_conversion_uses_pre_and_post_2007_dst_rules",
        "test_schedule_candidates_preserve_frozen_development_interval",
        "test_bls_calendar_csv_contains_only_event_identity_and_provenance",
        "test_tick_source_url_uses_zero_based_month_and_hour_bucket",
        "test_decode_tick_object_validates_coherent_bid_ask",
        "test_required_tick_hours_are_bounded_and_exclude_hyp0005",
        "test_event_geometry_uses_timestamps_only_and_requires_strict_pre_release",
        "test_geometry_output_schema_contains_no_price_or_outcome_fields",
        "test_preparation_decision_is_non_market_geometry_gate",
    )
    core.CONTENT_MARKERS[HYP0006_CONTROLLED_DOWNLOAD_TOOL] = (
        'TASK_ID = "ATS2-RF-027"',
        'SUBSTAGE = "DUKASCOPY_CONTROLLED_PRELOAD"',
        'SOURCE_POLICY = "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF"',
        'CANONICAL_BASE = "https://datafeed.dukascopy.com/datafeed"',
        "AUTHORIZED_CALENDAR_SHA256",
        "AUTHORIZED_EVENT_COUNT = 217",
        "AUTHORIZED_REQUIRED_OBJECT_COUNT = 1085",
        "DRY_RUN_READY",
        "OWNER_AUTHORIZATION_REQUIRED",
        "OWNER_AUTHORIZATION_CONSUMED",
        "ACTIVE_AUTHORIZATION_MARKER",
        "canonical_authorization_is_active",
        "SOURCE_BLOCKED",
        "semantic_missing_count",
        '"outcome_metrics_computed": False',
        '"primary_claim_evaluated": False',
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    )
    core.CONTENT_MARKERS[HYP0006_CONTROLLED_DOWNLOAD_TEST] = (
        "test_inventory_uses_frozen_required_hours_and_canonical_base",
        "test_controlled_download_stops_after_first_external_failure",
        "test_controlled_download_does_not_overwrite_existing_file",
        "test_execute_requires_explicit_owner_authorization",
        "test_execute_rejects_consumed_canonical_authorization",
        "test_dry_run_never_starts_controlled_download",
    )
    core.CONTENT_MARKERS[HYP0006_BROWSER_PILOT_TOOL] = (
        'TASK_ID = "ATS2-RF-027"',
        'SUBSTAGE = "DUKASCOPY_BROWSER_PILOT_50"',
        'SOURCE_IDENTITY = "DUKASCOPY_HOURLY_TICK_BI5"',
        "PILOT_OBJECT_COUNT = 50",
        "MAX_ATTEMPTS_PER_OBJECT = 2",
        "OWNER_AUTHORIZED_BROWSER_PILOT_50_2026_10_05",
        "SKIPPED_AFTER_2_ATTEMPTS",
        "CONSUMED_SENTINEL",
        "canonical_authorization_is_active",
        "promote_valid_download",
        '"outcome_metrics_computed": False',
        '"primary_claim_evaluated": False',
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    )
    core.CONTENT_MARKERS[HYP0006_BROWSER_PILOT_TEST] = (
        "test_pilot_inventory_selects_first_50_missing",
        "test_run_pilot_retries_once_then_skips",
        "test_consumed_sentinel_blocks_before_browser",
        "test_promote_valid_download_preserves_bytes_and_validates",
    )
    core.CONTENT_MARKERS[HYP0006_BROWSER_BATCH_250_TOOL] = (
        'TASK_ID = "ATS2-RF-027"',
        'SUBSTAGE = "DUKASCOPY_BROWSER_BATCH_250"',
        'SOURCE_IDENTITY = "DUKASCOPY_HOURLY_TICK_BI5"',
        "BATCH_OBJECT_COUNT = 250",
        "MAX_ATTEMPTS_PER_OBJECT = 2",
        "OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05",
        "SKIPPED_AFTER_2_ATTEMPTS",
        "CONSUMED_SENTINEL",
        "canonical_authorization_is_active",
        "run_batch",
        '"outcome_metrics_computed": False',
        '"primary_claim_evaluated": False',
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    )
    core.CONTENT_MARKERS[HYP0006_BROWSER_BATCH_250_TEST] = (
        "test_batch_inventory_selects_first_250_missing",
        "test_run_batch_retries_once_then_skips",
        "test_consumed_sentinel_blocks_before_browser",
    )
    core.CONTENT_MARKERS[HYP0006_BROWSER_REMAINING_748_TOOL] = (
        'TASK_ID = "ATS2-RF-027"',
        'SUBSTAGE = "DUKASCOPY_BROWSER_REMAINING_748"',
        'SOURCE_IDENTITY = "DUKASCOPY_HOURLY_TICK_BI5"',
        "REMAINING_OBJECT_COUNT = 748",
        "MAX_ATTEMPTS_PER_OBJECT = 2",
        "OWNER_AUTHORIZED_REMAINING_748_2026_10_05",
        "inventory drift",
        "SKIPPED_AFTER_2_ATTEMPTS",
        "CONSUMED_SENTINEL",
        "canonical_authorization_is_active",
        "run_remaining",
        '"outcome_metrics_computed": False',
        '"primary_claim_evaluated": False',
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    )
    core.CONTENT_MARKERS[HYP0006_BROWSER_REMAINING_748_TEST] = (
        "test_remaining_inventory_selects_exact_748_missing",
        "test_remaining_inventory_blocks_on_count_drift",
        "test_run_remaining_retries_once_then_skips",
        "test_consumed_sentinel_blocks_before_browser",
    )
    core.CONTENT_MARKERS[HYP0006_BLS_SNAPSHOT_MANIFEST] = (
        "year,source_url,snapshot_relative_path",
        "2003,https://www.bls.gov/schedule/2003/home.htm",
        "2021,https://www.bls.gov/schedule/2021/home.htm",
        "data/raw/bls/hyp0006/schedules/2003.html",
        "data/raw/bls/hyp0006/schedules/2021.html",
    )
    core.CONTENT_MARKERS[HYP0006_BLS_SNAPSHOT_INTAKE] = (
        "HYP-0006 BLS Schedule Snapshot Intake",
        "one-time capture of official BLS annual release schedules",
        "data/raw/bls/hyp0006/schedules/YYYY.html",
        "OWNER_INPUT_REQUIRED_BLS_SCHEDULE_SNAPSHOTS",
        "Do this only when GPT explicitly says",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    )
    core.CONTENT_MARKERS[HYP0006_DUKASCOPY_SOURCE_RECOVERY] = (
        "SOURCE_BLOCKED_NO_OUTCOME",
        "f3151d8915b61d1a08e79cf27133764201475e65",
        "2004-03-17T13:00:00Z",
        "FROZEN_LOCAL_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
        "OWNER_INPUT_REQUIRED_DUKASCOPY_BI5_SNAPSHOT_BUNDLE",
        "DUKASCOPY_HOURLY_TICK_BI5",
        "OWNER_AUTHORIZED_BROWSER_PILOT_50_2026_10_05",
        "SKIPPED_AFTER_2_ATTEMPTS",
        "tools/hyp0006_dukascopy_browser_pilot.py",
        "PASS_50_OF_50_AUTHORIZATION_CONSUMED",
        "c7a10c8bcd84ca4754db92af4c63f39c02101543",
        "87",
        "998",
        "CONFIRMED_ZERO_NETWORK",
        "OWNER_AUTHORIZED_BROWSER_BATCH_250_2026_10_05",
        "tools/hyp0006_dukascopy_browser_batch_250.py",
        "PASS_250_OF_250_AUTHORIZATION_CONSUMED",
        "438bc59aa6f2cc81a762914f111017f75a2e46b2",
        "337",
        "748",
        "FULL_JSON_MANIFEST_REVIEW_PASS",
        "36e1301d551a69990ca707e7bf33da1ce07e5e88b1e7dc23a379a66b814e6b2c",
        "9aa6d7646c809f7a8fb2caaf421f13553ec30ba26dee5d8d991464e1e6cad2e1",
        "CONFIRMED_ZERO_NETWORK",
        "OWNER_AUTHORIZED_REMAINING_748_2026_10_05",
        "PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED",
        "0131dd82d286814adaa76ff6e2524e0d000ca13c",
        "a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4",
        "391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7",
        "6810",
        "CONFIRMED_ZERO_NETWORK_COMPLETE",
        "1085 / 1085",
        "ATS_TASK_CHECK.bat",
        "ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112",
        "2011-11-16T11:00:00Z",
        "no_valid_bi5_download_within_45s_attempt_2",
        "FULL_JSON_MANIFEST_REVIEW_PASS",
        "tools/hyp0006_dukascopy_browser_remaining_748.py",
        "REQUIRE_EXACTLY_748_CURRENT_MISSING",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    )
    core.CONTENT_MARKERS[HYP0006_DATA_TOLERANCE_FREEZE] = (
        "Task: `ATS2-RF-028`",
        "15/22",
        "bbbdbd301b610dfc61316c9ff82015fb0e039a47",
        "READY_FOR_DATA_FEASIBILITY_FREEZE",
        "DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001@1.0.0",
        "5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425",
        "e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034",
        "NEAREST_TO_T_MINUS_60M_WITHIN_30000MS_TIE_PREVIOUS",
        "LAST_QUOTE_STRICTLY_BEFORE_RELEASE_MAX_STALENESS_30000MS",
        "NEAREST_TO_T_PLUS_60M_WITHIN_30000MS_TIE_PREVIOUS",
        "LAST_RAW_RECORD_AT_SELECTED_MILLISECOND",
        "BID_AND_ASK_FROM_SAME_RAW_TICK_RECORD",
        "EXCLUDE_EVENT_IF_ANY_REQUIRED_ANCHOR_FAILS_FROZEN_GAP_RULE",
        "FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION",
        "FREEZE_DATA_AND_TOLERANCES",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    )
    core.CONTENT_MARKERS[HYP0006_DATA_TOLERANCE_FREEZE_TOOL] = (
        'TASK_ID = "ATS2-RF-028"',
        'RF027_COMMIT = "bbbdbd301b610dfc61316c9ff82015fb0e039a47"',
        "BOUNDARY_MAX_ABS_GAP_MS = 30_000",
        "PRE_RELEASE_MAX_STALENESS_MS = 30_000",
        'BOUNDARY_TIE_BREAK = "PREVIOUS_ON_EQUAL_GAP"',
        'DUPLICATE_TIMESTAMP_TIE_BREAK = "LAST_RAW_RECORD_AT_SELECTED_MILLISECOND"',
        'PRE_RELEASE_RULE = "LAST_QUOTE_STRICTLY_BEFORE_RELEASE"',
        'PRICE_PAIRING_RULE = "BID_AND_ASK_FROM_SAME_RAW_TICK_RECORD"',
        "FREEZE_DATA_AND_TOLERANCES",
        '"outcome_metrics_computed": False',
        '"primary_claim_evaluated": False',
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
    )
    core.CONTENT_MARKERS[HYP0006_DATA_TOLERANCE_FREEZE_TEST] = (
        "test_numeric_tolerances_are_frozen_before_reveal",
        "test_nearest_anchor_tie_break_prefers_previous",
        "test_geometry_at_frozen_limits_is_eligible",
        "test_geometry_above_any_frozen_limit_is_excluded",
        "test_incomplete_or_missing_source_geometry_is_excluded",
        "test_freeze_contract_contains_no_market_outcome_calculation",
    )
    core.CONTENT_MARKERS[HYP0003_PROTOTYPE_TOOL] = (
        "HYP-0003",
        "PROTO-01",
        "FORMATION_MONTHS = (1, 3, 6, 9, 12)",
        "HOLDING_MONTHS = (1, 3, 6, 9, 12)",
        "EXPECTED_DATASET_SHA256",
        "EXPECTED_SOURCE_BUNDLE_SHA256",
        "basket_size",
        "select_baskets",
        "winner_long_return",
        "loser_short_return",
        "cell_observations",
        "breadth_summary",
        "prototype_decision",
        "CREATE_NEW_CONFIRMATORY_HYPOTHESIS_BEFORE_R4",
        "HYP0003_PROTO01_RESULT.json",
    )
    core.CONTENT_MARKERS[HYP0003_PROTOTYPE_TEST] = (
        "test_basket_size_uses_frozen_one_sixth_ceiling",
        "test_basket_selection_uses_currency_code_tie_break",
        "test_executable_winner_and_loser_side_conventions",
        "test_observation_turnover_is_zero_for_same_baskets_and_one_for_replacement",
        "test_breadth_and_decision_contract",
        "CREATE_NEW_CONFIRMATORY_HYPOTHESIS_BEFORE_R4",
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
    core.CONTENT_MARKERS[M6_EXIT] = (
        "M6_REFERENCE_STRATEGY_2",
        "Decision:** `PASS`",
        "REJECTED_AT_R3",
        "WBS-6.0",
        "WBS-6.7",
        "Candidate count",
        "deep platform generalization beyond the Research Funnel remains untested",
        "M4.9 remains",
        "Strategy #3 sourcing",
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
        "reports/research/HYP-0003-PROTOTYPE-01-result.json -text",
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
        "ATS_AGENT_PREFLIGHT.bat",
        "AGENT_PREFLIGHT_REPORT.txt",
        "ATS_TASK_DIAG.bat",
        "CURRENT_TASK_DIAG_REPORT.txt",
        "agent/*",
        "uv run --frozen python tools/verify_repo.py",
        "ATS LOCAL CI: PASS",
        "LOCAL_CI_TROUBLESHOOTING.md",
        "AGENT_PRE_PUSH_CHECKLIST.md",
        ".githooks/pre-commit",
        ".githooks/pre-push",
        "GitHub Actions status is not a completion criterion",
        "Fast preflight before the completion check",
        "launcher exits with code `16`",
    )
    core.CONTENT_MARKERS[AGENT_PRE_PUSH_CHECKLIST] = (
        "Before any material remote repository write",
        "FORMAT_UNVERIFIED_UNTIL_PINNED_RUFF",
        "Exact Ruff diff is authoritative",
        "Validator marker audit",
        "Canonical state reconciliation",
        "last_completed_artifact",
        "next_artifact",
        "next_task_id",
        "First failing stage",
        "socket/`OSError`",
        "provider-native fallback",
        "agent/*",
        "ATS_AGENT_PREFLIGHT.bat",
        "BLOCKED_PENDING_OWNER_AGENT_PREFLIGHT",
        "ATS_TASK_DIAG.bat",
        "PENDING_OWNER_LAUNCHER",
        "do not declare completion without `ATS TASK LAUNCHER: PASS`",
    )
    core.CONTENT_MARKERS["AGENTS.md"] = (
        "AGENT_PRE_PUSH_CHECKLIST.md",
        "FORMAT_UNVERIFIED_UNTIL_PINNED_RUFF",
        "PENDING_OWNER_LAUNCHER",
        "agent/*",
        "ATS_AGENT_PREFLIGHT.bat",
        "ATS_TASK_DIAG.bat",
        "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF",
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
        "LCI-007",
        "probe_side_resilient",
        "CONTROL_REQUIRED",
        "REPEAT_AFTER_CONTROL_THRESHOLD",
        "ConnectionResetError",
        "LCI-011",
        "HistoryStart.bi5",
        "DATA_SOURCE_DISCOVERY_PROTOCOL",
        "history_start_60min",
        "7dec11ceb34c456a6c2f6b93833eeb02b2f0e804",
        "LCI-013",
        "DATA_SOURCE_COHERENCE",
        "Mixed source format inside one BID/ASK month-pair",
        "LCI-014",
        "DATA_OHLC_SIDE_SEMANTICS",
        "Separately aggregated BID/ASK OHLC extrema treated as synchronous quotes",
        "LCI-010",
        "IMPORT_CONTEXT",
        "current task checker import smoke",
        "LCI-015",
        "DATA_JETTA_QUANTIZATION",
        "ATS imposed a Jetta OHLC geometry threshold not required by provider semantics",
        "577910",
        "provider-native compact-candle semantics",
        "ATS_AGENT_PREFLIGHT.bat",
        "ATS_TASK_DIAG.bat",
    )
    core.CONTENT_MARKERS[LOCAL_CI_FAILURE_REGISTRY] = (
        "Escalation policy",
        "LCI-002",
        "Confirmed occurrences",
        "REPEAT_AFTER_CONTROL_THRESHOLD",
        "fast Local CI preflight",
        "9fb041c51cf93071ca6735b52897cbb2b24e5568",
        "9134c44d1d3d861124c44e00b4df820ad181cb5d",
        "f989e6d77c94aaaa93df9bf6fdd994708b570404",
        "4d4f5546c54bc1b8985f37dd63c251b87517245e",
        "6d452c4f340825eaa39b8e28dad3f6691332b217",
        "3a0dc9af4cc2191cc98c65b190b6f1f1c5cb1ea3",
        "124 passed",
        "Reusable resolution rule",
        "Rule-conversion discipline",
        "LCI-007",
        "CONTROL_REQUIRED",
        "REPEAT_AFTER_CONTROL_THRESHOLD",
        "b82e827c0c8510a38aac3179411b3b2a8d455310",
        "0988069a525a7cd0d8acb48a3d9ed34d3ceb0332",
        "LCI-011",
        "338ad44867d9ae68e11eb613a96b92101a5ac853",
        "DATA_SOURCE_DISCOVERY_PROTOCOL",
        "7dec11ceb34c456a6c2f6b93833eeb02b2f0e804",
        "LCI-013",
        "DATA_SOURCE_COHERENCE",
        "d2fd7d83b40aa60a65b1b9f9d59461523ecd27ec",
        "LCI-010",
        "IMPORT_CONTEXT",
        "927eb6349142bb9cea0007e5290a421fe3c0fc7a",
        "LCI-014",
        "DATA_OHLC_SIDE_SEMANTICS",
        "4135fc4d7bbbc9522ff09e7447c887b1a0c5ae02",
        "LCI-015",
        "DATA_JETTA_QUANTIZATION",
        "816d333e0d19447103fe782ab4e6ef2f39f55c8c",
        "e6f232fc68d700a39fecd1a76d66dbbc3c228878",
        "558b9790ce54adeefaed16541bf9256ff8b086ca",
        "ATS_AGENT_PREFLIGHT.bat",
        "agent/*",
    )
    core.CONTENT_MARKERS["ATS_TASK_CHECK.bat"] = (
        "git pull --ff-only",
        "tools/run_and_tee.py",
        "Progress:",
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
    core.CONTENT_MARKERS["ATS_AGENT_PREFLIGHT.bat"] = (
        "git fetch origin main",
        "uv sync --frozen",
        "tools/run_and_tee.py",
        "tools/agent_preflight.py",
        "AGENT_PREFLIGHT_REPORT.txt",
        "ATS AGENT PREFLIGHT: PASS",
        "ATS AGENT PREFLIGHT: FAIL",
    )
    core.CONTENT_MARKERS["ATS_TASK_DIAG.bat"] = (
        "uv sync --frozen",
        "tools/run_and_tee.py",
        "tools/current_task_diag.py",
        "CURRENT_TASK_DIAG_REPORT.txt",
        "ATS TASK DIAGNOSTIC: COMPLETE",
        "ATS TASK DIAGNOSTIC: FAIL",
    )
    core.CONTENT_MARKERS["tools/agent_preflight.py"] = (
        'AGENT_BRANCH_PREFIX = "agent/"',
        "current task checker import smoke",
        "run_current_task_import_smoke",
        "origin/main",
        "full ATS Local CI on agent branch",
        "tools/verify_repo.py",
        "agent branch has no changes relative to main",
    )
    core.CONTENT_MARKERS["tools/current_task_diag.py"] = (
        "ATS2-RF-023 — HYP-0005 confirmatory Data Feasibility preparation",
        "distinguish current-month source availability from general provider failure",
        "JETTA_CURRENT_2026_09",
        "JETTA_CONTROL_2026_08",
        "BI5_CURRENT_2026_09",
        "BI5_CONTROL_2026_08",
        "BI5_ALT_CURRENT_2026_09",
        "BI5_ALT_CONTROL_2026_08",
        "NO_CONFIRMATORY_OUTCOME_COMPUTED",
        "Hypothesis outcome fields requested: 0",
        "ATS TASK DIAGNOSTIC: COMPLETE",
    )
    core.CONTENT_MARKERS["tools/current_task_check.py"] = (
        'TASK_ID = "ATS2-RF-027"',
        'TASK_NAME = "HYP-0006 Data Feasibility preparation"',
        "HYP0006_DATA_FEASIBILITY_PREP.json",
        "HYP-0006-DEV-01-EURUSD-CPI-EVENTS.csv",
        "FROZEN_BLOBS",
        "ALLOWED_DECISIONS",
        "RF-027 frozen HYP-0005/HYP-0006 lineage",
        "RF-027 frozen preparation contract",
        "RF-027 machine preparation result",
        "RF-027 HYP-0006 official-event and tick geometry preparation",
        "full ATS Local CI before RF-027 source preparation",
        "HYP-0005 outcome computed by RF-027: NO",
        "HYP-0006 outcome computed by RF-027: NO",
        "NO_HYPOTHESIS_OUTCOME_COMPUTED",
        "hyp0006_dukascopy_controlled_download.py",
        "ATS CURRENT TASK CHECK:",
    )
    core.CONTENT_MARKERS["tools/run_and_tee.py"] = (
        "PYTHONUNBUFFERED",
        "PROGRESS_PREFIX",
        "render_progress",
        "subprocess.Popen",
        "stderr=subprocess.STDOUT",
        "report.flush",
        "process.wait",
    )
    core.CONTENT_MARKERS["tools/verify_repo.py"] = (
        "ATS Local CI Gate", "repository validator", "ruff lint", "ruff format",
        "pytest collection", "pytest", "environment fingerprint",
        "ATS LOCAL CI:", "LATEST.json",
        "tools/agent_preflight.py", "tools/current_task_diag.py",
        "tools/hyp0003_proto01.py", "tools/hyp0004_development_data.py",
        "tools/hyp0004_proto01.py",
        "tools/hyp0005_data_feasibility.py",
        "tools/hyp0006_data_feasibility.py",
        "tools/hyp0006_dukascopy_controlled_download.py",
        "tools/hyp0006_dukascopy_browser_remaining_748.py",
    )
    core.CONTENT_MARKERS["governance/methodology/DATA_FEASIBILITY_REVIEW.md"] = (
        "Data Feasibility Review",
        "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF",
        "After the first proven HTTP/network/access failure",
        "explicit OWNER authorization",
    )
    core.CONTENT_MARKERS[PROJECT_GPT_SYSTEM_INSTRUCTION] = (
        "ATS Project GPT — системная инструкция",
        "Source of truth",
        "ПЛАН HYP-xxxx",
        "ПЕРЕСМОТР ПЛАНА HYP-xxxx",
        "техническая ошибка, диагностика, форматирование, retry",
        "Source blockers",
        "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF",
        "OWNER input discipline",
        "GitHub workflow",
        "RUFF_LINT_UNVERIFIED_UNTIL_PINNED_RUFF",
        "Task закрывается только после exact-main PASS",
    )
    core.CONTENT_MARKERS["reports/local_ci/README.md"] = (
        "ATS_TASK_CHECK.bat",
        "CURRENT_TASK_REPORT.txt",
        "ATS_AGENT_PREFLIGHT.bat",
        "AGENT_PREFLIGHT_REPORT.txt",
        "ATS_TASK_DIAG.bat",
        "CURRENT_TASK_DIAG_REPORT.txt",
        "LATEST.json",
        "LOCAL_CI_GATE.md",
        "LOCAL_CI_TROUBLESHOOTING.md",
        "HYP0003_PROTO01_RESULT.json",
        "HYP0003_PROTO01_RESULT_REPORT.txt",
        "HYP0004_DEVELOPMENT_DATA.json",
        "HYP0004_DEVELOPMENT_DATA_REPORT.txt",
        "HYP0004_PROTO01_RESULT.json",
        "HYP0004_PROTO01_RESULT_REPORT.txt",
        "HYP0005_DATA_FEASIBILITY_PREP.json",
        "HYP0005_DATA_FEASIBILITY_PREP_REPORT.txt",
        "HYP0006_DATA_FEASIBILITY_PREP.json",
        "HYP0006_DATA_FEASIBILITY_PREP_REPORT.txt",
        "HYP0006_DUKASCOPY_CONTROLLED_DOWNLOAD.json",
        "HYP0006_DUKASCOPY_CONTROLLED_DOWNLOAD_REPORT.txt",
        "HYP0006_DUKASCOPY_CONTROLLED_DOWNLOAD_INVENTORY.csv",
        "HYP0006_DUKASCOPY_BROWSER_PILOT_50.json",
        "HYP0006_DUKASCOPY_BROWSER_PILOT_50_REPORT.txt",
        "HYP0006_DUKASCOPY_BROWSER_PILOT_50_MANIFEST.csv",
        "HYP0006_DUKASCOPY_BROWSER_PILOT_50_CONSUMED.json",
        "HYP0006_DUKASCOPY_BROWSER_BATCH_250.json",
        "HYP0006_DUKASCOPY_BROWSER_BATCH_250_REPORT.txt",
        "HYP0006_DUKASCOPY_BROWSER_BATCH_250_MANIFEST.csv",
        "HYP0006_DUKASCOPY_BROWSER_BATCH_250_CONSUMED.json",
        "HYP0006_DUKASCOPY_BROWSER_REMAINING_748.json",
        "HYP0006_DUKASCOPY_BROWSER_REMAINING_748_REPORT.txt",
        "HYP0006_DUKASCOPY_BROWSER_REMAINING_748_MANIFEST.csv",
        "HYP0006_DUKASCOPY_BROWSER_REMAINING_748_CONSUMED.json",
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
        "reports/local_ci/AGENT_PREFLIGHT_REPORT.txt",
        "reports/local_ci/CURRENT_TASK_DIAG_REPORT.txt",
        "reports/local_ci/HYP0002_DATA_FEASIBILITY.json",
        "reports/local_ci/HYP0002_DATA_FEASIBILITY_REPORT.txt",
        "reports/local_ci/HYP0002_PROTO01_RESULT.json",
        "reports/local_ci/HYP0002_PROTO01_RESULT_REPORT.txt",
        "reports/local_ci/HYP0003_DATA_FEASIBILITY.json",
        "reports/local_ci/HYP0003_DATA_FEASIBILITY_REPORT.txt",
        "reports/local_ci/HYP0003_DEVELOPMENT_DATA.json",
        "reports/local_ci/HYP0003_DEVELOPMENT_DATA_REPORT.txt",
        "reports/local_ci/HYP0003_PROTO01_RESULT.json",
        "reports/local_ci/HYP0003_PROTO01_RESULT_REPORT.txt",
        "reports/local_ci/HYP0004_DEVELOPMENT_DATA.json",
        "reports/local_ci/HYP0004_DEVELOPMENT_DATA_REPORT.txt",
        "reports/local_ci/HYP0004_PROTO01_RESULT.json",
        "reports/local_ci/HYP0004_PROTO01_RESULT_REPORT.txt",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_PILOT_50.json",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_PILOT_50_REPORT.txt",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_PILOT_50_MANIFEST.csv",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_PILOT_50_CONSUMED.json",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_BATCH_250.json",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_BATCH_250_REPORT.txt",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_BATCH_250_MANIFEST.csv",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_BATCH_250_CONSUMED.json",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_REMAINING_748.json",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_REMAINING_748_REPORT.txt",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_REMAINING_748_MANIFEST.csv",
        "reports/local_ci/HYP0006_DUKASCOPY_BROWSER_REMAINING_748_CONSUMED.json",
        "data/derived/HYP-0003-DEV-01-G10EXUSD-H1.csv*",
        "data/derived/HYP-0004-DEV-01-EURUSD-H1.csv*",
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
        "tools/run_and_tee.py",
        "tools/agent_preflight.py",
        "tools/current_task_diag.py",
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
        "src/ats/discovery/__init__.py",
        "src/ats/discovery/bounded.py",
        "src/ats/discovery/eurusd_h1.py",
        "tools/discover_eurusd_h1.py",
        "tools/hyp0002_data_feasibility.py",
        "tools/hyp0002_proto01.py",
        "tools/hyp0003_data_feasibility.py",
        "tools/hyp0003_development_data.py",
        "tools/hyp0003_proto01.py",
        "tools/hyp0004_development_data.py",
        "tools/hyp0004_proto01.py",
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
        "tests/test_discovery_bounded.py",
        "tests/test_discovery_eurusd_h1.py",
        "tests/test_hyp0002_proto01.py",
        "tests/test_hyp0003_data_feasibility.py",
        "tests/test_hyp0003_development_data.py",
        "tests/test_hyp0003_proto01.py",
        "tests/test_hyp0004_development_data.py",
        "tests/test_hyp0004_proto01.py",
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
        'schema_version: "2.0"', "phase: RESEARCH_FACTORY_CONTINUOUS",
        "M0_PROGRAM_REBASELINE: COMPLETED", "M1_RESEARCH_METHODOLOGY: COMPLETED",
        "M2_RESEARCH_PLATFORM_MVP: COMPLETED", "M3_REFERENCE_STRATEGY_1: COMPLETED",
        "M4_VALIDATION_FRAMEWORK: IN_PROGRESS", "M6_REFERENCE_STRATEGY_2: COMPLETED",
        "exit_decision: PASS",
        'm1_exit_review: "governance/program/M1_EXIT_REVIEW.md"',
        'm2_exit_review: "governance/program/M2_EXIT_REVIEW.md"',
        'm3_exit_review: "governance/program/M3_EXIT_REVIEW.md"',
        'm6_exit_review: "governance/program/M6_EXIT_REVIEW.md"',
        'validation_framework: "governance/methodology/VALIDATION_FRAMEWORK.md"',
        'market_pattern_discovery: "governance/methodology/MARKET_PATTERN_DISCOVERY.md"',
        'independent_exam_protocol: "governance/methodology/INDEPENDENT_EXAM_PROTOCOL.md"',
        'multiple_research_accounting: "governance/methodology/MULTIPLE_RESEARCH_ACCOUNTING.md"',
        'technical_strategy_validation_profile: "governance/methodology/TECHNICAL_STRATEGY_VALIDATION_PROFILE.md"',
        'discovery_search_manifest_template: "governance/methodology/templates/discovery/SEARCH_MANIFEST_TEMPLATE.yaml"',
        'bounded_discovery_engine: "src/ats/discovery/bounded.py"',
        'first_discovery_search_manifest: "research/discovery/SEARCH-EURUSD-H1-2021-2025-001.yaml"',
        'first_discovery_runner: "tools/discover_eurusd_h1.py"',
        'first_discovery_result_summary: "reports/research/SEARCH-EURUSD-H1-2021-2025-001-summary.md"',
        'reference_strategy_2_selection: "governance/program/REFERENCE_STRATEGY_2_SELECTION.md"',
        'reference_strategy_2_idea: "research/ideas/IDEA-0002.md"',
        'reference_strategy_2_hypothesis: "research/hypotheses/HYP-0002.md"',
        'reference_strategy_2_data_feasibility_prep: "research/reviews/HYP-0002-DATA-FEASIBILITY-PREP.md"',
        'reference_strategy_2_data_feasibility: "research/reviews/HYP-0002-DATA-FEASIBILITY.md"',
        'reference_strategy_2_confirmatory_manifest: "data/manifests/DATA-DUKASCOPY-EURUSDH1-HYP0002-001.yaml"',
        'reference_strategy_2_confirmatory_schema: "data/manifests/DATA-EURUSD-DUKASCOPY-H1-HYP0002.schema.json"',
        'reference_strategy_2_prototype: "research/reviews/HYP-0002-PROTOTYPE-01.md"',
        'reference_strategy_2_prototype_runner: "tools/hyp0002_proto01.py"',
        'reference_strategy_2_prototype_result: "reports/research/HYP-0002-PROTOTYPE-01-result.json"',
        'reference_strategy_2_closeout: "governance/program/REFERENCE_STRATEGY_2_CLOSEOUT.md"',
        'strategy_3_sourcing_rebaseline: "governance/program/STRATEGY_3_SOURCING_REBASELINE.md"',
        'strategy_3_idea_sourcing: "governance/program/STRATEGY_3_IDEA_SOURCING.md"',
        'strategy_3_family_selection: "governance/program/STRATEGY_3_FAMILY_SELECTION.md"',
        'strategy_3_idea: "research/ideas/IDEA-0003.md"',
        'strategy_3_hypothesis: "research/hypotheses/HYP-0003.md"',
        'strategy_3_data_feasibility: "research/reviews/HYP-0003-DATA-FEASIBILITY.md"',
        'strategy_3_data_feasibility_prep: "research/reviews/HYP-0003-DATA-FEASIBILITY-PREP.md"',
        'strategy_3_data_feasibility_prep_result: "reports/research/HYP-0003-DATA-FEASIBILITY-PREP-result.json"',
        'strategy_3_data_feasibility_tool: "tools/hyp0003_data_feasibility.py"',
        'strategy_3_development_data_prep: "research/reviews/HYP-0003-DEVELOPMENT-DATA-PREP.md"',
        'strategy_3_development_data_tool: "tools/hyp0003_development_data.py"',
        'strategy_3_development_data_prep_result: "reports/research/HYP-0003-DEVELOPMENT-DATA-PREP-result.json"',
        'strategy_3_development_dataset_manifest: "data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001.yaml"',
        'strategy_3_development_dataset_schema: "data/manifests/DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV.schema.json"',
        'strategy_3_prototype: "research/reviews/HYP-0003-PROTOTYPE-01.md"',
        'strategy_3_prototype_runner: "tools/hyp0003_proto01.py"',
        'strategy_3_prototype_test: "tests/test_hyp0003_proto01.py"',
        'strategy_3_prototype_result: "reports/research/HYP-0003-PROTOTYPE-01-result.json"',
        'strategy_3_closeout: "governance/program/STRATEGY_3_CLOSEOUT.md"',
        'strategy_4_idea_sourcing: "governance/program/STRATEGY_4_IDEA_SOURCING.md"',
        'strategy_4_family_selection: "governance/program/STRATEGY_4_FAMILY_SELECTION.md"',
        'strategy_4_idea: "research/ideas/IDEA-0004.md"',
        'strategy_4_hypothesis: "research/hypotheses/HYP-0004.md"',
        'strategy_4_data_feasibility: "research/reviews/HYP-0004-DATA-FEASIBILITY.md"',
        'strategy_4_development_data_prep: "research/reviews/HYP-0004-DEVELOPMENT-DATA-PREP.md"',
        'strategy_4_development_data_tool: "tools/hyp0004_development_data.py"',
        'strategy_4_development_data_test: "tests/test_hyp0004_development_data.py"',
        'strategy_4_development_data_prep_result: "reports/research/HYP-0004-DEVELOPMENT-DATA-PREP-result.json"',
        'strategy_4_development_dataset_manifest: "data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001.yaml"',
        'strategy_4_development_dataset_schema: "data/manifests/DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV.schema.json"',
        'strategy_4_prototype: "research/reviews/HYP-0004-PROTOTYPE-01.md"',
        'strategy_4_prototype_runner: "tools/hyp0004_proto01.py"',
        'strategy_4_prototype_test: "tests/test_hyp0004_proto01.py"',
        'strategy_4_prototype_result: "reports/research/HYP-0004-PROTOTYPE-01-result.json"',
        'strategy_4_confirmatory_hypothesis: "research/hypotheses/HYP-0005.md"',
        'strategy_4_confirmatory_data_feasibility_prep: "research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md"',
        'strategy_4_confirmatory_data_feasibility_tool: "tools/hyp0005_data_feasibility.py"',
        'strategy_4_confirmatory_data_feasibility_test: "tests/test_hyp0005_data_feasibility.py"',
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
        'last_completed_task_id: "ATS2-RF-027"',
        'current_task: "ATS2-RF-028"', 'current_ready_task: "ATS2-RF-028"',
        'next_task: "UNASSIGNED_UNTIL_RF028_PASS"',
        'current_wbs: "WBS-RF.2"',
        'current_strategy_sequence: 5',
        'rf006_verified_commit: "acf197d5774116c7d9a8b742eab77c6ee3447214"',
        'preparation_decision: "READY_FOR_FREEZE_REVIEW"',
        'source_qualified_currency_count: 9',
        'common_possible_development_start: "2003-08-03T21:00:00Z"',
        'probe_bundle_sha256: "a88add123fd42e83396ba17de13cf65fedf18d8e0a5e1eca476ed6338c91b45e"',
        'development_dataset_id: "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001"',
        'rf007_verified_commit: "21942dccc1985bfc422579c185e9836610627b8b"',
        'development_data_acquisition_contract_status: "FROZEN_RF007"',
        'development_data_preparation_status: "RF008_OWNER_PASS_READY_FOR_FREEZE"',
        'rf008_verified_commit: "63e1bc9c7e1ba2e001ecdd9918244d83db0e58c3"',
        'development_data_freeze_status: "FROZEN_RF009"',
        'rf009_verified_commit: "74057ebcb6d43fbb66a275c74fbd2081b148f9a2"',
        'development_source_objects_acquired: 3906',
        'development_source_objects_missing: 0',
        'development_source_bundle_sha256: "9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a"',
        'development_prepared_rows: 1014509',
        'development_prepared_csv_sha256: "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2"',
        'development_eligible_monthly_points_ge6: 207',
        'development_eligible_longest_12_12_geometry_points: 184',
        'protected_tail_source_objects_requested: 0',
        'prototype_id: "PROTO-01"',
        'prototype_freeze_status: "FROZEN_RF010"',
        'rf010_verified_commit: "dbb93b2510334561c7c38aa14b859aa42a420bbc"',
        'prototype_runner_git_blob: "d65746f39476ba3fee8cf59acfd0b2f82af9c663"',
        'prototype_result_status: "REVEALED_REJECTED"',
        'prototype_outcome: "REJECT"',
        'prototype_result_sha256: "a1feee3d6495afdcc46f81ce0ee8e137896a77a3bd52de8baf6cbf53da1a7620"',
        'prototype_reveal_commit: "f974b9bb60a6cc295cb8aaba4a263499c14769c0"',
        'research_line_status: "REJECTED_AT_R3"',
        'strategy_4_sourcing_status: "RF013_SHORTLIST_COMPLETE"',
        'strategy_4_families_reviewed: 5',
        'strategy_4_families_shortlisted: 4',
        'rf013_verified_commit: "d8ba5544111ff05fc48c59939acccb337b220e99"',
        'rf014_verified_commit: "b1392ad843c57bf0ca4c2d0575f4095957b80e82"',
        'rf015_verified_commit: "79d83a5fb900e00f510c4348cc6dcb8a5489c5c0"',
        'rf016_verified_commit: "3628010fc04045de040794c482e57ccd2639f99b"',
        'rf017_verified_commit: "ae9767a71b3860e55d345afb34b2f9c18b5dd063"',
        'rf018_verified_commit: "6d388c500d2c5e1671e11700966b713b95a395b8"',
        'rf019_verified_commit: "95174c2922fd5882c995ff14b3031d690ecc80bf"',
        'rf020_verified_commit: "60371d16b71c1e7d1fb0ccd83c5104984e4b740a"',
        'rf021_verified_commit: "79cb1d36bd544cc14db49ea5f6e85ef138a579eb"',
        'rf022_verified_commit: "136b62b52922abc1556396377c6cd6fca88fba75"',
        'strategy_4_selected_family: "S4-FAM-03"',
        'strategy_4_selected_family_class: "INTRADAY_TIME_SESSION_EFFECT"',
        'strategy_4_idea_id: "IDEA-0004"',
        'strategy_4_idea_status: "SCREENING"',
        'strategy_4_hypothesis_id: "HYP-0004"',
        'strategy_4_hypothesis_status: "DEVELOPMENT_PASS_CONFIRMATION_REQUIRED"',
        'strategy_4_hypothesis_instrument: "EURUSD"',
        'strategy_4_data_feasibility_decision: "CONDITIONAL"',
        'strategy_4_data_feasibility_status: "CONDITIONAL"',
        'strategy_4_parent_dataset_id: "DATA-DUKASCOPY-G10EXUSD-H1-HYP0003-DEV-001"',
        'strategy_4_parent_dataset_sha256: "8933379ed936367fca55e3f5db4d50a3da9f4fbaeca58b28906cdafa90e35dd2"',
        'strategy_4_parent_source_bundle_sha256: "9fa05651dd6253d843685460d0c549284432f51573568ecf206939e789fccc5a"',
        'strategy_4_planned_development_dataset_id: "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001"',
        'strategy_4_development_data_preparation_status: "RF017_OWNER_PASS_READY_FOR_FREEZE"',
        'strategy_4_development_data_freeze_status: "FROZEN_RF018"',
        'strategy_4_development_dataset_id: "DATA-DUKASCOPY-EURUSD-H1-HYP0004-DEV-001"',
        'strategy_4_development_dataset_version: "1.0.0"',
        'strategy_4_development_prepared_rows: 112900',
        'strategy_4_development_csv_sha256: "3a3a9b5ba99cc504c5bcb66536886113b2f6659a66718a0f122e9982fbc8a9d6"',
        'strategy_4_development_first_event_time: "2003-08-03T21:00:00Z"',
        'strategy_4_development_last_event_time: "2021-08-31T23:00:00Z"',
        'strategy_4_development_eligible_exact_next_hour_count: 111938',
        'strategy_4_development_eligible_core_active_count: 47012',
        'strategy_4_development_eligible_transition_count: 18189',
        'strategy_4_development_eligible_off_hours_count: 46737',
        'strategy_4_development_ineligible_closed_market_next_hour_count: 940',
        'strategy_4_development_ineligible_missing_expected_next_hour_count: 21',
        'strategy_4_development_ineligible_dataset_end_count: 1',
        'strategy_4_boundary_availability_mode: "H1_OPEN_PROXY_AT_EVENT_TIME"',
        'strategy_4_exact_tick_boundary_time_known: false',
        'strategy_4_prototype_id: "PROTO-01"',
        'strategy_4_prototype_freeze_status: "FROZEN_RF019"',
        'strategy_4_prototype_runner_git_blob: "cbc9a46bf5e5296615f51c0ea564153968bc2a55"',
        'strategy_4_prototype_result_status: "REVEALED_ADVANCE_CONFIRMATION_REQUIRED"',
        'strategy_4_prototype_outcome: "ADVANCE_TO_ECONOMIC_SCREEN"',
        'strategy_4_prototype_decision_reason: "BOTH_PRIMARY_INEQUALITIES_MET"',
        'strategy_4_prototype_result_sha256: "1c9b2cb1a1628599e935ee61fd8c9b152d7bd3447969b065c920c8d13e3e5230"',
        'strategy_4_prototype_reveal_commit: "60371d16b71c1e7d1fb0ccd83c5104984e4b740a"',
        'strategy_4_route_selected: "CONFIRMATORY_STRUCTURAL_HYPOTHESIS"',
        'strategy_4_next_hypothesis_id: "HYP-0005"',
        'strategy_4_next_hypothesis_role: "CONFIRMATORY_STRUCTURAL_REPLICATION"',
        'strategy_4_confirmatory_hypothesis_id: "HYP-0005"',
        'strategy_4_confirmatory_hypothesis_status: "READY_FOR_DATA_FEASIBILITY"',
        'strategy_4_confirmatory_parent_idea_id: "IDEA-0004"',
        'strategy_4_confirmatory_development_predecessor: "HYP-0004"',
        'strategy_4_confirmatory_dataset_selected: false',
        'strategy_4_confirmatory_dataset_candidate_id: "DATA-DUKASCOPY-EURUSD-H1-HYP0005-CONF-001"',
        'strategy_4_confirmatory_dataset_candidate_version: "1.0.0"',
        'strategy_4_confirmatory_prep_status: "RF023_PROTOCOL_FROZEN_PENDING_OWNER_PREPARATION"',
        'strategy_4_confirmatory_left_segment_start: "2003-05-04T21:00:00Z"',
        'strategy_4_confirmatory_left_segment_end_exclusive: "2003-08-03T21:00:00Z"',
        'strategy_4_confirmatory_right_segment_start: "2026-09-01T00:00:00Z"',
        'strategy_4_confirmatory_right_segment_end_exclusive: "2026-09-26T00:00:00Z"',
        'strategy_4_confirmatory_consumed_interval_start: "2003-08-03T21:00:00Z"',
        'strategy_4_confirmatory_consumed_interval_end_exclusive: "2026-09-01T00:00:00Z"',
        'strategy_4_confirmatory_outcome_computed: false',
        'strategy_4_direct_r4_allowed: false',
        'strategy_4_research_line_status: "DEVELOPMENT_PASS_CONFIRMATORY_HYPOTHESIS_FORMED"',
        'strategy_4_information_boundary: "NO_CONFIRMATORY_OUTCOME_COMPUTED"',
        'strategy_5_source_family: "S4-FAM-02"',
        'strategy_5_family_class: "MACROECONOMIC_ANNOUNCEMENT_RESPONSE"',
        'strategy_5_lineage_type: "NEW_IDEA_FROM_RETAINED_RESEARCH_FAMILY"',
        'strategy_5_idea_id: "IDEA-0005"',
        'strategy_5_idea_status: "SCREENING"',
        'strategy_5_hypothesis_id: "HYP-0006"',
        'strategy_5_hypothesis_status: "READY_FOR_DATA_FEASIBILITY"',
        'strategy_5_hypothesis_instrument: "EURUSD"',
        'strategy_5_event_class: "SCHEDULED_US_CPI_RELEASE"',
        'strategy_5_primary_horizon: "PRE_60M_VS_POST_60M"',
        'strategy_5_material_research_attempts_registered: 2',
        'strategy_5_hyp0005_protected_segments_consumed: false',
        'strategy_5_outcome_computed: false',
        'strategy_5_information_boundary: "NO_HYPOTHESIS_OUTCOME_COMPUTED"',
        'strategy_5_research_line_status: "HYPOTHESIS_FORMED_DATA_FEASIBILITY_CONDITIONAL"',
        'rf025_verified_commit: "9b0a6c8898a7ebf9b03167a871ad02af96ca2807"',
        'strategy_5_data_feasibility_decision: "CONDITIONAL"',
        'strategy_5_data_feasibility_status: "CONDITIONAL"',
        'strategy_5_development_start: "2003-08-03T21:00:00Z"',
        'strategy_5_development_end_exclusive: "2021-09-01T00:00:00Z"',
        'strategy_5_event_source_candidate: "BLS_OFFICIAL_CPI_RELEASE_SCHEDULE_AND_ARCHIVE"',
        'strategy_5_quote_source_candidate: "DUKASCOPY_EURUSD_TICK"',
        'strategy_5_same_time_cluster_policy: "FLAG_ONLY_NO_PERFORMANCE_BASED_EXCLUSION"',
        'strategy_5_prototype_authorized: false',
        'rf026_verified_commit: "5e0ff9e4481e5dc28c14a73adcf32433715973a3"',
        'strategy_5_data_feasibility_prep_status: "RF027_EXACT_MAIN_PASS"',
        'strategy_5_data_feasibility_prep_decision: "READY_FOR_DATA_FEASIBILITY_FREEZE"',
        'rf027_failed_exact_main_commit: "a4c6331949e9c71fc68eb1baa870d20a03518d48"',
        'rf027_second_failed_exact_main_commit: "2ce019bb51b0e45e900c0555ed44be5a3433e23a"',
        'strategy_5_source_access_blocker: "DUKASCOPY_HTTP_503_2004_03_17T13_00_00Z"',
        'strategy_5_source_access_correction: "FROZEN_LOCAL_DUKASCOPY_BI5_SNAPSHOT_ARCHITECTURE_REQUIRED"',
        'strategy_5_required_protected_hyp0005_source_requests: 0',
        'strategy_5_bls_runtime_network_mode: "PROHIBITED"',
        'strategy_5_bls_snapshot_years: "2003..2021"',
        'strategy_5_bls_snapshot_canonical_count: 19',
        'rf027_offline_architecture_merged_commit: "79a01623c3fef4deb3757e4d2940b8cd16b9bff3"',
        'rf027_latest_exact_main_blocker: "DUKASCOPY_HTTP_503_2004_03_17T13_00_00Z"',
        'strategy_5_bls_snapshot_intake_status: "CANONICAL_19_READY_LOCAL"',
        'strategy_5_bls_calendar_observed_event_count: 217',
        'strategy_5_bls_calendar_observed_sha256: "646a1029779d5e5eca1e2c48322531dcdf55f7cc7fb0649113cfd387d553eaa9"',
        'strategy_5_dukascopy_failed_hour: "2004-03-17T13:00:00Z"',
        "strategy_5_dukascopy_http_status: 503",
        'strategy_5_external_source_failure_policy: "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF"',
        'strategy_5_dukascopy_retry_rule: "FIRST_EXTERNAL_SOURCE_FAILURE_HANDOFF_REQUIRES_OWNER_AUTHORIZATION"',
        'rf027_first_failure_policy_merged_commit: "367976fa7510d0fe8c3662d5b33a9889fc824c94"',
        "strategy_5_dukascopy_inventory_required_object_count: 1085",
        "strategy_5_dukascopy_inventory_existing_object_count: 37",
        "strategy_5_dukascopy_inventory_missing_object_count: 1048",
        "strategy_5_dukascopy_controlled_downloader_status: "
        '"SOURCE_BLOCKED_AFTER_AUTHORIZED_EXECUTE"',
        'strategy_5_dukascopy_controlled_downloader_branch: "MERGED_TO_MAIN"',
        'strategy_5_dukascopy_controlled_execution_status: "SOURCE_BLOCKED_AUTHORIZATION_CONSUMED"',
        "strategy_5_dukascopy_controlled_execution_authorization_count: 1",
        'strategy_5_dukascopy_controlled_execution_authorization_record: "AUTHORIZED_ONCE_BY_OWNER_2026_10_05"',
        'strategy_5_dukascopy_controlled_execution_commit: "f3151d8915b61d1a08e79cf27133764201475e65"',
        "strategy_5_dukascopy_controlled_execution_network_requests: 1",
        "strategy_5_dukascopy_controlled_execution_downloaded_count: 0",
        "strategy_5_dukascopy_controlled_execution_existing_after: 37",
        "strategy_5_dukascopy_controlled_execution_missing_after: 1048",
        'strategy_5_dukascopy_normal_runtime_network_mode: "PROHIBITED"',
        'strategy_5_dukascopy_snapshot_bundle_status: "COMPLETE_1085_OF_1085_ZERO_NETWORK_CONFIRMED"',
        'strategy_5_dukascopy_manual_browser_probe_status: "PASS_3_OF_3_VALID_BI5"',
        'strategy_5_dukascopy_browser_pilot_status: "PASS_50_OF_50_AUTHORIZATION_CONSUMED"',
        "strategy_5_dukascopy_browser_pilot_object_limit: 50",
        "strategy_5_dukascopy_browser_pilot_max_attempts_per_object: 2",
        'strategy_5_dukascopy_browser_pilot_source_mode: "CANONICAL_BROWSER_ASSISTED_DUKASCOPY_BI5"',
        'strategy_5_dukascopy_browser_pilot_execution_status: "COMPLETE_50_OF_50"',
        'strategy_5_dukascopy_browser_pilot_fallback_policy: "NO_ALTERNATE_HOSTNAME_MIRROR_PROXY_OR_PROVIDER"',
        "strategy_5_dukascopy_browser_pilot_outcome_computed: false",
        'strategy_5_dukascopy_browser_pilot_execution_commit: "c7a10c8bcd84ca4754db92af4c63f39c02101543"',
        "strategy_5_dukascopy_browser_pilot_selected_count: 50",
        "strategy_5_dukascopy_browser_pilot_promoted_count: 50",
        "strategy_5_dukascopy_browser_pilot_skipped_count: 0",
        "strategy_5_dukascopy_browser_pilot_expected_existing_after: 87",
        "strategy_5_dukascopy_browser_pilot_expected_missing_after: 998",
        'strategy_5_dukascopy_next_external_batch_status: "OWNER_AUTHORIZATION_REQUIRED"',
        'strategy_5_dukascopy_post_pilot_inventory_status: "CONFIRMED_ZERO_NETWORK"',
        "strategy_5_dukascopy_post_pilot_inventory_required_object_count: 1085",
        "strategy_5_dukascopy_post_pilot_inventory_existing_object_count: 87",
        "strategy_5_dukascopy_post_pilot_inventory_missing_object_count: 998",
        "strategy_5_dukascopy_post_pilot_inventory_network_requests: 0",
        "strategy_5_dukascopy_post_pilot_inventory_downloaded_count: 0",
        "strategy_5_dukascopy_post_pilot_inventory_semantic_missing_count: 0",
        "strategy_5_dukascopy_post_pilot_inventory_outcome_computed: false",
        'strategy_5_dukascopy_browser_batch_250_status: "PASS_250_OF_250_AUTHORIZATION_CONSUMED"',
        "strategy_5_dukascopy_browser_batch_250_object_limit: 250",
        "strategy_5_dukascopy_browser_batch_250_max_attempts_per_object: 2",
        'strategy_5_dukascopy_browser_batch_250_source_mode: "CANONICAL_BROWSER_ASSISTED_DUKASCOPY_BI5"',
        'strategy_5_dukascopy_browser_batch_250_execution_status: "COMPLETE_250_OF_250"',
        'strategy_5_dukascopy_browser_batch_250_fallback_policy: "NO_ALTERNATE_HOSTNAME_MIRROR_PROXY_OR_PROVIDER"',
        "strategy_5_dukascopy_browser_batch_250_outcome_computed: false",
        'strategy_5_dukascopy_browser_batch_250_execution_commit: "438bc59aa6f2cc81a762914f111017f75a2e46b2"',
        "strategy_5_dukascopy_browser_batch_250_selected_count: 250",
        "strategy_5_dukascopy_browser_batch_250_promoted_count: 250",
        "strategy_5_dukascopy_browser_batch_250_skipped_count: 0",
        "strategy_5_dukascopy_browser_batch_250_expected_existing_after: 337",
        "strategy_5_dukascopy_browser_batch_250_expected_missing_after: 748",
        'strategy_5_dukascopy_browser_batch_250_evidence_status: "FULL_JSON_MANIFEST_REVIEW_PASS"',
        "strategy_5_dukascopy_browser_batch_250_attempts_1_count: 250",
        "strategy_5_dukascopy_browser_batch_250_attempts_2_count: 0",
        "strategy_5_dukascopy_browser_batch_250_record_count_min: 341",
        "strategy_5_dukascopy_browser_batch_250_record_count_max: 8535",
        'strategy_5_dukascopy_browser_batch_250_json_sha256: "36e1301d551a69990ca707e7bf33da1ce07e5e88b1e7dc23a379a66b814e6b2c"',
        'strategy_5_dukascopy_browser_batch_250_manifest_sha256: "9aa6d7646c809f7a8fb2caaf421f13553ec30ba26dee5d8d991464e1e6cad2e1"',
        'strategy_5_dukascopy_post_batch_250_inventory_status: "CONFIRMED_ZERO_NETWORK"',
        "strategy_5_dukascopy_post_batch_250_inventory_required_object_count: 1085",
        "strategy_5_dukascopy_post_batch_250_inventory_existing_object_count: 337",
        "strategy_5_dukascopy_post_batch_250_inventory_missing_object_count: 748",
        "strategy_5_dukascopy_post_batch_250_inventory_network_requests: 0",
        "strategy_5_dukascopy_post_batch_250_inventory_downloaded_count: 0",
        "strategy_5_dukascopy_post_batch_250_inventory_semantic_missing_count: 0",
        "strategy_5_dukascopy_post_batch_250_inventory_outcome_computed: false",
        'strategy_5_dukascopy_browser_remaining_748_status: "PARTIAL_747_OF_748_AUTHORIZATION_CONSUMED"',
        'strategy_5_dukascopy_browser_remaining_748_authorization_record: "OWNER_AUTHORIZED_REMAINING_748_2026_10_05"',
        "strategy_5_dukascopy_browser_remaining_748_object_count: 748",
        "strategy_5_dukascopy_browser_remaining_748_max_attempts_per_object: 2",
        'strategy_5_dukascopy_browser_remaining_748_source_mode: "CANONICAL_BROWSER_ASSISTED_DUKASCOPY_BI5"',
        'strategy_5_dukascopy_browser_remaining_748_execution_status: "COMPLETE_747_PROMOTED_1_SKIPPED"',
        'strategy_5_dukascopy_browser_remaining_748_execution_commit: "0131dd82d286814adaa76ff6e2524e0d000ca13c"',
        'strategy_5_dukascopy_browser_remaining_748_inventory_rule: "REQUIRE_EXACTLY_748_CURRENT_MISSING"',
        'strategy_5_dukascopy_browser_remaining_748_manifest_status: "MANIFEST_REVIEW_PASS_748_OF_748"',
        'strategy_5_dukascopy_browser_remaining_748_manifest_sha256: "a0d35fef473552dce8776ecbd83bf16270ecbb9767333e0fda7cc512a8b7e0f4"',
        "strategy_5_dukascopy_browser_remaining_748_selected_count: 748",
        "strategy_5_dukascopy_browser_remaining_748_promoted_count: 747",
        "strategy_5_dukascopy_browser_remaining_748_skipped_count: 1",
        "strategy_5_dukascopy_browser_remaining_748_expected_existing_after: 1084",
        "strategy_5_dukascopy_browser_remaining_748_expected_missing_after: 1",
        'strategy_5_dukascopy_browser_remaining_748_evidence_status: "FULL_JSON_MANIFEST_REVIEW_PASS"',
        'strategy_5_dukascopy_browser_remaining_748_evidence_review_commit: "b4802ea909ff7c2436f43f817bf0160dbb67cffc"',
        "strategy_5_dukascopy_browser_remaining_748_attempts_1_count: 746",
        "strategy_5_dukascopy_browser_remaining_748_attempts_2_count: 2",
        "strategy_5_dukascopy_browser_remaining_748_record_count_min: 419",
        "strategy_5_dukascopy_browser_remaining_748_record_count_max: 31693",
        "strategy_5_dukascopy_browser_remaining_748_promoted_sha256_count: 747",
        "strategy_5_dukascopy_browser_remaining_748_promoted_sha256_unique_count: 747",
        "strategy_5_dukascopy_browser_remaining_748_promoted_sha256_duplicate_count: 0",
        'strategy_5_dukascopy_browser_remaining_748_json_sha256: "ba4086fb57e71228e25c9c7ccd443a5bdea3549a9e190d2823b28a284d01c112"',
        "strategy_5_dukascopy_browser_remaining_748_skipped_ordinal: 159",
        'strategy_5_dukascopy_browser_remaining_748_skipped_hour: "2011-11-16T11:00:00Z"',
        'strategy_5_dukascopy_browser_remaining_748_skipped_source_url: "https://datafeed.dukascopy.com/datafeed/EURUSD/2011/10/16/11h_ticks.bi5"',
        'strategy_5_dukascopy_browser_remaining_748_skipped_local_path: "data/raw/dukascopy/hyp0006/EURUSD/2011/11/16/11h_ticks.bi5"',
        'strategy_5_dukascopy_browser_remaining_748_skipped_failure: "no_valid_bi5_download_within_45s_attempt_2"',
        'strategy_5_dukascopy_browser_remaining_748_skipped_file_status: "ABSENT"',
        'strategy_5_dukascopy_browser_remaining_748_consumed_sentinel_status: "VALIDATED_PASS"',
        'strategy_5_dukascopy_final_manual_intake_status: "PASS_OWNER_SUPPLIED_VALIDATED"',
        'strategy_5_dukascopy_final_manual_intake_hour: "2011-11-16T11:00:00Z"',
        'strategy_5_dukascopy_final_manual_intake_source_url: "https://datafeed.dukascopy.com/datafeed/EURUSD/2011/10/16/11h_ticks.bi5"',
        'strategy_5_dukascopy_final_manual_intake_local_path: "data/raw/dukascopy/hyp0006/EURUSD/2011/11/16/11h_ticks.bi5"',
        'strategy_5_dukascopy_final_manual_intake_sha256: "391a35cff2d48ea3a62e4121cda94a244b5d793d49354080cd77c5696d172de7"',
        "strategy_5_dukascopy_final_manual_intake_record_count: 6810",
        'strategy_5_dukascopy_final_manual_intake_decoder_status: "PASS"',
        "strategy_5_dukascopy_final_manual_intake_destination_existed_before: false",
        'strategy_5_dukascopy_final_manual_intake_byte_preserving_copy_status: "PASS"',
        'strategy_5_dukascopy_post_manual_intake_inventory_status: "CONFIRMED_ZERO_NETWORK_COMPLETE"',
        "strategy_5_dukascopy_post_manual_intake_inventory_required_object_count: 1085",
        "strategy_5_dukascopy_post_manual_intake_inventory_existing_object_count: 1085",
        "strategy_5_dukascopy_post_manual_intake_inventory_missing_object_count: 0",
        "strategy_5_dukascopy_post_manual_intake_inventory_network_requests: 0",
        "strategy_5_dukascopy_post_manual_intake_inventory_downloaded_count: 0",
        "strategy_5_dukascopy_post_manual_intake_inventory_semantic_missing_count: 0",
        "strategy_5_dukascopy_post_manual_intake_inventory_outcome_computed: false",
        'strategy_5_dukascopy_browser_remaining_748_fallback_policy: "NO_ALTERNATE_HOSTNAME_MIRROR_PROXY_OR_PROVIDER"',
        "strategy_5_dukascopy_browser_remaining_748_outcome_computed: false",
        "strategy_5_dukascopy_controlled_execution_authorized_command:",
        'rf027_controlled_downloader_merged_commit: "a638e49108e05e9618208ca577c6ebd0c74aa4e1"',
        'rf027_controlled_downloader_dry_run_commit: "a638e49108e05e9618208ca577c6ebd0c74aa4e1"',
        'rf027_controlled_downloader_dry_run_status: "DRY_RUN_READY"',
        "rf027_controlled_downloader_dry_run_event_count: 217",
        "rf027_controlled_downloader_dry_run_required_object_count: 1085",
        "rf027_controlled_downloader_dry_run_existing_object_count: 37",
        "rf027_controlled_downloader_dry_run_missing_object_count: 1048",
        "rf027_controlled_downloader_dry_run_network_requests: 0",
        'strategy_5_geometry_output_status: "RF027_CREATED_HASH_FROZEN"',
        'rf027_verified_commit: "bbbdbd301b610dfc61316c9ff82015fb0e039a47"',
        "strategy_5_rf027_candidate_event_count: 217",
        "strategy_5_rf027_complete_timestamp_geometry_event_count: 217",
        "strategy_5_rf027_required_tick_object_count: 1085",
        "strategy_5_rf027_acquired_tick_object_count: 1085",
        "strategy_5_rf027_missing_tick_object_count: 0",
        "strategy_5_rf027_protected_hyp0005_source_requests: 0",
        'strategy_5_rf027_source_bundle_sha256: "5865691103e464a86bcbb6ee9f3827aa27c68e372946fe248905ffddecb09425"',
        'strategy_5_rf027_geometry_csv_sha256: "e5830eecb920f810e44e324beb0b7691b8dc86ddfaf410d0da83877940b89034"',
        'strategy_5_data_tolerance_freeze_status: "RF028_STAGED_PRE_REVEAL"',
        'strategy_5_development_dataset_id: "DATA-BLS-DUKASCOPY-EURUSD-TICK-HYP0006-DEV-001"',
        'strategy_5_development_dataset_version: "1.0.0"',
        "strategy_5_anchor_boundary_max_abs_gap_ms: 30000",
        "strategy_5_pre_release_max_staleness_ms: 30000",
        'strategy_5_boundary_tie_break: "PREVIOUS_ON_EQUAL_GAP"',
        'strategy_5_pre_release_rule: "LAST_QUOTE_STRICTLY_BEFORE_RELEASE"',
        'strategy_5_duplicate_timestamp_tie_break: "LAST_RAW_RECORD_AT_SELECTED_MILLISECOND"',
        'strategy_5_price_pairing_rule: "BID_AND_ASK_FROM_SAME_RAW_TICK_RECORD"',
        'strategy_5_missing_data_policy: "EXCLUDE_EVENT_IF_ANY_REQUIRED_ANCHOR_FAILS_FROZEN_GAP_RULE"',
        'strategy_5_bls_calendar_candidate: "data/derived/HYP-0006-BLS-CPI-CALENDAR-2003-2021.csv"',
        'active_idea_id: "IDEA-0004"',
        'active_hypothesis_id: "HYP-0005"',
        'parallel_active_idea_id: "IDEA-0005"',
        'parallel_active_hypothesis_id: "HYP-0006"',
        "reference_strategy_selection_allowed: true",
        'selected_reference_strategy: "SINGLE_INSTRUMENT_1H_LONG_FLAT_TREND_BREAKOUT"',
        'idea_id: "IDEA-0001"', 'hypothesis_id: "HYP-0001"',
        'data_feasibility_decision: "CONDITIONAL"',
        'prototype_id: "PROTO-01"', 'prototype_status: "REJECTED"',
        'prototype_outcome: "REJECT"', 'research_line_status: "REJECTED_AT_R3"',
        'selected_market_context: "FX_SPOT_OTC"',
        'selected_instrument: "EURUSD"', "ideas_registered: 5",
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

    if core.backlog_status(backlog, "ATS2-RF-007") != "DONE":
        core.fail("RF-007 must be DONE in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-008") != "DONE / PASS":
        core.fail("RF-008 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-009") != "DONE / PASS":
        core.fail("RF-009 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-010") != "DONE / PASS":
        core.fail("RF-010 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-011") != "DONE / PASS":
        core.fail("RF-011 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-012") != "DONE / PASS":
        core.fail("RF-012 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-013") != "DONE / PASS":
        core.fail("RF-013 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-014") != "DONE / PASS":
        core.fail("RF-014 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-015") != "DONE / PASS":
        core.fail("RF-015 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-016") != "DONE / PASS":
        core.fail("RF-016 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-017") != "DONE / PASS":
        core.fail("RF-017 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-018") != "DONE / PASS":
        core.fail("RF-018 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-019") != "DONE / PASS":
        core.fail("RF-019 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-020") != "DONE / PASS":
        core.fail("RF-020 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-021") != "DONE / PASS":
        core.fail("RF-021 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-022") != "DONE / PASS":
        core.fail("RF-022 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-023") != "READY":
        core.fail("RF-023 must be READY in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-024") != "BLOCKED":
        core.fail("RF-024 must be BLOCKED in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-025") != "DONE / PASS":
        core.fail("RF-025 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-026") != "DONE / PASS":
        core.fail("RF-026 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-027") != "DONE / PASS":
        core.fail("RF-027 must be DONE / PASS in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-RF-028") != "READY":
        core.fail("RF-028 must be READY in Program Backlog")
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
