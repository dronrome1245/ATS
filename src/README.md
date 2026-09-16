# Source code

ATS is in `M2_RESEARCH_PLATFORM_MVP`.

Canonical stack decision:

`governance/decisions/ADR-0001-RESEARCH-STACK.md`

M2 source code will use:

- CPython 3.13 series;
- `pyproject.toml` + `uv` + committed `uv.lock` for environment/dependency reproducibility;
- Pydantic v2 + PyYAML at manifest/config boundaries;
- NumPy 2.x for baseline numerical analytics;
- standard-library CSV/JSON and a typed ordered-record interface for the initial loader/replay path;
- pytest + Ruff for development quality gates.

Planned package boundary:

```text
src/ats/
├── schemas/
├── data/
├── strategy/
├── replay/
├── costs/
├── analytics/
└── runner/
```

M2 is not DataFrame-first and does not baseline pandas, Polars, PyArrow, DuckDB, an external backtesting framework, Docker, broker adapters or live execution. Such capabilities are added only after a real consumer demonstrates the need.

A concrete Reference Strategy #1 is not selected until M3. Deterministic synthetic software fixtures used for platform tests are not research entities or trading evidence.

Next implementation step is `ATS2-M2-002 — Reproducible environment`; no loader/replay implementation should precede the pinned environment baseline.
