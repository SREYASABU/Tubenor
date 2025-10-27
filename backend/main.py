import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import register_routes

app = FastAPI(
    title="Tubenor API",
    description="API for managing YouTube analytics and content",
    version="1.0.0"
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

register_routes(app)
@app.get("/")
async def root():
    return {"message": "Welcome to Tubenor API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


