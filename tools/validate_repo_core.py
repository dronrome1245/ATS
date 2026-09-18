#!/usr/bin/env python3
"""Structural validator for the ATS v2 repository."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from urllib.parse import unquote

REQUIRED_FILES = (
    "README.md",
    "00_НАЧАТЬ_ЗДЕСЬ.md",
    "AGENTS.md",
    "AI_HANDOFF.md",
    "01_СТАТУС_ПРОЕКТА.md",
    "02_СЛЕДУЮЩИЙ_ШАГ.md",
    "03_СОСТОЯНИЕ_ПРОЕКТА.yaml",
    "SECURITY.md",
    "governance/program/PROGRAM_CHARTER_V2.md",
    "governance/program/OPERATING_MODEL_V2.md",
    "governance/program/PROGRAM_WBS_V2.md",
    "governance/program/REPOSITORY_STRUCTURE_V2.md",
    "governance/program/M0_FINAL_SWEEP.md",
    "governance/program/M0_EXIT_REVIEW.md",
    "governance/methodology/STRATEGY_LIFECYCLE_V2.md",
    "governance/methodology/RESEARCH_METHODOLOGY_V1.md",
    "governance/methodology/IDEA_INTAKE_PROCESS.md",
    "governance/methodology/HYPOTHESIS_MODEL.md",
    "governance/methodology/DATA_FEASIBILITY_REVIEW.md",
    "governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md",
    "governance/methodology/ECONOMIC_PRE_SCREEN.md",
    "governance/methodology/CANDIDATE_PROMOTION_PROCESS.md",
    "governance/methodology/EXPERIMENT_REGISTRATION.md",
    "governance/backlog/PROGRAM_BACKLOG_V2.md",
    "governance/methodology/templates/README.md",
    "governance/methodology/templates/IDEA_TEMPLATE.md",
    "governance/methodology/templates/HYPOTHESIS_TEMPLATE.md",
    "governance/methodology/templates/DATA_FEASIBILITY_TEMPLATE.md",
    "governance/methodology/templates/CHEAP_PROTOTYPE_TEMPLATE.md",
    "governance/methodology/templates/ECONOMIC_PRE_SCREEN_TEMPLATE.md",
    "governance/methodology/templates/CANDIDATE_PROMOTION_REVIEW_TEMPLATE.md",
    "governance/methodology/templates/CANDIDATE_TEMPLATE.md",
    "governance/methodology/templates/CANDIDATE_EVIDENCE_INDEX_TEMPLATE.md",
    "governance/methodology/templates/experiment/manifest.yaml",
    "governance/methodology/templates/experiment/result.json",
    "governance/methodology/templates/experiment/conclusion.md",
    "governance/methodology/templates/strategy_version/VERSION.yaml",
    "governance/methodology/templates/strategy_version/SPECIFICATION.md",
    "governance/methodology/templates/strategy_version/PARAMETERS.yaml",
    "governance/methodology/templates/strategy_version/EVIDENCE_INDEX.md",
    "experiments/README.md",
    "experiments/REGISTRY.csv",
    "tools/search_experiments.py",
    "legacy/v1/README.md",
    "legacy/v1/MIGRATION_INDEX.md",
    "legacy/v1/CARRYOVER.md",
    "legacy/v1/program-management/БЭКЛОГ_ЗАДАЧ.md",
    "legacy/v1/program-management/ДОРОЖНАЯ_КАРТА.md",
    "legacy/v1/program-management/МАТРИЦА_ВОРОТ.md",
    "legacy/v1/program-management/РЕЕСТР_ЭКСПЕРИМЕНТОВ.csv",
    "legacy/v1/product/ВИДЕНИЕ_И_ЦЕЛИ.md",
    "legacy/v1/product/ФУНКЦИОНАЛЬНЫЕ_ТРЕБОВАНИЯ.md",
    "legacy/v1/architecture/АРХИТЕКТУРА_РОБОТА.md",
    "legacy/v1/architecture/БАЗОВЫЙ_СТЕК.md",
    "legacy/v1/architecture/ADR/ADR-0001-13-ворот.md",
    "legacy/v1/architecture/ADR/ADR-0002-защитный-контур.md",
    "legacy/v1/architecture/ADR/ADR-0003-независимый-период.md",
    "legacy/v1/regulations/ИСТОЧНИКИ.md",
    "legacy/v1/regulations/РЕГЛАМЕНТЫ.md",
    "legacy/v1/registers/РЕЕСТР_АРТЕФАКТОВ.csv",
    "legacy/v1/collisions/ОТКРЫТЫЕ_ВОПРОСЫ.md",
    "data/README.md",
    "reports/README.md",
    "src/README.md",
    "tests/README.md",
)

MIGRATED_CURRENT_V2_FILES = (
    "00_Управление_проектом/v2/PROGRAM_CHARTER_V2.md",
    "00_Управление_проектом/v2/OPERATING_MODEL_V2.md",
    "00_Управление_проектом/v2/PROGRAM_WBS_V2.md",
    "00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md",
    "00_Управление_проектом/v2/STRATEGY_LIFECYCLE_V2.md",
    "00_Управление_проектом/v2/RESEARCH_METHODOLOGY_V1.md",
)

MIGRATED_LEGACY_SOURCE_FILES = (
    "00_Управление_проектом/БЭКЛОГ_ЗАДАЧ.md",
    "00_Управление_проектом/ДОРОЖНАЯ_КАРТА.md",
    "00_Управление_проектом/МАТРИЦА_ВОРОТ.md",
    "00_Управление_проектом/РЕЕСТР_ЭКСПЕРИМЕНТОВ.csv",
    "01_Контур_продукта/ВИДЕНИЕ_И_ЦЕЛИ.md",
    "01_Контур_продукта/ФУНКЦИОНАЛЬНЫЕ_ТРЕБОВАНИЯ.md",
    "02_Архитектура_и_решения/АРХИТЕКТУРА_РОБОТА.md",
    "02_Архитектура_и_решения/БАЗОВЫЙ_СТЕК.md",
    "02_Архитектура_и_решения/ADR/ADR-0001-13-ворот.md",
    "02_Архитектура_и_решения/ADR/ADR-0002-защитный-контур.md",
    "02_Архитектура_и_решения/ADR/ADR-0003-независимый-период.md",
    "03_Нормативная_база_и_правила/ИСТОЧНИКИ.md",
    "03_Нормативная_база_и_правила/РЕГЛАМЕНТЫ.md",
    "04_Реестры_и_связи/РЕЕСТР_АРТЕФАКТОВ.csv",
    "05_Коллизии/ОТКРЫТЫЕ_ВОПРОСЫ.md",
)

STALE_V1_PREFIXES = (
    "00_Управление_проектом/",
    "01_Контур_продукта/",
    "02_Архитектура_и_решения/",
    "03_Нормативная_база_и_правила/",
    "04_Реестры_и_связи/",
    "05_Коллизии/",
)

OPERATIONAL_FILES = (
    "README.md",
    "00_НАЧАТЬ_ЗДЕСЬ.md",
    "AGENTS.md",
    "AI_HANDOFF.md",
    "01_СТАТУС_ПРОЕКТА.md",
    "02_СЛЕДУЮЩИЙ_ШАГ.md",
    "03_СОСТОЯНИЕ_ПРОЕКТА.yaml",
    "governance/backlog/PROGRAM_BACKLOG_V2.md",
    "experiments/README.md",
    ".github/copilot-instructions.md",
    "CLAUDE.md",
)

CANONICAL_PATH_KEYS = (
    "canonical_state_file",
    "ai_handoff",
    "agent_rules",
    "human_status",
    "next_action",
    "program_charter",
    "operating_model",
    "strategy_lifecycle",
    "research_methodology",
    "idea_intake_process",
    "hypothesis_model",
    "data_feasibility_review",
    "cheap_prototype_protocol",
    "economic_pre_screen",
    "candidate_promotion_process",
    "experiment_registration",
    "experiment_registry",
    "program_wbs",
    "repository_structure",
    "program_backlog",
    "research_templates",
    "m0_exit_review",
    "legacy_readme",
    "migration_index",
    "carryover",
)

CONTENT_MARKERS = {
    "governance/program/M0_EXIT_REVIEW.md": (
        "Decision:** `PASS`",
        "M0_PROGRAM_REBASELINE = COMPLETED",
        "ATS2-M1-001",
    ),
    "legacy/v1/MIGRATION_INDEX.md": (
        "HISTORY",
        "REFERENCE",
        "REVIEW_NEEDED",
        "всего: 15 artifacts",
    ),
    "legacy/v1/CARRYOVER.md": (
        "OQ-001",
        "OQ-009",
        "ATS2-M2-001",
        "does **not** create speculative duplicate future tasks",
    ),
    "governance/methodology/IDEA_INTAKE_PROCESS.md": (
        "IDEA-0001",
        "SCREEN",
        "PARK",
        "REJECT",
        "Duplicate / overlap",
        "Structural acceptance test",
    ),
    "governance/methodology/templates/IDEA_TEMPLATE.md": (
        "Origin / provenance",
        "Duplicate / overlap check",
        "SCREEN",
        "PARK",
        "REJECT",
    ),
    "governance/methodology/HYPOTHESIS_MODEL.md": (
        "HYP-0001",
        "Falsifiability admission rule",
        "DATA_FEASIBILITY",
        "Decision-time information premise",
        "Structural acceptance test",
    ),
    "governance/methodology/templates/HYPOTHESIS_TEMPLATE.md": (
        "Supersedes Hypothesis ID",
        "Decision-time information premise",
        "Falsifiability check",
        "DATA_FEASIBILITY",
        "READY_FOR_DATA_FEASIBILITY",
    ),
    "governance/methodology/DATA_FEASIBILITY_REVIEW.md": (
        "Decision-time information availability",
        "Universe, survivorship and selection bias",
        "Transformation trace and dataset identity",
        "FEASIBLE",
        "CONDITIONAL",
        "Structural acceptance test",
    ),
    "governance/methodology/templates/DATA_FEASIBILITY_TEMPLATE.md": (
        "Hypothesis ID",
        "Decision-time availability assessment",
        "Survivorship risk",
        "Leakage and overlap risks",
        "Known gaps",
        "FEASIBLE",
        "CONDITIONAL",
    ),
    "governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md": (
        "one prototype, one question",
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "ITERATE",
        "EXPLORATORY_PROTOTYPE",
        "Prototype versus formal Experiment",
        "Structural acceptance test",
    ),
    "governance/methodology/templates/CHEAP_PROTOTYPE_TEMPLATE.md": (
        "Prototype sequence",
        "Prototype question",
        "Pre-run decision rule",
        "Search and iteration accounting",
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "EXPLORATORY_PROTOTYPE",
    ),
    "governance/methodology/ECONOMIC_PRE_SCREEN.md": (
        "No universal profitability threshold",
        "E1 — Effect Magnitude",
        "E9 — Economic Margin of Safety",
        "ADVANCE_TO_CANDIDATE_REVIEW",
        "RETURN_TO_RESEARCH",
        "Relationship to Candidate promotion",
        "Structural acceptance test",
    ),
    "governance/methodology/templates/ECONOMIC_PRE_SCREEN_TEMPLATE.md": (
        "E1 Effect Magnitude",
        "E9 Economic Margin of Safety",
        "ADVANCE_TO_CANDIDATE_REVIEW",
        "RETURN_TO_RESEARCH",
        "Capital use / efficiency",
        "Evidence weakness and research freedom",
    ),
    "governance/methodology/CANDIDATE_PROMOTION_PROCESS.md": (
        "CAND-0001",
        "READY_FOR_S01",
        "PROMOTE",
        "PARK",
        "REJECT",
        "Strategy ID",
        "Structural acceptance test",
    ),
    "governance/methodology/templates/CANDIDATE_PROMOTION_REVIEW_TEMPLATE.md": (
        "CPR-01",
        "ADVANCE_TO_CANDIDATE_REVIEW",
        "Candidate ID created",
        "PROMOTE",
        "PARK",
        "REJECT",
    ),
    "governance/methodology/templates/CANDIDATE_TEMPLATE.md": (
        "READY_FOR_S01",
        "Strategy ID: `null`",
        "EVIDENCE_INDEX.md",
        "ADVANCE_TO_CANDIDATE_REVIEW",
        "Decision: `PROMOTE`",
    ),
    "governance/methodology/templates/CANDIDATE_EVIDENCE_INDEX_TEMPLATE.md": (
        "EXPLORATORY_PROTOTYPE",
        "Pre-registered",
        "Formal validation claim eligible",
        "Negative and discarded evidence",
    ),
    "governance/methodology/EXPERIMENT_REGISTRATION.md": (
        "EXP-YYYYMMDD-nnn",
        "REGISTERED_EXPERIMENT",
        "Registration boundary in Git",
        "Amendments before result observation",
        "Post-result changes",
        "Structural acceptance test",
    ),
    "governance/methodology/templates/experiment/manifest.yaml": (
        'schema_version: "2.0"',
        "evidence_class: REGISTERED_EXPERIMENT",
        "registered_on:",
        "registered_by_role:",
        "amendments: []",
        "implementation_reference:",
        "source_snapshot_reference:",
        "predefined_decision_rule:",
    ),
    "governance/methodology/templates/experiment/result.json": (
        '"schema_version": "2.0"',
        '"run_context"',
        '"primary_metrics"',
        '"machine_outcome"',
        '"reproducibility_status"',
    ),
    "governance/methodology/templates/experiment/conclusion.md": (
        "Evidence class: `REGISTERED_EXPERIMENT`",
        "Registered primary metrics and decision rule",
        "Decision-rule evaluation",
        "Deviations and defects",
    ),
    "governance/methodology/templates/README.md": (
        "Candidate Promotion Review",
        "CANDIDATE_EVIDENCE_INDEX_TEMPLATE.md",
        "READY_FOR_S01",
        "EXPERIMENT_REGISTRATION.md",
        "REGISTERED_EXPERIMENT",
    ),
    "experiments/README.md": (
        "Experiment Registry",
        "experiments/REGISTRY.csv",
        "tools/search_experiments.py",
        "registration_revision",
        "zero fictitious experiment rows",
    ),
    "tools/search_experiments.py": (
        "REGISTRY.csv",
        "FILTER_FIELDS",
        "--contains",
        "evidence_class",
        "machine_outcome",
    ),
}

FORBIDDEN_PLACEHOLDERS = (
    re.compile(r"\{\{[^{}]+\}\}"),
    re.compile(r"\[(?:Имя|Дата|ФИО|Сумма|XXX|Вставить[^\]]*)\]", re.IGNORECASE),
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".csv", ".py", ".txt", ".json"}
IGNORED_RUNTIME_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
}
TRANSITIONAL_STATE = Path("00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml")
EXPERIMENT_ID = re.compile(r"^EXP-\d{8}-\d{3}$")
REGISTRY_HEADER = (
    "experiment_id",
    "status",
    "research_stage",
    "evidence_class",
    "idea_id",
    "hypothesis_id",
    "candidate_id",
    "strategy_id",
    "strategy_version",
    "package_path",
    "manifest_path",
    "registration_revision",
    "registered_at",
    "completed_at",
    "machine_outcome",
    "decision",
    "supersedes_experiment_id",
    "superseded_by_experiment_id",
)
REGISTRY_STATUSES = {
    "DRAFT",
    "REGISTERED",
    "RUNNING",
    "COMPLETED",
    "CANCELLED",
    "SUPERSEDED",
}
REGISTERED_OR_LATER = {"REGISTERED", "RUNNING", "COMPLETED", "SUPERSEDED"}


def fail(message: str) -> None:
    print(f"BLOCKING: {message}")


def extract_quoted_scalar(text: str, key: str) -> str | None:
    match = re.search(rf'(?m)^\s*{re.escape(key)}:\s*"([^"]+)"\s*$', text)
    return match.group(1) if match else None


def current_text_files(repo: Path):
    for path in repo.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(repo)
        if relative.parts and relative.parts[0] == "legacy":
            continue
        if any(part in IGNORED_RUNTIME_DIRS for part in relative.parts):
            continue
        if len(relative.parts) >= 2 and relative.parts[:2] == ("reports", "local_ci"):
            continue
        yield path, relative


def validate_local_markdown_links(repo: Path, path: Path, relative: Path) -> int:
    if path.suffix.lower() != ".md":
        return 0

    blocking = 0
    text = path.read_text(encoding="utf-8")
    for match in MARKDOWN_LINK.finditer(text):
        raw = match.group(1).strip()
        if not raw:
            continue
        target = raw.split(maxsplit=1)[0].strip("<>")
        if target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        target = unquote(target)
        candidate = (repo / target.lstrip("/")) if target.startswith("/") else (path.parent / target)
        if not candidate.exists():
            fail(f"broken local Markdown link in {relative}: {raw}")
            blocking += 1
    return blocking


def backlog_status(backlog: str, task_id: str) -> str | None:
    for line in backlog.splitlines():
        if line.startswith("|") and f"`{task_id}`" in line:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 4:
                return cells[3]
    return None


def validate_content_markers(repo: Path) -> int:
    blocking = 0
    for relative, markers in CONTENT_MARKERS.items():
        path = repo / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                fail(f"content marker missing in {relative}: {marker}")
                blocking += 1
    return blocking


def validate_registry(repo: Path) -> int:
    blocking = 0
    path = repo / "experiments/REGISTRY.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        actual_header = tuple(reader.fieldnames or ())
        if actual_header != REGISTRY_HEADER:
            fail(f"Experiment Registry header mismatch: {actual_header}")
            blocking += 1
            return blocking
        rows = list(reader)

    seen_ids: set[str] = set()
    references: list[tuple[str, str, str]] = []

    for line_no, row in enumerate(rows, start=2):
        experiment_id = row["experiment_id"].strip()
        status = row["status"].strip()

        if not EXPERIMENT_ID.fullmatch(experiment_id):
            fail(f"Experiment Registry invalid experiment_id at line {line_no}: {experiment_id}")
            blocking += 1
            continue
        if experiment_id in seen_ids:
            fail(f"Experiment Registry duplicate experiment_id: {experiment_id}")
            blocking += 1
        seen_ids.add(experiment_id)

        if status not in REGISTRY_STATUSES:
            fail(f"Experiment Registry invalid status for {experiment_id}: {status}")
            blocking += 1

        expected_package = f"experiments/{experiment_id}/"
        expected_manifest = f"experiments/{experiment_id}/manifest.yaml"
        if row["package_path"].strip() != expected_package:
            fail(f"Experiment Registry package_path mismatch for {experiment_id}")
            blocking += 1
        if row["manifest_path"].strip() != expected_manifest:
            fail(f"Experiment Registry manifest_path mismatch for {experiment_id}")
            blocking += 1

        if not (repo / expected_package).is_dir():
            fail(f"Experiment Registry package missing for {experiment_id}: {expected_package}")
            blocking += 1
        if not (repo / expected_manifest).is_file():
            fail(f"Experiment Registry manifest missing for {experiment_id}: {expected_manifest}")
            blocking += 1

        if status in REGISTERED_OR_LATER:
            if row["evidence_class"].strip() != "REGISTERED_EXPERIMENT":
                fail(f"Experiment Registry registered evidence class mismatch for {experiment_id}")
                blocking += 1
            if not row["registration_revision"].strip():
                fail(f"Experiment Registry registration_revision missing for {experiment_id}")
                blocking += 1
            if not row["registered_at"].strip():
                fail(f"Experiment Registry registered_at missing for {experiment_id}")
                blocking += 1

        if status == "COMPLETED":
            if not row["completed_at"].strip():
                fail(f"Experiment Registry completed_at missing for {experiment_id}")
                blocking += 1
            if not row["decision"].strip():
                fail(f"Experiment Registry decision missing for completed {experiment_id}")
                blocking += 1

        for field in ("supersedes_experiment_id", "superseded_by_experiment_id"):
            reference = row[field].strip()
            if reference:
                if not EXPERIMENT_ID.fullmatch(reference):
                    fail(f"Experiment Registry invalid {field} for {experiment_id}: {reference}")
                    blocking += 1
                references.append((experiment_id, field, reference))

    for experiment_id, field, reference in references:
        if reference not in seen_ids:
            fail(f"Experiment Registry {field} for {experiment_id} references missing ID: {reference}")
            blocking += 1

    return blocking


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    blocking = 0

    for relative in REQUIRED_FILES:
        if not (repo / relative).is_file():
            fail(f"missing required file: {relative}")
            blocking += 1

    if (repo / TRANSITIONAL_STATE).exists():
        fail(f"transitional duplicate state must not exist: {TRANSITIONAL_STATE}")
        blocking += 1

    for relative in MIGRATED_CURRENT_V2_FILES:
        if (repo / relative).exists():
            fail(f"migrated current-v2 duplicate must not exist: {relative}")
            blocking += 1

    for relative in MIGRATED_LEGACY_SOURCE_FILES:
        if (repo / relative).exists():
            fail(f"migrated legacy source path must not exist: {relative}")
            blocking += 1

    state_path = repo / "03_СОСТОЯНИЕ_ПРОЕКТА.yaml"
    state = state_path.read_text(encoding="utf-8") if state_path.is_file() else ""
    required_state_markers = (
        'schema_version: "2.0"',
        "phase: M1_RESEARCH_METHODOLOGY",
        "status: IN_PROGRESS",
        "M0_PROGRAM_REBASELINE: COMPLETED",
        "M1_RESEARCH_METHODOLOGY: IN_PROGRESS",
        "exit_decision: PASS",
        'idea_intake_process: "governance/methodology/IDEA_INTAKE_PROCESS.md"',
        'hypothesis_model: "governance/methodology/HYPOTHESIS_MODEL.md"',
        'data_feasibility_review: "governance/methodology/DATA_FEASIBILITY_REVIEW.md"',
        'cheap_prototype_protocol: "governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md"',
        'economic_pre_screen: "governance/methodology/ECONOMIC_PRE_SCREEN.md"',
        'candidate_promotion_process: "governance/methodology/CANDIDATE_PROMOTION_PROCESS.md"',
        'experiment_registration: "governance/methodology/EXPERIMENT_REGISTRATION.md"',
        'experiment_registry: "experiments/REGISTRY.csv"',
        'current_task: "ATS2-M1-009"',
        'current_ready_task: "ATS2-M1-009"',
        "reference_strategy_selection_allowed: false",
        "candidates_active: 0",
        "experiments_registered: 0",
        "physical_migration_complete: true",
        "real_money_trading_allowed: false",
        "minimal_live_trading_allowed: false",
        "demo_trading_allowed: false",
        "scaling_allowed: false",
        "martingale_allowed: false",
        "thirteen_gate_model_is_program_roadmap: false",
    )
    for marker in required_state_markers:
        if marker not in state:
            fail(f"canonical state marker missing or changed: {marker}")
            blocking += 1

    for key in CANONICAL_PATH_KEYS:
        relative = extract_quoted_scalar(state, key)
        if not relative:
            fail(f"canonical state must define quoted path: {key}")
            blocking += 1
        elif not (repo / relative).exists():
            fail(f"canonical state path does not exist for {key}: {relative}")
            blocking += 1

    blocking += validate_content_markers(repo)
    blocking += validate_registry(repo)

    search_tool = repo / "tools/search_experiments.py"
    if search_tool.is_file():
        try:
            compile(search_tool.read_text(encoding="utf-8"), str(search_tool), "exec")
        except SyntaxError as exc:
            fail(f"search_experiments.py syntax error: {exc}")
            blocking += 1

    next_artifact = extract_quoted_scalar(state, "next_artifact")
    last_completed = extract_quoted_scalar(state, "last_completed_artifact")
    next_task_id = extract_quoted_scalar(state, "next_task_id")

    if not next_artifact:
        fail("canonical state must define quoted next_artifact")
        blocking += 1
    if not last_completed:
        fail("canonical state must define quoted last_completed_artifact")
        blocking += 1
    elif not (repo / last_completed).exists():
        fail(f"canonical last_completed_artifact does not exist: {last_completed}")
        blocking += 1
    if not next_task_id:
        fail("canonical state must define quoted next_task_id")
        blocking += 1

    handoff_path = repo / "AI_HANDOFF.md"
    next_path = repo / "02_СЛЕДУЮЩИЙ_ШАГ.md"
    backlog_path = repo / "governance/backlog/PROGRAM_BACKLOG_V2.md"
    handoff = handoff_path.read_text(encoding="utf-8") if handoff_path.is_file() else ""
    next_step = next_path.read_text(encoding="utf-8") if next_path.is_file() else ""
    backlog = backlog_path.read_text(encoding="utf-8") if backlog_path.is_file() else ""

    if backlog_status(backlog, "ATS2-M1-008") != "DONE":
        fail("Program Backlog does not record M1-008 as DONE")
        blocking += 1
    if backlog_status(backlog, "ATS2-M1-009") != "READY":
        fail("Program Backlog does not expose M1-009 as READY")
        blocking += 1

    if next_artifact:
        if next_artifact not in handoff:
            fail("AI_HANDOFF.md does not mention canonical next_artifact")
            blocking += 1
        if next_artifact not in next_step:
            fail("02_СЛЕДУЮЩИЙ_ШАГ.md does not mention canonical next_artifact")
            blocking += 1

    if next_task_id:
        if next_task_id not in backlog:
            fail("canonical next_task_id is missing from Program Backlog")
            blocking += 1
        if next_task_id not in handoff:
            fail("AI_HANDOFF.md does not mention canonical next_task_id")
            blocking += 1
        if next_task_id not in next_step:
            fail("02_СЛЕДУЮЩИЙ_ШАГ.md does not mention canonical next_task_id")
            blocking += 1

    if last_completed and last_completed not in handoff:
        fail("AI_HANDOFF.md does not mention canonical last_completed_artifact")
        blocking += 1

    agents = (repo / "AGENTS.md").read_text(encoding="utf-8") if (repo / "AGENTS.md").is_file() else ""
    for marker in ("03_СОСТОЯНИЕ_ПРОЕКТА.yaml", "governance/backlog/PROGRAM_BACKLOG_V2.md", "legacy/v1/"):
        if marker not in agents:
            fail(f"AGENTS.md marker missing: {marker}")
            blocking += 1

    for relative_name in OPERATIONAL_FILES:
        path = repo / relative_name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for stale_prefix in STALE_V1_PREFIXES:
            if stale_prefix in text:
                fail(f"stale pre-migration v1 namespace in operational file {relative_name}: {stale_prefix}")
                blocking += 1

    for path, relative in current_text_files(repo):
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PLACEHOLDERS:
            if pattern.search(text):
                fail(f"forbidden placeholder pattern in {relative}")
                blocking += 1
                break
        blocking += validate_local_markdown_links(repo, path, relative)

    if blocking:
        print(f"ATS repository validation: BLOCKING ({blocking})")
        return 1

    print("ATS repository validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
