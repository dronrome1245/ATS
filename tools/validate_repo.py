#!/usr/bin/env python3
"""Structural validator for the ATS v2 repository."""

from __future__ import annotations

import re
from pathlib import Path


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
    "governance/methodology/STRATEGY_LIFECYCLE_V2.md",
    "governance/methodology/RESEARCH_METHODOLOGY_V1.md",
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

FORBIDDEN_PLACEHOLDERS = (
    re.compile(r"\{\{[^{}]+\}\}"),
    re.compile(r"\[(?:Имя|Дата|ФИО|Сумма|XXX|Вставить[^\]]*)\]", re.IGNORECASE),
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
)

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".csv", ".py", ".txt", ".json"}
TRANSITIONAL_STATE = Path("00_Управление_проектом/v2/PROGRAM_STATE_V2.yaml")


def fail(message: str) -> None:
    print(f"BLOCKING: {message}")


def extract_quoted_scalar(text: str, key: str) -> str | None:
    match = re.search(rf'(?m)^\s*{re.escape(key)}:\s*"([^"]+)"\s*$', text)
    return match.group(1) if match else None


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
        "phase: M0_PROGRAM_REBASELINE",
        "status: IN_PROGRESS",
        'canonical_state_file: "03_СОСТОЯНИЕ_ПРОЕКТА.yaml"',
        'program_charter: "governance/program/PROGRAM_CHARTER_V2.md"',
        'operating_model: "governance/program/OPERATING_MODEL_V2.md"',
        'program_wbs: "governance/program/PROGRAM_WBS_V2.md"',
        'repository_structure: "governance/program/REPOSITORY_STRUCTURE_V2.md"',
        'strategy_lifecycle: "governance/methodology/STRATEGY_LIFECYCLE_V2.md"',
        'research_methodology: "governance/methodology/RESEARCH_METHODOLOGY_V1.md"',
        'program_backlog: "governance/backlog/PROGRAM_BACKLOG_V2.md"',
        'research_templates: "governance/methodology/templates/README.md"',
        'legacy_readme: "legacy/v1/README.md"',
        'migration_index: "legacy/v1/MIGRATION_INDEX.md"',
        'carryover: "legacy/v1/CARRYOVER.md"',
        "designated_artifacts: 15",
        "physical_migration_complete: true",
        "real_money_trading_allowed: false",
        "scaling_allowed: false",
        "martingale_allowed: false",
        "thirteen_gate_model_is_program_roadmap: false",
    )
    for marker in required_state_markers:
        if marker not in state:
            fail(f"canonical v2 state marker missing or changed: {marker}")
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

    next_artifact = extract_quoted_scalar(state, "next_artifact")
    last_completed = extract_quoted_scalar(state, "last_completed_artifact")
    next_task_id = extract_quoted_scalar(state, "next_task_id")

    if not next_artifact:
        fail("canonical state must define quoted next_artifact")
        blocking += 1
    if not last_completed:
        fail("canonical state must define quoted last_completed_artifact")
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

    agents_path = repo / "AGENTS.md"
    agents = agents_path.read_text(encoding="utf-8") if agents_path.is_file() else ""
    if "03_СОСТОЯНИЕ_ПРОЕКТА.yaml" not in agents:
        fail("AGENTS.md must point to canonical state")
        blocking += 1
    if "governance/backlog/PROGRAM_BACKLOG_V2.md" not in agents:
        fail("AGENTS.md must point to canonical Program Backlog")
        blocking += 1
    if "governance/program/PROGRAM_WBS_V2.md" not in agents:
        fail("AGENTS.md must point to canonical Program WBS")
        blocking += 1

    for path in repo.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(repo)
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PLACEHOLDERS:
            if pattern.search(text):
                fail(f"forbidden placeholder pattern in {relative}")
                blocking += 1
                break

    if blocking:
        print(f"ATS repository validation: BLOCKING ({blocking})")
        return 1

    print("ATS repository validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
