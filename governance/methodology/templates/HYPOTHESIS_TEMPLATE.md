# Hypothesis Card

## Identity

- Hypothesis ID: `null`
- Parent Idea ID: `null`
- Portfolio proposal ID: `null`
- Portfolio approval reference: `null`
- Research family ID: `null`
- Supersedes Hypothesis ID: `null`
- Status: `DRAFT`
- Created on: `null`

## Research classification

- Research purpose: `null`
- Economic role: `null`
- Directional claim: `null`

Allowed primary research-purpose values:

- `PLATFORM_QUALIFICATION`
- `MARKET_STRUCTURE`
- `REGIME_FILTER`
- `ALPHA_DISCOVERY`
- `EXECUTION_RESEARCH`
- `CONFIRMATORY_REPLICATION`

Allowed primary economic-role values:

- `NO_DIRECT_TRADING_ROLE`
- `REGIME_FILTER`
- `ENTRY_SIGNAL`
- `EXIT_SIGNAL`
- `POSITION_SIZING`
- `EXECUTION_RULE`
- `RISK_FILTER`

A new research Hypothesis should reference an OWNER-approved portfolio proposal under `RESEARCH_PORTFOLIO_PROTOCOL.md`. Existing historical hypotheses are exempt from retroactive relabeling.

## Statement

Сформулировать проверяемое утверждение о рынке так, чтобы его можно было опровергнуть наблюдаемыми данными.

Для directional/trading claim явно указать знак или decision rule. Нельзя выводить direction только из volatility/activity effect.

## Mechanism

Объяснить предполагаемый экономический, поведенческий, структурный, event-driven или microstructure-механизм возникновения эффекта. Не использовать прибыльный backtest как механизм.

## Market

- Market / asset class: `null`
- Instrument or universe: `null`

## Conditions

Указать условия, при которых эффект должен проявляться, и условия, при которых гипотеза не делает предсказания.

## Horizon

- Decision horizon: `null`
- Research/effect horizon: `null`
- Final strategy exit already defined: `NO`

Research horizon не считается автоматически production exit rule.

## Expected direction

Описать ожидаемое направление, ordering или форму эффекта без подгонки численного результата под известную историю.

## Decision-time information premise

Зафиксировать, какая информация предполагается доступной системе на момент исторического решения и какие timing assumptions критичны для утверждения.

## Value-of-information gate

- What changes if positive: `null`
- What changes if negative: `null`
- Cheaper equivalent test exists: `null`
- Known structural fact / novelty concern: `null`
- Protected evidence required before trading mechanism exists: `null`
- Decision: `PROCEED / PARK / REJECT / REFERENCE_ONLY`

Если положительный и отрицательный результат не меняют последующее решение, не запускать дорогой confirmatory test по инерции.

## Falsification

Перечислить наблюдения или результаты, которые считаются evidence against the claim, делают гипотезу опровергнутой или требуют новой Hypothesis с новым ID.

## Required data

- Required datasets / information types: `null`
- Timestamp requirements: `null`
- Cost/execution inputs: `null`
- Required market-data level: `null`
- Exact source/vendor known: `null`

До Data Feasibility допустимо не знать конкретного vendor или точную доступную глубину истории, но тип данных и критичные timestamp semantics должны быть понятны.

## Execution premise

Для trading claim указать предварительно:

- intended order type: `null`
- decision timestamp semantics: `null`
- latency relevance: `null`
- fill-price semantics: `null`
- spread/slippage relevance: `null`
- financing relevance: `null`
- capacity/depth relevance: `null`

Для purely structural claim отметить `NOT_APPLICABLE_TO_PRIMARY_CLAIM` и не считать это trading P&L specification.

## Known biases and leakage risks

Зафиксировать известные угрозы достоверности: look-ahead, survivorship, revisions, universe selection, multiple testing, temporal leakage, event timestamp ambiguity, dependent observations, outcome-conditioned MAE/MFE use, horizon search, barrier search и другие применимые риски.

## Planned cheap test

Определить один ограниченный исследовательский вопрос, который позже может быть проверен после Data Feasibility. Не формулировать задачу как поиск самых прибыльных параметров.

Если предполагается bounded grid горизонтов/параметров, перечислить весь grid заранее и связать его с Research Family / Multiple Research Accounting.

## Search-family declaration

- Bounded search planned: `YES / NO`
- Alternatives planned: `null`
- Selection metric: `null`
- Full denominator retained: `null`

Alpha-decay, MAE/MFE и Triple Barrier exploration считаются development research freedom, если используются для выбора trading rule.

## Falsifiability check

- Observable claim defined: `null`
- Context/conditions defined: `null`
- Expected direction/form defined: `null`
- Decision-time information premise defined: `null`
- Failure condition defined: `null`
- Non-tautological claim: `null`
- Portfolio approval present for new research: `null`
- Value-of-information gate passed: `null`

## Status decision

- Decision: `DATA_FEASIBILITY`
- Reason: `null`

Допустимые решения: `DATA_FEASIBILITY`, `PARK`, `REJECT`.

Соответствие decision → status:

- `DATA_FEASIBILITY` → `READY_FOR_DATA_FEASIBILITY`
- `PARK` → `PARKED`
- `REJECT` → `REJECTED`

После downstream use material reformulation создаёт новую `HYP-xxxx`; старую Hypothesis сохраняют и при необходимости помечают `SUPERSEDED`.

## Translation / completion route

После результата явно зафиксировать один маршрут:

- `STOP`
- `PARK`
- `STRUCTURAL_REFERENCE`
- `REGIME_FILTER`
- `NEW_TRADING_HYPOTHESIS`
- `CANDIDATE_PATH`

Positive structural result не получает `CANDIDATE_PATH` без отдельной falsifiable trading formulation.
