import requests
import datetime
import config as cfg
import getData


def invalid_city(city):
    return f"Город {city} не найден, попробуйте другой"
    # bot.send_message(message.chat.id, f"Город {message.text} не найден, попробуйте другой")


def weather_emodzy(city):
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={cfg.api_key}&units=metric")
    json = r.json()
    des = json["weather"][0]["description"]
    # print(des)
    if des == "clear sky":
        return "☀"
    elif des == "few clouds" or "broken clouds":
        return "⛅"
    elif des == "scattered clouds":
        return "☁"
    elif des == "overcast clouds":
        return "☁"
    elif des == "shower rain":
        return "🌧"
    elif des == "light rain" or "moderate rain":
        return "🌦"
    elif des == "thunderstorm":
        return "⛈"
    elif des == "snow":
        return "❄"
    elif des == "mist":
        return "🌫"


def weather(city):
    data = getData.get_weather(city)

    if data['cod'] != 200:
        return invalid_city(city), data['cod']
    else:
        return f" ---------- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ---------- \n" \
               f"{weather_emodzy(data['name'])} Погода в г. {data['name']}: {data['weather'][0]['description']} {weather_emodzy(data['name'])}\n" \
               f"🌡 Температура: {data['main']['temp']}°C ({data['main']['feels_like']}°C) 🌡\n " \
               f"💧 Влажность: {data['main']['humidity']}% 💧\n" \
               f"🌪 Скорость ветра: {data['wind']['speed']} м/с 🌪\n" \
               f"🕰 Давление: {data['main']['pressure']} мм рт. ст. 🕰", data['cod']
