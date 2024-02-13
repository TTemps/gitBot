import openmeteo_requests
from openmeteo_sdk.Variable import Variable
import geocoder
from datetime import datetime

def weather_code_to_emoji(code):
    """
    Convert weather condition codes to corresponding emojis.

    Args:
    code (int): Weather condition code.

    Returns:
    str: Corresponding emoji for the weather condition.
    """
    if code == 0:
        return "☀️ Dégagés"  # Clear sky
    elif code in [1, 2, 3]:
        return "🌤️ Partiellement dégagé "  # Mainly clear, partly cloudy, and overcast
    elif code in [45, 48]:
        return "🌫️"  # Fog and depositing rime fog
    elif code in [51, 53, 55]:
        return "🌦️ Crachin"  # Drizzle: Light, moderate, and dense intensity
    elif code in [56, 57]:
        return "❄️🌧️ Crachin gélant"  # Freezing Drizzle: Light and dense intensity
    elif code in [61, 63, 65]:
        return "🌧️ Pluie modère "  # Rain: Slight, moderate, and heavy intensity
    elif code in [66, 67]:
        return "❄️🌧️ Pluie verglacente"  # Freezing Rain: Light and heavy intensity
    elif code in [71, 73, 75]:
        return "❄️ Neige"  # Snow fall: Slight, moderate, and heavy intensity
    elif code == 77:
        return "❄️ Neige abondante"  # Snow grains
    elif code in [80, 81, 82]:
        return "🌧️🌦️ Pluie modéré"  # Rain showers: Slight, moderate, and violent
    elif code in [85, 86]:
        return "❄️🌨️ Blizzard"  # Snow showers slight and heavy
    elif code == 95:
        return "⛈️ Orage"  # Thunderstorm: Slight or moderate
    elif code in [96, 99]:
        return "⛈️🌨️ Orage violent"  # Thunderstorm with slight and heavy hail
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

def get_weather(position = None):
    om = openmeteo_requests.Client() # Create a new client
    params = {
        "latitude": position[0], # Latitude of the location
        "longitude": position[1], # Longitude of the location
        "current": ["temperature_2m", "is_day", "weather_code"],
	    "daily": ["sunrise", "sunset"],
        "timezone": "auto", 
    }
    responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]
    
    # Get the current weather information
    
    current = response.Current() 
    current_temperature_2m = current.Variables(0).Value()
    current_is_day = current.Variables(1).Value()
    current_weather_code = current.Variables(2).Value()
    
    # Get the daily weather information
    daily = response.json()
    daily_sunrise = daily.Variables(0)
    daily_sunset = daily.Variables(1)
    print(daily_sunrise)
    # Create a dictionary with the weather information
    
    weather_data = {
        "Température": str(int(current_temperature_2m)) + "°C",
        "Jour/Nuit": is_day(current_is_day),
        "Météo code": weather_code_to_emoji(current_weather_code),
        "Sunrise": daily_sunrise,
        "Sunset": daily_sunset
    }
    
    for i in weather_data:
        print(i, ":", weather_data[i])

    
    
    
    
    
    
    
    
    
    
    
    meteo_info = {}
    return meteo_info

position = get_lattitude_longitude() # Get the current position of the script
weather = get_weather(position) # Get the current weather
for i in weather:
    print(i, ":", weather[i]) # Print the weather information