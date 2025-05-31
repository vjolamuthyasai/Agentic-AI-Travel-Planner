from crewai import Agent, Task, Crew, Process
from functools import lru_cache
from app.config.settings import settings
import asyncio
import logging

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def initialize_llm():
    """Initialize and cache the LLM instance"""
    from crewai import LLM
    return LLM(
        model=settings.model_name,
        provider="google",
        api_key=settings.google_api_key
    )


async def get_ai_recommendation(data_type, formatted_data):
    """Get AI recommendation for flights or hotels"""
    logger.info(f"Getting {data_type} analysis from AI")
    llm_model = initialize_llm()

    # Agent configuration remains the same as your original code
    # ...