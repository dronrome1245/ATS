from __future__ import annotations

import json
from dataclasses import FrozenInstanceError

import pytest

from ats.validation.resampling import (
    ResamplingBlock,
    ResamplingContractError,
    ResamplingMethod,
    ResamplingPlan,
    run_block_resampling,
)


def fixture_plan() -> ResamplingPlan:
    return ResamplingPlan(
        plan_id="SYNTH-BLOCK-BOOTSTRAP-001",
        method=ResamplingMethod.BLOCK_BOOTSTRAP,
        block_semantics="synthetic dependent episode",
        repetitions=5,
        blocks_per_replicate=3,
        seed=17,
    )


def fixture_blocks() -> tuple[ResamplingBlock, ...]:
    return (
        ResamplingBlock(block_id="episode-a", values=(1.0, 2.0)),
        ResamplingBlock(block_id="episode-b", values=(10.0, 20.0, 30.0)),
        ResamplingBlock(block_id="episode-c", values=(-1.0, -2.0)),
    )


def test_repeated_block_resampling_is_exactly_deterministic() -> None:
    first = run_block_resampling(fixture_plan(), fixture_blocks())
    second = run_block_resampling(fixture_plan(), fixture_blocks())

    assert first == second
    assert first.to_json() == second.to_json()
    assert len(first.replicates) == 5


def test_source_block_identity_and_count_are_retained() -> None:
    result = run_block_resampling(fixture_plan(), fixture_blocks())

    assert result.source_block_ids == ("episode-a", "episode-b", "episode-c")
    assert result.source_observation_count == 7
    assert result.method is ResamplingMethod.BLOCK_BOOTSTRAP
    assert result.block_semantics == "synthetic dependent episode"


def test_each_selected_block_is_preserved_whole_and_in_order() -> None:
    blocks = fixture_blocks()
    source = {block.block_id: block.values for block in blocks}
    result = run_block_resampling(fixture_plan(), blocks)

    for replicate in result.replicates:
        rebuilt = tuple(
            value for block_id in replicate.selected_block_ids for value in source[block_id]
        )
        assert replicate.values == rebuilt


def test_serialization_declares_no_iid_fallback() -> None:
    result = run_block_resampling(fixture_plan(), fixture_blocks())
    decoded = json.loads(result.to_json())

    assert decoded["assumption_policy"] == "DECLARED_BLOCKS_PRESERVED"
    assert decoded["method"] == "BLOCK_BOOTSTRAP"
    assert "IID" not in decoded["method"]
    assert decoded["seed"] == 17
    assert len(decoded["replicates"]) == 5


def test_duplicate_block_ids_are_rejected() -> None:
    with pytest.raises(
        ResamplingContractError,
        match="block_id values must be unique",
    ):
        run_block_resampling(
            fixture_plan(),
            (
                ResamplingBlock(block_id="same", values=(1.0,)),
                ResamplingBlock(block_id="same", values=(2.0,)),
            ),
        )


def test_empty_or_non_finite_blocks_are_rejected() -> None:
    with pytest.raises(ResamplingContractError, match="must not be empty"):
        ResamplingBlock(block_id="empty", values=())

    with pytest.raises(ResamplingContractError, match="must be finite"):
        ResamplingBlock(block_id="bad", values=(float("nan"),))


def test_plan_requires_explicit_positive_shape_and_seed() -> None:
    with pytest.raises(ResamplingContractError, match="repetitions must be positive"):
        ResamplingPlan(
            plan_id="BAD",
            method=ResamplingMethod.BLOCK_BOOTSTRAP,
            block_semantics="synthetic",
            repetitions=0,
            blocks_per_replicate=1,
            seed=1,
        )

    with pytest.raises(
        ResamplingContractError,
        match="blocks_per_replicate must be positive",
    ):
        ResamplingPlan(
            plan_id="BAD",
            method=ResamplingMethod.BLOCK_BOOTSTRAP,
            block_semantics="synthetic",
            repetitions=1,
            blocks_per_replicate=0,
            seed=1,
        )


def test_no_implicit_method_or_empty_block_set() -> None:
    with pytest.raises(ResamplingContractError, match="blocks must not be empty"):
        run_block_resampling(fixture_plan(), ())

    with pytest.raises(ResamplingContractError, match="must use ResamplingMethod"):
        ResamplingPlan(
            plan_id="BAD",
            method="IID_BOOTSTRAP",  # type: ignore[arg-type]
            block_semantics="synthetic",
            repetitions=1,
            blocks_per_replicate=1,
            seed=1,
        )


def test_plan_and_result_are_immutable() -> None:
    plan = fixture_plan()
    result = run_block_resampling(plan, fixture_blocks())

    with pytest.raises(FrozenInstanceError):
        plan.plan_id = "OTHER"

    with pytest.raises(FrozenInstanceError):
        result.plan_id = "OTHER"
