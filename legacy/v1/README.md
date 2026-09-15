# ATS v1 — legacy archive

**Статус:** LEGACY / SUPERSEDED  
**Период исходной модели:** с 11 сентября 2026 года до Program Rebaseline ATS v2  
**Current program model:** ATS v2 / Strategy Factory

## Назначение

Этот каталог хранит документы исходной модели ATS v1 для истории решений, traceability и извлечения полезных требований.

ATS v1 рассматривал проект преимущественно как последовательный lifecycle одной торговой системы через G01–G13. ATS v2 заменил эту модель программой, в которой существуют Research Factory, Shared Trading Platform, отдельные Strategy Lifecycles, Portfolio & Capital и Operations & Governance.

Документы в `legacy/v1/` **не являются current instructions, current roadmap, current state или разрешением на торговлю**.

Текущие источники истины находятся в:

- `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
- `AI_HANDOFF.md`;
- `governance/backlog/PROGRAM_BACKLOG_V2.md`;
- `governance/program/`;
- `governance/methodology/`.

## Почему v1 superseded

Сильные стороны v1 сохраняются: reproducibility, независимый protective/risk contour, protected independent evidence, stress testing, staged real execution, change/version control, запрет martingale/rescue funding и сохранение отрицательных результатов.

Но v1 имел ограничения для новой цели программы:

- одна Strategy line фактически блокировала весь ATS;
- G01 Risk Mandate возникал до безопасного research;
- не было отдельного раннего Economic Viability gate;
- program roadmap и strategy lifecycle были одним объектом;
- не было Research Factory для множества идей;
- shared platform и portfolio layer не были самостоятельными программными контурами.

Эти ограничения устранены в ATS v2.

## Классификация legacy-документов

Каждый v1 artifact получает одну основную классификацию в `MIGRATION_INDEX.md`.

### `HISTORY`

Артефакт сохраняется для истории и traceability. Его процесс/статус superseded, и перенос содержания в current v2 не требуется.

### `REFERENCE`

Артефакт не является current source of truth, но содержит полезное обоснование или принципы, уже перенесённые либо пригодные как справочный материал.

При конфликте всегда действует v2 source of truth.

### `REVIEW_NEEDED`

Артефакт содержит потенциально полезные требования, решения, источники или открытые вопросы, которые нельзя автоматически объявить current v2.

Для такого содержания необходимо одно из действий:

- создать отдельную v2 backlog task;
- оформить новый ADR/policy/specification;
- подтвердить актуальность внешнего источника;
- явно решить, что перенос не требуется.

Сам legacy-файл при этом всё равно архивируется и не становится current документом.

## Правило физической миграции

`ATS2-M0-011` переносит перечисленные в `MIGRATION_INDEX.md` документы из старых top-level каталогов в `legacy/v1/` без изменения их исторического содержания.

Одновременно создаётся `legacy/v1/CARRYOVER.md`, где перечисляются только действительно незакрытые v2-вопросы и новые backlog items, возникшие после review.

Запрещено:

- переписывать legacy-документ так, будто он всегда был v2;
- автоматически переносить старый статус `ACTIVE/PASS/BLOCKED` в current state;
- считать старый broker/platform/risk assumption принятым решением v2;
- терять отрицательную историю или причины supersede.

## Старые G01–G13

G01–G13 являются исторической основой Strategy Lifecycle, но не current program roadmap.

Их полезные элементы переработаны в `governance/methodology/STRATEGY_LIFECYCLE_V2.md`; старые ворота не считаются искусственно пройденными.

## Навигация

- `MIGRATION_INDEX.md` — полный список v1 artifacts, classification, target path и carryover action.
- `CARRYOVER.md` — создаётся на следующем шаге при физической миграции и содержит только актуальные вопросы, требующие дальнейшей работы v2.
