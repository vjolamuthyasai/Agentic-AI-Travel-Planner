from pydantic import BaseModel, Field
from typing import List,Optional,Union

from app.models.flight.flightInfo import FlightInfo
from app.models.hotel.hotelInfo import HotelInfo

class ErrorResponse(BaseModel):
    code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")

class SearchResponse(BaseModel):
    flights: List[Union[FlightInfo, dict]] = Field(default_factory=list)
    hotels: List[Union[HotelInfo, dict]] = Field(default_factory=list)
    ai_flight_recommendation: Optional[str] = None
    ai_hotel_recommendation: Optional[str] = None
    itinerary: Optional[str] = None
    error_response: Optional[ErrorResponse] = Field(
        None,
        description="Error details if the request failed"
    )