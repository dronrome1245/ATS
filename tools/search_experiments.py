#!/usr/bin/env python3
"""Search the canonical ATS experiment registry using exact field filters or text."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REGISTRY_PATH = Path(__file__).resolve().parents[1] / "experiments" / "REGISTRY.csv"
FILTER_FIELDS = {
    "id": "experiment_id",
    "status": "status",
    "stage": "research_stage",
    "evidence_class": "evidence_class",
    "idea": "idea_id",
    "hypothesis": "hypothesis_id",
    "candidate": "candidate_id",
    "strategy": "strategy_id",
    "decision": "decision",
    "outcome": "machine_outcome",
}
DISPLAY_FIELDS = (
    "experiment_id",
    "status",
    "research_stage",
    "evidence_class",
    "hypothesis_id",
    "candidate_id",
    "strategy_id",
    "machine_outcome",
    "decision",
    "manifest_path",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search experiments/REGISTRY.csv")
    for arg_name in FILTER_FIELDS:
        parser.add_argument(f"--{arg_name.replace('_', '-')}")
    parser.add_argument(
        "--contains",
        help="Case-insensitive substring matched against all registry fields.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def load_rows() -> list[dict[str, str]]:
    with REGISTRY_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def matches(row: dict[str, str], args: argparse.Namespace) -> bool:
    for arg_name, field_name in FILTER_FIELDS.items():
        expected = getattr(args, arg_name)
        if expected is not None and row.get(field_name, "") != expected:
            return False
    if args.contains:
        needle = args.contains.casefold()
        if not any(needle in value.casefold() for value in row.values() if value):
            return False
    return True


def print_table(rows: list[dict[str, str]]) -> None:
    if not rows:
        print("No experiments matched.")
        return

    widths = {
        field: max(len(field), *(len(row.get(field, "")) for row in rows))
        for field in DISPLAY_FIELDS
    }
    header = "  ".join(field.ljust(widths[field]) for field in DISPLAY_FIELDS)
    print(header)
    print("  ".join("-" * widths[field] for field in DISPLAY_FIELDS))
    for row in rows:
        print("  ".join(row.get(field, "").ljust(widths[field]) for field in DISPLAY_FIELDS))


def main() -> int:
    args = parse_args()
    rows = [row for row in load_rows() if matches(row, args)]
    if args.as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print_table(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
