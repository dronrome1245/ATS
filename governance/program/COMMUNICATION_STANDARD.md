# ATS Communication Standard

**Status:** RF-039 PROPOSED BASELINE  
**Purpose:** make ATS explanations understandable to OWNER without sacrificing technical precision.

## 1. Default language

Communicate with OWNER primarily in clear Russian.

English research/governance terms may be used when they are canonical or useful, but on first meaningful use explain them in ordinary Russian.

Example:

`protected evidence` — данные, которые специально ещё не смотрели, чтобы позже честно проверить уже сформулированную идею.

Do not assume that an English label is self-explanatory merely because it exists in repository methodology.

## 2. Meaning before label

For any important gate, method or decision:

1. first say in plain language what it means and why it matters;
2. then give the formal ATS term/ID;
3. then state the concrete next action.

Prefer:

> Мы пока не смотрим отложенный кусок истории, потому что после просмотра он уже не будет независимой проверкой. Формально: protected block remains `UNSEEN`.

Avoid:

> Protected evidence admission blocked by family contamination.

without explanation.

## 3. Jargon rule

Do not use unexplained jargon, abbreviations or mixed Russian/English phrases when a simple Russian sentence can express the same meaning.

When a technical term is necessary, add a short explanation such as:

- `простыми словами: ...`;
- `это означает: ...`;
- `зачем это нужно: ...`.

Do not oversimplify formulas, IDs, frozen rules or research distinctions when precision matters.

## 4. Decision-first answers

For OWNER-facing research decisions, prioritize this order:

1. what happened / what we know;
2. what it means;
3. what we do next;
4. only then technical detail, hashes, IDs and implementation notes.

For purely technical diagnostics, LIGHT MODE may start with the technical failure/result but must still state the practical consequence.

## 5. Explain irreversible actions

Before OWNER is asked to authorize or execute an irreversible action, explain in plain Russian:

- what will happen;
- what information will become known or consumed;
- what cannot honestly be undone afterward;
- why the action is needed now.

This is mandatory for protected-data reveal, protocol exception, capital/live decisions and other irreversible gates.

## 6. Ambiguous terminology

If a phrase can reasonably be misunderstood, do not merely repeat it. Replace it with a concrete description.

Example:

Instead of `only then protected evidence`, say:

> Отложенные ранее не просмотренные данные открываем только тогда, когда результат этой проверки реально изменит решение и более дешёвого честного способа получить ответ уже нет.

## 7. Repository precision

Plain language does not replace canonical labels. When recording governance state in repository artifacts, retain exact ATS IDs/statuses and accompany them with understandable explanation where OWNER must act on them.

## 8. Acceptance rule

An OWNER-facing answer fails this communication standard if a technically correct reader can follow it but a non-specialist OWNER cannot tell:

- what the term means;
- why it matters;
- what changes because of it;
- what action is expected next.