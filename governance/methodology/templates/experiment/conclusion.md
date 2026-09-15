# Experiment Conclusion

## Identity

- Experiment ID: `null`
- Hypothesis ID: `null`
- Candidate ID: `null`
- Strategy / Version: `null`
- Research stage: `null`
- Evidence class: `REGISTERED_EXPERIMENT`

## Registered question

Повторить predefined question из зарегистрированного `manifest.yaml` без изменения формулировки после просмотра результата.

## Registered primary metrics and decision rule

Перечислить primary metrics и decision rule в том виде, в котором они были зафиксированы до result observation.

## Result summary

Кратко описать фактический результат со ссылкой на `result.json`. Не заменять зарегистрированные primary metrics более привлекательными secondary metrics.

## Decision-rule evaluation

Показать, выполнен ли заранее определённый rule. Если rule невозможно честно оценить из-за data/runtime defect, зафиксировать это как limitation/failed execution context, а не придумывать новый success rule.

## Evidence quality

Оценить применимое:

- data quality и соответствие зарегистрированному information set;
- sample/evidence sufficiency;
- cost realism;
- leakage/bias concerns;
- concentration/outliers;
- reproducibility status;
- deviations/anomalies during execution.

## Interpretation

Зафиксировать отдельно:

- что experiment действительно поддерживает;
- что experiment не доказывает;
- какие ограничения сужают допустимый claim;
- является ли результат только registered research либо относится к более сильной lifecycle stage по отдельному protocol.

## Decision

- Machine outcome from result.json: `null`
- Human decision: `null`
- Reason: `null`

Допустимое решение определяется зарегистрированным research stage и protocol, например `PROMOTE`, `PARK`, `REJECT`, `PASS`, `FAIL` или `RETURN_TO_RESEARCH`.

Human decision не может задним числом менять preregistered decision rule.

## Deviations and defects

- Deviations from registered context: `null`
- Material result-affecting defect discovered: `null`
- Effect on evidence validity: `null`

Если material defect требует другого code/data/config/cost context, зарегистрировать новый Experiment ID вместо переписывания исходной preregistration.

## Follow-up

Если требуется следующий experiment, сформулировать новый ограниченный вопрос и зарегистрировать новый `EXP-YYYYMMDD-nnn` до просмотра его результата.

Не переписывать completed experiment post hoc и не превращать exploratory finding в original preregistered criterion.
