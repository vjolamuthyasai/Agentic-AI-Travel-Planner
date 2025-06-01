from pydantic import BaseModel

class HotelInfo(BaseModel):
    name: str
    price: str
    rating: float
    location: str
    link: str