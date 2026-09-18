from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ats.costs.interface import (
    CostApplicability,
    CostComponentConfig,
    CostComponentResult,
    CostContractError,
    CostInput,
    CostModel,
    CostModelConfig,
    CostResult,
    apply_cost_model,
)


class DeterministicFixtureCostModel(CostModel):
    def evaluate(self, cost_input: CostInput, config: CostModelConfig) -> CostResult:
        attributes = dict(cost_input.attributes)
        activity_units = attributes["activity_units"]
        cost_unit = attributes["cost_unit"]
        assert isinstance(activity_units, (int, float))
        assert isinstance(cost_unit, str)

        results: list[CostComponentResult] = []
        for component in config.components:
            if component.applicability is CostApplicability.NOT_APPLICABLE:
                results.append(
                    CostComponentResult(
                        name=component.name,
                        applicability=component.applicability,
                        details=(("reason", component.reason),),
                    )
                )
                continue

            per_unit = dict(component.parameters)["per_unit"]
            assert isinstance(per_unit, (int, float))
            results.append(
                CostComponentResult(
                    name=component.name,
                    applicability=component.applicability,
                    value=activity_units * per_unit,
                    unit=cost_unit,
                    details=(("per_unit", per_unit),),
                )
            )

        return CostResult(reference_id=cost_input.reference_id, components=tuple(results))


class MissingComponentModel(CostModel):
    def evaluate(self, cost_input: CostInput, config: CostModelConfig) -> CostResult:
        first = config.components[0]
        return CostResult(
            reference_id=cost_input.reference_id,
            components=(
                CostComponentResult(
                    name=first.name,
                    applicability=CostApplicability.APPLICABLE,
                    value=1.0,
                    unit="fixture-units",
                ),
            ),
        )


def explicit_config() -> CostModelConfig:
    return CostModelConfig(
        components=(
            CostComponentConfig(
                name="fee",
                applicability=CostApplicability.APPLICABLE,
                parameters=(("per_unit", 0.25),),
            ),
            CostComponentConfig(
                name="spread_proxy",
                applicability=CostApplicability.APPLICABLE,
                parameters=(("per_unit", 0.5),),
            ),
            CostComponentConfig(
                name="slippage_proxy",
                applicability=CostApplicability.NOT_APPLICABLE,
                reason="synthetic fixture excludes slippage",
            ),
        )
    )


def explicit_input() -> CostInput:
    return CostInput(
        reference_id="fixture-effect-001",
        attributes=(("activity_units", 4), ("cost_unit", "fixture-units")),
    )


def test_applicable_component_requires_explicit_parameters() -> None:
    with pytest.raises(ValueError, match="must declare explicit parameters"):
        CostComponentConfig(
            name="fee",
            applicability=CostApplicability.APPLICABLE,
        )


def test_not_applicable_component_is_explicit_and_parameter_free() -> None:
    with pytest.raises(ValueError, match="must declare a reason"):
        CostComponentConfig(
            name="slippage_proxy",
            applicability=CostApplicability.NOT_APPLICABLE,
        )

    with pytest.raises(ValueError, match="cannot declare parameters"):
        CostComponentConfig(
            name="slippage_proxy",
            applicability=CostApplicability.NOT_APPLICABLE,
            parameters=(("per_unit", 0.0),),
            reason="not used",
        )


def test_cost_config_rejects_duplicate_component_names() -> None:
    component = CostComponentConfig(
        name="fee",
        applicability=CostApplicability.APPLICABLE,
        parameters=(("per_unit", 0.1),),
    )
    with pytest.raises(ValueError, match="component names must be unique"):
        CostModelConfig(components=(component, component))


def test_non_finite_cost_inputs_and_results_are_rejected() -> None:
    with pytest.raises(ValueError, match="float values must be finite"):
        CostInput(reference_id="x", attributes=(("value", float("nan")),))

    with pytest.raises(ValueError, match="cost result value must be finite"):
        CostComponentResult(
            name="fee",
            applicability=CostApplicability.APPLICABLE,
            value=float("inf"),
            unit="fixture-units",
        )


def test_cost_contract_is_immutable() -> None:
    config = explicit_config()
    with pytest.raises(FrozenInstanceError):
        config.components = ()  # type: ignore[misc]


def test_fixture_model_is_exactly_deterministic() -> None:
    model = DeterministicFixtureCostModel()
    first = apply_cost_model(explicit_input(), explicit_config(), model)
    second = apply_cost_model(explicit_input(), explicit_config(), model)

    assert first == second
    assert first.components[0].value == 1.0
    assert first.components[1].value == 2.0
    assert first.components[2].applicability is CostApplicability.NOT_APPLICABLE
    assert first.components[2].value is None


def test_cost_result_serialization_is_canonical_and_cost_only() -> None:
    result = apply_cost_model(explicit_input(), explicit_config(), DeterministicFixtureCostModel())

    assert result.to_json() == result.to_json()
    payload = result.to_dict()
    assert payload["reference_id"] == "fixture-effect-001"
    assert [component["name"] for component in payload["components"]] == [
        "fee",
        "spread_proxy",
        "slippage_proxy",
    ]
    assert "gross" not in payload
    assert "net" not in payload


def test_model_cannot_silently_omit_configured_component() -> None:
    with pytest.raises(CostContractError, match="exactly match configured order"):
        apply_cost_model(explicit_input(), explicit_config(), MissingComponentModel())


def test_model_result_must_preserve_input_identity_and_applicability() -> None:
    class WrongIdentityModel(CostModel):
        def evaluate(self, cost_input: CostInput, config: CostModelConfig) -> CostResult:
            return CostResult(
                reference_id="different",
                components=tuple(
                    CostComponentResult(
                        name=component.name,
                        applicability=component.applicability,
                        value=(
                            0.0
                            if component.applicability is CostApplicability.APPLICABLE
                            else None
                        ),
                        unit=(
                            "fixture-units"
                            if component.applicability is CostApplicability.APPLICABLE
                            else None
                        ),
                    )
                    for component in config.components
                ),
            )

    with pytest.raises(CostContractError, match="reference_id must match"):
        apply_cost_model(explicit_input(), explicit_config(), WrongIdentityModel())
