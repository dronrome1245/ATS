from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from ats.discovery.bounded import (
    DiscoveryAlternative,
    DiscoveryContractError,
    SearchManifest,
    load_search_manifest,
    run_bounded_discovery,
)

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "governance/methodology/templates/discovery/SEARCH_MANIFEST_TEMPLATE.yaml"


def synthetic_evaluator(alternative: DiscoveryAlternative) -> dict[str, int | float]:
    threshold = {parameter.name: parameter.value for parameter in alternative.parameters}[
        "threshold"
    ]
    assert isinstance(threshold, float)
    return {"effect": threshold - 0.5, "count": 10}


def test_template_loads_and_full_search_space_is_retained() -> None:
    manifest = load_search_manifest(TEMPLATE)
    result = run_bounded_discovery(manifest, synthetic_evaluator)

    assert result.search_space_count == 3
    assert result.evaluated_alternatives == 3
    assert tuple(point.alternative_id for point in result.points) == (
        "alt-low",
        "alt-mid",
        "alt-high",
    )
    assert result.shortlisted_alternative_ids == ("alt-mid", "alt-high")
    assert result.outcome == "SHORTLIST_FOR_IDEA_INTAKE"
    assert result.points[0].shortlisted is False


def test_result_serialization_is_deterministic_and_exploratory_only() -> None:
    manifest = load_search_manifest(TEMPLATE)
    first = run_bounded_discovery(manifest, synthetic_evaluator)
    second = run_bounded_discovery(manifest, synthetic_evaluator)

    assert first.to_json() == second.to_json()
    decoded = json.loads(first.to_json())
    assert decoded["attempt_type"] == "DISCOVERY_SEARCH"
    assert decoded["qualified_evidence_class"] == "EXPLORATORY_OBSERVATION"
    assert decoded["selection_policy"] == "PREDECLARED_SHORTLIST_RULE_ONLY"
    assert decoded["search_space_count"] == 3
    assert len(decoded["points"]) == 3
    assert all("rank" not in point for point in decoded["points"])


def test_no_shortlist_retains_all_negative_alternatives() -> None:
    data = load_search_manifest(TEMPLATE).model_dump()
    data["shortlist_rule"]["threshold"] = 10.0
    manifest = SearchManifest.model_validate(data)
    result = run_bounded_discovery(manifest, synthetic_evaluator)

    assert result.outcome == "NO_PATTERN_SHORTLISTED"
    assert result.shortlisted_alternative_ids == ()
    assert len(result.points) == 3


def test_search_budget_blocks_undeclared_expansion() -> None:
    data = load_search_manifest(TEMPLATE).model_dump()
    data["max_combinations"] = 2

    with pytest.raises(ValidationError, match="exceed max_combinations"):
        SearchManifest.model_validate(data)


def test_alternative_must_use_declared_dimensions() -> None:
    data = load_search_manifest(TEMPLATE).model_dump()
    data["alternatives"][0]["horizon"] = "UNDECLARED"

    with pytest.raises(ValidationError, match="undeclared horizon"):
        SearchManifest.model_validate(data)


def test_shortlist_metric_must_be_declared() -> None:
    data = load_search_manifest(TEMPLATE).model_dump()
    data["shortlist_rule"]["metric_name"] = "missing"

    with pytest.raises(ValidationError, match="shortlist metric"):
        SearchManifest.model_validate(data)


def test_stochastic_seed_and_protocol_must_be_declared_together() -> None:
    data = load_search_manifest(TEMPLATE).model_dump()
    data["random_seed"] = 7

    with pytest.raises(ValidationError, match="declared together"):
        SearchManifest.model_validate(data)


def test_metric_set_mismatch_is_rejected() -> None:
    manifest = load_search_manifest(TEMPLATE)

    with pytest.raises(DiscoveryContractError, match="metric set mismatch"):
        run_bounded_discovery(manifest, lambda _alternative: {"effect": 1.0})


def test_non_finite_metric_is_rejected() -> None:
    manifest = load_search_manifest(TEMPLATE)

    with pytest.raises(DiscoveryContractError, match="must be finite"):
        run_bounded_discovery(
            manifest,
            lambda _alternative: {"effect": float("inf"), "count": 1},
        )
