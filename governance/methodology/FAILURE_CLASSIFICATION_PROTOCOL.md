# ATS Failure Classification Protocol

**Status:** RF-039 PROPOSED BASELINE  
**Purpose:** prevent engineering or data-access failures from being misreported as market evidence.

## 1. Primary classes

Every failed or blocked run that could be confused with a research result must be assigned exactly one primary class.

### `TECHNICAL_FAILURE`

The intended research computation did not produce a valid interpretable result because the software/runtime/workflow failed.

Examples:
- Python/environment mismatch;
- Windows path or permission problem;
- encoding/locale issue;
- dependency/bootstrap failure;
- syntax/runtime exception;
- CI/lint/test infrastructure failure;
- corrupted report rendering where the frozen computation was not validly obtained.

A technical failure is **not market evidence**.

A retry with identical research semantics is a technical retry, not a new research attempt. If the repair changes data, formulas, eligibility, parameters, runner behavior or another research-relevant rule, apply normal material-change accounting.

### `SOURCE_FAILURE`

The intended research computation could not be completed because required external data/source access or source integrity was unavailable under the frozen source rules.

Examples:
- vendor/API unavailable;
- required file cannot be obtained after the allowed bounded attempts;
- source coverage is insufficient;
- required timestamps/fields do not exist;
- downloaded source fails integrity/provenance requirements.

A source failure is **not evidence against the market claim**.

Do not silently change provider, period, event definition or dataset merely to obtain a favorable/available result. Any material source change follows Data Feasibility and research-attempt rules.

### `RESEARCH_OUTCOME`

The frozen computation executed validly on eligible data and returned a result that can be interpreted under the declared decision rule.

Only this class may produce a market/research PASS, FAIL, PARK-for-sample-size, or similar evidence conclusion.

## 2. Fail closed on ambiguity

If it is unclear whether a failure is technical/source-related or a valid research outcome, classify it as blocked and do not infer a market result until the distinction is resolved.

## 3. Structured report contract

Local BAT/PowerShell/Python gate reports should emit machine-readable or stable key/value fields whenever practical:

```text
STATUS=PASS|FAIL|BLOCKED
FAILURE_CLASS=TECHNICAL_FAILURE|SOURCE_FAILURE|RESEARCH_OUTCOME|NONE
BRANCH=<branch>
HEAD=<sha>
PYTHON=<version-or-na>
ENCODING=UTF-8|<actual>
VALIDATOR=PASS|FAIL|NA
RUFF=PASS|FAIL|NA
PYTEST=PASS|FAIL|NA
EXIT_CODE=<integer-or-na>
ERROR_STAGE=<stable-stage-name-or-na>
ERROR_CODE=<stable-code-or-na>
```

A JSON companion report is preferred when the script already produces structured artifacts.

Human-readable diagnostics may be added, but the stable fields must not depend on localized console wording.

## 4. Windows robustness

Repository gate scripts should, where feasible:

- use repository-relative paths;
- state the expected Python/runtime identity;
- write UTF-8 reports explicitly;
- preserve subprocess exit codes;
- identify the failed stage;
- distinguish a missing source from a broken program;
- avoid treating console-codepage differences as research outcomes.

## 5. Research accounting

- `TECHNICAL_FAILURE` with unchanged semantics: engineering audit trail; normally no new Material Research Attempt.
- `SOURCE_FAILURE`: record the source attempt/blocker; do not count as market failure.
- `RESEARCH_OUTCOME`: record under the applicable research attempt and preserve negative outcomes.
- A result-driven repair/change after observing a valid `RESEARCH_OUTCOME` is a new material attempt when it can affect the result.

## 6. Communication rule

When reporting a failure to OWNER, say in plain language first what failed:

- "сломалась техника/окружение";
- "не удалось получить/подтвердить данные";
- "тест корректно выполнился и гипотеза не прошла/прошла".

Then provide the formal class and technical detail.

## 7. Boundary

This protocol classifies execution outcomes. It does not weaken freeze/reveal rules and does not permit a source substitution or research-rule change without the normal governance path.