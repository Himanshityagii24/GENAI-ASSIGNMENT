from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
import uvicorn

app = FastAPI(
    title="AI Operations Assistant",
    description="Multi-agent system for processing natural language tasks with parallel execution, caching, and cost tracking",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
planner = PlannerAgent()
executor = ExecutorAgent()
verifier = VerifierAgent()

class TaskRequest(BaseModel):
    task: str

class TaskResponse(BaseModel):
    success: bool
    data: Dict[str, Any]

@app.get("/")
def root():
    """API information and available endpoints"""
    return {
        "name": "AI Operations Assistant",
        "version": "2.0.0",
        "description": "Multi-agent system with Planner, Executor, and Verifier",
        "features": [
            "Parallel execution of independent tasks",
            "API response caching",
            "Cost tracking per request",
            "Graceful fallback for partial data",
            "Retry logic with exponential backoff"
        ],
        "endpoints": {
            "/": "GET - API information",
            "/health": "GET - Health check",
            "/process": "POST - Process a natural language task",
            "/cache/clear": "POST - Clear API response cache",
            "/cache/stats": "GET - Get cache statistics",
            "/docs": "GET - Interactive API documentation"
        },
        "example_tasks": [
            "Find top 5 Python repositories on GitHub",
            "Get current weather in London",
            "Search for AI news",
            "Get info for facebook/react and weather in San Francisco"
        ]
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    cache_stats = executor.get_cache_stats()
    return {
        "status": "healthy",
        "agents": ["planner", "executor", "verifier"],
        "tools": ["github", "weather", "news"],
        "features": {
            "parallel_execution": True,
            "api_caching": True,
            "cost_tracking": True,
            "graceful_fallback": True
        },
        "cache": {
            "enabled": True,
            "entries": cache_stats["cached_entries"]
        }
    }

@app.post("/cache/clear")
def clear_cache():
    """Clear the API response cache"""
    executor.clear_cache()
    return {
        "success": True,
        "message": "Cache cleared successfully"
    }

@app.get("/cache/stats")
def cache_stats():
    """Get cache statistics"""
    stats = executor.get_cache_stats()
    return {
        "success": True,
        "stats": stats
    }

@app.post("/process", response_model=TaskResponse)
def process_task(request: TaskRequest):
    """
    Process a natural language task through the multi-agent system.
    
    Flow:
    1. Planner creates execution plan
    2. Executor runs the plan with parallel execution and caching
    3. Verifier validates and formats output
    
    Features:
    - Parallel execution of independent steps
    - API response caching to avoid duplicate calls
    - Cost tracking for each request
    - Graceful fallback when some steps fail
    - Retry logic with exponential backoff
    """
    try:
        user_task = request.task
        
        #  Planning
        plan_result = planner.create_plan(user_task)
        if not plan_result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=f"Planning failed: {plan_result.get('error')}"
            )
        
        plan = plan_result.get("plan")
        
        # Execution (with parallel execution, caching, and graceful fallback)
        execution_result = executor.execute_plan(plan)
        
       
        # Verification
        verification_result = verifier.verify_and_format(user_task, execution_result)
        if not verification_result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=f"Verification failed: {verification_result.get('error')}"
            )
        
       
        return TaskResponse(
            success=True,
            data={
                "plan": plan,
                "execution_summary": execution_result.get("summary"),
                "verified_output": verification_result.get("output"),
                "performance": {
                    "total_steps": execution_result.get("summary", {}).get("total_steps"),
                    "successful_steps": execution_result.get("summary", {}).get("successful_steps"),
                    "failed_steps": execution_result.get("summary", {}).get("failed_steps"),
                    "total_cost_usd": execution_result.get("summary", {}).get("total_cost")
                }
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)