from pyrogram import Client
import datetime
import time
import sqliteorm
import os
import sys
import math
from colorama import init
init(strip=not sys.stdout.isatty()) 
from termcolor import cprint 
from pyfiglet import figlet_format

def logo():
    cprint(figlet_format('telegram bot', font='standard'),
       'white', 'on_blue', attrs=['bold'])

def progress_bar(progress,total):   
    percent = 100 * (progress / float(total))
    bar = "█" * int(percent) + "-" * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%",end="\r")


account = sqliteorm.read_account()
time_delay = 10

app = Client(account[2],api_id=account[0],api_hash=account[1])

app.start()






while True:
    setting = sqliteorm.read_settings()
    scraping = setting[0]
    scraping_limit = setting[1]
    scraping_completed = setting[2]
    remove = setting[3]
    channel = setting[4]
    user = setting[5]
    add = setting[6]
    add_channel = setting[7]
    add_user = setting[8]
    spam = setting[9]
    spam_message = setting[10]*6000
    spam_photo = setting[11]
    spam_time = setting[12]
    spam_channel = setting[13]
    exit = setting[14]
    #app.send_message("me",f'{setting}')
    if scraping == True:
        if scraping_limit == 0:
            scraping_limit = None
        dialogs = app.get_dialogs()
        total = len(list(dialogs))
        print("Start scraping\n")
        progress_bar(0,total)
        i=0
        for dialog in app.get_dialogs():
            i+=1
            group = dialog.chat.username 
            group_id =  dialog.chat.id

            if group != None and group not in sqliteorm.table():  
                sqliteorm.create_table(group)
            history = app.get_chat_history(group_id,limit=scraping_limit)
            for mess in history:
                try:
                    user_id = int(mess.from_user.id)
                    username = mess.from_user.username
                    first_name = mess.from_user.first_name
                    last_name = mess.from_user.last_name
                    phone = mess.from_user.phone_number
                    status = str(mess.from_user.status)
                    group = mess.chat.username
                    group_id = int(mess.chat.id)
                    group_name = mess.chat.first_name or mess.chat.title
                    sqliteorm.add(group,value=(user_id,username,first_name,last_name,status,phone,group_id,group_name))
                except Exception as e:
                    pass 
            progress_bar(i,total)
        sqliteorm.edit_settings("scraping",0)
        sqliteorm.edit_settings("scraping_completed",1)

    if spam == True and (time.time() - float(spam_time)) > time_delay:
        channels = spam_channel.split("/")
        list_message = []
        if len(spam_message)>3000:
            spam_message = spam_message.split()
            n = len(spam_message)//400
            prec = 0
            for x in range(n):
                x += 1
                x*= 400
                list_message.append(spam_message[prec:x]) 
                prec = x

        if spam_photo != "None":
            try:
                for channel in channels:
                    if list_message:
                        for mess in list_message:
                            if mess == list_message[0]:
                                mess = " ".join(mess)
                                app.send_photo(int(channel),photo=spam_photo,caption=mess)
                            else:
                                mess = " ".join(mess)
                                app.send_message(int(channel),mess)
                            time.sleep(1)
                    else:
                        app.send_photo(int(channel),photo=spam_photo,caption=spam_message)
                sqliteorm.edit_settings("spam_time",str(time.time()))
            except:pass
        else:
            try:
                for channel in channels:
                    if list_message:
                        for mess in list_message:
                            mess = " ".join(mess)
                            app.send_message(int(channel),mess)
                            time.sleep(1)
                    else:
                        app.send_message(int(channel),spam_message)
                sqliteorm.edit_settings("spam_time",str(time.time()))
            except Exception as e:
                print(e)
    if remove == True:
        try:
            app.ban_chat_member(int(channel), int(user))
        except:
            pass
        sqliteorm.edit_settings("remove",0)
    if add == True:
        try:
            mess = app.send_message(int(add_user),text=".")
            app.delete_messages(chat_id=int(add_user),message_ids=mess.id)
            app.add_chat_members(int(add_channel), int(add_user))
            
        except:
            pass
        sqliteorm.edit_settings("adding",0)
    if exit == True:
        sqliteorm.edit_settings("exit",0)
        break




app.stop()
