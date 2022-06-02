import sqlite3
import os
import subprocess
import threading
import time
import sqliteorm
import sys




def run_bot():
    subprocess.run(["python3", "telegrambot.py"],stderr=subprocess.DEVNULL)
    #,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL

def install_requirments():
    subprocess.call("pip3 install -r requirments.txt",shell=True)

def logo():
    cprint(figlet_format('telegram bot', font='standard'),
       'white', 'on_blue', attrs=['bold'])




if not os.path.isfile("scraping.db"):
    requirment = input("Did you want to install requirments? (y/n):")
    if requirment == "y":
        install_requirments()
    clients= sqlite3.connect("scraping.db")
    c = clients.cursor()
    c.execute(f"""CREATE TABLE None (
            user_id int UNIQUE,
            username text,
            first_name text,
            last_name text,
            status text,
            phone text,
            group_id int,
            group_name text)""")
    c.execute(f"""CREATE TABLE settings (
            scraping integer,
            scraping_limit integer,
            scraping_completed integer,
            remove integer,
            remove_channel text,
            remove_user text,
            adding integer,
            add_channel text,
            add_user text,
            spam integer,
            spam_message text,
            spam_photo text,
            spam_time text,
            spam_channel text,
            exit integer)""")
    c.execute(f"""CREATE TABLE account (
            api_id int,
            api_hash text,
            username text)""")
    clients.commit()
    c.execute(f"""INSERT INTO settings (scraping,scraping_limit,scraping_completed,remove,remove_channel,remove_user,adding,add_channel,add_user,spam,spam_message,spam_photo,spam_time,spam_channel,exit)
                    VALUES (0,0,0,0,'None','None',0,'None','None',0,'None','None','0','None',0)""")
    clients.commit()

    api_id = input("insert your api_id:")
    api_hash = input("insert your api_hash:")
    username = input("insert your telegram username:")
    c.execute(f"""INSERT INTO account (api_id,api_hash,username)
                    VALUES ({api_id},'{api_hash}','{username}')""")
    clients.commit()
    clients.close()
    if not os.path.isfile(f"{username}.session"):
        from pyrogram import Client
        app = Client(username,api_id=api_id,api_hash=api_hash)
        app.start()
        app.stop()

from pandas import DataFrame
from pyrogram import Client
from colorama import init
init(strip=not sys.stdout.isatty()) 
from termcolor import cprint 
from pyfiglet import figlet_format

sqliteorm.edit_settings("exit",0)

   
t1 = threading.Thread(target=run_bot,daemon=True)
t1.start()


while True:
    os.system("clear")
    logo()
    option = input("\n[0] scraping\n[1] create an excel file\n[2] remove user from channel\n[3] add user to channel\n[4] set a spam message\n[5] stop spamming\n[6] exit\n\ntype a number:")
    os.system("clear")
    if option == "0":
        logo()
        edit_limit = input("\nWrite the numbers of messages that scraping must read for each chat or leave blank for reading all messages !!!ATTENTION leave blank take a very long time!!!:")
        if edit_limit == "":
            sqliteorm.edit_settings("scraping_limit",0) 
            sqliteorm.edit_settings("scraping",1) 
            os.system("clear")
            logo()
        else:
            edit_limit = int(edit_limit)
            os.system("clear")
            logo()
            sqliteorm.edit_settings("scraping_limit",edit_limit) 
            sqliteorm.edit_settings("scraping",1)
        sqliteorm.edit_settings("scraping_completed",0)
        while True:
            setting = sqliteorm.read_settings()
            scraping_completed = setting[2]
            if scraping_completed == True:
                break
        
    if option == "1":
        logo()
        tables = sqliteorm.table()
        tables.remove('settings')
        tables.remove('account')
        tables.sort()
        n = 0
        for tab in tables:
            print(f"[{n}] {tab}")
            n+=1
        print(f"\n\n[{n}] RETURN TO MAIN MENU\n")
        i  = input("Enter number of group:")
        try:
            table = tables[int(i)]
            clients= sqlite3.connect("scraping.db")
            c = clients.cursor()
            c.execute(f"SELECT * FROM '{table}'")
            value=c.fetchall()
            clients.close()
            dic = {'user_id': [],'username': [],'first_name': [],'last_name': [],'status': [],'phone': [],'group_id': [],'group_name': []}
            for user_id,username,first_name,last_name,status,phone,group_id,group_name in value:
                dic["user_id"].append(user_id)
                dic["username"].append(username)
                dic["first_name"].append(first_name)
                dic["last_name"].append(last_name)
                dic["status"].append(status)
                dic["phone"].append(phone)
                dic["group_id"].append(group_id)
                dic["group_name"].append(group_name)
            df = DataFrame(dic)
            df.to_excel(f'{table}.xlsx', sheet_name='sheet1', index=False)
            os.system("clear")
        except:
            os.system("clear")

    elif option == "2":
        logo()
        search = input("\n[0] search users from database\n[1] enter manually user ID and channel ID\n[2] return to main menu\n\ntype a number:")

        if search == "0":
            user_list = []
            while True:
                os.system("clear")
                logo()
                tables = sqliteorm.table()
                tables.remove('settings')
                tables.remove('account')
                tables.sort()
                n = 0
                for tab in tables:
                    print(f"[{n}] {tab}")
                    n+=1
                print(f"\n\n[{n}] stop to select\n\n")
                i  = input("Enter number of group:")
                if int(i) == n:
                    break
                os.system("clear")
                logo()
                try:
                    table = tables[int(i)]
                    users = sqliteorm.search(table)
                    n = 0
                    for user in users:
                        num = f'[{n}]'
                        utente = f'user:   {user[0]}-{user[1]}' 
                        group = f'from group:   {user[7]}'
                        print(f"{num:<10}{utente:<50}{group:>10}")
                        n+=1
                    print(f"\n\n[{n}] back to group list\n\n")
                    user_value = input("Enter number of user:")
                        
                    user = users[int(user_value)]
                    userID = user[0]
                    channelID = user[6]
                    user_list.append((channelID,userID))
                except:pass
            os.system("clear")
            logo()
            print(f'this user will be removed:\n{user_list}')
            time.sleep(3)
            for channel,user in user_list:
                sqliteorm.edit_settings("remove_channel",channel)
                sqliteorm.edit_settings("remove_user",user)
                sqliteorm.edit_settings("remove",1)
                while True:
                    setting = sqliteorm.read_settings()
                    remove = setting[3]
                    if remove == False:
                        break
        elif search == "1":
            os.system("clear")
            logo()
            channelID = input("\nInsert the channelID:")
            userID = input("Insert the user ID :")
            sqliteorm.edit_settings("remove_channel",channelID)
            sqliteorm.edit_settings("remove_user",userID)
            sqliteorm.edit_settings("remove",1)
        os.system("clear")
            


    elif option == "3":
        logo()
        search = input("\n[0] search users from database\n[1] enter manually user ID and channel ID\n[2] return to main menu\n\ntype a number:")

        if search == "0":
            user_list = []
            while True:
                os.system("clear")
                logo()
                tables = sqliteorm.table()
                tables.remove('settings')
                tables.remove('account')
                tables.sort()
                n = 0
                for tab in tables:
                    print(f"[{n}] {tab}")
                    n+=1
                print(f"\n\n[{n}] stop to select\n\n")
                i  = input("Enter number of group:")
                if int(i) == n:
                    break
                os.system("clear")
                logo()
                try:
                    table = tables[int(i)]
                    users = sqliteorm.search(table)
                    n = 0
                    for user in users:
                        num = f'[{n}]'
                        utente = f'user:   {user[0]}-{user[1]}' 
                        group = f'from group:   {user[7]}'
                        print(f"{num:<10}{utente:<50}{group:>10}")
                        n+=1
                    print(f"\n\n[{n}] back to group list\n\n")
                    user_value = input("Enter number of user:")
                        
                    user = users[int(user_value)]
                    userID = user[0]
                    channelID = user[6]
                    user_list.append(userID)
                except:pass
            os.system("clear")
            logo()
            channel = input("enter the channel ID where you would like add user:")
            print(f'this user will be add:\n{user_list}')
            time.sleep(3)
            for user in user_list:
                sqliteorm.edit_settings("add_channel",channel)
                sqliteorm.edit_settings("add_user",user)
                sqliteorm.edit_settings("adding",1)
                while True:
                    setting = sqliteorm.read_settings()
                    add = setting[6]
                    if add == False:
                        break
        elif search == "1":
            os.system("clear")
            logo()
            channelID = input("\nInsert the channelID:")
            userID = input("Insert the user ID :")
            sqliteorm.edit_settings("add_channel",channelID)
            sqliteorm.edit_settings("add_user",userID)
            sqliteorm.edit_settings("adding",1)
        os.system("clear")


    elif option == "4":
        logo()
        mess = input("\n[0] spam only message\n[1] spam message with photo\n[2] return to main menu\n\ntype a number:")
        if mess == "0":
            os.system("clear")
            logo()
            text = input("Type the message to spam:")
            os.system("clear")
            logo()
            select = input("\n[0] select users from database\n[1] enter users manually\n[2] return to main menu\n\ntype a number:")
            if select == "0":
                user_list = []
                while True:
                    os.system("clear")
                    logo()
                    tables = sqliteorm.table()
                    tables.remove('settings')
                    tables.remove('account')
                    tables.sort()
                    n = 0
                    for tab in tables:
                        print(f"[{n}] {tab}")
                        n+=1
                    print(f"\n\n[{n}] stop to select\n\n")
                    i  = input("Enter number of group:")
                    if int(i) == n:
                        break
                    os.system("clear")
                    logo()
                    try:
                        table = tables[int(i)]
                        users = sqliteorm.search(table)
                        n = 0
                        for user in users:
                            num = f'[{n}]'
                            utente = f'user:   {user[0]}-{user[1]}' 
                            group = f'from group:   {user[7]}'
                            print(f"{num:<10}{utente:<50}{group:>10}")
                            n+=1
                        print(f"\n\n[{n}] back to group list\n\n")
                        user_value = input("Enter number of user:")
                        
                        user = users[int(user_value)]
                        userID = user[0]
                        user_list.append(str(userID))
                    except:pass
                os.system("clear")
                logo()
                print(f'spam {text} to this users:\n{user_list}')
                time.sleep(3)
                spam_channel = "/".join(user_list)
                sqliteorm.edit_settings("spam_channel",spam_channel)
                sqliteorm.edit_settings("spam_photo","None")
                sqliteorm.edit_settings("spam_message",text)
                sqliteorm.edit_settings("spam",1)
            if select == "1":
                os.system("clear")
                logo()
                text = input("\nenter the text of your message :")
                channels = input("enter the chat ID where you want send message:")
                channels = channels.split()
                spam_channel = "/".join(channels)
                sqliteorm.edit_settings("spam_channel",spam_channel)
                sqliteorm.edit_settings("spam_photo","None")
                sqliteorm.edit_settings("spam_message",text)
                sqliteorm.edit_settings("spam",1)

        elif mess == "1":
            os.system("clear")
            logo()
            photo = input("\nenter the full name of photo example - sunrise.jpg !!!ATTENTION photo must be in this path!!!:")
            text = input("enter the text of your message :")
            os.system("clear")
            logo()
            select = input("\n[0] select users from database\n[1] enter users manually\n[2] return to main menu\n\ntype a number:")
            if select == "0":
                user_list = []
                while True:
                    os.system("clear")
                    logo()
                    tables = sqliteorm.table()
                    tables.remove('settings')
                    tables.remove('account')
                    tables.sort()
                    n = 0
                    for tab in tables:
                        print(f"[{n}] {tab}")
                        n+=1
                    print(f"\n\n[{n}] stop to select\n\n")
                    i  = input("Enter number of group:")
                    if int(i) == n:
                        break
                    os.system("clear")
                    logo()
                    try:
                        table = tables[int(i)]
                        users = sqliteorm.search(table)
                        n = 0
                        for user in users:
                            num = f'[{n}]'
                            utente = f'user:   {user[0]}-{user[1]}' 
                            group = f'from group:   {user[7]}'
                            print(f"{num:<10}{utente:<50}{group:>10}")
                            n+=1
                        print(f"\n\n[{n}] back to group list\n\n")
                        user_value = input("Enter number of user:")
                        
                        user = users[int(user_value)]
                        userID = user[0]
                        user_list.append(str(userID))
                    except:pass
                os.system("clear")
                logo()
                print(f'spam {text} to this users:\n{user_list}')
                time.sleep(3)
                spam_channel = "/".join(user_list)
                sqliteorm.edit_settings("spam_channel",spam_channel)
                sqliteorm.edit_settings("spam_photo",photo)
                sqliteorm.edit_settings("spam_message",text)
                sqliteorm.edit_settings("spam",1)
            if select == "1":
                os.system("clear")
                logo()
                channels = input("enter the chat ID where you want send message:")
                channels = channels.split()
                spam_channel = "/".join(channels)
                sqliteorm.edit_settings("spam_channel",spam_channel)
                sqliteorm.edit_settings("spam_photo",photo)
                sqliteorm.edit_settings("spam_message",text)
                sqliteorm.edit_settings("spam",1)
        os.system("clear")
    elif option == "5":
        sqliteorm.edit_settings("spam",0)    
    elif option == "6":
        sqliteorm.edit_settings("exit",1)
        sqliteorm.edit_settings("spam",0)
        sqliteorm.edit_settings("remove",0)
        sqliteorm.edit_settings("adding",0)
        while True:
            setting = sqliteorm.read_settings()
            exit = setting[14]
            if exit == False:
                break
        break


