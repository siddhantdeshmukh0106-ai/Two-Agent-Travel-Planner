from crewai import Crew, Process

from agents.local_expert import create_local_expert
from tasks.research_task import create_research_task


# Step 1: Define sample traveler details
destination = "Jaipur, Rajasthan"
budget = 10000
travel_dates = "15-16 November 2026"
travelers = 2
preferences = "History, Photography, Local Food"


# Step 2: Create the Local Expert Agent
local_expert = create_local_expert()


# Step 3: Create the Research Task
research_task = create_research_task(
    agent=local_expert,
    destination=destination,
    budget=budget,
    travel_dates=travel_dates,
    travelers=travelers,
    preferences=preferences
)


# Step 4: Create a Crew with one agent
research_crew = Crew(
    agents=[local_expert],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)


# Step 5: Execute the Crew
print("\nStarting Local Expert Agent...\n")

result = research_crew.kickoff()


# Step 6: Display the Research Report
print("\n" + "=" * 60)
print("LOCAL EXPERT RESEARCH REPORT")
print("=" * 60)

print(result.raw)

# Save the research report to a text file
report_filename = "local_expert_report.txt"

with open(report_filename, "w", encoding="utf-8") as file:
    file.write(result.raw)

print(f"\nResearch report saved to: {report_filename}")

print("\n" + "=" * 60)
print("AGENT EXECUTION COMPLETED")
print("=" * 60)