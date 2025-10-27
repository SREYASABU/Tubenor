from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from . import prompt

AGENT_MODEL = "gemini/gemini-2.0-flash"


response_generator_agent = Agent(
    name="response_generator_agent",
    model=LiteLlm(AGENT_MODEL),
    description="Transforms raw YouTube API responses into clear, insightful natural language responses with actionable recommendations.",
    instruction=prompt.INSTRUCTION,
    tools=[],  # This agent doesn't need tools - it analyzes data using its LLM capabilities
)