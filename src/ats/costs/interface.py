"""Explicit deterministic cost-model contracts for ATS M2."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, runtime_checkable

JsonScalar = str | int | float | bool | None


def _validate_pairs(
    pairs: tuple[tuple[str, JsonScalar], ...],
    *,
    label: str,
) -> None:
    names: set[str] = set()
    for name, value in pairs:
        if not name:
            raise ValueError(f"{label} key must be non-empty")
        if name in names:
            raise ValueError(f"{label} contains duplicate key: {name}")
        names.add(name)
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(f"{label} float values must be finite")


def _pairs_to_dict(pairs: tuple[tuple[str, JsonScalar], ...]) -> dict[str, JsonScalar]:
    return dict(pairs)


class CostApplicability(StrEnum):
    """Explicit applicability state for one modeled cost component."""

    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class CostContractError(ValueError):
    """Raised when a cost model violates the explicit M2 contract."""


@dataclass(frozen=True, slots=True)
class CostComponentConfig:
    """Declared assumptions for one named cost component."""

    name: str
    applicability: CostApplicability
    parameters: tuple[tuple[str, JsonScalar], ...] = ()
    reason: str | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("cost component name must be non-empty")
        if not isinstance(self.applicability, CostApplicability):
            raise ValueError("cost component applicability must use CostApplicability")
        _validate_pairs(self.parameters, label=f"cost component {self.name!r} parameters")

        if self.applicability is CostApplicability.APPLICABLE:
            if not self.parameters:
                raise ValueError("applicable cost component must declare explicit parameters")
        else:
            if self.parameters:
                raise ValueError("not-applicable cost component cannot declare parameters")
            if not self.reason:
                raise ValueError("not-applicable cost component must declare a reason")

    def to_dict(self) -> dict[str, object]:
        return {
            "applicability": self.applicability.value,
            "name": self.name,
            "parameters": _pairs_to_dict(self.parameters),
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class CostModelConfig:
    """Complete explicit cost configuration supplied to one model evaluation."""

    components: tuple[CostComponentConfig, ...]

    def __post_init__(self) -> None:
        if not self.components:
            raise ValueError("cost model config must declare at least one component")
        names = [component.name for component in self.components]
        if len(names) != len(set(names)):
            raise ValueError("cost model config component names must be unique")

    def to_dict(self) -> dict[str, object]:
        return {"components": [component.to_dict() for component in self.components]}

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )


@dataclass(frozen=True, slots=True)
class CostInput:
    """Deterministic model input kept outside Strategy logic and gross results."""

    reference_id: str
    attributes: tuple[tuple[str, JsonScalar], ...] = ()

    def __post_init__(self) -> None:
        if not self.reference_id:
            raise ValueError("cost input reference_id must be non-empty")
        _validate_pairs(self.attributes, label="cost input attributes")

    def to_dict(self) -> dict[str, object]:
        return {
            "attributes": _pairs_to_dict(self.attributes),
            "reference_id": self.reference_id,
        }


@dataclass(frozen=True, slots=True)
class CostComponentResult:
    """Modeled contribution from one configured cost component."""

    name: str
    applicability: CostApplicability
    value: float | int | None = None
    unit: str | None = None
    details: tuple[tuple[str, JsonScalar], ...] = ()

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("cost result component name must be non-empty")
        if not isinstance(self.applicability, CostApplicability):
            raise ValueError("cost result applicability must use CostApplicability")
        _validate_pairs(self.details, label=f"cost result {self.name!r} details")

        if self.applicability is CostApplicability.APPLICABLE:
            if self.value is None:
                raise ValueError("applicable cost result must declare a value")
            if isinstance(self.value, bool) or not isinstance(self.value, (int, float)):
                raise ValueError("cost result value must be numeric")
            if isinstance(self.value, float) and not math.isfinite(self.value):
                raise ValueError("cost result value must be finite")
            if not self.unit:
                raise ValueError("applicable cost result must declare a unit")
        else:
            if self.value is not None or self.unit is not None:
                raise ValueError("not-applicable cost result cannot declare value or unit")

    def to_dict(self) -> dict[str, object]:
        return {
            "applicability": self.applicability.value,
            "details": _pairs_to_dict(self.details),
            "name": self.name,
            "unit": self.unit,
            "value": self.value,
        }


@dataclass(frozen=True, slots=True)
class CostResult:
    """Serializable cost-only result with no gross/net performance fields."""

    reference_id: str
    components: tuple[CostComponentResult, ...]

    def __post_init__(self) -> None:
        if not self.reference_id:
            raise ValueError("cost result reference_id must be non-empty")
        if not self.components:
            raise ValueError("cost result must contain configured components")
        names = [component.name for component in self.components]
        if len(names) != len(set(names)):
            raise ValueError("cost result component names must be unique")

    def to_dict(self) -> dict[str, object]:
        return {
            "components": [component.to_dict() for component in self.components],
            "reference_id": self.reference_id,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )


@runtime_checkable
class CostModel(Protocol):
    """Deterministic model consuming only explicit cost input and configuration."""

    def evaluate(self, cost_input: CostInput, config: CostModelConfig) -> CostResult:
        """Return the modeled cost components for one explicit input."""


def apply_cost_model(
    cost_input: CostInput,
    config: CostModelConfig,
    model: CostModel,
) -> CostResult:
    """Evaluate and validate one explicit deterministic cost-model boundary."""

    result = model.evaluate(cost_input, config)
    if not isinstance(result, CostResult):
        raise CostContractError("cost model evaluate must return CostResult")
    if result.reference_id != cost_input.reference_id:
        raise CostContractError("cost result reference_id must match cost input")

    configured_names = tuple(component.name for component in config.components)
    result_names = tuple(component.name for component in result.components)
    if result_names != configured_names:
        raise CostContractError("cost result components must exactly match configured order")

    for configured, observed in zip(config.components, result.components, strict=True):
        if observed.applicability is not configured.applicability:
            raise CostContractError(
                f"cost result applicability must match config for component: {configured.name}"
            )

    return result
