from pydantic import BaseModel
from datetime import date

class SearchRequest(BaseModel):
    origin: str
    destination: str
    outbound_date: date
    return_date: date