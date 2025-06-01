from pydantic import BaseModel
from datetime import date

class HotelRequest(BaseModel):
    location: str
    check_in_date: date
    check_out_date: date