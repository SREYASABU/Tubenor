import os
from datetime import date, timedelta
from typing import Dict, Optional

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from fastapi import HTTPException, APIRouter, Query

router = APIRouter(prefix="/analytics", tags=["analytics"])

YTA_SCOPE = "https://www.googleapis.com/auth/yt-analytics.readonly"
YT_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"

def _load_credentials() -> Credentials:
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
        scopes=[YTA_SCOPE, YT_SCOPE],
    )

    # Ensure we have a valid access token
    request = Request()
    try:
        creds.refresh(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh YouTube token: {e}")

    return creds

def _build_services(creds: Credentials):
    yta = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
    yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
    return yta, yt

def query_yt_analytics(
    start_date: date,
    end_date: date,
    metrics: str,
    dimensions: Optional[str] = None,
    filters: Optional[str] = None,
    sort: Optional[str] = None,
    max_results: int = 1000,
    ids: str = "channel==MINE",
) -> Dict:
    """
    Wraps youtubeAnalytics.reports().query
    Docs: https://developers.google.com/youtube/analytics/reference/reports/query
    """
    creds = _load_credentials()
    yta, _ = _build_services(creds)

    try:
        request = yta.reports().query(
            ids=ids,
            startDate=start_date.isoformat(),
            endDate=end_date.isoformat(),
            metrics=metrics,
            dimensions=dimensions,
            filters=filters,
            sort=sort,
            maxResults=max_results,
        )
        response = request.execute()
        return response
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"YouTube Analytics API error: {e}")

def get_channel_basic_info() -> Dict:
    """
    Optional helper to verify auth and get channel info.
    """
    creds = _load_credentials()
    _, yt = _build_services(creds)
    try:
        resp = yt.channels().list(part="snippet,statistics", mine=True).execute()
        return resp
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"YouTube Data API error: {e}")


@router.get("/channel/info")
async def get_channel_info():
    """
    Get basic channel information and statistics.
    """
    return get_channel_basic_info()


@router.get("/reports")
async def get_analytics_report(
    start_date: date = Query(..., description="Start date for analytics (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date for analytics (YYYY-MM-DD)"),
    metrics: str = Query(..., description="Comma-separated list of metrics (e.g., views,likes,comments)"),
    dimensions: Optional[str] = Query(None, description="Comma-separated list of dimensions"),
    filters: Optional[str] = Query(None, description="Filters to apply to the query"),
    sort: Optional[str] = Query(None, description="Sorting options"),
    max_results: int = Query(1000, description="Maximum number of results to return", ge=1, le=10000),
    ids: str = Query("channel==MINE", description="Channel or content owner ID")
):
    """
    Query YouTube Analytics data.

    Common metrics: views, likes, comments, shares, subscribersGained, subscribersLost, averageViewDuration, etc.
    Common dimensions: day, month, country, video, etc.
    """
    return query_yt_analytics(
        start_date=start_date,
        end_date=end_date,
        metrics=metrics,
        dimensions=dimensions,
        filters=filters,
        sort=sort,
        max_results=max_results,
        ids=ids
    )


@router.get("/reports/predefined")
async def get_predefined_reports(
    report_type: str = Query(..., description="Type of predefined report", enum=["overview", "demographics", "traffic_sources"]),
    days: int = Query(30, description="Number of days to look back", ge=1, le=365)
):
    """
    Get predefined analytics reports.

    Available report types:
    - overview: Basic metrics (views, likes, comments, subscribers)
    - demographics: Age and gender demographics
    - traffic_sources: Traffic source types
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    if report_type == "overview":
        metrics = "views,likes,comments,shares,subscribersGained,subscribersLost"
        dimensions = "day"
    elif report_type == "demographics":
        metrics = "viewerPercentage"
        dimensions = "ageGroup,gender"
    elif report_type == "traffic_sources":
        metrics = "views"
        dimensions = "insightTrafficSourceType"
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")

    return query_yt_analytics(
        start_date=start_date,
        end_date=end_date,
        metrics=metrics,
        dimensions=dimensions,
        max_results=1000
    )
