from serpapi import GoogleSearch
import asyncio
from app.config.settings import settings
from app.models.schemas import FlightInfo
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


async def search_flights(flight_request):
    """Fetch real-time flight details from Google Flights using SerpAPI."""
    logger.info(f"Searching flights: {flight_request.origin} to {flight_request.destination}")

    params = {
        "api_key": settings.serpapi_api_key,
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": flight_request.origin.strip().upper(),
        "arrival_id": flight_request.destination.strip().upper(),
        "outbound_date": flight_request.outbound_date,
        "return_date": flight_request.return_date,
        "currency": "USD"
    }

    try:
        search_results = await asyncio.to_thread(lambda: GoogleSearch(params).get_dict())

        if "error" in search_results:
            logger.error(f"Flight search error: {search_results['error']}")
            return {"error": search_results["error"]}

        best_flights = search_results.get("best_flights", [])
        if not best_flights:
            logger.warning("No flights found in search results")
            return []

        formatted_flights = []
        for flight in best_flights:
            if not flight.get("flights") or len(flight["flights"]) == 0:
                continue

            first_leg = flight["flights"][0]
            formatted_flights.append(FlightInfo(
                airline=first_leg.get("airline", "Unknown Airline"),
                price=str(flight.get("price", "N/A")),
                duration=f"{flight.get('total_duration', 'N/A')} min",
                stops="Nonstop" if len(flight["flights"]) == 1 else f"{len(flight['flights']) - 1} stop(s)",
                departure=f"{first_leg.get('departure_airport', {}).get('name', 'Unknown')} ({first_leg.get('departure_airport', {}).get('id', '???')}) at {first_leg.get('departure_airport', {}).get('time', 'N/A')}",
                arrival=f"{first_leg.get('arrival_airport', {}).get('name', 'Unknown')} ({first_leg.get('arrival_airport', {}).get('id', '???')}) at {first_leg.get('arrival_airport', {}).get('time', 'N/A')}",
                travel_class=first_leg.get("travel_class", "Economy"),
                return_date=flight_request.return_date,
                airline_logo=first_leg.get("airline_logo", "")
            ))

        logger.info(f"Found {len(formatted_flights)} flights")
        return formatted_flights
    except Exception as e:
        logger.exception(f"Flight search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Flight search error: {str(e)}")