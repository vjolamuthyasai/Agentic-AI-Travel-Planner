from datetime import date
from pydantic import BaseModel


class HotelRequest(BaseModel):
    location: str
    check_in_date: date
    check_out_date: date