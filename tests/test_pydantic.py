from datetime import date

from crew import create_travel_crew
from models.schemas import (
    DestinationResearch,
    TravelItinerary
)


def test_structured_configuration():

    print("\n========== TEST 1: CREW CONFIGURATION ==========")

    crew = create_travel_crew(
        destination="Jaipur, Rajasthan",
        budget=10000,
        travel_dates="15-16 November 2026",
        travelers=2,
        preferences="History, Photography, Local Food"
    )

    assert len(crew.agents) == 2
    assert len(crew.tasks) == 2

    print("Crew configuration: PASSED")


    print("\n========== TEST 2: RESEARCH SCHEMA ==========")

    assert crew.tasks[0].output_pydantic == DestinationResearch

    print("Agent 1 Pydantic schema: PASSED")


    print("\n========== TEST 3: ITINERARY SCHEMA ==========")

    assert crew.tasks[1].output_pydantic == TravelItinerary

    print("Agent 2 Pydantic schema: PASSED")


    print("\n========== TEST 4: TASK CONTEXT ==========")

    assert crew.tasks[0] in crew.tasks[1].context

    print("Agent communication: PASSED")


    print("\n========== TEST 5: MODEL VALIDATION ==========")

    from models.schemas import TravelActivity

    activity = TravelActivity(
        activity_name="Amber Fort Visit",
        location="Jaipur",
        description="Explore the historical fort",
        start_time="09:00",
        end_time="12:00",
        duration_minutes=180,
        estimated_cost=200,
        travel_distance_km=5,
        travel_time_minutes=15,
        activity_type="Attraction"
    )

    assert activity.duration_minutes == 180
    assert activity.estimated_cost == 200

    print("Pydantic validation: PASSED")


    print("\n========================================")
    print("ALL STRUCTURED CONFIGURATION TESTS PASSED!")
    print("========================================")


if __name__ == "__main__":
    test_structured_configuration()