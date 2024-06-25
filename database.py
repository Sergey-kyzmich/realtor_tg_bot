import sqlite3


class database():
    def __init__(self) -> None:
        pass


    def add_photo(self, data):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()#number type location sum description photo
        id = len(list(cursor.execute("SELECT number from apartment")))+1
        cursor.execute((f'INSERT INTO apartment  VALUES ("{id}", "{data["number"]}", "{data["type"]}", "{data["location"]}", "{data["sum"]}", "{data["description"]}", "{data["photo"]}")'))
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
        CREATE TABLE IF NOT EXISTS apartments (
        number STRING PRIMARY KEY,
        type STRING,
        location STRING,
        sum STRING,
        description STRING,
        photo STRING[]
        )
        ''')
        db.commit()
        
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS user (
        id STRING PRIMARY KEY,
        phone STRING[],
        name STRING,
        list_show STRING[],
        last_use DATE
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
            cursor.execute(f'''UPDATE {name} SET {item} = "{data[item]}" WHERE id = {id}''')
            db.commit()
        db.close()
    

    def get_line(self, id, name):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        res = cursor.execute(f"SELECT * FROM {name} WHERE {'id' if name=='user' else 'number'} = {id}")
        for i in res:
            db.close()
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
        a = len(list(cursor.execute(f"SELECT {'id' if name=='user' else 'number'} from {name}")))
        db.close()
        return a
    
    def delete(self, id, name):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM {name} WHERE {'id' if name=='user' else 'number'} = {id}");db.commit()
        len_d = int(database().len_db())
        id = int(id)
        if name=="apartment":
            for id in range(id, len_d+1):
                cursor.execute(f'''UPDATE {name} SET number = "{id}" WHERE number = {id+1}''');db.commit()
            db.close()