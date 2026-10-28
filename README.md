# Command-Line Weather App

## Description
A Python command-line application that retrieves current weather information for a user-provided city using the Open-Meteo API. It validates city names, checks weather data, and displays the results in a clean format.

## Features
- Search for a city by name.
- Retrieve latitude and longitude using the geocoding API.
- Display current temperature and feels-like temperature.
- Show humidity, wind speed, precipitation, and weather conditions.
- Display local time and daytime status.
- Handle invalid city names and empty inputs.
- Handle connection failures, HTTP errors, invalid JSON, and missing weather data.
- Validate weather values before displaying the report.
- No API key required for normal non-commercial use.

## Requirements
- Python 3.8 or later
- `requests` library
- Internet connection

## Installation

1. Clone or download this project.
2. Open a terminal in the project folder.
3. Install the required library:

```bash
pip install requests
```

## Usage

Run the Python script:

```bash
python weather_app.py
```

Enter a city name when prompted, for example:

```text
Enter city name: Bengaluru
```

The application retrieves the weather data and displays the report.

## APIs Used

**Geocoding API**

`https://geocoding-api.open-meteo.com/v1/search`

Converts a city name into geographic coordinates.

**Weather API**

`https://api.open-meteo.com/v1/forecast`

Retrieves current weather information for the selected coordinates.

Documentation: https://open-meteo.com/en/docs

## Error Handling
The application handles:
- Empty city names
- Cities that cannot be found
- Network and connection failures
- HTTP errors
- Invalid JSON responses
- Missing or invalid weather values
- Unknown weather codes

## Project Structure

```text
weather-app/
├── weather_app.py
└── README.md
```

## Example Output

```text
COMMAND-LINE WEATHER APP
Enter city name: Bengaluru

Weather in Bengaluru
Country: India
Temperature: 27.5 °C
Feels like: 29.1 °C
Condition: Partly cloudy
Humidity: 65%
Wind speed: 12.4 km/h
Precipitation: 0.0 mm
```

*Example values are illustrative; actual readings depend on the API response.*

## Future Improvements
- Add a five-day weather forecast.
- Support searching for multiple cities.
- Add temperature conversion between Celsius and Fahrenheit.
- Save weather reports to a file.
- Add unit tests for validation and error handling.

## License
This project is intended for educational and personal learning purposes. Review Open-Meteo's terms of use before using the API commercially.
