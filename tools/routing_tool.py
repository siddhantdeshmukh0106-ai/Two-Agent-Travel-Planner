import requests
from geopy.geocoders import Nominatim
from crewai.tools import tool

geolocator = Nominatim(
    user_agent="two_agent_travel_planner"
)


def get_coordinates(location):
    """Convert a location name into latitude and longitude."""

    try:
        result = geolocator.geocode(
            location,
            timeout=10
        )

        if result:
            return result.latitude, result.longitude

        return None

    except Exception as error:
        print(f"Geocoding Error: {error}")
        return None


@tool("Travel Route Calculator")
def calculate_route(origin: str, destination: str) -> str:
    """
    Calculate driving distance and estimated travel time
    between two locations using OpenStreetMap and OSRM.
    """

    origin_coords = get_coordinates(origin)
    destination_coords = get_coordinates(destination)

    if not origin_coords or not destination_coords:
        return "Error: Could not find coordinates for one or both locations."

    origin_lat, origin_lon = origin_coords
    dest_lat, dest_lon = destination_coords

    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{origin_lon},{origin_lat};{dest_lon},{dest_lat}"
        f"?overview=false"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()

        if data.get("code") != "Ok" or not data.get("routes"):
            return "Error: No valid driving route found."

        route = data["routes"][0]

        distance_km = round(route["distance"] / 1000, 2)
        duration_min = round(route["duration"] / 60, 1)

        return (
            f"Origin: {origin}\n"
            f"Destination: {destination}\n"
            f"Road Distance: {distance_km} km\n"
            f"Estimated Driving Time: {duration_min} minutes\n"
            f"Source: OpenStreetMap / OSRM\n"
            f"Note: Traffic delays are not included."
        )

    except Exception as error:
        return f"Routing Error: {error}"