from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, pickle

app = FastAPI()

SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly"]
CREDENTIALS_FILE = "client_secret_XXXXX.json"
TOKEN_PICKLE = "token.pickle"

def get_youtube_analytics_service():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, "wb") as token:
            pickle.dump(creds, token)
    return build("youtubeAnalytics", "v2", credentials=creds)

@app.get("/analytics")
def get_analytics():
    analytics = get_youtube_analytics_service()
    # Example: Fetch channel views by day
    response = analytics.reports().query(
        ids="channel==MINE",
        startDate="2024-01-01",
        endDate="2024-01-31",
        metrics="views,estimatedMinutesWatched,averageViewDuration",
        dimensions="day"
    ).execute()
    return JSONResponse(content=response)
