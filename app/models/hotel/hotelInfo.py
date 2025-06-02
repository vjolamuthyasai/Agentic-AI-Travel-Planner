from typing import Optional, List, Dict
from pydantic import BaseModel


class GPSCoordinates(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Rate(BaseModel):
    lowest: Optional[str] = None
    extracted_lowest: Optional[int] = None
    before_taxes_fees: Optional[str] = None
    extracted_before_taxes_fees: Optional[int] = None

class Transportation(BaseModel):
    type: Optional[str] = None
    duration: Optional[str] = None

class NearbyPlace(BaseModel):
    name: Optional[str] = None
    transportations: Optional[List[Transportation]] = []

class Image(BaseModel):
    thumbnail: Optional[str] = None
    original_image: Optional[str] = None

class Rating(BaseModel):
    stars: Optional[int] = None
    count: Optional[int] = None

class ReviewBreakdown(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    total_mentioned: Optional[int] = None
    positive: Optional[int] = None
    negative: Optional[int] = None
    neutral: Optional[int] = None

class HotelInfo(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    property_token: Optional[str] = None
    serpapi_property_details_link: Optional[str] = None
    gps_coordinates: Optional[GPSCoordinates] = None
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    rate_per_night: Optional[Rate] = None
    total_rate: Optional[Rate] = None
    nearby_places: Optional[List[NearbyPlace]] = []
    hotel_class: Optional[str] = None
    extracted_hotel_class: Optional[int] = None
    images: Optional[List[Image]] = []
    overall_rating: Optional[float] = None
    reviews: Optional[int] = None
    ratings: Optional[List[Rating]] = []
    location_rating: Optional[float] = None
    reviews_breakdown: Optional[List[ReviewBreakdown]] = []
    amenities: Optional[List[str]] = []