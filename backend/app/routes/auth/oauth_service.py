import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import secrets
import tempfile

# OAuth Configuration
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube.upload',  # Add this
    'https://www.googleapis.com/auth/youtube'  # Add this
]
REDIRECT_URI = os.getenv('OAUTH_REDIRECT_URI')

# Validate REDIRECT_URI is set
if not REDIRECT_URI:
    raise ValueError(
        "OAUTH_REDIRECT_URI environment variable is required. "
        "Please set it in your .env file (e.g., OAUTH_REDIRECT_URI=https://your-domain.com/oauth/callback)"
    )


class YouTubeOAuthService:
    """Service for handling YouTube OAuth authentication"""
    
    def __init__(self):
        self.client_config = self._get_client_config()
        self.credentials_store: Dict[str, Credentials] = {}
    
    def _get_client_config(self) -> Dict[str, Any]:
        """
        Get OAuth client configuration from environment variables or file
        """
        # Try to get from environment variables first
        client_id = os.getenv('YT_CLIENT_ID')
        client_secret = os.getenv('YT_CLIENT_SECRET')
        
        if client_id and client_secret:
            print("Using OAuth credentials from environment variables")
            return {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": [REDIRECT_URI],
                    "javascript_origins": [REDIRECT_URI.rsplit('/', 1)[0]]
                }
            }
        
        # Fallback to file-based config
        possible_paths = [
            os.getenv('GOOGLE_CLIENT_SECRETS_FILE'),
            '/app/temp_client_secrets.json',
            '/app/client_secrets.json',
            os.path.join(os.getcwd(), 'temp_client_secrets.json'),
            os.path.join(os.getcwd(), 'client_secrets.json'),
        ]
        
        for path in possible_paths:
            if path and os.path.exists(path):
                print(f"Using OAuth credentials from file: {path}")
                with open(path, 'r') as f:
                    return json.load(f)
        
        # No credentials found
        raise ValueError(
            "OAuth credentials not found. Please set YT_CLIENT_ID and YT_CLIENT_SECRET "
            "in your .env file, or provide a client_secrets.json file."
        )
    
    def create_authorization_url(self, state: Optional[str] = None) -> tuple[str, str]:
        """
        Create the authorization URL for OAuth flow
        
        Returns:
            tuple: (authorization_url, state)
        """
        if not state:
            state = secrets.token_urlsafe(32)
        
        flow = Flow.from_client_config(
            self.client_config,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state
            # No prompt parameter - Google will auto-select if user is already logged in
        )
        
        return authorization_url, state
    
    def exchange_code_for_tokens(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access and refresh tokens
        
        Args:
            code: Authorization code from OAuth callback
        
        Returns:
            dict: Token information including access_token, refresh_token, expiry
        """
        flow = Flow.from_client_config(
            self.client_config,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        
        flow.fetch_token(code=code)
        
        credentials = flow.credentials
        
        # Store credentials
        user_id = self._generate_user_id()
        self.credentials_store[user_id] = credentials
        
        return {
            'user_id': user_id,
            'access_token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_expiry': credentials.expiry.isoformat() if credentials.expiry else None,
            'scopes': credentials.scopes
        }
    
    def refresh_access_token(self, user_id: str, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh the access token using refresh token
        
        Args:
            user_id: User identifier
            refresh_token: Refresh token
        
        Returns:
            dict: New token information
        """
        from google.auth.transport.requests import Request
        
        # Get client credentials from config
        client_id = self.client_config['web']['client_id']
        client_secret = self.client_config['web']['client_secret']
        
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )
        
        # Refresh the token
        credentials.refresh(Request())
        
        # Update stored credentials
        self.credentials_store[user_id] = credentials
        
        return {
            'user_id': user_id,
            'access_token': credentials.token,
            'token_expiry': credentials.expiry.isoformat() if credentials.expiry else None
        }
    
    def get_user_credentials(self, user_id: str) -> Optional[Credentials]:
        """
        Get stored credentials for a user
        
        Args:
            user_id: User identifier
        
        Returns:
            Credentials object or None
        """
        return self.credentials_store.get(user_id)
    
    def get_user_channel_info(self, user_id: str) -> Dict[str, Any]:
        """
        Get YouTube channel information for authenticated user
        
        Args:
            user_id: User identifier
        
        Returns:
            dict: Channel information
        """
        credentials = self.get_user_credentials(user_id)
        if not credentials:
            raise ValueError("User not authenticated")
        
        youtube = build('youtube', 'v3', credentials=credentials, cache_discovery=False)
        
        request = youtube.channels().list(
            part='snippet,statistics,contentDetails',
            mine=True
        )
        response = request.execute()
        
        if not response.get('items'):
            return {}
        
        channel = response['items'][0]
        return {
            'channel_id': channel['id'],
            'channel_name': channel['snippet']['title'],
            'subscriber_count': channel['statistics'].get('subscriberCount', '0'),
            'video_count': channel['statistics'].get('videoCount', '0'),
            'view_count': channel['statistics'].get('viewCount', '0'),
            'thumbnail': channel['snippet']['thumbnails']['default']['url']
        }
    
    def revoke_access(self, user_id: str) -> bool:
        """
        Revoke access for a user
        
        Args:
            user_id: User identifier
        
        Returns:
            bool: Success status
        """
        if user_id in self.credentials_store:
            del self.credentials_store[user_id]
            return True
        return False
    
    def _generate_user_id(self) -> str:
        """Generate a unique user ID"""
        return secrets.token_urlsafe(16)
    
    def store_credentials_to_db(self, user_id: str, credentials: Credentials, db_session):
        """
        Store credentials to database
        
        Args:
            user_id: User identifier
            credentials: OAuth credentials
            db_session: Database session
        """
        # TODO: Implement database storage
        # For now, using in-memory storage
        pass


# Singleton instance
oauth_service = YouTubeOAuthService()

