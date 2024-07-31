import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import threading
from text import text
from catalog import init_catalog
from tk import token
from admin import admin_panel
from check_last_use import check_last_use
#Константы
bot=telebot.TeleBot(token)
catalog = init_catalog(bot, text)
admin = admin_panel(bot, text, token)
#Системные переменные
wait_password = []
admin_wait_add_description = []
admin_wait_add_name = []
admin_wait_add_photo = []

admin_edit_wait_name = []
admin_edit_wait_description = []
admin_edit_wait_photo = []

#Создание потока
thread = threading.Thread(target=check_last_use,args=(bot,), daemon=True)
thread.start()

#Функции
@bot.message_handler(commands=['start'])
def start_message(message):
    #проверка на наличие пользователя в базе данных
    admin.check_user(chat_id=message.chat.id, username=message.from_user.username)

    main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    mb_1 = KeyboardButton(text="Каталог")
    mb_2 = KeyboardButton(text="Ссылка на блог")
    mb_3 = KeyboardButton(text="Ссылка на специалиста")
    main_kb.add(mb_1, mb_2, mb_3)
    kb_catalog= InlineKeyboardMarkup()
    bc=InlineKeyboardButton(text="НАЧАТЬ ПОИСК", callback_data="start_catalog")
    kb_catalog.add(bc)
    bot.send_photo(message.chat.id, photo=open('./database_photo/media/start.jpg', 'rb'),
                     reply_markup=main_kb)
    bot.send_message(message.chat.id, 
                     "<b>"+text["start"]+"</b>",
                     reply_markup=kb_catalog,
                     parse_mode="HTML")


@bot.message_handler(commands=["admin"])
def admin_start(message):
    if not(admin.check_on_admin(message.chat.id)):
        wait_password.append(message.chat.id)
    admin.get_password_admin(message)


@bot.message_handler(commands=["help"])
def help(message):
    print("help")
    admin.check_user(chat_id=message.chat.id, username=message.from_user.username)
    bot.send_message(message.chat.id, 
                     text="<b>"+text["help"]+f"\n{'/admin-панель администратора' if admin.check_on_admin(message.chat.id) else ''}"+"</b>", 
                     parse_mode="HTML")

#!Обработчик фотографий
@bot.message_handler(content_types=["document"])
def photo_message_handler(message):
    admin.check_user(chat_id=message.chat.id, username=message.from_user.username)
    if message.chat.id in admin_wait_add_photo:
        admin.admin_apartment.add_to_photo_list(message, key="to-add")
    
    elif message.chat.id in admin_edit_wait_photo:
        admin.admin_apartment.add_to_photo_list(message, key="to-edit")

#! Обработчик текстовых сообщений
@bot.message_handler(content_types="text")
def text_message_handler(message):
    admin.check_user(chat_id=message.chat.id, username=message.from_user.username)
    if message.chat.id in wait_password and message.chat.id not in ["Каталог", "Ссылка на блог", "Ссылка на специалиста"]:
        if message.chat.id in wait_password:
            wait_password.remove(message.chat.id)
        if message.text==token:
            admin.add_to_admin(message)
            admin.main_admin_menu(message, back=False)
        else:
            bot.send_message(chat_id=message.chat.id, text="<b>Пароль неверный</b>", parse_mode="HTML")
    
    elif message.chat.id in admin_wait_add_name and message.chat.id not in ["Каталог", "Ссылка на блог", "Ссылка на специалиста"]:
        if message.chat.id in admin_wait_add_name: 
            admin_wait_add_name.remove(message.chat.id)
        if message.chat.id not in admin_wait_add_description:
            admin_wait_add_description.append(message.chat.id)
        admin.admin_apartment.add_apartment_5(message, back=False)
        
    elif message.chat.id in admin_wait_add_description and message.chat.id not in ["Каталог", "Ссылка на блог", "Ссылка на специалиста"]:
        if message.chat.id in admin_wait_add_description: 
            admin_wait_add_description.remove(message.chat.id)
        if message.chat.id not in admin_wait_add_photo:
            admin_wait_add_photo.append(message.chat.id)
        admin.admin_apartment.add_apartment_6(message)
    
    elif message.chat.id in admin_edit_wait_name and message.chat.id not in ["Каталог", "Ссылка на блог", "Ссылка на специалиста"]:
        admin_edit_wait_name.remove(message.chat.id)
        admin.admin_apartment.edit_apartment_4(message, key="name")

    elif message.chat.id in admin_edit_wait_description and message.chat.id not in ["Каталог", "Ссылка на блог", "Ссылка на специалиста"]:
        admin_edit_wait_description.remove(message.chat.id)
        admin.admin_apartment.edit_apartment_4(message, key="description")

    elif message.text=="Каталог":
        catalog.start(message=message, back=False)
    
    elif message.text=="Ссылка на блог":
        bot.send_message(chat_id=message.chat.id,
                         text="<b>"+text["blog_info"]+"</b>",
                         parse_mode="HTML")
    
    elif message.text=="Ссылка на специалиста":
        bot.send_message(chat_id=message.chat.id,
                         text="<b>"+text["specialist_info"]+"</b>",
                         parse_mode="HTML")


#! ---CALLBACK---
@bot.callback_query_handler(func=lambda  callback: callback.data)
def check_callback_data(callback):
    admin.check_user(chat_id=callback.message.chat.id, username=callback.from_user.username)
    if callback.data=="connect_to_spec":
        bot.send_message(chat_id=callback.message.chat.id,
                         text="<b>"+text["specialist_info"]+"</b>",
                         parse_mode="HTML")

    elif callback.data == "start_catalog":
        catalog.start(message=callback.message, back=False)

    #* callback при выборе типа жилья в каталоге
    elif callback.data in ["apartment", "house", "comm_apartment"]:
        catalog.edit(callback,  {"type": callback.data})
        catalog.select_location(callback)

    #* callback при выборе расположения жилья в каталоге
    elif callback.data in ["in_the_mountains", "by_the_sea"]:
        catalog.edit(callback, {"location":callback.data})
        catalog.select_sum(callback)

    #* callback при выборе суммы жилья в каталоге
    elif callback.data in ["sum-1", "sum-2", "sum-3", "4"]:
        catalog.edit(callback=callback, edit={"sum": callback.data[-1]})
        catalog.show_apartment(callback)
    elif callback.data in ["back-to-past-image", "next-image"]:
        catalog.show_apartment(callback)

    elif "select-apartment-this-name-" in callback.data:
        catalog.select_apartment(callback)

    elif callback.data == "send_select_apartment":
        catalog.send_select_apartment(callback)

    elif callback.data=="delete_select_apartment_menu":
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)    
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
        if callback.message.chat.id not in admin_wait_add_name:
            admin_wait_add_name.append(callback.message.chat.id)
    elif callback.data == "admin-add-back-to-5":
        if callback.message.chat.id in admin_wait_add_name:
            admin_wait_add_name.remove(callback.message.chat.id)
        if callback.message.chat.id not in admin_wait_add_description:
            admin_wait_add_description.append(callback.message.chat.id)
        admin.admin_apartment.add_apartment_5(callback, back=True)

    elif callback.data == "admin-add-load-photo-end":
        if callback.message.chat.id in admin_wait_add_photo: 
            admin_wait_add_photo.remove(callback.message.chat.id)
        admin.admin_apartment.add_apartment_7(callback)


    elif callback.data in ["edit-apartment-start", "admin-edit-back-to-1"]:
        admin.admin_apartment.edit_apartment_start(callback)
    
    #изменение апартаментов 1-2
    elif "edit-apartment-this-name-" in callback.data or callback.data=="admin-edit-back-to-2":
        admin.admin_apartment.edit_apartment_2(callback=callback)

    #изменение апартаментов 2-3
    elif "edit-select-" in callback.data:
        if callback.data.split("-")[-1]=="name":
            admin_edit_wait_name.append(callback.message.chat.id)
        elif callback.data.split("-")[-1]=="description":
            admin_edit_wait_description.append(callback.message.chat.id)
        elif callback.data.split("-")[-1]=="photo":
            admin_edit_wait_photo.append(callback.message.chat.id)
        admin.admin_apartment.edit_apartment_3(callback=callback)

    elif "admin-edit-3-" in callback.data:
        admin.admin_apartment.edit_apartment_4(callback, key=callback.data.replace("admin-edit-3", ""))

    elif callback.data=="admin-edit-photo-load-end":
        if callback.message.chat.id in admin_edit_wait_photo: 
            admin_edit_wait_photo.remove(callback.message.chat.id)
        admin.admin_apartment.edit_apartment_4(callback, key="photo")

    # TODO Окончание callback для изменения

    # TODO Начало callback для показа администратору
    elif callback.data == "show-apartment":
        admin.admin_apartment.show_apartment_start(callback)
    
    if "show-apartment-this-name-" in callback.data:
        admin.admin_apartment.show_apartment_2(callback)
    elif callback.data == "delete-apartment": 
        admin.admin_apartment.delete_apartment_start(callback)

    elif callback.data == "get-user-list":
        admin.admin_user.get_list_user_start(callback)
    
    # TODO callback для удаления карточек апартаментов
    elif callback.data == "delete-user-info":
        admin.admin_user.delete_user_start(callback)

    elif "delete-apartment-this-name-" in callback.data:
        admin.admin_apartment.delete_apartment_2(callback=callback)

    # TODO callback для удаления пользователя
    elif "delete-user-this-name-" in callback.data:
        admin.admin_user.delete_user_2(callback)


    elif callback.data == "admin-back-to-main":
        admin.main_admin_menu(message=callback, back=True)



bot.infinity_polling()