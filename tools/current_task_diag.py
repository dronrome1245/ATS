#!/usr/bin/env python3
"""Diagnose RF-023 Dukascopy access without computing HYP-0005 outcomes."""

from __future__ import annotations

import urllib.error
import urllib.request

CURRENT_JETTA = "https://jetta.dukascopy.com/v1/candles/hour/EUR-USD/{side}/2026/9"
CONTROL_JETTA = "https://jetta.dukascopy.com/v1/candles/hour/EUR-USD/{side}/2026/8"
CURRENT_BI5 = "https://datafeed.dukascopy.com/datafeed/EURUSD/2026/08/{side}_candles_hour_1.bi5"
CONTROL_BI5 = "https://datafeed.dukascopy.com/datafeed/EURUSD/2026/07/{side}_candles_hour_1.bi5"
ALT_CURRENT_BI5 = "https://www.dukascopy.com/datafeed/EURUSD/2026/08/{side}_candles_hour_1.bi5"
ALT_CONTROL_BI5 = "https://www.dukascopy.com/datafeed/EURUSD/2026/07/{side}_candles_hour_1.bi5"
USER_AGENT = "ATS-Research/1.0"


def probe(label: str, url: str) -> None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            sample = response.read(64)
            print(
                f"{label}: HTTP {response.status}; "
                f"sample_bytes={len(sample)}; "
                f"content_type={response.headers.get('Content-Type', '')!r}; "
                f"last_modified={response.headers.get('Last-Modified', '')!r}; "
                f"etag={response.headers.get('ETag', '')!r}",
                flush=True,
            )
    except urllib.error.HTTPError as exc:
        body = exc.read(256)
        print(
            f"{label}: HTTP {exc.code}; reason={exc.reason!r}; body_sample={body!r}",
            flush=True,
        )
    except urllib.error.URLError as exc:
        print(f"{label}: URL_ERROR {exc.reason!r}", flush=True)
    except OSError as exc:
        print(f"{label}: OS_ERROR {exc!r}", flush=True)


def main() -> int:
    print("ATS CURRENT TASK DIAGNOSTIC")
    print("Task: ATS2-RF-023 — HYP-0005 confirmatory Data Feasibility preparation")
    print("Purpose: distinguish current-month source availability from general provider failure")
    print("Information boundary: NO_CONFIRMATORY_OUTCOME_COMPUTED")
    print("Hypothesis outcome fields requested: 0")
    print()

    for side in ("BID", "ASK"):
        probe(f"JETTA_CURRENT_2026_09_{side}", CURRENT_JETTA.format(side=side))
        probe(f"JETTA_CONTROL_2026_08_{side}", CONTROL_JETTA.format(side=side))
        probe(f"BI5_CURRENT_2026_09_{side}", CURRENT_BI5.format(side=side))
        probe(f"BI5_CONTROL_2026_08_{side}", CONTROL_BI5.format(side=side))
        probe(f"BI5_ALT_CURRENT_2026_09_{side}", ALT_CURRENT_BI5.format(side=side))
        probe(f"BI5_ALT_CONTROL_2026_08_{side}", ALT_CONTROL_BI5.format(side=side))

    print()
    print("ATS TASK DIAGNOSTIC: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
