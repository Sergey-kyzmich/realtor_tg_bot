import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from database import database

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
        self.list_show = {}#{"chat.id":[]}
        db = database()
        db.create_db()


    def delete_list_show(self, callback): self.list_show[callback.message.chat.id] = self.list_show[callback.message.chat.id][:-1]
    def add_to_list_show(self, callback, item): 
        if self.list_show[callback.message.chat.id]:
            self.list_show[callback.message.chat.id].append(item)
    def edit(self, callback,edit):
        if callback.message.chat.id not in self.select:
            self.select[callback.message.chat.id]={
            "location": "",
            "type": "",
            "sum": ""#квартиры/дома-1,2,3,4, коммерческое-1,2,3
        }
        if "location" in edit:self.select[callback.message.chat.id]["location"] = edit["location"]
        elif "type" in edit:self.select[callback.message.chat.id]["type"] = edit["type"]
        else: self.select[callback.message.chat.id]["sum"] = edit["sum"]

    def start(self, message, back=bool):
        #* Создание клавиатуры
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="🏢Квартира", callback_data=f"apartment")
        b2 = InlineKeyboardButton(text="🏠Дом", callback_data=f"house")
        b3 = InlineKeyboardButton(text="🏛Коммерческая недвижимость", callback_data=f"comm_apartment")
        kb.add(b1,b2)
        kb.add(b3)
        # if (back): callback->message else: message->message
        if back: self.msg[message.message.chat.id] = self.bot.edit_message_text(chat_id=message.message.chat.id, 
                                                                                message_id=self.msg[message.message.chat.id].message_id, 
                                                                                text = "<b>"+self.text["catalog-1"]+"</b>", 
                                                                                reply_markup=kb, 
                                                                                parse_mode="HTML")
        else: self.msg[message.chat.id] = self.bot.send_message(message.chat.id, 
                                                                text="<b>"+self.text["catalog-1"]+"</b>", 
                                                                reply_markup=kb, 
                                                                parse_mode="HTML")


    def select_location(self, callback):
        #* Создание клавиатуры
        kb = InlineKeyboardMarkup()
        b2 = InlineKeyboardButton(text="⛰️В горах", callback_data=f"in_the_mountains")
        b1 = InlineKeyboardButton(text="🏖️У моря", callback_data=f"by_the_sea")
        b3 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"back-to-catalog-1")
        kb.add(b1,b2)
        kb.add(b3)
        self.msg[callback.message.chat.id] = self.bot.edit_message_text(chat_id = callback.message.chat.id, 
                                                                        message_id=self.msg[callback.message.chat.id].message_id, 
                                                                        text="<b>"+self.text["catalog-2"]+"</b>", 
                                                                        reply_markup=kb, 
                                                                        parse_mode="HTML")

    
    def select_sum(self, callback):
        if self.select[callback.message.chat.id]["type"]=="apartment":
            text_button = self.text["but-sum-apartment"]
        elif self.select[callback.message.chat.id]["type"]=="house":
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
        self.msg[callback.message.chat.id] = self.bot.edit_message_text(chat_id = callback.message.chat.id, 
                                                                        message_id=self.msg[callback.message.chat.id].message_id, 
                                                                        text="<b>"+self.text["catalog-2"]+"</b>", 
                                                                        reply_markup=kb, 
                                                                        parse_mode="HTML")

    


    def show_apartment(self, callback):
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="Далее➡️", callback_data=f"next-image")
        b2 = InlineKeyboardButton(text="⬅️Назад", callback_data=f"back-to-past-image" if self.list_show[callback.message.chat.id]!=[] else "back-to-catalog-3")
        kb.add(b1)
        kb.add(b2)
        self.msg[callback.message.chat.id] = self.bot.edit_message_text(chat_id = callback.message.chat.id, 
                                                                        message_id=self.msg[callback.message.chat.id].message_id, 
                                                                        text="<b>"+self.text["catalog-2"]+"</b>", 
                                                                        reply_markup=kb, 
                                                                        parse_mode="HTML")