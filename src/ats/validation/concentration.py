"""Deterministic observation/group concentration analysis for ATS M4."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass

Numeric = int | float


class ConcentrationContractError(ValueError):
    """Raised when concentration inputs violate the declared M4 contract."""


def _finite_number(value: Numeric, *, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConcentrationContractError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ConcentrationContractError(f"{label} must be finite")
    return result


@dataclass(frozen=True, slots=True)
class Contribution:
    """One retained observation contribution and optional declared group."""

    observation_id: str
    value: Numeric
    group_id: str | None = None

    def __post_init__(self) -> None:
        if not self.observation_id:
            raise ConcentrationContractError("observation_id must be non-empty")
        _finite_number(self.value, label="contribution value")
        if self.group_id is not None and not self.group_id:
            raise ConcentrationContractError("group_id must be non-empty when provided")

    def to_dict(self) -> dict[str, object]:
        return {
            "group_id": self.group_id,
            "observation_id": self.observation_id,
            "value": self.value,
        }


@dataclass(frozen=True, slots=True)
class ConcentrationPlan:
    """Immutable predeclared concentration diagnostics."""

    plan_id: str
    top_counts: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.plan_id:
            raise ConcentrationContractError("plan_id must be non-empty")
        if not self.top_counts:
            raise ConcentrationContractError("top_counts must not be empty")
        if len(self.top_counts) != len(set(self.top_counts)):
            raise ConcentrationContractError("top_counts must contain unique values")
        for value in self.top_counts:
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ConcentrationContractError("top_counts must contain positive integers")


@dataclass(frozen=True, slots=True)
class TopConcentration:
    """Absolute contribution captured by one predeclared top-count diagnostic."""

    requested_count: int
    actual_count: int
    absolute_effect: float
    absolute_share: float | None

    def to_dict(self) -> dict[str, object]:
        return {
            "absolute_effect": self.absolute_effect,
            "absolute_share": self.absolute_share,
            "actual_count": self.actual_count,
            "requested_count": self.requested_count,
        }


@dataclass(frozen=True, slots=True)
class GroupContribution:
    """Complete declared group aggregation retained for review."""

    group_id: str
    observation_count: int
    signed_effect: float
    absolute_net_effect: float

    def to_dict(self) -> dict[str, object]:
        return {
            "absolute_net_effect": self.absolute_net_effect,
            "group_id": self.group_id,
            "observation_count": self.observation_count,
            "signed_effect": self.signed_effect,
        }


@dataclass(frozen=True, slots=True)
class ConcentrationResult:
    """Full concentration diagnostics without automatic observation exclusion."""

    plan_id: str
    observation_count: int
    total_effect: float
    total_absolute_effect: float
    observations: tuple[Contribution, ...]
    top_observations: tuple[TopConcentration, ...]
    groups: tuple[GroupContribution, ...]
    top_groups: tuple[TopConcentration, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "groups": [item.to_dict() for item in self.groups],
            "observation_count": self.observation_count,
            "observations": [item.to_dict() for item in self.observations],
            "plan_id": self.plan_id,
            "ranking_basis": "ABSOLUTE_MAGNITUDE_DIAGNOSTIC_ONLY",
            "removal_policy": "NO_AUTOMATIC_OUTLIER_REMOVAL",
            "schema_version": "m4-concentration-1",
            "top_groups": [item.to_dict() for item in self.top_groups],
            "top_observations": [item.to_dict() for item in self.top_observations],
            "total_absolute_effect": self.total_absolute_effect,
            "total_effect": self.total_effect,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )


def _top_concentration(
    magnitudes: tuple[float, ...],
    top_counts: tuple[int, ...],
) -> tuple[TopConcentration, ...]:
    denominator = math.fsum(magnitudes)
    result: list[TopConcentration] = []

    for requested_count in top_counts:
        actual_count = min(requested_count, len(magnitudes))
        absolute_effect = math.fsum(magnitudes[:actual_count])
        absolute_share = None
        if denominator > 0.0:
            absolute_share = absolute_effect / denominator
        result.append(
            TopConcentration(
                requested_count=requested_count,
                actual_count=actual_count,
                absolute_effect=absolute_effect,
                absolute_share=absolute_share,
            )
        )

    return tuple(result)


def analyze_concentration(
    plan: ConcentrationPlan,
    contributions: tuple[Contribution, ...],
) -> ConcentrationResult:
    """Expose concentration diagnostics while retaining every input observation."""

    if not contributions:
        raise ConcentrationContractError("contributions must not be empty")

    observation_ids = [item.observation_id for item in contributions]
    if len(observation_ids) != len(set(observation_ids)):
        raise ConcentrationContractError("observation_id values must be unique")

    values = tuple(_finite_number(item.value, label="contribution value") for item in contributions)
    total_effect = math.fsum(values)
    total_absolute_effect = math.fsum(abs(value) for value in values)

    ordered_observation_indices = sorted(
        range(len(contributions)),
        key=lambda index: (-abs(values[index]), index),
    )
    observation_magnitudes = tuple(abs(values[index]) for index in ordered_observation_indices)

    group_values: dict[str, list[float]] = {}
    group_counts: dict[str, int] = {}
    group_order: list[str] = []
    for item, value in zip(contributions, values, strict=True):
        if item.group_id is None:
            continue
        if item.group_id not in group_values:
            group_values[item.group_id] = []
            group_counts[item.group_id] = 0
            group_order.append(item.group_id)
        group_values[item.group_id].append(value)
        group_counts[item.group_id] += 1

    groups: list[GroupContribution] = []
    for group_id in group_order:
        signed_effect = math.fsum(group_values[group_id])
        groups.append(
            GroupContribution(
                group_id=group_id,
                observation_count=group_counts[group_id],
                signed_effect=signed_effect,
                absolute_net_effect=abs(signed_effect),
            )
        )

    ordered_group_indices = sorted(
        range(len(groups)),
        key=lambda index: (-groups[index].absolute_net_effect, index),
    )
    group_magnitudes = tuple(groups[index].absolute_net_effect for index in ordered_group_indices)

    return ConcentrationResult(
        plan_id=plan.plan_id,
        observation_count=len(contributions),
        total_effect=total_effect,
        total_absolute_effect=total_absolute_effect,
        observations=contributions,
        top_observations=_top_concentration(
            observation_magnitudes,
            plan.top_counts,
        ),
        groups=tuple(groups),
        top_groups=_top_concentration(group_magnitudes, plan.top_counts),
    )


__all__ = [
    "ConcentrationContractError",
    "ConcentrationPlan",
    "ConcentrationResult",
    "Contribution",
    "GroupContribution",
    "TopConcentration",
    "analyze_concentration",
]
