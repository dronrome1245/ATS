"""Minimal broker-independent Strategy/Research interface for ATS M2."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime
from typing import Generic, Protocol, TypeVar, runtime_checkable

from ats.data.loader import LoadedRecord

JsonScalar = str | int | float | bool | None
StateT = TypeVar("StateT")


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


@dataclass(frozen=True, slots=True)
class ResearchRunContext:
    """Immutable declared run/configuration context supplied to research logic."""

    configuration: tuple[tuple[str, JsonScalar], ...] = ()
    parameters: tuple[tuple[str, JsonScalar], ...] = ()
    seed: int | None = None

    def __post_init__(self) -> None:
        _validate_pairs(self.configuration, label="configuration")
        _validate_pairs(self.parameters, label="parameters")

    def to_dict(self) -> dict[str, object]:
        return {
            "configuration": _pairs_to_dict(self.configuration),
            "parameters": _pairs_to_dict(self.parameters),
            "seed": self.seed,
        }


@dataclass(frozen=True, slots=True)
class ResearchObservation:
    """Immutable observation available to strategy logic at one research step."""

    sequence_index: int
    event_time: datetime
    availability_time: datetime
    fields: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if self.sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        if self.event_time.tzinfo is None or self.event_time.utcoffset() is None:
            raise ValueError("event_time must be timezone-aware")
        if self.availability_time.tzinfo is None or self.availability_time.utcoffset() is None:
            raise ValueError("availability_time must be timezone-aware")
        field_names = [name for name, _ in self.fields]
        if any(not name for name in field_names):
            raise ValueError("observation field names must be non-empty")
        if len(field_names) != len(set(field_names)):
            raise ValueError("observation field names must be unique")

    def value(self, field_name: str) -> str:
        for name, value in self.fields:
            if name == field_name:
                return value
        raise KeyError(field_name)


@dataclass(frozen=True, slots=True)
class ResearchDecision:
    """Serializable broker-independent research decision/intent."""

    decision_type: str
    decision_time: datetime
    payload: tuple[tuple[str, JsonScalar], ...] = ()

    def __post_init__(self) -> None:
        if not self.decision_type:
            raise ValueError("decision_type must be non-empty")
        if self.decision_time.tzinfo is None or self.decision_time.utcoffset() is None:
            raise ValueError("decision_time must be timezone-aware")
        _validate_pairs(self.payload, label="decision payload")

    def to_dict(self) -> dict[str, object]:
        return {
            "decision_time": self.decision_time.isoformat(),
            "decision_type": self.decision_type,
            "payload": _pairs_to_dict(self.payload),
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )


@dataclass(frozen=True, slots=True)
class ResearchDiagnostic:
    """Serializable non-decision diagnostic emitted by research logic."""

    code: str
    message: str
    details: tuple[tuple[str, JsonScalar], ...] = ()

    def __post_init__(self) -> None:
        if not self.code:
            raise ValueError("diagnostic code must be non-empty")
        if not self.message:
            raise ValueError("diagnostic message must be non-empty")
        _validate_pairs(self.details, label="diagnostic details")

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "details": _pairs_to_dict(self.details),
            "message": self.message,
        }


@dataclass(frozen=True, slots=True)
class StrategyStep(Generic[StateT]):
    """One deterministic research-logic transition."""

    state: StateT
    decisions: tuple[ResearchDecision, ...] = ()
    diagnostics: tuple[ResearchDiagnostic, ...] = ()


@runtime_checkable
class ResearchStrategy(Protocol[StateT]):
    """Technology-neutral strategy contract consumed later by deterministic replay."""

    def initial_state(self, context: ResearchRunContext) -> StateT:
        """Return deterministic initial research state."""

    def on_observation(
        self,
        context: ResearchRunContext,
        observation: ResearchObservation,
        state: StateT,
    ) -> StrategyStep[StateT]:
        """Process one immutable observation and return one deterministic transition."""


def observation_from_loaded_record(
    record: LoadedRecord,
    *,
    sequence_index: int,
) -> ResearchObservation:
    """Bridge the deterministic base-loader record into the Strategy/Research interface."""

    return ResearchObservation(
        sequence_index=sequence_index,
        event_time=record.event_time,
        availability_time=record.availability_time,
        fields=record.fields,
    )
