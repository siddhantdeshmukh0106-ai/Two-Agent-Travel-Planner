from crewai.tools import tool
from utils.validators import validate_budget


@tool("Travel Budget Calculator")
def calculate_travel_budget(
    total_budget: float,
    attraction_cost: float,
    food_cost: float,
    transport_cost: float,
    accommodation_cost: float,
    other_cost: float
) -> str:
    """
    Calculate total trip expenses and check whether
    they fit within the user's budget.

    All expenses must cover all travelers.
    Use 0 only for categories confirmed to have no cost
    or explicitly excluded from the calculation.
    """

    result = validate_budget(
        total_budget=total_budget,
        attraction_cost=attraction_cost,
        food_cost=food_cost,
        transport_cost=transport_cost,
        accommodation_cost=accommodation_cost,
        other_cost=other_cost
    )

    return (
        f"Total Budget: ₹{result['total_budget']:.2f}\n"
        f"Attractions: ₹{attraction_cost:.2f}\n"
        f"Food: ₹{food_cost:.2f}\n"
        f"Transportation: ₹{transport_cost:.2f}\n"
        f"Accommodation: ₹{accommodation_cost:.2f}\n"
        f"Other Expenses: ₹{other_cost:.2f}\n"
        f"Total Expenses: ₹{result['total_expenses']:.2f}\n"
        f"Remaining Budget: ₹{result['remaining_budget']:.2f}\n"
        f"Within Budget: {result['within_budget']}"
    )