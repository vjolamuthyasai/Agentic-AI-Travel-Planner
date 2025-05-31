from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ItineraryRequest(BaseModel):
    destination: str
    check_in_date: str
    check_out_date: str
    flights: str
    hotels: str