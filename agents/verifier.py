import json
from typing import Dict, Any
from llm.llm_client import LLMClient

class VerifierAgent:
    """
    Verifier Agent: Validates execution results and formats final output.
    Ensures completeness and data quality.
    """
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    def verify_and_format(self, user_input: str, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Verify execution results and create final structured output"""
        
        system_prompt = """You are a verification and formatting expert. Review execution results and create a final structured response.

Your tasks:
1. Check if all steps completed successfully
2. Extract and organize relevant data
3. Identify any missing or incomplete information
4. Provide a clear, concise summary

Return a JSON object with this structure:
{
  "status": "complete" or "incomplete",
  "summary": "brief summary of what was accomplished",
  "data": [extracted relevant data from results],
  "missing": ["list of any missing information, empty array if none"]
}

Return ONLY valid JSON, no explanation."""

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
            # Fallback: create basic verification if LLM output is invalid
            return self._create_fallback_verification(execution_results)
        except Exception as e:
            return {"success": False, "error": f"Verification failed: {str(e)}"}
    
    def _create_fallback_verification(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create a basic verification when LLM parsing fails"""
        results = execution_results.get("results", [])
        all_success = all(r.get("result", {}).get("success", False) for r in results)
        
        data = []
        for result in results:
            if result.get("result", {}).get("success"):
                data.append(result.get("result", {}).get("data"))
        
        return {
            "success": True,
            "output": {
                "status": "complete" if all_success else "incomplete",
                "summary": f"Executed {len(results)} steps",
                "data": data,
                "missing": [] if all_success else ["Some steps failed"]
            }
        }