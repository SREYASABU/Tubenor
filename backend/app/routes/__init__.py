from fastapi import FastAPI

from . import analytics, auth

def register_routes(app: FastAPI):
    app.include_router(auth.router)
    app.include_router(analytics.router)