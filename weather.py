# weather.py

import argparse
import json
import sys
import time
from configparser import ConfigParser
from urllib import error, parse, request

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
PADDING = 20

def read_user_cli_args():
    """Handles the CLI user interactions.

    Returns:
        argparse.Namespace: Populated namespace object
    """
    parser = argparse.ArgumentParser(
        description="gets weather and temperature information for a city"
    )
    parser.add_argument(
        "city", nargs="+", type=str, help="enter the city name"
    )
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial units",
    )
    return parser.parse_args()


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
    """Fetch the API key from your configuration file.

    Expects a configuration file named "secrets.ini" with structure:

        [openweather]
        api_key=<YOUR-OPENWEATHER-API-KEY>
    """
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
    city = weather_data["name"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]

    print(f"{city:^{PADDING}}", end="")
    print(
        f"\t{weather_description.capitalize():^{PADDING}}",
        end=" ",
    )
    print(f"{temperature}°{'F' if imperial else 'C'}", end=" ")
    print(f"{humidity}%")


if __name__ == "__main__":
    # user_args = read_user_cli_args()
    user_args = ["Dallas", "Lusaka", "Miami", "Austin", "Houston", "London"]
    print(user_args)
    print(type(user_args))
    # user_args = "new york"

    for x in user_args:
        query_url = build_weather_query(x, "-i")
        weather_data = get_weather_data(query_url)
        # print(weather_data)
        display_weather_info(weather_data)
        # print(x)
        time.sleep(1)