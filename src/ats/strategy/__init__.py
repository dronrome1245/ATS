"""Broker-independent ATS research-strategy contracts."""

from .interface import (
    JsonScalar,
    ResearchDecision,
    ResearchDiagnostic,
    ResearchObservation,
    ResearchRunContext,
    ResearchStrategy,
    StrategyStep,
    observation_from_loaded_record,
)

__all__ = [
    "JsonScalar",
    "ResearchDecision",
    "ResearchDiagnostic",
    "ResearchObservation",
    "ResearchRunContext",
    "ResearchStrategy",
    "StrategyStep",
    "observation_from_loaded_record",
]
