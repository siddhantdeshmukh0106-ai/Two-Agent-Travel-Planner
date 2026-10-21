import os
from dotenv import load_dotenv
from tavily import TavilyClient
from crewai.tools import tool
from functools import lru_cache


# Load environment variables
load_dotenv()

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

@lru_cache(maxsize=100)
def cached_travel_search(query: str) -> str:
    """
    Execute a Tavily search and cache its result.
    """

    response = tavily_client.search(
        query=query,
        search_depth="basic",
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return "No search results found."

    formatted_results = []

    for result in results:
        formatted_results.append(
            f"Title: {result.get('title', 'N/A')}\n"
            f"URL: {result.get('url', 'N/A')}\n"
            f"Content: {result.get('content', 'N/A')}"
        )

    return "\n\n".join(formatted_results)

@tool("Travel Web Search")
def travel_web_search(query: str) -> str:
    """
    Search the web for destination and travel information.
    """

    normalized_query = " ".join(query.strip().split())

    if not normalized_query:
        return "Error: Search query cannot be empty."

    return cached_travel_search(normalized_query)