"""Deterministic dependence-preserving block resampling for ATS M4."""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from enum import StrEnum

Numeric = int | float


class ResamplingContractError(ValueError):
    """Raised when a resampling plan or declared block violates the M4 contract."""


class ResamplingMethod(StrEnum):
    """Supported resampling mechanics with explicit dependence semantics."""

    BLOCK_BOOTSTRAP = "BLOCK_BOOTSTRAP"


@dataclass(frozen=True, slots=True)
class ResamplingBlock:
    """One declared dependence block whose internal order is preserved."""

    block_id: str
    values: tuple[Numeric, ...]

    def __post_init__(self) -> None:
        if not self.block_id:
            raise ResamplingContractError("block_id must be non-empty")
        if not self.values:
            raise ResamplingContractError("block values must not be empty")
        for value in self.values:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ResamplingContractError("block values must be numeric")
            if isinstance(value, float) and not math.isfinite(value):
                raise ResamplingContractError("block values must be finite")


@dataclass(frozen=True, slots=True)
class ResamplingPlan:
    """Immutable resampling assumptions declared before result inspection."""

    plan_id: str
    method: ResamplingMethod
    block_semantics: str
    repetitions: int
    blocks_per_replicate: int
    seed: int

    def __post_init__(self) -> None:
        if not self.plan_id:
            raise ResamplingContractError("plan_id must be non-empty")
        if not isinstance(self.method, ResamplingMethod):
            raise ResamplingContractError("method must use ResamplingMethod")
        if not self.block_semantics:
            raise ResamplingContractError("block_semantics must be non-empty")
        if isinstance(self.repetitions, bool) or not isinstance(self.repetitions, int):
            raise ResamplingContractError("repetitions must be an integer")
        if self.repetitions <= 0:
            raise ResamplingContractError("repetitions must be positive")
        if isinstance(self.blocks_per_replicate, bool) or not isinstance(
            self.blocks_per_replicate, int
        ):
            raise ResamplingContractError("blocks_per_replicate must be an integer")
        if self.blocks_per_replicate <= 0:
            raise ResamplingContractError("blocks_per_replicate must be positive")
        if isinstance(self.seed, bool) or not isinstance(self.seed, int):
            raise ResamplingContractError("seed must be an integer")


@dataclass(frozen=True, slots=True)
class ResamplingReplicate:
    """One deterministic replicate with complete selected-block trace."""

    replicate_index: int
    selected_block_ids: tuple[str, ...]
    values: tuple[Numeric, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "replicate_index": self.replicate_index,
            "selected_block_ids": list(self.selected_block_ids),
            "values": list(self.values),
        }


@dataclass(frozen=True, slots=True)
class ResamplingResult:
    """Complete resampling trace; no IID fallback or hidden block splitting."""

    plan_id: str
    method: ResamplingMethod
    block_semantics: str
    seed: int
    source_block_ids: tuple[str, ...]
    source_observation_count: int
    replicates: tuple[ResamplingReplicate, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "assumption_policy": "DECLARED_BLOCKS_PRESERVED",
            "block_semantics": self.block_semantics,
            "method": self.method.value,
            "plan_id": self.plan_id,
            "replicates": [item.to_dict() for item in self.replicates],
            "schema_version": "m4-resampling-1",
            "seed": self.seed,
            "source_block_ids": list(self.source_block_ids),
            "source_observation_count": self.source_observation_count,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )


def run_block_resampling(
    plan: ResamplingPlan,
    blocks: tuple[ResamplingBlock, ...],
) -> ResamplingResult:
    """Resample whole declared blocks with replacement and preserve internal order."""

    if plan.method is not ResamplingMethod.BLOCK_BOOTSTRAP:
        raise ResamplingContractError("unsupported resampling method")
    if not blocks:
        raise ResamplingContractError("blocks must not be empty")

    block_ids = tuple(block.block_id for block in blocks)
    if len(block_ids) != len(set(block_ids)):
        raise ResamplingContractError("block_id values must be unique")

    rng = random.Random(plan.seed)
    replicates: list[ResamplingReplicate] = []

    for replicate_index in range(plan.repetitions):
        selected_indices = tuple(
            rng.randrange(len(blocks)) for _ in range(plan.blocks_per_replicate)
        )
        selected_blocks = tuple(blocks[index] for index in selected_indices)
        selected_block_ids = tuple(block.block_id for block in selected_blocks)
        values = tuple(value for block in selected_blocks for value in block.values)
        replicates.append(
            ResamplingReplicate(
                replicate_index=replicate_index,
                selected_block_ids=selected_block_ids,
                values=values,
            )
        )

    return ResamplingResult(
        plan_id=plan.plan_id,
        method=plan.method,
        block_semantics=plan.block_semantics,
        seed=plan.seed,
        source_block_ids=block_ids,
        source_observation_count=sum(len(block.values) for block in blocks),
        replicates=tuple(replicates),
    )


__all__ = [
    "ResamplingBlock",
    "ResamplingContractError",
    "ResamplingMethod",
    "ResamplingPlan",
    "ResamplingReplicate",
    "ResamplingResult",
    "run_block_resampling",
]
