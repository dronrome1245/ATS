from __future__ import annotations

import csv
import json
from pathlib import Path

from ats.analytics.standard import ActivityCount, EffectSeries, build_standard_analytics
from ats.costs.interface import (
    CostApplicability,
    CostComponentConfig,
    CostComponentResult,
    CostInput,
    CostModel,
    CostModelConfig,
    CostResult,
    apply_cost_model,
)
from ats.data.loader import load_dataset
from ats.replay.engine import run_replay
from ats.schemas.dataset_manifest import load_dataset_manifest
from ats.strategy.interface import (
    ResearchDecision,
    ResearchDiagnostic,
    ResearchObservation,
    ResearchRunContext,
    ResearchStrategy,
    StrategyStep,
)

ROOT = Path(__file__).resolve().parents[1]
DATASET_MANIFEST = ROOT / "tests" / "fixtures" / "datasets" / "ordered_events.manifest.yaml"
EXPECTED_RESULT = ROOT / "tests" / "fixtures" / "platform" / "reference_consumer_expected.json"
REGISTRY = ROOT / "experiments" / "REGISTRY.csv"


class AcceptanceStrategy(ResearchStrategy[int]):
    def initial_state(self, context: ResearchRunContext) -> int:
        start = dict(context.parameters).get("start", 0)
        assert isinstance(start, int)
        return start

    def on_observation(
        self,
        context: ResearchRunContext,
        observation: ResearchObservation,
        state: int,
    ) -> StrategyStep[int]:
        next_state = state + 1
        return StrategyStep(
            state=next_state,
            decisions=(
                ResearchDecision(
                    decision_type="M2_ACCEPTANCE",
                    decision_time=observation.availability_time,
                    payload=(
                        ("sequence", observation.sequence_index),
                        ("value", observation.value("value")),
                    ),
                ),
            ),
            diagnostics=(
                ResearchDiagnostic(
                    code="M2_ACCEPTANCE_STEP",
                    message="synthetic acceptance observation processed",
                    details=(("state_after", next_state),),
                ),
            ),
        )


class AcceptanceCostModel(CostModel):
    def evaluate(self, cost_input: CostInput, config: CostModelConfig) -> CostResult:
        event_count = dict(cost_input.attributes)["event_count"]
        assert isinstance(event_count, int)

        components: list[CostComponentResult] = []
        for component in config.components:
            if component.applicability is CostApplicability.NOT_APPLICABLE:
                components.append(
                    CostComponentResult(
                        name=component.name,
                        applicability=component.applicability,
                    )
                )
                continue

            per_event = dict(component.parameters)["per_event"]
            assert isinstance(per_event, (int, float))
            components.append(
                CostComponentResult(
                    name=component.name,
                    applicability=component.applicability,
                    value=event_count * per_event,
                    unit="fixture-units",
                )
            )

        return CostResult(
            reference_id=cost_input.reference_id,
            components=tuple(components),
        )


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _acceptance_run() -> dict[str, object]:
    manifest = load_dataset_manifest(DATASET_MANIFEST)
    loaded = load_dataset(manifest, root=ROOT)

    context = ResearchRunContext(
        configuration=(("mode", "acceptance-fixture"),),
        parameters=(("start", 2),),
        seed=17,
    )
    replay = run_replay(loaded, context, AcceptanceStrategy())

    cost_config = CostModelConfig(
        components=(
            CostComponentConfig(
                name="fee",
                applicability=CostApplicability.APPLICABLE,
                parameters=(("per_event", 0.25),),
            ),
            CostComponentConfig(
                name="slippage_proxy",
                applicability=CostApplicability.NOT_APPLICABLE,
                reason="synthetic acceptance fixture excludes slippage",
            ),
        )
    )
    costs = apply_cost_model(
        CostInput(
            reference_id="m2-acceptance-costs",
            attributes=(("event_count", replay.observation_count),),
        ),
        cost_config,
        AcceptanceCostModel(),
    )
    analytics = build_standard_analytics(
        replay,
        effects=EffectSeries(
            semantics="one synthetic effect unit per accepted fixture observation",
            unit="fixture-units",
            increments=tuple(1.0 for _ in replay.frames),
        ),
        costs=costs,
        trade_or_event_count=ActivityCount(
            kind="synthetic_event",
            count=replay.observation_count,
        ),
    )

    return {
        "analytics": analytics.to_dict(),
        "dataset": {
            "computed_sha256": loaded.computed_sha256,
            "dataset_id": loaded.dataset_id,
            "dataset_version": loaded.dataset_version,
            "dropped_malformed_count": loaded.dropped_malformed_count,
            "duplicate_discard_count": loaded.duplicate_discard_count,
            "missing_policy": loaded.missing_policy.value,
            "out_of_order_detected": loaded.out_of_order_detected,
            "source_location": loaded.source_location,
            "source_row_count": loaded.source_row_count,
        },
        "replay": {
            "decisions": [decision.to_dict() for decision in replay.decisions],
            "diagnostics": [diagnostic.to_dict() for diagnostic in replay.diagnostics],
            "final_state": replay.final_state,
            "initial_state": replay.initial_state,
        },
        "run_context": context.to_dict(),
        "schema_version": "m2-reference-consumer-1",
    }


def test_reference_consumer_acceptance_matches_committed_regression() -> None:
    expected = json.loads(EXPECTED_RESULT.read_text(encoding="utf-8"))

    assert _acceptance_run() == expected


def test_reference_consumer_acceptance_repeats_exactly() -> None:
    assert _canonical_json(_acceptance_run()) == _canonical_json(_acceptance_run())


def test_reference_consumer_fixture_preserves_cost_applicability() -> None:
    result = _acceptance_run()
    costs = result["analytics"]["costs"]  # type: ignore[index]
    components = costs["components"]  # type: ignore[index]

    assert costs["total"]["value"] == 0.75  # type: ignore[index]
    assert components[0]["name"] == "fee"
    assert components[0]["value"] == 0.75
    assert components[1]["name"] == "slippage_proxy"
    assert components[1]["applicability"] == "NOT_APPLICABLE"
    assert components[1]["value"] is None


def test_reference_consumer_fixture_has_no_formal_research_identity() -> None:
    expected_text = EXPECTED_RESULT.read_text(encoding="utf-8")
    for prefix in ("EXP-", "HYP-", "CAND-", "STRAT-"):
        assert prefix not in expected_text

    with REGISTRY.open(newline="", encoding="utf-8") as handle:
        assert list(csv.DictReader(handle)) == []
