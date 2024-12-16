import requests

#this part is just creating data to use. the whole database thing didn't make much sense especially because
#at least at the start the scale will be really small. i decided to start w/ just five mountains bc its enough
#to get a feel and a working model
ski_resorts = [
    {"name": "Wachusett Mountain", "latitude": 42.4889793, "longitude": -71.8870186, "state": "Massachusetts",
     "elevation_ft": 2006
     ###add any other info needed for each of these.
     ###possibly need to store the number of trails by level
     ##and do some sort of rating for difficulty
     # idk if you've ever skiied but theres basically 3 main leves (green, blue, black)
     # so like we could give a place a score based on like 1 for a green, 3 for a blue, 5 for a black
     # or something like that, so the user could say they want the best mountain w/ a minimum score x
     },
    {"name": "Waterville Valley", "latitude": 43.9509, "longitude": -71.4991, "state": "New Hampshire",
     "elevation_ft": 4004},
    {"name": "Cannon Mountain", "latitude": 44.1565, "longitude": -71.6984, "state": "New Hampshire",
     "elevation_ft": 4080},
    {"name": "Sunday River", "latitude": 44.4600, "longitude": -70.8000, "state": "Maine",
     "elevation_ft": 3140},
    {"name": "Tenney Mountain", "latitude": 43.7378, "longitude": -71.7910, "state": "New Hampshire",
     "elevation_ft": 2149}
]



#this is the part that actually does the scraping
def get_weather_data(lat, lon):
    url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(url)
    #makes sure the request went thru
    if response.status_code == 200:
        data = response.json()
        forecast_url = data['properties']['forecast']

        #gets forecast
        forecast_response = requests.get(forecast_url)
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            #properties is a dictionary in the json
            return forecast_data['properties']['periods']
    return None


# Example coordinates for Wachusett Mountain
lat = 42.4889793
lon = -71.8870186
weather = get_weather_data(lat, lon)
for period in weather:
    print(f"{period['name']}: {period['temperature']}°F, {period['shortForecast']}")


#example of a bigger print statement w/ more values:
#print(f"{period['name']} - Temp: {period['temperature']}°F, {period['shortForecast']}, "
#      f"Wind: {period['windSpeed']} from {period['windDirection']}, Precipitation: {period['precipitationAmount']} inches.")