# Strategy Version Specification

## Identity

- Strategy ID: `null`
- Strategy Version: `null`
- Hypothesis ID: `null`
- Candidate ID: `null`

## Economic rationale

Опишите предполагаемый источник edge и почему он должен существовать.

## Market and universe

- Market / asset class: `null`
- Instrument or universe: `null`
- Timeframe / event horizon: `null`

## Inputs and features

Перечислить все данные и признаки, которые разрешено использовать. Для каждого временно чувствительного поля указать timestamp semantics и доступность на момент решения.

## Entry logic

Однозначно описать условия формирования торгового намерения.

## Exit logic

Однозначно описать обычные условия выхода.

## Protective exits

Описать stop/timeout/emergency rules, относящиеся к логике стратегии. Program/Portfolio Risk остаётся отдельным контуром.

## Position management

Определить допустимое управление открытой позицией: partial exit, trailing, holding time, re-entry и другие применимые правила.

## Filters and no-trade conditions

Зафиксировать session, spread, volatility, event и другие фильтры, если они входят в гипотезу.

## Position intent

Описать, какие данные Strategy Engine передаёт Risk Engine для расчёта допустимого объёма. Strategy Version не должна обходить Strategy Risk или Portfolio Risk.

## Deterministic examples

Привести набор контрольных сценариев, по которым другой developer может однозначно определить ожидаемое trading intent.

## Falsification and failure conditions

Указать, какие observed results или logical contradictions опровергают данную версию hypothesis/strategy.

## Known limitations

Зафиксировать известные ограничения, режимы, где стратегия не проверена, и assumptions, которые должны быть проверены последующими experiments.
