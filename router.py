from fastapi import FastAPI, HTTPException
from open_weathermap_sample import get_weather_data
import os
import json



app = FastAPI()


@app.get("/weather/{city}")
def read_weather(city: str):
    API_KEY = os.getenv("OPEN_WEATHERMAP_API_KEY")
    weather_data = get_weather_data(city, API_KEY)
    if weather_data:
        return {
            "city": city,
            "main": weather_data['main'],
            "temperature": weather_data['temp'],
            "feels_like": weather_data['feels_like'],
            "humidity": weather_data['humidity'],
            "pressure": weather_data['pressure']

        }
    else:
        raise HTTPException(status_code=404, detail="Weather data not found")
    





@app.get("/weatherof/{city}/{units}")
def read_weather_with_units(city: str, units: str):
    API_KEY = os.getenv("OPEN_WEATHERMAP_API_KEY")
    weather_data = get_weather_data(city, API_KEY, units=units)
    if weather_data:
        return {
            "city": city,
            "main": weather_data['main'],
            "temperature": weather_data['temp'],
            "feels_like": weather_data['feels_like'],
            "humidity": weather_data['humidity']
        }
    else:
        raise HTTPException(status_code=404, detail="Weather data not found")









if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    

