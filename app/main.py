from fastapi import FastAPI
from app.api.routes import router

def create_app():
    app = FastAPI(title="Agentic AI Travel Planner")
    app.include_router(router)
    return app

