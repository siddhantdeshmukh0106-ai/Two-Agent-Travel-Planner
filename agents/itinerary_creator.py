import os
from crewai import Agent, LLM
from dotenv import load_dotenv
from tools.routing_tool import calculate_route
from tools.budget_tool import calculate_travel_budget
load_dotenv()


def create_itinerary_creator():
    """Create and return the Itinerary Creator Agent."""

    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL")

    if not api_key or not model_name:
        raise ValueError("Gemini configuration missing in .env")

    llm = LLM(
        model=model_name,
        api_key=api_key,
        temperature=0.4
    )

    itinerary_creator = Agent(
        role="Travel Itinerary Creator",

        goal=(
            "Create practical, personalized, and budget-conscious "
            "travel itineraries using destination research provided "
            "by the Local Expert Agent."
        ),

        backstory=(
            "You are an experienced travel planner specializing in "
            "organizing efficient travel schedules. You consider "
            "attraction proximity, opening hours, visiting durations, "
            "transportation time, meal breaks, traveler preferences, "
            "and budget limitations. You avoid unrealistic schedules "
            "and clearly identify uncertain costs or travel times."
        ),

        llm=llm,
        tools=[calculate_route, calculate_travel_budget],
        verbose=True,
        allow_delegation=False,
        max_iter=10,
        max_retry_limit=2,
    )

    return itinerary_creator