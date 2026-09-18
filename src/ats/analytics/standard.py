"""Deterministic baseline analytics/report output for ATS M2."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from enum import StrEnum

from ats.costs.interface import CostApplicability, CostComponentResult, CostResult
from ats.replay.engine import ReplayResult

Numeric = int | float


class AnalyticsApplicability(StrEnum):
    """Applicability state for analytics inputs and metrics."""

    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True, slots=True)
class NotApplicable:
    """Explicit marker for an analytics input that is genuinely not applicable."""

    reason: str

    def __post_init__(self) -> None:
        if not self.reason:
            raise ValueError("not-applicable analytics input must declare a reason")

    def to_dict(self) -> dict[str, object]:
        return {
            "applicability": AnalyticsApplicability.NOT_APPLICABLE.value,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class MetricValue:
    """One finite metric value or an explicit not-applicable marker."""

    applicability: AnalyticsApplicability
    value: Numeric | None = None
    unit: str | None = None
    reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.applicability, AnalyticsApplicability):
            raise ValueError("metric applicability must use AnalyticsApplicability")

        if self.applicability is AnalyticsApplicability.APPLICABLE:
            if self.value is None:
                raise ValueError("applicable metric must declare a value")
            if isinstance(self.value, bool) or not isinstance(self.value, (int, float)):
                raise ValueError("metric value must be numeric")
            if isinstance(self.value, float) and not math.isfinite(self.value):
                raise ValueError("metric value must be finite")
            if self.reason is not None:
                raise ValueError("applicable metric cannot declare a not-applicable reason")
        else:
            if self.value is not None or self.unit is not None:
                raise ValueError("not-applicable metric cannot declare value or unit")
            if not self.reason:
                raise ValueError("not-applicable metric must declare a reason")

    def to_dict(self) -> dict[str, object]:
        return {
            "applicability": self.applicability.value,
            "reason": self.reason,
            "unit": self.unit,
            "value": self.value,
        }


@dataclass(frozen=True, slots=True)
class EffectSeries:
    """Explicit ordered gross-effect increments with declared semantics and unit."""

    semantics: str
    unit: str
    increments: tuple[Numeric, ...]

    def __post_init__(self) -> None:
        if not self.semantics:
            raise ValueError("effect semantics must be non-empty")
        if not self.unit:
            raise ValueError("effect unit must be non-empty")
        for value in self.increments:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError("effect increments must be numeric")
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError("effect increments must be finite")


@dataclass(frozen=True, slots=True)
class ActivityCount:
    """Explicit trade/event/opportunity count with caller-declared semantics."""

    kind: str
    count: int

    def __post_init__(self) -> None:
        if not self.kind:
            raise ValueError("activity count kind must be non-empty")
        if isinstance(self.count, bool) or not isinstance(self.count, int) or self.count < 0:
            raise ValueError("activity count must be a non-negative integer")

    def to_dict(self) -> dict[str, object]:
        return {
            "applicability": AnalyticsApplicability.APPLICABLE.value,
            "count": self.count,
            "kind": self.kind,
        }


@dataclass(frozen=True, slots=True)
class EffectAnalytics:
    """Gross-effect distribution and path metrics, or explicit non-applicability."""

    applicability: AnalyticsApplicability
    semantics: str | None
    unit: str | None
    count: MetricValue
    gross_effect: MetricValue
    mean_effect: MetricValue
    minimum_effect: MetricValue
    maximum_effect: MetricValue
    max_drawdown: MetricValue
    reason: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "applicability": self.applicability.value,
            "count": self.count.to_dict(),
            "gross_effect": self.gross_effect.to_dict(),
            "maximum_effect": self.maximum_effect.to_dict(),
            "max_drawdown": self.max_drawdown.to_dict(),
            "mean_effect": self.mean_effect.to_dict(),
            "minimum_effect": self.minimum_effect.to_dict(),
            "reason": self.reason,
            "semantics": self.semantics,
            "unit": self.unit,
        }


@dataclass(frozen=True, slots=True)
class CostAnalytics:
    """Explicit cost components plus a compatible aggregate when one is meaningful."""

    applicability: AnalyticsApplicability
    reference_id: str | None
    components: tuple[CostComponentResult, ...]
    total: MetricValue
    reason: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "applicability": self.applicability.value,
            "components": [component.to_dict() for component in self.components],
            "reason": self.reason,
            "reference_id": self.reference_id,
            "total": self.total.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class StandardAnalyticsResult:
    """Deterministic machine-readable analytics result plus a small text report."""

    dataset_id: str
    dataset_version: str
    source_location: str
    computed_sha256: str
    observation_count: int
    decision_count: int
    diagnostic_count: int
    effects: EffectAnalytics
    costs: CostAnalytics
    net_effect: MetricValue
    trade_or_event_count: ActivityCount | NotApplicable

    def to_dict(self) -> dict[str, object]:
        return {
            "costs": self.costs.to_dict(),
            "primary_metrics": {
                "gross_effect": self.effects.gross_effect.to_dict(),
                "net_effect": self.net_effect.to_dict(),
            },
            "risk_metrics": {
                "max_drawdown": self.effects.max_drawdown.to_dict(),
            },
            "run_context": {
                "computed_sha256": self.computed_sha256,
                "dataset_id": self.dataset_id,
                "dataset_version": self.dataset_version,
                "source_location": self.source_location,
            },
            "schema_version": "2.0",
            "secondary_metrics": {
                "decision_count": self.decision_count,
                "diagnostic_count": self.diagnostic_count,
                "effect_count": self.effects.count.to_dict(),
                "effect_maximum": self.effects.maximum_effect.to_dict(),
                "effect_mean": self.effects.mean_effect.to_dict(),
                "effect_minimum": self.effects.minimum_effect.to_dict(),
                "observation_count": self.observation_count,
            },
            "trade_or_event_count": self.trade_or_event_count.to_dict(),
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )

    def to_markdown(self) -> str:
        lines = [
            "# ATS Standard Analytics",
            "",
            f"Dataset: {self.dataset_id}@{self.dataset_version}",
            f"Observations: {self.observation_count}",
            f"Decisions: {self.decision_count}",
            f"Diagnostics: {self.diagnostic_count}",
            "",
            "## Economic metrics",
            f"Gross effect: {_metric_text(self.effects.gross_effect)}",
            f"Modeled costs: {_metric_text(self.costs.total)}",
            f"Net effect: {_metric_text(self.net_effect)}",
            f"Max drawdown: {_metric_text(self.effects.max_drawdown)}",
            "",
            "## Activity",
            f"Trade/event count: {_activity_text(self.trade_or_event_count)}",
        ]
        return "\n".join(lines) + "\n"


def _applicable_metric(value: Numeric, *, unit: str | None = None) -> MetricValue:
    return MetricValue(
        applicability=AnalyticsApplicability.APPLICABLE,
        value=value,
        unit=unit,
    )


def _not_applicable_metric(reason: str) -> MetricValue:
    return MetricValue(
        applicability=AnalyticsApplicability.NOT_APPLICABLE,
        reason=reason,
    )


def _build_effect_analytics(effects: EffectSeries | NotApplicable) -> EffectAnalytics:
    if isinstance(effects, NotApplicable):
        metric = _not_applicable_metric(effects.reason)
        return EffectAnalytics(
            applicability=AnalyticsApplicability.NOT_APPLICABLE,
            semantics=None,
            unit=None,
            count=metric,
            gross_effect=metric,
            mean_effect=metric,
            minimum_effect=metric,
            maximum_effect=metric,
            max_drawdown=metric,
            reason=effects.reason,
        )

    values = tuple(float(value) for value in effects.increments)
    gross = math.fsum(values)
    count = len(values)

    if values:
        mean_metric = _applicable_metric(gross / count, unit=effects.unit)
        minimum_metric = _applicable_metric(min(values), unit=effects.unit)
        maximum_metric = _applicable_metric(max(values), unit=effects.unit)
    else:
        empty_reason = "effect series is empty"
        mean_metric = _not_applicable_metric(empty_reason)
        minimum_metric = _not_applicable_metric(empty_reason)
        maximum_metric = _not_applicable_metric(empty_reason)

    cumulative = 0.0
    peak = 0.0
    max_drawdown = 0.0
    for value in values:
        cumulative += value
        peak = max(peak, cumulative)
        max_drawdown = max(max_drawdown, peak - cumulative)

    return EffectAnalytics(
        applicability=AnalyticsApplicability.APPLICABLE,
        semantics=effects.semantics,
        unit=effects.unit,
        count=_applicable_metric(count, unit="effect-points"),
        gross_effect=_applicable_metric(gross, unit=effects.unit),
        mean_effect=mean_metric,
        minimum_effect=minimum_metric,
        maximum_effect=maximum_metric,
        max_drawdown=_applicable_metric(max_drawdown, unit=effects.unit),
    )


def _build_cost_analytics(costs: CostResult | NotApplicable) -> CostAnalytics:
    if isinstance(costs, NotApplicable):
        return CostAnalytics(
            applicability=AnalyticsApplicability.NOT_APPLICABLE,
            reference_id=None,
            components=(),
            total=_not_applicable_metric(costs.reason),
            reason=costs.reason,
        )

    applicable = tuple(
        component
        for component in costs.components
        if component.applicability is CostApplicability.APPLICABLE
    )
    if not applicable:
        total = _not_applicable_metric("cost result has no applicable components")
    else:
        units = {component.unit for component in applicable}
        if len(units) != 1:
            total = _not_applicable_metric("applicable cost components use incompatible units")
        else:
            unit = next(iter(units))
            total = _applicable_metric(
                math.fsum(float(component.value) for component in applicable),
                unit=unit,
            )

    return CostAnalytics(
        applicability=AnalyticsApplicability.APPLICABLE,
        reference_id=costs.reference_id,
        components=costs.components,
        total=total,
    )


def _build_net_effect(effects: EffectAnalytics, costs: CostAnalytics) -> MetricValue:
    gross = effects.gross_effect
    total_cost = costs.total

    if gross.applicability is AnalyticsApplicability.NOT_APPLICABLE:
        return _not_applicable_metric("gross effect is not applicable")
    if total_cost.applicability is AnalyticsApplicability.NOT_APPLICABLE:
        return _not_applicable_metric("modeled cost total is not applicable")
    if gross.unit != total_cost.unit:
        return _not_applicable_metric("gross effect and modeled costs use different units")

    assert gross.value is not None
    assert total_cost.value is not None
    return _applicable_metric(float(gross.value) - float(total_cost.value), unit=gross.unit)


def _metric_text(metric: MetricValue) -> str:
    if metric.applicability is AnalyticsApplicability.NOT_APPLICABLE:
        return f"NOT_APPLICABLE ({metric.reason})"
    suffix = f" {metric.unit}" if metric.unit else ""
    return f"{metric.value}{suffix}"


def _activity_text(activity: ActivityCount | NotApplicable) -> str:
    if isinstance(activity, NotApplicable):
        return f"NOT_APPLICABLE ({activity.reason})"
    return f"{activity.count} {activity.kind}"


def build_standard_analytics(
    replay: ReplayResult[object],
    *,
    effects: EffectSeries | NotApplicable,
    costs: CostResult | NotApplicable,
    trade_or_event_count: ActivityCount | NotApplicable,
) -> StandardAnalyticsResult:
    """Build deterministic baseline analytics without inventing missing semantics."""

    effect_analytics = _build_effect_analytics(effects)
    cost_analytics = _build_cost_analytics(costs)
    return StandardAnalyticsResult(
        dataset_id=replay.dataset_id,
        dataset_version=replay.dataset_version,
        source_location=replay.source_location,
        computed_sha256=replay.computed_sha256,
        observation_count=replay.observation_count,
        decision_count=len(replay.decisions),
        diagnostic_count=len(replay.diagnostics),
        effects=effect_analytics,
        costs=cost_analytics,
        net_effect=_build_net_effect(effect_analytics, cost_analytics),
        trade_or_event_count=trade_or_event_count,
    )
