import datetime as dt
import requests as rq
import os
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

coordinates = ("49.8383", "24.0232")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q="

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def weather_by_city(city: str) -> dict:
    """Returns the weather for provided city
       
       Args: 
            city: city for which weather is looked for. e.g. Kyiv    
    """
    url = BASE_URL + city + f"&appid={WEATHER_API_KEY}"
    response = rq.get(url).json()
    temp_kelvin = response["main"]["temp"]
    temp_celsius = f"{round(kelvin_to_celsius(temp_kelvin))} \u00B0C"

    feels_like_kelvin = response["main"]["feels_like"]
    feels_like_celsius = f"{round(kelvin_to_celsius(feels_like_kelvin))} \u00B0C"

    humidity = f"{response["main"]["humidity"]}%"
    description = response["weather"][0]["description"]

    dt_sunrise = dt.datetime.fromtimestamp(response["sys"]["sunrise"] + response["timezone"], dt.timezone.utc)
    dt_sunset = dt.datetime.fromtimestamp(response["sys"]["sunset"] + response["timezone"],  dt.timezone.utc)
    date = dt_sunrise.strftime("%d.%m")
    sunrise = dt_sunrise.strftime("%H:%M:%S AM")
    sunset = dt_sunset.strftime("%H:%M:%S PM")

    wind_speed = f"{response["wind"]["speed"]} m/s"

    return {
        "city": city,
        "date": date,
        "temperature": temp_celsius,
        "feels_like": feels_like_celsius,
        "humidity": humidity,
        "description": description,
        "sunrise": sunrise,
        "sunset": sunset,
        "wind_speed": wind_speed
    }