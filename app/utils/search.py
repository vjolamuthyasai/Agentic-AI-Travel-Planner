import os
import asyncio
from serpapi import GoogleSearch

from app.models.flight import FlightInfo
from app.models.flight.flightInfo import AirportInfo, CarbonEmissions
from app.models.hotel import HotelInfo
from app.models.hotel.hotelInfo import GPSCoordinates, Rate, NearbyPlace, Transportation, ReviewBreakdown, Rating, Image
from app.utils.logger import logger



async def run_search(params):
    try:
        return await asyncio.to_thread(lambda: GoogleSearch(params).get_dict())
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise


async def search_flights(request):
    params = {
        "api_key": os.getenv("SERPER_API_KEY"),
        "engine": "google_flights",
        "departure_id": request.origin.upper(),
        "arrival_id": request.destination.upper(),
        "outbound_date": request.outbound_date,
        "return_date": request.return_date,
        "currency": "USD"
    }

    results = await run_search(params)

    formatted_flights = []
    for flight in results.get("best_flights", []):
        # Handle case where flights array might be empty
        if not flight.get("flights"):
            continue

        # Take the first flight segment (assuming it's the main one)
        segment = flight["flights"][0]

        # Transform to match FlightInfo model
        flight_data = {
            "departure_airport": AirportInfo(
                name=segment["departure_airport"].get("name"),
                id=segment["departure_airport"].get("id"),
                time=segment["departure_airport"].get("time")
            ),
            "arrival_airport": AirportInfo(
                name=segment["arrival_airport"].get("name"),
                id=segment["arrival_airport"].get("id"),
                time=segment["arrival_airport"].get("time")
            ),
            "duration": segment.get("duration"),
            "airplane": segment.get("airplane"),
            "airline": segment.get("airline"),
            "airline_logo": segment.get("airline_logo"),
            "travel_class": segment.get("travel_class"),
            "flight_number": segment.get("flight_number"),
            "legroom": segment.get("legroom"),
            "extensions": segment.get("extensions", []),
            "total_duration": flight.get("total_duration"),
            "carbon_emissions": CarbonEmissions(
                this_flight=flight.get("carbon_emissions", {}).get("this_flight"),
                typical_for_this_route=flight.get("carbon_emissions", {}).get("typical_for_this_route"),
                difference_percent=flight.get("carbon_emissions", {}).get("difference_percent")
            ) if flight.get("carbon_emissions") else None,
            "price": flight.get("price"),
            "type": flight.get("type"),
            "departure_token": flight.get("departure_token")
        }

        formatted_flights.append(FlightInfo(**flight_data))

    return formatted_flights


async def search_hotels(request):
    params = {
        "api_key": os.getenv("SERPER_API_KEY"),
        "engine": "google_hotels",
        "q": request.location,
        "check_in_date": request.check_in_date,
        "check_out_date": request.check_out_date
    }

    results = await run_search(params)

    formatted_hotels = []
    for hotel in results.get("properties", []):
        # Transform to match HotelInfo model
        hotel_data = {
            "type": hotel.get("type"),
            "name": hotel.get("name"),
            "description": hotel.get("description"),
            "link": hotel.get("link"),
            "property_token": hotel.get("property_token"),
            "serpapi_property_details_link": hotel.get("serpapi_property_details_link"),
            "gps_coordinates": GPSCoordinates(
                latitude=hotel.get("gps_coordinates", {}).get("latitude"),
                longitude=hotel.get("gps_coordinates", {}).get("longitude")
            ) if hotel.get("gps_coordinates") else None,
            "check_in_time": hotel.get("check_in_time"),
            "check_out_time": hotel.get("check_out_time"),
            "rate_per_night": Rate(
                lowest=hotel.get("rate_per_night", {}).get("lowest"),
                extracted_lowest=hotel.get("rate_per_night", {}).get("extracted_lowest"),
                before_taxes_fees=hotel.get("rate_per_night", {}).get("before_taxes_fees"),
                extracted_before_taxes_fees=hotel.get("rate_per_night", {}).get("extracted_before_taxes_fees")
            ) if hotel.get("rate_per_night") else None,
            "total_rate": Rate(
                lowest=hotel.get("total_rate", {}).get("lowest"),
                extracted_lowest=hotel.get("total_rate", {}).get("extracted_lowest"),
                before_taxes_fees=hotel.get("total_rate", {}).get("before_taxes_fees"),
                extracted_before_taxes_fees=hotel.get("total_rate", {}).get("extracted_before_taxes_fees")
            ) if hotel.get("total_rate") else None,
            "hotel_class": hotel.get("hotel_class"),
            "extracted_hotel_class": hotel.get("extracted_hotel_class"),
            "overall_rating": hotel.get("overall_rating"),
            "reviews": hotel.get("reviews"),
            "location_rating": hotel.get("location_rating"),
            "amenities": hotel.get("amenities", []),
            "price": hotel.get("price")
        }

        # Handle nested arrays
        if hotel.get("nearby_places"):
            hotel_data["nearby_places"] = [
                NearbyPlace(
                    name=place.get("name"),
                    transportations=[
                        Transportation(
                            type=trans.get("type"),
                            duration=trans.get("duration")
                        ) for trans in place.get("transportations", [])
                    ]
                ) for place in hotel.get("nearby_places", [])
            ]

        if hotel.get("images"):
            hotel_data["images"] = [
                Image(
                    thumbnail=img.get("thumbnail"),
                    original_image=img.get("original_image")
                ) for img in hotel.get("images", [])
            ]

        if hotel.get("ratings"):
            hotel_data["ratings"] = [
                Rating(
                    stars=rating.get("stars"),
                    count=rating.get("count")
                ) for rating in hotel.get("ratings", [])
            ]

        if hotel.get("reviews_breakdown"):
            hotel_data["reviews_breakdown"] = [
                ReviewBreakdown(
                    name=rb.get("name"),
                    description=rb.get("description"),
                    total_mentioned=rb.get("total_mentioned"),
                    positive=rb.get("positive"),
                    negative=rb.get("negative"),
                    neutral=rb.get("neutral")
                ) for rb in hotel.get("reviews_breakdown", [])
            ]

        formatted_hotels.append(HotelInfo(**hotel_data))

    return formatted_hotels


def format_travel_data(data_type, data):
    if data_type == "flights":
        return "\n".join([f"Flight {i + 1}: {f.airline} ({f.price})" for i, f in enumerate(data)])
    else:
        return "\n".join([f"Hotel {i + 1}: {h.name} ({h.price})" for i, h in enumerate(data)])