"""Deterministic bounded market-pattern discovery for ATS M6."""

from __future__ import annotations

import json
import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

JsonScalar = str | int | float | bool | None
Numeric = int | float


class DiscoveryContractError(ValueError):
    """Raised when a discovery manifest or evaluator violates the M6 contract."""


class StrictModel(BaseModel):
    """Immutable discovery boundary model with unknown fields rejected."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class ShortlistOperator(StrEnum):
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"


class ParameterAssignment(StrictModel):
    name: str = Field(min_length=1)
    value: JsonScalar

    @field_validator("value")
    @classmethod
    def require_finite_parameter(cls, value: JsonScalar) -> JsonScalar:
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("parameter values must be finite")
        return value


class DiscoveryAlternative(StrictModel):
    alternative_id: str = Field(min_length=1)
    pattern_family: str = Field(min_length=1)
    feature_condition: str = Field(min_length=1)
    horizon: str = Field(min_length=1)
    direction: str = Field(min_length=1)
    filter_regime: str | None = None
    parameters: tuple[ParameterAssignment, ...] = ()

    @model_validator(mode="after")
    def require_unique_parameter_names(self) -> "DiscoveryAlternative":
        names = [parameter.name for parameter in self.parameters]
        if len(names) != len(set(names)):
            raise ValueError("alternative parameter names must be unique")
        return self


class ShortlistRule(StrictModel):
    metric_name: str = Field(min_length=1)
    operator: ShortlistOperator
    threshold: float

    @field_validator("threshold")
    @classmethod
    def require_finite_threshold(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("shortlist threshold must be finite")
        return value


class SearchManifest(StrictModel):
    schema_version: Literal["1.0"]
    search_id: str = Field(min_length=1)
    dataset_id: str = Field(min_length=1)
    dataset_version: str = Field(min_length=1)
    development_scope: str = Field(min_length=1)
    market_universe: tuple[str, ...] = Field(min_length=1)
    timestamp_semantics: str = Field(min_length=1)
    pattern_families: tuple[str, ...] = Field(min_length=1)
    feature_condition_families: tuple[str, ...] = Field(min_length=1)
    horizons: tuple[str, ...] = Field(min_length=1)
    directions: tuple[str, ...] = Field(min_length=1)
    filters_regimes: tuple[str, ...] = ()
    metric_names: tuple[str, ...] = Field(min_length=1)
    max_combinations: int = Field(ge=1)
    shortlist_rule: ShortlistRule | None
    random_seed: int | None
    stochastic_protocol: str | None
    cost_execution_applicability: str = Field(min_length=1)
    excluded_protected_blocks: tuple[str, ...] = Field(min_length=1)
    code_revision: str = Field(min_length=1)
    implementation_reference: str = Field(min_length=1)
    alternatives: tuple[DiscoveryAlternative, ...] = Field(min_length=1)
    known_limitations: tuple[str, ...] = ()

    @field_validator(
        "market_universe",
        "pattern_families",
        "feature_condition_families",
        "horizons",
        "directions",
        "filters_regimes",
        "metric_names",
        "excluded_protected_blocks",
        "known_limitations",
    )
    @classmethod
    def require_nonempty_unique_items(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if any(not value.strip() for value in values):
            raise ValueError("manifest list items must be non-empty")
        if len(values) != len(set(values)):
            raise ValueError("manifest list items must be unique")
        return values

    @model_validator(mode="after")
    def validate_search_contract(self) -> "SearchManifest":
        alternative_ids = [alternative.alternative_id for alternative in self.alternatives]
        if len(alternative_ids) != len(set(alternative_ids)):
            raise ValueError("alternative_id values must be unique")
        if len(self.alternatives) > self.max_combinations:
            raise ValueError("declared alternatives exceed max_combinations")

        for alternative in self.alternatives:
            if alternative.pattern_family not in self.pattern_families:
                raise ValueError("alternative uses undeclared pattern_family")
            if alternative.feature_condition not in self.feature_condition_families:
                raise ValueError("alternative uses undeclared feature_condition")
            if alternative.horizon not in self.horizons:
                raise ValueError("alternative uses undeclared horizon")
            if alternative.direction not in self.directions:
                raise ValueError("alternative uses undeclared direction")
            if (
                alternative.filter_regime is not None
                and alternative.filter_regime not in self.filters_regimes
            ):
                raise ValueError("alternative uses undeclared filter_regime")

        if self.shortlist_rule is not None:
            if self.shortlist_rule.metric_name not in self.metric_names:
                raise ValueError("shortlist metric must be declared in metric_names")

        if (self.random_seed is None) != (self.stochastic_protocol is None):
            raise ValueError("random_seed and stochastic_protocol must be declared together")

        return self


Evaluator = Callable[[DiscoveryAlternative], Mapping[str, Numeric]]


@dataclass(frozen=True, slots=True)
class DiscoveryPoint:
    alternative_id: str
    pattern_family: str
    feature_condition: str
    horizon: str
    direction: str
    filter_regime: str | None
    parameters: tuple[tuple[str, JsonScalar], ...]
    metrics: tuple[tuple[str, Numeric], ...]
    shortlisted: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "alternative_id": self.alternative_id,
            "direction": self.direction,
            "feature_condition": self.feature_condition,
            "filter_regime": self.filter_regime,
            "horizon": self.horizon,
            "metrics": dict(self.metrics),
            "parameters": dict(self.parameters),
            "pattern_family": self.pattern_family,
            "shortlisted": self.shortlisted,
        }


@dataclass(frozen=True, slots=True)
class DiscoveryResult:
    search_id: str
    dataset_id: str
    dataset_version: str
    metric_names: tuple[str, ...]
    search_space_count: int
    evaluated_alternatives: int
    shortlisted_alternative_ids: tuple[str, ...]
    outcome: str
    points: tuple[DiscoveryPoint, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "attempt_type": "DISCOVERY_SEARCH",
            "dataset_id": self.dataset_id,
            "dataset_version": self.dataset_version,
            "evaluated_alternatives": self.evaluated_alternatives,
            "metric_names": list(self.metric_names),
            "outcome": self.outcome,
            "points": [point.to_dict() for point in self.points],
            "qualified_evidence_class": "EXPLORATORY_OBSERVATION",
            "schema_version": "m6-bounded-discovery-1",
            "search_id": self.search_id,
            "search_space_count": self.search_space_count,
            "selection_policy": "PREDECLARED_SHORTLIST_RULE_ONLY",
            "shortlisted_alternative_ids": list(self.shortlisted_alternative_ids),
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )


def parse_search_manifest(data: Any) -> SearchManifest:
    """Validate a parsed bounded-discovery Search Manifest mapping."""

    if not isinstance(data, dict):
        raise TypeError("Search Manifest top level must be a mapping")
    return SearchManifest.model_validate(data)


def load_search_manifest(path: str | Path) -> SearchManifest:
    """Load one UTF-8 YAML Search Manifest using safe parsing."""

    manifest_path = Path(path)
    with manifest_path.open("r", encoding="utf-8") as handle:
        parsed = yaml.safe_load(handle)
    return parse_search_manifest(parsed)


def _validate_metric_value(value: Numeric, *, metric_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DiscoveryContractError(f"metric {metric_name!r} must be numeric")
    if isinstance(value, float) and not math.isfinite(value):
        raise DiscoveryContractError(f"metric {metric_name!r} must be finite")


def _is_shortlisted(rule: ShortlistRule | None, metrics: Mapping[str, Numeric]) -> bool:
    if rule is None:
        return False
    value = metrics[rule.metric_name]
    if rule.operator is ShortlistOperator.GREATER_EQUAL:
        return value >= rule.threshold
    return value <= rule.threshold


def run_bounded_discovery(manifest: SearchManifest, evaluator: Evaluator) -> DiscoveryResult:
    """Evaluate every declared alternative exactly once under the predeclared manifest."""

    if not callable(evaluator):
        raise TypeError("evaluator must be callable")

    expected_metric_names = set(manifest.metric_names)
    points: list[DiscoveryPoint] = []
    shortlisted_ids: list[str] = []

    for alternative in manifest.alternatives:
        raw_metrics = evaluator(alternative)
        if not isinstance(raw_metrics, Mapping):
            raise DiscoveryContractError("evaluator must return a mapping of metrics")

        actual_metric_names = set(raw_metrics)
        if actual_metric_names != expected_metric_names:
            missing = sorted(expected_metric_names - actual_metric_names)
            extra = sorted(actual_metric_names - expected_metric_names)
            raise DiscoveryContractError(
                f"metric set mismatch for {alternative.alternative_id!r}: "
                f"missing={missing}, extra={extra}"
            )

        ordered_metrics: list[tuple[str, Numeric]] = []
        for metric_name in manifest.metric_names:
            value = raw_metrics[metric_name]
            _validate_metric_value(value, metric_name=metric_name)
            ordered_metrics.append((metric_name, value))

        metric_mapping = dict(ordered_metrics)
        shortlisted = _is_shortlisted(manifest.shortlist_rule, metric_mapping)
        if shortlisted:
            shortlisted_ids.append(alternative.alternative_id)

        points.append(
            DiscoveryPoint(
                alternative_id=alternative.alternative_id,
                pattern_family=alternative.pattern_family,
                feature_condition=alternative.feature_condition,
                horizon=alternative.horizon,
                direction=alternative.direction,
                filter_regime=alternative.filter_regime,
                parameters=tuple(
                    (parameter.name, parameter.value) for parameter in alternative.parameters
                ),
                metrics=tuple(ordered_metrics),
                shortlisted=shortlisted,
            )
        )

    outcome = "SHORTLIST_FOR_IDEA_INTAKE" if shortlisted_ids else "NO_PATTERN_SHORTLISTED"
    return DiscoveryResult(
        search_id=manifest.search_id,
        dataset_id=manifest.dataset_id,
        dataset_version=manifest.dataset_version,
        metric_names=manifest.metric_names,
        search_space_count=len(manifest.alternatives),
        evaluated_alternatives=len(points),
        shortlisted_alternative_ids=tuple(shortlisted_ids),
        outcome=outcome,
        points=tuple(points),
    )


__all__ = [
    "DiscoveryAlternative",
    "DiscoveryContractError",
    "DiscoveryPoint",
    "DiscoveryResult",
    "Evaluator",
    "ParameterAssignment",
    "SearchManifest",
    "ShortlistOperator",
    "ShortlistRule",
    "load_search_manifest",
    "parse_search_manifest",
    "run_bounded_discovery",
]
