# HYP-0005 September 2026 Local Source Intake — Git Hygiene and Evidence

Technical task: `ATS2-RF-033`.
Parent research gate: `ATS2-RF-023` / HYP-0005 `1/5` — **still open**.
Source contract: `research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md`.
Offline intake contract: `research/reviews/HYP-0005-OFFLINE-SOURCE-INTAKE.md`.
Evidence type: **owner-reported file-only intake**, not market evidence.
Information boundary: `NO_CONFIRMATORY_OUTCOME_COMPUTED`.

## Provenance and completed local file intake

On 2026-10-09, OWNER supplied separate manually downloaded Jetta JSON files
and identified the source side by the exact original official URLs:

- BID: `9 (1).json` from
  `https://jetta.dukascopy.com/v1/candles/hour/EUR-USD/BID/2026/9`;
- ASK: `9.json` from
  `https://jetta.dukascopy.com/v1/candles/hour/EUR-USD/ASK/2026/9`.

Provider provenance classification:
`USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER`.
The owner-supplied report states that all three objects were
successfully written in byte-preserving fashion, with expected
size and SHA-256. Verification below is the **required future
exact-main local hash gate**, not a claim that the GitHub agent
has accessed OWNER's protected local files.

| Local file (relative to ATS root) | Bytes | SHA-256 |
|---|---:|---|
| `data/external/dukascopy/EURUSD/H1/2026/09/BID_candles_hour_1.json` | 12724 | `4da5797f7abba1e015f137474a0116dcd35056ddbf5633200e65a40e5a259943` |
| `data/external/dukascopy/EURUSD/H1/2026/09/ASK_candles_hour_1.json` | 12745 | `1672abce57189bf8519bdf7a806dcbd1e8152bc0d6f4ce06c9bb244289f10530` |
| `reports/local_ci/HYP0005_2026_09_SOURCE_INTAKE_PROVENANCE.json` | 1321 | `9f79cea766237a73992275d500217c1d91c3a8f5a4e2182cb1402e2a0d6fc410` |

Original inbound archive:
`HYP0005_DUKASCOPY_EURUSD_H1_2026_09_INTAKE (1).zip`
SHA-256: `05d369d7d487a6db98e8e977f9bd4cad423f75dd974c3747c2efb48bd3f633d7`.
The ZIP is **not** a versioned research artifact.

The first two local .NET staging attempts were stopped due to a
transient `Get-Item` discrepancy. The last reported controlled
attempt used a direct .NET FileStream hash and no-overwrite
`System.IO.File.Move`; all three final files were hash-verified.
Staging files were reported absent after move.
No HTTP, no price decoding, no outcome calculation, and no rollback.
Do **not** rerun the intake or overwrite the final files.

## Provenance-only Git hygiene defect

Immediately after the successful final byte-preserving move, OWNER's
`git status --porcelain` returned exactly:

```text
?? reports/local_ci/HYP0005_2026_09_SOURCE_INTAKE_PROVENANCE.json
```

This is a missing *narrow ignore rule*, not a source integrity defect.
Existing `.gitignore` excludes the entire
`data/external/dukascopy/` directory and other local-only
`reports/local_ci/` evidence, but had no rule for this specific
new provenance file.

The only new ignore path authorized:

`reports/local_ci/HYP0005_2026_09_SOURCE_INTAKE_PROVENANCE.json`

Do NOT use `git add -f`, commit the provenance JSON, delete the file,
make an all-encompassing ignore for `reports/local_ci/`, or change
the raw source bytes/hashes. The committed `.gitignore` rule should
make the worktree clean upon checkout of the exact RF-033 agent branch,
even when the provenance file stays physically present.

## Frozen source/research contract unchanged

EURUSD / Dukascopy H1 BID+ASK, exact previously frozen periods:
- `[2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)` (LEFT_UNSEEN);
- `[2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)` (RIGHT_UNSEEN).

Already consumed ATS history remains excluded.
There is **no** dataset freeze or confirmatory result.
File existence, size, and SHA-256 do NOT certify:
provider independent authenticity, decoder agreement,
per-record timestamp/side coherence, eligible observation
geometry, spread/return comparisons, or the hypothesis outcome.

RF-033 is only the source metadata/Git hygiene technical gate.
Its exact-main runtime will hash the three local source/provenance
files and verify the narrow ignore rule while preserving all bytes.
The RF-023 research gate remains OPEN until a separately approved
offline source/geometry preparation and later RF-024 freeze.
Do not run `tools/hyp0005_data_feasibility.py`, any downloader,
or any HYP-0005 primary inequality under RF-033.

HYP-0006: `DEVELOPMENT_REVEALED_EXPLORATORY_ONLY`.
HYP-0007: `NO_CONFIRMATORY_OUTCOME_COMPUTED`, paused.
