"""Manifest-driven deterministic experiment runner for ATS M2."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Generic, TypeVar

import yaml

from ats.analytics.standard import (
    ActivityCount,
    EffectSeries,
    NotApplicable,
    StandardAnalyticsResult,
    build_standard_analytics,
)
from ats.costs.interface import (
    CostApplicability,
    CostComponentConfig,
    CostInput,
    CostModel,
    CostModelConfig,
    CostResult,
    apply_cost_model,
)
from ats.data.loader import load_dataset
from ats.replay.engine import ReplayResult, run_replay
from ats.schemas.dataset_manifest import load_dataset_manifest
from ats.strategy.interface import JsonScalar, ResearchRunContext, ResearchStrategy

StateT = TypeVar("StateT")
EXPERIMENT_ID_RE = re.compile(r"^EXP-\d{8}-\d{3}$")


class ExperimentRunError(ValueError):
    """Raised when registered context and actual runtime inputs do not match."""


def _mapping(value: object, *, label: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ExperimentRunError(f"{label} must be a string-keyed mapping")
    return value


def _required_text(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExperimentRunError(f"{label} must be a non-empty string")
    return value


def _scalar_pairs(value: object, *, label: str) -> tuple[tuple[str, JsonScalar], ...]:
    mapping = _mapping(value, label=label)
    pairs: list[tuple[str, JsonScalar]] = []
    for key, item in mapping.items():
        if not key:
            raise ExperimentRunError(f"{label} keys must be non-empty")
        if item is not None and not isinstance(item, (str, int, float, bool)):
            raise ExperimentRunError(f"{label} values must be JSON scalars")
        if isinstance(item, float) and not math.isfinite(item):
            raise ExperimentRunError(f"{label} float values must be finite")
        pairs.append((key, item))
    return tuple(pairs)


def _string_tuple(value: object, *, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ExperimentRunError(f"{label} must be a list")
    return tuple(_required_text(item, label=f"{label} item") for item in value)


def _parse_seed(value: object) -> tuple[int | None, int | str]:
    if value == "NOT_APPLICABLE":
        return None, "NOT_APPLICABLE"
    if isinstance(value, bool) or not isinstance(value, int):
        raise ExperimentRunError(
            "reproducibility.random_seed must be an integer or NOT_APPLICABLE"
        )
    return value, value


def _parse_cost_config(
    value: object,
    *,
    applicability_notes: object,
) -> tuple[CostModelConfig | None, str | None]:
    if value == "NOT_APPLICABLE":
        reason = _required_text(
            applicability_notes,
            label="assumptions.applicability_notes for NOT_APPLICABLE cost_model",
        )
        return None, reason

    mapping = _mapping(value, label="assumptions.cost_model")
    raw_components = mapping.get("components")
    if not isinstance(raw_components, list) or not raw_components:
        raise ExperimentRunError("assumptions.cost_model.components must be a non-empty list")

    components: list[CostComponentConfig] = []
    for index, raw_component in enumerate(raw_components):
        component = _mapping(raw_component, label=f"cost component {index}")
        name = _required_text(component.get("name"), label=f"cost component {index}.name")
        try:
            applicability = CostApplicability(component.get("applicability"))
        except ValueError as exc:
            raise ExperimentRunError(
                f"cost component {name!r} has invalid applicability"
            ) from exc
        parameters = _scalar_pairs(
            component.get("parameters", {}),
            label=f"cost component {name!r}.parameters",
        )
        reason = component.get("reason")
        if reason is not None:
            reason = _required_text(reason, label=f"cost component {name!r}.reason")
        components.append(
            CostComponentConfig(
                name=name,
                applicability=applicability,
                parameters=parameters,
                reason=reason,
            )
        )

    return CostModelConfig(components=tuple(components)), None


@dataclass(frozen=True, slots=True)
class RegisteredExperimentContext:
    """Frozen subset of a registered Experiment manifest used by the M2 runner."""

    experiment_id: str
    research_stage: str
    registered_on: str
    hypothesis_id: str
    code_revision: str
    implementation_reference: str
    environment_id: str
    dataset_id: str
    source_snapshot_reference: str
    data_period: str
    parameters: tuple[tuple[str, JsonScalar], ...]
    configuration: tuple[tuple[str, JsonScalar], ...]
    seed: int | None
    registered_random_seed: int | str
    cost_config: CostModelConfig | None
    cost_not_applicable_reason: str | None
    primary_metrics: tuple[str, ...]
    secondary_metrics: tuple[str, ...]
    decision_rule: str
    manifest_sha256: str

    def research_context(self) -> ResearchRunContext:
        return ResearchRunContext(
            configuration=self.configuration,
            parameters=self.parameters,
            seed=self.seed,
        )


@dataclass(frozen=True, slots=True)
class RuntimeIdentity:
    """Actual resolved runtime identity supplied explicitly to the runner."""

    code_revision: str
    implementation_reference: str
    environment_id: str

    def __post_init__(self) -> None:
        for label, value in (
            ("code_revision", self.code_revision),
            ("implementation_reference", self.implementation_reference),
            ("environment_id", self.environment_id),
        ):
            if not value:
                raise ValueError(f"runtime {label} must be non-empty")


@dataclass(frozen=True, slots=True)
class ExperimentRuntime(Generic[StateT]):
    """Pre-resolved typed runtime components; no dynamic imports from manifest text."""

    identity: RuntimeIdentity
    strategy: ResearchStrategy[StateT]
    effect_builder: Callable[[ReplayResult[StateT]], EffectSeries | NotApplicable]
    activity_builder: Callable[[ReplayResult[StateT]], ActivityCount | NotApplicable]
    cost_model: CostModel | None = None
    cost_input_builder: Callable[[ReplayResult[StateT]], CostInput] | None = None


@dataclass(frozen=True, slots=True)
class ExperimentRunResult:
    """Machine-readable result compatible with the registered Experiment result vocabulary."""

    context: RegisteredExperimentContext
    completed_on: datetime
    analytics: StandardAnalyticsResult
    dataset_version: str
    computed_sha256: str
    diagnostics: tuple[dict[str, object], ...]
    artifacts: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.completed_on.tzinfo is None or self.completed_on.utcoffset() is None:
            raise ValueError("completed_on must be timezone-aware")
        if any(not artifact for artifact in self.artifacts):
            raise ValueError("artifact references must be non-empty")

    def to_dict(self) -> dict[str, object]:
        analytics = self.analytics.to_dict()
        return {
            "anomalies_or_execution_notes": list(self.diagnostics),
            "artifacts": list(self.artifacts),
            "completed_on": self.completed_on.isoformat(),
            "costs": analytics["costs"],
            "experiment_id": self.context.experiment_id,
            "machine_outcome": None,
            "primary_metrics": analytics["primary_metrics"],
            "reproducibility_status": "REGISTERED_CONTEXT_MATCH",
            "risk_metrics": analytics["risk_metrics"],
            "run_context": {
                "code_revision": self.context.code_revision,
                "computed_sha256": self.computed_sha256,
                "data_period": self.context.data_period,
                "dataset_id": self.context.dataset_id,
                "dataset_version": self.dataset_version,
                "environment_id": self.context.environment_id,
                "implementation_reference": self.context.implementation_reference,
                "random_seed": self.context.registered_random_seed,
                "registered_manifest_sha256": self.context.manifest_sha256,
                "source_snapshot_reference": self.context.source_snapshot_reference,
            },
            "schema_version": "2.0",
            "secondary_metrics": analytics["secondary_metrics"],
            "trade_or_event_count": analytics["trade_or_event_count"],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )


def load_registered_experiment_context(path: str | Path) -> RegisteredExperimentContext:
    """Read and validate a registered manifest without modifying preregistration content."""

    manifest_path = Path(path)
    raw_bytes = manifest_path.read_bytes()
    try:
        parsed = yaml.safe_load(raw_bytes.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise ExperimentRunError("experiment manifest must be UTF-8") from exc

    root = _mapping(parsed, label="experiment manifest")
    if root.get("schema_version") != "2.0":
        raise ExperimentRunError("experiment manifest schema_version must be 2.0")

    experiment = _mapping(root.get("experiment"), label="experiment")
    experiment_id = _required_text(experiment.get("experiment_id"), label="experiment_id")
    if EXPERIMENT_ID_RE.fullmatch(experiment_id) is None:
        raise ExperimentRunError("experiment_id must match EXP-YYYYMMDD-nnn")
    if experiment.get("status") != "REGISTERED":
        raise ExperimentRunError("experiment status must be REGISTERED before runner execution")
    if experiment.get("evidence_class") != "REGISTERED_EXPERIMENT":
        raise ExperimentRunError("experiment evidence_class must be REGISTERED_EXPERIMENT")
    research_stage = _required_text(
        experiment.get("research_stage"),
        label="experiment.research_stage",
    )

    registration = _mapping(root.get("registration"), label="registration")
    registered_on = _required_text(
        registration.get("registered_on"),
        label="registration.registered_on",
    )
    _required_text(
        registration.get("registered_by_role"),
        label="registration.registered_by_role",
    )

    links = _mapping(root.get("links"), label="links")
    hypothesis_id = _required_text(links.get("hypothesis_id"), label="links.hypothesis_id")

    reproducibility = _mapping(root.get("reproducibility"), label="reproducibility")
    code_revision = _required_text(
        reproducibility.get("code_revision"),
        label="reproducibility.code_revision",
    )
    implementation_reference = _required_text(
        reproducibility.get("implementation_reference"),
        label="reproducibility.implementation_reference",
    )
    environment_id = _required_text(
        reproducibility.get("environment_id"),
        label="reproducibility.environment_id",
    )
    dataset_id = _required_text(
        reproducibility.get("dataset_id"),
        label="reproducibility.dataset_id",
    )
    source_snapshot_reference = _required_text(
        reproducibility.get("source_snapshot_reference"),
        label="reproducibility.source_snapshot_reference",
    )
    data_period = _required_text(
        reproducibility.get("data_period"),
        label="reproducibility.data_period",
    )
    parameters = _scalar_pairs(
        reproducibility.get("parameters", {}),
        label="reproducibility.parameters",
    )
    configuration = _scalar_pairs(
        reproducibility.get("configuration", {}),
        label="reproducibility.configuration",
    )
    seed, registered_random_seed = _parse_seed(reproducibility.get("random_seed"))

    assumptions = _mapping(root.get("assumptions"), label="assumptions")
    cost_config, cost_reason = _parse_cost_config(
        assumptions.get("cost_model"),
        applicability_notes=assumptions.get("applicability_notes"),
    )

    question = _mapping(root.get("question"), label="question")
    primary_metrics = _string_tuple(
        question.get("primary_metrics"),
        label="question.primary_metrics",
    )
    if not primary_metrics:
        raise ExperimentRunError("question.primary_metrics must not be empty for M2 runner")
    secondary_metrics = _string_tuple(
        question.get("secondary_metrics", []),
        label="question.secondary_metrics",
    )
    decision_rule = _required_text(
        question.get("predefined_decision_rule"),
        label="question.predefined_decision_rule",
    )

    return RegisteredExperimentContext(
        experiment_id=experiment_id,
        research_stage=research_stage,
        registered_on=registered_on,
        hypothesis_id=hypothesis_id,
        code_revision=code_revision,
        implementation_reference=implementation_reference,
        environment_id=environment_id,
        dataset_id=dataset_id,
        source_snapshot_reference=source_snapshot_reference,
        data_period=data_period,
        parameters=parameters,
        configuration=configuration,
        seed=seed,
        registered_random_seed=registered_random_seed,
        cost_config=cost_config,
        cost_not_applicable_reason=cost_reason,
        primary_metrics=primary_metrics,
        secondary_metrics=secondary_metrics,
        decision_rule=decision_rule,
        manifest_sha256=hashlib.sha256(raw_bytes).hexdigest(),
    )


def _validate_runtime_identity(
    context: RegisteredExperimentContext,
    identity: RuntimeIdentity,
) -> None:
    for label, registered, actual in (
        ("code_revision", context.code_revision, identity.code_revision),
        (
            "implementation_reference",
            context.implementation_reference,
            identity.implementation_reference,
        ),
        ("environment_id", context.environment_id, identity.environment_id),
    ):
        if registered != actual:
            raise ExperimentRunError(
                f"runtime {label} does not match registered manifest: "
                f"registered={registered!r}, actual={actual!r}"
            )


def _validate_registered_metrics(
    context: RegisteredExperimentContext,
    analytics: StandardAnalyticsResult,
) -> None:
    payload = analytics.to_dict()
    available = set(payload["primary_metrics"])
    available.update(payload["secondary_metrics"])
    available.update(payload["risk_metrics"])
    available.update(("costs", "trade_or_event_count"))

    missing = [
        name
        for name in context.primary_metrics + context.secondary_metrics
        if name not in available
    ]
    if missing:
        raise ExperimentRunError(
            "registered metrics are not available from standard analytics: " + ", ".join(missing)
        )


def run_registered_experiment(
    manifest_path: str | Path,
    dataset_manifest_path: str | Path,
    *,
    root: str | Path,
    runtime: ExperimentRuntime[StateT],
    completed_on: datetime,
    artifacts: tuple[str, ...] = (),
) -> ExperimentRunResult:
    """Run one frozen registered context through loader, replay, costs and analytics."""

    context = load_registered_experiment_context(manifest_path)
    _validate_runtime_identity(context, runtime.identity)

    dataset_manifest = load_dataset_manifest(dataset_manifest_path)
    if dataset_manifest.dataset_id != context.dataset_id:
        raise ExperimentRunError(
            "dataset_id does not match registered manifest: "
            f"registered={context.dataset_id!r}, actual={dataset_manifest.dataset_id!r}"
        )
    if dataset_manifest.source.snapshot_reference != context.source_snapshot_reference:
        raise ExperimentRunError("dataset source snapshot does not match registered manifest")

    loaded = load_dataset(dataset_manifest, root=root)
    replay = run_replay(loaded, context.research_context(), runtime.strategy)

    if context.cost_config is None:
        if runtime.cost_model is not None or runtime.cost_input_builder is not None:
            raise ExperimentRunError(
                "registered cost_model is NOT_APPLICABLE but runtime supplied cost components"
            )
        costs: CostResult | NotApplicable = NotApplicable(
            context.cost_not_applicable_reason or "registered cost model is not applicable"
        )
    else:
        if runtime.cost_model is None or runtime.cost_input_builder is None:
            raise ExperimentRunError("registered cost_model requires runtime cost model and input")
        cost_input = runtime.cost_input_builder(replay)
        if not isinstance(cost_input, CostInput):
            raise ExperimentRunError("runtime cost_input_builder must return CostInput")
        costs = apply_cost_model(cost_input, context.cost_config, runtime.cost_model)

    effects = runtime.effect_builder(replay)
    if not isinstance(effects, (EffectSeries, NotApplicable)):
        raise ExperimentRunError("runtime effect_builder returned unsupported analytics input")
    activity = runtime.activity_builder(replay)
    if not isinstance(activity, (ActivityCount, NotApplicable)):
        raise ExperimentRunError("runtime activity_builder returned unsupported analytics input")

    analytics = build_standard_analytics(
        replay,
        effects=effects,
        costs=costs,
        trade_or_event_count=activity,
    )
    _validate_registered_metrics(context, analytics)

    diagnostics = tuple(diagnostic.to_dict() for diagnostic in replay.diagnostics)
    return ExperimentRunResult(
        context=context,
        completed_on=completed_on,
        analytics=analytics,
        dataset_version=loaded.dataset_version,
        computed_sha256=loaded.computed_sha256,
        diagnostics=diagnostics,
        artifacts=artifacts,
    )
