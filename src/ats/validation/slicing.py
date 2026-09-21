"""Deterministic declared time/regime slicing for ATS M4."""

from __future__ import annotations

import json
import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import TypeVar

ObservationT = TypeVar("ObservationT")
Numeric = int | float
SliceAssigner = Callable[[ObservationT], tuple[str, ...]]
SliceEvaluator = Callable[[tuple[ObservationT, ...]], Mapping[str, Numeric]]


class SlicingContractError(ValueError):
    """Raised when a declared slicing plan or evaluation violates the contract."""


class EmptySlicePolicy(StrEnum):
    """Declared handling for a slice with zero assigned observations."""

    INCLUDE = "INCLUDE"
    REJECT = "REJECT"


@dataclass(frozen=True, slots=True)
class SliceDefinition:
    """One predeclared time/regime slice."""

    slice_id: str
    label: str

    def __post_init__(self) -> None:
        if not self.slice_id:
            raise SlicingContractError("slice_id must be non-empty")
        if not self.label:
            raise SlicingContractError("slice label must be non-empty")


@dataclass(frozen=True, slots=True)
class SlicePlan:
    """Immutable slicing plan declared before inspecting slice results."""

    plan_id: str
    slices: tuple[SliceDefinition, ...]
    metric_names: tuple[str, ...]
    require_exhaustive: bool = True
    allow_overlap: bool = False
    empty_slice_policy: EmptySlicePolicy = EmptySlicePolicy.INCLUDE

    def __post_init__(self) -> None:
        if not self.plan_id:
            raise SlicingContractError("plan_id must be non-empty")
        if not self.slices:
            raise SlicingContractError("slices must not be empty")
        slice_ids = tuple(item.slice_id for item in self.slices)
        if len(slice_ids) != len(set(slice_ids)):
            raise SlicingContractError("slice_id values must be unique")
        if not self.metric_names:
            raise SlicingContractError("metric_names must not be empty")
        if any(not name for name in self.metric_names):
            raise SlicingContractError("metric_names must contain non-empty names")
        if len(self.metric_names) != len(set(self.metric_names)):
            raise SlicingContractError("metric_names must contain unique names")
        if not isinstance(self.empty_slice_policy, EmptySlicePolicy):
            raise SlicingContractError("empty_slice_policy must use EmptySlicePolicy")


@dataclass(frozen=True, slots=True)
class SlicePoint:
    """One declared slice result retained in plan order."""

    slice_id: str
    label: str
    observation_count: int
    metrics: tuple[tuple[str, Numeric], ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "label": self.label,
            "metrics": dict(self.metrics),
            "observation_count": self.observation_count,
            "slice_id": self.slice_id,
        }


@dataclass(frozen=True, slots=True)
class SliceResult:
    """Complete declared slice set plus coverage/overlap diagnostics."""

    plan_id: str
    observation_count: int
    unassigned_observation_count: int
    multiply_assigned_observation_count: int
    slices: tuple[SlicePoint, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "multiply_assigned_observation_count": self.multiply_assigned_observation_count,
            "observation_count": self.observation_count,
            "plan_id": self.plan_id,
            "reporting_policy": "ALL_DECLARED_SLICES_REPORTED",
            "schema_version": "m4-slicing-1",
            "slices": [item.to_dict() for item in self.slices],
            "unassigned_observation_count": self.unassigned_observation_count,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )


def _validate_metric_value(value: Numeric, *, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SlicingContractError(f"metric {name!r} must be numeric")
    if isinstance(value, float) and not math.isfinite(value):
        raise SlicingContractError(f"metric {name!r} must be finite")


def evaluate_declared_slices(
    plan: SlicePlan,
    observations: Sequence[ObservationT],
    assigner: SliceAssigner[ObservationT],
    evaluator: SliceEvaluator[ObservationT],
) -> SliceResult:
    """Evaluate every declared slice without selective omission or reranking."""

    if not callable(assigner):
        raise TypeError("assigner must be callable")
    if not callable(evaluator):
        raise TypeError("evaluator must be callable")

    declared = {item.slice_id: item for item in plan.slices}
    buckets: dict[str, list[ObservationT]] = {item.slice_id: [] for item in plan.slices}
    unassigned = 0
    multiply_assigned = 0

    for observation in observations:
        memberships = assigner(observation)
        if not isinstance(memberships, tuple):
            raise SlicingContractError("assigner must return a tuple of slice_ids")
        if len(memberships) != len(set(memberships)):
            raise SlicingContractError("one observation cannot repeat the same slice_id")

        unknown = sorted(set(memberships) - set(declared))
        if unknown:
            raise SlicingContractError(f"assigner returned unknown slice_ids: {unknown}")

        if not memberships:
            unassigned += 1
            if plan.require_exhaustive:
                raise SlicingContractError("require_exhaustive plan has an unassigned observation")
        if len(memberships) > 1:
            multiply_assigned += 1
            if not plan.allow_overlap:
                raise SlicingContractError(
                    "overlap is not allowed but observation has multiple slice_ids"
                )

        for slice_id in memberships:
            buckets[slice_id].append(observation)

    points: list[SlicePoint] = []
    expected_metric_names = set(plan.metric_names)

    for definition in plan.slices:
        items = tuple(buckets[definition.slice_id])
        if not items and plan.empty_slice_policy is EmptySlicePolicy.REJECT:
            raise SlicingContractError(
                f"slice {definition.slice_id!r} is empty under REJECT policy"
            )

        raw_metrics = evaluator(items)
        if not isinstance(raw_metrics, Mapping):
            raise SlicingContractError("evaluator must return a mapping of metrics")
        actual_metric_names = set(raw_metrics)
        if actual_metric_names != expected_metric_names:
            missing = sorted(expected_metric_names - actual_metric_names)
            extra = sorted(actual_metric_names - expected_metric_names)
            raise SlicingContractError(
                f"metric set mismatch for {definition.slice_id!r}: missing={missing}, extra={extra}"
            )

        metrics: list[tuple[str, Numeric]] = []
        for name in plan.metric_names:
            value = raw_metrics[name]
            _validate_metric_value(value, name=name)
            metrics.append((name, value))

        points.append(
            SlicePoint(
                slice_id=definition.slice_id,
                label=definition.label,
                observation_count=len(items),
                metrics=tuple(metrics),
            )
        )

    return SliceResult(
        plan_id=plan.plan_id,
        observation_count=len(observations),
        unassigned_observation_count=unassigned,
        multiply_assigned_observation_count=multiply_assigned,
        slices=tuple(points),
    )


__all__ = [
    "EmptySlicePolicy",
    "SliceAssigner",
    "SliceDefinition",
    "SliceEvaluator",
    "SlicePlan",
    "SlicePoint",
    "SliceResult",
    "SlicingContractError",
    "evaluate_declared_slices",
]
