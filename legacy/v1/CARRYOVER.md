# ATS v1 Carryover into ATS v2

**Task:** `ATS2-M0-011`  
**Status:** BASELINE  
**Source classification:** `legacy/v1/MIGRATION_INDEX.md`

## 1. Purpose

This document records which unresolved ATS v1 concerns remain relevant after archival and where they belong in ATS v2.

A carryover item is not an answer. It is a routing decision: which v2 stage, work package or decision must resolve the concern later.

No financial, trading, legal or technology value is invented here.

## 2. Principles retained without new tasks

The following v1 principles are already represented by current ATS v2 governance/methodology and therefore require no duplicate backlog task:

- independent Strategy Risk / Portfolio Risk separation;
- stable intent identity and idempotency;
- state recovery and reconciliation;
- safe mode when state or position is unknown;
- logging of rejects, partial fills, slippage and latency;
- end-to-end auditability;
- stress/fault testing before live;
- Strategy Version ↔ evidence binding;
- one-shot independent examination / no post-hoc reuse as fresh evidence;
- no martingale, uncontrolled averaging or rescue funding.

Current sources of truth are `governance/program/OPERATING_MODEL_V2.md`, `governance/methodology/STRATEGY_LIFECYCLE_V2.md`, `governance/methodology/RESEARCH_METHODOLOGY_V1.md` and the Program WBS.

## 3. Platform and architecture carryover

### CARRY-PLAT-001 — Review v1 functional requirements against Research Platform MVP

**Source:** `legacy/v1/product/ФУНКЦИОНАЛЬНЫЕ_ТРЕБОВАНИЯ.md`  
**Disposition:** covered by existing M2/M5 WBS; no new backlog task required during M0.

When M2 capabilities are designed, review only the research-relevant requirements: reproducibility, Strategy Version linkage, deterministic decisions, data/cost assumptions, experiment traceability and testability.

Execution/risk/runtime requirements stay deferred to M5 and must not expand the M2 MVP prematurely.

### CARRY-ARCH-001 — Review robot-centric architecture before platform/execution architecture

**Source:** `legacy/v1/architecture/АРХИТЕКТУРА_РОБОТА.md`  
**Disposition:** covered by WBS-2 and WBS-5.

Useful concepts to reconsider rather than copy literally:

- market data adapter;
- strategy intent layer;
- protective/risk controller;
- execution adapter;
- persistent state and reconciliation;
- audit/observability;
- watchdog/emergency stop;
- replay/test contour.

The v1 single-robot component diagram is not current architecture.

### CARRY-TECH-001 — Re-evaluate runtime technology stack

**Source:** `legacy/v1/architecture/БАЗОВЫЙ_СТЕК.md`  
**Disposition:** existing `ATS2-M2-001 Research stack ADR` covers the research stack. Live runtime/platform remains a later M5 decision.

Git/GitHub/Markdown/YAML/Python repository tooling is factual current infrastructure. MT5/MQL5 remains a historical candidate only.

## 4. Legal and external-source carryover

### CARRY-LEGAL-001 — Fresh jurisdiction/broker/instrument review before live environment selection

**Sources:** `legacy/v1/regulations/ИСТОЧНИКИ.md`, `legacy/v1/regulations/РЕГЛАМЕНТЫ.md`.

**Disposition:** covered by M5/S08 live-environment work; no M0/M1 blocking task.

At activation time, use fresh authoritative sources for:

- owner/account jurisdiction and relevant tax/legal context;
- broker legal entity and regulator status;
- legal nature of the instrument;
- client protections and leverage/margin conditions;
- algorithmic-trading permission and platform constraints;
- actual fees, swaps and contractual execution terms.

The archived FCA/MetaTrader references are illustrative history, not automatically applicable current law or platform evidence.

## 5. Open-question remap

### OQ-001 — experiment capital currency/amount

**v2 stage:** Program Capital Policy / S08+ before real exposure.  
**Current effect:** does not block M0–M4 safe research.

### OQ-002 — maximum loss/drawdown/drawdown duration

**v2 stage:** Program/Strategy Risk Mandate before real exposure.  
**Current effect:** does not block safe research.

### OQ-003 — maximum share of total capital

**v2 stage:** Program Capital Policy / later portfolio governance.  
**Current effect:** deferred.

### OQ-004 — jurisdiction and tax residence

**v2 stage:** Live Environment/legal review in M5/S08.  
**Current effect:** deferred until a validated candidate approaches live preparation.

### OQ-005 — legal nature of traded instrument

**v2 stage:** strategy-specific live-environment selection.  
**Current effect:** research hypothesis may name a market/instrument for testing, but legal-live classification is resolved later.

### OQ-006 — broker/legal entity/account type

**v2 stage:** M5/S08.  
**Current effect:** not a program-wide prerequisite.

### OQ-007 — execution platform

**v2 split:**

- research stack → `ATS2-M2-001` and related M2 tasks;
- live execution platform → M5 after independent strategy evidence.

### OQ-008 — instrument, horizon and trading hypothesis

**v2 stage:** Research Funnel / Reference Strategy #1 selection.  
**Current effect:** not a program-level blocker; resolved per research line.

### OQ-009 — tick/data sources and historical coverage

**v2 stage:** per-hypothesis Data Feasibility, Dataset Manifest and Research Protocol.  
**Current effect:** no universal source is selected before a concrete consumer exists.

## 6. Backlog impact

Review of all carryover items found that their required future work is already represented in the current Program WBS/backlog at the appropriate abstraction level:

- M1 research/data feasibility;
- M2 research stack and platform MVP;
- M3 Reference Strategy selection and hypothesis/data work;
- M5 live environment, execution, risk and legal/broker decisions;
- M7 portfolio capital/risk governance.

Therefore `ATS2-M0-011` does **not** create speculative duplicate future tasks. When M3–M8 epics are decomposed closer to execution, this carryover document must be consulted so these requirements are not lost.

## 7. Physical migration rule

The 15 files listed in `MIGRATION_INDEX.md` are archived byte-for-byte into their target `legacy/v1/` locations. After target copies are verified and validator is switched to the new paths, the original v1 source paths are deleted.

Archived files remain evidence/history only. Current v2 decisions continue to come from canonical state, governance, methodology and backlog.
