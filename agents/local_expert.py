import os

from crewai import Agent, LLM
from dotenv import load_dotenv
from tools.search_tool import travel_web_search

# Load environment variables from .env
load_dotenv()


def create_local_expert():
    """
    Creates and returns the Local Expert AI Agent.
    """

    # Retrieve Gemini configuration
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL")

    # Validate configuration
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing from the .env file."
        )

    if not model_name:
        raise ValueError(
            "GEMINI_MODEL is missing from the .env file."
        )

    # Initialize Gemini LLM
    llm = LLM(
        model=model_name,
        api_key=api_key,
        temperature=0.7
    )

    # Create the Local Expert Agent
    local_expert = Agent(
        role="Local Travel Expert",

        goal=(
            "Research travel destinations using web search "
            "and recommend popular attractions, hidden gems, "
            "local food, and practical travel information "
            "based on traveler preferences and budget."
        ),

        backstory=(
            "You are an experienced travel researcher who "
            "specializes in discovering tourist attractions, "
            "hidden gems, historical landmarks, and local cuisine. "
            "You use web search to research destinations and "
            "verify important travel information. "
            "Prioritize reliable sources, accurate information, "
            "and budget-conscious recommendations. "
            "Clearly identify information that could not "
            "be verified."
        ),

        llm=llm,

        tools=[travel_web_search],

        verbose=True,

        allow_delegation=False,
        max_iter=8,
        max_retry_limit=2
    )

    return local_expert