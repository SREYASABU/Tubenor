import os

from database.core import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import register_routes

app = FastAPI(
    title="tubentor",
    version="1.0.0",
    description="tubentor API",
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Register routes
register_routes(app)

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Welcome to Kimbal Logic Builder API"}


@app.get("/health")
async def health():
    return {"status": "ok"}



# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from dotenv import load_dotenv
# import os
# import pickle
# import json


# # Load environment variables
# load_dotenv()

# app = FastAPI()

# # Configuration from .env
# SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly"]
# CLIENT_CONFIG = {
#     "web": {
#         "client_id": os.getenv("GOOGLE_CLIENT_ID"),
#         "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
#         "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")],
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://oauth2.googleapis.com/token"
#     }
# }
# TOKEN_FILE = "token.pickle"
# PORT = int(os.getenv("PORT", 8081))

# def get_youtube_analytics_service():
#     creds = None
#     if os.path.exists(TOKEN_FILE):
#         with open(TOKEN_FILE, "rb") as token:
#             creds = pickle.load(token)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             # Create temp client_secrets.json from env vars
#             with open("temp_client_secrets.json", "w") as f:
#                 json.dump(CLIENT_CONFIG, f)
                
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "temp_client_secrets.json",
#                 SCOPES
#             )
#             creds = flow.run_local_server(
#                 port=PORT,
#                 redirect_uri_trailing_slash=False,
#                 open_browser=True
#             )
#             os.remove("temp_client_secrets.json")  # Clean up

#         with open(TOKEN_FILE, "wb") as token:
#             pickle.dump(creds, token)

#     return build("youtubeAnalytics", "v2", credentials=creds)

# @app.get("/analytics")
# async def get_analytics():
#     try:
#         analytics = get_youtube_analytics_service()
#         response = analytics.reports().query(
#             ids="channel==MINE",
#             startDate="2024-01-01",
#             endDate="2024-01-31",
#             metrics="views,estimatedMinutesWatched,averageViewDuration",
#             dimensions="day"
#         ).execute()
#         return JSONResponse(content=response)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
