import pytest
from datetime import date, timedelta
from app.agents.flight_agent import FlightAgent
from app.models.flight import FlightSearchParams
from app.tasks.flight_task import create_flight_search_task

class TestFlightAgent:
    @pytest.fixture
    def flight_agent(self):
        return FlightAgent().create_agent()

    @pytest.fixture
    def flight_params(self):
        return FlightSearchParams(
            origin="JFK",
            destination="LAX",
            departure_date=date.today() + timedelta(days=7),
            return_date=date.today() + timedelta(days=14),
            budget=500
        )

    def test_agent_creation(self, flight_agent):
        assert flight_agent.role == "Flight Booking Expert"
        assert "flight bookings" in flight_agent.backstory

    def test_task_creation(self, flight_agent, flight_params):
        task = create_flight_search_task(flight_agent, flight_params)
        assert "JFK" in task.description
        assert "LAX" in task.description
        assert "markdown table" in task.expected_output