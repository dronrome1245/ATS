"""EUR/USD H1 return-tail evaluator for the first bounded ATS discovery run."""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass
from datetime import datetime, timedelta

import numpy as np

from ats.discovery.bounded import DiscoveryAlternative, SearchManifest


class EurusdH1DiscoveryError(ValueError):
    """Raised when the frozen EUR/USD H1 discovery contract is violated."""


@dataclass(frozen=True, slots=True)
class PriceBar:
    event_time: datetime
    bid_open: float
    bid_close: float
    ask_open: float
    ask_close: float

    def __post_init__(self) -> None:
        if self.event_time.tzinfo is None or self.event_time.utcoffset() is None:
            raise EurusdH1DiscoveryError("bar event_time must be timezone-aware")
        prices = (self.bid_open, self.bid_close, self.ask_open, self.ask_close)
        if any(not math.isfinite(value) or value <= 0 for value in prices):
            raise EurusdH1DiscoveryError("bar prices must be finite and positive")
        if self.ask_open < self.bid_open or self.ask_close < self.bid_close:
            raise EurusdH1DiscoveryError("ASK price must not be below BID price")

    @property
    def mid_close(self) -> float:
        return (self.bid_close + self.ask_close) / 2.0


@dataclass(frozen=True, slots=True)
class AlternativeSpec:
    lookback_hours: int
    tail_quantile: float
    tail: str
    forward_hours: int
    expected_direction: str


class EurusdH1Evaluator:
    """Evaluate one frozen family of return-tail continuation/reversal alternatives."""

    def __init__(self, bars: tuple[PriceBar, ...], manifest: SearchManifest) -> None:
        if len(bars) < 3:
            raise EurusdH1DiscoveryError("at least three bars are required")
        ordered_pairs = zip(bars, bars[1:])
        if any(current.event_time <= previous.event_time for previous, current in ordered_pairs):
            raise EurusdH1DiscoveryError("bars must be strictly ordered by event_time")

        self._bars = bars
        self._specs = {
            alternative.alternative_id: self._parse_alternative(alternative)
            for alternative in manifest.alternatives
        }
        self._max_forward = max(spec.forward_hours for spec in self._specs.values())
        self._eligible: dict[int, tuple[int, ...]] = {}
        self._prior_returns: dict[int, dict[int, float]] = {}
        self._prepare_eligibility()

    @staticmethod
    def _parameter_map(alternative: DiscoveryAlternative) -> dict[str, object]:
        values = {parameter.name: parameter.value for parameter in alternative.parameters}
        expected = {"lookback_hours", "tail_quantile", "tail"}
        if set(values) != expected:
            raise EurusdH1DiscoveryError(
                "alternative "
                f"{alternative.alternative_id!r} parameter set must be {sorted(expected)}"
            )
        return values

    def _parse_alternative(self, alternative: DiscoveryAlternative) -> AlternativeSpec:
        if alternative.feature_condition != "PRIOR_MID_CLOSE_RETURN_QUANTILE":
            raise EurusdH1DiscoveryError("unsupported feature_condition")
        if alternative.pattern_family not in {
            "RETURN_TAIL_CONTINUATION",
            "RETURN_TAIL_REVERSAL",
        }:
            raise EurusdH1DiscoveryError("unsupported pattern_family")

        values = self._parameter_map(alternative)
        lookback = values["lookback_hours"]
        quantile = values["tail_quantile"]
        tail = values["tail"]
        if isinstance(lookback, bool) or not isinstance(lookback, int) or lookback <= 0:
            raise EurusdH1DiscoveryError("lookback_hours must be a positive integer")
        if isinstance(quantile, bool) or not isinstance(quantile, (int, float)):
            raise EurusdH1DiscoveryError("tail_quantile must be numeric")
        quantile = float(quantile)
        if not 0.0 < quantile < 0.5:
            raise EurusdH1DiscoveryError("tail_quantile must be between 0 and 0.5")
        if tail not in {"HIGH", "LOW"}:
            raise EurusdH1DiscoveryError("tail must be HIGH or LOW")

        if not alternative.horizon.endswith("H"):
            raise EurusdH1DiscoveryError("horizon must use <hours>H form")
        try:
            forward = int(alternative.horizon[:-1])
        except ValueError as exc:
            raise EurusdH1DiscoveryError("horizon must use <hours>H form") from exc
        if forward <= 0:
            raise EurusdH1DiscoveryError("forward horizon must be positive")

        continuation_direction = "UP" if tail == "HIGH" else "DOWN"
        if alternative.pattern_family == "RETURN_TAIL_CONTINUATION":
            expected_direction = continuation_direction
        else:
            expected_direction = "DOWN" if continuation_direction == "UP" else "UP"
        if alternative.direction != expected_direction:
            raise EurusdH1DiscoveryError("alternative.direction does not match pattern semantics")

        return AlternativeSpec(
            lookback_hours=lookback,
            tail_quantile=quantile,
            tail=tail,
            forward_hours=forward,
            expected_direction=expected_direction,
        )

    def _is_contiguous(self, start: int, end: int) -> bool:
        return all(
            self._bars[index].event_time - self._bars[index - 1].event_time
            == timedelta(hours=1)
            for index in range(start + 1, end + 1)
        )

    def _prepare_eligibility(self) -> None:
        for lookback in sorted({spec.lookback_hours for spec in self._specs.values()}):
            indices: list[int] = []
            prior_returns: dict[int, float] = {}
            final_signal_index = len(self._bars) - self._max_forward - 2
            for index in range(lookback, final_signal_index + 1):
                end = index + 1 + self._max_forward
                if not self._is_contiguous(index - lookback, end):
                    continue
                prior = self._bars[index].mid_close / self._bars[index - lookback].mid_close - 1.0
                indices.append(index)
                prior_returns[index] = prior
            if not indices:
                raise EurusdH1DiscoveryError(f"no eligible observations for lookback {lookback}")
            self._eligible[lookback] = tuple(indices)
            self._prior_returns[lookback] = prior_returns

    def _threshold(self, spec: AlternativeSpec) -> float:
        values = tuple(self._prior_returns[spec.lookback_hours].values())
        level = 1.0 - spec.tail_quantile if spec.tail == "HIGH" else spec.tail_quantile
        return float(np.quantile(values, level))

    def _forward_return(self, index: int, spec: AlternativeSpec) -> float:
        entry = self._bars[index + 1]
        exit_bar = self._bars[index + 1 + spec.forward_hours]
        if spec.expected_direction == "UP":
            return exit_bar.bid_open / entry.ask_open - 1.0
        return entry.bid_open / exit_bar.ask_open - 1.0

    @staticmethod
    def _overlap_share(indices: list[int], forward_hours: int) -> float:
        if not indices:
            return 0.0
        overlaps = 0
        previous_exit: int | None = None
        for index in indices:
            entry = index + 1
            exit_index = entry + forward_hours
            if previous_exit is not None and entry <= previous_exit:
                overlaps += 1
            previous_exit = max(previous_exit or exit_index, exit_index)
        return overlaps / len(indices)

    def __call__(self, alternative: DiscoveryAlternative) -> dict[str, int | float]:
        spec = self._specs[alternative.alternative_id]
        threshold = self._threshold(spec)
        eligible = self._eligible[spec.lookback_hours]
        prior_returns = self._prior_returns[spec.lookback_hours]

        event_indices = [
            index
            for index in eligible
            if (
                prior_returns[index] >= threshold
                if spec.tail == "HIGH"
                else prior_returns[index] <= threshold
            )
        ]
        if not event_indices:
            raise EurusdH1DiscoveryError("tail condition produced zero events")

        event_returns = [self._forward_return(index, spec) for index in event_indices]
        baseline_returns = [self._forward_return(index, spec) for index in eligible]
        mean_return = statistics.fmean(event_returns)
        baseline_mean = statistics.fmean(baseline_returns)
        excess = mean_return - baseline_mean

        return {
            "event_count": len(event_returns),
            "mean_signed_forward_return": mean_return,
            "mean_excess_vs_baseline": excess,
            "median_signed_forward_return": statistics.median(event_returns),
            "positive_share": sum(value > 0 for value in event_returns) / len(event_returns),
            "overlap_share": self._overlap_share(event_indices, spec.forward_hours),
            "shortlist_score": min(mean_return, excess),
        }


__all__ = [
    "AlternativeSpec",
    "EurusdH1DiscoveryError",
    "EurusdH1Evaluator",
    "PriceBar",
]
