from hypothesis import given, strategies as st
from salon_booking import parse_booking, duration_average, payable_bill

# A ValueError is a controlled rejection of bad input and is allowed.
# Any other exception type (AttributeError, TypeError, ...) is a bug.

@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"parse_booking crashed with: {type(e).__name__}: {e}"

@given(st.text() | st.none())
def test_duration_average_no_crash(s):
    try:
        duration_average(s)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"duration_average crashed with: {type(e).__name__}: {e}"

@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    try:
        payable_bill(s)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"payable_bill crashed with: {type(e).__name__}: {e}"