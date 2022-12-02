import telebot
import token
import time
import requests
from bs4 import BeautifulSoup as BS
from telebot import types

r = requests.get("https://ru.wikipedia.org/wiki/Статистика_выступлений_сборной_России_по_футболу#Подготовка_к_турниру")
html = BS(r.content, 'html.parser')
# for string in html.stripped_strings:
#    if string != ' ':
#        help += repr(string)
 #   else:
 #       dict += repr(help)
 #       help = ''
# dict += help

bot = telebot.TeleBot(token.TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAN8Y4ibiKIFp7Z-PzIcDE2TqKVh2KcAAkoJAAJ5XOIJbIauOPX8g6grBA')
    bot.send_message(message.chat.id, 'Приветствую тебя, путник, желайющий узнать сколько раз и как сходились звезды')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item=types.KeyboardButton("Info")
    markup.add(item)
    bot.send_message(message.chat.id, 'Выбери, какой команде с Чемпионата Мира ты симпатизируешь.', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
 #   p = 0
 #   k = 0
 #   list = message.text.split(" ")
 #   for i in range(len(dict)):
 #       if dict[i] == list[0] and dict[i + 1] == list[1]:
 #           p += 1
  #      elif dict[i] == list[1] and dict[i + 2] == list[0]:
#         k += 1
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Испания", callback_data='good', )
    item2 = types.InlineKeyboardButton("Аргентина", callback_data='bad')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Выбери, какой команде с Чемпионата Мира ты симпатизируешь.', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Rojo FUriA', )
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Beer')


            # bot.edit_message_text(chat.id=call.message.chat.id, message_id=call.message.message_id,
            # text="Info", reply_markup=None)
            bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False, text='тест')
    except Exception as e:
        print(repr(e))


# bot.polling(none_stop=True)
bot.polling(none_stop=True)
