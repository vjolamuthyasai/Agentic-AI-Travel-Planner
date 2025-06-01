import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "your_gemini_api_key_here")
    serpapi_api_key: str = os.getenv("SERP_API_KEY", "your_serpapi_key_here")
    model_name: str = "gemini/gemini-2.0-flash"

    class Config:
        env_file = ".env"


settings = Settings()