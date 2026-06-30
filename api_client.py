import requests

API_URL = "https://api.open-meteo.com/v1/forecast"

def obtener_clima_api(latitud, longitud):
    params = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto"
    }

    response = requests.get(API_URL, params=params, timeout=10)

    if response.status_code == 200:
        return response.json()
    else:
        return None