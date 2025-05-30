from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import config

class FlightAgent:
    def create_agent(self):
        return Agent(
            role="Flight Booking Expert",
            goal="Find optimal flight options based on requirements",
            backstory=(
                "An experienced travel agent specializing in flight bookings with "
                "access to real-time flight data and pricing information."
            ),
            verbose=True,
            llm=ChatGoogleGenerativeAI(
                model="gemini-pro",
                temperature=0.5,
                google_api_key=config.GOOGLE_API_KEY
            ),
            memory=True
        )