from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class HotelRequest(BaseModel):
    location: str
    check_in_date: str
    check_out_date: str