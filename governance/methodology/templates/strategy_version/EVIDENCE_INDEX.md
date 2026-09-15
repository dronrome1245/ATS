# Strategy Version Evidence Index

## Identity

- Strategy ID: `null`
- Strategy Version: `null`

Canonical taxonomy:

`governance/methodology/EVIDENCE_TAXONOMY.md`

## Evidence table

| Source class | Qualified evidence class | Experiment / Report | Result / Status | Claim supported | Key limitations | Evidence status |
|---|---|---|---|---|---|---|
| `REGISTERED_EXPERIMENT` | `REGISTERED_EXPERIMENT` | `null` | `NOT_STARTED` | `null` | `null` | `CURRENT` |
| `REGISTERED_EXPERIMENT` | `VALIDATION_EVIDENCE` | `null` | `NOT_STARTED` | `null` | `null` | `CURRENT` |
| `REGISTERED_EXPERIMENT` | `INDEPENDENT_EXAMINATION_EVIDENCE` | `null` | `NOT_STARTED` | `null` | `null` | `CURRENT` |
| `REGISTERED_EXPERIMENT` | `STRESS_EVIDENCE` | `null` | `NOT_STARTED` | `null` | `null` | `CURRENT` |
| `DEMO_SHADOW_EVIDENCE` | `DEMO_SHADOW_EVIDENCE` | `null` | `NOT_STARTED` | `null` | `null` | `CURRENT` |
| `MINIMAL_LIVE_EVIDENCE` | `MINIMAL_LIVE_EVIDENCE` | `null` | `NOT_STARTED` | `null` | `null` | `CURRENT` |
| `ACTIVE_LIVE_EVIDENCE` | `ACTIVE_LIVE_EVIDENCE` | `null` | `NOT_STARTED` | `null` | `null` | `CURRENT` |
| `PORTFOLIO_EVIDENCE` | `PORTFOLIO_EVIDENCE` | `null` | `NOT_STARTED` | `null` | `null` | `CURRENT` |
| `SCALING_EVIDENCE` | `SCALING_EVIDENCE` | `null` | `NOT_STARTED` | `null` | `null` | `CURRENT` |

Allowed evidence status values:

`CURRENT / SUPERSEDED / INVALIDATED / HISTORICAL`

## Classification rules

- `source_class` records how the artifact was produced and does not change because a result is attractive.
- `qualified_evidence_class` records the strongest claim class whose protocol prerequisites are actually satisfied.
- `research_stage = VALIDATION` alone is not enough for `VALIDATION_EVIDENCE`.
- A failed validation or independent examination retains its qualified class and records `FAIL` as the result.
- Demo/shadow evidence does not prove profitability.
- Historical/backtest evidence does not prove live execution.
- Minimal-live evidence does not by itself justify scaling.

## Evidence integrity notes

Record here:

- which evidence blocks were revealed and therefore are no longer protected/independent for subsequent tuning;
- which experiments were invalidated by material change;
- which reports belong only to another Strategy Version;
- which known gaps block progression;
- which evidence was superseded but remains part of historical context;
- why each qualified class satisfies the prerequisites in `EVIDENCE_TAXONOMY.md`.

Evidence from another Strategy Version is not inherited automatically.

Material trade-affecting change requires a review of which evidence remains current and which stages must be repeated.
