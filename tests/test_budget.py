from utils.validators import validate_budget
from tools.budget_tool import calculate_travel_budget


def test_budget_validation():

    print("\n========== TEST 1: WITHIN BUDGET ==========")

    result = validate_budget(
        total_budget=10000,
        attraction_cost=700,
        food_cost=2500,
        transport_cost=1500,
        accommodation_cost=3000,
        other_cost=500
    )

    print(result)

    assert result["total_expenses"] == 8200
    assert result["remaining_budget"] == 1800
    assert result["within_budget"] is True

    print("TEST 1 PASSED!")


    print("\n========== TEST 2: OVER BUDGET ==========")

    result = validate_budget(
        total_budget=10000,
        attraction_cost=2000,
        food_cost=3500,
        transport_cost=2500,
        accommodation_cost=4000,
        other_cost=1000
    )

    print(result)

    assert result["total_expenses"] == 13000
    assert result["remaining_budget"] == -3000
    assert result["within_budget"] is False

    print("TEST 2 PASSED!")


    print("\n========== TEST 3: EXACT BUDGET ==========")

    result = validate_budget(
        total_budget=10000,
        attraction_cost=1000,
        food_cost=2000,
        transport_cost=2000,
        accommodation_cost=4000,
        other_cost=1000
    )

    assert result["total_expenses"] == 10000
    assert result["remaining_budget"] == 0
    assert result["within_budget"] is True

    print("TEST 3 PASSED!")


    print("\n========== TEST 4: NEGATIVE EXPENSE ==========")

    try:
        validate_budget(
            total_budget=10000,
            attraction_cost=-500,
            food_cost=2000,
            transport_cost=1000
        )

        raise AssertionError("Negative expense was accepted!")

    except ValueError:
        print("TEST 4 PASSED!")


    print("\n========== TEST 5: CREWAI BUDGET TOOL ==========")

    output = calculate_travel_budget.run(
        10000, 700, 2500, 1500, 3000, 500
    )

    print(output)

    assert "Total Expenses: ₹8200.00" in output
    assert "Remaining Budget: ₹1800.00" in output
    assert "Within Budget: True" in output

    print("TEST 5 PASSED!")


    print("\n====================================")
    print("ALL BUDGET VALIDATION TESTS PASSED!")
    print("====================================")


if __name__ == "__main__":
    test_budget_validation()