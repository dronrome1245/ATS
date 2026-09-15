#!/usr/bin/env python3
"""Structural validator for the ATS v2 repository."""

from __future__ import annotations

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
    "experiments/README.md",
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
    "program_wbs",
    "repository_structure",
    "program_backlog",
    "research_templates",
    "m0_exit_review",
    "legacy_readme",
    "migration_index",
    "carryover",
)

FORBIDDEN_PLACEHOLDERS = (
    re.compile(r"\{\{[^{}]+\}\}"),
    re.compile(r"\[(?:Имя|Дата|ФИО|Сумма|XXX|Вставить[^\]]*)\]", re.IGNORECASE),
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".csv", ".py", ".txt", ".json"}
TRANSITIONAL_STATE = Path("00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml")


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
        'current_task: "ATS2-M1-008"',
        'current_ready_task: "ATS2-M1-008"',
        "reference_strategy_selection_allowed: false",
        "candidates_active: 0",
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

    exit_review = (repo / "governance/program/M0_EXIT_REVIEW.md").read_text(encoding="utf-8")
    for marker in ("Decision:** `PASS`", "M0_PROGRAM_REBASELINE = COMPLETED", "ATS2-M1-001"):
        if marker not in exit_review:
            fail(f"M0 exit review marker missing: {marker}")
            blocking += 1

    migration_index = (repo / "legacy/v1/MIGRATION_INDEX.md").read_text(encoding="utf-8")
    for marker in ("HISTORY", "REFERENCE", "REVIEW_NEEDED", "всего: 15 artifacts"):
        if marker not in migration_index:
            fail(f"legacy migration index marker missing: {marker}")
            blocking += 1

    carryover = (repo / "legacy/v1/CARRYOVER.md").read_text(encoding="utf-8")
    for marker in ("OQ-001", "OQ-009", "ATS2-M2-001", "does **not** create speculative duplicate future tasks"):
        if marker not in carryover:
            fail(f"legacy carryover marker missing: {marker}")
            blocking += 1

    idea_process = (repo / "governance/methodology/IDEA_INTAKE_PROCESS.md").read_text(encoding="utf-8")
    for marker in ("IDEA-0001", "SCREEN", "PARK", "REJECT", "Duplicate / overlap", "Structural acceptance test"):
        if marker not in idea_process:
            fail(f"Idea intake process marker missing: {marker}")
            blocking += 1

    idea_template = (repo / "governance/methodology/templates/IDEA_TEMPLATE.md").read_text(encoding="utf-8")
    for marker in ("Origin / provenance", "Duplicate / overlap check", "SCREEN", "PARK", "REJECT"):
        if marker not in idea_template:
            fail(f"Idea template marker missing: {marker}")
            blocking += 1

    hypothesis_model = (repo / "governance/methodology/HYPOTHESIS_MODEL.md").read_text(encoding="utf-8")
    for marker in ("HYP-0001", "Falsifiability admission rule", "DATA_FEASIBILITY", "Decision-time information premise", "Structural acceptance test"):
        if marker not in hypothesis_model:
            fail(f"Hypothesis model marker missing: {marker}")
            blocking += 1

    hypothesis_template = (repo / "governance/methodology/templates/HYPOTHESIS_TEMPLATE.md").read_text(encoding="utf-8")
    for marker in ("Supersedes Hypothesis ID", "Decision-time information premise", "Falsifiability check", "DATA_FEASIBILITY", "READY_FOR_DATA_FEASIBILITY"):
        if marker not in hypothesis_template:
            fail(f"Hypothesis template marker missing: {marker}")
            blocking += 1

    data_review = (repo / "governance/methodology/DATA_FEASIBILITY_REVIEW.md").read_text(encoding="utf-8")
    for marker in (
        "Decision-time information availability",
        "Universe, survivorship and selection bias",
        "Transformation trace and dataset identity",
        "FEASIBLE",
        "CONDITIONAL",
        "PARK",
        "REJECT",
        "Structural acceptance test",
    ):
        if marker not in data_review:
            fail(f"Data Feasibility process marker missing: {marker}")
            blocking += 1

    data_template = (repo / "governance/methodology/templates/DATA_FEASIBILITY_TEMPLATE.md").read_text(encoding="utf-8")
    for marker in (
        "Hypothesis ID",
        "Decision-time availability assessment",
        "Survivorship risk",
        "Leakage and overlap risks",
        "Known gaps",
        "FEASIBLE",
        "CONDITIONAL",
        "PARK",
        "REJECT",
    ):
        if marker not in data_template:
            fail(f"Data Feasibility template marker missing: {marker}")
            blocking += 1

    prototype_protocol = (repo / "governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md").read_text(encoding="utf-8")
    for marker in (
        "one prototype, one question",
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "ITERATE",
        "EXPLORATORY_PROTOTYPE",
        "Prototype versus formal Experiment",
        "Structural acceptance test",
    ):
        if marker not in prototype_protocol:
            fail(f"Cheap Prototype protocol marker missing: {marker}")
            blocking += 1

    prototype_template = (repo / "governance/methodology/templates/CHEAP_PROTOTYPE_TEMPLATE.md").read_text(encoding="utf-8")
    for marker in (
        "Prototype sequence",
        "Prototype question",
        "Pre-run decision rule",
        "Search and iteration accounting",
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "EXPLORATORY_PROTOTYPE",
        "Registered Experiment ID: `NOT_APPLICABLE`",
    ):
        if marker not in prototype_template:
            fail(f"Cheap Prototype template marker missing: {marker}")
            blocking += 1

    economic_screen = (repo / "governance/methodology/ECONOMIC_PRE_SCREEN.md").read_text(encoding="utf-8")
    for marker in (
        "No universal profitability threshold",
        "E1 — Effect Magnitude",
        "E9 — Economic Margin of Safety",
        "ADVANCE_TO_CANDIDATE_REVIEW",
        "RETURN_TO_RESEARCH",
        "Relationship to Candidate promotion",
        "Structural acceptance test",
    ):
        if marker not in economic_screen:
            fail(f"Economic Pre-Screen marker missing: {marker}")
            blocking += 1

    economic_template = (repo / "governance/methodology/templates/ECONOMIC_PRE_SCREEN_TEMPLATE.md").read_text(encoding="utf-8")
    for marker in (
        "E1 Effect Magnitude",
        "E9 Economic Margin of Safety",
        "ADVANCE_TO_CANDIDATE_REVIEW",
        "RETURN_TO_RESEARCH",
        "Capital use / efficiency",
        "Evidence weakness and research freedom",
    ):
        if marker not in economic_template:
            fail(f"Economic Pre-Screen template marker missing: {marker}")
            blocking += 1

    candidate_process = (repo / "governance/methodology/CANDIDATE_PROMOTION_PROCESS.md").read_text(encoding="utf-8")
    for marker in (
        "CAND-0001",
        "READY_FOR_S01",
        "PROMOTE",
        "PARK",
        "REJECT",
        "Strategy ID",
        "Structural acceptance test",
    ):
        if marker not in candidate_process:
            fail(f"Candidate promotion process marker missing: {marker}")
            blocking += 1

    promotion_template = (repo / "governance/methodology/templates/CANDIDATE_PROMOTION_REVIEW_TEMPLATE.md").read_text(encoding="utf-8")
    for marker in (
        "CPR-01",
        "ADVANCE_TO_CANDIDATE_REVIEW",
        "Candidate ID created",
        "PROMOTE",
        "PARK",
        "REJECT",
    ):
        if marker not in promotion_template:
            fail(f"Candidate promotion review template marker missing: {marker}")
            blocking += 1

    candidate_template = (repo / "governance/methodology/templates/CANDIDATE_TEMPLATE.md").read_text(encoding="utf-8")
    for marker in (
        "READY_FOR_S01",
        "Strategy ID: `null`",
        "EVIDENCE_INDEX.md",
        "ADVANCE_TO_CANDIDATE_REVIEW",
        "Decision: `PROMOTE`",
    ):
        if marker not in candidate_template:
            fail(f"Candidate template marker missing: {marker}")
            blocking += 1

    candidate_evidence_template = (repo / "governance/methodology/templates/CANDIDATE_EVIDENCE_INDEX_TEMPLATE.md").read_text(encoding="utf-8")
    for marker in (
        "EXPLORATORY_PROTOTYPE",
        "Pre-registered",
        "Formal validation claim eligible",
        "Negative and discarded evidence",
    ):
        if marker not in candidate_evidence_template:
            fail(f"Candidate evidence index template marker missing: {marker}")
            blocking += 1

    experiment_registration = (repo / "governance/methodology/EXPERIMENT_REGISTRATION.md").read_text(encoding="utf-8")
    for marker in (
        "EXP-YYYYMMDD-nnn",
        "REGISTERED_EXPERIMENT",
        "Registration boundary in Git",
        "Amendments before result observation",
        "Post-result changes",
        "Structural acceptance test",
    ):
        if marker not in experiment_registration:
            fail(f"Experiment registration marker missing: {marker}")
            blocking += 1

    experiment_manifest = (repo / "governance/methodology/templates/experiment/manifest.yaml").read_text(encoding="utf-8")
    for marker in (
        'schema_version: "2.0"',
        "evidence_class: REGISTERED_EXPERIMENT",
        "registered_on:",
        "registered_by_role:",
        "amendments: []",
        "implementation_reference:",
        "source_snapshot_reference:",
        "predefined_decision_rule:",
    ):
        if marker not in experiment_manifest:
            fail(f"Experiment manifest marker missing: {marker}")
            blocking += 1

    experiment_result = (repo / "governance/methodology/templates/experiment/result.json").read_text(encoding="utf-8")
    for marker in (
        '"schema_version": "2.0"',
        '"run_context"',
        '"primary_metrics"',
        '"machine_outcome"',
        '"reproducibility_status"',
    ):
        if marker not in experiment_result:
            fail(f"Experiment result schema marker missing: {marker}")
            blocking += 1

    experiment_conclusion = (repo / "governance/methodology/templates/experiment/conclusion.md").read_text(encoding="utf-8")
    for marker in (
        "Evidence class: `REGISTERED_EXPERIMENT`",
        "Registered primary metrics and decision rule",
        "Decision-rule evaluation",
        "Deviations and defects",
    ):
        if marker not in experiment_conclusion:
            fail(f"Experiment conclusion marker missing: {marker}")
            blocking += 1

    templates_index = (repo / "governance/methodology/templates/README.md").read_text(encoding="utf-8")
    for marker in (
        "Candidate Promotion Review",
        "CANDIDATE_EVIDENCE_INDEX_TEMPLATE.md",
        "READY_FOR_S01",
        "Experiment",
        "EXPERIMENT_REGISTRATION.md",
        "REGISTERED_EXPERIMENT",
    ):
        if marker not in templates_index:
            fail(f"Templates index marker missing: {marker}")
            blocking += 1

    experiments_readme = (repo / "experiments/README.md").read_text(encoding="utf-8")
    for marker in (
        "EXPERIMENT_REGISTRATION.md",
        "REGISTERED_EXPERIMENT",
        "experiments/REGISTRY.csv",
        "Formal experiment",
    ):
        if marker not in experiments_readme:
            fail(f"Experiments README marker missing: {marker}")
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

    if "ATS2-M1-007" not in backlog or "Experiment registration schema" not in backlog or "DONE" not in backlog:
        fail("Program Backlog does not record completed M1-007")
        blocking += 1
    if "ATS2-M1-008" not in backlog or "Experiment registry" not in backlog or "READY" not in backlog:
        fail("Program Backlog does not expose M1-008 as ready work")
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
