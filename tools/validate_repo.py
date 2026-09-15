#!/usr/bin/env python3
"""ATS repository validator after M1-009."""

from __future__ import annotations

import csv
from pathlib import Path

import validate_repo_core as core

TAXONOMY = "governance/methodology/EVIDENCE_TAXONOMY.md"
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
    core.REQUIRED_FILES = core.REQUIRED_FILES + (TAXONOMY,)
    core.CANONICAL_PATH_KEYS = core.CANONICAL_PATH_KEYS + ("evidence_taxonomy",)
    core.REGISTRY_HEADER = HEADER
    core.CONTENT_MARKERS[TAXONOMY] = (
        "source_class", "qualified_evidence_class", "EXPLORATORY_PROTOTYPE",
        "REGISTERED_EXPERIMENT", "VALIDATION_EVIDENCE",
        "INDEPENDENT_EXAMINATION_EVIDENCE", "STRESS_EVIDENCE",
        "DEMO_SHADOW_EVIDENCE", "MINIMAL_LIVE_EVIDENCE",
        "Negative evidence and class retention", "Structural acceptance test",
    )
    core.CONTENT_MARKERS["governance/methodology/templates/CANDIDATE_EVIDENCE_INDEX_TEMPLATE.md"] = (
        "Source class", "Qualified evidence class",
        "CURRENT / SUPERSEDED / INVALIDATED / HISTORICAL",
        "Negative and discarded evidence", "Candidate promotion never upgrades evidence class",
    )
    core.CONTENT_MARKERS["governance/methodology/templates/strategy_version/EVIDENCE_INDEX.md"] = (
        "Source class", "Qualified evidence class", "VALIDATION_EVIDENCE",
        "INDEPENDENT_EXAMINATION_EVIDENCE", "MINIMAL_LIVE_EVIDENCE", "Evidence status",
    )
    core.CONTENT_MARKERS["experiments/README.md"] = (
        "Experiment Registry", "EVIDENCE_TAXONOMY.md", "qualified_evidence_class",
        "tools/search_experiments.py", "registration_revision",
    )
    core.CONTENT_MARKERS["tools/search_experiments.py"] = (
        "REGISTRY.csv", "FILTER_FIELDS", "qualified_evidence_class", "--contains",
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
        'schema_version: "2.0"', "phase: M1_RESEARCH_METHODOLOGY",
        "M0_PROGRAM_REBASELINE: COMPLETED", "M1_RESEARCH_METHODOLOGY: IN_PROGRESS",
        'evidence_taxonomy: "governance/methodology/EVIDENCE_TAXONOMY.md"',
        'current_task: "ATS2-M1-010"', 'current_ready_task: "ATS2-M1-010"',
        "reference_strategy_selection_allowed: false", "experiments_registered: 0",
        "physical_migration_complete: true", "thirteen_gate_model_is_program_roadmap: false",
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
            core.fail("Experiment Registry header mismatch after taxonomy extension")
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

    if core.backlog_status(backlog, "ATS2-M1-009") != "DONE":
        core.fail("M1-009 must be DONE in Program Backlog")
        blocking += 1
    if core.backlog_status(backlog, "ATS2-M1-010") != "READY":
        core.fail("M1-010 must be READY in Program Backlog")
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
