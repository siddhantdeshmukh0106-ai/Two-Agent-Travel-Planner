from crewai import Crew, Process

from agents.local_expert import create_local_expert
from agents.itinerary_creator import create_itinerary_creator

from tasks.research_task import create_research_task
from tasks.itinerary_task import create_itinerary_task


def create_travel_crew(
    destination,
    budget,
    travel_dates,
    travelers,
    preferences
):
    """Create the two-agent travel planning crew."""

    # Step 1: Initialize both agents
    local_expert = create_local_expert()
    itinerary_creator = create_itinerary_creator()

    # Step 2: Create Agent 1's research task
    research_task = create_research_task(
        agent=local_expert,
        destination=destination,
        budget=budget,
        travel_dates=travel_dates,
        travelers=travelers,
        preferences=preferences
    )

    # Step 3: Create Agent 2's itinerary task
    itinerary_task = create_itinerary_task(
        agent=itinerary_creator,
        destination=destination,
        budget=budget,
        travel_dates=travel_dates,
        travelers=travelers,
        preferences=preferences
    )

    # Step 4: Pass Agent 1's output to Agent 2
    itinerary_task.context = [research_task]

    # Step 5: Create the sequential crew
    travel_crew = Crew(
        agents=[local_expert, itinerary_creator],
        tasks=[research_task, itinerary_task],
        process=Process.sequential,
        verbose=True
    )

    return travel_crew