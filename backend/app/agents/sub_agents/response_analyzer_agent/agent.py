from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from . import prompt, tools

AGENT_MODEL = "gemini/gemini-2.0-flash"


response_analyzer_agent = Agent(
    name="response_analyzer_agent",
    model=LiteLlm(AGENT_MODEL),
    description="The incident manager agent manages all existing incident related tasks.",
    instruction=prompt.INSTRUCTION,
    tools = [tools.analyze_youtube_data],
)