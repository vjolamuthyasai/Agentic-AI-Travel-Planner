import os
import uvicorn
import logging
from app.main import create_app


GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "gemini_api_key_here")
SERP_API_KEY = os.getenv("SERPER_API_KEY", "serpapi_key_here")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    logger.info("Starting FastAPI application...")
    uvicorn.run("app.main:app", host="127.0.0.1",port=8000, reload=True)

