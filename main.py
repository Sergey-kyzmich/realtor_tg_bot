import json
import random
import time
import datetime

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from text import text
from catalog import init_catalog
from tk import token, admin

bot=telebot.TeleBot(token)
catalog = init_catalog(bot, text)

@bot.message_handler(commands=['start'])
def start_message(message):
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    mb_1 = KeyboardButton(text="Каталог")
    mb_2 = KeyboardButton(text="Ссылка на блог")
    mb_3 = KeyboardButton(text="Ссылка на специалиста")
    main_kb.add(mb_1, mb_2, mb_3)
    bot.send_message(message.chat.id, 
                     "<b>"+text["start"]+"</b>", 
                     reply_markup=main_kb, 
                     parse_mode="HTML")



@bot.message_handler(content_types="text")
def catalog_start(message):
    if message.text=="Каталог":
        catalog.start(message=message, back=False)

@bot.callback_query_handler(func=lambda  callback: callback.data)
def check_callback_data(callback):
    if callback.data in ["apartment", "house", "comm_apartment"]:
        catalog.edit(callback,  {"type": callback.data})
        catalog.select_location(callback)

    elif callback.data in ["in_the_mountains", "by_the_sea"]:
        catalog.edit(callback, {"location":callback.data})
        catalog.select_sum(callback)
    elif callback.data == "back-to-catalog-1":
        catalog.start(message=callback, back=True)
    
    elif callback.data == "back-to-catalog-2":
        catalog.select_location(callback)
    elif callback.data == "back-to-catalog-3":
        catalog.select_sum(callback)
    elif callback.data in ["sum-1", "sum-2", "sum-3", "sum-4"]:
        catalog.edit(callback=callback, edit={"sum": callback.data[-1]})

@bot.message_handler(commands="help")
def help(message):
    bot.send_message(message.chat.id, 
                     text="<b>"+text["help"]+"</b>", 
                     parse_mode="HTML")
bot.infinity_polling()