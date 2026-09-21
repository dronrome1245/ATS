from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import FrozenInstanceError

import pytest

from ats.validation.slicing import (
    EmptySlicePolicy,
    SliceDefinition,
    SlicePlan,
    SlicingContractError,
    evaluate_declared_slices,
)


def plan(
    *,
    require_exhaustive: bool = True,
    allow_overlap: bool = False,
    empty_slice_policy: EmptySlicePolicy = EmptySlicePolicy.INCLUDE,
) -> SlicePlan:
    return SlicePlan(
        plan_id="SYNTH-SLICING-001",
        slices=(
            SliceDefinition(slice_id="early", label="Early block"),
            SliceDefinition(slice_id="late", label="Late block"),
            SliceDefinition(slice_id="unused", label="Declared empty block"),
        ),
        metric_names=("count", "sum"),
        require_exhaustive=require_exhaustive,
        allow_overlap=allow_overlap,
        empty_slice_policy=empty_slice_policy,
    )


def exclusive_assigner(value: int) -> tuple[str, ...]:
    return ("early",) if value < 3 else ("late",)


def metrics(items: Sequence[int]) -> dict[str, int | float]:
    return {"sum": sum(items), "count": len(items)}


def test_every_declared_slice_is_reported_in_plan_order() -> None:
    result = evaluate_declared_slices(
        plan(),
        (1, 2, 3, 4),
        exclusive_assigner,
        metrics,
    )

    assert tuple(item.slice_id for item in result.slices) == (
        "early",
        "late",
        "unused",
    )
    assert result.slices[0].observation_count == 2
    assert result.slices[0].metrics == (("count", 2), ("sum", 3))
    assert result.slices[1].metrics == (("count", 2), ("sum", 7))
    assert result.slices[2].observation_count == 0
    assert result.slices[2].metrics == (("count", 0), ("sum", 0))


def test_serialization_is_deterministic_and_declares_reporting_policy() -> None:
    first = evaluate_declared_slices(
        plan(),
        (1, 2, 3, 4),
        exclusive_assigner,
        metrics,
    )
    second = evaluate_declared_slices(
        plan(),
        (1, 2, 3, 4),
        exclusive_assigner,
        metrics,
    )

    assert first.to_json() == second.to_json()
    decoded = json.loads(first.to_json())
    assert decoded["reporting_policy"] == "ALL_DECLARED_SLICES_REPORTED"
    assert [item["slice_id"] for item in decoded["slices"]] == [
        "early",
        "late",
        "unused",
    ]


def test_unassigned_observation_is_blocking_when_exhaustive() -> None:
    with pytest.raises(
        SlicingContractError,
        match="unassigned observation",
    ):
        evaluate_declared_slices(
            plan(),
            (1, 2, 3),
            lambda value: () if value == 2 else exclusive_assigner(value),
            metrics,
        )


def test_non_exhaustive_plan_counts_unassigned_observations() -> None:
    result = evaluate_declared_slices(
        plan(require_exhaustive=False),
        (1, 2, 3),
        lambda value: () if value == 2 else exclusive_assigner(value),
        metrics,
    )

    assert result.unassigned_observation_count == 1
    assert result.observation_count == 3


def test_overlap_is_blocked_unless_explicitly_allowed() -> None:
    def overlapping(value: int) -> tuple[str, ...]:
        if value == 2:
            return ("early", "late")
        return exclusive_assigner(value)

    with pytest.raises(SlicingContractError, match="overlap is not allowed"):
        evaluate_declared_slices(
            plan(),
            (1, 2, 3),
            overlapping,
            metrics,
        )

    result = evaluate_declared_slices(
        plan(allow_overlap=True),
        (1, 2, 3),
        overlapping,
        metrics,
    )
    assert result.multiply_assigned_observation_count == 1


def test_unknown_or_duplicate_membership_is_rejected() -> None:
    with pytest.raises(SlicingContractError, match="unknown slice_ids"):
        evaluate_declared_slices(
            plan(),
            (1,),
            lambda _value: ("unknown",),
            metrics,
        )

    with pytest.raises(SlicingContractError, match="repeat the same slice_id"):
        evaluate_declared_slices(
            plan(allow_overlap=True),
            (1,),
            lambda _value: ("early", "early"),
            metrics,
        )


def test_empty_slice_policy_can_reject_declared_empty_slice() -> None:
    with pytest.raises(SlicingContractError, match="empty under REJECT policy"):
        evaluate_declared_slices(
            plan(empty_slice_policy=EmptySlicePolicy.REJECT),
            (1, 2, 3, 4),
            exclusive_assigner,
            metrics,
        )


def test_metric_contract_and_finite_values_fail_closed() -> None:
    with pytest.raises(SlicingContractError, match="metric set mismatch"):
        evaluate_declared_slices(
            plan(),
            (1, 2, 3),
            exclusive_assigner,
            lambda _items: {"count": 1},
        )

    with pytest.raises(SlicingContractError, match="must be finite"):
        evaluate_declared_slices(
            plan(),
            (1, 2, 3),
            exclusive_assigner,
            lambda _items: {"count": 1, "sum": float("nan")},
        )


def test_assigner_must_return_tuple() -> None:
    with pytest.raises(SlicingContractError, match="must return a tuple"):
        evaluate_declared_slices(
            plan(),
            (1,),
            lambda _value: ["early"],  # type: ignore[return-value]
            metrics,
        )


def test_plan_and_result_are_immutable() -> None:
    slicing_plan = plan()
    result = evaluate_declared_slices(
        slicing_plan,
        (1, 2, 3, 4),
        exclusive_assigner,
        metrics,
    )

    with pytest.raises(FrozenInstanceError):
        slicing_plan.plan_id = "OTHER"

    with pytest.raises(FrozenInstanceError):
        result.plan_id = "OTHER"
