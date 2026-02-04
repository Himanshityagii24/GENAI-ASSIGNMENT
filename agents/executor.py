import time
import asyncio
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from tools.github_tool import GitHubTool
from tools.weather_tool import WeatherTool
from tools.news_tool import NewsTool

class ExecutorAgent:
    """
    Executor Agent: Executes the plan by calling appropriate tools.
    Features:
    - Parallel execution of independent steps
    - Retry logic with exponential backoff
    - Graceful fallback for partial data
    - API response caching
    - Cost tracking per request
    """
    
    def __init__(self):
        self.github_tool = GitHubTool()
        self.weather_tool = WeatherTool()
        self.news_tool = NewsTool()
        self.max_retries = 3
        self.retry_delay = 1
        
        # API Response Cache
        self.cache = {}
        
        # Cost tracking (example costs per API call)
        self.api_costs = {
            "github": 0.01,
            "weather": 0.005,
            "news": 0.008
        }
        self.request_cost = 0
    
    def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute all steps in the plan with parallel execution and graceful fallback"""
        results = []
        steps = plan.get("steps", [])
        self.request_cost = 0  # Reset cost for this request
        
        # Group steps by dependencies for parallel execution
        step_groups = self._group_steps_for_parallel_execution(steps)
        
        for group in step_groups:
            # Execute steps in parallel within each group
            group_results = self._execute_steps_in_parallel(group)
            results.extend(group_results)
        
        # Calculate success rate
        successful_steps = sum(1 for r in results if r.get("result", {}).get("success"))
        total_steps = len(results)
        
        return {
            "success": True,
            "results": results,
            "summary": {
                "total_steps": total_steps,
                "successful_steps": successful_steps,
                "failed_steps": total_steps - successful_steps,
                "total_cost": round(self.request_cost, 3)
            }
        }
    
    def _group_steps_for_parallel_execution(self, steps: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """
        Group steps that can be executed in parallel.
        For simplicity, all steps at the same level can run in parallel.
        In a more complex system, you'd check for data dependencies.
        """
        # Simple implementation: execute all steps in parallel
        # In production, you'd analyze dependencies between steps
        return [steps]
    
    def _execute_steps_in_parallel(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute multiple steps in parallel using ThreadPoolExecutor"""
        results = []
        
        with ThreadPoolExecutor(max_workers=min(len(steps), 5)) as executor:
            # Submit all steps for execution
            future_to_step = {
                executor.submit(self._execute_step_with_retry, step): step
                for step in steps
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_step):
                step = future_to_step[future]
                try:
                    step_result = future.result()
                    results.append({
                        "step_number": step.get("step_number"),
                        "action": step.get("action"),
                        "result": step_result
                    })
                except Exception as e:
                    # Graceful fallback: continue execution even if a step fails
                    results.append({
                        "step_number": step.get("step_number"),
                        "action": step.get("action"),
                        "result": {
                            "success": False,
                            "error": f"Exception during execution: {str(e)}"
                        }
                    })
        
        # Sort results by step number
        results.sort(key=lambda x: x.get("step_number", 0))
        return results
    
    def _execute_step_with_retry(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step with retry logic and exponential backoff"""
        for attempt in range(self.max_retries):
            try:
                # Check cache first
                cache_key = self._get_cache_key(step)
                if cache_key in self.cache:
                    cached_result = self.cache[cache_key]
                    cached_result["cached"] = True
                    return cached_result
                
                # Execute the step
                result = self._execute_step(step)
                
                if result.get("success"):
                    # Cache successful results
                    self.cache[cache_key] = result
                    
                    # Track cost
                    tool = step.get("tool")
                    self.request_cost += self.api_costs.get(tool, 0)
                    
                    return result
                
                # Retry on failure with exponential backoff
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    time.sleep(wait_time)
                    
            except Exception as e:
                if attempt == self.max_retries - 1:
                    # Graceful fallback: return error but don't stop execution
                    return {
                        "success": False,
                        "error": str(e),
                        "graceful_fallback": True
                    }
                # Exponential backoff
                wait_time = self.retry_delay * (2 ** attempt)
                time.sleep(wait_time)
        
        return {
            "success": False,
            "error": "Max retries exceeded",
            "graceful_fallback": True
        }
    
    def _get_cache_key(self, step: Dict[str, Any]) -> str:
        """Generate a unique cache key for a step"""
        tool = step.get("tool", "")
        action = step.get("action", "")
        params = str(sorted(step.get("parameters", {}).items()))
        return f"{tool}:{action}:{params}"
    
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
    
    def clear_cache(self):
        """Clear the response cache"""
        self.cache = {}
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "cached_entries": len(self.cache),
            "cache_keys": list(self.cache.keys())
        }