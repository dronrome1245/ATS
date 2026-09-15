# ATS Research Entity Templates

**Статус:** BASELINE  
**Work package:** `WBS-0.8` / `ATS2-M0-008` with M1 operational extensions

## Назначение

Этот каталог содержит canonical templates для создания основных исследовательских сущностей и повторяемых research-review artifacts ATS v2 без повторного проектирования структуры каждого объекта.

Шаблоны основаны на `STRATEGY_LIFECYCLE_V2.md`, `RESEARCH_METHODOLOGY_V1.md`, `REPOSITORY_STRUCTURE_V2.md` и operational M1 methodology.

## Правила использования

1. Шаблон копируется в canonical location соответствующей сущности/review.
2. Поля со значением `null` означают «фактическое значение ещё не зафиксировано» и должны быть заполнены до стадии, где поле обязательно.
3. Если поле действительно неприменимо, в экземпляре используется явное значение `NOT_APPLICABLE` и при необходимости объяснение причины.
4. Нельзя подставлять типовые финансовые, торговые, data-vendor или юридические значения только ради заполнения формы.
5. ID после выдачи не переиспользуется.
6. Формальный Experiment считается evidence только после фиксации manifest, результата и conclusion.
7. Material change Strategy Version создаёт новую версию, а не переписывает старую как будто изменения не было.
8. Structural process tests шаблонов не создают fictitious research entities, datasets или prototype results.
9. Exploratory Cheap Prototype не становится formal Experiment задним числом; если его результат нужен как registered evidence, соответствующий run повторяется после предварительной регистрации `EXP-...`.

## Templates

### Idea

`IDEA_TEMPLATE.md`

Canonical instance:

`research/ideas/IDEA-NNNN.md`

### Hypothesis

`HYPOTHESIS_TEMPLATE.md`

Canonical instance:

`research/hypotheses/HYP-NNNN.md`

### Data Feasibility Review

`DATA_FEASIBILITY_TEMPLATE.md`

Canonical instance for a real Hypothesis:

`research/reviews/HYP-NNNN-DATA_FEASIBILITY.md`

Review process:

`governance/methodology/DATA_FEASIBILITY_REVIEW.md`

### Cheap Prototype

`CHEAP_PROTOTYPE_TEMPLATE.md`

Canonical review instance:

`research/reviews/HYP-NNNN-PROTOTYPE-nn.md`

Operational protocol:

`governance/methodology/CHEAP_PROTOTYPE_PROTOCOL.md`

Prototype identity is parent Hypothesis plus local sequence `PROTO-nn`. Evidence class is `EXPLORATORY_PROTOTYPE`; it is not automatically a registered Experiment.

### Candidate

`CANDIDATE_TEMPLATE.md`

Canonical instance directory:

`research/candidates/CAND-NNNN/`

Основной файл экземпляра: `CANDIDATE.md`.

### Experiment

Каталог `experiment/` содержит:

- `manifest.yaml` — immutable experiment context;
- `result.json` — machine-readable результат;
- `conclusion.md` — human-readable interpretation и decision.

Canonical instance:

`experiments/EXP-YYYYMMDD-nnn/`

### Strategy Version

Каталог `strategy_version/` содержит:

- `VERSION.yaml` — identity/version manifest;
- `SPECIFICATION.md` — торговая спецификация;
- `PARAMETERS.yaml` — параметры конкретной версии;
- `EVIDENCE_INDEX.md` — ссылки на evidence этой версии.

Canonical instance:

`strategies/STRAT-.../versions/vMAJOR.MINOR/`

## Минимальные переходы

- `Idea` создаётся на R0.
- `Hypothesis` создаётся не позднее R1 и должна быть falsifiable до formal quantitative evidence.
- Data Feasibility Review выполняется после Hypothesis decision `DATA_FEASIBILITY` и до Cheap Prototype.
- Cheap Prototype R3 отвечает на один ранний quantitative question и не является formal validation evidence.
- `Candidate` создаётся только после `R4 Economic Pre-Screen = PROMOTE`.
- Formal `Experiment` регистрируется до использования соответствующего результата как registered evidence.
- `Strategy Version` создаётся после Candidate admission, когда правила стратегии становятся versioned research object.

## Что этот пакет не определяет

Templates задают структуру объекта/review, но не подменяют:

- конкретные pass/fail thresholds;
- выбор рынка или стратегии;
- универсальный data vendor;
- выбор broker/jurisdiction;
- live risk limits;
- статистические критерии конкретного класса стратегии.

Эти решения появляются только в соответствующих lifecycle work packages и evidence.