from crewai import Task
from models.schemas import TravelItinerary

def create_itinerary_task(
    agent,
    destination,
    budget,
    travel_dates,
    travelers,
    preferences
):
    """Create the itinerary generation task."""

    itinerary_task = Task(

        description=f"""
        Create a personalized travel itinerary using the
        destination research provided by the Local Expert Agent.
        
        

        TRAVELER DETAILS:
        Destination: {destination}
        Total Budget: ₹{budget}
        Travel Dates: {travel_dates}
        Number of Travelers: {travelers}
        Preferences: {preferences}
        
        STRUCTURED OUTPUT REQUIREMENTS:
        - Return data matching the TravelItinerary schema.
        - Use YYYY-MM-DD for dates.
        - Use HH:MM (24-hour format) for activity times.
        - Include all activities in chronological order.
        - Activity costs must cover all travelers.
        - Use null for unknown costs and routing information.
        - Include a BudgetBreakdown object.
        - Use the Travel Budget Calculator for expense calculations.
        - Ensure budget totals and remaining balance are consistent.
        - Use PARTIAL ESTIMATE when any expense category is unknown.
        - Do not invent routing results, opening hours, or prices.

        INSTRUCTIONS:

        1. Create a day-wise itinerary covering the travel dates.

        2. Include a realistic hour-by-hour schedule with:
           - Activity or attraction name
           - Start and end time
           - Estimated visiting duration
           - Meal and rest breaks
           - Estimated activity cost

        3. Use the attractions, hidden gems, and food
           recommendations researched by Agent 1.

        4. Group nearby attractions together to reduce
           unnecessary travel.

        5. Consider opening hours and recommended visit durations.

        6. Use the Travel Route Calculator tool to calculate
           road distances and estimated driving times between
           consecutive attractions.

           Include:
           - Origin and destination
           - Road distance in kilometers
           - Estimated driving time in minutes

           If routing fails, clearly mark the travel time
           as unverified.

           Estimate transportation costs separately.
        
        7. Use the Travel Budget Calculator tool to calculate
           total trip expenses for all travelers.

           Include:
           - Attraction costs
           - Food costs
           - Transportation costs
           - Accommodation costs
           - Other expenses

           Never invent missing expense values.

           If a cost is unknown, clearly identify it.
           Calculate a subtotal using known or estimated costs
           and explain that the full trip budget is not verified.

           Use the calculator's result to determine whether
           the calculated expenses fit within the budget.

        8. Compare estimated expenses against the total budget.

        9. If the estimated expenses exceed the budget,
           suggest cheaper alternatives.

        10. Do not invent verified travel times, ticket
            prices, or opening hours.

        IMPORTANT:
        - Use Agent 1's research as the primary information source.
        - Use routing API results only when successfully
          returned by the Travel Route Calculator.
        - Routing estimates do not include live traffic.
        - Do not invent routing results if the tool fails.
        - Do not schedule attractions outside known opening hours.
        - Clearly flag missing or uncertain information.
        - Avoid overcrowded or unrealistic schedules.
        - If accommodation or intercity travel costs are
          unknown, exclude them from the calculated subtotal
          and clearly state that the full trip budget
          cannot yet be verified.
        """,

        expected_output="""
         Generate a complete, structured travel itinerary.

         1. TRIP OVERVIEW
            - Destination
            - Travel Dates
            - Number of Travelers
            - Total Budget

         2. DAY-WISE ITINERARY
            For each day, include:
            - Time
            - Attraction / Activity
            - Visit Duration
            - Travel Distance
            - Estimated Travel Time
            - Estimated Activity Cost
            - Meal Breaks

         3. FOOD RECOMMENDATIONS
            - Breakfast
            - Lunch
            - Dinner
            - Estimated Food Expenses

         4. DETAILED BUDGET BREAKDOWN

            Display the following table:

            | Expense Category | Estimated Cost (₹) |
            |------------------|--------------------|
            | Attractions      | Amount             |
            | Food             | Amount             |
            | Transportation   | Amount             |
            | Accommodation    | Amount             |
            | Other Expenses   | Amount             |
            | TOTAL EXPENSES   | Amount             |
            | REMAINING BUDGET | Amount             |

            Use the Travel Budget Calculator tool for calculations.

            IMPORTANT:
            - All expenses must cover all travelers.
            - Distinguish verified costs from estimates.
            - Mark unknown or excluded expenses clearly.
            - Do not treat unknown expenses as free.
            - If any category is excluded, label the total
            as a partial estimate rather than the full trip cost.

         5. BUDGET STATUS

            Display one of the following:

            WITHIN BUDGET:
            Calculated expenses do not exceed the user's budget.

            OVER BUDGET:
            Calculated expenses exceed the user's budget.

            PARTIAL ESTIMATE:
            Some required expenses are unknown or excluded,
            so the full trip budget cannot be verified.

            If over budget, suggest cheaper alternatives.

         6. TRAVEL TIPS
            - Transportation suggestions
            - Best visiting times
            - Practical recommendations

         7. ASSUMPTIONS AND LIMITATIONS
            - Unverified opening hours
            - Estimated transportation costs
            - Missing expense information
            - Routing limitations
         """,

        agent=agent,
        output_pydantic=TravelItinerary
    )

    return itinerary_task