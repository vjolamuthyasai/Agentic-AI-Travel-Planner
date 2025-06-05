from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Travel Planning API", version="1.2.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    from app.routes import travel
    app.include_router(travel.router, prefix="/api/v1", tags=["travel"])
    print("✅ Routes imported successfully")
except ImportError as e:
    print(f"❌ Route import failed: {e}")

if __name__ == "__main__":
    import uvicorn
    print("⏳ Starting server...")
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        print(f"❌ Server failed to start: {e}")