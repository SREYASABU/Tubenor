import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastapi import HTTPException

# YouTube API scopes
YT_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YTA_SCOPE = "https://www.googleapis.com/auth/yt-analytics.readonly"
YT_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YT_MANAGE_SCOPE = "https://www.googleapis.com/auth/youtube"

def _load_credentials(scopes: List[str] = None) -> Credentials:
    """Load OAuth credentials from environment variables."""
    if scopes is None:
        scopes = [YT_SCOPE, YTA_SCOPE]

    client_id = os.getenv("YT_CLIENT_ID")
    client_secret = os.getenv("YT_CLIENT_SECRET")
    refresh_token = os.getenv("YT_REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        raise HTTPException(
            status_code=500,
            detail="YouTube OAuth env vars missing. Set YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN."
        )

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
    )

    # Ensure we have a valid access token
    request = Request()
    try:
        creds.refresh(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh YouTube token: {e}")

    return creds

def _build_youtube_service(creds: Credentials):
    """Build YouTube Data API service."""
    return build("youtube", "v3", credentials=creds, cache_discovery=False)

def _build_analytics_service(creds: Credentials):
    """Build YouTube Analytics API service."""
    return build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)

class YouTubeService:
    """Service class for YouTube API operations."""

    def __init__(self, scopes: List[str] = None):
        self.creds = _load_credentials(scopes)
        self.youtube = _build_youtube_service(self.creds)
        self.analytics = _build_analytics_service(self.creds) if YTA_SCOPE in (scopes or []) else None

    def get_channel_info(self) -> Dict[str, Any]:
        """Get channel information and statistics."""
        try:
            response = self.youtube.channels().list(
                part="snippet,statistics,contentDetails,brandingSettings",
                mine=True
            ).execute()
            return response
        except HttpError as e:
            raise HTTPException(status_code=502, detail=f"YouTube API error: {e}")

    def get_videos(self, max_results: int = 50, order: str = "date") -> Dict[str, Any]:
        """Get user's uploaded videos."""
        try:
            response = self.youtube.search().list(
                part="snippet",
                forMine=True,
                type="video",
                order=order,
                maxResults=max_results
            ).execute()
            return response
        except HttpError as e:
            raise HTTPException(status_code=502, detail=f"YouTube API error: {e}")

    def get_video_analytics(self, video_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get analytics for a specific video."""
        if not self.analytics:
            raise HTTPException(status_code=500, detail="Analytics API not available")

        try:
            response = self.analytics.reports().query(
                ids=f"channel==MINE",
                startDate=start_date.strftime("%Y-%m-%d"),
                endDate=end_date.strftime("%Y-%m-%d"),
                metrics="views,likes,comments,shares,averageViewDuration",
                dimensions="video",
                filters=f"video=={video_id}",
                maxResults=1000
            ).execute()
            return response
        except HttpError as e:
            raise HTTPException(status_code=502, detail=f"YouTube Analytics API error: {e}")

    def get_top_videos(self, days: int = 30, limit: int = 10) -> Dict[str, Any]:
        """Get top performing videos in the last N days."""
        if not self.analytics:
            raise HTTPException(status_code=500, detail="Analytics API not available")

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        try:
            response = self.analytics.reports().query(
                ids="channel==MINE",
                startDate=start_date.strftime("%Y-%m-%d"),
                endDate=end_date.strftime("%Y-%m-%d"),
                metrics="views,likes,comments,shares,averageViewDuration",
                dimensions="video",
                sort="-views",
                maxResults=limit
            ).execute()
            return response
        except HttpError as e:
            raise HTTPException(status_code=502, detail=f"YouTube Analytics API error: {e}")

    def get_playlist_videos(self, playlist_id: str, max_results: int = 50) -> Dict[str, Any]:
        """Get videos from a specific playlist."""
        try:
            response = self.youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=max_results
            ).execute()
            return response
        except HttpError as e:
            raise HTTPException(status_code=502, detail=f"YouTube API error: {e}")

    def get_channel_playlists(self, max_results: int = 50) -> Dict[str, Any]:
        """Get user's playlists."""
        try:
            response = self.youtube.playlists().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=max_results
            ).execute()
            return response
        except HttpError as e:
            raise HTTPException(status_code=502, detail=f"YouTube API error: {e}")

    def get_subscriber_count(self) -> int:
        """Get current subscriber count."""
        channel_info = self.get_channel_info()
        return int(channel_info["items"][0]["statistics"]["subscriberCount"])

    def get_total_views(self) -> int:
        """Get total channel views."""
        channel_info = self.get_channel_info()
        return int(channel_info["items"][0]["statistics"]["viewCount"])

    def search_videos(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search for videos on YouTube."""
        try:
            response = self.youtube.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=max_results
            ).execute()
            return response
        except HttpError as e:
            raise HTTPException(status_code=502, detail=f"YouTube API error: {e}")

    def get_video_details(self, video_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific video."""
        try:
            response = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            ).execute()
            return response
        except HttpError as e:
            raise HTTPException(status_code=502, detail=f"YouTube API error: {e}")

    def get_comments(self, video_id: str, max_results: int = 100) -> Dict[str, Any]:
        """Get comments for a specific video."""
        try:
            response = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results,
                order="relevance"
            ).execute()
            return response
        except HttpError as e:
            raise HTTPException(status_code=502, detail=f"YouTube API error: {e}")

# Convenience functions for direct use
def get_youtube_service(scopes: List[str] = None) -> YouTubeService:
    """Get a YouTube service instance."""
    return YouTubeService(scopes)

def get_channel_info() -> Dict[str, Any]:
    """Get channel information."""
    service = YouTubeService()
    return service.get_channel_info()

def get_videos(max_results: int = 50) -> Dict[str, Any]:
    """Get user's videos."""
    service = YouTubeService()
    return service.get_videos(max_results)

def get_top_videos(days: int = 30, limit: int = 10) -> Dict[str, Any]:
    """Get top performing videos."""
    service = YouTubeService([YT_SCOPE, YTA_SCOPE])
    return service.get_top_videos(days, limit)