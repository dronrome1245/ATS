# ATS Signal-to-Strategy Protocol

**Status:** PROPOSED BASELINE FOR RF-039  
**Purpose:** separate market-structure/signal discovery from strategy formulation, execution feasibility and profitability claims.

## 1. Core separation

ATS must distinguish four different questions:

1. `STRUCTURE_OR_SIGNAL_DISCOVERY` — does an observable market relationship exist?
2. `ALPHA_PATH_CHARACTERIZATION` — how does the conditional effect evolve across time/path?
3. `STRATEGY_FORMULATION` — what exact entry, exit and risk/execution rule is proposed?
4. `CONFIRMATORY_TRADING_EVALUATION` — does the frozen trading rule survive costs, execution assumptions and stronger evidence?

A positive result at an earlier stage is not evidence that later stages pass.

## 2. Structural effects are not trading strategies

Examples of structural evidence:

- higher absolute movement in one session;
- wider/narrower spread by time of day;
- higher post-event volatility;
- a conditional distributional difference with no action sign.

These may become:

- `STRUCTURAL_REFERENCE`;
- `REGIME_FILTER`;
- `PLATFORM_QUALIFICATION_EVIDENCE`;
- input to a new trading hypothesis;
- `PARK` / `CLOSE`.

They do not automatically become `ALPHA_SIGNAL` or justify P&L calculation.

## 3. Translation Gate

After a positive structural/non-directional result, select exactly one route:

- `CLOSE_AS_STRUCTURAL_REFERENCE`
- `RETAIN_AS_REGIME_FILTER`
- `RETAIN_AS_PLATFORM_QUALIFICATION_EVIDENCE`
- `FORM_TRADING_HYPOTHESIS`
- `PARK`
- `REJECT`

Before choosing further confirmatory structural work, answer:

> What concrete downstream decision changes if another structural replication passes?

If no decision changes, further replication should normally be parked.

## 4. Signal discovery

A directional signal hypothesis asks whether information available at time `t` changes the distribution of a later signed outcome.

At this stage, fixed forward horizons are preferred to ad-hoc stop/take-profit optimization because they isolate signal information from exit-parameter search.

Do not interpret a development forward-return horizon as an automatically optimal production exit.

## 5. Alpha path characterization

After a directional signal survives a cheap development screen, ATS may characterize its path before freezing a strategy.

Permitted diagnostics may include:

- forward return / IC by a predeclared horizon grid;
- alpha-decay profile;
- MAE distribution;
- MFE distribution;
- time-to-MAE;
- time-to-MFE;
- spread evolution;
- volatility evolution;
- event-time concentration;
- regime concentration.

These diagnostics are development evidence, not confirmatory evidence.

## 6. Horizon search accounting

A horizon grid is a parameter/search family.

Example:

`H = {5m, 15m, 30m, 60m, 120m, 240m}`

If ATS inspects all six horizons, the research denominator is six alternatives even if only one is later selected.

The complete grid must be frozen before the development result is inspected and recorded under `MULTIPLE_RESEARCH_ACCOUNTING.md`.

A later frozen trading hypothesis may choose one horizon or a deterministic rule, but cannot describe the selected horizon as if it had been prespecified before the development search.

## 7. MAE/MFE discipline

MAE/MFE are primarily `PATH_DIAGNOSTIC` tools.

Do not automatically convert an observation such as:

`most historical winners had MAE < X`

into a stop rule and then treat the resulting strategy as independently supported.

That is outcome-conditioned tuning unless the selection freedom is explicitly recorded and followed by a new frozen evaluation.

Permitted workflow:

`signal evidence → path diagnostics → proposed exit/risk model → freeze → new evaluation`.

## 8. Triple Barrier discipline

Triple Barrier is an allowed strategy/labeling framework, not an overfitting exemption.

Material choices include:

- upper multiplier;
- lower multiplier;
- symmetric/asymmetric barriers;
- volatility estimator;
- volatility lookback;
- vertical/time barrier;
- price field;
- entry semantics;
- gap/touch semantics.

If several alternatives are inspected, all inspected alternatives belong to the research denominator.

## 9. Fixed-time exits

A fixed-time exit is a valid strategy rule when it is intentionally specified and frozen.

ATS must not require every strategy to use stop-loss or take-profit orders.

Large intra-horizon adverse excursion may affect:

- acceptable leverage;
- position sizing;
- capital efficiency;
- drawdown/risk limits;
- viability of the strategy.

It does not by itself make a fixed-time exit mathematically invalid.

## 10. Strategy formulation

Before a trading strategy can enter confirmatory profitability evaluation, freeze at minimum:

- information available at decision time;
- action/direction;
- entry trigger;
- entry timing;
- intended order type;
- exit rule;
- holding/time-stop rule;
- trade-level barrier rule, if any;
- position sizing premise or fixed research size;
- cost model class;
- execution model class;
- invalidation/falsification rule.

If these fields do not exist, the object is not yet a complete trading strategy.

## 11. Execution Feasibility

Before expensive confirmatory evaluation of a trading claim, determine whether the available data can honestly model the proposed execution.

Freeze as applicable:

- decision timestamp;
- order type;
- assumed decision/order latency;
- fill-price semantics;
- spread representation;
- slippage representation;
- commission;
- financing/rollover;
- trade size/capacity premise;
- required quote/depth granularity.

Level 2/order-book data are not universally required.

They become materially important when the claim depends on passive limit fills, queue position, depth, immediate fast-market execution, adverse selection or market impact that cannot be represented by top-of-book data.

## 12. Dynamic cost discipline

For trading claims, model costs at the level supported by data.

Conceptually:

`Cost = f(market state, volatility, time/event regime, order type, latency, trade size, liquidity)`

Do not claim false precision for components not observed.

If plausible omitted costs can reverse the sign of the effect, economic PASS is not allowed until the uncertainty is resolved or the line is parked.

## 13. Profitability metrics

Profitability metrics belong to a frozen trading object, not to a purely structural hypothesis.

Typical metrics may include:

- net P&L/return;
- Sharpe or another risk-adjusted measure;
- drawdown;
- turnover;
- hit rate where meaningful;
- tail loss;
- exposure/capital usage;
- execution degradation;
- capacity.

The metric set and decision rule must be registered before protected/confirmatory evaluation.

## 14. Multiple-research statistical control

Program-wide search freedom must be considered before strong performance claims.

Each research family should record where applicable:

- `family_id`;
- hypotheses/proposals in family;
- parameter/horizon/feature alternatives inspected;
- markets/instruments inspected;
- metrics used for selection;
- number of material variants;
- protected blocks consumed;
- method used to account for multiplicity/selection.

No universal method is mandatory for every research class.

Possible tools:

- family-wise error control for small strict confirmatory families when p-values are primary decision statistics;
- FDR for broader screening families when appropriate;
- selection-adjusted performance measures for strategy selection.

Do not apply p-value corrections mechanically when the test has no p-value-based decision rule.

## 15. Deflated Sharpe Ratio

DSR may be considered for Strategy Candidate/Validation stages when:

- a trading return series exists;
- Sharpe is decision-relevant;
- multiple strategies/specifications/trials were inspected;
- the effective number of trials and non-normality inputs can be defended.

Do not apply DSR to a structural median inequality with no strategy return series.

## 16. Research purpose and evidence labels

Each new object should identify its primary purpose:

- `PLATFORM_QUALIFICATION`
- `MARKET_STRUCTURE`
- `REGIME_FILTER`
- `ALPHA_DISCOVERY`
- `EXECUTION_RESEARCH`
- `CONFIRMATORY_REPLICATION`

And its economic role:

- `NO_DIRECT_TRADING_ROLE`
- `REGIME_FILTER`
- `ENTRY_SIGNAL`
- `EXIT_SIGNAL`
- `POSITION_SIZING`
- `EXECUTION_RULE`
- `RISK_FILTER`

These labels control interpretation; they do not change observed results.

## 17. Research velocity rule

ATS optimizes:

`research integrity × information value × research velocity`

When two workflows provide equivalent integrity, prefer the one that:

- consumes less protected evidence;
- uses fewer manual gates;
- costs less data/engineering effort;
- gives an earlier decision to stop or continue.

Do not add confirmatory layers merely because the previous layer was positive.

## 18. Completion routes

A research object should end with one explicit route:

- `STOP`
- `PARK`
- `STRUCTURAL_REFERENCE`
- `REGIME_FILTER`
- `NEW_TRADING_HYPOTHESIS`
- `CANDIDATE_PATH`

Continuation by inertia is not an allowed reason.
