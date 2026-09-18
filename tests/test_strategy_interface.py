from __future__ import annotations

import json
from dataclasses import FrozenInstanceError, dataclass
from datetime import UTC, datetime

import pytest

from ats.data.loader import LoadedRecord
from ats.strategy.interface import (
    ResearchDecision,
    ResearchDiagnostic,
    ResearchObservation,
    ResearchRunContext,
    ResearchStrategy,
    StrategyStep,
    observation_from_loaded_record,
)


@dataclass(frozen=True, slots=True)
class CounterState:
    count: int = 0


class DeterministicFixtureStrategy(ResearchStrategy[CounterState]):
    def initial_state(self, context: ResearchRunContext) -> CounterState:
        start = dict(context.parameters).get("start", 0)
        assert isinstance(start, int)
        return CounterState(count=start)

    def on_observation(
        self,
        context: ResearchRunContext,
        observation: ResearchObservation,
        state: CounterState,
    ) -> StrategyStep[CounterState]:
        next_count = state.count + 1
        threshold = dict(context.parameters).get("emit_at", 2)
        assert isinstance(threshold, int)

        decisions = ()
        if next_count == threshold:
            decisions = (
                ResearchDecision(
                    decision_type="FIXTURE_SIGNAL",
                    decision_time=observation.availability_time,
                    payload=(
                        ("count", next_count),
                        ("value", observation.value("value")),
                    ),
                ),
            )

        diagnostic = ResearchDiagnostic(
            code="STEP",
            message="fixture step processed",
            details=(("count", next_count),),
        )
        return StrategyStep(
            state=CounterState(count=next_count),
            decisions=decisions,
            diagnostics=(diagnostic,),
        )


def observation(index: int, value: str) -> ResearchObservation:
    timestamp = datetime(2026, 1, 1, 0, index, tzinfo=UTC)
    return ResearchObservation(
        sequence_index=index,
        event_time=timestamp,
        availability_time=timestamp,
        fields=(("value", value),),
    )


def run_fixture() -> tuple[CounterState, tuple[str, ...]]:
    context = ResearchRunContext(parameters=(("emit_at", 2), ("start", 0)), seed=7)
    strategy = DeterministicFixtureStrategy()
    state = strategy.initial_state(context)
    serialized: list[str] = []

    for index, value in enumerate(("alpha", "beta", "gamma")):
        step = strategy.on_observation(context, observation(index, value), state)
        state = step.state
        serialized.extend(decision.to_json() for decision in step.decisions)

    return state, tuple(serialized)


def test_loaded_record_bridge_preserves_research_times_and_fields() -> None:
    event_time = datetime(2026, 1, 1, 0, 0, tzinfo=UTC)
    availability_time = datetime(2026, 1, 1, 0, 0, 5, tzinfo=UTC)
    loaded = LoadedRecord(
        source_line=2,
        event_time=event_time,
        availability_time=availability_time,
        fields=(("event_time", "2026-01-01T00:00:00Z"), ("value", "alpha")),
    )

    result = observation_from_loaded_record(loaded, sequence_index=3)

    assert result.sequence_index == 3
    assert result.event_time == event_time
    assert result.availability_time == availability_time
    assert result.value("value") == "alpha"


def test_repeated_fixture_transitions_are_exactly_deterministic() -> None:
    first = run_fixture()
    second = run_fixture()

    assert first == second
    assert first[0] == CounterState(count=3)
    assert len(first[1]) == 1


def test_decision_serialization_is_canonical_and_broker_neutral() -> None:
    decision = ResearchDecision(
        decision_type="FIXTURE_SIGNAL",
        decision_time=datetime(2026, 1, 1, tzinfo=UTC),
        payload=(("z", 2), ("a", "alpha")),
    )

    encoded = decision.to_json()
    decoded = json.loads(encoded)

    assert encoded == (
        '{"decision_time":"2026-01-01T00:00:00+00:00",'
        '"decision_type":"FIXTURE_SIGNAL","payload":{"a":"alpha","z":2}}'
    )
    assert set(decoded) == {"decision_time", "decision_type", "payload"}
    assert "broker" not in encoded.lower()
    assert "order_id" not in encoded.lower()
    assert "account" not in encoded.lower()


def test_run_context_is_immutable() -> None:
    context = ResearchRunContext(configuration=(("mode", "fixture"),))

    with pytest.raises(FrozenInstanceError):
        context.seed = 10


def test_observation_is_immutable() -> None:
    item = observation(0, "alpha")

    with pytest.raises(FrozenInstanceError):
        item.sequence_index = 2


def test_duplicate_context_keys_are_rejected() -> None:
    with pytest.raises(ValueError, match="duplicate key"):
        ResearchRunContext(parameters=(("x", 1), ("x", 2)))


def test_non_finite_decision_payload_is_rejected() -> None:
    with pytest.raises(ValueError, match="finite"):
        ResearchDecision(
            decision_type="FIXTURE_SIGNAL",
            decision_time=datetime(2026, 1, 1, tzinfo=UTC),
            payload=(("score", float("nan")),),
        )


def test_naive_decision_time_is_rejected() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        ResearchDecision(
            decision_type="FIXTURE_SIGNAL",
            decision_time=datetime(2026, 1, 1),
        )


def test_observation_requires_unique_fields() -> None:
    timestamp = datetime(2026, 1, 1, tzinfo=UTC)

    with pytest.raises(ValueError, match="unique"):
        ResearchObservation(
            sequence_index=0,
            event_time=timestamp,
            availability_time=timestamp,
            fields=(("value", "a"), ("value", "b")),
        )


def test_diagnostic_is_serializable_and_immutable() -> None:
    diagnostic = ResearchDiagnostic(
        code="FIXTURE",
        message="synthetic diagnostic",
        details=(("count", 1),),
    )

    assert diagnostic.to_dict() == {
        "code": "FIXTURE",
        "details": {"count": 1},
        "message": "synthetic diagnostic",
    }
    with pytest.raises(FrozenInstanceError):
        diagnostic.code = "OTHER"
