"""Deterministic predefined parameter-sensitivity evaluation for ATS M4."""

from __future__ import annotations

import json
import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MappingProxyType

JsonScalar = str | int | float | bool | None
Numeric = int | float
Evaluator = Callable[[Mapping[str, JsonScalar]], Mapping[str, Numeric]]


class SensitivityContractError(ValueError):
    """Raised when a sensitivity plan or evaluator violates the M4 contract."""


def _validate_name(value: str, *, label: str) -> None:
    if not value:
        raise SensitivityContractError(f"{label} must be non-empty")


def _validate_parameter_value(value: JsonScalar) -> None:
    if value is not None and not isinstance(value, (str, int, float, bool)):
        raise SensitivityContractError("parameter values must be JSON scalars")
    if isinstance(value, float) and not math.isfinite(value):
        raise SensitivityContractError("parameter values must be finite")


def _validate_metric_value(value: Numeric, *, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SensitivityContractError(f"metric {name!r} must be numeric")
    if isinstance(value, float) and not math.isfinite(value):
        raise SensitivityContractError(f"metric {name!r} must be finite")


def _validate_unique_names(names: tuple[str, ...], *, label: str) -> None:
    if not names:
        raise SensitivityContractError(f"{label} must not be empty")
    if any(not name for name in names):
        raise SensitivityContractError(f"{label} must contain non-empty names")
    if len(names) != len(set(names)):
        raise SensitivityContractError(f"{label} must contain unique names")


@dataclass(frozen=True, slots=True)
class ParameterVariant:
    """One explicitly declared point in a sensitivity neighbourhood."""

    variant_id: str
    values: tuple[JsonScalar, ...]

    def __post_init__(self) -> None:
        _validate_name(self.variant_id, label="variant_id")
        for value in self.values:
            _validate_parameter_value(value)


@dataclass(frozen=True, slots=True)
class SensitivityPlan:
    """Immutable ordered sensitivity plan defined before result inspection."""

    plan_id: str
    parameter_names: tuple[str, ...]
    metric_names: tuple[str, ...]
    variants: tuple[ParameterVariant, ...]

    def __post_init__(self) -> None:
        _validate_name(self.plan_id, label="plan_id")
        _validate_unique_names(self.parameter_names, label="parameter_names")
        _validate_unique_names(self.metric_names, label="metric_names")
        if not self.variants:
            raise SensitivityContractError("variants must not be empty")

        variant_ids = [variant.variant_id for variant in self.variants]
        if len(variant_ids) != len(set(variant_ids)):
            raise SensitivityContractError("variant_id values must be unique")

        expected = len(self.parameter_names)
        for variant in self.variants:
            if len(variant.values) != expected:
                raise SensitivityContractError(
                    f"variant {variant.variant_id!r} must provide "
                    f"{expected} parameter values"
                )


@dataclass(frozen=True, slots=True)
class SensitivityPoint:
    """One evaluated parameter point with ordered parameters and metrics."""

    variant_id: str
    parameters: tuple[tuple[str, JsonScalar], ...]
    metrics: tuple[tuple[str, Numeric], ...]

    def __post_init__(self) -> None:
        _validate_name(self.variant_id, label="variant_id")
        parameter_names = tuple(name for name, _ in self.parameters)
        metric_names = tuple(name for name, _ in self.metrics)
        _validate_unique_names(parameter_names, label="point parameter names")
        _validate_unique_names(metric_names, label="point metric names")
        for _, value in self.parameters:
            _validate_parameter_value(value)
        for name, value in self.metrics:
            _validate_metric_value(value, name=name)

    def to_dict(self) -> dict[str, object]:
        return {
            "metrics": dict(self.metrics),
            "parameters": dict(self.parameters),
            "variant_id": self.variant_id,
        }


@dataclass(frozen=True, slots=True)
class SensitivityResult:
    """Full ordered sensitivity region with no automatic ranking or winner."""

    plan_id: str
    parameter_names: tuple[str, ...]
    metric_names: tuple[str, ...]
    points: tuple[SensitivityPoint, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "metric_names": list(self.metric_names),
            "parameter_names": list(self.parameter_names),
            "plan_id": self.plan_id,
            "points": [point.to_dict() for point in self.points],
            "schema_version": "m4-sensitivity-1",
            "selection_policy": "NO_AUTOMATIC_SELECTION",
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )


def evaluate_parameter_sensitivity(
    plan: SensitivityPlan,
    evaluator: Evaluator,
) -> SensitivityResult:
    """Evaluate every predefined variant in order without ranking or selection."""

    if not callable(evaluator):
        raise TypeError("evaluator must be callable")

    points: list[SensitivityPoint] = []
    expected_metric_names = set(plan.metric_names)

    for variant in plan.variants:
        parameters = tuple(zip(plan.parameter_names, variant.values, strict=True))
        readonly_parameters = MappingProxyType(dict(parameters))
        raw_metrics = evaluator(readonly_parameters)

        if not isinstance(raw_metrics, Mapping):
            raise SensitivityContractError(
                "evaluator must return a mapping of metrics"
            )

        actual_metric_names = set(raw_metrics)
        if actual_metric_names != expected_metric_names:
            missing = sorted(expected_metric_names - actual_metric_names)
            extra = sorted(actual_metric_names - expected_metric_names)
            raise SensitivityContractError(
                f"metric set mismatch for {variant.variant_id!r}: "
                f"missing={missing}, extra={extra}"
            )

        metrics: list[tuple[str, Numeric]] = []
        for name in plan.metric_names:
            value = raw_metrics[name]
            _validate_metric_value(value, name=name)
            metrics.append((name, value))

        points.append(
            SensitivityPoint(
                variant_id=variant.variant_id,
                parameters=parameters,
                metrics=tuple(metrics),
            )
        )

    return SensitivityResult(
        plan_id=plan.plan_id,
        parameter_names=plan.parameter_names,
        metric_names=plan.metric_names,
        points=tuple(points),
    )


__all__ = [
    "Evaluator",
    "ParameterVariant",
    "SensitivityContractError",
    "SensitivityPlan",
    "SensitivityPoint",
    "SensitivityResult",
    "evaluate_parameter_sensitivity",
]
