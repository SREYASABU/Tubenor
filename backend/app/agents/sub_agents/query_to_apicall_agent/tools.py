from typing import Any, Dict, Optional
from datetime import datetime, date, timedelta
from ....services.youtube_service import YouTubeService
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

youtube_service = YouTubeService()

def _get_youtube_clients():
    """Get authenticated YouTube Data and Analytics API clients."""
    client_id = os.getenv("YT_CLIENT_ID")
    client_secret = os.getenv("YT_CLIENT_SECRET")
    refresh_token = os.getenv("YT_REFRESH_TOKEN")
    
    if not all([client_id, client_secret, refresh_token]):
        raise Exception("YouTube OAuth credentials not configured")
    
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=[
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/yt-analytics.readonly"
        ],
    )
    
    request = Request()
    creds.refresh(request)
    
    youtube_data = build("youtube", "v3", credentials=creds, cache_discovery=False)
    youtube_analytics = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
    
    return youtube_data, youtube_analytics

def execute_dynamic_youtube_query(
    query_type: str,
    metrics: Optional[str],
    dimensions: Optional[str],
    filters: Optional[str],
    sort: Optional[str],
    start_date: Optional[str],
    end_date: Optional[str],
    max_results: Optional[int],
    **additional_params
) -> Dict[str, Any]:
    """
    Dynamically execute ANY YouTube Analytics or Data API query.
    
    This is the most flexible tool - it can handle any YouTube API query by 
    constructing the appropriate API call based on the parameters provided.
    
    Args:
        query_type: Type of query - "analytics", "search", "video_details", "channel_details", "my_videos", "playlists", "comments"
        metrics: Comma-separated metrics for analytics (e.g., "views,likes,comments,shares"). Optional, defaults to "views,likes,comments" for analytics.
        dimensions: Comma-separated dimensions for analytics (e.g., "day", "video", "country"). Optional.
        filters: Filters for analytics (e.g., "video==VIDEO_ID"). Optional.
        sort: Sort order (e.g., "-views" for descending views). Optional.
        start_date: Start date for analytics (YYYY-MM-DD). Optional, defaults to 30 days ago for analytics.
        end_date: End date for analytics (YYYY-MM-DD). Optional, defaults to today for analytics.
        max_results: Maximum results to return. Optional, defaults to 100.
        additional_params: Any other parameters specific to the query type
    
    Returns:
        Dict containing the API response
    
    Examples:
        # Get views for all videos in the last 7 days
        execute_dynamic_youtube_query(
            query_type="analytics",
            metrics="views,likes,comments",
            dimensions="video",
            start_date="2024-01-01",
            end_date="2024-01-07",
            sort="-views"
        )
        
        # Get daily views trend
        execute_dynamic_youtube_query(
            query_type="analytics",
            metrics="views,estimatedMinutesWatched",
            dimensions="day",
            start_date="2024-01-01",
            end_date="2024-01-31"
        )
        
        # Search for videos
        execute_dynamic_youtube_query(
            query_type="search",
            q="Python tutorial",
            max_results=10
        )
        
        # Get my most recent videos
        execute_dynamic_youtube_query(
            query_type="my_videos",
            max_results=5,
            order="date"
        )
    """
    try:
        youtube_data, youtube_analytics = _get_youtube_clients()
        
        # Handle default values (Google AI doesn't support defaults in function signatures)
        if max_results is None:
            max_results = 100
        
        if query_type == "analytics":
            # YouTube Analytics API query
            if not start_date:
                start_date = (date.today() - timedelta(days=30)).isoformat()
            if not end_date:
                end_date = date.today().isoformat()
            
            if not metrics:
                metrics = "views,likes,comments"
            
            query_params = {
                "ids": "channel==MINE",
                "startDate": start_date,
                "endDate": end_date,
                "metrics": metrics,
                "maxResults": max_results
            }
            
            if dimensions:
                query_params["dimensions"] = dimensions
            if filters:
                query_params["filters"] = filters
            if sort:
                query_params["sort"] = sort
            
            response = youtube_analytics.reports().query(**query_params).execute()
            return response
            
        elif query_type == "search":
            # Search for videos/channels/playlists
            search_params = {
                "part": "snippet",
                "maxResults": max_results,
                "type": additional_params.get("type", "video")
            }
            
            if "q" in additional_params:
                search_params["q"] = additional_params["q"]
            if "order" in additional_params:
                search_params["order"] = additional_params["order"]
            if "relevance_language" in additional_params:
                search_params["relevanceLanguage"] = additional_params["relevance_language"]
            if "region_code" in additional_params:
                search_params["regionCode"] = additional_params["region_code"]
                
            response = youtube_data.search().list(**search_params).execute()
            return response
            
        elif query_type == "video_details":
            # Get detailed video information
            video_id = additional_params.get("video_id")
            if not video_id:
                return {"error": "video_id is required for video_details query"}
            
            response = youtube_data.videos().list(
                part="snippet,statistics,contentDetails,status",
                id=video_id
            ).execute()
            return response
            
        elif query_type == "my_videos":
            # Get authenticated user's videos
            search_params = {
                "part": "snippet",
                "forMine": True,
                "type": "video",
                "maxResults": max_results,
                "order": additional_params.get("order", "date")
            }
            
            response = youtube_data.search().list(**search_params).execute()
            
            # If we need statistics, make a second call to get video details
            if additional_params.get("include_statistics", True) and response.get("items"):
                video_ids = [item["id"]["videoId"] for item in response["items"]]
                videos_response = youtube_data.videos().list(
                    part="snippet,statistics,contentDetails",
                    id=",".join(video_ids)
                ).execute()
                return videos_response
            
            return response
            
        elif query_type == "channel_details":
            # Get channel information
            response = youtube_data.channels().list(
                part="snippet,statistics,contentDetails,brandingSettings",
                mine=True
            ).execute()
            return response
            
        elif query_type == "playlists":
            # Get user's playlists
            response = youtube_data.playlists().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=max_results
            ).execute()
            return response
            
        elif query_type == "comments":
            # Get comments for a video
            video_id = additional_params.get("video_id")
            if not video_id:
                return {"error": "video_id is required for comments query"}
            
            response = youtube_data.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=max_results,
                order=additional_params.get("order", "relevance")
            ).execute()
            return response
            
        else:
            return {"error": f"Unsupported query_type: {query_type}"}
            
    except Exception as e:
        return {
            "error": str(e),
            "query_type": query_type,
            "parameters": {
                "metrics": metrics,
                "dimensions": dimensions,
                "filters": filters,
                "sort": sort,
                "start_date": start_date,
                "end_date": end_date,
                "additional_params": additional_params
            }
        }

def execute_youtube_api_call(api_type: str, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a YouTube API call based on the specified parameters
    
    Args:
        api_type: Type of API ('data' or 'analytics')
        endpoint: The API endpoint to call
        params: Dictionary of parameters for the API call
    
    Returns:
        Dictionary containing the API response
    
    Examples:
        # Search for videos
        execute_youtube_api_call("data", "search", {"query": "Python tutorial", "max_results": 10})
        
        # Get video details
        execute_youtube_api_call("data", "videos", {"video_id": "dQw4w9WgXcQ"})
        
        # Get channel info
        execute_youtube_api_call("data", "channels", {})
        
        # Get top videos analytics
        execute_youtube_api_call("analytics", "top_videos", {"days": 30, "limit": 10})
    """
    try:
        if api_type == "data":
            # Handle YouTube Data API calls
            if endpoint == "search":
                query = params.get("query", "")
                max_results = params.get("max_results", 10)
                return youtube_service.search_videos(query=query, max_results=max_results)
            
            elif endpoint == "videos":
                video_id = params.get("video_id")
                if not video_id:
                    return {"error": "video_id is required for videos endpoint"}
                return youtube_service.get_video_details(video_id=video_id)
            
            elif endpoint == "channels":
                # Get authenticated user's channel info
                return youtube_service.get_channel_info()
            
            elif endpoint == "playlists":
                # Get user's playlists
                max_results = params.get("max_results", 50)
                return youtube_service.get_channel_playlists(max_results=max_results)
            
            elif endpoint == "my_videos":
                # Get authenticated user's uploaded videos
                max_results = params.get("max_results", 10)
                order = params.get("order", "date")  # date, viewCount, rating, etc.
                return youtube_service.get_videos(max_results=max_results, order=order)
                
        elif api_type == "analytics":
            # Handle YouTube Analytics API calls
            if endpoint == "top_videos":
                days = params.get("days", 30)
                limit = params.get("limit", 10)
                return youtube_service.get_top_videos(days=days, limit=limit)
            
            elif endpoint == "video_analytics":
                video_id = params.get("video_id")
                days = params.get("days", 30)
                if not video_id:
                    return {"error": "video_id is required for video_analytics endpoint"}
                
                from datetime import datetime, timedelta
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
                return youtube_service.get_video_analytics(
                    video_id=video_id,
                    start_date=start_date,
                    end_date=end_date
                )
            else:
                return {"error": f"Unsupported analytics endpoint: {endpoint}"}
        else:
            return {"error": f"Unsupported API type: {api_type}"}
            
    except Exception as e:
        return {
            "error": str(e),
            "api_type": api_type,
            "endpoint": endpoint,
            "params": params
        }

