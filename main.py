from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
import uvicorn

app = FastAPI(
    title="AI Operations Assistant",
    description="Multi-agent system for processing natural language tasks",
    version="1.0.0"
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
        "version": "1.0.0",
        "description": "Multi-agent system with Planner, Executor, and Verifier",
        "endpoints": {
            "/": "GET - API information",
            "/health": "GET - Health check",
            "/process": "POST - Process a natural language task",
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
    return {
        "status": "healthy",
        "agents": ["planner", "executor", "verifier"],
        "tools": ["github", "weather", "news"]
    }

@app.post("/process", response_model=TaskResponse)
def process_task(request: TaskRequest):
    """
    Process a natural language task through the multi-agent system.
    
    Flow::
    1. Planner creates execution plan
    2. Executor runs the plan and calls APIs
    3. Verifier validates and formats output
    """
    try:
        user_task = request.task
        
        #Planning
        plan_result = planner.create_plan(user_task)
        if not plan_result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=f"Planning failed: {plan_result.get('error')}"
            )
        
        plan = plan_result.get("plan")
        
        #Execution
        execution_result = executor.execute_plan(plan)
        if not execution_result.get("success"):
            raise HTTPException(
                status_code=500,
                detail="Execution failed"
            )
        
        #Verification
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
                "execution": execution_result,
                "verified_output": verification_result.get("output")
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)