# 🌍 Two-Agent AI Travel Planner

### 🌐 Live Application

🚀 **[Try the Two-Agent AI Travel Planner](https://two-agent-travel-planner-en4nlrncawhxdpuj42ysz3.streamlit.app/)**

An AI-powered travel planning application built using CrewAI,
Google Gemini, Tavily Search, OpenStreetMap, and Streamlit.

Generate personalized travel itineraries with destination research,
day-wise activities, route planning, budget estimation, and
downloadable travel plans.

### An Intelligent Multi-Agent Travel Planning Application Using CrewAI and Google Gemini

A Python-based AI travel planning application that uses two collaborative AI agents to research travel destinations and generate personalized, budget-aware, day-wise itineraries.

Built using **CrewAI, Google Gemini, Tavily Search, OpenStreetMap, OSRM, Pydantic, and Streamlit**.

---

## 📌 Project Overview

Planning a trip involves researching attractions, estimating expenses, identifying suitable routes, and organizing activities into a practical schedule.

The **Two-Agent AI Travel Planner** simplifies this process through a multi-agent AI architecture.

The system consists of two specialized agents:

**Agent 1 — Local Travel Expert**
- Researches destinations using Tavily Search.
- Identifies popular tourist attractions.
- Discovers lesser-known places.
- Recommends local food.
- Collects available travel information and source references.

**Agent 2 — Itinerary Creator**
- Receives structured research from Agent 1.
- Generates personalized day-wise itineraries.
- Uses routing tools to estimate travel distances and durations.
- Calculates estimated travel expenses.
- Evaluates the itinerary against the user's budget.

The results are displayed through an interactive Streamlit dashboard.

---

## ✨ Key Features

- 🤖 **Two-Agent AI Architecture:** Specialized agents collaborate using CrewAI.
- 🌐 **Web-Based Destination Research:** Retrieves travel information through Tavily.
- 🗺️ **Route Estimation:** Uses OpenStreetMap geocoding and OSRM routing.
- 📅 **Day-Wise Itinerary Generation:** Organizes attractions, meals, and activities.
- 💰 **Budget-Aware Planning:** Calculates estimated expenses and remaining budget.
- 🎯 **Personalized Recommendations:** Considers travel preferences and group size.
- ✅ **Structured AI Outputs:** Uses Pydantic for data validation.
- 🖥️ **Interactive Dashboard:** Built with Streamlit.
- 📥 **Downloadable Results:** Supports Markdown and JSON exports.
- 🛡️ **Error Handling:** Validates inputs and handles common API failures.
- ⚡ **Performance Monitoring:** Displays AI workflow execution time.

---

## 🏗️ System Architecture

```text
                  USER
                   |
                   v
          STREAMLIT INTERFACE
                   |
                   v
           INPUT VALIDATION
                   |
                   v
          CREWAI ORCHESTRATOR
                   |
                   v
       +-----------------------+
       | AGENT 1              |
       | Local Travel Expert   |
       +-----------------------+
                   |
                   v
             TAVILY SEARCH
                   |
                   v
         DESTINATION RESEARCH
           (Pydantic Model)
                   |
                   v
       +-----------------------+
       | AGENT 2              |
       | Itinerary Creator     |
       +-----------------------+
                   |
          +--------+--------+
          |                 |
          v                 v
     OSRM ROUTING      BUDGET TOOL
          |                 |
          +--------+--------+
                   |
                   v
          STRUCTURED ITINERARY
            (Pydantic Model)
                   |
                   v
          STREAMLIT DASHBOARD
                   |
                   v
           MARKDOWN / JSON
                EXPORT
```

CrewAI executes the agents sequentially, allowing the itinerary creator to use the destination research produced by the local expert.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Application development |
| CrewAI | Multi-agent orchestration |
| Google Gemini | Large language model |
| Tavily API | Web-based destination research |
| OpenStreetMap / Nominatim | Location geocoding |
| OSRM | Driving route estimation |
| Pydantic | Structured output validation |
| Streamlit | Interactive web interface |
| python-dotenv | Environment variable management |
| Requests | HTTP requests |

---
## 🏗️ System Architecture

The Two-Agent AI Travel Planner uses a sequential multi-agent
architecture powered by CrewAI.

Two specialized AI agents collaborate to research travel destinations
and generate personalized itineraries based on user preferences.

### Architecture Diagram

```text
                  ┌─────────────────────────┐
                  │         USER            │
                  │ Destination, Budget,    │
                  │ Dates, Travelers,       │
                  │ Preferences             │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │    STREAMLIT WEB APP    │
                  │         app.py          │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │    INPUT VALIDATION     │
                  │   utils/validators.py   │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │    CREWAI ORCHESTRATOR  │
                  │         crew.py         │
                  └────────────┬────────────┘
                               │
                               ▼
             ┌───────────────────────────────┐
             │       AGENT 1                 │
             │       LOCAL EXPERT            │
             │                               │
             │ • Destination Research        │
             │ • Tourist Attractions         │
             │ • Local Food                  │
             │ • Travel Recommendations      │
             │                               │
             │ Tool: Tavily Web Search       │
             └───────────────┬───────────────┘
                             │
                             ▼
             ┌───────────────────────────────┐
             │     STRUCTURED RESEARCH       │
             │     DestinationResearch       │
             │     (Pydantic Schema)         │
             └───────────────┬───────────────┘
                             │
                             ▼
             ┌───────────────────────────────┐
             │       AGENT 2                 │
             │       ITINERARY CREATOR       │
             │                               │
             │ • Day-wise Travel Planning    │
             │ • Activity Scheduling         │
             │ • Route Estimation            │
             │ • Budget Allocation           │
             │                               │
             │ Tools: OSRM, Budget Calculator│
             └───────────────┬───────────────┘
                             │
                             ▼
             ┌───────────────────────────────┐
             │     STRUCTURED ITINERARY      │
             │       TravelItinerary         │
             │      (Pydantic Schema)        │
             └───────────────┬───────────────┘
                             │
                             ▼
             ┌───────────────────────────────┐
             │       FINAL OUTPUT            │
             │                               │
             │ • Day-wise Itinerary          │
             │ • Budget Breakdown            │
             │ • Destination Research        │
             │ • JSON / Markdown Downloads   │
             └───────────────────────────────┘
```

### AI Agent Responsibilities

**Agent 1 — Local Expert**

The Local Expert Agent researches the selected destination using
Tavily Search and Google Gemini.

Its responsibilities include:

- Discovering tourist attractions and landmarks.
- Researching local cuisine and food recommendations.
- Identifying useful destination information.
- Producing structured research using the `DestinationResearch` schema.

**Agent 2 — Itinerary Creator**

The Itinerary Creator Agent receives the research generated by Agent 1
and converts it into a personalized travel itinerary.

Its responsibilities include:

- Creating a day-wise activity schedule.
- Organizing attractions into a practical travel plan.
- Estimating travel distances and durations using OSRM.
- Allocating expenses according to the user's budget.
- Producing structured output using the `TravelItinerary` schema.

### Agent Collaboration

The agents execute sequentially through CrewAI.

1. The user submits travel preferences through Streamlit.
2. The application validates the input.
3. CrewAI executes the Local Expert Agent.
4. The Local Expert produces destination research.
5. CrewAI passes the research to the Itinerary Creator Agent.
6. The Itinerary Creator generates the travel itinerary.
7. Pydantic validates the structured outputs.
8. Streamlit displays the results and provides download options.

### External Tools and APIs

| Tool / API | Purpose |
|---|---|
| Google Gemini | Language model powering both agents |
| Tavily Search | Destination research and travel information |
| OpenStreetMap Nominatim | Converts location names into coordinates |
| OSRM | Estimates driving distances and travel durations |
| Budget Calculator | Estimates and validates travel expenses |
| Pydantic | Validates structured agent outputs |
| Streamlit | Displays the generated travel plan |

### Error Handling

The application includes centralized error handling to manage
unexpected failures during input validation, API calls, and
agent execution.

Errors are logged for debugging, while the user interface
displays readable error messages.

## 📂 Project Structure

```text
Two-Agent-Travel-Planner/
|
|-- agents/
|   |-- local_expert.py
|   |-- itinerary_creator.py
|
|-- tasks/
|   |-- research_task.py
|   |-- itinerary_task.py
|
|-- tools/
|   |-- search_tool.py
|   |-- routing_tool.py
|   |-- budget_tool.py
|
|-- models/
|   |-- schemas.py
|
|-- utils/
|   |-- validators.py
|   |-- error_handler.py
|
|-- tests/
|
|-- .streamlit/
|   |-- config.toml
|
|-- app.py
|-- crew.py
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- README.md
```

---

## ⚙️ Installation and Setup

### Prerequisites

Before running the application, ensure you have:

- Python 3.11
- Git
- An active internet connection
- Google Gemini API key
- Tavily API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Two-Agent-Travel-Planner.git
cd Two-Agent-Travel-Planner
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure API Keys

Create a `.env` file in the project root.

Use `.env.example` as a reference.

```env
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=gemini/gemini-3.5-flash-lite

TAVILY_API_KEY=your_actual_tavily_api_key

APP_NAME=Two-Agent AI Travel Planner
```

Never commit your `.env` file or expose API keys publicly.

### Step 5: Run the Application

```bash
streamlit run app.py
```

Open the local address displayed in the terminal, typically:

`http://localhost:8501`

---

## 🚀 How to Use

1. Enter your travel destination.
2. Select your travel start and end dates.
3. Specify your total budget in INR.
4. Select the number of travelers.
5. Choose your travel preferences.
6. Click **Generate Travel Plan**.
7. Wait for the AI agents to complete their tasks.
8. Explore the itinerary, budget breakdown, and destination research.
9. Download the generated results in Markdown or JSON format.

---

## 🧠 Multi-Agent Workflow

### Agent 1: Local Travel Expert

The first agent researches the selected destination.

Its structured output includes:

- Three popular attractions.
- Two hidden gems.
- Three local food recommendations.
- Available entry fees and opening hours.
- Estimated visit durations.
- Travel tips and source references.

Research results are validated using the `DestinationResearch` Pydantic model.

### Agent 2: Itinerary Creator

The second agent receives Agent 1's research and generates a travel schedule.

Its responsibilities include:

- Organizing activities by day.
- Assigning approximate activity times.
- Estimating travel distances and durations.
- Calculating expenses.
- Evaluating budget feasibility.
- Recording assumptions and uncertain information.

The itinerary is validated using the `TravelItinerary` Pydantic model.

---

## 💰 Budget Management

The application estimates expenses across five categories:

| Category | Description |
|---|---|
| Attractions | Entry tickets and sightseeing |
| Food | Meals and local food |
| Transport | Estimated local transportation |
| Accommodation | Estimated lodging |
| Other | Miscellaneous expenses |

The budget validator checks expense totals and remaining budget.

When costs are missing or provisional, the application can identify the result as a **PARTIAL ESTIMATE**.

**Note:** Estimated costs are not guaranteed prices. Users should verify actual rates before booking.

---

## 🗺️ Routing Integration

The routing component uses:

- **Nominatim:** Converts location names into geographic coordinates.
- **OSRM:** Calculates approximate driving distances and durations.

Route estimates do not account for real-time traffic, temporary road closures, or all transportation modes.

---

## 🧪 Testing

The project includes tests for:

- CrewAI configuration.
- Pydantic structured outputs.
- Routing calculations.
- Budget validation.
- Invalid user inputs.
- Error handling.
- End-to-end agent execution.

Example commands:

```bash
python test_pydantic.py
python test_budget.py
python test_error_handling.py
```

If the test files are organized under `tests/`, use their corresponding paths.

Some integration tests require working API credentials and internet access.

---

## ⚠️ Limitations

- Generated itineraries depend on the accuracy of retrieved information.
- Ticket prices and opening hours may change.
- Route estimates do not include live traffic conditions.
- Budget estimates may be incomplete or approximate.
- API availability and rate limits can affect generation time.
- AI-generated recommendations should be verified before making reservations.

---

## 🔮 Future Enhancements

- Integration with live hotel and transportation booking services.
- Interactive maps displaying complete travel routes.
- Real-time weather information and travel alerts.
- Multi-city itinerary planning.
- Support for additional currencies and languages.
- User accounts and saved travel plans.
- Collaborative itinerary editing.

---

## 🎓 Academic Project

**Project Title:** Two-Agent AI Travel Planner

**Domain:** Artificial Intelligence / Multi-Agent Systems / Travel Technology

**Project Type:** Academic Mini-Project

The project demonstrates the integration of LLM-powered agents, external APIs, structured data validation, and an interactive web application.

---

## 📄 License

This project is currently intended for academic and educational purposes.

A formal open-source license may be added before public distribution.

---

## ⭐ Acknowledgment

Developed using open-source Python technologies and publicly available APIs.

The application uses Google Gemini for language generation, CrewAI for agent orchestration, Tavily for web research, and OpenStreetMap-based services for geographic information.

