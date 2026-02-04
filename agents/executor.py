import time
from typing import Dict, Any
from tools.github_tool import GitHubTool
from tools.weather_tool import WeatherTool
from tools.news_tool import NewsTool

class ExecutorAgent:
    """
    Executor Agent: Executes the plan by calling appropriate tools.
    Handles retries and error recovery.
    """
    
    def __init__(self):
        self.github_tool = GitHubTool()
        self.weather_tool = WeatherTool()
        self.news_tool = NewsTool()
        self.max_retries = 3
        self.retry_delay = 1
    
    def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute all steps in the plan"""
        results = []
        steps = plan.get("steps", [])
        
        for step in steps:
            step_result = self._execute_step_with_retry(step)
            results.append({
                "step_number": step.get("step_number"),
                "action": step.get("action"),
                "result": step_result
            })
            
            # Stop execution if a critical step fails
            if not step_result.get("success"):
                break
        
        return {"success": True, "results": results}
    
    def _execute_step_with_retry(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step with retry logic"""
        for attempt in range(self.max_retries):
            try:
                result = self._execute_step(step)
                
                if result.get("success"):
                    return result
                
                # Retry on failure
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return {"success": False, "error": str(e)}
                time.sleep(self.retry_delay)
        
        return {"success": False, "error": "Max retries exceeded"}
    
    def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step"""
        tool = step.get("tool")
        action = step.get("action", "")
        params = step.get("parameters", {})
        
        # Route to appropriate tool
        if tool == "github":
            return self._call_github_tool(action, params)
        elif tool == "weather":
            return self._call_weather_tool(action, params)
        elif tool == "news":
            return self._call_news_tool(action, params)
        else:
            return {"success": False, "error": f"Unknown tool: {tool}"}
    
    def _call_github_tool(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call GitHub tool based on action"""
        action_lower = action.lower()
        
        if "search" in action_lower:
            query = params.get("query", "")
            max_results = params.get("max_results", 5)
            return self.github_tool.search_repositories(query, max_results)
        
        elif "info" in action_lower or "get" in action_lower:
            owner = params.get("owner", "")
            repo = params.get("repo", "")
            return self.github_tool.get_repo_info(owner, repo)
        
        else:
            return {"success": False, "error": "Unknown GitHub action"}
    
    def _call_weather_tool(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call weather tool based on action"""
        city = params.get("city", "")
        
        if "forecast" in action.lower():
            days = params.get("days", 3)
            return self.weather_tool.get_forecast(city, days)
        else:
            return self.weather_tool.get_current_weather(city)
    
    def _call_news_tool(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call news tool based on action"""
        if "search" in action.lower():
            query = params.get("query", "")
            max_results = params.get("max_results", 5)
            return self.news_tool.search_news(query, max_results)
        else:
            country = params.get("country", "us")
            category = params.get("category")
            max_results = params.get("max_results", 5)
            return self.news_tool.get_top_headlines(country, category, max_results)