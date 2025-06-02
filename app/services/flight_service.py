import os

from app.utils.logger import logger

from ..models.flight import FlightRequest
from ..models.search.searchResponse import SearchResponse

from ..utils.search import search_flights, format_travel_data


async def get_flight_recommendations(flight_request: FlightRequest) -> SearchResponse:
    """Search flights and get AI recommendation."""
    try:

        flights = await search_flights(flight_request)

        if not flights:
            return SearchResponse(
                flights=[],
                ai_flight_recommendation="No flights found"
            )

        flights_text = format_travel_data("flights", flights)
        from app.services.recommendation_service import get_ai_recommendation
        ai_recommendation = await get_ai_recommendation("flights", flights_text)

        return SearchResponse(
            flights=flights,
            ai_flight_recommendation=ai_recommendation
        )
    except Exception as e:
        logger.error(f"Flight service error: {str(e)}")
        raise