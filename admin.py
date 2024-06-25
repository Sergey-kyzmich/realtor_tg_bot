import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from database import database

class admin_panel():
    def __init__(self, bot, text, token):
        self.bot = bot
        self.text = text
        self.token = token
        self.db = database()
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
            self.main_admin_menu(message, back=False)
        else:
            self.bot.send_message(chat_id=message.chat.id, 
                                text="<b>Введите пароль от панели администратора👇</b>",
                                parse_mode="HTML")
        

    def main_admin_menu(self, message, back):
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="Добавить апартаменты", callback_data="add-apartment")
        b2 = InlineKeyboardButton(text="Изменить настройки апартаментов", callback_data="edit-apartment")
        b3 = InlineKeyboardButton(text="Удалить апартаменты", callback_data="delete-apartment")
        b4 = InlineKeyboardButton(text="Получить список пользователей", callback_data="get-user-list")
        b5 = InlineKeyboardButton(text="Изменить данные пользователя", callback_data="edit-user-info")
        b6 = InlineKeyboardButton(text="Удалить данные о пользователе", callback_data="delete-user-info")
        kb.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6)

        if not(back):self.bot.send_message(chat_id=message.chat.id,
                                    reply_markup=kb, 
                                    text="<b>"+self.text["admin-panel-start"]+"</b>",
                                    parse_mode="HTML")
        #* callback->message
        else: self.bot.edit_message_text(chat_id = message.message.chat.id,
                                         message_id=message.message.message_id,
                                         text = "<b>"+self.text["admin-panel-start"]+"</b>",
                                         reply_markup=kb,
                                         parse_mode="HTML")



class admin_apartment():
    def __init__(self, bot, text):
        self.db = database()
        self.bot = bot
        self.text = {
            "add-start":"Выберите тип недвижимости:",
            "add-2":"Выберите расположение:",
            "add-3":"Выберите ценовой диапозон:",
            "add-4":"Введите название:",
            "add-5":"Введите описание:",
            "add-6":"Отправьте фотографии(одним сообщением):",
            "add-7-ok":"Отлично! Апартаменты добавлены.",
            "add-7-error":"Апартаменты добавлены. Нету фотографий.(их можно добавить в меню изменения апартаментов)"
        }
        
    def add_apartment_start(self, callback):
        if callback.data !="admin-add-back-to-1":self.select = {
                                                    "location": "",
                                                    "type": "",
                                                    "sum": "",
                                                    "description":"",
                                                    "name":""
                                                    }
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="🏢Квартира", callback_data=f"admin-add-apartment")
        b2 = InlineKeyboardButton(text="🏠Дом", callback_data=f"admin-add-house")
        b3 = InlineKeyboardButton(text="🏛Коммерческая недвижимость", callback_data=f"admin-add-comm_apartment")
        b4 = InlineKeyboardButton(text="⬅️Назад", callback_data="admin-back-to-main")
        kb.add(b1,b2).add(b3).add(b4)

        self.bot.edit_message_text(chat_id=callback.message.chat.id, 
                                    message_id=callback.message.message_id, 
                                    text = "<b>"+self.text["add-start"]+"</b>",
                                    reply_markup=kb,
                                    parse_mode="HTML")

    def add_apartment_2(self, callback):
        if callback.data !="admin-add-back-to-2":self.select["type"]=callback.data.replace("admin-add-", "")
        
        kb = InlineKeyboardMarkup()
        b2 = InlineKeyboardButton(text="⛰️В горах", callback_data=f"admin-add-in_the_mountains")
        b1 = InlineKeyboardButton(text="🏖️У моря", callback_data=f"admin-add-by_the_sea")
        b3 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-add-back-to-1")
        kb.add(b1,b2).add(b3)
        self.bot.edit_message_text(chat_id = callback.message.chat.id, 
                                    message_id=callback.message.message_id, 
                                    text="<b>"+self.text["add-2"]+"</b>", 
                                    reply_markup=kb, 
                                    parse_mode="HTML")
    
    
    def add_apartment_3(self, callback):
        if callback.data !="admin-add-back-to-3":self.select["location"] = callback.data.replace("admin-add-", "")
        text_button = [
            ["До 20 млн руб", "До 50 млн руб", "До 100 млн руб", "От 100 млн руб"],
            ["До 50 млн руб", "До 100 млн руб", "До 500 млн руб", "От 500 млн руб"],
            ["До 100 млн руб", "До 500 млн руб", "От 500 млн руб"]
        ]
        if self.select["type"]=="apartment":text_button = text_button[0]
        elif self.select["type"]=="house":text_button = text_button[1]
        else:text_button = text_button[2]

        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text=text_button[0], 
                                  callback_data=f"admin-add-sum-1")
        b2 = InlineKeyboardButton(text=text_button[1], 
                                  callback_data=f"admin-add-sum-2")
        b3 = InlineKeyboardButton(text=text_button[2], 
                                  callback_data=f"admin-add-sum-3")
        if self.select["type"]=="comm_apartment":kb.add(b1,b2);kb.add(b3)
        else:
            b4 = InlineKeyboardButton(text=text_button[3], callback_data=f"admin-add-sum-4")
            kb.add(b1,b2)
            kb.add(b3,b4)
        b5 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-add-back-to-2")
        kb.add(b5)
        self.bot.edit_message_text(chat_id = callback.message.chat.id, 
                                    message_id=callback.message.message_id, 
                                    text="<b>"+self.text["add-3"]+"</b>", 
                                    reply_markup=kb, 
                                    parse_mode="HTML")
    
    
    def add_apartment_4(self, callback):
        if callback.data !="admin-add-back-to-4": self.select["sum"]=callback.data.replace("admin-add-","")
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-add-back-to-3")
        kb.add(b1)
        self.bot.edit_message_text(chat_id = callback.message.chat.id, 
                                    message_id=callback.message.message_id, 
                                    text="<b>"+self.text["add-4"]+"</b>", 
                                    reply_markup=kb, 
                                    parse_mode="HTML")

    def add_apartment_5(self, message, back):
        if not(back):self.select["name"]=message.text     
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-add-back-to-4")
        kb.add(b1) 
        
        if not(back):           
            self.bot.edit_message_text(chat_id = message.chat.id, 
                                    message_id=message.message_id, 
                                    text="<b>"+self.text["add-5"]+"</b>", 
                                    reply_markup=kb, 
                                    parse_mode="HTML")
        else:
            self.bot.edit_message_text(chat_id=message.message.chat.id, 
                                    message_id=message.message.message_id, 
                                    text = "<b>"+self.text["add-start"]+"</b>",
                                    reply_markup=kb,
                                    parse_mode="HTML")
        

    def add_apartment_6(self, message):
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-add-back-to-5")
        kb.add(b1)            
        self.bot.send_message(chat_id = message.chat.id, 
                            text="<b>"+self.text["add-6"]+"</b>", 
                            reply_markup=kb, 
                            parse_mode="HTML")
    
    def add_apartment_7(self, message):#получение фотографий
        print(self.select)
    
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
