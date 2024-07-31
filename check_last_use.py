from database import database
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import time
import datetime
from text import text
def check_last_use(bot):
    db = database()
    while True:
        for item in db.get_all(name="user"):
            user={
                        "name":item[1],
                        "id":item[0],
                        "last_use":item[2],
                        "last_reminder":item[3]
                    }
            user_date, user_time = user["last_use"][:user["last_use"].index(".")].split(" ")
            year, month, day = user_date.split("-")
            hour, minute, second = user_time.split(":")
            date = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))
            td_use = datetime.datetime.now()-date

            td_reminder = user["last_reminder"]
            # last_reminder: 
            # 0 - небыло оповещений 
            # 1 - 30-ти минутное  
            # 2 - после 1-го дня
            # 3 - после 3-х дней
            # print(td_use.seconds,"|",td_use.days, "|", td_use.days>=3)
            if td_use.seconds>=1800:
                if td_reminder==0:
                    bot.send_message(chat_id=user["id"], text="<b>"+"Ваш риелтор еще на связи! Запросите дополнительные объекты для просмотра."+"</b>", parse_mode="HTML")
                    db.edit(name="user", id=user["id"], data={"last_reminder":1})
            if td_use.days>=1:
                if td_reminder==1:
                    bot.send_message(chat_id=user["id"], text="<b>"+"Вам понравилось что то из предложенных объектов? Напишите специалисту для отправки  дополнительных вариантов по вашему запросу."+"</b>", parse_mode="HTML")
                    db.edit(name="user", id=user["id"], data={"last_reminder":2})
            if td_use.days>=3:
                if td_reminder==2:
                    kb = InlineKeyboardMarkup()
                    b1 = InlineKeyboardButton("Каталог", callback_data="start_catalog")
                    b2 = InlineKeyboardButton("Связь со специалистом", callback_data="connect_to_spec")
                    kb.add(b1).add(b2)
                    print(kb)
                    print("add_kb")
                    bot.send_message(chat_id=user["id"], text="<b>"+"Среди вариантов недвижимости Сочи появились новые интересные предложения. Посмотрите их 👇"+"</b>", reply_markup=kb, parse_mode="HTML")
                    db.edit(name="user", id=user["id"], data={"last_reminder":3})

        time.sleep(1)
