import requests
import config as cfg


def get_weather(city):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={cfg.api_key}&units=metric")
        json = r.json()
        return json
    except Exception as ex:
        print(ex)
        print("invalid city:", city)
