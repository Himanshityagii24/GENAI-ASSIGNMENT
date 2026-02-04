import os
import requests
from typing import Dict, Any

class NewsTool:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
    
    def get_top_headlines(self, country: str = "us", category: str = None, max_results: int = 5) -> Dict[str, Any]:
        """Get top news headlines"""
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                "apiKey": self.api_key,
                "country": country,
                "pageSize": max_results
            }
            
            if category:
                params["category"] = category
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for article in data.get("articles", []):
                articles.append({
                    "title": article["title"],
                    "description": article["description"],
                    "source": article["source"]["name"],
                    "url": article["url"],
                    "published_at": article["publishedAt"]
                })
            
            return {"success": True, "data": articles}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_news(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Search for news articles"""
        try:
            url = f"{self.base_url}/everything"
            params = {
                "apiKey": self.api_key,
                "q": query,
                "sortBy": "relevancy",
                "pageSize": max_results
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for article in data.get("articles", []):
                articles.append({
                    "title": article["title"],
                    "description": article["description"],
                    "source": article["source"]["name"],
                    "url": article["url"],
                    "published_at": article["publishedAt"]
                })
            
            return {"success": True, "data": articles}
        
        except Exception as e:
            return {"success": False, "error": str(e)}