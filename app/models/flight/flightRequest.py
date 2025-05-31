from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FlightRequest(BaseModel):
    origin: str
    destination: str
    outbound_date: str
    return_date: str

