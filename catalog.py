import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from database import database
import json
class init_catalog():
    def __init__(self, bot, text) -> None:
        self.bot = bot
        self.text = text
        self.msg = {}
        self.select = {}#{"",{
            # "location": "",
            # "type": "",
            # "sum": ""#квартиры/дома-1,2,3,4, коммерческое-1,2,3
        # }}
        self.count_show={}
        self.list_show={}
        self.apartment_for_select={}
        self.db = database()
        self.db.create_db()


    def edit(self, callback,edit):
        try:
            if callback.message.chat.id not in self.select:
                self.select[callback.message.chat.id]={
                "location": "",
                "type": "",
                "sum": ""#квартиры/дома-1,2,3,4, коммерческое-1,2,3
            }
            if "location" in edit:self.select[callback.message.chat.id]["location"] = edit["location"]
            elif "type" in edit:self.select[callback.message.chat.id]["type"] = edit["type"]
            else: self.select[callback.message.chat.id]["sum"] = edit["sum"]
        except Exception as e: print("error in catalog/edit:"+str(e))
    def start(self, message, back=bool):
        try:
            #* Создание клавиатуры
            kb = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text="🏢Квартира", callback_data=f"apartment")
            b2 = InlineKeyboardButton(text="🏠Дом", callback_data=f"house")
            b3 = InlineKeyboardButton(text="🏛Коммерческая недвижимость", callback_data=f"comm_apartment")
            kb.add(b1,b2)
            kb.add(b3)
            # if (back): callback->message else: message->message
            if back:
                self.bot.edit_message_text(chat_id=message.message.chat.id, 
                                                message_id=message.message.message_id, 
                                                text = "<b>"+self.text["catalog-1"]+"</b>", 
                                                reply_markup=kb, 
                                                parse_mode="HTML")
            else:
                self.bot.send_message(message.chat.id, 
                                        text="<b>"+self.text["catalog-1"]+"</b>", 
                                        reply_markup=kb, 
                                        parse_mode="HTML")
        except Exception as e: print("error in catalog/start:"+str(e))

    def select_location(self, callback):
        try:
            #* Создание клавиатуры
            kb = InlineKeyboardMarkup()
            b2 = InlineKeyboardButton(text="⛰️Красная поляна", callback_data=f"in_the_mountains")
            b1 = InlineKeyboardButton(text="🏖️Побережье", callback_data=f"by_the_sea")
            b3 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"back-to-catalog-1")
            kb.add(b1,b2)
            kb.add(b3)
            self.bot.edit_message_text(chat_id = callback.message.chat.id, 
                                        message_id=callback.message.message_id, 
                                        text="<b>"+self.text["catalog-2"]+"</b>", 
                                        reply_markup=kb, 
                                        parse_mode="HTML")
        except Exception as e: print("error in catalog/select_location: "+str(e))
        
    def select_sum(self, callback):
        try:
            print(f"{self.select=}")
            if self.select[callback.message.chat.id]["type"] in ["apartment", "Квартира"]:
                text_button = self.text["but-sum-apartment"]
            elif self.select[callback.message.chat.id]["type"] in ["house", "Дом"]:
                text_button = self.text["but-sum-house"]
            else:
                text_button = self.text["but-sum-comm_apartment"]

            kb = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text=text_button[0], 
                                    callback_data=f"sum-1")
            b2 = InlineKeyboardButton(text=text_button[1], 
                                    callback_data=f"sum-2")
            b3 = InlineKeyboardButton(text=text_button[2], 
                                    callback_data=f"sum-3")
            if self.select[callback.message.chat.id]["type"]=="comm_apartment":kb.add(b1,b2);kb.add(b3)
            else:
                b4 = InlineKeyboardButton(text=text_button[3], callback_data=f"sum-4")
                kb.add(b1,b2)
                kb.add(b3,b4)
            b5 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"back-to-catalog-2")
            kb.add(b5)
            self.bot.edit_message_text(chat_id = callback.message.chat.id, 
                                        message_id=callback.message.message_id, 
                                        text="<b>"+self.text["catalog-2"]+"</b>", 
                                        reply_markup=kb, 
                                        parse_mode="HTML")
        except Exception as e: print("error in catalog/select_sum:"+str(e))
    


    def show_apartment(self, callback):
        # try:
        if "sum-" in callback.data:
            self.list_show[callback.message.chat.id]=[]
            self.count_show[callback.message.chat.id]=0
        for i in self.list_show[callback.message.chat.id]:
            for msg in i:
                try:self.bot.delete_message(chat_id=callback.message.chat.id, message_id=msg.message_id)
                except:continue
        self.list_show[callback.message.chat.id]=[]

        if "back" in callback.data:
            self.count_show[callback.message.chat.id] -=1
        else:
            self.count_show[callback.message.chat.id] +=1

        print(self.count_show[callback.message.chat.id])
        if self.count_show[callback.message.chat.id]==0:
            print("go-to-sum")
            self.select_sum(callback)
        else:
                
            apartments={}
            for item in database().get_all(name="apartment"):
                apartments[item[0]] = {
                    "name":item[0],
                    "type":item[1],
                    "location":item[2],
                    "sum": item[3],
                    "description":item[4],
                    "photo":json.loads(item[5])
                }
            true_apartment=[]
            for item in apartments:
                if apartments[item]["type"]==self.select[callback.message.chat.id]["type"] and \
                    apartments[item]["location"]==self.select[callback.message.chat.id]["location"] and \
                    self.select[callback.message.chat.id]["sum"] in apartments[item]["sum"][-1]:
                        apartments[item]["name"]=item
                        true_apartment.append(apartments[item])
            
            
            if true_apartment!=[]:
                apartment=true_apartment[self.count_show[callback.message.chat.id]-1]
                # Замена callback названий на Русские
                apartment["type"] = apartment["type"].replace("comm_apartment", "Коммерческая недвижимость").replace("apartment", "Квартира").replace("house", "Дом")
                apartment["location"] = apartment["location"].replace("by_the_sea", "Побережье").replace("in_the_mountains", "Красная поляна")
                if apartment["type"]=="Квартира":apartment["sum"]=apartment["sum"].replace("sum-1", "До 20 млн руб").replace("sum-2", "До 50 млн руб").replace("sum-3","До 100 млн руб").replace("sum-4", "От 100 млн руб")
                if apartment["type"]=="Дом":apartment["sum"]=apartment["sum"].replace("sum-1", "До 50 млн руб").replace("sum-2", "До 100 млн руб").replace("sum-4","До 500 млн руб").replace("sum-4", "От 500 млн руб")
                else:apartment["sum"]=apartment["sum"].replace("sum-1", "До 100 млн руб").replace("sum-2", "До 500 млн руб").replace("sum-3","От 500 млн руб")
                
                self.apartment_for_select[callback.message.chat.id]=apartment

                text =f"""Тип: {apartment['type']}
Расположение: {apartment['location']}
Ценовая категория: {apartment['sum']}

{apartment['description']}

""" 
            else:
                apartment={
                    "type":self.select[callback.message.chat.id]["type"],
                    "location":self.select[callback.message.chat.id]["location"],
                    "sum":self.select[callback.message.chat.id]["sum"]
                }
                apartment["type"] = apartment["type"].replace("comm_apartment", "Коммерческая недвижимость").replace("apartment", "Квартира").replace("house", "Дом")
                apartment["location"] = apartment["location"].replace("by_the_sea", "Побережье").replace("in_the_mountains", "Красная поляна")
                if apartment["type"]=="Квартира":apartment["sum"]=apartment["sum"].replace("1", "До 20 млн руб").replace("2", "До 50 млн руб").replace("3","До 100 млн руб").replace("4", "От 100 млн руб")
                elif apartment["type"]=="Дом":apartment["sum"]=apartment["sum"].replace("1", "До 50 млн руб").replace("2", "До 100 млн руб").replace("3","До 500 млн руб").replace("4", "От 500 млн руб")
                else:apartment["sum"]=apartment["sum"].replace("1", "До 100 млн руб").replace("2", "До 500 млн руб").replace("3", "От 500 млн руб")
                                    
                text=f"""Не найдено апартаментов по данным характеристикам.
Вы выбрали:
Тип: {apartment["type"]}
Расположение: {apartment["location"]}
Ценовая категория: {apartment["sum"]}"""
                apartment["photo"]=[]
                apartment["name"]="error"

            kb = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text="Далее➡️", callback_data=f"next-image")
            b2 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"back-to-past-image")
            b3 = InlineKeyboardButton(text="✔️Выбрать", callback_data=f"select-apartment-this-name-")
            if "Не найдено апартаментов по данным характеристикам." not in text:    
                if self.count_show[callback.message.chat.id]!=len(true_apartment):
                    kb.add(b3)
                    kb.add(b1)
                    kb.add(b2)
                else:
                    kb.add(b3)
                    kb.add(b2)
            else:
                kb.add(b2)
            print(kb)
            if len(apartment['photo'])>=1:
                print("send photo")
                self.list_show[callback.message.chat.id].append(self.bot.send_media_group(chat_id=callback.message.chat.id, media=[telebot.types.InputMediaPhoto(open(dir, 'rb')) for dir in apartment['photo']]))
                print(self.list_show)
            self.bot.edit_message_text(chat_id = callback.message.chat.id, 
                                        message_id=callback.message.message_id, 
                                        text="<b>"+text+"</b>", 
                                        reply_markup=kb, 
                                        parse_mode="HTML")
    
        # except Exception as e: print("error in catalog/show_apartment:"+str(e))    



    def select_apartment(self, callback):
        try:
            kb = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text="Да, отправить", callback_data="send_select_apartment")
            b2 = InlineKeyboardButton(text="Нет, вернуться к выбору", callback_data="delete_select_apartment_menu")
            kb.add(b1).add(b2)
            
            text = """Хотите отправить свой выбор специалисту?"""

            self.bot.send_message(chat_id=callback.message.chat.id, text="<b>"+text+"</b>", reply_markup=kb, parse_mode="HTML")
        
        except Exception as e: print("error in catalog/select_apartment:"+str(e))
    
    def send_select_apartment(self, callback):
        try:
            self.bot.edit_message_text(chat_id=callback.message.chat.id, 
                                       message_id=callback.message.message_id,
                                       text="<b>Отправлено!</b>",
                                       parse_mode="HTML")
            chat_specialist = self.db.get_column(name="admin", column="id")[-1]
            apartment = self.apartment_for_select[callback.message.chat.id]
            text=f"""<b>Поступил новый выбор:
        
Пользователь: @{callback.from_user.username}

Выбрал карточку под именем: <em>{apartment['name']}</em>
 Тип: <em>{apartment['type']}</em>
 Расположение: <em>{apartment['location']}</em>
 Ценовой диапазон: <em>{apartment['sum']}</em></b>"""

            self.bot.send_message(chat_id=chat_specialist, text=text, parse_mode="HTML")
        
        except Exception as e: print("error in catalog/send_select_apartment:"+str(e))
        