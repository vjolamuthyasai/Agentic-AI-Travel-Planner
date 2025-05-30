from crewai import Task
from app.models.flight import  FlightSearchParams

def create_flight_search_task(agent, params: FlightSearchParams):
    return Task(
        description=(
            f"Find flight options from {params.origin} to {params.destination} "
            f"departing {params.departure_date} and returning {params.return_date}. "
            f"Budget: ${params.budget}. Passengers: {params.passengers}. "
            f"Preferences: {params.preferences}"
        ),
        agent=agent,
        expected_output=(
            "A markdown table with columns: Airline, Flight Number, "
            "Departure/Arrival Times, Price, Duration, Stops.\n"
            "Include 3-5 best options sorted by value (price/quality)."
        )
    )