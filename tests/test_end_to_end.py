import json
from datetime import date

from crew import create_travel_crew
from models.schemas import DestinationResearch, TravelItinerary


def test_end_to_end():

    print("\n========== END-TO-END TEST ==========")

    destination = "Jaipur, Rajasthan"
    budget = 10000
    travel_dates = "15-16 November 2026"
    travelers = 2
    preferences = "History, Photography, Local Food"

    # Step 1: Initialize Crew
    print("\n[1/5] Initializing CrewAI...")

    crew = create_travel_crew(
        destination=destination,
        budget=budget,
        travel_dates=travel_dates,
        travelers=travelers,
        preferences=preferences
    )

    assert len(crew.agents) == 2
    assert len(crew.tasks) == 2

    print("Crew initialization: PASSED")

    # Step 2: Execute both agents
    print("\n[2/5] Executing Agent 1 and Agent 2...")

    result = crew.kickoff()

    # Step 3: Validate Agent 1 output
    print("\n[3/5] Validating Agent 1 research...")

    research_output = crew.tasks[0].output

    assert research_output is not None
    assert isinstance(
        research_output.pydantic,
        DestinationResearch
    )

    research = research_output.pydantic

    assert len(research.top_attractions) == 3
    assert len(research.hidden_gems) == 2
    assert len(research.local_food) == 3

    print("Agent 1 structured research: PASSED")

    # Step 4: Validate Agent 2 output
    print("\n[4/5] Validating Agent 2 itinerary...")

    assert isinstance(result.pydantic, TravelItinerary)

    itinerary = result.pydantic

    assert itinerary.travelers == travelers
    assert itinerary.total_budget == budget
    assert len(itinerary.days) == 2

    print("Agent 2 structured itinerary: PASSED")

    # Step 5: Save results
    print("\n[5/5] Saving test results...")

    with open(
        "end_to_end_research.json",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(research.model_dump_json(indent=4))

    with open(
        "end_to_end_itinerary.json",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(itinerary.model_dump_json(indent=4))

    print("JSON files generated successfully.")

    print("\n====================================")
    print("END-TO-END TEST PASSED!")
    print("====================================")


if __name__ == "__main__":
    test_end_to_end()