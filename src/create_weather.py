import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("WeatherApi_TOKEN")


# lat 60.17048551529536, lon 24.938833170979652

# https://openweathermap.org/api/one-call-api

def fetch_weather():
    url = "https://api.openweathermap.org/data/2.5/weather?q=helsinki&units=metric&appid=" + token
    data = requests.get(url).json()

    return data


def create_weather_msg(weather_data):
    msg_text = "Current weather in " '<b>' + "Helsinki: " '</b>' \
                                             '\n' + "Temperature: " '<b>' + str(
        weather_data['main']['temp']) + ' Celcius' + '</b>' '\n' \
                                                     "Air humidity: " + '<b>' + str(
        weather_data['main']['humidity']) + '%' + '</b>' + '\n' \
               + "Weather conditions: " + '<b>' + weather_data['weather'][0]['description'] + '</b>' + '\n' \
               + "Wind: " + '<b>' + str(weather_data['wind']['speed']) + 'm/s' + '</b>' \

    return msg_text
