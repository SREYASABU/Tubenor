from app.database.core import DbSession
from fastapi import HTTPException
from google.adk.agents import LlmAgent
# from routes.auth.service import CurrentUser
from app.utils.logger import get_service_logger
from uuid import UUID
from .agent_runner import call_agent_async, get_or_create_session, get_runner

# Setup centralized logging
logger = get_service_logger("agents_utils")


async def handle_agent_request(
    db: DbSession,query: str, agent: LlmAgent
) -> str:
    APP_NAME = "test_app"
    initial_state = {"user:preferences": {"language": "English"}}
    user_id = '9b9b9a78-6dab-488b-b51b-e8a4ec063fd4'
    if not user_id:
        logger.warning("Unauthorized agent request attempt")
        raise HTTPException(status_code=401, detail="Unauthorized")
    logger.info(f"Processing agent request for user {user_id}")
    session_id = "session_001"  # Using a fixed ID for simplicity
    await get_or_create_session(APP_NAME, str(user_id), session_id, initial_state)
    runner = get_runner(APP_NAME, agent)
    response = await call_agent_async(query, runner, str(user_id), session_id)
    logger.info(f"Agent request processed for user {user_id}")
    return response
