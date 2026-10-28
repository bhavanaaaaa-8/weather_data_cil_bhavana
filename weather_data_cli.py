
import requests
import math

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_coordinates(city):
    """Find the coordinates of a city."""

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(
            GEOCODING_URL, params=params, timeout=10
        )
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException:
        print("Error: Could not connect to the geocoding API.")
        return None
    except ValueError:
        print("Error: Invalid JSON received from the API.")
        return None

    results = data.get("results")

    if not isinstance(results, list) or not results:
        print("Error: City not found. Enter a valid city name.")
        return None

    location = results[0]
    latitude = location.get("latitude")
    longitude = location.get("longitude")

    if not valid_number(latitude) or not valid_number(longitude):
        print("Error: Invalid coordinates received.")
        return None

    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        print("Error: Coordinates are outside valid ranges.")
        return None

    return latitude, longitude, location.get("country", "")


def valid_number(value):
    """Check whether a value is a finite number."""

    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def get_weather(latitude, longitude):
    """Retrieve and validate current weather."""

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "is_day,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto"
    }

    try:
        response = requests.get(
            WEATHER_URL, params=params, timeout=10
        )
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException:
        print("Error: Could not retrieve weather information.")
        return None
    except ValueError:
        print("Error: Invalid JSON received from the weather API.")
        return None

    current = data.get("current")

    if not isinstance(current, dict):
        print("Error: Current weather data is unavailable.")
        return None

    required_fields = [
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "is_day",
        "precipitation",
        "weather_code",
        "wind_speed_10m"
    ]

    if any(field not in current for field in required_fields):
        print("Error: Weather information is incomplete.")
        return None

    for field in required_fields:
        if current[field] is None:
            print(f"Error: Missing value for {field}.")
            return None

    numeric_fields = [
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "precipitation",
        "weather_code",
        "wind_speed_10m"
    ]

    for field in numeric_fields:
        if not valid_number(current[field]):
            print(f"Error: Invalid value for {field}.")
            return None

    if not isinstance(current["is_day"], int) or isinstance(
        current["is_day"], bool
    ) or current["is_day"] not in (0, 1):
        print("Error: Invalid day/night information.")
        return None

    if not 0 <= current["relative_humidity_2m"] <= 100:
        print("Error: Invalid humidity value.")
        return None

    if current["precipitation"] < 0 or current["wind_speed_10m"] < 0:
        print("Error: Invalid precipitation or wind speed.")
        return None

    weather_code = current["weather_code"]

    if not weather_code.is_integer() or not 0 <= weather_code <= 99:
        print("Error: Invalid weather code.")
        return None

    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    if int(weather_code) not in weather_descriptions:
        print("Error: Unknown weather code.")
        return None

    return {
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "precipitation": current["precipitation"],
        "condition": weather_descriptions[int(weather_code)],
        "time": data.get("current", {}).get("time"),
        "is_day": current["is_day"]
    }


def main():
    print("=" * 32)
    print("       COMMAND-LINE WEATHER APP")
    print("=" * 32)

    city = input("Enter city name: ").strip()

    if not city:
        print("Error: City name cannot be empty.")
        return

    coordinates = get_coordinates(city)

    if coordinates is None:
        return

    latitude, longitude, country = coordinates

    weather = get_weather(latitude, longitude)

    if weather is None:
        return

    print("\n" + "=" * 32)
    print(f"Weather in {city.title()}")
    if country:
        print(f"Country: {country}")
    print("=" * 32)
    print(f"Temperature : {weather['temperature']} °C")
    print(f"Feels like  : {weather['feels_like']} °C")
    print(f"Condition   : {weather['condition']}")
    print(f"Humidity    : {weather['humidity']}%")
    print(f"Wind speed  : {weather['wind_speed']} km/h")
    print(f"Precipitation: {weather['precipitation']} mm")

    if weather["time"]:
        print(f"Local time  : {weather['time']}")

    print(f"Daytime     : {'Yes' if weather['is_day'] else 'No'}")
    print("=" * 32)
    print("Weather information retrieved successfully!")


if __name__ == "__main__":
    main()
