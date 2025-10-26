from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from . import prompt, tools

AGENT_MODEL = "gemini/gemini-2.0-flash"

# Create the agent instance
query_to_apicall_agent = Agent(
    name="query_to_apicall_agent",
    model=LiteLlm(AGENT_MODEL),
    description="Converts natural language queries into YouTube API calls and executes them",
    instruction=prompt.INSTRUCTION,
    tools=[tools.execute_youtube_api_call],
)

