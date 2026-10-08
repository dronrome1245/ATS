"""Synthetic-only RF-029 tests; importing the runner must not reveal market outcomes."""

from __future__ import annotations

import lzma
from datetime import UTC, datetime, timedelta

import pytest

from tools import hyp0006_proto01 as proto


def at(milliseconds: int) -> datetime:
    return datetime(2020, 1, 14, 13, 30, tzinfo=UTC) + timedelta(
        milliseconds=milliseconds
    )


def test_rf028_denominator_and_hash_are_precommitted() -> None:
    assert proto.FROZEN_CANDIDATE_COUNT == 217
    assert proto.FROZEN_ELIGIBLE_COUNT == 216
    assert proto.FROZEN_INELIGIBLE_ID == "BLS-CPI-20030815"
    assert proto.FROZEN_TOLERANCE_MS == 30_000
    assert len(proto.FROZEN_RF028_JSON_SHA256) == 64


def test_nearest_boundary_equal_gap_chooses_previous() -> None:
    quotes = [(at(-25), 100_000, 100_010), (at(25), 100_020, 100_030)]
    chosen, side, gap = proto.select_nearest(quotes, at(0))
    assert chosen == quotes[0]
    assert (side, gap) == ("PREVIOUS", 25)


def test_duplicate_selected_timestamp_chooses_last_raw_bid_ask_pair() -> None:
    quotes = [
        (at(-10), 100_000, 100_010),
        (at(-10), 100_100, 100_140),
        (at(20), 100_200, 100_210),
    ]
    chosen, side, gap = proto.select_nearest(quotes, at(0))
    assert (side, gap) == ("PREVIOUS", 10)
    assert chosen == quotes[1]
    assert proto.mid(chosen) == pytest.approx(1.00120)
    assert proto.relative_spread(chosen) == pytest.approx(40 / 100120)


def test_strict_pre_release_excludes_tick_at_release() -> None:
    quotes = [(at(-200), 99_900, 99_910), (at(0), 100_000, 100_010)]
    chosen, gap = proto.select_pre_release(quotes, at(0))
    assert chosen == quotes[0]
    assert gap == 200


def test_stale_and_incomplete_quote_selection_fails_closed() -> None:
    with pytest.raises(proto.PrototypeError):
        proto.select_pre_release([(at(-30_001), 100_000, 100_010)], at(0))
    with pytest.raises(proto.PrototypeError):
        proto.select_nearest([(at(30_001), 100_000, 100_010)], at(0))


def test_absolute_returns_and_direction_free_primary_rule() -> None:
    first = (at(-10), 100_000, 100_010)
    last = (at(10), 100_500, 100_510)
    assert proto.absolute_return(first, last) > 0
    assert proto.absolute_return(last, first) > 0
    assert proto.primary_decision(0.002, 0.003) == (
        True,
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "CREATE_NEW_CONFIRMATORY_OR_TRADING_HYPOTHESIS_BEFORE_R4",
    )
    assert proto.primary_decision(0.003, 0.003) == (False, "REJECT", "STOP_HYP0006")


def test_bi5_decoder_preserves_last_record_pair(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(proto, "ROOT", tmp_path)
    hour = datetime(2020, 1, 14, 13, 0, tzinfo=UTC)
    path = tmp_path / "data/raw/dukascopy/hyp0006/EURUSD/2020/01/14/13h_ticks.bi5"
    path.parent.mkdir(parents=True)
    packed = (
        proto.TICK_RECORD.pack(1800000, 100_010, 100_000, 1.0, 1.0)
        + proto.TICK_RECORD.pack(1800000, 100_050, 100_020, 2.0, 2.0)
        + proto.TICK_RECORD.pack(1800100, 100_060, 100_040, 3.0, 3.0)
    )
    path.write_bytes(lzma.compress(packed))
    identity = {
        "relative_path": path.relative_to(tmp_path).as_posix(),
        "sha256": proto.sha256_file(path),
        "record_count": 3,
    }
    quotes = proto.decode_quotes(path, hour, identity)
    assert quotes[1][1:] == (100_020, 100_050)
    selected, _, _ = proto.select_nearest(quotes, hour + timedelta(minutes=30))
    assert selected == quotes[1]


def test_import_is_pre_reveal_only_and_default_cli_is_blocked(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["hyp0006_proto01.py"])
    assert proto.main() == 2
