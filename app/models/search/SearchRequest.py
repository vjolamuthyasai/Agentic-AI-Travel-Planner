from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class SearchRequest(BaseModel):
    origin: str
    destination: str
    outbound_date: date
    return_date: date