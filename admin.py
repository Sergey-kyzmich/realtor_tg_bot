import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from database import database
import os
import shutil
import json
import datetime

class admin_panel():
    def __init__(self, bot, text, token):
        self.bot = bot
        self.text = text
        self.token = token
        self.db = database()
        self.admin_apartment=admin_apartment(bot, text)
        self.admin_user = admin_user(bot, text)


    def check_user(self, message):
        names=[]
        for item in self.db.get_all("user"):
            if message.chat.id == item[0]:
                return self.db.edit(name="user", id=message.chat.id, data={"last_use":datetime.datetime.now()})
        #Не нашлось такого элемента
        self.db.add_user(user={
            "id":message.chat.id,
            "phone":"",
            "name":message.from_user.username,
            "last_use":datetime.datetime.now()})
            


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
        b2 = InlineKeyboardButton(text="Посмотреть карточку апартаментов", callback_data="show-apartment")
        b3 = InlineKeyboardButton(text="Изменить настройки апартаментов", callback_data="edit-apartment-start")
        b4 = InlineKeyboardButton(text="Удалить апартаменты", callback_data="delete-apartment")
        b5 = InlineKeyboardButton(text="Получить список пользователей", callback_data="get-user-list")
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
        self.msg={}
        self.old_text=text
        self.select={}
        self.apartments={}
        self.delete_apartments={}
        self.select_name={}
        self.photo_to_edit={}
        self.show_photo_img={}
        self.text = {
            "add-start":"Выберите тип недвижимости:",
            "add-2":"Выберите расположение:",
            "add-3":"Выберите ценовой диапозон:",
            "add-4":"Введите название (Должно содержать минимум одну букву):",
            "add-5":"Введите описание:",
            "add-6":"Отправьте фотографии(без сжатия/группировки):",
            "add-7-ok":"Отлично! Апартаменты добавлены.",
            "add-7-error":"Апартаменты добавлены. Нету фотографий.(их можно добавить в меню изменения апартаментов)",

            "edit-1": "Выберите апартаменты, которые хотите изменить👇",
            "edit-2": "Выберите параметр, который хотите изменить👇",
            "edit-3-type": "Выберите тип недвижимости, на который желаете заменить👇",
            "edit-3-location":"Выберите расположение недвижимости, на которое желаете заменить👇",
            "edit-3-sum":"Выберите ценовой диапазон, на который желаете заменить👇",
            "edit-3-name":"Введите новое название:",
            "edit-3-description":"Введите новое описание:",
            "edit-3-photo":"Отправьте фотографии(без сжатия/группировки):",
            "edit-4-type":"Отлично! тип недвижимости обновлен.",
            "edit-4-location":"Отлично! расположение недвижимости обновлено.",
            "edit-4-sum":"Отлично! ценовая категория обновлена.",
            "edit-4-name":"Отлично! название обновлено.",
            "edit-4-description":"Отлично! описание обновлено.",
            "edit-4-photo":"Отлично! список фотографий обновлен.",
            "show-1": "Выберите апартаменты, которые желаете посмотреть👇",
            "delete-1":"Выберите апартаменты, которые желаете удалить👇",
            "delete-2":"Апартаменты успешно удалены!"
        }
    
    #! функции для добавления новых апартаментов
    def add_to_photo_list(self, message, key):
        print(message.document)
        file_path = self.bot.get_file(message.document.file_id).file_path
        if key == "to-add":self.select[message.chat.id]["photo"].append(self.bot.download_file(file_path))
        elif key == "to-edit":
            print("to-edit")
            if message.chat.id not in self.photo_to_edit:
                self.photo_to_edit[message.chat.id]=[]
                print("create-id")
            self.photo_to_edit[message.chat.id].append(self.bot.download_file(file_path))
        
    def save_photo(self, list_photo, name):

        if not(os.path.exists(os.getcwd()+f"\\database_photo\\{name}")):
            os.mkdir(f"{os.getcwd()}\\database_photo\\{name}")
        k=0
        photo_dir=[]
        for img in list_photo:
            print(len(img))
            print(type(img))
            k+=1
            # print(img)
            # print(type(img))
            with open(f"{os.getcwd()}\\database_photo\\{name}\\{k}.png", "wb") as write:
                write.write(img)
            print(f'save to: {os.getcwd()}/database_photo/{name}/{k}.png')
            photo_dir.append(os.getcwd()+f"\\database_photo\\{name}\\{k}.png")
        return photo_dir
    

    def delete_photo_in_folder(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def add_apartment_start(self, callback):
        if callback.message.chat.id not in self.select:self.select[callback.message.chat.id]={"type":"",
                                                                                                "sum":"",
                                                                                                "location":"",
                                                                                                "name":"",
                                                                                                "description":"",
                                                                                                "photo":[]}
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
        if callback.data !="admin-add-back-to-2":self.select[callback.message.chat.id]["type"]=callback.data.replace("admin-add-", "")
        
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
        if callback.data !="admin-add-back-to-3":self.select[callback.message.chat.id]["location"] = callback.data.replace("admin-add-", "")
        text_button = [
            self.old_text["but-sum-apartment"],
            self.old_text["but-sum-house"],
            self.old_text["but-sum-comm_apartment"]
        ]
        if self.select[callback.message.chat.id]["type"]=="apartment":text_button = text_button[0]
        elif self.select[callback.message.chat.id]["type"]=="house":text_button = text_button[1]
        else:text_button = text_button[2]

        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text=text_button[0], 
                                  callback_data=f"admin-add-sum-1")
        b2 = InlineKeyboardButton(text=text_button[1], 
                                  callback_data=f"admin-add-sum-2")
        b3 = InlineKeyboardButton(text=text_button[2], 
                                  callback_data=f"admin-add-sum-3")
        if self.select[callback.message.chat.id]["type"]=="comm_apartment":kb.add(b1,b2);kb.add(b3)
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
        if callback.data !="admin-add-back-to-4": self.select[callback.message.chat.id]["sum"]=callback.data.replace("admin-add-","")
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-add-back-to-3")
        kb.add(b1)
        msg = self.bot.edit_message_text(chat_id = callback.message.chat.id, 
                                    message_id=callback.message.message_id, 
                                    text="<b>"+self.text["add-4"]+"</b>", 
                                    reply_markup=kb, 
                                    parse_mode="HTML")
        self.msg[callback.message.chat.id]=msg


    def add_apartment_5(self, message, back):
        if not(back):self.select[message.chat.id]["name"]=message.text     
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-add-back-to-4")
        kb.add(b1) 
        
        if not(back):           
            self.bot.send_message(chat_id = message.chat.id, 
                                    text="<b>"+self.text["add-5"]+"</b>", 
                                    reply_markup=kb, 
                                    parse_mode="HTML")
        else:
            self.bot.edit_message_text(chat_id=message.message.chat.id, 
                                    message_id=message.message.message_id, 
                                    text = "<b>"+self.text["add-5"]+"</b>",
                                    reply_markup=kb,
                                    parse_mode="HTML")
        

    def add_apartment_6(self, message):
        self.select[message.chat.id]["description"]=message.text     
        
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="Все фотографии загружены", callback_data="admin-add-load-photo-end")
        b2 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-add-back-to-5")
        
        kb.add(b1).add(b2)           
        msg = self.bot.send_message(chat_id = message.chat.id, 
                            text="<b>"+self.text["add-6"]+"</b>", 
                            reply_markup=kb, 
                            parse_mode="HTML")
        
        self.msg[message.chat.id]=msg
    
    def add_apartment_7(self, callback):#получение фотографий
        self.select[callback.message.chat.id]["photo"] = self.save_photo(self.select[callback.message.chat.id]["photo"], 
                                                                         self.select[callback.message.chat.id]["name"])
        
        self.db.add_apartment(self.select[callback.message.chat.id])
        
        self.select[callback.message.chat.id]={"type":"","sum":"","location":"","name":"","description":"","photo":[]}
        
        self.bot.send_message(chat_id=callback.message.chat.id, 
                              text="<b>"+self.text["add-7-ok" if self.select[callback.message.chat.id]["photo"]!=[] else "add-7-error"]+"</b>",
                              parse_mode="HTML")
        
        #Изменение сообщения с ожиданием фотогграфий(чтобы кнопка не моргала)
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="Все фотографии загружены", callback_data="None")
        b2 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"None")
        kb.add(b1).add(b2)           
        self.bot.edit_message_text(chat_id = callback.message.chat.id,
                            message_id = callback.message.message_id, 
                            text="<b>"+self.text["add-6"]+"</b>", 
                            reply_markup=kb, 
                            parse_mode="HTML")
        
    #!Окончание функций добоавления апартаментов

    #!Начало функций изменения
    def edit_apartment_start(self, callback):
        kb = InlineKeyboardMarkup()
        self.apartments[callback.message.chat.id] = {}
        for item in self.db.get_all(name="apartment"):
            self.apartments[callback.message.chat.id][item[0]] = {
                "name":item[0],
                "type":item[1],
                "location":item[2],
                "sum": item[3],
                "description":item[4],
                "photo":json.loads(item[5])
            }
        for item in self.apartments[callback.message.chat.id]:
            b = InlineKeyboardButton(text=f"{item}", callback_data=f"edit-apartment-this-name-{item}")
            kb.add(b)
        
        b = InlineKeyboardButton(text="⬅️Назад", callback_data="admin-back-to-main")
        kb.add(b)

        self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                   message_id=callback.message.message_id,
                                   text="<b>"+self.text["edit-1"]+"</b>",
                                   reply_markup=kb, 
                                   parse_mode="HTML")
        
    
    def edit_apartment_2(self, callback):
        if not(callback.message.chat.id in self.select_name):
            self.select_name[callback.message.chat.id] = callback.data.replace("edit-apartment-this-name-", "")

        elif callback.data != "admin-edit-back-to-2":
            self.select_name[callback.message.chat.id] = callback.data.replace("edit-apartment-this-name-", "")
   
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="Тип недвижимости", callback_data=f"edit-select-type")
        b2 = InlineKeyboardButton(text="Расположение недвижимости", callback_data=f"edit-select-location")
        b3 = InlineKeyboardButton(text="Ценовой диапазон", callback_data=f"edit-select-sum")
        b4 = InlineKeyboardButton(text="Название", callback_data=f"edit-select-name")
        b5 = InlineKeyboardButton(text="Описание", callback_data=f"edit-select-description")
        b6 = InlineKeyboardButton(text="Фотографии", callback_data=f"edit-select-photo")
        
        kb.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6)
        b = InlineKeyboardButton(text="⬅️Назад", callback_data="admin-edit-back-to-1")
        kb.add(b)

        self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                   message_id=callback.message.message_id,
                                   text="<b>"+self.text["edit-2"]+"</b>",
                                   reply_markup=kb,
                                   parse_mode="HTML")
    
    def edit_apartment_3(self, callback):
        id = callback.data.split("-")[-1]

        if id == "location":#изменить тип
            kb = InlineKeyboardMarkup() 
            b2 = InlineKeyboardButton(text="⛰️В горах", callback_data=f"admin-edit-3-in_the_mountains")
            b1 = InlineKeyboardButton(text="🏖️У моря", callback_data=f"admin-edit-3-by_the_sea")
            b3 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-edit-back-to-2")
            kb.add(b2, b1).add(b3)
            text = self.text["edit-3-location"]
        elif id == "type":
            kb = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text="🏢Квартира", callback_data=f"admin-edit-3-apartment")
            b2 = InlineKeyboardButton(text="🏠Дом", callback_data=f"admin-edit-3-house")
            b3 = InlineKeyboardButton(text="🏛Коммерческая недвижимость", callback_data=f"admin-edit-3-comm_apartment")
            b4 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-edit-back-to-2")
            kb.add(b1,b2).add(b3).add(b4)
        
            text = self.text["edit-3-type"]
    
        elif id == "sum":
            text_button = [
            self.old_text["but-sum-apartment"],
            self.old_text["but-sum-house"],
            self.old_text["but-sum-comm_apartment"]
            ]
            select_type = self.apartments[
                                        callback.message.chat.id
                                            ][
                                            self.select_name[
                                                callback.message.chat.id
                                            ]
                                        ][
                                            "type"
                                        ]
            if select_type=="apartment":text_button = text_button[0]
            elif select_type=="house":text_button = text_button[1]
            else:text_button = text_button[2]

            kb = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text=text_button[0], 
                                    callback_data=f"admin-edit-3-sum-1")
            b2 = InlineKeyboardButton(text=text_button[1], 
                                    callback_data=f"admin-edit-3-sum-2")
            b3 = InlineKeyboardButton(text=text_button[2], 
                                    callback_data=f"admin-edit-3-sum-3")
            if select_type=="comm_apartment":kb.add(b1,b2);kb.add(b3)
            else:
                b4 = InlineKeyboardButton(text=text_button[3], callback_data=f"admin-edit-3-sum-4")
                kb.add(b1,b2)
                kb.add(b3,b4)
            b5 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-edit-back-to-2")
            kb.add(b5)

            text = self.text["edit-3-sum"]
        
        elif id == "name":
            kb = InlineKeyboardMarkup()
            b5 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-edit-back-to-2")
            kb.add(b5)

            text = self.text["edit-3-name"]
        
        elif id == "description":
            kb = InlineKeyboardMarkup()
            b5 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-edit-back-to-2")
            kb.add(b5)

            text = self.text["edit-3-description"]

        elif id == "photo":
            kb = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text="Все фотографии загружены", callback_data="admin-edit-photo-load-end")
            b2 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"admin-edit-back-to-2")
            
            kb.add(b1).add(b2)
            text = self.text["edit-3-photo"]
        
        self.bot.edit_message_text(chat_id = callback.message.chat.id,
                                   message_id = callback.message.message_id,
                                   text = "<b>"+text+"</b>",
                                   reply_markup=kb,
                                   parse_mode="HTML")
    
    def edit_apartment_4(self, callback, key):
        if key in ["-apartment", "-house", "-comm_apartment"]:
            self.db.edit(name="apartment", id=self.select_name[callback.message.chat.id], data={"type":key[1:]})
            text = self.text["edit-4-type"]
        elif key in ["-in_the_mountains","-by_the_sea"]:
            self.db.edit(name="apartment", id=self.select_name[callback.message.chat.id], data={"location":key[1:]})
            text = self.text["edit-4-location"]
        elif key in ["-sum-1","-sum-2","-sum-3","-sum-4"]:
            self.db.edit(name="apartment", id=self.select_name[callback.message.chat.id], data={"sum":key[1:]})
            text = self.text["edit-4-sum"]
        elif key == "name":
            #  изменение дериктории
            old_name = os.getcwd().replace("\\", "/")+f"/database_photo/{self.select_name[callback.chat.id]}"
            new_name = os.getcwd().replace("\\", "/")+f"/database_photo/{callback.text}"
            os.rename(old_name, new_name)
            self.select_name[callback.chat.id]=callback.text

            self.db.edit(name="apartment", id=self.select_name[callback.chat.id], data={"name":callback.text})
            text = self.text["edit-4-name"]
        elif key == "description":
            self.db.edit(name="apartment", id=self.select_name[callback.chat.id], data={"description":callback.text})
            text = self.text["edit-4-description"]
        elif key=="photo":
            # for i in self.photo_to_edit:print(f"{i=}")
            self.delete_photo_in_folder(f"{os.getcwd()}/database_photo/{self.select_name[callback.message.chat.id]}")
            self.photo_to_edit[callback.message.chat.id] = self.save_photo(self.photo_to_edit[callback.message.chat.id], 
                                                                         self.select_name[callback.message.chat.id])
        
            photo_in_text= json.dumps(self.photo_to_edit[callback.message.chat.id])
            

            self.db.edit(name="apartment", id=self.select_name[callback.message.chat.id], data={"photo":photo_in_text})
            self.photo_to_edit[callback.message.chat.id]=[]
            text = self.text["edit-4-photo"]
            print("ok")
        
        if key not in ["name","description"]:
            self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text = "<b>"+text+"</b>",
                                        parse_mode="HTML")
        elif key=="photo":
            self.bot.send_message(chat_id=callback.message.chat.id,
                                        text = "<b>"+text+"</b>",
                                        parse_mode="HTML")

        else:
            self.bot.send_message(chat_id=callback.chat.id,
                                        text = "<b>"+text+"</b>",
                                        parse_mode="HTML")



    def show_apartment_start(self, callback):

        self.apartments[callback.message.chat.id] = {}
        kb = InlineKeyboardMarkup()
        for item in database.get_all("None", name="apartment"):
            self.apartments[callback.message.chat.id][item[0]] = {
                "name":item[0],
                "type":item[1],
                "location":item[2],
                "sum": item[3],
                "description":item[4],
                "photo":json.loads(item[5])
            }
        for item in self.apartments[callback.message.chat.id]:
            b = InlineKeyboardButton(text=f"{item}", callback_data=f"show-apartment-this-name-{item}")
            kb.add(b)
        
        b = InlineKeyboardButton(text="⬅️Назад", callback_data="admin-back-to-main")
        kb.add(b)

        self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                   message_id=callback.message.message_id,
                                   text="<b>"+self.text["show-1"]+"</b>",
                                   reply_markup=kb, 
                                   parse_mode="HTML")
        
        
        if callback.message.chat.id in self.show_photo_img:
            if self.show_photo_img[callback.message.chat.id] != []:
                for msg in self.show_photo_img[callback.message.chat.id]:
                    self.bot.delete_message(chat_id=callback.message.chat.id, message_id=msg.message_id)
                self.show_photo_img[callback.message.chat.id]=[]
        
    def show_apartment_2(self, callback):
        name = callback.data.replace("show-apartment-this-name-", "")
        print(self.apartments[callback.message.chat.id])
        apartment = self.apartments[callback.message.chat.id][name]

        # Замена callback названий на Русские
        apartment["type"] = apartment["type"].replace("comm_apartment", "Коммерческая недвижимость").replace("apartment", "Квартира").replace("house", "Дом")
        apartment["location"] = apartment["location"].replace("by_the_sea", "У моря").replace("in_the_mountains", "В горах")
        if apartment["type"]=="Квартира":apartment["sum"]=apartment["sum"].replace("sum-1", "До 20 млн руб").replace("sum-2", "До 50 млн руб").replace("До 100 млн руб", "От 100 млн руб")
        if apartment["type"]=="Дом":apartment["sum"]=apartment["sum"].replace("sum-1", "До 50 млн руб").replace("sum-2", "До 100 млн руб").replace("До 500 млн руб", "От 500 млн руб")
        else:apartment["sum"]=apartment["sum"].replace("sum-1", "До 100 млн руб").replace("sum-2", "До 500 млн руб").replace("От 500 млн руб", "От 100 млн руб")
        
        
        text =f"""
Карточка апартаментов с названием: {apartment['name']}

Тип: {apartment['type']}
Расположение: {apartment['location']}
Ценовая категория: {apartment['sum']}

Описание:
{apartment['description']}

""" 
        kb = InlineKeyboardMarkup()
        b = InlineKeyboardButton(text="⬅️Назад", callback_data="show-apartment")
        kb.add(b)
        self.bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text = "<b>"+text+"</b>", reply_markup=kb, parse_mode="HTML")
        if len(apartment['photo'])>=1:
            self.show_photo_img[callback.message.chat.id]=self.bot.send_media_group(chat_id=callback.message.chat.id, media=[telebot.types.InputMediaPhoto(open(dir, 'rb')) for dir in apartment['photo']])
            # print(self.show_photo_img[callback.message.chat.id].message_id)
        


    def delete_apartment_start(self, callback):
        kb = InlineKeyboardMarkup()
        self.delete_apartments[callback.message.chat.id] = {}
        for item in database.get_all("None", name="apartment"):
            self.delete_apartments[callback.message.chat.id][item[0]] = {
                "name":item[0],
                "type":item[1],
                "location":item[2],
                "sum": item[3],
                "description":item[4],
                "photo":json.loads(item[5])
            }


        for item in self.delete_apartments[callback.message.chat.id]:
            b = InlineKeyboardButton(text=f"{item}", callback_data=f"delete-apartment-this-name-{item}")
            kb.add(b)
        
        b = InlineKeyboardButton(text="⬅️Назад", callback_data="admin-back-to-main")
        kb.add(b)

        self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                   message_id=callback.message.message_id,
                                   text="<b>"+self.text["delete-1"]+"</b>",
                                   reply_markup=kb, 
                                   parse_mode="HTML")
        
    def delete_apartment_2(self, callback):
        name = callback.data.replace("delete-apartment-this-name-", "")
        self.db.delete(id=name, name="apartment")
        self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                   message_id=callback.message.message_id,
                                   text="<b>"+self.text["delete-2"]+"</b>",
                                   parse_mode="HTML")



class admin_user():
    def __init__(self, bot, text):
        self.db = database()
        self.bot = bot
        self.text={
            "delete-1":"Выберите имя пользователя, которого хотите удалить из базы данных👇",
            "delete-2":"Пользователь успешло удален!"
        }
    

    def get_list_user_start(self, callback):
        users={}
        for item in self.db.get_all("user"):
            users[str(item[0])] = {
                "id":item[0],
                "phone":item[1],
                "name":item[2],
                "last_use":item[3]
            }
        text="Список пользователей:"
        for i in users:
            text+=f"""

Имя:@{users[i]['name']}
Номер телефона: {'None' if users[i]['phone']=='' else users[i]['phone']}
Последний раз был в сети: {users[i]['last_use']}
ID чата с пользователем: {users[i]['id']}"""
            
        kb = InlineKeyboardMarkup()
        b = InlineKeyboardButton(text="⬅️Назад", callback_data="admin-back-to-main")
        kb.add(b)
        self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id,
                                    text="<b>"+text+"</b>",
                                    reply_markup=kb,
                                    parse_mode="HTML")

    def delete_user_start(self, callback):
        kb = InlineKeyboardMarkup()
        for item in self.db.get_all("user"):
            b = InlineKeyboardButton(text=item[2], callback_data=f"delete-user-this-name-{item[2]}")
            kb.add(b)
        b = InlineKeyboardButton(text="⬅️Назад", callback_data="admin-back-to-main")
        kb.add(b)

        self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                   message_id=callback.message.message_id,
                                   text="<b>"+self.text["delete-1"]+"</b>",
                                   reply_markup=kb,
                                   parse_mode="HTML")
        
    def delete_user_2(self, callback):
        name_user=callback.data.replace("delete-user-this-name-", "")
        for item in self.db.get_all("user"):
            if item[2]==name_user:
                id_user=item[0]
        self.db.delete(id=id_user, name="user")

        self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                   message_id=callback.message.message_id,
                                   text="<b>"+self.text["delete-2"]+"</b>",
                                   parse_mode="HTML")
