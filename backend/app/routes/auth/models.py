from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class YouTubeCredentials(BaseModel):
    """Model for YouTube OAuth credentials"""
    user_id: str
    access_token: str
    refresh_token: str
    token_expiry: datetime
    scope: str


class OAuthCallbackRequest(BaseModel):
    """Model for OAuth callback"""
    code: str
    state: Optional[str] = None


class TokenResponse(BaseModel):
    """Model for token response"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    user_id: str


class UserSession(BaseModel):
    """Model for user session"""
    user_id: str
    youtube_connected: bool = False
    channel_id: Optional[str] = None
    channel_name: Optional[str] = None
