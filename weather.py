# weather.py

import argparse
import json
import sys
import time
import csv
from datetime import datetime
from configparser import ConfigParser
from urllib import error, parse, request

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
PADDING = 20


def build_weather_query(city_input, imperial=False):
    api_key = _get_api_key()
    url_encoded_city_name = city_input
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url


def _get_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]


def get_weather_data(query_url):
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401:  # 401 - Unauthorized
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404:  # 404 - Not Found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong... ({http_error.code})")

    data = response.read()

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't read the server response.")


def display_weather_info(weather_data, imperial=False):
    now = datetime.now()
    dateTime_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M:%S")

    city = weather_data["name"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]

    print(f"{dateTime_string:^{PADDING}}", end="")
    print(f"{time_string:^{PADDING}}", end="")
    print(f"{city:^{PADDING}}", end="")
    print(
        f"\t{weather_description.capitalize():^{PADDING}}",
        end=" ",
    )
    print(f"{temperature}°{'F' if imperial else 'C'}", end=" ")
    print(f"{humidity}%")

    with open("weather.csv", "a", newline="") as f:
        writer = csv.writer(f)
        # writer.writerow(["Date", "Time", "Location", "Weather", "Temperature", "Humidity"])
        writer.writerow([dateTime_string, time_string, city, weather_description, temperature, humidity])

def simple_output(location):
    query_url = build_weather_query(location, "-i")
    weather_data = get_weather_data(query_url)
    display_weather_info(weather_data)


if __name__ == "__main__":
    user_args = ["Dallas", "Lusaka", "Miami", "Austin", "Houston", "London"]

    for x in range(1):
        for x in user_args:
            simple_output(x)
        time.sleep(1)