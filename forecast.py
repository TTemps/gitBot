import openmeteo_requests
from openmeteo_sdk.Variable import Variable
import geocoder
g = geocoder.ip('me')
print(g.latlng)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast" # URL for the Open-Meteo API
params = {
	"latitude": 49.4431, # Latitude of the location
	"longitude": 1.0993, # Longitude of the location
	"daily": "weather_code", # Get the weather code for each day
	"forecast_days": 0 # Get the current day's weather
}
# code a function that get the current position of where the script is running
# and return the latitude and longitude





