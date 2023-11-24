# weather.py
import argparse
import json
import sys
from configparser import ConfigParser
from urllib import parse, request, request

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_api_key():
    """Fetch the API key from your configuration file.

    Expects a configuration file named "secrets.ini" with structure:

        [openweather]
        api_key=<YOUR-OPENWEATHER-API-KEY>
    """
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]


def read_user_cli_args():
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
    """
    Builds the URL for an API request to OpenWeather's weather API.
    Returns: sr: URL formatted for a call to OpenWeather's city name endpoint
    """
    api_key = get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid{api_key}"
    )
    return url


def get_weather_data(query_url):
    response = request.urlopen(query_url)
    data = response.read()
    return json.loads(data)




if __name__ == "__main__":
    user_args = read_user_cli_args()
    query_url = build_weather_query(user_args.city, user_args.imperial)
    weather_data = get_weather_data(query_url)
    print(weather_data)