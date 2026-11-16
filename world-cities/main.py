from flask import Flask, render_template
import requests
import pytz
from datetime import datetime

app = Flask(__name__)

# ----------------------------------------------------------------
# HOW TO GET YOUR API KEY:
# 1. Go to https://openweathermap.org/
# 2. Sign up for a free account
# 3. Go to API Keys section in your profile
# 4. Copy your key and paste it below
# ----------------------------------------------------------------
WEATHER_API_KEY = "YOUR_API_KEY_HERE"

# Cities to display — add or remove as you like
CITIES = [
    {"name": "London",       "country": "GB", "timezone": "Europe/London"},
    {"name": "New York",     "country": "US", "timezone": "America/New_York"},
    {"name": "Tokyo",        "country": "JP", "timezone": "Asia/Tokyo"},
    {"name": "Istanbul",     "country": "TR", "timezone": "Europe/Istanbul"},
    {"name": "Sydney",       "country": "AU", "timezone": "Australia/Sydney"},
    {"name": "Dubai",        "country": "AE", "timezone": "Asia/Dubai"},
    {"name": "Paris",        "country": "FR", "timezone": "Europe/Paris"},
    {"name": "New York",     "country": "US", "timezone": "America/Los_Angeles"},
]

# Fix duplicates — replace Los Angeles entry
CITIES = [
    {"name": "London",       "country": "GB", "timezone": "Europe/London"},
    {"name": "New York",     "country": "US", "timezone": "America/New_York"},
    {"name": "Tokyo",        "country": "JP", "timezone": "Asia/Tokyo"},
    {"name": "Istanbul",     "country": "TR", "timezone": "Europe/Istanbul"},
    {"name": "Sydney",       "country": "AU", "timezone": "Australia/Sydney"},
    {"name": "Dubai",        "country": "AE", "timezone": "Asia/Dubai"},
    {"name": "Paris",        "country": "FR", "timezone": "Europe/Paris"},
    {"name": "Los Angeles",  "country": "US", "timezone": "America/Los_Angeles"},
    {"name": "Singapore",    "country": "SG", "timezone": "Asia/Singapore"},
    {"name": "São Paulo",    "country": "BR", "timezone": "America/Sao_Paulo"},
    {"name": "Cairo",        "country": "EG", "timezone": "Africa/Cairo"},
    {"name": "Mumbai",       "country": "IN", "timezone": "Asia/Kolkata"},
]


def get_weather(city_name, country_code):
    """Fetch weather data from OpenWeatherMap API."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f"{city_name},{country_code}",
        "appid": WEATHER_API_KEY,
        "units": "metric",   # Celsius — change to "imperial" for Fahrenheit
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "humidity": data["main"]["humidity"],
            "wind": round(data["wind"]["speed"]),
        }
    except Exception:
        # If API key not set yet or request fails, return placeholder data
        return {
            "temp": "--",
            "feels_like": "--",
            "description": "Add your API key",
            "icon": "01d",
            "humidity": "--",
            "wind": "--",
        }


def get_local_time(timezone_str):
    """Get the current local time for a given timezone."""
    tz = pytz.timezone(timezone_str)
    local_time = datetime.now(tz)
    return local_time.strftime("%H:%M"), local_time.strftime("%A, %d %b %Y")


@app.route("/")
def home():
    city_data = []
    for city in CITIES:
        weather = get_weather(city["name"], city["country"])
        time_str, date_str = get_local_time(city["timezone"])
        city_data.append({
            "name": city["name"],
            "country": city["country"],
            "time": time_str,
            "date": date_str,
            "weather": weather,
        })
    return render_template("index.html", cities=city_data)


if __name__ == "__main__":
    app.run(debug=True)
