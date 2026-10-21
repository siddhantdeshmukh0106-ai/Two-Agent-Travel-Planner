from crewai import Task
from models.schemas import DestinationResearch

def create_research_task(
    agent,
    destination,
    budget,
    travel_dates,
    travelers,
    preferences
):
    """
    Creates the destination research task
    for the Local Expert Agent.
    """

    research_task = Task(

        description=f"""
        You are responsible for researching a travel destination
        and preparing useful information for a personalized
        travel itinerary.
        
        
        TRAVELER DETAILS:
        -----------------
        Destination: {destination}
        Total Budget: ₹{budget}
        Travel Dates: {travel_dates}
        Number of Travelers: {travelers}
        Preferences: {preferences}

        YOUR RESPONSIBILITIES:
        ----------------------

        1. Identify the top 3 tourist attractions in
           {destination} that match the traveler's interests.

        2. Recommend 2 lesser-known attractions or hidden gems.

        3. Suggest 3 local dishes or food experiences
           that travelers should try.

        4. For each attraction, provide:
           - Name
           - Short description
           - Approximate entry fee
           - Opening hours
           - Recommended visiting duration
           - Location or area

        5. Consider the traveler's total budget and
           number of travelers when recommending activities.

        6. Provide practical travel tips relevant to
           the destination and travel dates.

        STRUCTURED OUTPUT REQUIREMENTS:
        - Return exactly 3 top attractions, 2 hidden gems, and 3 local foods.
        - Include all fields required by the DestinationResearch schema.
        - Use null for unknown prices, hours, or source URLs where permitted.
        - Entry fees and food costs must be per person in INR.
        - Visit durations must be positive numbers in hours.
        - Do not invent source URLs or missing information.
         
        IMPORTANT GUIDELINES:
        ---------------------
        - Prioritize attractions matching user preferences.
        - Avoid recommending unnecessarily expensive activities.
        - Do not invent exact prices or opening hours.
        - Clearly mark uncertain information as unverified.
        - Do not claim information is current unless verified
          through a reliable source.
        - Do not create a day-wise itinerary.
        - Your responsibility is research only.
        - The Itinerary Creator Agent will handle scheduling.
        """,

        expected_output="""
        A structured destination research report containing:

        1. Destination Overview

        2. Top 3 Tourist Attractions
           - Name
           - Description
           - Entry Fee
           - Opening Hours
           - Recommended Visit Duration
           - Location

        3. Hidden Gems (2)
           - Name
           - Description
           - Entry Fee
           - Opening Hours
           - Recommended Visit Duration
           - Location

        4. Local Food Recommendations (3)
           - Dish or Food Experience
           - Description
           - Approximate Cost

        5. Budget Considerations
           - Estimated attraction expenses
           - Budget-friendly suggestions

        6. Practical Travel Tips

        7. Sources and Verification Notes
           - Source links, if available
           - Clearly identified unverified details

        The report must be clear, organized, and suitable
        for use by the Itinerary Creator Agent.
        """,

        agent=agent,
        output_pydantic=DestinationResearch
        
    )

    return research_task