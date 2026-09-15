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
    "governance/backlog/PROGRAM_BACKLOG_V2.md",
    "governance/methodology/templates/README.md",
    "governance/methodology/templates/IDEA_TEMPLATE.md",
    "governance/methodology/templates/HYPOTHESIS_TEMPLATE.md",
    "governance/methodology/templates/CANDIDATE_TEMPLATE.md",
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
        'current_task: "ATS2-M1-003"',
        'current_ready_task: "ATS2-M1-003"',
        "reference_strategy_selection_allowed: false",
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

    if "ATS2-M1-002" not in backlog or "Hypothesis model" not in backlog or "DONE" not in backlog:
        fail("Program Backlog does not record completed M1-002")
        blocking += 1
    if "ATS2-M1-003" not in backlog or "Data Feasibility review" not in backlog or "READY" not in backlog:
        fail("Program Backlog does not expose M1-003 as ready work")
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
