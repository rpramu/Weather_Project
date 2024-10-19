import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
import aiohttp
import json
from dataclasses import dataclass
from redis import Redis
from config import Config




@dataclass
class WeatherData:
    city_id: int
    city_name: str
    timestamp: int
    temperature: float
    feels_like: float
    weather_condition: str
    raw_data: dict

class DataCollectorService:
    def __init__(self, config: Config, redis_client: Redis):
        self.api_key = config.OPENWEATHER_API_KEY
        self.cities = config.MONITORED_CITIES
        self.polling_interval = config.POLLING_INTERVAL
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.redis_client = redis_client
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(__name__)

    async def start(self):
        """Initialize and start the data collection process"""
        self.session = aiohttp.ClientSession()
        try:
            while True:
                await self.collect_weather_data()
                await asyncio.sleep(self.polling_interval)
        except Exception as e:
            self.logger.error(f"Error in data collection: {str(e)}")
        finally:
            await self.cleanup()

    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()

    async def collect_weather_data(self):
        """Collect weather data for all configured cities"""
        tasks = [self.fetch_city_weather(city) for city in self.cities]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"Failed to fetch weather: {str(result)}")
                continue
            
            if result:
                await self.process_weather_data(result)

    async def fetch_city_weather(self, city: Dict) -> Optional[WeatherData]:
        """Fetch weather data for a single city"""
        try:
            params = {
                'q': f"{city['name']},{city['country']}",
                'appid': self.api_key,
                'units': 'metric' 
            }
            
            async with self.session.get(self.base_url, params=params) as response:
                if response.status != 200:
                    self.logger.error(f"API error for {city['name']}: {response.status}")
                    return None
                
                data = await response.json()
                return WeatherData(
                    city_id=city['id'],
                    city_name=city['name'],
                    timestamp=data['dt'],
                    temperature=data['main']['temp'],
                    feels_like=data['main']['feels_like'],
                    weather_condition=data['weather'][0]['main'],
                    raw_data=data
                )

        except Exception as e:
            self.logger.error(f"Error fetching data for {city['name']}: {str(e)}")
            return None

    async def process_weather_data(self, weather_data: WeatherData):
        """Process and store the collected weather data"""
        try:
            # Store the latest data in Redis for quick access
            redis_key = f"weather:{weather_data.city_id}:latest"
            self.redis_client.setex(
                redis_key,
                3600,  # expire after 1 hour
                json.dumps(weather_data.__dict__)
            )

            # Publish the data for real-time consumers
            self.redis_client.publish(
                'weather_updates',
                json.dumps({
                    'city_id': weather_data.city_id,
                    'city_name': weather_data.city_name,
                    'temperature': weather_data.temperature,
                    'weather_condition': weather_data.weather_condition,
                    'timestamp': weather_data.timestamp
                })
            )

            # Log successful data collection
            self.logger.info(
                f"Collected data for {weather_data.city_name}: "
                f"{weather_data.temperature}°C, {weather_data.weather_condition}"
            )

        except Exception as e:
            self.logger.error(f"Error processing weather data: {str(e)}")

class RateLimiter:
    """Rate limiter for API calls"""
    def __init__(self, calls_per_minute: int):
        self.calls_per_minute = calls_per_minute
        self.calls = []
        
    async def acquire(self):
        """Acquire permission to make an API call"""
        now = datetime.now().timestamp()
        self.calls = [t for t in self.calls if now - t < 60]
        
        if len(self.calls) >= self.calls_per_minute:
            wait_time = 60 - (now - self.calls[0])
            await asyncio.sleep(wait_time)
            
        self.calls.append(now)