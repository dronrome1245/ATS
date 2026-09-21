from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import FrozenInstanceError

import pytest

from ats.validation.sensitivity import (
    ParameterVariant,
    SensitivityContractError,
    SensitivityPlan,
    evaluate_parameter_sensitivity,
)


def fixture_plan() -> SensitivityPlan:
    return SensitivityPlan(
        plan_id="SYNTH-SENSITIVITY-001",
        parameter_names=("lookback", "threshold"),
        metric_names=("score", "count"),
        variants=(
            ParameterVariant(variant_id="v-center", values=(20, 2.0)),
            ParameterVariant(variant_id="v-left", values=(10, 1.0)),
            ParameterVariant(variant_id="v-right", values=(30, 3.0)),
        ),
    )


def synthetic_evaluator(
    parameters: Mapping[str, object],
) -> dict[str, int | float]:
    lookback = parameters["lookback"]
    threshold = parameters["threshold"]
    assert isinstance(lookback, int)
    assert isinstance(threshold, float)
    return {
        "count": lookback,
        "score": float(lookback) - threshold,
    }


def test_full_predeclared_region_is_preserved_in_input_order() -> None:
    result = evaluate_parameter_sensitivity(fixture_plan(), synthetic_evaluator)

    assert tuple(point.variant_id for point in result.points) == (
        "v-center",
        "v-left",
        "v-right",
    )
    assert result.points[0].parameters == (
        ("lookback", 20),
        ("threshold", 2.0),
    )
    assert result.points[1].metrics == (("score", 9.0), ("count", 10))
    assert result.points[2].metrics == (("score", 27.0), ("count", 30))


def test_serialization_is_deterministic_and_has_no_selected_winner() -> None:
    first = evaluate_parameter_sensitivity(fixture_plan(), synthetic_evaluator)
    second = evaluate_parameter_sensitivity(fixture_plan(), synthetic_evaluator)

    assert first.to_json() == second.to_json()

    decoded = json.loads(first.to_json())
    assert decoded["selection_policy"] == "NO_AUTOMATIC_SELECTION"
    assert set(decoded) == {
        "metric_names",
        "parameter_names",
        "plan_id",
        "points",
        "schema_version",
        "selection_policy",
    }
    assert all("rank" not in point for point in decoded["points"])
    assert all("selected" not in point for point in decoded["points"])


def test_metric_order_comes_from_plan_not_evaluator_mapping_order() -> None:
    def reverse_metric_order(
        parameters: Mapping[str, object],
    ) -> dict[str, int | float]:
        lookback = parameters["lookback"]
        threshold = parameters["threshold"]
        assert isinstance(lookback, int)
        assert isinstance(threshold, float)
        return {
            "count": lookback,
            "score": float(lookback) - threshold,
        }

    result = evaluate_parameter_sensitivity(
        fixture_plan(),
        reverse_metric_order,
    )

    assert result.points[0].metrics == (("score", 18.0), ("count", 20))


def test_duplicate_variant_ids_are_rejected() -> None:
    with pytest.raises(
        SensitivityContractError,
        match="variant_id values must be unique",
    ):
        SensitivityPlan(
            plan_id="SYNTH",
            parameter_names=("x",),
            metric_names=("score",),
            variants=(
                ParameterVariant(variant_id="same", values=(1,)),
                ParameterVariant(variant_id="same", values=(2,)),
            ),
        )


def test_variant_must_match_declared_parameter_shape() -> None:
    with pytest.raises(
        SensitivityContractError,
        match="must provide 2 parameter values",
    ):
        SensitivityPlan(
            plan_id="SYNTH",
            parameter_names=("x", "y"),
            metric_names=("score",),
            variants=(ParameterVariant(variant_id="v1", values=(1,)),),
        )


def test_missing_or_extra_metrics_are_rejected() -> None:
    plan = fixture_plan()

    with pytest.raises(SensitivityContractError, match="metric set mismatch"):
        evaluate_parameter_sensitivity(
            plan,
            lambda _params: {"score": 1.0},
        )

    with pytest.raises(SensitivityContractError, match="metric set mismatch"):
        evaluate_parameter_sensitivity(
            plan,
            lambda _params: {"score": 1.0, "count": 1, "extra": 3.0},
        )


def test_non_finite_values_are_rejected() -> None:
    with pytest.raises(
        SensitivityContractError,
        match="parameter values must be finite",
    ):
        ParameterVariant(variant_id="bad", values=(float("nan"),))

    with pytest.raises(
        SensitivityContractError,
        match="metric 'score' must be finite",
    ):
        evaluate_parameter_sensitivity(
            fixture_plan(),
            lambda _params: {"score": float("inf"), "count": 1},
        )


def test_non_scalar_parameter_values_are_rejected() -> None:
    with pytest.raises(
        SensitivityContractError,
        match="parameter values must be JSON scalars",
    ):
        ParameterVariant(
            variant_id="bad",
            values=(["not", "scalar"],),
        )


def test_plan_and_results_are_immutable() -> None:
    plan = fixture_plan()
    result = evaluate_parameter_sensitivity(plan, synthetic_evaluator)

    with pytest.raises(FrozenInstanceError):
        plan.plan_id = "OTHER"

    with pytest.raises(FrozenInstanceError):
        result.plan_id = "OTHER"
