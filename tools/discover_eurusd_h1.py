#!/usr/bin/env python3
"""Run the first frozen bounded ATS market-pattern discovery search."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ats.data.loader import load_dataset  # noqa: E402
from ats.discovery.bounded import load_search_manifest, run_bounded_discovery  # noqa: E402
from ats.discovery.eurusd_h1 import EurusdH1Evaluator, PriceBar  # noqa: E402
from ats.schemas.dataset_manifest import load_dataset_manifest  # noqa: E402

SEARCH_MANIFEST_PATH = ROOT / "research/discovery/SEARCH-EURUSD-H1-2021-2025-001.yaml"
DATASET_MANIFEST_PATH = ROOT / "data/manifests/DATA-EURUSD-DUKASCOPY-H1-PROTO01.yaml"
RESULT_PATH = ROOT / "reports/local_ci/SEARCH-EURUSD-H1-2021-2025-001-result.json"
REPORT_PATH = ROOT / "reports/local_ci/SEARCH-EURUSD-H1-2021-2025-001-report.txt"
IMPLEMENTATION_PATHS = (
    "src/ats/discovery/bounded.py",
    "src/ats/discovery/eurusd_h1.py",
    "tools/discover_eurusd_h1.py",
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class DiscoveryRunError(RuntimeError):
    """Raised when the frozen first discovery run cannot be reproduced."""


def git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_implementation_revision(revision: str) -> None:
    if SHA_RE.fullmatch(revision) is None:
        raise DiscoveryRunError("Search Manifest code_revision must be an exact 40-hex commit")

    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", revision, "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        raise DiscoveryRunError("Search Manifest code_revision is not an ancestor of HEAD")

    diff = subprocess.run(
        ["git", "diff", "--quiet", revision, "HEAD", "--", *IMPLEMENTATION_PATHS],
        cwd=ROOT,
    )
    if diff.returncode == 1:
        raise DiscoveryRunError("discovery implementation changed after Search Manifest freeze")
    if diff.returncode != 0:
        raise DiscoveryRunError("cannot verify discovery implementation revision")


def build_price_bars(loaded_dataset: object) -> tuple[PriceBar, ...]:
    records = getattr(loaded_dataset, "records", None)
    if not isinstance(records, tuple):
        raise DiscoveryRunError("loaded dataset does not expose immutable records")

    bars: list[PriceBar] = []
    for record in records:
        bars.append(
            PriceBar(
                event_time=record.event_time,
                bid_open=float(record.value("bid_open")),
                bid_close=float(record.value("bid_close")),
                ask_open=float(record.value("ask_open")),
                ask_close=float(record.value("ask_close")),
            )
        )
    return tuple(bars)


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def run() -> int:
    search_manifest = load_search_manifest(SEARCH_MANIFEST_PATH)
    verify_implementation_revision(search_manifest.code_revision)

    dataset_manifest = load_dataset_manifest(DATASET_MANIFEST_PATH)
    if dataset_manifest.dataset_id != search_manifest.dataset_id:
        raise DiscoveryRunError("Search Manifest dataset_id does not match Dataset Manifest")
    if dataset_manifest.dataset_version != search_manifest.dataset_version:
        raise DiscoveryRunError("Search Manifest dataset_version does not match Dataset Manifest")

    loaded = load_dataset(dataset_manifest, root=ROOT)
    bars = build_price_bars(loaded)
    evaluator = EurusdH1Evaluator(bars, search_manifest)
    result = run_bounded_discovery(search_manifest, evaluator)

    payload = result.to_dict()
    payload["run_context"] = {
        "completed_at": now_iso(),
        "dataset_sha256": loaded.computed_sha256,
        "git_commit": git_head(),
        "implementation_revision": search_manifest.code_revision,
        "search_manifest_sha256": sha256_file(SEARCH_MANIFEST_PATH),
    }
    payload["limitations"] = [
        "Exploratory discovery only; not validation evidence.",
        "The 2021-2025 EURUSD H1 dataset is development-known for this research lane.",
        "Spread is represented by BID/ASK opens; commission and financing are excluded.",
        "Shortlisted alternatives still require separate Idea/Hypothesis conversion.",
    ]

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "ATS FIRST BOUNDED DISCOVERY RESULT",
        "==================================",
        f"Search ID: {result.search_id}",
        f"Git commit: {payload['run_context']['git_commit']}",
        f"Implementation revision: {search_manifest.code_revision}",
        f"Dataset: {result.dataset_id}@{result.dataset_version}",
        f"Dataset SHA256: {loaded.computed_sha256}",
        f"Evaluated alternatives: {result.evaluated_alternatives}",
        f"Shortlisted alternatives: {len(result.shortlisted_alternative_ids)}",
        f"Outcome: {result.outcome}",
        "Evidence class: EXPLORATORY_OBSERVATION",
        "Selection policy: PREDECLARED_SHORTLIST_RULE_ONLY",
        "",
        "SHORTLIST IDS",
        "-------------",
    ]
    if result.shortlisted_alternative_ids:
        lines.extend(result.shortlisted_alternative_ids)
    else:
        lines.append("NONE")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nMachine result: {RESULT_PATH.relative_to(ROOT)}")
    return 0


def main() -> int:
    try:
        return run()
    except (
        DiscoveryRunError,
        OSError,
        ValueError,
        subprocess.SubprocessError,
    ) as exc:
        print(f"M6 DISCOVERY BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
