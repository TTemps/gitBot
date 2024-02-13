import requests
import pandas as pd

# Paramètres de l'API
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 49.4431,
    "longitude": 1.0993,
    "current": ["temperature_2m", "is_day", "weather_code"],
    "daily": "sunrise,sunset",
    "timezone": "auto",
}

# Faire la requête à l'API
response = requests.get(url, params=params)
data = response.json()

# Vérification et extraction des données
if 'daily' in data:
    dates = data['daily']['time']
    sunrise = data['daily']['sunrise']
    sunset = data['daily']['sunset']
    temperature = data['current']['temperature_2m']
    is_day = data['current']['is_day']
    weather_code = data['current']['weather_code']
    
    # Préparation du DataFrame
    daily_data = {
        "date": dates,
        "sunrise": sunrise,
        "sunset": sunset,
        "temperature": temperature,
        "is_day": is_day,
        "weather_code": weather_code
    }
    
    #daily_dataframe = pd.DataFrame(daily_data)
    print(daily_data)
else:
    print("Données journalières non trouvées dans la réponse de l'API.")
