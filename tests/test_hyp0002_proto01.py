"""Synthetic contract tests for frozen HYP-0002 PROTO-01 logic."""

from tools.hyp0002_proto01 import (
    down_signed_return,
    prototype_decision,
    up_signed_return,
)


def test_signed_return_side_conventions() -> None:
    entry = {"bid_open": 1.0100, "ask_open": 1.0102}
    exit_bar = {"bid_open": 1.0200, "ask_open": 1.0202}

    assert up_signed_return(entry, exit_bar) == 1.0200 / 1.0102 - 1.0
    assert down_signed_return(entry, exit_bar) == 1.0100 / 1.0202 - 1.0


def test_two_sided_decision_contract() -> None:
    passing = {
        "event_count": 10,
        "mean_signed_return": 0.001,
        "mean_minus_baseline": 0.0005,
    }
    failing = {
        "event_count": 10,
        "mean_signed_return": -0.001,
        "mean_minus_baseline": 0.0005,
    }
    empty = {
        "event_count": 0,
        "mean_signed_return": 0.0,
        "mean_minus_baseline": 0.0,
    }

    assert prototype_decision(passing, passing) == (
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "ALL_FOUR_PRIMARY_INEQUALITIES_MET",
    )
    assert prototype_decision(passing, failing) == (
        "REJECT",
        "ONE_OR_MORE_PRIMARY_INEQUALITIES_FAILED",
    )
    assert prototype_decision(passing, empty) == (
        "PARK",
        "ONE_OR_BOTH_TAILS_HAVE_ZERO_EVENTS",
    )
