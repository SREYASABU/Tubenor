# Dynamic YouTube Query Capabilities

## Overview

Your agent system can now handle **ANY** YouTube-related query by dynamically constructing the appropriate API calls. The `execute_dynamic_youtube_query` tool provides complete flexibility to access all YouTube Data and Analytics APIs.

---

## What's New?

### Before:
- Limited to predefined endpoints (search, videos, channels, etc.)
- Had to manually add new endpoints for new query types
- Couldn't handle complex analytics queries

### Now:
- **Dynamic query construction** - Agent builds the exact API call needed
- **Full YouTube Analytics API access** - All metrics and dimensions available
- **Complex queries supported** - Multi-dimensional analysis, filtering, sorting
- **Unlimited flexibility** - If YouTube's API supports it, the agent can query it

---

## Available Metrics

### View & Engagement Metrics
| Metric | Description | Example Query |
|--------|-------------|---------------|
| `views` | Number of views | "How many views did I get today?" |
| `estimatedMinutesWatched` | Total watch time | "What's my total watch time this month?" |
| `averageViewDuration` | Average seconds watched | "What's my average view duration?" |
| `averageViewPercentage` | Percentage of video watched | "What percentage of my videos do people watch?" |
| `likes` | Number of likes | "How many likes on my latest video?" |
| `comments` | Number of comments | "How many comments did I get this week?" |
| `shares` | Times shared | "Which video was shared the most?" |

### Subscriber Metrics
| Metric | Description | Example Query |
|--------|-------------|---------------|
| `subscribersGained` | New subscribers | "How many subscribers did I gain yesterday?" |
| `subscribersLost` | Lost subscribers | "Did I lose any subscribers this week?" |

### Revenue Metrics (Monetized Channels)
| Metric | Description | Example Query |
|--------|-------------|---------------|
| `estimatedRevenue` | Total estimated revenue | "What's my revenue for last month?" |
| `estimatedAdRevenue` | Ad revenue | "How much did I earn from ads?" |
| `cpm` | Cost per thousand impressions | "What's my CPM?" |

### Engagement Rates
| Metric | Description | Example Query |
|--------|-------------|---------------|
| `cardClickRate` | Card click rate | "How effective are my cards?" |
| `annotationClickThroughRate` | Annotation CTR | "What's my annotation performance?" |

---

## Available Dimensions (Grouping)

### Time Dimensions
- `day` - Group by individual days
- `month` - Group by months
- `year` - Group by years

**Example Queries:**
- "Show me my daily views for the last 30 days"
- "Compare my performance month by month"
- "What were my yearly totals?"

### Content Dimensions
- `video` - Group by individual videos
- `playlist` - Group by playlists
- `channel` - Group by channels (for multi-channel owners)

**Example Queries:**
- "Which video got the most views this week?"
- "Rank my videos by engagement"
- "Show me playlist performance"

### Geographic Dimensions
- `country` - Group by country (ISO codes: US, GB, IN, etc.)
- `province` - Group by US states/territories
- `continent` - Group by continents

**Example Queries:**
- "Where are my viewers from?"
- "Compare views from US vs UK"
- "Which countries watch my content the most?"
- "Show me views by continent"

### Demographic Dimensions
- `ageGroup` - Age ranges (13-17, 18-24, 25-34, 35-44, 45-54, 55-64, 65+)
- `gender` - MALE, FEMALE, user_specified

**Example Queries:**
- "What's my audience age breakdown?"
- "Do more men or women watch my videos?"
- "Show me demographics for the 18-24 age group"

### Traffic Source Dimensions
- `insightTrafficSourceType` - Where viewers found your videos
  - YT_SEARCH (YouTube search)
  - RELATED_VIDEO (Suggested videos)
  - SUBSCRIBER (From subscriber feed)
  - YT_CHANNEL (Your channel page)
  - NOTIFICATION (Notifications)
  - EXTERNAL (External websites)
  - PLAYLIST (From playlists)
  - ADVERTISING (Paid ads)
  - And many more...

**Example Queries:**
- "Where is my traffic coming from?"
- "How many views come from YouTube search?"
- "What percentage of views are from subscribers?"

### Device/Platform Dimensions
- `deviceType` - DESKTOP, MOBILE, TABLET, TV, GAME_CONSOLE
- `operatingSystem` - Windows, macOS, Android, iOS, etc.
- `youtubeProduct` - CORE (main YouTube), GAMING, KIDS

**Example Queries:**
- "Do more people watch on mobile or desktop?"
- "How many views come from TV?"
- "What operating systems do my viewers use?"

### Subscription Status
- `subscribedStatus` - SUBSCRIBED, UNSUBSCRIBED

**Example Queries:**
- "How many views come from subscribers vs non-subscribers?"

---

## Example Queries You Can Now Handle

### Basic Performance
```
✅ "Give me the views accumulated by my most recent post"
✅ "How many views did I get today?"
✅ "What's my total views this month?"
✅ "Show me my subscriber count"
✅ "How many likes did I get yesterday?"
```

### Time-Based Trends
```
✅ "Show me my daily views for the last 30 days"
✅ "Compare this month to last month"
✅ "What's my weekly average watch time?"
✅ "Show me my performance over the last quarter"
✅ "How did I do in December compared to November?"
```

### Video Comparisons
```
✅ "Which video got the most views this week?"
✅ "Rank my top 10 videos by engagement"
✅ "Which video has the best retention rate?"
✅ "Show me my worst performing videos"
✅ "Compare my last 5 uploads"
```

### Subscriber Growth
```
✅ "How many subscribers did I gain yesterday?"
✅ "Show me subscriber growth over the last month"
✅ "Did I lose any subscribers this week?"
✅ "What's my net subscriber change?"
```

### Geographic Analysis
```
✅ "Where are my viewers from?"
✅ "Compare views from US vs UK vs Canada"
✅ "Which countries watch my content the most?"
✅ "Show me my top 10 countries by watch time"
✅ "How many views come from India?"
```

### Demographic Insights
```
✅ "What's my audience age breakdown?"
✅ "Do more men or women watch my videos?"
✅ "Show me demographics for my top video"
✅ "What age group engages the most?"
```

### Traffic Source Analysis
```
✅ "Where is my traffic coming from?"
✅ "How many views come from YouTube search?"
✅ "What percentage comes from suggested videos?"
✅ "Show me my top traffic sources"
✅ "How effective are my external promotions?"
```

### Device & Platform
```
✅ "Do more people watch on mobile or desktop?"
✅ "How many TV views do I get?"
✅ "What devices do my viewers use?"
✅ "Show me platform breakdown"
```

### Engagement Analysis
```
✅ "What's my average view duration?"
✅ "What percentage of videos do people watch?"
✅ "How many comments did my latest video get?"
✅ "Which video got the most shares?"
✅ "Show me engagement metrics for this week"
```

### Revenue Queries (Monetized)
```
✅ "What's my revenue for last month?"
✅ "How much did I earn from ads?"
✅ "What's my CPM?"
✅ "Show me daily revenue for the last week"
```

### Complex Queries
```
✅ "Show me my most engaging content from last quarter"
✅ "Compare mobile vs desktop views for my top 5 videos"
✅ "What's my subscriber conversion rate from views?"
✅ "Show me views by country for videos published this month"
✅ "How does my US audience compare to my UK audience demographically?"
```

---

## How It Works

### 1. User Asks Any Question
```
User: "How many views did I get from YouTube search last week?"
```

### 2. API Executor Agent Analyzes
The agent identifies:
- **Metric needed:** `views`
- **Dimension needed:** `insightTrafficSourceType`
- **Filter needed:** Only YouTube search traffic
- **Time period:** Last 7 days
- **Date range:** Calculate start_date and end_date

### 3. Dynamic Query Construction
```python
execute_dynamic_youtube_query(
    query_type="analytics",
    metrics="views",
    dimensions="insightTrafficSourceType",
    filters="insightTrafficSourceType==YT_SEARCH",
    start_date="2024-01-20",
    end_date="2024-01-27"
)
```

### 4. API Execution
The tool constructs and executes the exact YouTube Analytics API call needed.

### 5. Response Generation
Raw API data is passed to the Response Generator Agent, which creates:
```
"Last week, you received 12,450 views from YouTube search, which 
accounts for 35% of your total views. This shows strong SEO performance! 
Your videos are ranking well in search results."
```

---

## Technical Details

### The Dynamic Query Tool

**Function:** `execute_dynamic_youtube_query()`

**Parameters:**
- `query_type`: Type of query (analytics, my_videos, video_details, etc.)
- `metrics`: Comma-separated metrics
- `dimensions`: Comma-separated dimensions  
- `filters`: Filter expressions
- `sort`: Sort order (-views for descending)
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `max_results`: Maximum results
- `**additional_params`: Any other query-specific parameters

**Supports:**
- ✅ YouTube Analytics API (all metrics and dimensions)
- ✅ YouTube Data API v3 (search, videos, channels, etc.)
- ✅ Complex filtering and sorting
- ✅ Multi-dimensional analysis
- ✅ Date range queries
- ✅ Geographic and demographic filtering

---

## Real-World Use Cases

### Content Creator Dashboard
```
"Show me a complete overview of my channel performance this month"
→ Agent fetches: total views, watch time, subscriber growth, 
   top videos, traffic sources, and demographics
```

### Video Performance Analysis
```
"Analyze the performance of my video uploaded on Monday"
→ Agent fetches: views, likes, comments, shares, retention,
   traffic sources, and compares to channel average
```

### Audience Understanding
```
"Who is my audience and where are they from?"
→ Agent fetches: age/gender breakdown, top countries,
   device types, and subscription status
```

### Growth Tracking
```
"Track my subscriber growth over the last 3 months"
→ Agent fetches: daily subscribers gained/lost, net growth,
   and identifies peak growth periods
```

### Revenue Optimization
```
"Which videos generate the most revenue?"
→ Agent fetches: revenue by video, CPM rates,
   and correlates with engagement metrics
```

---

## Advanced Query Examples

### Multi-Dimensional Analysis
```
Query: "Show me views by country and device type for my top video"

Agent constructs:
execute_dynamic_youtube_query(
    query_type="analytics",
    metrics="views",
    dimensions="country,deviceType",
    filters="video==TOP_VIDEO_ID",
    start_date="2024-01-01",
    end_date="2024-01-27",
    sort="-views"
)
```

### Filtered Time Series
```
Query: "Show me daily subscriber growth for just US viewers"

Agent constructs:
execute_dynamic_youtube_query(
    query_type="analytics",
    metrics="subscribersGained,subscribersLost",
    dimensions="day",
    filters="country==US",
    start_date="2024-01-01",
    end_date="2024-01-27",
    sort="day"
)
```

### Comparative Analysis
```
Query: "Compare engagement between mobile and desktop viewers"

Agent constructs:
execute_dynamic_youtube_query(
    query_type="analytics",
    metrics="likes,comments,shares,averageViewDuration",
    dimensions="deviceType",
    start_date="2024-01-01",
    end_date="2024-01-27"
)
```

---

## Limitations

The system can query anything YouTube's API supports, but:

1. **API Quotas**: YouTube has daily quota limits
2. **Date Ranges**: Analytics data typically available from 2-3 days ago
3. **Monetization**: Revenue metrics only for monetized channels
4. **Historical Data**: Some metrics have limited historical availability
5. **Real-time**: Analytics are not real-time (24-48 hour delay)

---

## Summary

Your agent system now has **unlimited flexibility** to handle any YouTube-related query. The agent:

✅ Understands natural language questions
✅ Dynamically constructs the right API call
✅ Accesses ALL YouTube API metrics and dimensions
✅ Handles complex, multi-dimensional queries
✅ Provides natural language responses with insights

**Bottom line:** If you can ask it about YouTube data, the agent can fetch and explain it!

---

## Testing

Try these queries to see the dynamic capabilities:

```bash
# Basic
"Give me the views accumulated by my most recent post"

# Trend Analysis
"Show me my daily views for the last month"

# Geographic
"Where are my viewers from?"

# Demographics
"What's my audience age breakdown?"

# Traffic
"Where is my traffic coming from?"

# Complex
"Show me my most engaging content from last quarter, broken down by country"
```

The agent will handle all of these by dynamically constructing the appropriate API calls! 🚀

