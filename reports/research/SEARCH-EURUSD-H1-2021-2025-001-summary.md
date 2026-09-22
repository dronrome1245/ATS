# First Bounded Discovery Result — SEARCH-EURUSD-H1-2021-2025-001

**Task:** `ATS2-M6-001`  
**Work package:** `WBS-6.0`  
**Evidence class:** `EXPLORATORY_OBSERVATION`  
**Outcome:** `SHORTLIST_FOR_IDEA_INTAKE`  
**Observed on exact task commit:** `d08e11f236c2318269314de64da85a7eacbb9105`

## Identity and reproducibility

- Search Manifest: `research/discovery/SEARCH-EURUSD-H1-2021-2025-001.yaml`
- Dataset: `DATA-DUKASCOPY-EURUSDH1-PROTO01-001@1.0.0`
- Dataset SHA-256: `aeda05d90994259a22e25d882398218aead968941fe0b1c73eb34894841291c0`
- Frozen implementation revision: `2e339ff9b1f1cbd6e48250a5202cc3e3294de59d`
- Search Manifest SHA-256: `759b74e55b1db1a5b272609dcccd94a1e4a00d2f076d46b79e47289adffd3117`
- Reviewed runtime result SHA-256: `2f363b3fcdc3f80600bf1f488197f9f848ad8b286248c611ff2aa8d71ac6a318`
- Evaluated alternatives: `16 / 16`
- Selection policy: `PREDECLARED_SHORTLIST_RULE_ONLY`

## Full denominator

| Alternative | Family | Dir | LB | Tail | H | N | Mean bps | Excess bps | Median bps | Positive | Overlap | Short |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| `alt-01-lb6-high-cont-6h` | CONTINUATION | UP | 6H | HIGH | 6H | 2319 | -0.5546 | -0.1647 | -0.4901 | 48.73% | 73.74% | NO |
| `alt-02-lb6-high-cont-24h` | CONTINUATION | UP | 6H | HIGH | 24H | 2319 | -2.4198 | -1.7824 | -5.7100 | 44.55% | 84.65% | NO |
| `alt-03-lb6-low-cont-6h` | CONTINUATION | DOWN | 6H | LOW | 6H | 2319 | -0.8380 | -0.3371 | -1.6153 | 46.92% | 74.17% | NO |
| `alt-04-lb6-low-cont-24h` | CONTINUATION | DOWN | 6H | LOW | 24H | 2319 | -3.5769 | -3.5386 | -1.3296 | 48.47% | 84.22% | NO |
| `alt-05-lb6-high-rev-6h` | REVERSAL | DOWN | 6H | HIGH | 6H | 2319 | -0.4159 | 0.0850 | -0.4817 | 48.51% | 73.74% | NO |
| `alt-06-lb6-high-rev-24h` | REVERSAL | DOWN | 6H | HIGH | 24H | 2319 | 1.8375 | 1.8758 | 4.6632 | 54.51% | 84.65% | YES |
| `alt-07-lb6-low-rev-6h` | REVERSAL | UP | 6H | LOW | 6H | 2319 | -0.1663 | 0.2235 | 0.5524 | 50.88% | 74.17% | NO |
| `alt-08-lb6-low-rev-24h` | REVERSAL | UP | 6H | LOW | 24H | 2319 | 2.9777 | 3.6151 | 0.1876 | 50.19% | 84.22% | YES |
| `alt-09-lb24-high-cont-6h` | CONTINUATION | UP | 24H | HIGH | 6H | 1849 | -0.6508 | -0.1633 | -1.4802 | 46.62% | 87.99% | NO |
| `alt-10-lb24-high-cont-24h` | CONTINUATION | UP | 24H | HIGH | 24H | 1849 | -4.6340 | -3.9869 | -9.9761 | 42.56% | 90.10% | NO |
| `alt-11-lb24-low-cont-6h` | CONTINUATION | DOWN | 24H | LOW | 6H | 1849 | -2.3393 | -1.9635 | -3.0510 | 42.18% | 87.34% | NO |
| `alt-12-lb24-low-cont-24h` | CONTINUATION | DOWN | 24H | LOW | 24H | 1849 | -3.0919 | -3.0798 | 0.3989 | 50.24% | 89.45% | NO |
| `alt-13-lb24-high-rev-6h` | REVERSAL | DOWN | 24H | HIGH | 6H | 1849 | -0.2686 | 0.1072 | 0.4804 | 50.62% | 87.99% | NO |
| `alt-14-lb24-high-rev-24h` | REVERSAL | DOWN | 24H | HIGH | 24H | 1849 | 4.0202 | 4.0323 | 9.1686 | 56.35% | 90.10% | YES |
| `alt-15-lb24-low-rev-6h` | REVERSAL | UP | 24H | LOW | 6H | 1849 | 1.3849 | 1.8724 | 2.3055 | 55.16% | 87.34% | YES |
| `alt-16-lb24-low-rev-24h` | REVERSAL | UP | 24H | LOW | 24H | 1849 | 2.3836 | 3.0308 | -1.2413 | 48.46% | 89.45% | YES |

## Family-level observations

- continuation: `0 / 8` shortlisted;
- reversal: `5 / 8` shortlisted;
- 24H-effect reversal: `4 / 4` shortlisted;
- 6H-effect reversal: `1 / 4` shortlisted.

The observation carried forward is `TWO_SIDED_RETURN_TAIL_REVERSAL`.

No exact lookback, tail threshold or effect/holding horizon is selected by this result review.

## Limitations

- The 2021–2025 EURUSD H1 block is development-known.
- Shortlisted 24H variants have approximately `84%–90%` overlap.
- Commission and financing were not modeled.
- The search inspected 16 alternatives, so later work inherits selection history.
- `alt-16` has a positive mean/excess but negative median and positive share below 50%.
- This result is exploratory, not validation evidence.

## Decision

`SHORTLIST_FOR_IDEA_INTAKE`

A later Hypothesis must cite the full 16-alternative history, freeze one formulation before new confirmatory data, and must not relabel this already revealed block as protected evidence.
