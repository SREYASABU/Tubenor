# Agent System Usage Examples

This document provides practical examples of how the YouTube Assistant agent system works.

---

## Quick Start

### Starting the Agent Runner

```bash
cd Tubentor/backend
python -m app.agents.agent_runner
```

Then enter queries interactively:
```
Enter your query: Find videos about Python programming
```

---

## Example Queries

### 1. Search for Videos

**Query:** "Find videos about machine learning"

**What happens:**
1. Coordinator Agent receives the query
2. Delegates to API Executor Agent
3. API Executor Agent:
   - Identifies intent: search for videos
   - Selects endpoint: `data/search`
   - Calls: `execute_youtube_api_call("data", "search", {"query": "machine learning", "max_results": 10})`
4. YouTube API returns search results
5. Coordinator delegates to Response Generator Agent
6. Response Generator transforms raw data to:

```
I found several videos about machine learning. Here are the top results:

1. **'Machine Learning Crash Course'** by Google Developers
   - 1.2M views • Posted 2 years ago
   - Complete course covering ML fundamentals

2. **'Neural Networks from Scratch'** by Sentdex
   - 450K views • Posted 1 year ago
   - Build neural networks using Python

3. **'Deep Learning Specialization'** by Andrew Ng
   - 2.8M views • Posted 3 years ago
   - Comprehensive deep learning series

These videos cover a range from beginner to advanced topics. 
The Google Developers course is great for getting started!
```

---

### 2. Get Channel Statistics

**Query:** "Show me my channel statistics"

**What happens:**
1. Coordinator → API Executor: "Show me my channel statistics"
2. API Executor:
   - Intent: get channel info
   - Endpoint: `data/channels`
   - Calls: `execute_youtube_api_call("data", "channels", {})`
3. YouTube API returns channel data
4. Coordinator → Response Generator
5. Response Generator generates:

```
Here's an overview of your channel performance:

📊 **Channel Statistics**
- **Subscribers:** 15,234
- **Total Views:** 2,456,789 across all videos
- **Total Videos:** 156 published
- **Channel Created:** March 15, 2020

**Performance Insights:**
- Your average views per video: 15,748
- Subscriber-to-view ratio: 0.62% (healthy engagement)
- You're averaging about 3 videos per month

**Recommendations:**
✓ Your engagement rate is solid! Keep maintaining consistent upload schedules
✓ Consider creating more content similar to your top performers
✓ Your subscriber count suggests good audience retention
```

---

### 3. Get Top Performing Videos

**Query:** "What are my top 5 videos from the last 7 days?"

**What happens:**
1. Coordinator → API Executor: "What are my top 5 videos from the last 7 days?"
2. API Executor:
   - Intent: analytics for top videos
   - Endpoint: `analytics/top_videos`
   - Parameters: `{"days": 7, "limit": 5}`
   - Calls: `execute_youtube_api_call("analytics", "top_videos", {"days": 7, "limit": 5})`
3. YouTube Analytics API returns performance data
4. Coordinator → Response Generator
5. Response Generator creates:

```
Here are your top 5 performing videos from the last 7 days:

🏆 **Top Performers**

1. **"Python Tips Every Developer Should Know"**
   - 📈 12,450 views
   - 👍 523 likes (4.2% like rate)
   - 💬 89 comments
   - ⏱️ Average view duration: 8:45 (87% of video length)
   - 🔥 This is performing exceptionally well!

2. **"Building a REST API with FastAPI"**
   - 📈 8,932 views
   - 👍 412 likes (4.6% like rate)
   - 💬 67 comments
   - ⏱️ Average view duration: 12:30 (75% of video length)

3. **"Docker for Beginners - Full Tutorial"**
   - 📈 7,654 views
   - 👍 298 likes (3.9% like rate)
   - 💬 45 comments
   - ⏱️ Average view duration: 15:20 (68% of video length)

4. **"Git Commands Cheat Sheet"**
   - 📈 6,123 views
   - 👍 234 likes (3.8% like rate)
   - 💬 32 comments
   - ⏱️ Average view duration: 5:10 (85% of video length)

5. **"JavaScript Array Methods Explained"**
   - 📈 5,897 views
   - 👍 276 likes (4.7% like rate)
   - 💬 41 comments
   - ⏱️ Average view duration: 7:45 (82% of video length)

**Key Insights:**
✅ Short-form tutorials (5-10 min) are showing highest engagement
✅ Python-related content is currently your top performer
✅ Like rates across all videos are strong (3.8-4.7%)
✅ Viewer retention is excellent on shorter videos

**Recommendations:**
💡 Consider creating more Python-focused content
💡 Your "tips and tricks" format is resonating well
💡 Short, focused tutorials are performing better than long-form
💡 FastAPI content is trending - consider a series
```

---

### 4. Get Specific Video Details

**Query:** "Get details for video dQw4w9WgXcQ"

**What happens:**
1. Coordinator → API Executor: "Get details for video dQw4w9WgXcQ"
2. API Executor:
   - Intent: video details
   - Endpoint: `data/videos`
   - Parameters: `{"video_id": "dQw4w9WgXcQ"}`
   - Calls: `execute_youtube_api_call("data", "videos", {"video_id": "dQw4w9WgXcQ"})`
3. YouTube API returns video details
4. Coordinator → Response Generator
5. Response Generator formats:

```
Here are the details for the video:

**"Rick Astley - Never Gonna Give You Up (Official Video)"**

📺 **Video Information**
- Channel: Rick Astley
- Published: October 25, 2009
- Duration: 3:33
- Category: Music

📊 **Statistics**
- Views: 1,234,567,890
- Likes: 14,567,890
- Comments: 3,456,789
- Like ratio: 98.5% positive

📝 **Description:**
The official video for "Never Gonna Give You Up" by Rick Astley...

**Performance Analysis:**
This video has exceptional engagement with over 1.2 billion views!
The like-to-view ratio of 1.18% is very strong for a music video.
With millions of comments, this content has sparked significant discussion.
```

---

### 5. Search with Specific Criteria

**Query:** "Find recent Python tutorials with more than 100k views"

**What happens:**
1. API Executor interprets the complex query
2. Makes assumptions about parameters:
   - `query`: "Python tutorials"
   - `max_results`: 10 (default)
3. Calls: `execute_youtube_api_call("data", "search", {"query": "Python tutorials", "max_results": 10})`
4. Response Generator filters/highlights videos matching criteria
5. Generates response:

```
I searched for recent Python tutorials. Here are videos with 100k+ views:

1. **"Python Full Course for Beginners"**
   - 850K views • Posted 2 months ago
   - Comprehensive 4-hour tutorial

2. **"Learn Python in 2024"**
   - 320K views • Posted 1 month ago
   - Updated with latest Python features

3. **"Python Project Ideas"**
   - 145K views • Posted 3 weeks ago
   - 10 practical project walkthroughs

Note: I found 3 videos matching your criteria (recent + 100k+ views).
Would you like me to search for more specific topics?
```

---

### 6. Analytics with Date Range

**Query:** "Show me analytics for video ABC123 for the last 30 days"

**What happens:**
1. API Executor:
   - Endpoint: `analytics/video_analytics`
   - Parameters: `{"video_id": "ABC123", "days": 30}`
2. Calls: `execute_youtube_api_call("analytics", "video_analytics", {"video_id": "ABC123", "days": 30})`
3. Response Generator analyzes the metrics:

```
Here's a 30-day analytics report for your video:

📊 **Performance Summary (Last 30 Days)**

**View Metrics:**
- Total Views: 45,678
- Average Daily Views: 1,523
- Peak Day: 3,456 views (March 15th)
- Lowest Day: 892 views (March 2nd)

**Engagement Metrics:**
- Likes: 1,234 (2.7% of views)
- Comments: 234 (0.51% of views)
- Shares: 89
- Average View Duration: 8:45 (73% of total length)

**Audience Retention:**
- 90% watched past 1 minute
- 75% watched past 3 minutes
- 58% watched past 5 minutes
- 42% watched until the end

**Traffic Sources:**
- YouTube Search: 45%
- Suggested Videos: 32%
- Direct/Unknown: 13%
- External: 8%
- Playlists: 2%

**Trends:**
📈 Views are trending upward (+15% week over week)
📈 Engagement rate improved in the last 7 days
📉 Click-through rate from impressions: 4.2% (slightly below average)

**Recommendations:**
💡 The upward trend is promising - consider promoting this video more
💡 Strong retention in the first 3 minutes - your hook is working well
💡 Search traffic is high - your SEO is effective
💡 Consider improving thumbnails to increase click-through rate from impressions
```

---

### 7. Get User's Playlists

**Query:** "Show me all my playlists"

**What happens:**
1. API Executor:
   - Endpoint: `data/playlists`
   - Calls: `execute_youtube_api_call("data", "playlists", {})`
2. Response Generator formats the list:

```
Here are all your playlists:

📁 **Your Playlists** (8 total)

1. **"Python Tutorials"**
   - 24 videos
   - Created: January 15, 2023
   - Last updated: 2 days ago

2. **"Web Development Series"**
   - 18 videos
   - Created: March 3, 2023
   - Last updated: 1 week ago

3. **"Data Science Basics"**
   - 15 videos
   - Created: February 10, 2023
   - Last updated: 3 weeks ago

[... more playlists ...]

**Playlist Insights:**
✓ You have a good variety of organized content
✓ Most playlists are actively maintained
✓ Your Python playlist has the most videos
✓ Consider creating playlists for cross-promotion
```

---

## Error Handling Examples

### Invalid Video ID

**Query:** "Get details for video INVALID123"

**Response:**
```
I tried to fetch the video details, but encountered an issue:

❌ **Error:** The video ID 'INVALID123' doesn't appear to be valid or 
the video may have been deleted.

**Suggestions:**
- Check if the video ID is correct
- Verify the video is still available on YouTube
- Try searching for the video by title instead

Would you like me to search for something specific?
```

### No Results Found

**Query:** "Find videos about asdfghjklzxcvbnm"

**Response:**
```
I searched for videos about "asdfghjklzxcvbnm" but didn't find any results.

**Suggestions:**
- Try using different search terms
- Check the spelling
- Use more general keywords
- Broaden your search criteria

Would you like to try a different search?
```

### API Rate Limit

**Query:** "Show me my channel statistics"

**Response:**
```
I encountered an issue while fetching your channel data:

⚠️ **API Rate Limit Exceeded**
YouTube's API quota has been reached. This typically resets at midnight Pacific Time.

**What you can do:**
- Try again in a few hours
- Reduce the number of queries
- Check the YouTube Studio dashboard directly for immediate access

Sorry for the inconvenience!
```

---

## Advanced Usage

### Combining Multiple Queries

You can ask follow-up questions in the same session:

```
Query 1: "Show me my top videos"
→ [Response with top videos]

Query 2: "Get details for the first one"
→ [Agent uses context from previous query to identify "first one"]
```

### Natural Language Variations

All of these work:
- "Find videos about Python"
- "Search for Python tutorials"
- "Look for Python programming content"
- "Show me videos related to Python"

### Implicit Parameters

The agent can infer missing parameters:
- "Show me my top videos" → defaults to last 30 days, limit 10
- "Search for tutorials" → defaults to max_results=10
- "Get my channel info" → uses authenticated user's channel

---

## Testing Checklist

✅ Search functionality
✅ Channel statistics
✅ Top videos analytics
✅ Specific video details
✅ Playlist management
✅ Error handling
✅ Natural language variations
✅ Date range queries
✅ Parameter inference

---

## Tips for Best Results

1. **Be specific when needed:** "Top 5 videos from last week" vs "Top videos"
2. **Use natural language:** The agents understand conversational queries
3. **Ask follow-up questions:** The system maintains context
4. **Try different phrasings:** Multiple ways to ask the same thing work
5. **Check error messages:** They provide helpful guidance

---

## Common Query Patterns

### Search Patterns
- "Find videos about [topic]"
- "Search for [keyword]"
- "Look for [content type] about [topic]"

### Analytics Patterns
- "Show me my [metric]"
- "What are my top [N] videos from [time period]"
- "Get analytics for [video] for [duration]"

### Information Patterns
- "Get details for [video]"
- "Show me my [resource type]"
- "What's my [metric]"

---

## Next Steps

- Try the examples above in your own environment
- Experiment with different query phrasings
- Check the AGENT_ARCHITECTURE.md for technical details
- Extend the system with new endpoints as needed

Happy querying! 🚀

