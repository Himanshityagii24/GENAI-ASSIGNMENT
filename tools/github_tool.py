import os
import requests
from typing import Dict, Any

class GitHubTool:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def search_repositories(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Search GitHub repositories"""
        try:
            url = f"{self.base_url}/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": max_results
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            repos = []
            
            for item in data.get("items", []):
                repos.append({
                    "name": item["name"],
                    "full_name": item["full_name"],
                    "description": item["description"],
                    "stars": item["stargazers_count"],
                    "language": item["language"],
                    "url": item["html_url"]
                })
            
            return {"success": True, "data": repos}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get detailed repository information"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            repo_info = {
                "name": data["name"],
                "full_name": data["full_name"],
                "description": data["description"],
                "stars": data["stargazers_count"],
                "forks": data["forks_count"],
                "language": data["language"],
                "open_issues": data["open_issues_count"],
                "url": data["html_url"]
            }
            
            return {"success": True, "data": repo_info}
        
        except Exception as e:
            return {"success": False, "error": str(e)}