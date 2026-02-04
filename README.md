# AI Operations Assistant 

Hey there! This is a pretty cool AI assistant that can handle all sorts of tasks by breaking them down and hitting different APIs to get stuff done. It is  as having a mini team of AI agents working together to help you out.

## What's This All About?

You throw a task at it in plain English, and it figures out what needs to happen. No complicated commands or syntax – just talk to it like you would a person.

For example:
- "Find me the top Python repos on GitHub"
- "What's the weather like in New York?"
- "Get me some AI news"
- "Search for React repos AND tell me the weather in Seattle" (it'll do both at once!)

The system creates a plan, runs it, and gives you back clean, organized results. Simple as that.


Okay, so we've added some seriously cool upgrades:

** Parallel Execution** - Got multiple tasks? No problem. Instead of doing them one-by-one like a chump, it runs them at the same time. Like 2-3x faster for complex requests.

** Cost Tracking** - Every API call costs money (not much, but still). Now you can see exactly how much each request costs you. Great for keeping tabs on your spending.

** Smart Caching** - Why call the same API twice? If you ask the same question again, it pulls from cache. Instant responses, zero cost. Pretty neat.

** Graceful Fallback** - Here's the big one: if part of your request fails, the system doesn't just give up. It'll give you whatever it could successfully fetch and tell you what went wrong. Way better than getting nothing at all.

** Smarter Retries** - APIs sometimes hiccup. When they do, the system retries with exponential backoff (1s, 2s, 4s delays) instead of hammering the poor API server.

## How Does It Work?

There are three agents working behind the scenes:

### 1. Planner Agent 
The strategist. Reads your request and figures out:
- What needs to be done
- Which tools to use
- In what order

Think of it as the team leader making the game plan.

### 2. Executor Agent 
The action hero. Takes the plan and:
- Actually calls the APIs (GitHub, Weather, News)
- Runs independent tasks in parallel (new!)
- Caches responses to avoid duplicate calls (new!)
- Retries if something fails
- Keeps going even if some steps fail (new!)
- Tracks costs (new!)

### 3. Verifier Agent 
The quality control person. It:
- Checks all the results
- Makes sure nothing critical is missing
- Handles partial data gracefully (new!)
- Formats everything nicely for you

### Architecture Diagram
```
our Natural Language Request
           ↓
    ┌──────────────┐
    │   Planner    │ → Creates JSON execution plan
    │   (LLM)      │    using GPT-3.5
    └──────────────┘
           ↓
    ┌──────────────┐
    │   Executor   │ → Calls APIs in parallel
    │  (Parallel)  │   with caching & retries
    └──────────────┘
           ↓
    ┌──────────────┐
    │   Verifier   │ → Validates & formats
    │   (LLM)      │    (handles partial data)
    └──────────────┘
           ↓
    Clean, Structured Response
```

## What APIs Are Hooked Up?

Right now we've got three different APIs integrated:

**🐙 GitHub API**
- Search for repositories (by language, stars, etc.)
- Get detailed info about specific repos
- Fetch stars, forks, descriptions, all that good stuff

**🌤️ OpenWeatherMap API**
- Current weather for any city
- Multi-day forecasts
- Temperature, humidity, wind speed, you name it

**📰 NewsAPI**
- Latest headlines by country/category
- Search for specific news articles
- Sources, publish dates, everything



## Deployed Version 🌐

Check out the live demo: [https://genai-assignment-beryl.vercel.app/](https://genai-assignment-beryl.vercel.app/)



## Getting Started

### What You'll Need

- Python 3.8 or newer (3.10+ recommended)
- API keys (free tiers work fine for testing!)
  - OpenAI API key
  - GitHub Personal Access Token
  - OpenWeatherMap API key
  - NewsAPI key

### Installation Steps

```bash
# 1. Clone the repo
git clone https://github.com/Himanshityagii24/GENAI-ASSIGNMENT
cd GENAI-ASSIGNMENT

# 2. Set up a virtual environment 
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root directory with your API keys:

```bash
# OpenAI (for planning and verification)
OPENAI_API_KEY=sk-your-key-here

# GitHub (for repo searches and info)
GITHUB_TOKEN=ghp_your-token-here

# Weather (for weather data)
WEATHER_API_KEY=your-key-here

# News (for news articles)
NEWS_API_KEY=your-key-here
```

**Where to get these keys?** Check out `.env.example` for direct links to each API's signup page.

### Running Locally

```bash
python main.py
```

That's it! The server starts on `http://localhost:8000`

**Interactive Docs**: Head to `http://localhost:8000/docs` for a super slick interactive playground where you can test everything.

## Try These Out 🎯

Here are some example prompts to get you started:

### GitHub Queries
```json
{"task": "Find the top 5 machine learning repositories"}
```
```json
{"task": "Get me info about the tensorflow/tensorflow repository"}
```
```json
{"task": "Search for React repositories with over 10k stars"}
```

### Weather Queries
```json
{"task": "What's the weather in Tokyo right now?"}
```
```json
{"task": "Give me a 5-day forecast for London"}
```
```json
{"task": "How's the weather in San Francisco and Seattle?"}
```

### News Queries
```json
{"task": "Find me recent news about artificial intelligence"}
```
```json
{"task": "What are the top tech headlines today?"}
```
```json
{"task": "Search for news about SpaceX launches"}
```

### Complex Multi-Step Queries (Runs in Parallel! ⚡)
```json
{"task": "Get info for facebook/react, weather in Seattle, and latest AI news"}
```
```json
{"task": "Find Python repos, get weather in New York, and search for climate news"}
```
```json
{"task": "Search for Vue.js repositories and tell me the weather forecast for Paris"}
```

## Available Endpoints

- `GET /` - API info and documentation
- `GET /health` - Health check (includes cache stats)
- `POST /process` - Main endpoint - send your tasks here
- `POST /cache/clear` - Clear the response cache
- `GET /cache/stats` - See what's cached
- `GET /docs` - Interactive Swagger docs (use this!)


## Project Structure 📁

```
GENAI-ASSIGNMENT/
├── agents/
│   ├── planner.py         # Plans the execution strategy
│   ├── executor.py        # Executes with parallel processing & caching
│   └── verifier.py        # Verifies and formats results
├── tools/
│   ├── github_tool.py     # GitHub API integration
│   ├── weather_tool.py    # Weather API integration
│   └── news_tool.py       # News API integration
├── llm/
│   └── llm_client.py      # OpenAI client wrapper
├── main.py                # FastAPI application
├── requirements.txt       # Python dependencies
├── .env                   # Your API keys (don't commit this!)
├── .env.example          # Template for API keys
└── README.md             # You are here!
```

### What Could Be Better

If we had more time , here's what would make it even cooler:

- **Persistent caching** with Redis or database
- **Streaming responses** for real-time updates
- **More APIs** (Spotify, Twitter, Slack, you name it)
- **User authentication** and rate limiting per user
- **Webhook support** for long-running tasks
- **Better error messages** with suggestions on how to fix things
- **Request queue** for handling high load
- **Monitoring dashboard** to see performance metrics
- **Actual API usage tracking** from provider dashboards
- **Smart dependency resolution** for truly complex multi-step workflows

## Tech Stack 

- **FastAPI** - Modern Python web framework (super fast!)
- **OpenAI GPT-3.5-turbo** - For natural language understanding
- **Pydantic** - Data validation and settings management
- **Requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management
- **ThreadPoolExecutor** - For parallel execution (built into Python!)


## Example Response Structure

Here's what you get back:

```json
{
  "success": true,
  "data": {
    "plan": {
      "steps": [/* execution plan */]
    },
    "execution_summary": {
      "total_steps": 2,
      "successful_steps": 2,
      "failed_steps": 0,
      "total_cost": 0.015
    },
    "verified_output": {
      "status": "complete",  // or "partial" or "failed"
      "summary": "Successfully retrieved...",
      "data": [/*  actual results */],
      "missing": [],
      "failed_steps": []
    },
    "performance": {
      "total_steps": 2,
      "successful_steps": 2,
      "failed_steps": 0,
      "total_cost_usd": 0.015
    }
  }
}
```




