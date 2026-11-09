"""Code Coverage Test Suite for course_registration.py.

This module contains unit tests designed to achieve 100% line/statement
coverage for all functions in course_registration.py:
- can_register
- waitlist_position
- late_fee
"""

import pytest
from course_registration import can_register, waitlist_position, late_fee


# ============================================================================
# Tests for can_register() - Line Coverage
# ============================================================================

def test_can_register_unknown_status():
    """Verify ValueError is raised when student_status is not in MAX_CREDITS."""
    with pytest.raises(ValueError, match="unknown status"):
        can_register("guest", 10, 4, True)


def test_can_register_invalid_credits():
    """Verify ValueError is raised when course_credits is <= 0."""
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)


def test_can_register_prerequisites_missing():
    """Verify 'prerequisites missing' is returned when prerequisites_met is False."""
    assert can_register("regular", 10, 4, False) == "prerequisites missing"


def test_can_register_credit_limit_exceeded():
    """Verify 'credit limit exceeded' is returned when credit limit is exceeded."""
    assert can_register("regular", 22, 4, True) == "credit limit exceeded"


def test_can_register_success():
    """Verify 'registered' is returned when all registration checks pass."""
    assert can_register("regular", 18, 4, True) == "registered"


# ============================================================================
# Tests for waitlist_position() - Line Coverage
# ============================================================================

def test_waitlist_position_invalid_capacity():
    """Verify ValueError is raised when capacity is <= 0."""
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)


def test_waitlist_position_seat_available():
    """Verify 0 is returned when enrolled < capacity."""
    assert waitlist_position(25, 30, 0) == 0


def test_waitlist_position_waitlist_full():
    """Verify -1 is returned when waitlist_length is >= 10."""
    assert waitlist_position(30, 30, 10) == -1


def test_waitlist_position_added_to_waitlist():
    """Verify waitlist_length + 1 is returned when waitlist is not full."""
    assert waitlist_position(30, 30, 4) == 5


# ============================================================================
# Tests for late_fee() - Line Coverage
# ============================================================================

def test_late_fee_not_late():
    """Verify fee is 0 when days_late is <= 0."""
    assert late_fee(0, 16, False) == 0


def test_late_fee_has_waiver():
    """Verify fee is 0 when student has a waiver."""
    assert late_fee(5, 16, True) == 0


def test_late_fee_within_7_days():
    """Verify base fee of 500 when days_late <= 7 and credits <= 20."""
    assert late_fee(5, 16, False) == 500


def test_late_fee_beyond_7_days_with_extra_credits_capped():
    """Verify calculation for days_late > 7, credits > 20, and fee capped at 2000."""
    # days_late = 25: 500 + (25 - 7) * 100 = 2300; credits = 24 (>20) -> +250 = 2550; capped at 2000
    assert late_fee(25, 24, False) == 2000
