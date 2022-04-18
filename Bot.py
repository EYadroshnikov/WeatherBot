import datetime
import config as cfg
import telebot
import requests


# from pprint import pprint


def log(message, cod):
    ss = f"{message.from_user.first_name} {message.from_user.last_name}:     {message.text}"
    print(
        f"{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')} | {ss:^45} | status = {cod}")


def get_weather(city):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={cfg.api_key}&units=metric")
        json = r.json()
        return json
    except Exception as ex:
        print(ex)
        print("invalid city:", city)


def invalid_city(message):
    return f"Город {message.text} не найден, попробуйте другой"
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


# def parametr_emodzy(par):
#     if par == "temp":
#         return "🌡"
#     elif par == "hum":
#         return "💧"
#     elif par == "wind":
#         return "🌪"
#     elif par == "pres":
#         return "🕰"


def weather(message):
    data = get_weather(message.text)
    if data['cod'] != 200:
        return invalid_city(message), data['cod']
    else:
        return f"* ---------- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ---------- *\n" \
               f"{weather_emodzy(data['name'])} Погода в г. {data['name']}: {data['weather'][0]['description']} {weather_emodzy(data['name'])}\n" \
               f"🌡 Температура: {data['main']['temp']}°C ({data['main']['feels_like']}°C) 🌡\n " \
               f"💧 Влажность: {data['main']['humidity']}% 💧\n" \
               f"🌪 Скорость ветра: {data['wind']['speed']} м/с 🌪\n" \
               f"🕰 Давление: {data['main']['pressure']} мм рт. ст. 🕰", data['cod']


def send(message):
    w = weather(message)
    try:
        bot.send_message(message.chat.id, w[0], parse_mode="Markdown")
    except Exception as ex:
        print(ex)
    log(message, w[1])


bot = telebot.TeleBot(cfg.token, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     f"Здравствуй {message.from_user.first_name}, введите город")


@bot.message_handler(func=lambda message: True)
def handler(message):
    send(message)


bot.infinity_polling()
