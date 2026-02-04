import os
import requests
from typing import Dict, Any

class WeatherTool:
    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city: str) -> Dict[str, Any]:
        """Get current weather for a city"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            weather_info = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
            
            return {"success": True, "data": weather_info}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_forecast(self, city: str, days: int = 3) -> Dict[str, Any]:
        """Get weather forecast for a city"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "cnt": days * 8
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            forecasts = []
            
            for item in data["list"][:days * 8:8]:
                forecasts.append({
                    "date": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "description": item["weather"][0]["description"]
                })
            
            return {"success": True, "data": {"city": city, "forecast": forecasts}}
        
        except Exception as e:
            return {"success": False, "error": str(e)}