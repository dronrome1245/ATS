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
    "00_Управление_проектом/v2/PROGRAM_CHARTER_V2.md",
    "00_Управление_проектом/v2/OPERATING_MODEL_V2.md",
    "00_Управление_проектом/v2/STRATEGY_LIFECYCLE_V2.md",
    "00_Управление_проектом/v2/RESEARCH_METHODOLOGY_V1.md",
    "00_Управление_проектом/v2/PROGRAM_WBS_V2.md",
    "00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md",
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
    "data/README.md",
    "experiments/README.md",
    "reports/README.md",
    "src/README.md",
    "tests/README.md",
)

LEGACY_REFERENCE_FILES = (
    "00_Управление_проектом/ДОРОЖНАЯ_КАРТА.md",
    "00_Управление_проектом/МАТРИЦА_ВОРОТ.md",
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

    for relative in LEGACY_REFERENCE_FILES:
        if not (repo / relative).is_file():
            fail(f"legacy reference file unexpectedly missing: {relative}")
            blocking += 1

    if (repo / TRANSITIONAL_STATE).exists():
        fail(f"transitional duplicate state must not exist: {TRANSITIONAL_STATE}")
        blocking += 1

    state_path = repo / "03_СОСТОЯНИЕ_ПРОЕКТА.yaml"
    state = state_path.read_text(encoding="utf-8") if state_path.is_file() else ""

    required_state_markers = (
        'schema_version: "2.0"',
        "phase: M0_PROGRAM_REBASELINE",
        "status: IN_PROGRESS",
        'canonical_state_file: "03_СОСТОЯНИЕ_ПРОЕКТА.yaml"',
        'repository_structure: "00_Управление_проектом/v2/REPOSITORY_STRUCTURE_V2.md"',
        'program_backlog: "governance/backlog/PROGRAM_BACKLOG_V2.md"',
        'research_templates: "governance/methodology/templates/README.md"',
        "real_money_trading_allowed: false",
        "scaling_allowed: false",
        "martingale_allowed: false",
        "thirteen_gate_model_is_program_roadmap: false",
    )
    for marker in required_state_markers:
        if marker not in state:
            fail(f"canonical v2 state marker missing or changed: {marker}")
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

    if "PROGRAM_STATE_V2.yaml" in handoff:
        fail("AI_HANDOFF.md still references removed transitional state")
        blocking += 1

    agents_path = repo / "AGENTS.md"
    agents = agents_path.read_text(encoding="utf-8") if agents_path.is_file() else ""
    if "03_СОСТОЯНИЕ_ПРОЕКТА.yaml" not in agents:
        fail("AGENTS.md must point to canonical state")
        blocking += 1
    if "governance/backlog/PROGRAM_BACKLOG_V2.md" not in agents:
        fail("AGENTS.md must point to canonical Program Backlog")
        blocking += 1
    if "PROGRAM_STATE_V2.yaml" in agents:
        fail("AGENTS.md still references removed transitional state")
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
