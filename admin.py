import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from database import database

class admin_panel():
    def __init__(self, bot, text, token):
        self.bot = bot
        self.text = text
        self.token = token
        self.db = database()
        self.msg = {}#{"id":message}
        self.admin_apartment=admin_apartment(bot, text)
        self.admin_user = admin_user(bot, text)


    def add_to_admin(self, message):
        self.db.add_admin({"id":message.chat.id, "contact":"@"+message.from_user.username})

    def check_on_admin(self,id):
        admin_list=self.db.get_column(name="admin", column="id")
        if id in admin_list:
            return True
        else:
            return False
    
    def get_password_admin(self, message):
        if self.check_on_admin(message.chat.id):
            self.main_admin_menu(message)
        else:
            msg = self.bot.send_message(chat_id=message.chat.id, 
                                text="<b>Введите пароль от панели администратора👇</b>",
                                parse_mode="HTML")
            self.msg[message.chat.id] = msg
        

    def main_admin_menu(self, message):
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="Добавить апартаменты", callback_data="add-apartment")
        b2 = InlineKeyboardButton(text="Изменить настройки апартаментов", callback_data="edit-apartment")
        b3 = InlineKeyboardButton(text="Удалить апартаменты", callback_data="delete-apartment")
        b4 = InlineKeyboardButton(text="Получить список пользователей", callback_data="get-user-list")
        b5 = InlineKeyboardButton(text="Изменить данные пользователя", callback_data="edit-user-info")
        b6 = InlineKeyboardButton(text="Удалить данные о пользователе", callback_data="delete-user-info")
        kb.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6)

        msg = self.bot.send_message(chat_id=message.chat.id,
                                    reply_markup=kb, 
                                    text="<b>"+self.text["admin-panel-start"]+"</b>",
                                    parse_mode="HTML")
        self.msg[message.chat.id] = msg
        # self.bot.edit_message_text(chat_id=callback.message.chat.id, 
        #                             message_id=self.msg[message.message.chat.id].message_id, 
        #                             text = "<b>"+self.text["catalog-1"]+"</b>", 
        #                             reply_markup=kb, 
        #                             parse_mode="HTML")
    


class admin_apartment():
    def __init__(self, bot, text):
        self.db = database()
        self.bot = bot
        self.text = text
        self.db = {}#{"id": message}

    def add_apartment_start(self, callback):
        self.bot.edit_message_text(chat_id=callback.message.chat.id, 
                                    message_id=callback.message.message_id, 
                                    text = "<b>"+self.text["catalog-1"]+"</b>",
                                    parse_mode="HTML")

    def edit_apartment_start(self, callback):
        print("edit_apartment_start")


    def delete_apartment_start(self, callback):
        print("delete_apartment_start")
    



class admin_user():
    def __init__(self, bot, text):
        self.db = database()
    

    def get_list_user_start(self, callback):
        print("get_list_user_start")
    

    def edit_user_start(self, callback):
        print("edit_user_start")


    def delete_user_start(self, callback):
        print("delete_user_start")
