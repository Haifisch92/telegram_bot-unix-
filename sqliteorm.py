import sqlite3



def create_table(group):
    clients= sqlite3.connect("scraping.db")
    c = clients.cursor()
    c.execute(f"""CREATE TABLE {group} (
            user_id int UNIQUE,
            username text,
            first_name text,
            last_name text,
            status text,
            phone text,
            group_id int,
            group_name text)""")
    clients.commit()
    clients.close()

def table():
    clients= sqlite3.connect("scraping.db")
    c = clients.cursor()
    table = c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    table_name = [x[0] for x in list(table)]
    clients.close()
    return table_name

def search(table):
    clients= sqlite3.connect("scraping.db")
    c = clients.cursor()
    c.execute(f"SELECT * FROM {table}")
    value = c.fetchall()
    clients.close()
    return value

def add(table,value):
    clients= sqlite3.connect("scraping.db")
    c = clients.cursor()
    c.execute(f"INSERT OR REPLACE INTO {table} (user_id,username,first_name,last_name,status,phone,group_id,group_name) VALUES(?,?,?,?,?,?,?,?)",value)
    clients.commit()
    clients.close()

def read_settings():
    clients= sqlite3.connect("scraping.db")
    c = clients.cursor()
    c.execute("SELECT * FROM settings")
    settings = c.fetchall()
    clients.close()
    return settings[0]    

def read_account():
    clients= sqlite3.connect("scraping.db")
    c = clients.cursor()
    c.execute("SELECT * FROM account")
    account = c.fetchall()
    clients.close()
    return account[0]  

def edit_settings(field,value):

    clients= sqlite3.connect("scraping.db")
    c = clients.cursor()
    if type(value) == int:
        c.execute(f"UPDATE settings SET {field} = {value} WHERE rowid = 1")
    else:
        c.execute(f"UPDATE settings SET {field} = '{value}' WHERE rowid = 1")
    clients.commit()
    clients.close()



if __name__ == "__main__":
    #create_table("gab")
    table()
    edit_settings("spam",1)