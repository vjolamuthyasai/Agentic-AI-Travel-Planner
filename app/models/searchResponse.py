from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.models.flight.flightInfo import FlightInfo
from app.models.hotel.hotelInfo import HotelInfo


class Search(BaseModel):
    flights: List[FlightInfo] = []
    hotels: List[HotelInfo] = []
    ai_flight_recommendation: str = ""
    ai_hotel_recommendation: str = ""
    itinerary: str = ""