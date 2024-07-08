
import sqlite3
import json

class database():
    def __init__(self) -> None:
        pass


    def add_apartment(self, data):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()#number type location sum description photo
        data["photo"] = json.dumps(data["photo"])
        id = len(list(cursor.execute("SELECT name from apartment")))+1
        cursor.execute(f'INSERT INTO apartment  VALUES (?, ?, ?, ?, ?, ?)', 
                        (data["name"], data["type"], data["location"], data["sum"], data["description"],data["photo"]))
        db.commit()
        db.close()

    def add_user(self, user):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO user VALUES (?,?,?,?)', (user["id"], user["name"], user["last_use"], user["last_reminder"]))
        db.commit()
        db.close()


    def add_admin(self, data):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute((f'INSERT INTO admin  VALUES ("{data["id"]}", "{data["contact"]}")'))
        db.commit()
        db.close()


    def create_db(self):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS apartment (
        name STRING PRIMARY KEY,
        type STRING,
        location STRING,
        sum STRING,
        description STRING,
        photo TEXT
        )
        ''')
        db.commit()
        
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS user (
        id STRING PRIMARY KEY,
        name STRING,
        last_use DATE,
        last_reminder DATE
        )
        ''')

        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS admin (
        id STRING PRIMARY KEY,
        contact STRING
        )
        ''')
        db.close()
        db.close()
    
    def delete_all_db(slef, name):#name -> apartment/user
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute(f"""DROP TABLE {name}""")
        db.commit()
        db.close()
    
    def edit(self, name, id, data):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        # data -> {"name": value}
        for item in data:
            cursor.execute(f'''UPDATE {name} SET {item} = '{data[item]}' WHERE {"id" if name!="apartment" else "name"} = "{id}"''')
            db.commit()
        db.close()
    
    def get_all(self, name):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        res = cursor.execute(f"SELECT * FROM {name}")
        a = []
        for item in res:
            a.append(item)
        return a

    def get_line(self, id, name):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        res = cursor.execute(f'SELECT * FROM {name} WHERE {"name" if name=="apartment" else "id"} = "{id}"')
        for i in res:
            db.close()
            print(f"{i=}")
            return i
        
    def get_column(self, name, column):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        res = cursor.execute(f"SELECT {column} FROM {name}")
        a = []
        for i in res:
            a.append(i[0])
        db.close()
        return a
    

    def len_db(self, name):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        a = len(list(cursor.execute(f"SELECT {'name' if name=='apartment' else 'id'} from {name}")))
        db.close()
        return a
    
    def delete(self, id, name):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute(f'DELETE FROM {name} WHERE {"name" if name=="apartment" else "id"} = "{id}"');db.commit()
        db.close()
