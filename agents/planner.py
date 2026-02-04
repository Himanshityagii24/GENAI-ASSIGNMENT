import json
from typing import Dict, Any
from llm.llm_client import LLMClient

class PlannerAgent:
    """
    Planner Agent: Converts user input into a structured execution plan.
    Uses LLM to reason about required steps and tools.
    """
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    def create_plan(self, user_input: str) -> Dict[str, Any]:
        """Create an execution plan from user input"""
        
        system_prompt = """You are a task planning expert. Analyze user requests and create structured execution plans.

Available tools and their capabilities:

1. github
   - search_repositories: Search GitHub repos by query
     params: {"query": "search term", "max_results": 5}
   - get_repo_info: Get detailed info about a specific repo
     params: {"owner": "owner_name", "repo": "repo_name"}

2. weather
   - get_current_weather: Get current weather for a city
     params: {"city": "city_name"}
   - get_forecast: Get weather forecast
     params: {"city": "city_name", "days": 3}

3. news
   - get_top_headlines: Get top news headlines
     params: {"country": "us", "category": "technology", "max_results": 5}
   - search_news: Search for specific news
     params: {"query": "search term", "max_results": 5}

Create a plan as a JSON object with this exact structure:
{
  "steps": [
    {
      "step_number": 1,
      "action": "brief description",
      "tool": "tool_name",
      "parameters": {"param": "value"}
    }
  ]
}

Rules:
- Break complex tasks into simple steps
- Each step uses ONE tool
- Include all required parameters
- Order steps logically
- Return ONLY valid JSON, no explanation"""

        user_prompt = f"Task: {user_input}\n\nCreate the execution plan:"
        
        try:
            response = self.llm_client.generate(system_prompt, user_prompt)
            
            # Clean response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            
            plan = json.loads(response.strip())
            
            # Validate plan structure
            if "steps" not in plan or not isinstance(plan["steps"], list):
                return {"success": False, "error": "Invalid plan structure"}
            
            return {"success": True, "plan": plan}
            
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON from planner: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Planning failed: {str(e)}"}