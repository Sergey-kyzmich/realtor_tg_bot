import json
import random
import time
import datetime

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from text import text
from catalog import init_catalog
from tk import token
from admin import admin_panel
#Константы
bot=telebot.TeleBot(token)
catalog = init_catalog(bot, text)
admin = admin_panel(bot, text, token)
#Системные переменные
wait_password = []
admin_wait_add_description = []
admin_wait_add_name = []

#Функции
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


@bot.message_handler(commands=["admin"])
def admin_start(message):
    if not(admin.check_on_admin(message.chat.id)):
        wait_password.append(message.chat.id)
    admin.get_password_admin(message)


@bot.message_handler(content_types="text")
def catalog_start(message):
    if message.chat.id in wait_password and message.chat.id not in ["Каталог", "Ссылка на блог", "Ссылка на специалиста"]:
        wait_password.remove(message.chat.id)
        if message.text==token:
            admin.add_to_admin(message)
            admin.main_admin_menu(message, back=False)
        else:
            bot.send_message(chat_id=message.chat.id, text="<b>Пароль неверный</b>", parse_mode="HTML")
    elif message.text=="Каталог":
        catalog.start(message=message, back=False)
    
    if message.chat.id in admin_wait_add_name and message.chat.id not in ["Каталог", "Ссылка на блог", "Ссылка на специалиста"]:
        admin_wait_add_name.remove(message.chat.id)
        admin_wait_add_description.append(message.chat.id)
        admin.admin_apartment.add_apartment_5(message, back=False)
        
    if message.chat.id in admin_wait_add_description and message.chat.id not in ["Каталог", "Ссылка на блог", "Ссылка на специалиста"]:
        admin_wait_add_description.remove(message.chat.id)
        admin.admin_apartment.add_apartment_6(message)
    if message.text=="Ссылка на блог":
        bot.send_message(chat_id=message.chat.id,
                         text="<b>"+text["blog_info"]+"</b>",
                         parse_mode="HTML")


#! ---CALLBACK---
@bot.callback_query_handler(func=lambda  callback: callback.data)
def check_callback_data(callback):

    #* callback при выборе типа жилья в каталоге
    if callback.data in ["apartment", "house", "comm_apartment"]:
        catalog.edit(callback,  {"type": callback.data})
        catalog.select_location(callback)

    #* callback при выборе расположения жилья в каталоге
    elif callback.data in ["in_the_mountains", "by_the_sea"]:
        catalog.edit(callback, {"location":callback.data})
        catalog.select_sum(callback)

    #* callback при выборе суммы жилья в каталоге
    elif callback.data in ["sum-1", "sum-2", "sum-3", "sum-4"]:
        catalog.edit(callback=callback, edit={"sum": callback.data[-1]})

    #* Возвращение к 1-й странице каталога
    elif callback.data == "back-to-catalog-1":
        catalog.start(message=callback, back=True)
    
    #* Возвращение ко 2-й странице каталога
    elif callback.data == "back-to-catalog-2":
        catalog.select_location(callback)

    #* Возвращение к 3-й странице каталога
    elif callback.data == "back-to-catalog-3":
        catalog.select_sum(callback)

    # TODO callback Панели администратора
    #* callback-и для добавления апартаментов
    elif callback.data in ["add-apartment", "admin-add-back-to-1"]:
        admin.admin_apartment.add_apartment_start(callback)
    
    elif callback.data in ["admin-add-back-to-2","admin-add-apartment", "admin-add-house", "admin-add-comm_apartment"]:
        admin.admin_apartment.add_apartment_2(callback=callback)

    elif callback.data in ["admin-add-back-to-3","admin-add-in_the_mountains", "admin-add-by_the_sea"]:
        admin.admin_apartment.add_apartment_3(callback=callback)
    
    elif callback.data in ["admin-add-back-to-4", "admin-add-sum-1", "admin-add-sum-2", "admin-add-sum-3", "admin-add-sum-4"]:
        admin.admin_apartment.add_apartment_4(callback=callback)
        admin_wait_add_name.append(callback.message.chat.id)
    elif callback.data == "admin-add-back-to-5":
        admin_wait_add_name.remove(callback.message.chat.id)
        admin_wait_add_description.append(callback.message.chat.id)
        admin.admin_apartment.add_apartment_5(callback, back=True)

    elif callback.data == "edit-apartment":
        admin.admin_apartment.edit_apartment_start(callback)
    
    elif callback.data == "delete-apartment": 
        admin.admin_apartment.delete_apartment_start(callback)

    elif callback.data == "get-user-list":
        admin.admin_user.get_list_user_start(callback)
    
    elif callback.data == "edit-user-info":
        admin.admin_user.edit_user_start(callback)
    
    elif callback.data == "delete-user-info":
        admin.admin_user.delete_user_start(callback)

    elif callback.data == "admin-back-to-main":
        admin.main_admin_menu(message=callback, back=True)



@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, 
                     text="<b>"+text["help"]+f"{'<br>/admin-панель администратора' if admin.check_on_admin(message.chat.id) else ''}"+"</b>", 
                     parse_mode="HTML")
bot.infinity_polling()