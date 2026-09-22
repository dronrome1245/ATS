from __future__ import annotations

import math
from datetime import UTC, datetime, timedelta

import pytest

from ats.discovery.bounded import (
    DiscoveryAlternative,
    ParameterAssignment,
    SearchManifest,
)
from ats.discovery.eurusd_h1 import (
    EurusdH1DiscoveryError,
    EurusdH1Evaluator,
    PriceBar,
)


def alternative(
    *,
    family: str = "RETURN_TAIL_CONTINUATION",
    tail: str = "HIGH",
    direction: str = "UP",
    horizon: str = "6H",
) -> DiscoveryAlternative:
    return DiscoveryAlternative(
        alternative_id=f"{family}-{tail}-{horizon}",
        pattern_family=family,
        feature_condition="PRIOR_MID_CLOSE_RETURN_QUANTILE",
        horizon=horizon,
        direction=direction,
        parameters=(
            ParameterAssignment(name="lookback_hours", value=6),
            ParameterAssignment(name="tail_quantile", value=0.1),
            ParameterAssignment(name="tail", value=tail),
        ),
    )


def bars(count: int = 240) -> tuple[PriceBar, ...]:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    values: list[PriceBar] = []
    for index in range(count):
        mid = 1.10 + 0.0002 * index + 0.003 * math.sin(index / 7)
        values.append(
            PriceBar(
                start + timedelta(hours=index),
                mid - 0.0001,
                mid - 0.00005,
                mid + 0.0001,
                mid + 0.00005,
            )
        )
    return tuple(values)


def manifest(alternatives: list[DiscoveryAlternative]) -> SearchManifest:
    return SearchManifest.model_construct(alternatives=tuple(alternatives))


def test_evaluator_returns_finite_metrics_and_events() -> None:
    item = alternative()
    metrics = EurusdH1Evaluator(bars(), manifest([item]))(item)

    assert metrics["event_count"] > 0
    assert all(math.isfinite(float(value)) for value in metrics.values())


def test_reversal_direction_contract_is_enforced() -> None:
    bad = alternative(
        family="RETURN_TAIL_REVERSAL",
        tail="HIGH",
        direction="UP",
    )

    with pytest.raises(EurusdH1DiscoveryError, match="direction"):
        EurusdH1Evaluator(bars(), manifest([bad]))


def test_low_tail_continuation_requires_down_direction() -> None:
    item = alternative(tail="LOW", direction="DOWN")
    metrics = EurusdH1Evaluator(bars(), manifest([item]))(item)

    assert metrics["event_count"] > 0


def test_gaps_are_not_crossed() -> None:
    values = list(bars())
    del values[100]
    item = alternative()
    metrics = EurusdH1Evaluator(tuple(values), manifest([item]))(item)

    assert metrics["event_count"] > 0


def test_parameter_set_is_closed() -> None:
    item = alternative().model_copy(
        update={
            "parameters": (ParameterAssignment(name="x", value=1),),
        }
    )

    with pytest.raises(EurusdH1DiscoveryError, match="parameter set"):
        EurusdH1Evaluator(bars(), manifest([item]))
