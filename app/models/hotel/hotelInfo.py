from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class HotelInfo(BaseModel):
    name: str
    price: str
    rating: float
    location: str
    link: str