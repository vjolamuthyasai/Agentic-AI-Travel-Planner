import asyncio
from functools import lru_cache
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

from app.models.Itinerary import ItineraryRequest
from app.models.flight import FlightRequest
from app.models.hotel import HotelRequest
from app.models.search import  SearchResponse, SearchRequest
from app.services.flight_service import get_flight_recommendations
from app.services.hotel_service import get_hotel_recommendations
from app.utils.search import format_travel_data

load_dotenv()


@lru_cache(maxsize=1)
def initialize_llm():
    return LLM(
        model="gemini/gemini-2.0-flash",
        provider="google",
        api_key=os.getenv("GOOGLE_API_KEY")
    )


async def get_ai_recommendation(data_type: str, formatted_data: str):
    llm_model = initialize_llm()

    if data_type == "flights":
        role = "AI Flight Analyst"
        goal = "Analyze flight options and recommend the best one"
    else:
        role = "AI Hotel Analyst"
        goal = "Analyze hotel options and recommend the best one"

    analyze_agent = Agent(
        role=role,
        goal=goal,
        backstory=f"Expert {data_type} analyst",
        llm=llm_model,
        verbose=True
    )

    analyze_task = Task(
        description=f"Analyze this {data_type} data:\n{formatted_data}",
        agent=analyze_agent
    )

    crew = Crew(
        agents=[analyze_agent],
        tasks=[analyze_task],
        process=Process.sequential
    )

    return await asyncio.to_thread(crew.kickoff)


async def generate_itinerary(request: ItineraryRequest) -> str:
    llm_model = initialize_llm()

    planner = Agent(
        role="Travel Planner",
        goal="Create detailed itineraries",
        backstory="Expert travel itinerary creator",
        llm=llm_model
    )

    task = Task(
        description=f"""Create itinerary for:
        Destination: {request.destination}
        Dates: {request.check_in_date} to {request.check_out_date}
        Flight Info: {request.flights}
        Hotel Info: {request.hotels}""",
        agent=planner
    )

    crew = Crew(agents=[planner], tasks=[task])
    return await asyncio.to_thread(crew.kickoff)


async def complete_travel_search(request: SearchRequest) -> SearchResponse:
    try:
        flight_request = FlightRequest(
            return_date=request.return_date,
            outbound_date=request.outbound_date,
            origin=request.origin,
            destination=request.destination
        )
        hotel_request = HotelRequest(
            location=request.destination,
            check_in_date=request.outbound_date,
            check_out_date=request.return_date
        )

        flight_task = get_flight_recommendations(flight_request)
        hotel_task = get_hotel_recommendations(hotel_request)

        flights, hotels = await asyncio.gather(flight_task, hotel_task)

        itinerary = ""
        if flights.flights and hotels.hotels:
            itinerary = await generate_itinerary(ItineraryRequest(
                destination=request.destination,
                check_in_date=request.outbound_date,
                check_out_date=request.return_date,
                flights=format_travel_data("flights", flights.flights),
                hotels=format_travel_data("hotels", hotels.hotels)
            ))

        return SearchResponse(
            flights=flights.flights,
            hotels=hotels.hotels,
            ai_flight_recommendation=flights.ai_flight_recommendation,
            ai_hotel_recommendation=hotels.ai_hotel_recommendation,
            itinerary=itinerary
        )
    except Exception as exception:
        return SearchResponse(
            flights=[],
            hotels=[],
            error_message=str(exception)
        )

