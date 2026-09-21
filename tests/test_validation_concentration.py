from __future__ import annotations

import json
from dataclasses import FrozenInstanceError

import pytest

from ats.validation.concentration import (
    ConcentrationContractError,
    ConcentrationPlan,
    Contribution,
    analyze_concentration,
)


def fixture_plan() -> ConcentrationPlan:
    return ConcentrationPlan(
        plan_id="SYNTH-CONCENTRATION-001",
        top_counts=(1, 2, 10),
    )


def fixture_contributions() -> tuple[Contribution, ...]:
    return (
        Contribution(observation_id="a", value=8.0, group_id="g1"),
        Contribution(observation_id="b", value=-3.0, group_id="g1"),
        Contribution(observation_id="c", value=2.0, group_id="g2"),
        Contribution(observation_id="d", value=1.0, group_id="g2"),
    )


def test_all_observations_are_retained_in_input_order() -> None:
    result = analyze_concentration(fixture_plan(), fixture_contributions())

    assert tuple(item.observation_id for item in result.observations) == (
        "a",
        "b",
        "c",
        "d",
    )
    assert result.observation_count == 4
    assert result.total_effect == 8.0
    assert result.total_absolute_effect == 14.0


def test_top_observation_concentration_uses_absolute_magnitude() -> None:
    result = analyze_concentration(fixture_plan(), fixture_contributions())

    top_one, top_two, top_ten = result.top_observations
    assert top_one.requested_count == 1
    assert top_one.actual_count == 1
    assert top_one.absolute_effect == 8.0
    assert top_one.absolute_share == pytest.approx(8.0 / 14.0)

    assert top_two.absolute_effect == 11.0
    assert top_two.absolute_share == pytest.approx(11.0 / 14.0)

    assert top_ten.actual_count == 4
    assert top_ten.absolute_effect == 14.0
    assert top_ten.absolute_share == pytest.approx(1.0)


def test_group_aggregation_retains_every_group_in_first_seen_order() -> None:
    result = analyze_concentration(fixture_plan(), fixture_contributions())

    assert tuple(item.group_id for item in result.groups) == ("g1", "g2")
    assert result.groups[0].observation_count == 2
    assert result.groups[0].signed_effect == 5.0
    assert result.groups[0].absolute_net_effect == 5.0
    assert result.groups[1].signed_effect == 3.0


def test_top_group_concentration_is_diagnostic_only() -> None:
    result = analyze_concentration(fixture_plan(), fixture_contributions())
    decoded = json.loads(result.to_json())

    assert decoded["ranking_basis"] == "ABSOLUTE_MAGNITUDE_DIAGNOSTIC_ONLY"
    assert decoded["removal_policy"] == "NO_AUTOMATIC_OUTLIER_REMOVAL"
    assert decoded["top_groups"][0]["absolute_effect"] == 5.0
    assert len(decoded["groups"]) == 2
    assert len(decoded["observations"]) == 4


def test_repeated_serialization_is_exactly_deterministic() -> None:
    first = analyze_concentration(fixture_plan(), fixture_contributions())
    second = analyze_concentration(fixture_plan(), fixture_contributions())

    assert first.to_json() == second.to_json()


def test_zero_absolute_effect_has_explicit_null_share() -> None:
    result = analyze_concentration(
        fixture_plan(),
        (
            Contribution(observation_id="a", value=0.0, group_id="g1"),
            Contribution(observation_id="b", value=0.0, group_id="g2"),
        ),
    )

    assert result.total_absolute_effect == 0.0
    assert result.top_observations[0].absolute_share is None
    assert result.top_groups[0].absolute_share is None


def test_duplicate_observation_ids_are_rejected() -> None:
    with pytest.raises(
        ConcentrationContractError,
        match="observation_id values must be unique",
    ):
        analyze_concentration(
            fixture_plan(),
            (
                Contribution(observation_id="same", value=1.0),
                Contribution(observation_id="same", value=2.0),
            ),
        )


def test_non_finite_or_empty_inputs_are_rejected() -> None:
    with pytest.raises(
        ConcentrationContractError,
        match="contribution value must be finite",
    ):
        Contribution(observation_id="bad", value=float("nan"))

    with pytest.raises(
        ConcentrationContractError,
        match="contributions must not be empty",
    ):
        analyze_concentration(fixture_plan(), ())


def test_invalid_top_counts_are_rejected() -> None:
    with pytest.raises(
        ConcentrationContractError,
        match="positive integers",
    ):
        ConcentrationPlan(plan_id="BAD", top_counts=(0,))

    with pytest.raises(
        ConcentrationContractError,
        match="unique values",
    ):
        ConcentrationPlan(plan_id="BAD", top_counts=(1, 1))


def test_plan_and_result_are_immutable() -> None:
    plan = fixture_plan()
    result = analyze_concentration(plan, fixture_contributions())

    with pytest.raises(FrozenInstanceError):
        plan.plan_id = "OTHER"

    with pytest.raises(FrozenInstanceError):
        result.plan_id = "OTHER"
