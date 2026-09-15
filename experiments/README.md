# Experiments

## Назначение

`experiments/` содержит formal registered experiments ATS v2.

Exploratory Cheap Prototype artifacts живут в Research Factory и не получают `EXP-...` задним числом.

Canonical registration methodology:

`governance/methodology/EXPERIMENT_REGISTRATION.md`

Canonical templates:

`governance/methodology/templates/experiment/`

## Canonical package

Каждый formal Experiment хранится в:

`experiments/EXP-YYYYMMDD-nnn/`

Минимальный состав:

- `manifest.yaml` — preregistered context до result observation;
- `result.json` — observed machine-readable result;
- `conclusion.md` — evaluation against the registered question/decision rule;
- optional `artifacts/` — supporting outputs согласно Git/data policy.

## Registration boundary

Formal experiment может считаться preregistered только если `manifest.yaml` со статусом `REGISTERED` зафиксирован в Git до наблюдения соответствующего результата.

Manifest связывает применимое:

- Experiment ID;
- Hypothesis ID;
- Candidate / Strategy / Strategy Version при наличии;
- code revision и implementation reference;
- dataset/source snapshot и period;
- parameters/configuration;
- random seed или `NOT_APPLICABLE`;
- cost/execution assumptions;
- predefined question;
- primary/secondary metrics;
- predefined decision rule;
- research stage и evidence class `REGISTERED_EXPERIMENT`.

Не существует обязательного универсального initial deposit, leverage, capital allocation или risk limit для research Experiment. Такие inputs фиксируются только когда они реально относятся к зарегистрированному вопросу и соответствующей lifecycle stage.

## Именование

Формат:

`EXP-YYYYMMDD-nnn`

Например: `EXP-20260915-001`.

ID после выдачи не переиспользуется.

## Неизменяемость

После `REGISTERED` decision-relevant context не переписывается под увиденный result.

Material change question/data/code/config/cost/metrics/decision rule требует нового Experiment ID.

Administrative non-semantic corrections допускаются только как явно записанные amendments.

Отрицательные, failed, cancelled и superseded experiments сохраняются.

## Registry

`ATS2-M1-008` создаёт searchable registry в:

`experiments/REGISTRY.csv`

Registry должен находить positive/negative/cancelled/superseded formal experiments по stable ID и связывать запись с canonical experiment package/registered manifest context.

До завершения M1-008 отсутствие `REGISTRY.csv` является ожидаемым program state, а не разрешением вести отдельный неканонический реестр.
