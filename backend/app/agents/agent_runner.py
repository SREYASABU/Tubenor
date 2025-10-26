import os

from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory import InMemoryMemoryService
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService, InMemorySessionService
from google.genai import types
from app.utils.logger import get_service_logger

from .main_agent import coordinator_agent

logger = get_service_logger("agent_runner")
DB_URL = os.getenv("DATABASE_URL", None)
session_service: DatabaseSessionService | InMemorySessionService
if DB_URL is None:
    logger.info("No DATABASE_URL env found, using in-memory session service.")
    session_service = InMemorySessionService()
else:
    logger.info("Using database session service")
    session_service = DatabaseSessionService(db_url=DB_URL)

memory_service = InMemoryMemoryService()
artifact_service = InMemoryArtifactService()


async def get_or_create_session(
    app_name: str, user_id: str, session_id: str, initial_state: dict
):
    retrieved_session = await session_service.get_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
    if retrieved_session:
        return retrieved_session
    return await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id, state=initial_state
    )


def get_runner(app_name, agent) -> Runner:
    return Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
        memory_service=memory_service,
        artifact_service=artifact_service,
        plugins=[LoggingPlugin()],
    )


async def call_agent_async(query: str, runner: Runner, user_id: str, session_id: str):
    """Sends a query to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response."  # Default

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        print(
            f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}"
        )

        if event.is_final_response():
            if event.content and event.content.parts and event.content.parts[0].text:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )
            break  # Stop processing events once the final response is found

    print(f"<<< Agent Response: {final_response_text}")
    return final_response_text


async def main():
    # Define constants for identifying the interaction context
    APP_NAME = "test_app"
    USER_ID = "user_1"
    SESSION_ID = "session_001"  # Using a fixed ID for simplicity

    """
    No prefix: Session-specific, persists only for the current session
    user:: User-specific, persists across all sessions for a particular user
    app:: Application-wide, shared across all users and sessions
    temp:: Temporary, exists only during the current execution cycle
    """
    initial_state = {"user:preferences": {"language": "English"}}
    await get_or_create_session(APP_NAME, USER_ID, SESSION_ID, initial_state)
    runner = get_runner(APP_NAME, coordinator_agent)
    print(f"Runner created for agent '{runner.agent.name}'.")

    while True:
        text = input("Enter your query: ")
        if text.lower() == "exit":
            break
        await call_agent_async(
            text, runner=runner, user_id=USER_ID, session_id=SESSION_ID
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
