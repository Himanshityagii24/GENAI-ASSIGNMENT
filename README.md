# AI Operations Assistant

Hey! This is a smart AI assistant that can handle tasks by breaking them down into steps and calling different APIs to get the job done.It as like  having three mini-agents working together.

## What Does It Do?

You give it a task in plain English, and it figures out what needs to be done. For example:
- "Find me the top Python repos on GitHub"
- "What's the weather like in New York?"
- "Get me some AI news"

It then creates a plan, executes it, and gives you back clean, organized results.

## How It Works

There are three agents doing the heavy lifting:

**Planner Agent** - The brain. It reads your request and figures out what steps are needed and which tools to use.

**Executor Agent** - The doer. It takes the plan and actually calls the APIs (GitHub, Weather, News). If something fails, it'll retry a few times before giving up.

**Verifier Agent** - The quality checker. It looks at all the results, makes sure nothing's missing, and formats everything nicely for you.

## What's Inside?

The project uses three different APIs:
- **GitHub** - Search repos, get repo details
- **Weather** - Current weather and forecasts for any city
- **News** - Latest headlines and article searches

Everything's powered by OpenAI's GPT-3.5 for the thinking parts.

## Getting Started
## Deployed Link- You can directly check the working of AI Operations Assistant here 
 
### What You'll Need

- Python 3.8 or newer
- API keys for OpenAI, GitHub, OpenWeatherMap, and NewsAPI

### Setting It Up
```bash
# Get the code
git clone https://github.com/Himanshityagii24/GENAI-ASSIGNMENT

#Go to the directory
cd GENAI-ASSIGNMENT

# Set up a virtual environment
python -m venv venv

# Turn it on
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install everything
pip install -r requirements.txt
```

### Add Your API Keys

Create a file called `.env` in the main folder and add your keys:
```bash
OPENAI_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
WEATHER_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

Not sure where to get these? Check the `.env.example` file for links.

### Fire It Up
```bash
python main.py
```

Head over to `http://localhost:8000/docs` and you'll see an interactive playground where you can test everything.

## Try It Out
/process api
Here are some things you can ask it to do:

**GitHub Stuff:**
```json
{
  "task": "Find the top 5 machine learning repositories"
}
```
```json
{
  "task": "Get me info about the facebook/react repository"
}
```

**Weather:**
```json
{
  "task": "What's the weather in London right now?"
}
```
```json
{
  "task": "Give me a 3-day forecast for Tokyo"
}
```

**News:**
```json
{
  "task": "Find me news about SpaceX"
}
```
```json
{
  "task": "What are the top tech headlines today?"
}
```

**Mix It Up:**
```json
{
  "task": "Search for React repositories and tell me the weather in Seattle"
}
```

## The Endpoints

- `GET /` - Basic info about the API
- `GET /health` - Check if everything's running
- `POST /process` - Send your task here
- `GET /docs` - Interactive documentation (this is the fun one!)

## How Everything Flows
```
Your task
   ↓
Planner figures out the steps
   ↓
Executor runs them
   ↓
Verifier checks and formats
   ↓
You get clean results
```


## Things That Could Be Better

If I had more time, here's what I'd add:
- Cache API responses so we're not calling the same thing twice
- Track how much each request costs
- Run some tools in parallel to speed things up
- Add more APIs like Spotify, weather alerts, etc.

## What's Under the Hood
```
├── agents/           # The three main agents
├── tools/            # API integrations
├── llm/              # OpenAI client
├── main.py           # FastAPI app
└── requirements.txt  # Everything you need to install
```



## Tech Stack

- FastAPI for the web server
- OpenAI GPT-3.5 for the smart bits
- Pydantic for making sure data looks right
- Standard requests library for API calls



Made for the GenAI internship assignment. Hope you like it!