from crew import create_travel_crew

# Test inputs
destination = "Jaipur, Rajasthan"
budget = 10000
travel_dates = "15-16 November 2026"
travelers = 2
preferences = "History, Photography, Local Food"

# Initialize the two-agent crew
travel_crew = create_travel_crew(
    destination=destination,
    budget=budget,
    travel_dates=travel_dates,
    travelers=travelers,
    preferences=preferences
)

print("\nStarting Two-Agent Travel Planner...\n")

# Execute Agent 1, followed by Agent 2
result = travel_crew.kickoff()

# Verify Agent 1 structured output
research_output = travel_crew.tasks[0].output

if research_output and research_output.pydantic:
    print("\nAgent 1 Structured Output: SUCCESS")

    research_data = research_output.pydantic

    print("Destination:", research_data.destination)
    print("Top Attractions:", len(research_data.top_attractions))
    print("Hidden Gems:", len(research_data.hidden_gems))
    print("Local Foods:", len(research_data.local_food))

else:
    print("\nAgent 1 Structured Output: FAILED")


# Verify Agent 2 structured output
if result.pydantic:
    print("\nAgent 2 Structured Output: SUCCESS")

    itinerary_data = result.pydantic

    print("Destination:", itinerary_data.destination)
    print("Days:", len(itinerary_data.days))
    print("Travelers:", itinerary_data.travelers)
    print("Total Budget:", itinerary_data.total_budget)

    # Save structured itinerary as JSON
    with open(
        "structured_itinerary.json",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(
            itinerary_data.model_dump_json(indent=4)
        )

    print("Structured itinerary saved successfully!")

else:
    print("\nAgent 2 Structured Output: FAILED")

# Display final itinerary
print("\n" + "=" * 60)
print("FINAL TRAVEL ITINERARY")
print("=" * 60)
print(result.raw)

# Save Agent 1's research report
research_output = travel_crew.tasks[0].output

if research_output:
    with open("agent1_research_report.txt", "w", encoding="utf-8") as file:
        file.write(research_output.raw)

    print("\nAgent 1 report saved successfully.")

# Save Agent 2's final itinerary
with open("final_travel_itinerary.txt", "w", encoding="utf-8") as file:
    file.write(result.raw)

print("Final itinerary saved successfully.")
print("\nTwo-Agent Execution Completed!")
