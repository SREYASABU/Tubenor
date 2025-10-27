# Quick Query Reference

Fast reference for testing your dynamic YouTube agent system.

---

## 🚀 Most Common Queries

### Recent Content Performance
```
✅ "Give me the views accumulated by my most recent post"
✅ "How is my latest video performing?"
✅ "Show me stats for my most recent upload"
✅ "What's the engagement on my last video?"
```

### Daily Performance
```
✅ "How many views did I get today?"
✅ "How many subscribers did I gain today?"
✅ "Show me today's performance"
✅ "What's my watch time today?"
```

### Weekly Overview
```
✅ "How did I do this week?"
✅ "Show me my weekly performance"
✅ "What are my top videos this week?"
✅ "How many views this week?"
```

### Monthly Trends
```
✅ "Show me my monthly performance"
✅ "How did I do this month compared to last month?"
✅ "What's my total views for the month?"
✅ "Monthly subscriber growth?"
```

### Top Content
```
✅ "What are my top 10 videos?"
✅ "Which video got the most views?"
✅ "Show me my most popular content"
✅ "Rank my videos by engagement"
```

### Subscriber Tracking
```
✅ "How many subscribers did I gain yesterday?"
✅ "Show me subscriber growth over time"
✅ "Am I losing subscribers?"
✅ "What's my net subscriber change?"
```

### Audience Insights
```
✅ "Where are my viewers from?"
✅ "What's my audience demographic?"
✅ "Who watches my videos?"
✅ "Show me age and gender breakdown"
```

### Traffic Sources
```
✅ "Where is my traffic coming from?"
✅ "How many views from YouTube search?"
✅ "What are my top traffic sources?"
✅ "How effective are suggested videos?"
```

### Engagement Metrics
```
✅ "What's my average view duration?"
✅ "How much of my videos do people watch?"
✅ "What's my engagement rate?"
✅ "Show me likes, comments, and shares"
```

---

## 📊 Query Patterns

### Time-Based Queries
Pattern: `[metric] + [time period]`

```
"views last 7 days"
"subscribers this month"
"watch time yesterday"
"comments this week"
"likes in January"
```

### Comparison Queries
Pattern: `compare [metric] between [A] and [B]`

```
"compare views between US and UK"
"compare this month to last month"
"compare mobile vs desktop"
"compare my top 3 videos"
```

### Ranking Queries
Pattern: `top/best [N] [content] by [metric]`

```
"top 5 videos by views"
"best performing content this month"
"most liked videos"
"highest retention videos"
```

### Geographic Queries
Pattern: `[metric] from/in [location]`

```
"views from India"
"traffic from Europe"
"subscribers in US"
"watch time by country"
```

### Demographic Queries
Pattern: `[metric] for [demographic]`

```
"views by age group"
"engagement for 18-24"
"male vs female viewers"
"demographics for my channel"
```

---

## 🎯 Query by Intent

### "I want to know if my latest video is doing well"
```
→ "Give me the views accumulated by my most recent post"
→ "How is my latest video performing?"
→ "Show me engagement on my last upload"
```

### "I want to understand my audience"
```
→ "Where are my viewers from?"
→ "What's my audience demographic breakdown?"
→ "Show me age and gender of my viewers"
→ "What devices do people watch on?"
```

### "I want to track growth"
```
→ "How many subscribers did I gain this week?"
→ "Show me subscriber growth over time"
→ "Compare this month to last month"
→ "What's my growth trend?"
```

### "I want to optimize content"
```
→ "Which videos get the most engagement?"
→ "What's my average view duration?"
→ "Where does my traffic come from?"
→ "Which topics perform best?"
```

### "I want to analyze traffic"
```
→ "How many views from YouTube search?"
→ "What are my top traffic sources?"
→ "How effective are my thumbnails?"
→ "External vs internal traffic?"
```

### "I want to check revenue" (monetized channels)
```
→ "What's my revenue this month?"
→ "How much did I earn from ads?"
→ "What's my CPM?"
→ "Show me revenue by video"
```

---

## 🔥 Power User Queries

### Multi-Dimensional Analysis
```
"Show me views by country and device type"
"Compare engagement metrics across age groups"
"Daily views from mobile users in the US"
"Traffic sources for my top 5 videos"
```

### Complex Time Ranges
```
"Compare Q4 2023 to Q4 2024"
"Show me performance for the last 90 days"
"Week-over-week growth for January"
"Year-to-date totals"
```

### Filtered Analysis
```
"Views from subscribers only"
"Mobile views for my latest video"
"Engagement from 18-24 age group"
"Traffic from external sources"
```

### Trend Analysis
```
"Is my channel growing or declining?"
"Show me my growth trajectory"
"Identify my peak performance periods"
"Find my best performing day of the week"
```

---

## 💡 Tips for Great Queries

### ✅ DO:
- Be specific about time periods: "last 7 days", "this month", "yesterday"
- Mention specific metrics: "views", "watch time", "subscribers"
- Use natural language: "How many...", "Show me...", "What's my..."
- Ask follow-up questions in the same session

### ❌ DON'T:
- Be too vague: "How am I doing?" → "How did I do this week?"
- Use API terminology unless you know it: Better to say "views" than "metrics"
- Ask multiple unrelated questions at once
- Expect real-time data (there's a 24-48 hour delay)

---

## 🧪 Test Queries

Use these to test your system:

```python
# Test 1: Recent post views
"Give me the views accumulated by my most recent post"

# Test 2: Daily trend
"Show me my daily views for the last 30 days"

# Test 3: Geographic
"Where are my viewers from?"

# Test 4: Subscribers
"How many subscribers did I gain yesterday?"

# Test 5: Top content
"What are my top 5 videos this week?"

# Test 6: Traffic
"Where is my traffic coming from?"

# Test 7: Demographics
"What's my audience age breakdown?"

# Test 8: Engagement
"What's my average view duration?"

# Test 9: Comparison
"Compare views from US vs UK"

# Test 10: Complex
"Show me mobile views by country for my latest video"
```

---

## 📱 API Testing

### Via API Endpoint
```bash
POST http://localhost:8000/agents/general-query
Content-Type: application/json

{
  "query": "Give me the views accumulated by my most recent post"
}
```

### Via Python
```python
from app.agents.agent_runner import call_agent_async, get_runner
from app.agents.main_agent import coordinator_agent

runner = get_runner("test_app", coordinator_agent)
response = await call_agent_async(
    query="Show me my daily views for the last week",
    runner=runner,
    user_id="user_1",
    session_id="session_001"
)
```

### Via CLI
```bash
cd Tubentor/backend
python -m app.agents.agent_runner
# Enter queries interactively
```

---

## 🎓 Learning Path

### Beginner Queries
Start with these simple queries:
1. "Show me my channel statistics"
2. "What's my most recent video?"
3. "How many subscribers do I have?"

### Intermediate Queries
Then try these:
1. "Show me my views for the last 7 days"
2. "Which video got the most views this week?"
3. "Where are my viewers from?"

### Advanced Queries
Finally, experiment with:
1. "Compare my performance by country and device type"
2. "Show me subscriber growth trends by traffic source"
3. "Analyze engagement patterns for different demographics"

---

## 🔍 Troubleshooting

### Query Not Working?
- ✓ Be more specific about the time period
- ✓ Make sure you're asking about your own channel
- ✓ Check if you're using correct video IDs
- ✓ Verify your API credentials are set up

### Getting Errors?
- ✓ Check API quota hasn't been exceeded
- ✓ Verify dates are recent (analytics need 24-48 hours)
- ✓ Make sure channel is eligible for requested metrics
- ✓ Check logs for detailed error messages

### Results Don't Look Right?
- ✓ Remember there's a 24-48 hour delay for analytics
- ✓ Verify the time zone interpretation
- ✓ Check if you're looking at the right metric
- ✓ Compare with YouTube Studio to validate

---

## 📚 Additional Resources

- **Full Capabilities:** See `DYNAMIC_QUERY_CAPABILITIES.md`
- **Architecture:** See `AGENT_ARCHITECTURE.md`
- **Examples:** See `USAGE_EXAMPLES.md`
- **YouTube Analytics API:** [Official Docs](https://developers.google.com/youtube/analytics)
- **YouTube Data API:** [Official Docs](https://developers.google.com/youtube/v3)

---

## 🚀 Quick Start Checklist

- [ ] Set up YouTube API credentials (YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN)
- [ ] Start the agent system
- [ ] Try: "Show me my channel statistics"
- [ ] Try: "Give me the views accumulated by my most recent post"
- [ ] Try: "Where are my viewers from?"
- [ ] Experiment with your own queries!

---

**Remember:** The agent can handle ANY YouTube-related query. If you can think it, you can ask it! 🎉

