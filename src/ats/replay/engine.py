"""Minimal deterministic replay engine for ATS M2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from ats.data.loader import LoadedDataset
from ats.strategy.interface import (
    ResearchDecision,
    ResearchDiagnostic,
    ResearchObservation,
    ResearchRunContext,
    ResearchStrategy,
    StrategyStep,
    observation_from_loaded_record,
)

StateT = TypeVar("StateT")


class ReplayContractError(ValueError):
    """Raised when replay inputs or strategy output violate the M2 contract."""


@dataclass(frozen=True, slots=True)
class ReplayFrame(Generic[StateT]):
    """Immutable trace entry for one processed observation."""

    observation: ResearchObservation
    state_before: StateT
    state_after: StateT
    decisions: tuple[ResearchDecision, ...]
    diagnostics: tuple[ResearchDiagnostic, ...]


@dataclass(frozen=True, slots=True)
class ReplayResult(Generic[StateT]):
    """Immutable deterministic replay result before costs or analytics."""

    dataset_id: str
    dataset_version: str
    source_location: str
    computed_sha256: str
    context: ResearchRunContext
    initial_state: StateT
    final_state: StateT
    frames: tuple[ReplayFrame[StateT], ...]

    @property
    def observation_count(self) -> int:
        return len(self.frames)

    @property
    def decisions(self) -> tuple[ResearchDecision, ...]:
        return tuple(decision for frame in self.frames for decision in frame.decisions)

    @property
    def diagnostics(self) -> tuple[ResearchDiagnostic, ...]:
        return tuple(diagnostic for frame in self.frames for diagnostic in frame.diagnostics)


def _validate_step(
    step: StrategyStep[StateT],
    *,
    observation: ResearchObservation,
) -> None:
    if not isinstance(step, StrategyStep):
        raise ReplayContractError("strategy on_observation must return StrategyStep")

    for decision in step.decisions:
        if decision.decision_time < observation.availability_time:
            raise ReplayContractError(
                "decision_time cannot be earlier than current observation availability_time"
            )


def run_replay(
    dataset: LoadedDataset,
    context: ResearchRunContext,
    strategy: ResearchStrategy[StateT],
) -> ReplayResult[StateT]:
    """Replay one finite loaded dataset through one research strategy deterministically."""

    state = strategy.initial_state(context)
    initial_state = state
    frames: list[ReplayFrame[StateT]] = []
    previous_availability = None

    for sequence_index, record in enumerate(dataset.records):
        observation = observation_from_loaded_record(
            record,
            sequence_index=sequence_index,
        )

        if (
            previous_availability is not None
            and observation.availability_time < previous_availability
        ):
            raise ReplayContractError(
                "availability_time must be nondecreasing in the loaded replay stream"
            )

        step = strategy.on_observation(context, observation, state)
        _validate_step(step, observation=observation)

        frames.append(
            ReplayFrame(
                observation=observation,
                state_before=state,
                state_after=step.state,
                decisions=step.decisions,
                diagnostics=step.diagnostics,
            )
        )
        state = step.state
        previous_availability = observation.availability_time

    return ReplayResult(
        dataset_id=dataset.dataset_id,
        dataset_version=dataset.dataset_version,
        source_location=dataset.source_location,
        computed_sha256=dataset.computed_sha256,
        context=context,
        initial_state=initial_state,
        final_state=state,
        frames=tuple(frames),
    )
