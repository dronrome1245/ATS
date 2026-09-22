"""Reusable ATS bounded market-pattern discovery capability."""

from ats.discovery.bounded import (
    DiscoveryAlternative,
    DiscoveryContractError,
    DiscoveryPoint,
    DiscoveryResult,
    Evaluator,
    ParameterAssignment,
    SearchManifest,
    ShortlistOperator,
    ShortlistRule,
    load_search_manifest,
    parse_search_manifest,
    run_bounded_discovery,
)

__all__ = [
    "DiscoveryAlternative",
    "DiscoveryContractError",
    "DiscoveryPoint",
    "DiscoveryResult",
    "Evaluator",
    "ParameterAssignment",
    "SearchManifest",
    "ShortlistOperator",
    "ShortlistRule",
    "load_search_manifest",
    "parse_search_manifest",
    "run_bounded_discovery",
]
