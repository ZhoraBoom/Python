import telebot
import config
import lxml
import pandas
from PIL import Image
import requests
from bs4 import BeautifulSoup as BS
from telebot import types

# parsing and processing data to the dictionary
r = requests.get("https://ru.wikipedia.org/wiki/Статистика_выступлений_сборной_России_по_футболу#Подготовка_к_турниру")
soup = BS(r.content, 'lxml')
new = soup.find('table').find_all('tr')
dict = {}
# iteration by string in table
for item in new:
    x = item.find_all('td')
    word = 'regs'
    list = []
    i = 0
    # iteration by column in string
    for y in x:
        if i != 0:
            if y.get_text(strip=True) != 'Подробнее о матчах' and y.get_text(strip=True) != 'Подробнее о матче':
                list.append(y.get_text(strip=True))
        else:
            if y.get_text(strip=True) != 'Сербия(Югославия)':
                word = y.get_text(strip=True)
            else:
                word = 'Сербия'
            i += 1
    dict[word] = list

bot = telebot.TeleBot(config.TOKEN)


# command to start: sticker and message
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAN8Y4ibiKIFp7Z-PzIcDE2TqKVh2KcAAkoJAAJ5XOIJbIauOPX8g6grBA')
    bot.send_message(message.chat.id, 'Приветствую тебя, путник!')


# command to help: message only
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, config.instructions)


# command to answer to request
@bot.message_handler(commands=['request'])
def request_message(message):
    # creating Keyboard of options which appears in your window of Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Хочу выбрать фаворита")
    item2 = types.KeyboardButton("Узнать историю игр")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Что тебя привело ко мне?', reply_markup=markup)


# processing simple message
@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Хочу выбрать фаворита":
        # creating Keyboard which binds with my message, you can choose option
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton('Испания 🇪🇸', callback_data='good', )
        item2 = types.InlineKeyboardButton('Аргентина 🇦🇷', callback_data='bad')
        item3 = types.InlineKeyboardButton("Франция 🇫🇷", callback_data='norm')
        item4 = types.InlineKeyboardButton("Бразилия 🇧🇷", callback_data='boy')
        item5 = types.InlineKeyboardButton("Англия 🏴󠁧󠁢󠁥󠁮󠁧󠁿", callback_data='joy')
        item6 = types.InlineKeyboardButton("Португалия 🇵🇹", callback_data='boom')
        markup.add(item1, item2, item3, item4, item5, item6)
        bot.send_message(message.chat.id, 'Выбери, какой команде с ЧМ ты симпатизируешь.', reply_markup=markup)
    elif message.text == "Узнать историю игр":
        bot.send_message(message.chat.id, 'С какой сборной тебя интересует статистика матчей сборной России? Напиши одним сообщением название сборной с большой буквы.')
    else:
        # checking country in list
        if message.text in dict.keys():
            list = dict[message.text]
            matches = list[0]
            wins = list[1]
            draws = list[2]
            loses = list[3]
            difference = list[6]
            bot.send_message(message.chat.id, f'Всего между сборными стран Россия и {message.text} было сыграно (матчей: {matches}) с общей разницей забитых и пропущенных мячей {difference}.')
            str = 'Сборная России '
            if wins != '0':
                str += f'одержала побед: {wins}, '
            if draws != '0':
                if (draws != '2' and draws != '3') and draws != '4':
                    str += f'сыграла вничью {draws} раз, '
                else:
                    str += f'сыграла вничью {draws} раза, '
            if loses != '0':
                str += f'а также потерпела поражений: {loses}.'
            if str[-2] == ',':
                str = str[0:-2] + '.' + str[-1]
            bot.send_message(message.chat.id, str)
        else:
            bot.send_message(message.chat.id, 'В мой функционал не входит возможность ответить на такое(((')
            bot.send_sticker(message.chat.id, config.SVIN)


# processing answer in inline Keyboard
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'FURIAAAAAAA ROJA', )
                bot.send_photo(call.message.chat.id, Image.open(r'spain.webp'))
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'LA ALBISELENTEEEE')
                bot.send_photo(call.message.chat.id, Image.open(r'argentina.jpg'))
            elif call.data == 'norm':
                bot.send_message(call.message.chat.id, 'GREENOUILLE')
                bot.send_photo(call.message.chat.id, Image.open(r'france.jpg'))
            elif call.data == 'boy':
                bot.send_message(call.message.chat.id, 'A SELECAOOOOOO')
                bot.send_photo(call.message.chat.id, Image.open(r'brazil.jpg'))
            elif call.data == 'joy':
                bot.send_message(call.message.chat.id, 'THREE LIONS')
                bot.send_photo(call.message.chat.id, Image.open(r'england.webp'))
            elif call.data == 'boom':
                bot.send_message(call.message.chat.id, 'PASTEIS')
                bot.send_photo(call.message.chat.id, Image.open(r'portugal.jpg'))


            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                text='Выбери, какой команде с Чемпионата Мира ты симпатизируешь.', reply_markup=None)
            bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False, text='тест')
    except Exception as e:
        print(repr(e))


# bot.polling(none_stop=True)
bot.polling(none_stop=True)
