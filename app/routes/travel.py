from fastapi import APIRouter

from app.models.Itinerary import ItineraryRequest
from app.models.flight.flightRequest import FlightRequest
from app.models.hotel.hotelRequest import HotelRequest
from app.models.search import SearchResponse, SearchRequest
from app.services.flight_service import get_flight_recommendations
from app.services.hotel_service import get_hotel_recommendations
from app.services.recommendation_service import complete_travel_search, generate_itinerary

router = APIRouter()


@router.post("/flights", response_model=SearchResponse)
async def search_flights_endpoint(flight_request: FlightRequest):
    return await get_flight_recommendations(flight_request)


@router.post("/hotels", response_model=SearchResponse)
async def search_hotels_endpoint(hotel_request: HotelRequest):
    return await get_hotel_recommendations(hotel_request)


@router.post("/itinerary", response_model=SearchResponse)
async def generate_itinerary_endpoint(itinerary_request: ItineraryRequest):
    return await generate_itinerary(itinerary_request)


@router.post("/search/all", response_model=SearchResponse)
async def complete_search(search_request: SearchRequest):
    return await complete_travel_search(search_request)

@router.get("/health", tags=["health"])
async def health_check():
    return {"status": "success", "message": "API is running"}