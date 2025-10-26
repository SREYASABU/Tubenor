from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool

from .guardrail import block_keyword_guardrail
from .sub_agents import (
    query_to_apicall_agent,
    response_analyzer_agent,
)

from . import prompt

# AGENT_MODEL = "ollama/qwen3:4b"
AGENT_MODEL = "gemini/gemini-2.0-flash"
# AGENT_MODEL = "gemini/gemini-2.5-flash-preview-05-20"

coordinator_agent = Agent(
    name="ai_assistant",
    model=LiteLlm(AGENT_MODEL),
    description="You are an AI based incident assistant. Your role is to assist the user in managing incidents by delegating tasks to the most appropriate specialized agents or utilizing available tools.",
    instruction=prompt.INSTRUCTION,
    tools=[
        AgentTool(agent=query_to_apicall_agent, skip_summarization=False),
        AgentTool(agent=response_analyzer_agent, skip_summarization=False),
    ],
    before_model_callback=block_keyword_guardrail,
)
