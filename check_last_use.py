from database import database
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

            user_date, user_time = user["last_reminder"][:user["last_reminder"].index(".")].split(" ")
            year, month, day = user_date.split("-")
            hour, minute, second = user_time.split(":")
            date = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))
            td_reminder = datetime.datetime.now()-date

            if td_use.days>=3:
                if td_reminder.days>=3:
                    bot.send_message(chat_id=user["id"], text=text["reminder"])
                    db.edit(name="user", id=user["id"], data={"last_reminder":datetime.datetime.now()})
            elif td_use.days>=7:
                if td_reminder.days>=4:#7дней-3дня
                    bot.send_message(chat_id=user["id"], text=text["reminder"])
                    db.edit(name="user", id=user["id"], data={"last_reminder":datetime.datetime.now()})
            elif td_use.days>=14:
                if td_reminder.days>=7:#14дней-7дней
                    bot.send_message(chat_id=user["id"], text=text["reminder"])
                    db.edit(name="user", id=user["id"], data={"last_reminder":datetime.datetime.now()})

        time.sleep(5*60)
