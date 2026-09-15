# Data

## Purpose

`data/` stores Dataset Manifests, provenance and data-control metadata for ATS v2. Large, licensed or broker/vendor datasets are not committed to Git merely because a research run uses them.

## ATS v2 data rules

Every dataset used for formal research must become identifiable through a manifest that records, as applicable:

- stable dataset ID/version;
- source or source-snapshot reference;
- schema/reference format;
- coverage/period;
- timezone and timestamp semantics;
- ordering/tie-breaking semantics;
- missing/bad/duplicate-data policy;
- transformation/preparation reference;
- checksum/hash where practical;
- known limitations and licensing/storage constraints.

A material cleaning/transformation change creates a new dataset version/context rather than silently changing historical evidence.

Development, validation and independent evidence partitions are governed by the current Research Methodology and Strategy Lifecycle. A protected evidence block stops being independent after it is revealed/used for the corresponding decision.

## M2 boundary

`WBS-2.3` will implement Dataset Manifest support and `WBS-2.4` the deterministic base loader.

M2 may use synthetic non-market fixtures for software tests. Such fixtures are platform-test inputs only: they do not receive research entity/Experiment IDs and are not trading evidence.

No real data source, instrument or period has been selected yet. Reference Strategy #1 remains M3 work.
