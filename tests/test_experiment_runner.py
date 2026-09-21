from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
import yaml

from ats.analytics.standard import (
    ActivityCount,
    AnalyticsApplicability,
    EffectSeries,
)
from ats.costs.interface import (
    CostApplicability,
    CostComponentResult,
    CostInput,
    CostModel,
    CostModelConfig,
    CostResult,
)
from ats.replay.engine import ReplayResult
from ats.runner.experiment import (
    ExperimentRunError,
    ExperimentRuntime,
    RuntimeIdentity,
    load_registered_experiment_context,
    run_registered_experiment,
)
from ats.strategy.interface import (
    ResearchDecision,
    ResearchObservation,
    ResearchRunContext,
    ResearchStrategy,
    StrategyStep,
)

ROOT = Path(__file__).resolve().parents[1]
DATASET_MANIFEST = ROOT / "tests" / "fixtures" / "datasets" / "ordered_events.manifest.yaml"
COMPLETED_ON = datetime(2026, 1, 2, tzinfo=UTC)


def fixture_experiment_id() -> str:
    # Transient software-only identity; never written to experiments/ or REGISTRY.csv.
    return "EXP-" + "20990101" + "-001"


class FixtureStrategy(ResearchStrategy[int]):
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
        return StrategyStep(
            state=state + 1,
            decisions=(
                ResearchDecision(
                    decision_type="FIXTURE",
                    decision_time=observation.availability_time,
                    payload=(("value", observation.value("value")),),
                ),
            ),
        )


class FixtureCostModel(CostModel):
    def evaluate(self, cost_input: CostInput, config: CostModelConfig) -> CostResult:
        activity_units = dict(cost_input.attributes)["activity_units"]
        assert isinstance(activity_units, (int, float))
        results: list[CostComponentResult] = []
        for component in config.components:
            if component.applicability is CostApplicability.NOT_APPLICABLE:
                results.append(
                    CostComponentResult(
                        name=component.name,
                        applicability=component.applicability,
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
                    unit="fixture-units",
                )
            )
        return CostResult(reference_id=cost_input.reference_id, components=tuple(results))


def effect_builder(replay: ReplayResult[int]) -> EffectSeries:
    return EffectSeries(
        semantics="one synthetic effect unit per processed observation",
        unit="fixture-units",
        increments=tuple(1.0 for _ in replay.frames),
    )


def activity_builder(replay: ReplayResult[int]) -> ActivityCount:
    return ActivityCount(kind="synthetic_event", count=replay.observation_count)


def cost_input_builder(replay: ReplayResult[int]) -> CostInput:
    return CostInput(
        reference_id="fixture-run-costs",
        attributes=(("activity_units", replay.observation_count),),
    )


def runtime(*, code_revision: str = "fixture-revision") -> ExperimentRuntime[int]:
    return ExperimentRuntime(
        identity=RuntimeIdentity(
            code_revision=code_revision,
            implementation_reference="tests.fixture.FixtureStrategy",
            environment_id="ats-m2-fixture-env",
        ),
        strategy=FixtureStrategy(),
        effect_builder=effect_builder,
        activity_builder=activity_builder,
        cost_model=FixtureCostModel(),
        cost_input_builder=cost_input_builder,
    )


def registered_manifest() -> dict[str, object]:
    return {
        "schema_version": "2.0",
        "experiment": {
            "experiment_id": fixture_experiment_id(),
            "status": "REGISTERED",
            "evidence_class": "REGISTERED_EXPERIMENT",
            "research_stage": "RESEARCH",
            "created_on": "2099-01-01T00:00:00Z",
        },
        "registration": {
            "registered_on": "2099-01-01T00:00:00Z",
            "registered_by_role": "TEST_FIXTURE",
            "supersedes_experiment_id": None,
            "amendments": [],
        },
        "links": {
            "idea_id": "NOT_APPLICABLE",
            "hypothesis_id": "HYP-9999",
            "candidate_id": "NOT_APPLICABLE",
            "strategy_id": "NOT_APPLICABLE",
            "strategy_version": "NOT_APPLICABLE",
        },
        "reproducibility": {
            "code_revision": "fixture-revision",
            "implementation_reference": "tests.fixture.FixtureStrategy",
            "environment_id": "ats-m2-fixture-env",
            "dataset_id": "DATA-SYNTHETIC-LOADER-001",
            "source_snapshot_reference": "synthetic-loader-snapshot-v1",
            "data_period": "2026-01-01T00:00:00Z/2026-01-01T00:01:00Z",
            "universe_or_sampling_scope": "synthetic fixture",
            "transformation_reference": "identity://synthetic-loader-fixture",
            "parameters": {"start": 2},
            "configuration": {"mode": "fixture"},
            "random_seed": 7,
        },
        "assumptions": {
            "cost_model": {
                "components": [
                    {
                        "name": "fee",
                        "applicability": "APPLICABLE",
                        "parameters": {"per_unit": 0.5},
                        "reason": None,
                    },
                    {
                        "name": "slippage_proxy",
                        "applicability": "NOT_APPLICABLE",
                        "parameters": {},
                        "reason": "synthetic fixture excludes slippage",
                    },
                ]
            },
            "execution_model": "NOT_APPLICABLE",
            "known_data_limitations": "synthetic software fixture",
            "applicability_notes": "execution model is not applicable to the software fixture",
        },
        "question": {
            "predefined_question": "Can the synthetic runner reproduce the registered fixture?",
            "primary_metrics": ["gross_effect", "net_effect"],
            "secondary_metrics": [
                "observation_count",
                "max_drawdown",
                "costs",
                "trade_or_event_count",
            ],
            "metric_definitions": {},
            "predefined_decision_rule": "Software fixture must match exact expected output.",
        },
        "files": {
            "result_file": "result.json",
            "conclusion_file": "conclusion.md",
        },
    }


def write_manifest(tmp_path: Path, data: dict[str, object]) -> Path:
    path = tmp_path / "manifest.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def test_registered_manifest_runs_end_to_end_without_mutation(tmp_path: Path) -> None:
    path = write_manifest(tmp_path, registered_manifest())
    before = path.read_bytes()

    result = run_registered_experiment(
        path,
        DATASET_MANIFEST,
        root=ROOT,
        runtime=runtime(),
        completed_on=COMPLETED_ON,
    )

    assert path.read_bytes() == before
    payload = result.to_dict()
    assert payload["experiment_id"] == fixture_experiment_id()
    assert payload["run_context"]["registered_manifest_sha256"] == result.context.manifest_sha256
    assert payload["primary_metrics"]["gross_effect"]["value"] == 3.0
    assert payload["costs"]["total"]["value"] == 1.5
    assert payload["primary_metrics"]["net_effect"]["value"] == 1.5
    assert payload["trade_or_event_count"]["count"] == 3
    assert payload["reproducibility_status"] == "REGISTERED_CONTEXT_MATCH"


def test_repeated_registered_run_is_exactly_deterministic(tmp_path: Path) -> None:
    path = write_manifest(tmp_path, registered_manifest())

    first = run_registered_experiment(
        path,
        DATASET_MANIFEST,
        root=ROOT,
        runtime=runtime(),
        completed_on=COMPLETED_ON,
    )
    second = run_registered_experiment(
        path,
        DATASET_MANIFEST,
        root=ROOT,
        runtime=runtime(),
        completed_on=COMPLETED_ON,
    )

    assert first.to_json() == second.to_json()


def test_draft_manifest_is_rejected_before_execution(tmp_path: Path) -> None:
    manifest = registered_manifest()
    manifest["experiment"]["status"] = "DRAFT"  # type: ignore[index]
    path = write_manifest(tmp_path, manifest)

    with pytest.raises(ExperimentRunError, match="status must be REGISTERED"):
        load_registered_experiment_context(path)


def test_runtime_identity_must_match_registered_context(tmp_path: Path) -> None:
    path = write_manifest(tmp_path, registered_manifest())

    with pytest.raises(ExperimentRunError, match="code_revision does not match"):
        run_registered_experiment(
            path,
            DATASET_MANIFEST,
            root=ROOT,
            runtime=runtime(code_revision="different-revision"),
            completed_on=COMPLETED_ON,
        )


def test_dataset_identity_and_snapshot_are_frozen(tmp_path: Path) -> None:
    manifest = registered_manifest()
    manifest["reproducibility"]["dataset_id"] = "DATA-DIFFERENT-FIXTURE-001"  # type: ignore[index]
    path = write_manifest(tmp_path, manifest)

    with pytest.raises(ExperimentRunError, match="dataset_id does not match"):
        run_registered_experiment(
            path,
            DATASET_MANIFEST,
            root=ROOT,
            runtime=runtime(),
            completed_on=COMPLETED_ON,
        )

    manifest = registered_manifest()
    manifest["reproducibility"]["source_snapshot_reference"] = (  # type: ignore[index]
        "different-snapshot"
    )
    path = write_manifest(tmp_path, manifest)
    with pytest.raises(ExperimentRunError, match="source snapshot does not match"):
        run_registered_experiment(
            path,
            DATASET_MANIFEST,
            root=ROOT,
            runtime=runtime(),
            completed_on=COMPLETED_ON,
        )


def test_registered_metric_must_exist_in_standard_analytics(tmp_path: Path) -> None:
    manifest = registered_manifest()
    manifest["question"]["primary_metrics"] = ["unsupported_metric"]  # type: ignore[index]
    path = write_manifest(tmp_path, manifest)

    with pytest.raises(ExperimentRunError, match="registered metrics are not available"):
        run_registered_experiment(
            path,
            DATASET_MANIFEST,
            root=ROOT,
            runtime=runtime(),
            completed_on=COMPLETED_ON,
        )


def test_registered_cost_model_requires_runtime_cost_components(tmp_path: Path) -> None:
    path = write_manifest(tmp_path, registered_manifest())
    base = runtime()
    missing_cost_runtime = ExperimentRuntime(
        identity=base.identity,
        strategy=base.strategy,
        effect_builder=base.effect_builder,
        activity_builder=base.activity_builder,
    )

    with pytest.raises(ExperimentRunError, match="requires runtime cost model and input"):
        run_registered_experiment(
            path,
            DATASET_MANIFEST,
            root=ROOT,
            runtime=missing_cost_runtime,
            completed_on=COMPLETED_ON,
        )


def test_registered_not_applicable_costs_remain_explicit(tmp_path: Path) -> None:
    manifest = registered_manifest()
    manifest["assumptions"]["cost_model"] = "NOT_APPLICABLE"  # type: ignore[index]
    manifest["assumptions"]["applicability_notes"] = (  # type: ignore[index]
        "gross-only synthetic fixture"
    )
    manifest["question"]["primary_metrics"] = ["gross_effect"]  # type: ignore[index]
    path = write_manifest(tmp_path, manifest)
    base = runtime()
    gross_only_runtime = ExperimentRuntime(
        identity=base.identity,
        strategy=base.strategy,
        effect_builder=base.effect_builder,
        activity_builder=base.activity_builder,
    )

    result = run_registered_experiment(
        path,
        DATASET_MANIFEST,
        root=ROOT,
        runtime=gross_only_runtime,
        completed_on=COMPLETED_ON,
    )

    assert result.analytics.costs.total.applicability is AnalyticsApplicability.NOT_APPLICABLE
    assert result.analytics.net_effect.applicability is AnalyticsApplicability.NOT_APPLICABLE


def test_completed_on_must_be_explicit_and_timezone_aware(tmp_path: Path) -> None:
    path = write_manifest(tmp_path, registered_manifest())

    with pytest.raises(ValueError, match="completed_on must be timezone-aware"):
        run_registered_experiment(
            path,
            DATASET_MANIFEST,
            root=ROOT,
            runtime=runtime(),
            completed_on=datetime(2026, 1, 2),
        )
