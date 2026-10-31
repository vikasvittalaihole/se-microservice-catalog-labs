import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# extra_time_charge: service not in INCLUDED_MIN -> True / False
def test_branch_unknown_service_true():
    with pytest.raises(ValueError):
        extra_time_charge("nails", 10, "junior", False)


def test_branch_unknown_service_false():
    assert extra_time_charge("haircut", 30, "junior", False) == 0


# duration_min < 0 -> True / False
def test_branch_negative_duration_true():
    with pytest.raises(ValueError):
        extra_time_charge("spa", -5, "junior", False)


def test_branch_negative_duration_false():
    assert extra_time_charge("spa", 0, "junior", False) == 0


# is_member and service != "spa" -> True / False
def test_branch_member_non_spa_true():
    assert extra_time_charge("colour", 74, "junior", True) == 0


def test_branch_member_false():
    assert extra_time_charge("colour", 74, "junior", False) == 14 * 10


def test_branch_member_spa_false():
    # spa is excluded from the membership bonus
    assert extra_time_charge("spa", 100, "junior", True) == 10 * 10


# extra <= 0 -> True / False
def test_branch_extra_nonpositive_true():
    assert extra_time_charge("spa", 90, "senior", False) == 0


def test_branch_extra_positive_false():
    assert extra_time_charge("spa", 91, "senior", False) == 18


# stylist_level == "junior" -> True / False
def test_branch_junior_true():
    assert extra_time_charge("haircut", 35, "junior", False) == 5 * 10


def test_branch_junior_false():
    assert extra_time_charge("haircut", 35, "senior", False) == 5 * 18


# extra > 60 -> True / False
def test_branch_extra_over_60_false():
    assert extra_time_charge("haircut", 80, "junior", False) == 50 * 10


def test_branch_extra_over_60_true():
    assert extra_time_charge("haircut", 120, "junior", False) == 90 * 18


# stylist_level == "senior" inside extra > 60 -> True / False
def test_branch_over_60_senior_true():
    assert extra_time_charge("haircut", 120, "senior", False) == 90 * 30


def test_branch_over_60_nonsenior_false():
    assert extra_time_charge("haircut", 120, "mid", False) == 90 * 26


# can_book: is_walk_in -> True / False
def test_branch_walk_in_true():
    assert can_book(1, 9, True) is True


def test_branch_walk_in_false_party_big():
    assert can_book(5, 1, False) is False


# can_book non-walk-in: party_size > 4 -> True / False
def test_branch_party_over_4_true():
    assert can_book(5, 1, False) is False


def test_branch_party_over_4_false_services_over():
    assert can_book(4, 3, False) is False


def test_branch_party_ok_services_ok():
    assert can_book(4, 2, False) is True


# arrival_status: is_colour -> True / False
def test_branch_colour_true():
    assert arrival_status(10, True, False) == "open"


def test_branch_colour_false():
    assert arrival_status(5, False, False) == "open"


# is_weekend -> True / False
def test_branch_weekend_true():
    assert arrival_status(7, False, True) == "late"


def test_branch_weekend_false():
    assert arrival_status(5, False, False) == "open"


# minutes_early >= cutoff -> True ; elif -> True ; else -> closed
def test_branch_open_true():
    assert arrival_status(5, False, False) == "open"


def test_branch_late_elif_true():
    assert arrival_status(0, False, False) == "late"


def test_branch_elif_false_closed():
    assert arrival_status(-20, False, False) == "closed"
