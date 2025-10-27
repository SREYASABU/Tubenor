# YouTube Assistant Agent Architecture

## Overview

This system uses a **SequentialAgent workflow** to handle YouTube data queries:

1. **API Executor Agent** - Converts natural language to API calls and executes them
2. **Response Generator Agent** - Transforms raw API responses into natural language

The agents are connected using ADK's `SequentialAgent`, which executes them in a deterministic order and automatically passes data between agents via shared session state.

---

## Agent Architecture

```
User Query
    ↓
┌─────────────────────────────────────────────────────┐
│  SequentialAgent (youtube_assistant)                │
│  ┌───────────────────────────────────────────────┐  │
│  │  Step 1: API Executor Agent                   │  │
│  │  - Executes YouTube API calls                 │  │
│  │  - Stores result in state['api_response']     │  │
│  └───────────────────────────────────────────────┘  │
│                       ↓                              │
│         (Data automatically passed via state)        │
│                       ↓                              │
│  ┌───────────────────────────────────────────────┐  │
│  │  Step 2: Response Generator Agent             │  │
│  │  - Reads state['api_response']                │  │
│  │  - Generates natural language response        │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
    ↓
Final Natural Language Response to User
```

**Key Benefits:**
- ✅ **Deterministic execution** - Agents run in exact order, every time
- ✅ **No looping** - Each agent runs exactly once per query
- ✅ **Automatic data passing** - Output from agent 1 → input to agent 2 via state
- ✅ **Built-in by ADK** - Uses official Google ADK `SequentialAgent` pattern

---

## Agent Responsibilities

### 1. SequentialAgent (`coordinator_agent`)

**Type:** Workflow Agent (ADK built-in)

**Location:** `Tubentor/backend/app/agents/main_agent.py`

**Configuration:**
```python
SequentialAgent(
    name="youtube_assistant",
    sub_agents=[api_executor_agent, response_generator_agent],
    description="Executes a sequence of YouTube data fetching and response generation."
)
```

**How it works:**
- Receives user query
- Executes `api_executor_agent` first (stores result in `state['api_response']`)
- Automatically executes `response_generator_agent` second (reads from `state['api_response']`)
- Returns final response to user
- **Not powered by LLM** - purely deterministic execution order

---

### 2. API Executor Agent (`api_executor_agent`)

**Type:** LLM Agent

**Role:** Execute YouTube API calls and store results

**Location:** `Tubentor/backend/app/agents/sub_agents/query_to_apicall_agent/`

**Configuration:**
```python
Agent(
    name="api_executor_agent",
    model=LiteLlm("gemini/gemini-2.0-flash"),
    tools=[execute_dynamic_youtube_query, execute_youtube_api_call],
    output_key="api_response"  # Stores output in state for next agent
)
```

**Responsibilities:**
- Parse user's natural language query
- Identify the appropriate YouTube API endpoint
- Extract or infer necessary parameters
- Execute API call using `execute_dynamic_youtube_query` tool
- **Store raw API response in `state['api_response']`** for the next agent

**Available API Endpoints:**

#### YouTube Data API (api_type="data")

1. **Search Endpoint** (`endpoint="search"`)
   - Parameters: `query` (required), `max_results` (optional, default=10)
   - Use case: Search for videos, channels, or playlists
   - Example: "Find videos about machine learning"

2. **Videos Endpoint** (`endpoint="videos"`)
   - Parameters: `video_id` (required)
   - Use case: Get detailed video information with statistics
   - Example: "Get details for video dQw4w9WgXcQ"

3. **Channels Endpoint** (`endpoint="channels"`)
   - Parameters: None (uses authenticated user's channel)
   - Use case: Get channel statistics and information
   - Example: "Show me my channel statistics"

4. **Playlists Endpoint** (`endpoint="playlists"`)
   - Parameters: `max_results` (optional, default=50)
   - Use case: Get user's playlists
   - Example: "Show me my playlists"

#### YouTube Analytics API (api_type="analytics")

1. **Top Videos Endpoint** (`endpoint="top_videos"`)
   - Parameters: `days` (optional, default=30), `limit` (optional, default=10)
   - Use case: Get top performing videos
   - Example: "What are my top 5 videos from the last 7 days?"

2. **Video Analytics Endpoint** (`endpoint="video_analytics"`)
   - Parameters: `video_id` (required), `days` (optional, default=30)
   - Use case: Get analytics for a specific video
   - Example: "Show me analytics for video XYZ for the last week"

**Tool Available:**
- `execute_youtube_api_call(api_type, endpoint, params)` - Executes YouTube API calls

---

### 3. Response Generator Agent (`response_generator_agent`)

**Type:** LLM Agent

**Role:** Transform raw API data into natural language responses

**Location:** `Tubentor/backend/app/agents/sub_agents/response_analyzer_agent/`

**Configuration:**
```python
Agent(
    name="response_generator_agent",
    model=LiteLlm("gemini/gemini-2.0-flash"),
    instruction="""... {api_response} ...""",  # Reads from state
    tools=[]  # No tools needed, pure LLM analysis
)
```

**Responsibilities:**
- **Read raw API data from `state['api_response']`** (automatically injected via `{api_response}` placeholder)
- Interpret the YouTube API response structure
- Extract key insights and patterns
- Present information in clear, natural language
- Provide actionable recommendations
- Return final user-facing response

**Response Style:**
- Professional but friendly
- Clear and concise
- Uses bullet points and formatting for clarity
- Highlights important metrics
- Provides context for numbers
- Offers practical recommendations

**State Injection:** The instruction template contains `{api_response}` which ADK automatically replaces with the value from `state['api_response']` set by the previous agent.

---

## Example Queries and Flows (SequentialAgent Pattern)

### Example 1: Search Query

**User Query:** "Find videos about machine learning"

**Sequential Flow:**
```
User Query → SequentialAgent → Agent 1 (api_executor) → Agent 2 (response_generator) → User
```

1. **SequentialAgent receives** user query: "Find videos about machine learning"

2. **Step 1 - API Executor Agent executes:**
   - Analyzes query to determine it needs video search
   - Calls `execute_dynamic_youtube_query(query_type="search", q="machine learning")`
   - Receives raw YouTube API response with video list
   - **Stores in `state['api_response']`** via `output_key="api_response"`

3. **Step 2 - Response Generator Agent executes:**
   - Instruction contains `{api_response}` placeholder
   - ADK automatically injects `state['api_response']` into the instruction
   - Analyzes the data and creates natural language response:
   ```
   I found several videos about machine learning. Here are the top results:

   1. **'Machine Learning Basics'** by Stanford Online
      - 2.3M views • Posted 1 year ago
      - Comprehensive introduction to ML concepts

   2. **'Neural Networks Explained'** by 3Blue1Brown
      - 5.1M views • Posted 3 years ago
      - Visual explanation of neural networks
   ```

4. **User receives** the natural language response

### Example 2: Latest Video Views

**User Query:** "How many views does my latest video have?"

**Sequential Flow:**

1. **API Executor Agent:**
   - Calls `execute_dynamic_youtube_query(query_type="my_videos", max_results=1, order="date", include_statistics=True)`
   - Stores result: `state['api_response'] = {"items": [{"title": "Tutorial on Python", "statistics": {"viewCount": "1201"}, ...}]}`

2. **Response Generator Agent:**
   - Reads `{api_response}` from state
   - Generates response:
   ```
   Your most recent video "Tutorial on Python" has 1,201 views.
   It was published 2 days ago, averaging about 600 views per day!
   ```

### Example 3: Channel Statistics

**User Query:** "Show me my channel statistics"

**Sequential Flow:**

1. **API Executor Agent:**
   - Calls `execute_dynamic_youtube_query(query_type="channel_details")`
   - Stores: `state['api_response'] = {"subscriberCount": "15234", "videoCount": "156", ...}`

2. **Response Generator Agent:**
   - Reads from state and generates:
   ```
   📊 **Channel Statistics**
   - **Subscribers:** 15,234
   - **Total Videos:** 156
   - **Total Views:** 2.4M

   Your channel is growing steadily!
   ```

---

## File Structure

```
Tubentor/backend/app/agents/
├── main_agent.py                    # Coordinator Agent
├── prompt.py                        # Coordinator Agent prompt
├── agent_runner.py                  # Runner for executing agents
├── guardrail.py                     # Guardrails for agents
├── utils.py                         # Agent utilities
└── sub_agents/
    ├── __init__.py                  # Export sub-agents
    ├── query_to_apicall_agent/      # API Executor Agent
    │   ├── agent.py                 # Agent definition
    │   ├── prompt.py                # Agent instruction
    │   ├── tools.py                 # execute_youtube_api_call tool
    │   └── utils.py                 # Utility functions
    └── response_analyzer_agent/     # Response Generator Agent
        ├── agent.py                 # Agent definition
        ├── prompt.py                # Agent instruction
        ├── tools.py                 # (Not used - LLM analyzes directly)
        └── utils.py                 # Utility functions
```

---

## Key Design Principles

1. **Separation of Concerns**
   - API execution is separate from response generation
   - Each agent has a single, clear responsibility

2. **Clear Data Flow**
   - User Query → API Execution → Response Generation → User
   - No ambiguity in the workflow

3. **Flexibility**
   - Easy to add new API endpoints
   - Easy to modify response styles
   - Coordinator can be enhanced with additional logic

4. **Maintainability**
   - Clear agent naming (api_executor, response_generator)
   - Well-documented prompts
   - Modular structure

5. **Error Handling**
   - Tools catch and return errors
   - Response Generator can explain errors naturally
   - Coordinator ensures graceful degradation

---

## Testing the System

### Via API Endpoint

```bash
POST http://localhost:8000/agents/general-query
Content-Type: application/json

{
  "query": "Find videos about Python programming"
}
```

### Via Python (Direct)

```python
from app.agents.agent_runner import call_agent_async, get_runner
from app.agents.main_agent import coordinator_agent

runner = get_runner("test_app", coordinator_agent)
response = await call_agent_async(
    query="Show me my channel statistics",
    runner=runner,
    user_id="user_1",
    session_id="session_001"
)
print(response)
```

### Via Command Line

```bash
cd Tubentor/backend
python -m app.agents.agent_runner
# Then enter queries interactively
```

---

## Extending the System

### Adding a New API Endpoint

1. **Update YouTube Service** (`services/youtube_service.py`)
   ```python
   def new_endpoint(self, param1, param2):
       # Implementation
       pass
   ```

2. **Update API Executor Tool** (`sub_agents/query_to_apicall_agent/tools.py`)
   ```python
   elif endpoint == "new_endpoint":
       param1 = params.get("param1")
       param2 = params.get("param2")
       return youtube_service.new_endpoint(param1=param1, param2=param2)
   ```

3. **Update API Executor Prompt** (`sub_agents/query_to_apicall_agent/prompt.py`)
   - Add documentation for the new endpoint
   - Provide examples of when to use it

### Modifying Response Style

Update the Response Generator prompt (`sub_agents/response_analyzer_agent/prompt.py`) to adjust:
- Tone and formality
- Level of detail
- Formatting preferences
- Recommendation style

---

## Troubleshooting

### Agent not calling API Executor

**Issue:** Coordinator responds directly without delegating

**Solution:** 
- Check coordinator prompt emphasizes delegation
- Ensure api_executor_agent is properly registered in tools
- Verify AgentTool is not set to skip_summarization incorrectly

### API calls failing

**Issue:** execute_youtube_api_call returns errors

**Solution:**
- Check YouTube API credentials in environment variables
- Verify API quotas haven't been exceeded
- Check if the parameters are being passed correctly
- Review YouTube Service implementation

### Response Generator not producing insights

**Issue:** Response is just raw data dump

**Solution:**
- Review Response Generator prompt
- Ensure raw API data is being passed correctly
- Check if the LLM model has sufficient capabilities
- Verify the prompt examples are clear and detailed

---

## Configuration

### Environment Variables

Required for YouTube API access:
```env
YT_CLIENT_ID=your_client_id
YT_CLIENT_SECRET=your_client_secret
YT_REFRESH_TOKEN=your_refresh_token
```

### Model Configuration

Default model: `gemini/gemini-2.0-flash`

To change models, update the `AGENT_MODEL` variable in:
- `main_agent.py` (Coordinator)
- `sub_agents/query_to_apicall_agent/agent.py` (API Executor)
- `sub_agents/response_analyzer_agent/agent.py` (Response Generator)

---

## Best Practices

1. **Always delegate to both agents** - Don't skip steps
2. **Pass complete context** - Include original query when delegating
3. **Handle errors gracefully** - Return helpful error messages
4. **Keep prompts updated** - Document all available endpoints
5. **Test new endpoints** - Verify the full flow works end-to-end
6. **Monitor API usage** - YouTube APIs have quotas
7. **Log agent interactions** - Use the logging plugin for debugging

---

## Summary

This agent architecture provides a clean, maintainable way to handle YouTube data queries:

- **User-friendly:** Natural language input and output
- **Modular:** Each agent has a clear purpose
- **Extensible:** Easy to add new features
- **Robust:** Error handling at each stage
- **Scalable:** Can handle various query types

The two-stage approach (fetch data → generate response) ensures consistent, high-quality outputs while keeping the codebase organized and maintainable.

