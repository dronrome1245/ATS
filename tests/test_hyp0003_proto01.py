"""Synthetic contract tests for frozen HYP-0003 PROTO-01 logic."""

from tools.hyp0003_proto01 import (
    basket_size,
    breadth_summary,
    loser_short_return,
    observation_turnover,
    prototype_decision,
    select_baskets,
    winner_long_return,
)


def make_cells(value: float, observation_count: int = 10) -> list[dict[str, object]]:
    return [
        {
            "formation_months": formation,
            "holding_months": holding,
            "observation_count": observation_count,
            "mean_return": value if observation_count else None,
        }
        for formation in (1, 3, 6, 9, 12)
        for holding in (1, 3, 6, 9, 12)
    ]


def test_basket_size_uses_frozen_one_sixth_ceiling() -> None:
    assert basket_size(6) == 1
    assert basket_size(7) == 2
    assert basket_size(9) == 2


def test_basket_selection_uses_currency_code_tie_break() -> None:
    returns = {
        "AUD": 0.02,
        "CAD": -0.01,
        "CHF": -0.01,
        "EUR": 0.00,
        "GBP": 0.01,
        "JPY": 0.02,
    }

    winners, losers = select_baskets(returns)

    assert winners == ("AUD",)
    assert losers == ("CAD",)


def test_executable_winner_and_loser_side_conventions() -> None:
    entry = (1.0100, 1.0110, 1.0102, 1.0112)
    exit_bar = (1.0200, 1.0210, 1.0202, 1.0212)

    assert winner_long_return(entry, exit_bar) == 1.0200 / 1.0102 - 1.0
    assert loser_short_return(entry, exit_bar) == 1.0100 / 1.0202 - 1.0


def test_observation_turnover_is_zero_for_same_baskets_and_one_for_replacement() -> None:
    first = {"winners": ("AUD", "EUR"), "losers": ("CAD", "CHF")}
    same = {"winners": ("AUD", "EUR"), "losers": ("CAD", "CHF")}
    replaced = {"winners": ("GBP", "JPY"), "losers": ("NOK", "SEK")}

    assert observation_turnover(first, same) == 0.0
    assert observation_turnover(first, replaced) == 1.0


def test_breadth_and_decision_contract() -> None:
    passing = make_cells(0.001)
    breadth = breadth_summary(passing)

    assert breadth["median_positive"] is True
    assert breadth["positive_mean_cell_count"] == 25
    assert breadth["formation_span_pass"] is True
    assert breadth["holding_span_pass"] is True
    assert prototype_decision(passing) == (
        "ADVANCE_TO_ECONOMIC_SCREEN",
        "ALL_BROAD_REGION_CRITERIA_MET",
        "CREATE_NEW_CONFIRMATORY_HYPOTHESIS_BEFORE_R4",
    )

    failing = make_cells(-0.001)
    assert prototype_decision(failing) == (
        "REJECT",
        "ONE_OR_MORE_BROAD_REGION_CRITERIA_FAILED",
        "STOP_HYP0003",
    )

    parked = make_cells(0.001)
    parked[0]["observation_count"] = 0
    parked[0]["mean_return"] = None
    assert prototype_decision(parked) == (
        "PARK",
        "ONE_OR_MORE_DECLARED_CELLS_HAVE_ZERO_OBSERVATIONS",
        "PARK",
    )
