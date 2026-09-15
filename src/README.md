# Source code

ATS is currently in `M2_RESEARCH_PLATFORM_MVP`.

M2 code is research-platform code: reproducible environment support, dataset manifests/loaders, Strategy/Research interface, deterministic replay, explicit costs, analytics, experiment runner and tests.

A concrete Reference Strategy #1 is not selected until M3. M2 may use trivial deterministic software fixtures to test platform semantics, but those fixtures are not Ideas, Candidates, Strategies or trading evidence.

M2 code must not create a broker/live execution path, real capital allocation, Strategy Risk Mandate or production trading permission.

The concrete language, package layout and platform module boundaries are chosen by `ATS2-M2-001 — Research stack ADR` against `governance/program/REFERENCE_CONSUMER_PROFILE.md`. Until that ADR is accepted, avoid prematurely locking in a framework or runtime.
