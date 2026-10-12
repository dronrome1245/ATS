# HYP-0005 — Controlled Offline RF-023 Data Feasibility Preparation Gate

Technical task: `ATS2-RF-034` — exact-main execution gate for **existing** `ATS2-RF-023`.
Hypothesis: `HYP-0005` under `IDEA-0004`.
Research plan: **1/5 — source/data feasibility preparation**, still OPEN until RF-023 exact-main machine PASS.
Status before running: `STAGED_PENDING_EXACT_HEAD_PREFLIGHT`.
Information boundary: `NO_CONFIRMATORY_OUTCOME_COMPUTED`.
OWNER authorization: `2026-10-09`, explicit approval to prepare offline RF-023 Data Feasibility, **not** to inspect any confirmatory primary result.

## Why this gate exists

- RF-033 exact-main PASS at `5ea7a923c59c44d6b733f8c7c6db352fd846d434` closed local provenance Git hygiene.
- All five predeclared source-month BID/ASK Jetta JSON pairs are locally present (as reported and hash-checked by OWNER). The September pair is **USER_ATTESTED_NOT_INDEPENDENTLY_VERIFIED_AGAINST_PROVIDER**. This does not certify market-source authenticity.
- The existing `research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md` and `tools/hyp0005_data_feasibility.py` already fix the source, segments, semantics, cleaning, geometry, permitted decision and outputs.
- RF-034 is the source/data **execution infrastructure** for the old RF-023 research gate; it is not another material research attempt or a second first reveal.

## Immutable frozen contract

Source: Dukascopy EURUSD H1 BID+ASK Jetta JSON, with the original predeclared BI5 alternative only if the frozen offline resolver selects it; do not switch sources post hoc.
For this exact local intake, the five complete Jetta JSON month pairs already exist and are hash-identified. Only those existing snapshots may be used.

Frozen exact periods (UTC, end exclusive):

- LEFT_UNSEEN: `[2003-05-04T21:00:00Z, 2003-08-03T21:00:00Z)`.
- RIGHT_UNSEEN: `[2026-09-01T00:00:00Z, 2026-09-26T00:00:00Z)`.
- ATS-wide consumed EURUSD: `[2003-08-03T21:00:00Z, 2026-09-01T00:00:00Z)`.

Frozen timing is `H1_OPEN_PROXY_AT_EVENT_TIME`, not an executable tick guarantee.
UTC bucket boundaries: CORE_ACTIVE 07–16, TRANSITION 17–20, OFF_HOURS 21–06.
Next-hour eligibility needs **exactly t+1h in the same segment** and cannot bridge closures or missing hours.
No new columns for spread, return, rolling volatility, medians, primary inequalities, directional P&L or cost optimization.

Frozen runner: `tools/hyp0005_data_feasibility.py`, git blob
`b8d72d858d5c2691de7dec9a709f6e4d7ccb2808`.
Frozen pre-result research protocol:
`research/reviews/HYP-0005-DATA-FEASIBILITY-PREP.md`, git blob
`c15b2b67700dd46fc592f1208731ce6b42f6905c`.
Neither artifact may be changed, optimized or refrozen to match the observed geometry.

## Exact raw file identity: offline SHA-256 preflight

Canonical root: `data/external/dukascopy/EURUSD/H1/`.
The expected file for each row is
`YYYY/MM/{SIDE}_candles_hour_1.json`. Verify each file's size and SHA-256 without decoding it before the single execution:

| Month | Side | Bytes | SHA-256 |
|---|---|---:|---|
| 2003-05 | BID | 12324 | `16f689edd5643b906de2cdc6b6069ed62489241892506f5624c4104ccfef1293` |
| 2003-05 | ASK | 12311 | `ac766b0ebe86ddb7fd818617dea5efefae71150a6b295f051608bac0487e02a5` |
| 2003-06 | BID | 13040 | `58d4dd1d34a74edfa66bfd22bf52cbc7000921a67559f5a91d2d97b3a2a5e7bc` |
| 2003-06 | ASK | 13016 | `a4252590d4bc432e2d7d151771f0c8de72b94b3fde671a1333f1f724a2eee72b` |
| 2003-07 | BID | 14023 | `69b14b1f6bcdf18fa43664529f75a740c2575079e2b769033f47277deef7c653` |
| 2003-07 | ASK | 14009 | `2f18e66d24d9b9325c45e10944eb11a54a9a7557e2a8c3504c97f90e37781dee` |
| 2003-08 | BID | 12763 | `71c0ba7c4871e2431198acf84233d93d88375e63b63434617c825e595b602d7f` |
| 2003-08 | ASK | 12740 | `96ab42f94d729de73a3fd2aa296e01645a01f5fd70a3679b3bf520166b380da7` |
| 2026-09 | BID | 12724 | `4da5797f7abba1e015f137474a0116dcd35056ddbf5633200e65a40e5a259943` |
| 2026-09 | ASK | 12745 | `1672abce57189bf8519bdf7a806dcbd1e8152bc0d6f4ce06c9bb244289f10530` |

Local provenance is preserved exactly at
`reports/local_ci/HYP0005_2026_09_SOURCE_INTAKE_PROVENANCE.json`,
1321 bytes, SHA-256
`9f79cea766237a73992275d500217c1d91c3a8f5a4e2182cb1402e2a0d6fc410`.
It remains ignored by Git and cannot be deleted, reformatted, committed or treated as independently corroborated provider history.

## Stage versus execute

On `agent/*`: OWNER runs only `.\\ATS_AGENT_PREFLIGHT.bat`.
This checks source code using synthetic tests, local CI and frozen governance; it **does not execute** the real RF-023 runner, decode protected prices or inspect source geometry.

After exact-head PASS and GPT squash merge, OWNER synchronizes the exact `main` and runs `.\\ATS_TASK_CHECK.bat` **once**.
The exact-main checker must:

1. Require exact `main==origin/main`, CLEAN tree and frozen code/protocol Git blobs.
2. Verify the ten local source-file SHA-256 and September provenance bytes before any decode. Never open a network URL.
3. Refuse to execute if any of the three outputs below already exists or a derived CSV staging `.part` exists. No overwrite or automatic cleanup.
4. Run the frozen `tools/hyp0005_data_feasibility.py` **one time only**, after the full Local CI gate.
5. Verify final report/data hashes and identity, source and bucket/segment geometry metadata, unchanged original source hashes and **no outcome values**.
6. Retain any positive or negative **data feasibility geometry** verdict without retrofitting frozen rules. If there is an exception, STOP with exact blocker evidence; no retry.
7. Leave all outputs local/ignored; no source bytes in Git.

Required runtime outputs:

- `reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP.json`
- `reports/local_ci/HYP0005_DATA_FEASIBILITY_PREP_REPORT.txt`
- `data/derived/HYP-0005-CONF-01-EURUSD-H1.csv`
- `reports/local_ci/CURRENT_TASK_REPORT.txt`

The only allowed preparation decisions:

- `READY_FOR_CONFIRMATORY_FEASIBILITY_FREEZE`
- `INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY`

They are **data feasibility**, not the HYP-0005 primary hypothesis outcome.
A source/decode/quote integrity exception is an infrastructure/data blocker,
not `INSUFFICIENT_UNSEEN_CONFIRMATORY_GEOMETRY` unless the frozen code explicitly reaches that decision based on geometry.

## Completion boundary

RF-034/023 preparation requires owner-reported exact-main
`ATS CURRENT TASK CHECK: PASS` and `ATS TASK LAUNCHER: PASS`.
A technical preflight PASS, squash merge, file-hash PASS or geometric
eligibility count is not completion by itself.

Even after a successful RF-023 preparation, **RF-024** must separately
review and freeze the actual confirmatory dataset or PARK the Hypothesis.
Do not compute any `relative_spread`, `abs_next_1h_return`,
median, primary inequality, trading P&L or independent/validation evidence.
Do not run the HYP-0004/HYP-0006/0007 runners or access other protected source blocks.
