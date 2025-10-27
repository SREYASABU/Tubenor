# YouTube Assistant Agent Architecture

## Overview

This system uses a **two-stage agent workflow** to handle YouTube data queries:

1. **API Executor Agent** - Converts natural language to API calls and executes them
2. **Response Generator Agent** - Transforms raw API responses into natural language

The **Coordinator Agent** orchestrates both sub-agents to provide a seamless user experience.

---

## Agent Architecture

```
User Query
    ↓
┌─────────────────────────┐
│  Coordinator Agent      │  ← Orchestrates the workflow
│  (youtube_assistant)    │
└─────────────────────────┘
    ↓                  ↓
    ↓                  ↓
┌─────────────────────────┐    ┌─────────────────────────┐
│  API Executor Agent     │ →  │ Response Generator      │
│  (api_executor_agent)   │    │ (response_generator)    │
└─────────────────────────┘    └─────────────────────────┘
    ↓                                      ↓
    ↓                                      ↓
[YouTube API Call]              [Natural Language Response]
```

---

## Agent Responsibilities

### 1. Coordinator Agent (`coordinator_agent`)

**Role:** Orchestrate the entire query handling workflow

**Location:** `Tubentor/backend/app/agents/main_agent.py`

**Responsibilities:**
- Receive user queries
- Delegate to API Executor Agent to fetch data
- Pass API response to Response Generator Agent
- Return final natural language response to user

**Example Workflow:**
```
User: "Find videos about Python programming"
  ↓
Step 1: Coordinator → API Executor: "Find videos about Python programming"
Step 2: API Executor → YouTube API: search(query="Python programming")
Step 3: API Executor → Coordinator: [Raw API Response]
Step 4: Coordinator → Response Generator: [Raw API Response]
Step 5: Response Generator → Coordinator: [Natural Language Response]
Step 6: Coordinator → User: "I found several videos about Python programming..."
```

---

### 2. API Executor Agent (`api_executor_agent`)

**Role:** Understand queries and execute YouTube API calls

**Location:** `Tubentor/backend/app/agents/sub_agents/query_to_apicall_agent/`

**Responsibilities:**
- Parse user's natural language query
- Identify the appropriate YouTube API endpoint
- Extract or infer necessary parameters
- Execute API call using `execute_youtube_api_call` tool
- Return raw API response

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

**Role:** Transform raw API data into natural language responses

**Location:** `Tubentor/backend/app/agents/sub_agents/response_analyzer_agent/`

**Responsibilities:**
- Interpret raw YouTube API responses
- Extract key insights and patterns
- Present information in clear, natural language
- Provide actionable recommendations
- Make complex data easy to understand

**Response Style:**
- Professional but friendly
- Clear and concise
- Uses bullet points and formatting for clarity
- Highlights important metrics
- Provides context for numbers
- Offers practical recommendations

**No tools needed** - This agent uses its LLM capabilities to analyze and transform data

---

## Example Queries and Flows

### Example 1: Search Query

**User Query:** "Find videos about machine learning"

**Flow:**
1. Coordinator receives query
2. Coordinator → API Executor: "Find videos about machine learning"
3. API Executor analyzes query:
   - Intent: Search for videos
   - Endpoint: `data/search`
   - Parameters: `{"query": "machine learning", "max_results": 10}`
4. API Executor calls tool: `execute_youtube_api_call("data", "search", {"query": "machine learning", "max_results": 10})`
5. Tool returns raw YouTube API response with video results
6. Coordinator → Response Generator: [Raw API response]
7. Response Generator creates natural language:
   ```
   I found several videos about machine learning. Here are the top results:

   1. **'Machine Learning Basics'** by Stanford Online
      - 2.3M views • Posted 1 year ago
      - Comprehensive introduction to ML concepts

   2. **'Neural Networks Explained'** by 3Blue1Brown
      - 5.1M views • Posted 3 years ago
      - Visual explanation of neural networks
   
   [etc...]
   ```

### Example 2: Channel Statistics

**User Query:** "Show me my channel statistics"

**Flow:**
1. Coordinator → API Executor: "Show me my channel statistics"
2. API Executor: `execute_youtube_api_call("data", "channels", {})`
3. Raw response includes subscriber count, total views, video count
4. Coordinator → Response Generator: [Raw API response]
5. Response Generator:
   ```
   Here's an overview of your channel performance:

   📊 **Channel Statistics**
   - **Subscribers:** 15,234
   - **Total Views:** 2.4M across all videos
   - **Total Videos:** 156

   Your channel is growing steadily! Consider maintaining your 
   current upload schedule and exploring similar content.
   ```

### Example 3: Top Videos Analytics

**User Query:** "What are my top 5 videos from the last 7 days?"

**Flow:**
1. Coordinator → API Executor: "What are my top 5 videos from the last 7 days?"
2. API Executor analyzes:
   - Intent: Get top performing videos
   - Endpoint: `analytics/top_videos`
   - Parameters: `{"days": 7, "limit": 5}`
3. API Executor: `execute_youtube_api_call("analytics", "top_videos", {"days": 7, "limit": 5})`
4. Raw analytics response with performance metrics
5. Coordinator → Response Generator: [Raw analytics data]
6. Response Generator provides insights:
   ```
   Here are your top 5 videos from the last 7 days:

   1. **"Tutorial: Advanced Python Tips"**
      - 12,500 views
      - 450 likes, 89 comments
      - Average view duration: 8:45

   [etc... with insights and recommendations]
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

