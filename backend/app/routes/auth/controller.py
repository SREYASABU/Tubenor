from fastapi import APIRouter, HTTPException, status, Response, Cookie, Depends
from fastapi.responses import RedirectResponse
from typing import Optional
from app.utils.logger import get_controller_logger
from . import models
from .oauth_service import oauth_service

logger = get_controller_logger("auth")
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def youtube_login():
    """
    Initiate YouTube OAuth flow
    
    Returns authorization URL for user to authenticate with YouTube
    """
    try:
        logger.info("Starting OAuth flow...")
        auth_url, state = oauth_service.create_authorization_url()
        logger.info(f"OAuth flow initiated with state: {state}")
        logger.info(f"Authorization URL: {auth_url}")
        
        if not auth_url:
            raise ValueError("Authorization URL is empty")
            
        return {
            "authorization_url": auth_url,
            "state": state
        }
    except Exception as e:
        logger.error(f"Failed to initiate OAuth: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate YouTube login: {str(e)}"
        )


@router.post("/callback")
async def youtube_callback(callback_data: models.OAuthCallbackRequest, response: Response):
    """
    Handle OAuth callback from frontend (after user authorizes with Google)
    
    Exchanges authorization code for access tokens
    """
    try:
        logger.info(f"Received OAuth callback with code: {callback_data.code[:20]}...")
        
        # Exchange code for tokens
        token_info = oauth_service.exchange_code_for_tokens(callback_data.code)
        
        # Get user's YouTube channel info
        try:
            channel_info = oauth_service.get_user_channel_info(token_info['user_id'])
        except Exception as e:
            logger.warning(f"Could not fetch channel info: {str(e)}")
            channel_info = {}
        
        # Set secure HTTP-only cookie with user_id
        response.set_cookie(
            key="user_id",
            value=token_info['user_id'],
            httponly=True,
            max_age=30 * 24 * 60 * 60,  # 30 days
            samesite='lax',
            secure=False  # Set to True in production with HTTPS
        )
        
        logger.info(f"User authenticated successfully: {token_info['user_id']}")
        
        return {
            "message": "Authentication successful",
            "user_id": token_info['user_id'],
            "channel_info": channel_info,
            "token_type": "Bearer",
            "expires_in": 3600
        }
    
    except Exception as e:
        logger.error(f"OAuth callback failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to complete authentication: {str(e)}"
        )


@router.get("/me", response_model=models.UserSession)
async def get_current_user(user_id: Optional[str] = Cookie(None)):
    """
    Get current authenticated user's information
    """
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        # Check if user has valid credentials
        credentials = oauth_service.get_user_credentials(user_id)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired. Please login again."
            )
        
        # Get channel info
        try:
            channel_info = oauth_service.get_user_channel_info(user_id)
            return models.UserSession(
                user_id=user_id,
                youtube_connected=True,
                channel_id=channel_info.get('channel_id'),
                channel_name=channel_info.get('channel_name')
            )
        except Exception as e:
            logger.warning(f"Could not fetch channel info: {str(e)}")
            return models.UserSession(
                user_id=user_id,
                youtube_connected=True
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user information"
        )


@router.post("/refresh")
async def refresh_token(user_id: str = Cookie(None)):
    """
    Refresh the access token
    """
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        credentials = oauth_service.get_user_credentials(user_id)
        if not credentials or not credentials.refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No refresh token available. Please login again."
            )
        
        # Refresh the token
        token_info = oauth_service.refresh_access_token(user_id, credentials.refresh_token)
        
        logger.info(f"Token refreshed for user: {user_id}")
        
        return {
            "message": "Token refreshed successfully",
            "access_token": token_info['access_token'],
            "expires_in": 3600
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refresh token: {str(e)}"
        )


@router.post("/logout")
async def logout(response: Response, user_id: Optional[str] = Cookie(None)):
    """
    Logout user and revoke access
    """
    if user_id:
        try:
            oauth_service.revoke_access(user_id)
            logger.info(f"User logged out: {user_id}")
        except Exception as e:
            logger.warning(f"Error during logout: {str(e)}")
    
    # Clear the cookie
    response.delete_cookie(key="user_id")
    
    return {"message": "Logged out successfully"}


@router.get("/status")
async def auth_status(user_id: Optional[str] = Cookie(None)):
    """
    Check authentication status
    """
    if not user_id:
        return {
            "authenticated": False,
            "youtube_connected": False
        }
    
    credentials = oauth_service.get_user_credentials(user_id)
    if not credentials:
        return {
            "authenticated": False,
            "youtube_connected": False
        }
    
    try:
        channel_info = oauth_service.get_user_channel_info(user_id)
        return {
            "authenticated": True,
            "youtube_connected": True,
            "user_id": user_id,
            "channel_info": channel_info
        }
    except Exception:
        return {
            "authenticated": True,
            "youtube_connected": True,
            "user_id": user_id
        }
