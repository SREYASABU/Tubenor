import os
from fastapi import APIRouter, HTTPException, Query
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from typing import Dict

router = APIRouter(prefix="/auth", tags=["authentication"])

# YouTube API scopes
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

def get_oauth_flow():
    """Create OAuth flow instance."""
    client_id = os.getenv("YT_CLIENT_ID")
    client_secret = os.getenv("YT_CLIENT_SECRET")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    
    if not client_id or not client_secret or not redirect_uri:
        raise HTTPException(
            status_code=500,
            detail="OAuth credentials not configured. Set YT_CLIENT_ID, YT_CLIENT_SECRET, and GOOGLE_REDIRECT_URI."
        )
    
    client_config = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [redirect_uri]
        }
    }
    
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    
    return flow

@router.get("/login")
async def login():
    """
    Initiate OAuth flow. Returns authorization URL.
    User should visit this URL to authorize the application.
    """
    try:
        flow = get_oauth_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'  # Force consent screen to get refresh token
        )
        
        return {
            "authorization_url": authorization_url,
            "state": state,
            "instructions": "Visit the authorization_url in your browser to authorize the application."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create authorization URL: {e}")

@router.get("/callback")
async def oauth_callback(code: str = Query(...), state: str = Query(None)):
    """
    OAuth callback endpoint. Exchange authorization code for tokens.
    After user authorizes, they will be redirected here with a code.
    """
    try:
        flow = get_oauth_flow()
        
        # Exchange authorization code for tokens
        flow.fetch_token(code=code)
        
        credentials = flow.credentials
        
        return {
            "message": "Authorization successful!",
            "refresh_token": credentials.refresh_token,
            "access_token": credentials.token,
            "instructions": "Copy the refresh_token and add it to your .env file as YT_REFRESH_TOKEN"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to exchange code for tokens: {e}")

@router.get("/test")
async def test_credentials():
    """
    Test if YouTube API credentials are working.
    """
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    
    client_id = os.getenv("YT_CLIENT_ID")
    client_secret = os.getenv("YT_CLIENT_SECRET")
    refresh_token = os.getenv("YT_REFRESH_TOKEN")
    
    if not client_id or not client_secret or not refresh_token:
        raise HTTPException(
            status_code=500,
            detail="YouTube OAuth env vars missing. Set YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN."
        )
    
    try:
        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES,
        )
        
        # Refresh to get access token
        request = Request()
        creds.refresh(request)
        
        # Test API call
        youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)
        response = youtube.channels().list(part="snippet,statistics", mine=True).execute()
        
        if response.get("items"):
            channel = response["items"][0]
            return {
                "status": "success",
                "message": "YouTube API credentials are working!",
                "channel_title": channel["snippet"]["title"],
                "subscriber_count": channel["statistics"].get("subscriberCount", "hidden"),
                "view_count": channel["statistics"]["viewCount"]
            }
        else:
            return {
                "status": "error",
                "message": "No channel found for this account"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to test credentials: {e}")
