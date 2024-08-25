import argparse
import datetime
import logging
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter, Retry
import yaml
from typing import Optional, List

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

def fetch_weather_data(session: requests.Session, latitude: float, longitude: float, forecast_days: Optional[int] = None) -> Optional[dict]:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "timezone": "auto",
    }
    if forecast_days:
        params["daily"] = "temperature_2m_max,temperature_2m_min,weathercode"
        params["forecast_days"] = forecast_days
    
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

def parse_weather_data(data: dict, forecast_days: Optional[int] = None) -> Optional[List[str]]:
    output = []
    if "current_weather" in data:
        temp_celsius = data["current_weather"]["temperature"]
        weather_code = data["current_weather"]["weathercode"]
        weather_description = WEATHER_DESCRIPTIONS.get(weather_code, "Unknown")
        current_weather = (
            f"Current weather ({datetime.datetime.now(tz=datetime.UTC)}):"
            f" {temp_celsius:.1f}°C, {weather_description}"
        )
        output.append(current_weather)
        logger.info("Current weather: %s", current_weather)
    
    if forecast_days and "daily" in data:
        daily_data = data["daily"]
        for i in range(forecast_days):
            date = daily_data["time"][i]
            max_temp = daily_data["temperature_2m_max"][i]
            min_temp = daily_data["temperature_2m_min"][i]
            weather_code = daily_data["weathercode"][i]
            weather_description = WEATHER_DESCRIPTIONS.get(weather_code, "Unknown")
            forecast = (
                f"Forecast for {date}: Max Temp: {max_temp:.1f}°C, "
                f"Min Temp: {min_temp:.1f}°C, {weather_description}"
            )
            output.append(forecast)
            logger.info("Forecast: %s", forecast)
    
    if output:
        return output
    logger.error("Failed to fetch weather data")
    return None

def get_weather(latitude: float, longitude: float, forecast_days: Optional[int] = None) -> Optional[List[str]]:
    logger.info("Fetching weather data for [lat: %f, long: %f] with forecast days: %s", latitude, longitude, forecast_days)

    if not validate_coordinates(latitude, longitude):
        return None

    session = create_session()
    data = fetch_weather_data(session, latitude, longitude, forecast_days)

    if data:
        print(data)
        return parse_weather_data(data, forecast_days)

    return None

def main() -> None:
    parser = argparse.ArgumentParser(description="Get weather data")
    parser.add_argument("--latitude", type=float, help="Latitude of the location")
    parser.add_argument("--longitude", type=float, help="Longitude of the location")
    parser.add_argument("--forecast", type=int, help="Number of forecast days (1-7)", choices=range(1, 8))
    args = parser.parse_args()

    # Load from config if not provided as arguments
    if args.latitude is None or args.longitude is None:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
            latitude = config.get("latitude")
            longitude = config.get("longitude")
            forecast_days = config.get("forecast_days", None)  # Get forecast_days from config
    else:
        latitude = args.latitude
        longitude = args.longitude
        forecast_days = args.forecast if args.forecast else None  # Handle optional forecast

    # Debugging print to check if forecast_days is correctly set
    print(f"Received latitude: {latitude}, longitude: {longitude}, forecast days: {forecast_days}")

    weather_report = get_weather(latitude, longitude, forecast_days)
    if not weather_report:
        return
    
    current_timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%MUTC")
    
    # File structure: /data/weather/YYYY/MM/DD/latitude_longitude_forecast_days_timestamp.txt
    filename = f"{latitude}_{longitude}_{forecast_days}_{current_timestamp}.txt"
    output_dir = Path(f"results/{datetime.datetime.utcnow().strftime('%Y/%m/%d/')}")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename

    logger.info("Writing weather report to %s", output_path)
    with output_path.open("w+") as f:
        for line in weather_report:
            f.write(line + "\n")

if __name__ == "__main__":
    main()
