import os
import asyncio
from serpapi import GoogleSearch

from app.models.flight import FlightInfo
from app.models.hotel import HotelInfo
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
    return [FlightInfo(**f) for f in results.get("best_flights", [])]


async def search_hotels(request):
    params = {
        "api_key": os.getenv("SERPER_API_KEY"),
        "engine": "google_hotels",
        "q": request.location,
        "check_in_date": request.check_in_date,
        "check_out_date": request.check_out_date
    }

    results = await run_search(params)
    return [HotelInfo(**h) for h in results.get("properties", [])]


def format_travel_data(data_type, data):
    if data_type == "flights":
        return "\n".join([f"Flight {i + 1}: {f.airline} ({f.price})" for i, f in enumerate(data)])
    else:
        return "\n".join([f"Hotel {i + 1}: {h.name} ({h.price})" for i, h in enumerate(data)])