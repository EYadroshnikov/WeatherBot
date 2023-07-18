import datetime
import config as cfg
import telebot
import message_constr
from telebot import types


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

def construct_inline_murkup():
    inline_key_board = types.InlineKeyboardMarkup()
    inline_key_board.add(types.InlineKeyboardButton(text="Обновить", callback_data="reload"))
    return inline_key_board


def send(message):
    w = message_constr.weather(message.text)
    try:
        bot.send_message(message.chat.id, w[0], parse_mode="Markdown", reply_markup=construct_inline_murkup())
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


@bot.callback_query_handler(func=lambda call: call.data == 'reload')
def reload(call):
    city = call.message.text.split()[8][:-1]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text=message_constr.weather(city), reply_markup=construct_inline_murkup())


bot.infinity_polling()
