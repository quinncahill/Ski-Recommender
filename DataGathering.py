import requests
import re

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



#
# Example coordinates for Wachusett Mountain
lat = 42.4889793
lon = -71.8870186
#weather = get_weather_data(lat, lon)

#Data in the form of:
#number, name, starttime, endtime, isDaytime, tempeerature, temperatureUnit, temperatureTrend,
# probabilityOfPrecipitation, windSpeed, windDirection, icon (some url idk if it is useful),
# short forecast, detailed forecast

#significantly easier to use number than name because the name of the current changes throughout the day, although after current day
#it does day night day night. numbers are just much more consistent.

#probably the most useful data would be precipitation and temperature
#print(weather)
#for period in weather:
    #print(f"{period['number']}")
    #print(f"Wachusett Mountain Weather")
    #print(f"{period['name']}: {period['temperature']}°F, {period['shortForecast']}")


#example of a bigger print statement w/ more values:
#print(f"{period['name']} - Temp: {period['temperature']}°F, {period['shortForecast']}, "
#      f"Wind: {period['windSpeed']} from {period['windDirection']}, Precipitation: {period['precipitationAmount']} inches.")



for resort in ski_resorts:
    resort["weather"] = get_weather_data(resort["latitude"], resort["longitude"])
    #print(resort)

#this method could be used to give some sort of score/value to the predicted snowfall. right now it just gets the probability
#from the nws data. this could be configured to loop through all the time periods or take in a time period

#just read your text, yea I agree, would probably use some sort of combination between temp, wind, and precipitation

def getPrecipitationPercent(resort, num):
    weather = resort['weather']
    #print(weather)
    periodOne = weather[num]
    #print(periodOne)
    precipitation = periodOne['probabilityOfPrecipitation']
    #print(precipitation)
    precipitationPercent = precipitation['value']
    #print (precipitationPercent)
    #print ("Chance of Precipitation")
    if precipitationPercent == None:
        precipitationPercent = 0
    return precipitationPercent
    #print(precipitationPercent)
    #output is either an int or string 'none'

def getWindSpeed(resort, num):
    weather = resort['weather']
    periodOne = weather[num]
    windSpeed = periodOne['windSpeed']
    #print(windSpeed)
    maxSpeed = re.search(r'\d+', windSpeed).group()
    #maxSpeed = windSpeed.split()[2]
    #print (windSpeed)
    #print(maxSpeed)
    #print("MPH")
    return maxSpeed

def getTemperature(resort, num):
    weather = resort['weather']
    print(weather)
    periodOne = weather[num]
    temperature = periodOne['temperature']
    #print(periodOne)
    #print(temperature)
    #print ("F")
    return temperature


def computeWeatherScore(precipitationChance, temp, wind):
    #print(precipitationChance)
    precipitationChance = int(precipitationChance)
    print(precipitationChance)
    temp = int(temp)
    wind = int(wind)
    if temp < 30:
        return precipitationChance - temp - (wind*1.25)
        #return (100 - precipitationChance) + temp + (wind * 1.25)
    elif temp < 60:
        return (.5 * precipitationChance) - temp - (wind*1.25)
        #return (1.25 * (100 - precipitationChance)) + temp + (1.25 * wind)
    else:
        return 100

#this method doesn't fully work because the data is NoneType. Unsure how to convert this to ints since it prints as ints
def addScoreToResorts(resort, num):
    precipitation = getPrecipitationPercent(resort, num)
    windSpeed = getWindSpeed(resort, num)
    temperature = getTemperature(resort, num)
    #print(precipitation)
    score = computeWeatherScore(precipitation, temperature, windSpeed)
    score = round(score, 2)
    #print(score)
    resort[f"score_{num}"] = score
    #resort["score"] = score



for resort in ski_resorts:
    #print(resort["name"])
    addScoreToResorts(resort, 1)
    addScoreToResorts(resort, 2)
    #print(resort["score"])

    #print("NONE")

def get_ski_resorts_with_scores(weatherNum):
    for resort in ski_resorts:
        addScoreToResorts(resort, weatherNum)
    #print(ski_resorts)
    return ski_resorts

