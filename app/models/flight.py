from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class FlightSearchParams(BaseModel):
    origin: str
    destination: str
    departure_date: date
    return_date: date
    budget: float
    passengers: int = 1
    preferences: Optional[List[str]] = None


class FlightOption(BaseModel):
    airline: str
    flight_number: str
    departure_time: str
    arrival_time: str
    price: float
    duration: str
    stops: int