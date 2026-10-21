import logging

from pydantic import ValidationError


logging.basicConfig(
    filename="travel_planner_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def handle_application_error(error):
    """
    Convert application errors into user-friendly messages.
    """

    logging.error(
        "Travel Planner Error: %s",
        str(error),
        exc_info=True
    )

    error_message = str(error).lower()

    if isinstance(error, ValidationError):
        return (
            "The generated travel itinerary contains invalid data. "
            "Please try generating it again."
        )

    if isinstance(error, ValueError):
        return str(error)

    if "429" in error_message or "rate limit" in error_message:
        return (
            "The AI service is temporarily busy or has reached its "
            "usage limit. Please try again later."
        )

    if "503" in error_message or "unavailable" in error_message:
        return (
            "The AI service is temporarily unavailable. "
            "Please try again shortly."
        )

    if "timeout" in error_message or "timed out" in error_message:
        return (
            "The request took too long to complete. "
            "Please try again."
        )

    if "401" in error_message or "invalid api key" in error_message:
        return (
            "API authentication failed. "
            "Please check the configured API credentials."
        )

    return (
        "An unexpected error occurred while generating your itinerary. "
        "Please try again."
    )