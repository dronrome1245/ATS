from __future__ import annotations

from dataclasses import dataclass

import pytest

from ats.analytics.standard import (
    ActivityCount,
    AnalyticsApplicability,
    EffectSeries,
    NotApplicable,
    build_standard_analytics,
)
from ats.costs.interface import CostApplicability, CostComponentResult, CostResult
from ats.replay.engine import ReplayResult


@dataclass(frozen=True, slots=True)
class FixtureFrame:
    decisions: tuple[object, ...] = ()
    diagnostics: tuple[object, ...] = ()


def replay_fixture() -> ReplayResult[object]:
    return ReplayResult(
        dataset_id="DATA-SYNTHETIC-ANALYTICS-001",
        dataset_version="1.0.0",
        source_location="synthetic://analytics-fixture",
        computed_sha256="a" * 64,
        context=object(),
        initial_state=object(),
        final_state=object(),
        frames=(
            FixtureFrame(decisions=(object(), object()), diagnostics=(object(),)),
            FixtureFrame(decisions=(object(),)),
        ),
    )


def cost_fixture() -> CostResult:
    return CostResult(
        reference_id="fixture-costs-001",
        components=(
            CostComponentResult(
                name="fee",
                applicability=CostApplicability.APPLICABLE,
                value=1.0,
                unit="fixture-units",
            ),
            CostComponentResult(
                name="spread_proxy",
                applicability=CostApplicability.APPLICABLE,
                value=2.0,
                unit="fixture-units",
            ),
            CostComponentResult(
                name="slippage_proxy",
                applicability=CostApplicability.NOT_APPLICABLE,
            ),
        ),
    )


def test_standard_analytics_keeps_gross_costs_and_net_separate() -> None:
    result = build_standard_analytics(
        replay_fixture(),
        effects=EffectSeries(
            semantics="synthetic effect per fixture activity",
            unit="fixture-units",
            increments=(4.0, -1.0, 2.0),
        ),
        costs=cost_fixture(),
        trade_or_event_count=ActivityCount(kind="synthetic_event", count=3),
    )

    payload = result.to_dict()
    assert payload["primary_metrics"]["gross_effect"]["value"] == 5.0
    assert payload["costs"]["total"]["value"] == 3.0
    assert payload["primary_metrics"]["net_effect"]["value"] == 2.0
    assert payload["risk_metrics"]["max_drawdown"]["value"] == 1.0


def test_replay_counts_are_reported_without_treating_decisions_as_trades() -> None:
    result = build_standard_analytics(
        replay_fixture(),
        effects=NotApplicable("fixture has no economic effect semantics"),
        costs=NotApplicable("costs are not applicable without economic effects"),
        trade_or_event_count=NotApplicable("research decisions are not trade records"),
    )

    payload = result.to_dict()
    assert payload["secondary_metrics"]["observation_count"] == 2
    assert payload["secondary_metrics"]["decision_count"] == 3
    assert payload["secondary_metrics"]["diagnostic_count"] == 1
    assert payload["trade_or_event_count"]["applicability"] == "NOT_APPLICABLE"


def test_effect_distribution_and_path_metrics_are_deterministic() -> None:
    result = build_standard_analytics(
        replay_fixture(),
        effects=EffectSeries(
            semantics="ordered synthetic effect increments",
            unit="fixture-units",
            increments=(2.0, -1.0, -3.0, 5.0),
        ),
        costs=NotApplicable("cost model omitted for this software fixture"),
        trade_or_event_count=ActivityCount(kind="synthetic_event", count=4),
    )

    assert result.effects.gross_effect.value == 3.0
    assert result.effects.mean_effect.value == pytest.approx(0.75)
    assert result.effects.minimum_effect.value == -3.0
    assert result.effects.maximum_effect.value == 5.0
    assert result.effects.max_drawdown.value == 4.0


def test_empty_explicit_effect_series_has_zero_gross_and_drawdown() -> None:
    result = build_standard_analytics(
        replay_fixture(),
        effects=EffectSeries(
            semantics="explicit empty synthetic effect series",
            unit="fixture-units",
            increments=(),
        ),
        costs=NotApplicable("no modeled costs"),
        trade_or_event_count=ActivityCount(kind="synthetic_event", count=0),
    )

    assert result.effects.count.value == 0
    assert result.effects.gross_effect.value == 0.0
    assert result.effects.max_drawdown.value == 0.0
    assert result.effects.mean_effect.applicability is AnalyticsApplicability.NOT_APPLICABLE


def test_incompatible_cost_units_keep_total_and_net_not_applicable() -> None:
    costs = CostResult(
        reference_id="fixture-costs-mixed-units",
        components=(
            CostComponentResult(
                name="fee",
                applicability=CostApplicability.APPLICABLE,
                value=1.0,
                unit="unit-a",
            ),
            CostComponentResult(
                name="spread_proxy",
                applicability=CostApplicability.APPLICABLE,
                value=2.0,
                unit="unit-b",
            ),
        ),
    )
    result = build_standard_analytics(
        replay_fixture(),
        effects=EffectSeries(
            semantics="synthetic gross effect",
            unit="unit-a",
            increments=(5.0,),
        ),
        costs=costs,
        trade_or_event_count=NotApplicable("activity semantics intentionally omitted"),
    )

    assert result.costs.total.applicability is AnalyticsApplicability.NOT_APPLICABLE
    assert result.net_effect.applicability is AnalyticsApplicability.NOT_APPLICABLE


def test_no_applicable_cost_components_do_not_create_hidden_zero_cost() -> None:
    costs = CostResult(
        reference_id="fixture-no-applicable-costs",
        components=(
            CostComponentResult(
                name="slippage_proxy",
                applicability=CostApplicability.NOT_APPLICABLE,
            ),
        ),
    )
    result = build_standard_analytics(
        replay_fixture(),
        effects=EffectSeries(
            semantics="synthetic gross effect",
            unit="fixture-units",
            increments=(5.0,),
        ),
        costs=costs,
        trade_or_event_count=NotApplicable("not meaningful for fixture"),
    )

    assert result.costs.total.applicability is AnalyticsApplicability.NOT_APPLICABLE
    assert result.costs.total.value is None
    assert result.net_effect.applicability is AnalyticsApplicability.NOT_APPLICABLE


def test_effect_input_must_be_finite_and_semantically_declared() -> None:
    with pytest.raises(ValueError, match="effect semantics must be non-empty"):
        EffectSeries(semantics="", unit="fixture-units", increments=(1.0,))

    with pytest.raises(ValueError, match="effect increments must be finite"):
        EffectSeries(
            semantics="synthetic effect",
            unit="fixture-units",
            increments=(float("nan"),),
        )


def test_activity_count_requires_explicit_non_negative_semantics() -> None:
    with pytest.raises(ValueError, match="kind must be non-empty"):
        ActivityCount(kind="", count=1)

    with pytest.raises(ValueError, match="non-negative integer"):
        ActivityCount(kind="trade", count=-1)


def test_not_applicable_reason_is_required() -> None:
    with pytest.raises(ValueError, match="must declare a reason"):
        NotApplicable("")


def test_json_and_markdown_outputs_are_deterministic() -> None:
    result = build_standard_analytics(
        replay_fixture(),
        effects=EffectSeries(
            semantics="synthetic effect per fixture activity",
            unit="fixture-units",
            increments=(4.0, -1.0, 2.0),
        ),
        costs=cost_fixture(),
        trade_or_event_count=ActivityCount(kind="synthetic_event", count=3),
    )

    assert result.to_json() == result.to_json()
    assert result.to_markdown() == result.to_markdown()
    assert "Gross effect: 5.0 fixture-units" in result.to_markdown()
    assert "Modeled costs: 3.0 fixture-units" in result.to_markdown()
    assert "Net effect: 2.0 fixture-units" in result.to_markdown()
