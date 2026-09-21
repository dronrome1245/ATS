# Reports

`reports/` stores derived human-readable research, validation, execution and portfolio reports. Reports summarize evidence; they do not become a second source of truth for Experiment inputs/results.

A formal report should link, as applicable, to:

- Experiment ID;
- Strategy / Strategy Version;
- code revision and environment;
- Dataset ID/version and period;
- configuration/parameters;
- cost/execution assumptions;
- `source_class` and `qualified_evidence_class`;
- applicable lifecycle/review decision.

A report never upgrades evidence class or changes a lifecycle/research decision automatically. The underlying Experiment/Evidence artifacts and explicit review decision remain authoritative.

M2 `WBS-2.8` materializes the minimum standard analytics/report output in `ats.analytics.standard`.

The baseline keeps gross effect, explicit modeled costs and net effect separate; exposes deterministic effect distribution/path metrics only when their semantics are declared; requires explicit applicability for trade/event counts; and renders canonical JSON plus a minimum deterministic Markdown report.

It does not invent return percentages, Sharpe, win rate, capital metrics or trade semantics. M2 later bound this output to the manifest-driven Experiment runner. M3 also added a real exploratory result under `reports/research/` for HYP-0001 / PROTO-01; that negative prototype remains exploratory evidence and is not upgraded to a formal Experiment.
