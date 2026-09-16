#!/usr/bin/env python3
"""ATS repository validator for the accepted M2 Research Stack ADR baseline."""

from __future__ import annotations

import csv
from pathlib import Path

import validate_repo_core as core

TAXONOMY = "governance/methodology/EVIDENCE_TAXONOMY.md"
REVIEW_PROTOCOL = "governance/methodology/RESEARCH_REVIEW_PROTOCOL.md"
REVIEW_CHECKS = "governance/methodology/RESEARCH_REVIEW_CHECKS.md"
REVIEW_DECISIONS = "governance/methodology/RESEARCH_REVIEW_DECISIONS.md"
REVIEW_TEMPLATE = "governance/methodology/templates/RESEARCH_REVIEW_TEMPLATE.md"
M1_EXIT = "governance/program/M1_EXIT_REVIEW.md"
CONSUMER_PROFILE = "governance/program/REFERENCE_CONSUMER_PROFILE.md"
RESEARCH_STACK_ADR = "governance/decisions/ADR-0001-RESEARCH-STACK.md"
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


def configure() -> None:
    core.REQUIRED_FILES = core.REQUIRED_FILES + (
        TAXONOMY, REVIEW_PROTOCOL, REVIEW_CHECKS, REVIEW_DECISIONS, REVIEW_TEMPLATE,
        M1_EXIT, CONSUMER_PROFILE, RESEARCH_STACK_ADR,
    )
    core.CANONICAL_PATH_KEYS = core.CANONICAL_PATH_KEYS + (
        "evidence_taxonomy", "research_review_protocol", "m1_exit_review",
        "reference_consumer_profile", "research_stack_adr",
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
    core.CONTENT_MARKERS[M1_EXIT] = (
        "Decision:** `PASS`", "M1_RESEARCH_METHODOLOGY = COMPLETED / PASS",
        "ATS2-M2-000 — Reference Consumer Profile", "Pipeline counters intentionally remain zero",
    )
    core.CONTENT_MARKERS[CONSUMER_PROFILE] = (
        "single research logic instance", "Minimum data contract",
        "Timestamp and ordering semantics", "Minimum research decision interface",
        "Deterministic replay/backtest contract", "Cost-model consumer contract",
        "Experiment integration", "M2 acceptance fixture", "ATS2-M2-001",
    )
    core.CONTENT_MARKERS[RESEARCH_STACK_ADR] = (
        "Status:** ACCEPTED", "CPython 3.13 series", "uv.lock",
        "Pydantic v2", "PyYAML 6.x", "NumPy 2.x", "M2 is **not DataFrame-first**",
        "Alternatives considered", "ATS2-M2-002 — Reproducible environment",
    )
    core.CONTENT_MARKERS["governance/program/PROGRAM_WBS_V2.md"] = (
        "`WBS-2.0`", "Reference Consumer Profile", "`WBS-2.1`",
        "Consumer Profile", "Reference Strategy #1 ещё не выбрана",
    )
    core.CONTENT_MARKERS["data/README.md"] = (
        "Dataset Manifests", "M2 boundary", "Reference Strategy #1 remains M3 work",
    )
    core.CONTENT_MARKERS["src/README.md"] = (
        "ADR-0001-RESEARCH-STACK.md", "CPython 3.13 series", "uv.lock",
        "src/ats/", "ATS2-M2-002",
    )
    core.CONTENT_MARKERS["reports/README.md"] = (
        "source_class", "qualified_evidence_class", "WBS-2.8",
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
    )
    core.CONTENT_MARKERS["tools/search_experiments.py"] = (
        "REGISTRY.csv", "qualified_evidence_class", "--contains",
    )


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
        'schema_version: "2.0"', "phase: M2_RESEARCH_PLATFORM_MVP",
        "M0_PROGRAM_REBASELINE: COMPLETED", "M1_RESEARCH_METHODOLOGY: COMPLETED",
        "M2_RESEARCH_PLATFORM_MVP: IN_PROGRESS", "exit_decision: PASS",
        'm1_exit_review: "governance/program/M1_EXIT_REVIEW.md"',
        'reference_consumer_profile: "governance/program/REFERENCE_CONSUMER_PROFILE.md"',
        'research_stack_adr: "governance/decisions/ADR-0001-RESEARCH-STACK.md"',
        'last_completed_task_id: "ATS2-M2-001"',
        'current_task: "ATS2-M2-002"', 'current_ready_task: "ATS2-M2-002"',
        'current_wbs: "WBS-2.2"', "reference_strategy_selection_allowed: false",
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

    if core.backlog_status(backlog, "ATS2-M2-001") != "DONE":
        core.fail("M2-001 must be DONE in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-M2-002") != "READY":
        core.fail("M2-002 must be READY in Program Backlog")
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
    for marker in ("03_СОСТОЯНИЕ_ПРОЕКТА.yaml", "governance/backlog/PROGRAM_BACKLOG_V2.md", "legacy/v1/"):
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
