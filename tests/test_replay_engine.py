from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from ats.data.loader import LoadedDataset, LoadedRecord, load_dataset
from ats.replay.engine import ReplayContractError, ReplayResult, run_replay
from ats.schemas.dataset_manifest import MissingPolicy, load_dataset_manifest
from ats.strategy.interface import (
    ResearchDecision,
    ResearchDiagnostic,
    ResearchObservation,
    ResearchRunContext,
    ResearchStrategy,
    StrategyStep,
)


ROOT = Path(__file__).resolve().parents[1]
LOADER_MANIFEST = ROOT / "tests" / "fixtures" / "datasets" / "ordered_events.manifest.yaml"


@dataclass(frozen=True, slots=True)
class CounterState:
    count: int = 0


class CountingStrategy(ResearchStrategy[CounterState]):
    def __init__(self) -> None:
        self.initial_calls = 0
        self.observation_calls = 0

    def initial_state(self, context: ResearchRunContext) -> CounterState:
        self.initial_calls += 1
        start = dict(context.parameters).get("start", 0)
        assert isinstance(start, int)
        return CounterState(start)

    def on_observation(
        self,
        context: ResearchRunContext,
        observation: ResearchObservation,
        state: CounterState,
    ) -> StrategyStep[CounterState]:
        self.observation_calls += 1
        next_state = CounterState(state.count + 1)
        return StrategyStep(
            state=next_state,
            decisions=(
                ResearchDecision(
                    decision_type="FIXTURE",
                    decision_time=observation.availability_time,
                    payload=(
                        ("sequence", observation.sequence_index),
                        ("value", observation.value("value")),
                    ),
                ),
            ),
            diagnostics=(
                ResearchDiagnostic(
                    code="COUNT",
                    message="fixture observation processed",
                    details=(("count", next_state.count),),
                ),
            ),
        )


class EarlyDecisionStrategy(ResearchStrategy[CounterState]):
    def initial_state(self, context: ResearchRunContext) -> CounterState:
        return CounterState()

    def on_observation(
        self,
        context: ResearchRunContext,
        observation: ResearchObservation,
        state: CounterState,
    ) -> StrategyStep[CounterState]:
        return StrategyStep(
            state=state,
            decisions=(
                ResearchDecision(
                    decision_type="INVALID_EARLY",
                    decision_time=observation.availability_time - timedelta(seconds=1),
                ),
            ),
        )


def record(
    minute: int,
    value: str,
    *,
    availability_minute: int | None = None,
) -> LoadedRecord:
    event_time = datetime(2026, 1, 1, 0, minute, tzinfo=UTC)
    available = minute if availability_minute is None else availability_minute
    availability_time = datetime(2026, 1, 1, 0, available, tzinfo=UTC)
    return LoadedRecord(
        source_line=minute + 2,
        event_time=event_time,
        availability_time=availability_time,
        fields=(("value", value),),
    )


def dataset(records: tuple[LoadedRecord, ...]) -> LoadedDataset:
    return LoadedDataset(
        dataset_id="DATA-SYNTHETIC-REPLAY-001",
        dataset_version="1.0.0",
        source_location="synthetic://replay-fixture",
        computed_sha256="0" * 64,
        records=records,
        source_row_count=len(records),
        dropped_malformed_count=0,
        duplicate_discard_count=0,
        out_of_order_detected=False,
        missing_policy=MissingPolicy.ALLOW_DECLARED_GAPS,
    )


def replay_fixture() -> ReplayResult[CounterState]:
    strategy = CountingStrategy()
    context = ResearchRunContext(parameters=(("start", 5),), seed=11)
    return run_replay(
        dataset((record(0, "alpha"), record(1, "beta"), record(2, "gamma"))),
        context,
        strategy,
    )


def test_replay_preserves_loaded_order_and_calls_strategy_once_per_record() -> None:
    strategy = CountingStrategy()
    context = ResearchRunContext()
    loaded = dataset((record(0, "alpha"), record(1, "beta"), record(2, "gamma")))

    result = run_replay(loaded, context, strategy)

    assert strategy.initial_calls == 1
    assert strategy.observation_calls == 3
    assert result.observation_count == 3
    assert [frame.observation.sequence_index for frame in result.frames] == [0, 1, 2]
    assert [frame.observation.value("value") for frame in result.frames] == [
        "alpha",
        "beta",
        "gamma",
    ]


def test_replay_state_trace_is_ordered_and_complete() -> None:
    result = replay_fixture()

    assert result.initial_state == CounterState(5)
    assert result.final_state == CounterState(8)
    assert [frame.state_before.count for frame in result.frames] == [5, 6, 7]
    assert [frame.state_after.count for frame in result.frames] == [6, 7, 8]
    assert [diagnostic.details for diagnostic in result.diagnostics] == [
        (("count", 6),),
        (("count", 7),),
        (("count", 8),),
    ]


def test_repeated_replay_is_exactly_equal() -> None:
    assert replay_fixture() == replay_fixture()


def test_replay_decisions_are_flattened_in_emission_order() -> None:
    result = replay_fixture()

    assert [decision.payload for decision in result.decisions] == [
        (("sequence", 0), ("value", "alpha")),
        (("sequence", 1), ("value", "beta")),
        (("sequence", 2), ("value", "gamma")),
    ]


def test_replay_result_binds_dataset_identity_and_hash() -> None:
    result = replay_fixture()

    assert result.dataset_id == "DATA-SYNTHETIC-REPLAY-001"
    assert result.dataset_version == "1.0.0"
    assert result.source_location == "synthetic://replay-fixture"
    assert result.computed_sha256 == "0" * 64


def test_empty_dataset_returns_initial_state_without_strategy_steps() -> None:
    strategy = CountingStrategy()
    context = ResearchRunContext(parameters=(("start", 4),))

    result = run_replay(dataset(()), context, strategy)

    assert result.initial_state == CounterState(4)
    assert result.final_state == CounterState(4)
    assert result.frames == ()
    assert strategy.initial_calls == 1
    assert strategy.observation_calls == 0


def test_availability_time_regression_is_rejected() -> None:
    loaded = dataset(
        (
            record(0, "delayed", availability_minute=2),
            record(1, "earlier-available", availability_minute=1),
        )
    )

    with pytest.raises(ReplayContractError, match="availability_time must be nondecreasing"):
        run_replay(loaded, ResearchRunContext(), CountingStrategy())


def test_decision_before_observation_availability_is_rejected() -> None:
    loaded = dataset((record(0, "alpha"),))

    with pytest.raises(ReplayContractError, match="decision_time cannot be earlier"):
        run_replay(loaded, ResearchRunContext(), EarlyDecisionStrategy())


def test_manifest_loader_strategy_replay_vertical_slice() -> None:
    manifest = load_dataset_manifest(LOADER_MANIFEST)
    loaded = load_dataset(manifest, root=ROOT)
    strategy = CountingStrategy()

    result = run_replay(
        loaded,
        ResearchRunContext(),
        strategy,
    )

    assert result.dataset_id == "DATA-SYNTHETIC-LOADER-001"
    assert result.observation_count == 3
    assert [decision.payload for decision in result.decisions] == [
        (("sequence", 0), ("value", "alpha")),
        (("sequence", 1), ("value", "beta")),
        (("sequence", 2), ("value", "gamma")),
    ]
