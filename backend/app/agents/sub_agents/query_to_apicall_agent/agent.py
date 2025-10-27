from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from . import prompt, tools

AGENT_MODEL = "gemini/gemini-2.0-flash"

# Create the agent instance
api_executor_agent = Agent(
    name="api_executor_agent",
    model=LiteLlm(AGENT_MODEL),
    description="Understands user queries about YouTube data and dynamically constructs and executes the appropriate YouTube API calls to fetch any requested information.",
    instruction=prompt.INSTRUCTION,
    tools=[
        tools.execute_dynamic_youtube_query,  # Primary tool - handles ANY YouTube query dynamically
        tools.execute_youtube_api_call,        # Legacy tool - kept for backwards compatibility
    ],
)

