
from app.utils.logger import logger
from ..models.hotel import HotelRequest

from ..models.search.searchResponse import SearchResponse
from ..utils.search import search_hotels, format_travel_data


async def get_hotel_recommendations(hotel_request: HotelRequest) -> SearchResponse:
    """Search hotels and get AI recommendation.
    :rtype: SearchResponse
    """
    try:
        hotels = await search_hotels(hotel_request)

        if not hotels:
            return SearchResponse(
                hotels=[],
                ai_hotel_recommendation="No hotels found"
            )

        hotels_text = format_travel_data("hotels", hotels)
        from app.services.recommendation_service import get_ai_recommendation
        ai_recommendation = await get_ai_recommendation("hotels", hotels_text)

        return SearchResponse(
            hotels=hotels,
            ai_hotel_recommendation=ai_recommendation
        )
    except Exception as e:
        logger.error(f"Hotel service error: {str(e)}")
        raise