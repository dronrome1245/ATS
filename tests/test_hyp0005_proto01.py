"""Synthetic-only HYP-0005 confirmatory runner tests; never open protected CSV."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from tools import hyp0005_proto01 as proto


def synthetic_row(timestamp: datetime, segment: str, bid: float = 1.1) -> dict:
    return {
        "event_time": timestamp,
        "confirmatory_segment": segment,
        "utc_bucket": proto._load_frozen_dependencies()[1].bucket_for_hour(timestamp.hour),
        "bid_open": bid,
        "ask_open": bid + 0.0002,
    }


def test_default_cli_and_unapproved_reveal_are_blocked(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    monkeypatch.setattr(proto, "DATA_PATH", tmp_path / "protected.csv")
    assert proto.main() == 2
    with pytest.raises(proto.ConfirmatoryProtoError, match="authorization required"):
        proto.run_first_reveal_once()
    assert not (tmp_path / "protected.csv").exists()


def test_inherited_fixed_utc_buckets_have_no_alternates() -> None:
    base, prep = proto._load_frozen_dependencies()
    assert proto.BUCKETS == ("CORE_ACTIVE", "TRANSITION", "OFF_HOURS")
    assert [base.bucket_for_hour(h) for h in range(24)] == [
        prep.bucket_for_hour(h) for h in range(24)
    ]
    assert proto.EXPECTED_GEOMETRY["eligible_rows_by_bucket"] == {
        "CORE_ACTIVE": 838,
        "OFF_HOURS": 837,
        "TRANSITION": 316,
    }


def test_exact_next_hour_requires_same_segment_and_existing_hour() -> None:
    left = datetime(2003, 5, 5, 6, tzinfo=UTC)
    right = datetime(2026, 9, 1, 6, tzinfo=UTC)
    rows = {
        ("LEFT_UNSEEN", left + timedelta(hours=h)): synthetic_row(
            left + timedelta(hours=h), "LEFT_UNSEEN"
        )
        for h in (0, 1, 2)
    }
    rows.update(
        {
            ("RIGHT_UNSEEN", right + timedelta(hours=h)): synthetic_row(
                right + timedelta(hours=h), "RIGHT_UNSEEN"
            )
            for h in (0, 2)
        }
    )
    assert proto.frozen_eligible_keys(rows) == [
        ("LEFT_UNSEEN", left),
        ("LEFT_UNSEEN", left + timedelta(hours=1)),
    ]


def test_synthetic_geometry_is_frozen_before_outcome_computation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, preparation = proto._load_frozen_dependencies()
    rows = {}
    for segment, start in (
        ("LEFT_UNSEEN", datetime(2003, 5, 5, 6, tzinfo=UTC)),
        ("RIGHT_UNSEEN", datetime(2026, 9, 1, 6, tzinfo=UTC)),
    ):
        for h in (0, 1, 2):
            when = start + timedelta(hours=h)
            rows[(segment, when)] = synthetic_row(when, segment)
    synthetic = preparation.geometry_summary(list(rows.values()))
    monkeypatch.setattr(proto, "EXPECTED_GEOMETRY", synthetic)
    assert len(proto.frozen_geometry(rows)) == 4
    rows.pop(("RIGHT_UNSEEN", datetime(2026, 9, 1, 7, tzinfo=UTC)))
    with pytest.raises(proto.ConfirmatoryProtoError, match="geometry drift"):
        proto.frozen_geometry(rows)


def test_exact_parent_formulas_and_two_independent_primary_booleans() -> None:
    base, _ = proto._load_frozen_dependencies()
    assert base.abs_next_1h_return(1.0, 1.002, 1.02, 1.022) > 0
    assert base.relative_spread(1.0, 1.002) > 0
    observations = [
        {
            "year": 2003,
            "utc_bucket": "CORE_ACTIVE",
            "abs_next_1h_return": 0.02,
            "relative_spread": 0.001,
        },
        {
            "year": 2026,
            "utc_bucket": "OFF_HOURS",
            "abs_next_1h_return": 0.01,
            "relative_spread": 0.002,
        },
        {
            "year": 2003,
            "utc_bucket": "TRANSITION",
            "abs_next_1h_return": 0.9,
            "relative_spread": 0.9,
        },
    ]
    passed = proto.evaluate_synthetic_or_revealed(observations)
    assert passed["decision"] == "CONFIRMATORY_STRUCTURAL_PASS"
    assert passed["primary"]["movement_inequality_pass"] is True
    assert passed["primary"]["spread_inequality_pass"] is True
    observations[1]["relative_spread"] = 0.0001
    failed = proto.evaluate_synthetic_or_revealed(observations)
    assert failed["decision"] == "CONFIRMATORY_STRUCTURAL_FAIL"
    assert failed["primary"]["movement_inequality_pass"] is True
    assert failed["primary"]["spread_inequality_pass"] is False
    observations[1]["relative_spread"] = 0.002
    observations[0]["abs_next_1h_return"] = 0.001
    movement_failed = proto.evaluate_synthetic_or_revealed(observations)
    assert movement_failed["decision"] == "CONFIRMATORY_STRUCTURAL_FAIL"
    assert movement_failed["primary"]["movement_inequality_pass"] is False
    assert movement_failed["primary"]["spread_inequality_pass"] is True


def test_no_positive_result_grants_trading_admission() -> None:
    observations = [
        {
            "year": 2003,
            "utc_bucket": "CORE_ACTIVE",
            "abs_next_1h_return": 0.02,
            "relative_spread": 0.001,
        },
        {
            "year": 2026,
            "utc_bucket": "OFF_HOURS",
            "abs_next_1h_return": 0.01,
            "relative_spread": 0.002,
        },
    ]
    result = proto.evaluate_synthetic_or_revealed(observations)
    assert result["decision"] == "CONFIRMATORY_STRUCTURAL_PASS"
    assert result["next_action"] == "REVIEW_CONFIRMATORY_STRUCTURAL_EVIDENCE_NO_DIRECT_R4"
