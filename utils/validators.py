def validate_budget(
    total_budget,
    attraction_cost,
    food_cost,
    transport_cost,
    accommodation_cost=0,
    other_cost=0
):
    """
    Calculate trip expenses and validate them
    against the user's total budget.

    All costs must be totals for all travelers.
    """

    expenses = {
        "Attractions": attraction_cost,
        "Food": food_cost,
        "Transportation": transport_cost,
        "Accommodation": accommodation_cost,
        "Other": other_cost
    }

    # Validate input values
    if total_budget < 0:
        raise ValueError("Total budget cannot be negative.")

    for category, amount in expenses.items():
        if amount < 0:
            raise ValueError(
                f"{category} cost cannot be negative."
            )

    # Calculate total expenses
    total_expenses = sum(expenses.values())

    # Calculate remaining budget
    remaining_budget = total_budget - total_expenses

    # Check budget status
    within_budget = total_expenses <= total_budget

    return {
        "total_budget": total_budget,
        "expenses": expenses,
        "total_expenses": total_expenses,
        "remaining_budget": remaining_budget,
        "within_budget": within_budget
    }

from datetime import date
from pydantic import ValidationError


def validate_travel_inputs(
    destination,
    budget,
    start_date,
    end_date,
    travelers,
    preferences
):
    """Validate user inputs before executing the AI agents."""

    if not isinstance(destination, str) or not destination.strip():
        raise ValueError("Please enter a valid destination.")

    if len(destination.strip()) > 150:
        raise ValueError("Destination name is too long.")

    if not isinstance(budget, (int, float)) or isinstance(budget, bool):
        raise ValueError("Budget must be a valid number.")

    if budget <= 0:
        raise ValueError("Budget must be greater than ₹0.")

    if not isinstance(travelers, int) or isinstance(travelers, bool):
        raise ValueError("Number of travelers must be an integer.")

    if not 1 <= travelers <= 20:
        raise ValueError("Number of travelers must be between 1 and 20.")

    if not isinstance(start_date, date) or not isinstance(end_date, date):
        raise ValueError("Please select valid travel dates.")

    if start_date < date.today():
        raise ValueError("Travel start date cannot be in the past.")

    if end_date < start_date:
        raise ValueError("End date cannot be before start date.")

    if (end_date - start_date).days > 30:
        raise ValueError("Trips longer than 31 days are not supported.")

    if not preferences:
        raise ValueError("Please select at least one travel preference.")

    return True