from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool

from .guardrail import block_keyword_guardrail
from .sub_agents import (
    api_executor_agent,
    response_generator_agent,
)

from . import prompt

# AGENT_MODEL = "ollama/qwen3:4b"
AGENT_MODEL = "gemini/gemini-2.0-flash"
# AGENT_MODEL = "gemini/gemini-2.5-flash-preview-05-20"

coordinator_agent = Agent(
    name="youtube_assistant",
    model=LiteLlm(AGENT_MODEL),
    description="You are an AI-powered YouTube assistant that helps users understand and analyze their YouTube channel data through natural language queries.",
    instruction=prompt.INSTRUCTION,
    tools=[
        AgentTool(agent=api_executor_agent, skip_summarization=False),
        AgentTool(agent=response_generator_agent, skip_summarization=False),
    ],
    before_model_callback=block_keyword_guardrail,
)
