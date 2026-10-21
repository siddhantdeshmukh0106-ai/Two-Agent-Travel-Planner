import math

from tools.routing_tool import calculate_route
from tools.budget_tool import calculate_travel_budget
from utils.validators import validate_budget
from models.schemas import BudgetBreakdown


def test_routing():

    print("\n========== TEST 1: ROUTING ==========")

    origin = "Amber Fort, Jaipur, Rajasthan, India"
    destination = "Hawa Mahal, Jaipur, Rajasthan, India"

    result = calculate_route.run(origin, destination)

    print("\nRouting Result:")
    print(result)

    assert isinstance(result, str)
    assert result.strip()

    # Inspect the response for routing errors.
    error_keywords = [
        "error",
        "failed",
        "not found",
        "unable",
        "could not"
    ]

    assert not any(
        keyword in result.lower()
        for keyword in error_keywords
    ), "Routing tool returned an error."

    print("\nRouting Tool: PASSED")


def test_budget():

    print("\n========== TEST 2: BUDGET ==========")

    result = validate_budget(
        total_budget=10000,
        attraction_cost=700,
        food_cost=2500,
        transport_cost=1500,
        accommodation_cost=3000,
        other_cost=500
    )

    print("\nBudget Result:")
    print(result)

    assert math.isclose(result["total_expenses"], 8200)
    assert math.isclose(result["remaining_budget"], 1800)
    assert result["within_budget"] is True

    print("\nBudget Calculation: PASSED")


def test_budget_tool():

    print("\n========== TEST 3: BUDGET TOOL ==========")

    result = calculate_travel_budget.run(
        10000,
        700,
        2500,
        1500,
        3000,
        500
    )

    print("\nBudget Tool Result:")
    print(result)

    assert isinstance(result, str)
    assert result.strip()

    print("\nBudget Tool: PASSED")


def test_budget_schema():

    print("\n========== TEST 4: PYDANTIC ==========")

    budget = BudgetBreakdown(
        attraction_cost=700,
        food_cost=2500,
        transport_cost=1500,
        accommodation_cost=3000,
        other_cost=500,
        total_budget=10000,
        total_expenses=8200,
        remaining_budget=1800,
        within_budget=True,
        budget_status="WITHIN BUDGET"
    )

    assert budget.total_expenses == 8200
    assert budget.remaining_budget == 1800
    assert budget.within_budget is True

    print("\nPydantic Budget Validation: PASSED")


def test_over_budget():

    print("\n========== TEST 5: OVER BUDGET ==========")

    result = validate_budget(
        total_budget=5000,
        attraction_cost=2000,
        food_cost=2500,
        transport_cost=1500,
        accommodation_cost=3000,
        other_cost=500
    )

    assert result["within_budget"] is False
    assert result["remaining_budget"] == -4500

    print("\nOver-Budget Detection: PASSED")


if __name__ == "__main__":

    test_routing()
    test_budget()
    test_budget_tool()
    test_budget_schema()
    test_over_budget()

    print("\n======================================")
    print("ALL ROUTING & BUDGET TESTS PASSED!")
    print("======================================")