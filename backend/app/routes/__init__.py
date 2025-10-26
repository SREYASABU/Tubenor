from fastapi import FastAPI

from . import analytics

from .agents.controller import router as agent_router
def register_routes(app: FastAPI):
    # app.include_router(auth.router)
    app.include_router(analytics.router)
    app.include_router(agent_router)