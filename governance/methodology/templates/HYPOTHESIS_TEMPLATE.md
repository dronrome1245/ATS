# Hypothesis Card

## Identity

- Hypothesis ID: `null`
- Parent Idea ID: `null`
- Supersedes Hypothesis ID: `null`
- Status: `DRAFT`
- Created on: `null`

## Statement

Сформулировать проверяемое утверждение о рынке так, чтобы его можно было опровергнуть наблюдаемыми данными.

## Mechanism

Объяснить предполагаемый экономический, поведенческий, структурный, event-driven или microstructure-механизм возникновения эффекта. Не использовать прибыльный backtest как механизм.

## Market

- Market / asset class: `null`
- Instrument or universe: `null`

## Conditions

Указать условия, при которых эффект должен проявляться, и условия, при которых гипотеза не делает предсказания.

## Horizon

- Decision horizon: `null`
- Holding/effect horizon: `null`

## Expected direction

Описать ожидаемое направление, ordering или форму эффекта без подгонки численного результата под известную историю.

## Decision-time information premise

Зафиксировать, какая информация предполагается доступной системе на момент исторического решения и какие timing assumptions критичны для утверждения.

## Falsification

Перечислить наблюдения или результаты, которые считаются evidence against the claim, делают гипотезу опровергнутой или требуют новой Hypothesis с новым ID.

## Required data

- Required datasets / information types: `null`
- Timestamp requirements: `null`
- Cost/execution inputs: `null`
- Exact source/vendor known: `null`

До Data Feasibility допустимо не знать конкретного vendor или точную доступную глубину истории, но тип данных и критичные timestamp semantics должны быть понятны.

## Known biases and leakage risks

Зафиксировать известные угрозы достоверности: look-ahead, survivorship, revisions, universe selection, multiple testing, temporal leakage, event timestamp ambiguity, dependent observations и другие применимые риски.

## Planned cheap test

Определить один ограниченный исследовательский вопрос, который позже может быть проверен после Data Feasibility. Не формулировать задачу как поиск самых прибыльных параметров.

## Falsifiability check

- Observable claim defined: `null`
- Context/conditions defined: `null`
- Expected direction/form defined: `null`
- Decision-time information premise defined: `null`
- Failure condition defined: `null`
- Non-tautological claim: `null`

## Status decision

- Decision: `DATA_FEASIBILITY`
- Reason: `null`

Допустимые решения: `DATA_FEASIBILITY`, `PARK`, `REJECT`.

Соответствие decision → status:

- `DATA_FEASIBILITY` → `READY_FOR_DATA_FEASIBILITY`
- `PARK` → `PARKED`
- `REJECT` → `REJECTED`

После downstream use material reformulation создаёт новую `HYP-xxxx`; старую Hypothesis сохраняют и при необходимости помечают `SUPERSEDED`.