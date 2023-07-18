import datetime
import config as cfg
import telebot
import message_constr


# from pprint import pprint


def log(message, cod):
    ss = f"{message.from_user.first_name} {message.from_user.last_name}:     {message.text}"
    print(
        f"{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')} | {ss:^45} | status = {cod}")


# def parametr_emodzy(par):
#     if par == "temp":
#         return "🌡"
#     elif par == "hum":
#         return "💧"
#     elif par == "wind":
#         return "🌪"
#     elif par == "pres":
#         return "🕰"

def send(message):
    w = message_constr.weather(message)
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
