# ATS Protected Evidence Policy

**Status:** RF-039 PROPOSED BASELINE  
**Purpose:** treat unseen/independent market history as a limited research resource and prevent accidental reuse as if it were still independent.

## 1. Plain-language rule

Protected evidence means data deliberately kept unseen so ATS can later ask a stronger question without having already tuned the idea to that same history.

Such data are not "free extra backtest data". Once ATS looks at the result, that information can influence future choices.

Therefore:

> Open a protected block only when its answer is decision-relevant and a cheaper development test cannot answer the same question honestly.

For a trading claim, this normally means ATS should first establish a plausible signal/trading mechanism, define the intended trade, and assess material execution/cost issues before spending a protected block on confirmatory profitability evidence.

This is not an absolute requirement that every structural study must first become a strategy. A structural/platform confirmatory reveal is allowed when PASS and FAIL would genuinely change a downstream decision and the value of that confirmation justifies consuming independent evidence.

## 2. Protected-block states

Each protected block has one state:

- `UNSEEN` — outcome/content not inspected for the research purpose;
- `RESERVED` — allocated prospectively to a defined future test, still unseen;
- `REVEALED` — decision-relevant result/content has been inspected;
- `CONSUMED` — reveal is part of research history and the block cannot be treated as unseen again for affected research lines.

A new Hypothesis ID, new chat, new runner or new strategy version does not move a block from `REVEALED/CONSUMED` back to `UNSEEN`.

## 3. Independence relation

Independence is evaluated relative to a research family/claim, not only by file name.

Record one of:

- `INDEPENDENT` — the block did not influence the design/selection of the claim being tested;
- `DEVELOPMENT_KNOWN` — the block is known and may be used for development/reference work but not as fresh confirmation of choices influenced by it;
- `FAMILY_CONTAMINATED` — revealed results from the block could reasonably have influenced later choices in this research family, so it is not independent evidence for those later choices.

"Contaminated" does not mean the data are bad. It means they are no longer an honest fresh test for a claim designed after seeing them.

## 4. Research-family evidence budget

For every research family that may consume protected evidence, record at minimum:

- family ID/name;
- protected blocks available or known;
- state of each block;
- independence relation;
- number of reveals already consumed;
- remaining genuinely independent blocks, if knowable;
- which claim/version consumed each reveal;
- what decision changed because of the reveal.

Suggested summary:

`Protected Evidence Consumption: X / N`

`Independent blocks remaining: N_remaining | UNKNOWN`

Do not invent a denominator when the future independent evidence universe is not well defined.

## 5. Protected Evidence Admission Gate

Before any protected/confirmatory reveal answer these questions:

1. What exact decision will change if the result is PASS?
2. What exact decision will change if the result is FAIL?
3. Can a cheaper development test answer the same question?
4. Is the claim already specified enough that the protected result will not be used for tuning?
5. Is the search family/denominator recorded?
6. For a trading claim, are entry/exit/timing and material execution/cost assumptions specified enough for the confirmatory question?
7. Could plausible omitted costs/execution effects reverse the economic conclusion?
8. Is this block genuinely independent of the claim/version being tested?
9. What independent evidence remains after this reveal?

If PASS and FAIL do not change a downstream decision, default route is `PARK / REFERENCE_ONLY`, not reveal.

If a cheaper honest test exists, use it first.

## 6. Trading-claim sequencing

The default economical sequence is:

`development data → cheap falsification → directional signal evidence → bounded path/horizon characterization if needed → strategy formulation → execution/economic feasibility → freeze → protected confirmatory trading evidence`.

This sequence exists to avoid spending scarce independent history on ideas that have not yet shown a coherent trading mechanism or cannot survive plausible costs.

It is a default, not a mechanical requirement for every research purpose. `PLATFORM_QUALIFICATION`, `MARKET_STRUCTURE` or another non-trading purpose may consume protected evidence earlier only when the confirmation itself is decision-relevant and justified.

## 7. Post-reveal rule

After a protected reveal:

- preserve PASS and FAIL;
- record the block as revealed/consumed;
- do not tune parameters on the block and then call another run on it confirmatory;
- if the result motivates a material claim/specification change, record a new Material Research Attempt and classify the revealed block as development-known/family-contaminated for that changed line;
- require genuinely fresh evidence for a later independent claim when independence matters.

## 8. Existing ATS application

HYP-0007 is an example of why the admission gate matters: it proposes consuming a genuinely unseen CPI event block to reconfirm a non-directional structural effect, but no concrete directional/executable trading decision currently depends on the answer. Therefore it should remain parked until a specific decision makes the confirmation worth the evidence cost.

This does not invalidate HYP-0007. It changes the priority of spending independent evidence.

## 9. Boundary

Protected evidence is a scarce information resource, not a score to maximize. Minimize consumption consistent with making the decisions ATS actually needs to make.