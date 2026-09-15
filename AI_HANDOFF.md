# ATS AI Handoff

**Назначение:** единая точка восстановления контекста для нового AI-чата, агента или разработчика.

Если вы впервые получили доступ к репозиторию, не начинайте с выбора стратегии, broker, instrument, risk limits или торгового кода. Сначала восстановите состояние по canonical artifacts.

## 1. Текущее состояние

- Program: `ATS — Algorithmic Trading Systems`.
- Current phase: `M0_PROGRAM_REBASELINE`.
- Status: `IN_PROGRESS`.
- Program model: ATS v2 / Strategy Factory.
- Canonical state: `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
- Canonical backlog: `governance/backlog/PROGRAM_BACKLOG_V2.md`.
- Current governance: `governance/program/` и `governance/methodology/`.
- Legacy archive: `legacy/v1/`.
- Реальная торговля, allocation и scaling сейчас не являются текущей задачей.
- G01–G13 — legacy ATS v1, не current roadmap.

## 2. Последний завершённый шаг

`ATS2-M0-011 — Legacy physical migration and unresolved-question carryover` завершена.

Последний завершённый artifact:

`legacy/v1/CARRYOVER.md`

Что сделано:

- 15 designated ATS v1 artifacts перенесены byte-for-byte в `legacy/v1/`;
- old v1 source paths удалены;
- `MIGRATION_INDEX.md` хранит classification/target mapping;
- `CARRYOVER.md` remap-ит review-needed requirements и OQ-001…009 на v2 stages;
- новые speculative tasks не создавались, потому что нужная будущая работа уже представлена WBS/backlog.

## 3. Следующая ready task

`ATS2-M0-012 — Final link/validator sweep`

Canonical next artifact anchor:

`tools/validate_repo.py`

Нужно просканировать current v2 namespace на stale old paths и ссылки, убедиться, что legacy не используется как source of truth, harden validator и получить зелёный CI.

После 0.12:

`ATS2-M0-013 — M0 Exit Review`, artifact `governance/program/M0_EXIT_REVIEW.md`.

## 4. Обязательный порядок чтения

1. `AGENTS.md`.
2. `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`.
3. `02_СЛЕДУЮЩИЙ_ШАГ.md`.
4. `governance/backlog/PROGRAM_BACKLOG_V2.md`.
5. Для current program work — `governance/program/`.
6. Для research — `governance/methodology/`.
7. Для historical rationale/carryover — `legacy/v1/README.md`, `MIGRATION_INDEX.md`, `CARRYOVER.md`.

## 5. Completion protocol

Program-level task не считается завершённой, пока синхронизированы deliverable, backlog, canonical state, human status, next-step, AI handoff, entrypoints и validator/tests при structural changes.

## 6. Запреты

Без явного решения OWNER нельзя:

- выделять реальный капитал;
- утверждать Strategy Risk Mandate;
- разрешать live admission;
- менять allocation/scaling;
- выдумывать broker/jurisdiction/instrument/return/risk limits;
- ослаблять independent evidence rules;
- вводить martingale, unlimited averaging или rescue funding;
- объявлять legacy requirement автоматически current v2 policy.

## 7. Проверка восстановления контекста

Новый агент должен ответить:

- Current phase? — `M0_PROGRAM_REBASELINE`.
- Last completed? — `ATS2-M0-011`, `legacy/v1/CARRYOVER.md`.
- Next task? — `ATS2-M0-012`.
- Next artifact anchor? — `tools/validate_repo.py`.
- Legacy location? — `legacy/v1/`.
- Old v1 source paths должны существовать? — нет.
- Можно ли сейчас выбирать live capital/broker/strategy? — нет.
