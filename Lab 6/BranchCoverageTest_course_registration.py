"""Branch Coverage Test Suite for course_registration.py.

This module contains exhaustive unit tests specifically targeting every decision
branch, conditional outcome (True and False), and edge/boundary case in:
- can_register()
- waitlist_position()
- late_fee()

Achieves 100% Branch Coverage and 100% Line Coverage.
"""

import pytest
from course_registration import can_register, waitlist_position, late_fee


# ============================================================================
# Branch Coverage Tests for can_register()
# ============================================================================

def test_can_register_status_invalid_branch():
    """Branch: student_status not in MAX_CREDITS -> True (raises ValueError)."""
    with pytest.raises(ValueError, match="unknown status"):
        can_register("alumni", 10, 4, True)


def test_can_register_credits_zero_branch():
    """Branch: course_credits <= 0 -> True with 0 credits (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)


def test_can_register_credits_negative_branch():
    """Branch: course_credits <= 0 -> True with negative credits (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, -3, True)


def test_can_register_prerequisites_missing_branch():
    """Branch: not prerequisites_met -> True (returns 'prerequisites missing')."""
    assert can_register("regular", 10, 4, False) == "prerequisites missing"


def test_can_register_regular_limit_exceeded_branch():
    """Branch: current_credits + course_credits > 24 -> True for regular."""
    assert can_register("regular", 22, 4, True) == "credit limit exceeded"


def test_can_register_probation_limit_exceeded_branch():
    """Branch: current_credits + course_credits > 16 -> True for probation."""
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"


def test_can_register_honors_limit_exceeded_branch():
    """Branch: current_credits + course_credits > 28 -> True for honors."""
    assert can_register("honors", 26, 4, True) == "credit limit exceeded"


def test_can_register_regular_exact_boundary_branch():
    """Branch: sum == MAX_CREDITS (24 == 24) -> False on > limit (returns 'registered')."""
    assert can_register("regular", 20, 4, True) == "registered"


def test_can_register_probation_exact_boundary_branch():
    """Branch: sum == MAX_CREDITS (16 == 16) -> False on > limit (returns 'registered')."""
    assert can_register("probation", 12, 4, True) == "registered"


def test_can_register_honors_exact_boundary_branch():
    """Branch: sum == MAX_CREDITS (28 == 28) -> False on > limit (returns 'registered')."""
    assert can_register("honors", 24, 4, True) == "registered"


def test_can_register_below_limit_branch():
    """Branch: sum < MAX_CREDITS -> False on > limit (returns 'registered')."""
    assert can_register("regular", 10, 4, True) == "registered"


# ============================================================================
# Branch Coverage Tests for waitlist_position()
# ============================================================================

def test_waitlist_capacity_zero_branch():
    """Branch: capacity <= 0 -> True with capacity=0 (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)


def test_waitlist_capacity_negative_branch():
    """Branch: capacity <= 0 -> True with negative capacity (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, -5, 0)


def test_waitlist_seat_available_branch():
    """Branch: enrolled < capacity -> True (returns 0)."""
    assert waitlist_position(29, 30, 0) == 0


def test_waitlist_exact_capacity_branch():
    """Branch: enrolled < capacity -> False (enrolled == capacity), enters waitlist check."""
    assert waitlist_position(30, 30, 0) == 1


def test_waitlist_over_capacity_branch():
    """Branch: enrolled < capacity -> False (enrolled > capacity), enters waitlist check."""
    assert waitlist_position(35, 30, 2) == 3


def test_waitlist_full_exact_ten_branch():
    """Branch: waitlist_length >= 10 -> True at exact boundary 10 (returns -1)."""
    assert waitlist_position(30, 30, 10) == -1


def test_waitlist_full_greater_than_ten_branch():
    """Branch: waitlist_length >= 10 -> True with 15 (returns -1)."""
    assert waitlist_position(30, 30, 15) == -1


def test_waitlist_under_ten_boundary_nine_branch():
    """Branch: waitlist_length >= 10 -> False at boundary 9 (returns 10)."""
    assert waitlist_position(30, 30, 9) == 10


def test_waitlist_under_ten_general_branch():
    """Branch: waitlist_length >= 10 -> False with 4 (returns 5)."""
    assert waitlist_position(30, 30, 4) == 5


# ============================================================================
# Branch Coverage Tests for late_fee()
# ============================================================================

def test_late_fee_zero_days_branch():
    """Branch: days_late <= 0 -> True with 0 days (returns 0)."""
    assert late_fee(0, 16, False) == 0


def test_late_fee_negative_days_branch():
    """Branch: days_late <= 0 -> True with negative days (returns 0)."""
    assert late_fee(-4, 16, False) == 0


def test_late_fee_waiver_true_branch():
    """Branch: has_waiver -> True (returns 0)."""
    assert late_fee(5, 16, True) == 0


def test_late_fee_within_7_days_exact_boundary():
    """Branch: days_late <= 7 -> True at boundary 7, credits <= 20 (returns 500)."""
    assert late_fee(7, 20, False) == 500


def test_late_fee_within_7_days_less_than_7():
    """Branch: days_late <= 7 -> True with 3 days, credits <= 20 (returns 500)."""
    assert late_fee(3, 16, False) == 500


def test_late_fee_within_7_days_with_extra_credits():
    """Branch: days_late <= 7 -> True, credits > 20 -> True (500 + 250 = 750)."""
    assert late_fee(5, 22, False) == 750


def test_late_fee_beyond_7_days_boundary_eight():
    """Branch: days_late <= 7 -> False with 8 days, credits <= 20 (500 + 1*100 = 600)."""
    assert late_fee(8, 20, False) == 600


def test_late_fee_beyond_7_days_without_surcharge():
    """Branch: days_late <= 7 -> False (12 days), credits <= 20 -> False (1000)."""
    assert late_fee(12, 18, False) == 1000


def test_late_fee_beyond_7_days_with_surcharge_uncapped():
    """Branch: days_late <= 7 -> False, credits > 20 -> True, fee <= 2000 -> False on cap."""
    # 500 + (10 - 7) * 100 = 800; + 250 = 1050 (not capped)
    assert late_fee(10, 22, False) == 1050


def test_late_fee_exact_2000_cap_boundary():
    """Branch: fee > 2000 -> False when fee is exactly 2000."""
    # days_late = 22: 500 + (22 - 7) * 100 = 2000; credits = 18 (<= 20) -> no surcharge; fee = 2000
    assert late_fee(22, 18, False) == 2000


def test_late_fee_capped_at_2000_branch():
    """Branch: fee > 2000 -> True (fee exceeds 2000, capped to 2000)."""
    # days_late = 25: 500 + 1800 = 2300; credits = 24 -> +250 = 2550; capped at 2000
    assert late_fee(25, 24, False) == 2000
