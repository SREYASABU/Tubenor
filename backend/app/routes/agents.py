import os
from datetime import date, timedelta
from typing import Dict, Optional

from fastapi import HTTPException, APIRouter, Query

router = APIRouter(prefix="/agents", tags=["agents"])

@router.get("/root_agent")
def get_root_agent(user_query: Optional[str] = Query(None, description="Optional user query to interact with the root agent")):
    """
    Endpoint to get information about the root agent.
    """
    return {"agent": "root_agent", "description": "This is the root agent responsible for coordinating sub-agents."}