# ATS v1 — legacy archive

**Статус:** LEGACY / SUPERSEDED  
**Период исходной модели:** с 11 сентября 2026 года до Program Rebaseline ATS v2  
**Current program model:** ATS v2 / Strategy Factory  
**Physical migration:** COMPLETE

## Назначение

Этот каталог хранит документы исходной модели ATS v1 для истории решений, traceability и извлечения полезных требований.

ATS v1 рассматривал проект преимущественно как последовательный lifecycle одной торговой системы через G01–G13. ATS v2 заменил эту модель программой, в которой существуют Research Factory, Shared Trading Platform, отдельные Strategy Lifecycles, Portfolio & Capital и Operations & Governance.

Документы в `legacy/v1/` **не являются current instructions, current roadmap, current state или разрешением на торговлю**.

Текущие источники истины:

- `03_СОСТОЯНИЕ_ПРОЕКТА.yaml`;
- `AI_HANDOFF.md`;
- `governance/backlog/PROGRAM_BACKLOG_V2.md`;
- `governance/program/`;
- `governance/methodology/`.

## Что сохранено из v1

Сильные принципы v1 уже переработаны в v2: reproducibility, независимый protective/risk contour, protected independent evidence, stress testing, staged execution, change/version control, запрет martingale/rescue funding и сохранение отрицательных результатов.

v1 superseded как program model, потому что одна Strategy line блокировала весь ATS, G01 появлялся до безопасного research, не было раннего Economic Viability gate, program roadmap смешивался со Strategy Lifecycle, отсутствовали Research Factory/shared platform/portfolio contours.

## Классификация

`MIGRATION_INDEX.md` присваивает каждому из 15 archived artifacts одну классификацию:

- `HISTORY` — только история/traceability;
- `REFERENCE` — полезный rationale/reference, но не source of truth;
- `REVIEW_NEEDED` — потенциально полезное содержание требует нового v2 review/decision перед promotion.

## Physical migration

`ATS2-M0-011` завершил физическую миграцию:

- все 15 designated v1 artifacts находятся в target paths внутри `legacy/v1/`;
- старые source paths удалены;
- историческое содержание сохранено byte-for-byte;
- `CARRYOVER.md` фиксирует remap review-needed requirements и OQ-001…009 на соответствующие v2 stages.

Запрещено переписывать legacy-документ так, будто он всегда был v2, переносить старые статусы в current state, считать старые broker/platform/risk assumptions принятыми или использовать legacy как current policy.

## Старые G01–G13

G01–G13 являются исторической основой части Strategy Lifecycle, но не current program roadmap. Их полезные элементы переработаны в `governance/methodology/STRATEGY_LIFECYCLE_V2.md`; старые ворота не считаются искусственно пройденными.

## Навигация

- `MIGRATION_INDEX.md` — inventory, classification, target path и carryover action;
- `CARRYOVER.md` — актуальный remap требований и открытых вопросов в v2;
- `program-management/` — старые roadmap/gates/backlog/experiment registry;
- `product/` — vision и functional requirements v1;
- `architecture/` — robot-centric architecture, stack и ADR;
- `regulations/` — historical regulatory/source checklist;
- `registers/` — historical artifact registry;
- `collisions/` — archived OQ-001…009.
