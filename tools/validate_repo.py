#!/usr/bin/env python3
"""Structural validator for the ATS repository."""

from __future__ import annotations

import re
from pathlib import Path


REQUIRED_FILES = (
    "README.md",
    "00_НАЧАТЬ_ЗДЕСЬ.md",
    "AGENTS.md",
    "01_СТАТУС_ПРОЕКТА.md",
    "02_СЛЕДУЮЩИЙ_ШАГ.md",
    "03_СОСТОЯНИЕ_ПРОЕКТА.yaml",
    "SECURITY.md",
    "00_Управление_проектом/ДОРОЖНАЯ_КАРТА.md",
    "00_Управление_проектом/МАТРИЦА_ВОРОТ.md",
    "00_Управление_проектом/БЭКЛОГ_ЗАДАЧ.md",
    "00_Управление_проектом/РЕЕСТР_ЭКСПЕРИМЕНТОВ.csv",
    "01_Контур_продукта/ВИДЕНИЕ_И_ЦЕЛИ.md",
    "01_Контур_продукта/ФУНКЦИОНАЛЬНЫЕ_ТРЕБОВАНИЯ.md",
    "02_Архитектура_и_решения/БАЗОВЫЙ_СТЕК.md",
    "02_Архитектура_и_решения/АРХИТЕКТУРА_РОБОТА.md",
    "02_Архитектура_и_решения/ADR/ADR-0001-13-ворот.md",
    "02_Архитектура_и_решения/ADR/ADR-0002-защитный-контур.md",
    "02_Архитектура_и_решения/ADR/ADR-0003-независимый-период.md",
    "03_Нормативная_база_и_правила/РЕГЛАМЕНТЫ.md",
    "03_Нормативная_база_и_правила/ИСТОЧНИКИ.md",
    "04_Реестры_и_связи/РЕЕСТР_АРТЕФАКТОВ.csv",
    "05_Коллизии/ОТКРЫТЫЕ_ВОПРОСЫ.md",
    "data/README.md",
    "experiments/README.md",
    "reports/README.md",
    "src/README.md",
    "tests/README.md",
)

FORBIDDEN_PLACEHOLDERS = (
    re.compile(r"\{\{[^{}]+\}\}"),
    re.compile(r"\[(?:Имя|Дата|ФИО|Сумма|XXX|Вставить[^\]]*)\]", re.IGNORECASE),
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
)

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".csv", ".py", ".txt"}


def fail(message: str) -> None:
    print(f"BLOCKING: {message}")


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    blocking = 0

    for relative in REQUIRED_FILES:
        path = repo / relative
        if not path.is_file():
            fail(f"missing required file: {relative}")
            blocking += 1

    state_path = repo / "03_СОСТОЯНИЕ_ПРОЕКТА.yaml"
    if state_path.is_file():
        state = state_path.read_text(encoding="utf-8")
        required_state_markers = (
            "gates_total: 13",
            "gate_id: G01",
            "real_money_trading_allowed: false",
            "scaling_allowed: false",
            "martingale_allowed: false",
        )
        for marker in required_state_markers:
            if marker not in state:
                fail(f"state marker missing or changed: {marker}")
                blocking += 1

        gate_rows = re.findall(r"(?m)^  G(\d{2}):\s+([A-Z_]+)\s*$", state)
        gate_ids = {int(number) for number, _ in gate_rows}
        if gate_ids != set(range(1, 14)):
            fail("state must contain exactly G01 through G13")
            blocking += 1

    matrix_path = repo / "00_Управление_проектом/МАТРИЦА_ВОРОТ.md"
    if matrix_path.is_file():
        matrix = matrix_path.read_text(encoding="utf-8")
        matrix_gate_ids = {int(value) for value in re.findall(r"\| `G(\d{2})` \|", matrix)}
        if matrix_gate_ids != set(range(1, 14)):
            fail("gate matrix must contain exactly G01 through G13")
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

    risk_mandate = repo / "01_Контур_продукта/РИСК_МАНДАТ.md"
    if risk_mandate.exists():
        state = state_path.read_text(encoding="utf-8") if state_path.exists() else ""
        if "G01: PASS" not in state:
            fail("risk mandate exists, but G01 is not PASS")
            blocking += 1

    if blocking:
        print(f"ATS repository validation: BLOCKING ({blocking})")
        return 1

    print("ATS repository validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
