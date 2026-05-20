import requests
import os


def get_weather(city: str) -> dict | None:
    """
    Fetch current weather from OpenWeatherMap for a given city.
    Returns a dict with temp, description, icon, city — or None on failure.
    """
    api_key = os.environ.get('OPENWEATHER_API_KEY', '')
    if not api_key:
        return None

    try:
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            'city': data['name'],
            'temp': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'description': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['icon'],
        }
    except Exception:
        return None
