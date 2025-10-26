from typing import Any, Dict, Optional
from ....services.youtube_service import YouTubeService

youtube_service = YouTubeService()

def execute_youtube_api_call(api_type: str, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a YouTube API call based on the specified parameters
    
    Args:
        api_type: Type of API ('data' or 'analytics')
        endpoint: The API endpoint to call
        params: Dictionary of parameters for the API call
    
    Returns:
        Dictionary containing the API response
    """
    if api_type == "data":
        # Handle YouTube Data API calls
        if endpoint == "search":
            return youtube_service.search_videos(**params)
        elif endpoint == "videos":
            return youtube_service.get_video_details(**params)
        elif endpoint == "channels":
            return youtube_service.get_channel_details(**params)
        elif endpoint == "playlists":
            return youtube_service.get_playlist_details(**params)
    elif api_type == "analytics":
        # Handle YouTube Analytics API calls
        return youtube_service.get_analytics_data(**params)
    
    raise ValueError(f"Unsupported API type or endpoint: {api_type}/{endpoint}")

