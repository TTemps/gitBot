import requests
import geocoder

def weather_code_to_emoji(code):
    """
    Convert weather condition codes to corresponding emojis.

    Args:
    code (int): Weather condition code.

    Returns:
    str: Corresponding emoji for the weather condition.
    """
    if code == 0:
        return "☀️  Dégagés"  # Clear sky
    elif code in [1, 2, 3]:
        return "🌤️  Partiellement dégagé "  # Mainly clear, partly cloudy, and overcast
    elif code in [45, 48]:
        return "🌫️"  # Fog and depositing rime fog
    elif code in [51, 53, 55]:
        return "🌦️  Crachin"  # Drizzle: Light, moderate, and dense intensity
    elif code in [56, 57]:
        return "❄️🌧️  Crachin gélant"  # Freezing Drizzle: Light and dense intensity
    elif code in [61, 63, 65]:
        return "🌧️  Pluie modère "  # Rain: Slight, moderate, and heavy intensity
    elif code in [66, 67]:
        return "❄️🌧️  Pluie verglacente"  # Freezing Rain: Light and heavy intensity
    elif code in [71, 73, 75]:
        return "❄️  Neige"  # Snow fall: Slight, moderate, and heavy intensity
    elif code == 77:
        return "❄️  Neige abondante"  # Snow grains
    elif code in [80, 81, 82]:
        return "🌧️🌦️  Pluie modéré"  # Rain showers: Slight, moderate, and violent
    elif code in [85, 86]:
        return "❄️🌨️  Blizzard"  # Snow showers slight and heavy
    elif code == 95:
        return "⛈️  Orage"  # Thunderstorm: Slight or moderate
    elif code in [96, 99]:
        return "⛈️🌨️  Orage violent"  # Thunderstorm with slight and heavy hail
    else:
        return "🤷‍♂️"  # Unknown weather condition
    
def is_day (is_day): 
    if is_day == 1:
        return "Jour"
    else:
        return "Nuit"

def get_lattitude_longitude():
    g = geocoder.ip('me') # Get the current position of the script
    latitude = g.latlng[0] # Get the latitude
    longitude = g.latlng[1] # Get the longitude
    city_name = g.city # Get the name of the city
    return latitude, longitude, city_name

def get_default_format_date(date): # expected format: 2024-02-13T08:02 in string return format: 13/02/2024 08:02 in string
    date = date.split("T")
    heure = date[1].split(":") # heure[0] = heure, heure[1] = minute
    date = date[0].split("-") # date[0] = année, date[1] = mois, date[2] = jour
    date = date[2] + "/" + date[1] + "/" + date[0] + " " + heure[0] + ":" + heure[1]
    return date
def get_weather():
    position = get_lattitude_longitude()
    params = {
        "latitude": position[0], # Latitude of the location
        "longitude": position[1], # Longitude of the location
        "current": ["temperature_2m", "is_day", "weather_code"],
	    "daily": ["sunrise", "sunset"],
        "timezone": "auto", 
    }
    url = "https://api.open-meteo.com/v1/forecast"
    response = requests.get(url, params=params)
    data = response.json()
    # Vérification et extraction des données
    if 'daily' in data:
        dates = data['daily']['time']
        sunrise = data['daily']['sunrise'][0]
        sunset = data['daily']['sunset'][0]
        temperature = data['current']['temperature_2m']
        is_day_night = data['current']['is_day']
        weather_code = data['current']['weather_code']
        
        # Préparation du DataFrame
        daily_data = {
            "sunrise": get_default_format_date(sunrise),
            "sunset": get_default_format_date(sunset),
            "temperature": str(temperature) + '°C',
            "is_day": is_day(is_day_night),
            "weather_code": weather_code_to_emoji(weather_code)
        }
    else:
        print("Données journalières non trouvées dans la réponse de l'API.")
    return daily_data