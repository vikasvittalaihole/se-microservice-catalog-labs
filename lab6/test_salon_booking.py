import pytest
from salon_booking import extra_time_charge, can_book, arrival_status

# Example test cases:
def test_within_included_time():
    assert extra_time_charge("haircut", 20, "junior", False) == 0

def test_can_book():
    assert can_book(2, 1, False) is True

# Unknown service and negative duration raise ValueError
def test_unknown_service_raises():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("massage", 60, "junior", False)

def test_negative_duration_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -1, "junior", False)

# Extra time charges
def test_junior_small_overrun():
    # haircut 30 included, 40 min -> 10 extra at junior rate 10
    assert extra_time_charge("haircut", 40, "junior", False) == 100

def test_non_junior_small_overrun():
    # haircut 30 included, 40 min -> 10 extra at rate 18
    assert extra_time_charge("haircut", 40, "senior", False) == 180

def test_member_gets_extra_15_minutes():
    # haircut member: 45 included, 50 min -> 5 extra at rate 10
    assert extra_time_charge("haircut", 50, "junior", True) == 50

def test_member_spa_no_bonus():
    # spa member gets no bonus: 90 included, 100 min -> 10 extra at rate 18
    assert extra_time_charge("spa", 100, "senior", True) == 180

def test_large_overrun_junior():
    # colour 60 included, 150 min -> 90 extra at rate 10 + 8 = 18
    assert extra_time_charge("colour", 150, "junior", False) == 90 * 18

def test_large_overrun_senior():
    # colour 60 included, 150 min -> 90 extra at rate 18 + 8 + 4 = 30
    assert extra_time_charge("colour", 150, "senior", False) == 90 * 30

def test_exactly_included_time_is_zero():
    assert extra_time_charge("spa", 90, "senior", False) == 0

# can_book
def test_walk_in_allowed():
    assert can_book(2, 5, True) is True

def test_walk_in_party_too_big():
    assert can_book(3, 1, True) is False

def test_party_too_big():
    assert can_book(5, 1, False) is False

def test_too_many_services():
    assert can_book(2, 3, False) is False

def test_valid_booking_max_party():
    assert can_book(4, 2, False) is True

# arrival_status
def test_arrival_open_weekday_hair():
    assert arrival_status(5, False, False) == "open"

def test_arrival_late_colour_weekend():
    # colour weekend cutoff 20, late window 5..19
    assert arrival_status(10, True, True) == "late"

def test_arrival_late_weekday_hair():
    assert arrival_status(0, False, False) == "late"

def test_arrival_closed():
    assert arrival_status(-20, False, False) == "closed"

def test_arrival_colour_open_weekday():
    assert arrival_status(10, True, False) == "open"

def test_arrival_weekend_open():
    assert arrival_status(15, False, True) == "open"
