from fastapi import FastAPI
from app.models.schemas import (
    FlightRequest, HotelRequest, ItineraryRequest, AIResponse
)
from app.services import (
    flight_service,
    hotel_service,
    ai_service
)
from app.utils.formatters import format_travel_data
import logging

app = FastAPI(title="Travel Planning API", version="1.1.0")
logger = logging.getLogger(__name__)

@app.post("/search_flights/", response_model=AIResponse)
async def flight_search(flight_request: FlightRequest):
    flights = await flight_service.search_flights(flight_request)
    flights_text = format_travel_data("flights", flights)
    recommendation = await ai_service.get_ai_recommendation("flights", flights_text)
    return AIResponse(flights=flights, ai_flight_recommendation=recommendation)

# Other endpoints...