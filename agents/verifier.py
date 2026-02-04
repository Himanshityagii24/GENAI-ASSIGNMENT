import json
from typing import Dict, Any
from llm.llm_client import LLMClient

class VerifierAgent:
    """
    Verifier Agent: Validates execution results and formats final output.
    Ensures completeness and data quality.
    Features:
    - Handles partial/incomplete data gracefully
    - Identifies missing information
    - Provides clear status indicators
    """
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    def verify_and_format(self, user_input: str, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Verify execution results and create final structured output"""
        
        system_prompt = """You are a verification and formatting expert. Review execution results and create a final structured response.

Your tasks:
1. Check which steps completed successfully and which failed
2. Extract and organize relevant data from successful steps
3. Identify any missing or incomplete information
4. Provide a clear, concise summary that acknowledges both successes and failures
5. If some steps failed, still present the available data

Return a JSON object with this structure:
{
  "status": "complete" (all steps succeeded) or "partial" (some steps failed) or "failed" (all steps failed),
  "summary": "brief summary acknowledging what was accomplished and what failed",
  "data": [extracted relevant data from successful results only],
  "missing": ["list of any missing information or failed steps"],
  "failed_steps": [{"step_number": N, "action": "description", "error": "error message"}]
}

IMPORTANT:
- For "partial" status, include both successful data and failed step information
- Don't ignore successful results just because some steps failed
- Provide a helpful summary that guides the user on what data is available
- Return ONLY valid JSON, no explanation."""

        user_prompt = f"""Original user request: {user_input}

Execution results:
{json.dumps(execution_results, indent=2)}

Verify and format the final output:"""
        
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
            
            verified_output = json.loads(response.strip())
            
            return {"success": True, "output": verified_output}
            
        except json.JSONDecodeError as e:
            # Fallback - create basic verification if LLM output is invalid
            return self._create_fallback_verification(execution_results)
        except Exception as e:
            return {"success": False, "error": f"Verification failed: {str(e)}"}
    
    def _create_fallback_verification(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create a basic verification when LLM parsing fails - handles partial data"""
        results = execution_results.get("results", [])
        
        successful_results = []
        failed_results = []
        
        for result in results:
            if result.get("result", {}).get("success"):
                successful_results.append(result)
            else:
                failed_results.append(result)
        
        # Extract data from successful steps
        data = []
        for result in successful_results:
            result_data = result.get("result", {}).get("data")
            if result_data:
                data.append(result_data)
        
        # Determine status
        if len(failed_results) == 0:
            status = "complete"
            summary = f"Successfully executed all {len(results)} steps"
        elif len(successful_results) == 0:
            status = "failed"
            summary = f"All {len(results)} steps failed"
        else:
            status = "partial"
            summary = f"Completed {len(successful_results)} of {len(results)} steps successfully"
        
       
        failed_steps = []
        for result in failed_results:
            failed_steps.append({
                "step_number": result.get("step_number"),
                "action": result.get("action"),
                "error": result.get("result", {}).get("error", "Unknown error")
            })
        
       
        missing = []
        if failed_results:
            missing = [f"Step {r.get('step_number')}: {r.get('action')}" for r in failed_results]
        
        return {
            "success": True,
            "output": {
                "status": status,
                "summary": summary,
                "data": data,
                "missing": missing,
                "failed_steps": failed_steps
            }
        }