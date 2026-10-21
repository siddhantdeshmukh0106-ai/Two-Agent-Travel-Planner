from crewai import Crew, Task, Process
from agents.itinerary_creator import create_itinerary_creator

# Initialize Agent 2
agent = create_itinerary_creator()

# Create a routing-specific task
routing_task = Task(
    description="""
    Calculate the driving routes for the following journeys
    in Jaipur, Rajasthan, India:

    Route 1:
    Amber Fort → Hawa Mahal

    Route 2:
    Hawa Mahal → City Palace

    Route 3:
    City Palace → Garh Ganesh Temple

    IMPORTANT:
    - Use the Travel Route Calculator for every route.
    - Report road distance in kilometers.
    - Report estimated driving time in minutes.
    - Do not invent distances or travel times.
    - Clearly report any routing failures.
    """,

    expected_output="""
    A routing report containing:
    1. Origin
    2. Destination
    3. Road distance (km)
    4. Estimated driving time (minutes)
    5. Routing status
    """,

    agent=agent
)

# Create a single-agent test crew
crew = Crew(
    agents=[agent],
    tasks=[routing_task],
    process=Process.sequential,
    verbose=True
)

print("\nStarting Routing Integration Test...\n")

# Execute
result = crew.kickoff()

print("\n" + "=" * 60)
print("ROUTING TEST RESULTS")
print("=" * 60)
print(result.raw)

# Save results
with open("routing_test_results.txt", "w", encoding="utf-8") as file:
    file.write(result.raw)

print("\nRouting test completed successfully!")