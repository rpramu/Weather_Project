import requests
from typing import Dict, Optional
import os
from dotenv import load_dotenv
load_dotenv()





def get_weather_data(city: str, api_key: str, units = "metric") -> Optional[Dict]:
    """
    Fetch weather data from OpenWeatherMap API for a given city.
    
    Args:
        city (str): Name of the city to get weather data for
        api_key (str): Your OpenWeatherMap API key
        
    Returns:
        Optional[Dict]: Dictionary containing main weather condition, temperature,
                       and feels like temperature. Returns None if request fails.
    """
    base_url = os.getenv("OPEN_WEATHERMAP_URL")
    
    params = {
        'q': city,
        'appid': api_key,
        'units': units,
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        weather_info = {
            'main': data['weather'][0]['main'],
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
        }
        
        return weather_info
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing response: {e}")
        return None






