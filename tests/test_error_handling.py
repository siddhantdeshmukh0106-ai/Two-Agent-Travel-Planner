from datetime import date, timedelta

from utils.validators import validate_travel_inputs
from utils.error_handler import handle_application_error


def test_valid_inputs():

    result = validate_travel_inputs(
        destination="Jaipur",
        budget=10000,
        start_date=date.today() + timedelta(days=10),
        end_date=date.today() + timedelta(days=12),
        travelers=2,
        preferences=["History", "Food"]
    )

    assert result is True

    print("Valid input test: PASSED")


def test_invalid_destination():

    try:
        validate_travel_inputs(
            destination="",
            budget=10000,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=12),
            travelers=2,
            preferences=["History"]
        )

    except ValueError:
        print("Invalid destination test: PASSED")
        return

    raise AssertionError("Invalid destination was accepted.")


def test_invalid_budget():

    try:
        validate_travel_inputs(
            destination="Jaipur",
            budget=-500,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=12),
            travelers=2,
            preferences=["History"]
        )

    except ValueError:
        print("Invalid budget test: PASSED")
        return

    raise AssertionError("Invalid budget was accepted.")


def test_invalid_dates():

    try:
        validate_travel_inputs(
            destination="Jaipur",
            budget=10000,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=5),
            travelers=2,
            preferences=["History"]
        )

    except ValueError:
        print("Invalid dates test: PASSED")
        return

    raise AssertionError("Invalid dates were accepted.")


def test_api_error():

    error = Exception("429 Rate limit exceeded")

    message = handle_application_error(error)

    assert "usage limit" in message.lower()

    print("API error handling test: PASSED")


if __name__ == "__main__":

    test_valid_inputs()
    test_invalid_destination()
    test_invalid_budget()
    test_invalid_dates()
    test_api_error()

    print("\nALL ERROR HANDLING TESTS PASSED!")