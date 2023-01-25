import requests
import json


class Location:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


def get_weather(lat, lon, cnt, api_key):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={cnt}&appid"
        f"={api_key}&units=metric")
    # print(json.dumps(json.loads(response.text), indent=4))
    json_response = json.loads(response.text)
    return json_response


def get_location(api_key):
    response = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&fields"
                            "=latitude,longitude")
    json_response = json.loads(response.text)
    return json_response


def parse_weather(weather_dict):
    day_info = {}
    rain_sum = 0
    for day in weather_dict["list"]:
        # print(day["temp"])
        # print(day["humidity"])
        # print(day["weather"][0]["id"])
        # print(day["weather"][0]["main"])
        if day["weather"][0]["id"] == 500:
            rain_sum += 1
    return int(rain_sum)


def parse_location(json_location):
    location = Location(json_location["latitude"], json_location["longitude"])
    return location


def get_rain_sum(location_response):
    # location_response = get_location("230eeb5cf5b045babc05ac6984d432a4")
    lat_lon = parse_location(location_response)
    weather = get_weather(lat_lon.lat, lat_lon.lon, 2, "debfa5e4207976ffb8d58a3ea30c607e")
    return parse_weather(weather)


if __name__ == '__main__':
    get_rain_sum()


