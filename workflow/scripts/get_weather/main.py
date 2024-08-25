import argparse
import datetime
import logging
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter, Retry
import yaml
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    95: "Thunderstorm",
}
OUTPUT_FILE = Path("results/weather_report.txt")

def validate_coordinates(latitude: float, longitude: float) -> bool:
    if -90 <= latitude <= 90 and -180 <= longitude <= 180:
        return True
    logger.error("Invalid latitude or longitude values")
    return False

def create_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session

def fetch_weather_data(session: requests.Session, latitude: float, longitude: float) -> Optional[dict]:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "timezone": "auto",
    }
    try:
        response = session.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logger.exception("Request to Open-Meteo API timed out")
    except requests.exceptions.TooManyRedirects:
        logger.exception("Too many redirects during API request")
    except requests.exceptions.RequestException as e:
        logger.exception("RequestException: Failed to fetch weather data: %s", e)
    except ValueError:
        logger.exception("JSON decoding failed for the response")
    return None

def parse_weather_data(data: dict) -> Optional[str]:
    if "current_weather" in data:
        temp_celsius = data["current_weather"]["temperature"]
        weather_code = data["current_weather"]["weathercode"]
        weather_description = WEATHER_DESCRIPTIONS.get(weather_code, "Unknown")
        output = (
            f"Current weather ({datetime.datetime.now(tz=datetime.UTC)}):"
            f" {temp_celsius:.1f}°C, {weather_description}"
        )
        logger.info("Output: %s", output)
        return output
    logger.error("Failed to fetch weather data")
    return None

def get_weather(latitude: float, longitude: float) -> Optional[str]:
    logger.info("Fetching weather data for [lat: %f, long: %f]", latitude, longitude)

    if not validate_coordinates(latitude, longitude):
        return None

    session = create_session()
    data = fetch_weather_data(session, latitude, longitude)

    if data:
        return parse_weather_data(data)

    return None

def main() -> None:
    parser = argparse.ArgumentParser(description="Get weather data")
    parser.add_argument("--latitude", type=float, help="Latitude of the location")
    parser.add_argument("--longitude", type=float, help="Longitude of the location")
    args = parser.parse_args()

    # Load from config if not provided as arguments
    if args.latitude is None or args.longitude is None:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
            latitude = config.get("latitude")
            longitude = config.get("longitude")
    else:
        latitude = args.latitude
        longitude = args.longitude

    print(f"Received latitude: {latitude}, longitude: {longitude}")  # Debugging line

    weather_report = get_weather(latitude, longitude)
    if not weather_report:
        return

    logger.info("Writing weather report to %s", OUTPUT_FILE)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w+") as f:
        f.write(weather_report)

if __name__ == "__main__":
    main()
