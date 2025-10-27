from google.adk.agents import SequentialAgent

from .guardrail import block_keyword_guardrail
from .sub_agents import (
    api_executor_agent,
    response_generator_agent,
)

# Create a SequentialAgent that executes agents in order:
# 1. api_executor_agent - fetches YouTube data and stores in state['api_response']
# 2. response_generator_agent - reads state['api_response'] and generates natural language

coordinator_agent = SequentialAgent(
    name="youtube_assistant",
    sub_agents=[api_executor_agent, response_generator_agent],
    description="Executes a sequence of YouTube data fetching and response generation.",
)
