from pydantic import BaseModel
from typing import List,Optional,Union

class AirportInfo(BaseModel):
    name: Optional[str] = None
    id: Optional[str] = None
    time: Optional[str] = None

class CarbonEmissions(BaseModel):
    this_flight: Optional[int] = None
    typical_for_this_route: Optional[int] = None
    difference_percent: Optional[int] = None

class FlightInfo(BaseModel):
    departure_airport: Optional[AirportInfo] = None
    arrival_airport: Optional[AirportInfo] = None
    duration: Optional[int] = None
    airplane: Optional[str] = None
    airline: Optional[str] = None
    airline_logo: Optional[str] = None
    travel_class: Optional[str] = None
    flight_number: Optional[str] = None
    legroom: Optional[str] = None
    extensions: Optional[List[str]] = []
    total_duration: Optional[int] = None
    carbon_emissions: Optional[CarbonEmissions] = None
    price: Optional[int] = None
    type: Optional[str] = None
    departure_token: Optional[str] = None