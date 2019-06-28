# -*- coding: utf-8 -*-
#! /usr/bin/env python 
import config
import telebot
import pickle
from datetime import datetime, date, time
import requests
import sys
import sqlite3
import base64
import logistic

path, user_cards_keys, link_photo, city_of_receiver = {}, {}, {}, {}
curr_message, name_of_receiver, track_number, report = {}, {}, {}, {} 
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['help'])
def Help(message):
    text='''
Чтобы начать введите команду /Start 
'''
    bot.send_message(message.chat.id, text)
    return

@bot.message_handler(commands=['/Start'])
@bot.message_handler(content_types=["text"])
def crm_main(message):
    global path
    global curr_user_id
    global service_user_id
    global service_user_balance
    
    user_id = str(message.from_user.id)
    curr_message[user_id] = message.text  
    
    if user_id not in path.keys():
        path[user_id] = None    
       
    if path[user_id] == 'get_name_of_receiver':
        name_of_receiver[user_id] = message.text
        bot.send_message(message.chat.id, 'введите город получателя')    
        path[user_id] = 'get_city_of_receiver'

    elif path[user_id] == 'get_city_of_receiver':
        city_of_receiver[user_id] = message.text
        report[user_id] = logistic.accepted(user_id, name_of_receiver[user_id], city_of_receiver[user_id])# функция генерирует трек номер.
        # записывает в базу: имя получателя, трек номер, город отправления(определяет по ID отправителя), дату-время
        # возвращает репорт (запись добавлена, сообщите другому курьеру трек ! . нажмите /start чтобы продолжить)
        bot.send_message(message.chat.id, report[user_id])
        path[user_id] = 'command'
        
    elif path[user_id] == 'get_tracking_number':

        if curr_message[user_id] == '/Start' :
            bot.send_message(message.chat.id, '''
                                                 вы находитесь в меню отправки отчетов. вам доступны следующие команды:
                                                 /1  - отправить отчет о приеме посылки
                                                 /2  - отправить отчет о доставке посылки                                 
                                                 ''')
            path[user_id] = 'command' 

        else:
            track_number[user_id] = message.text
                 
            # flag, report = logistic.check_track(track_number[user_id]) - функция проверяет трек на наличие в базе и на принадлежность курьеру
            flag = True
            if flag:
                bot.send_message(message.chat.id, 'отправьте фото')
                path[user_id] = 'command'
                
            else:
                 report[user_id] = 'трек неверный, попробуйте еще раз или нажмите /Start для переходу в меню отправки отчетов'
                
    elif path[user_id] == 'command':
        if curr_message[user_id] == '/1' :
            bot.send_message(message.chat.id, 'введите имя получателя')
            path[user_id]='get_name_of_receiver'

        if curr_message[user_id] == '/2' :
            bot.send_message(message.chat.id, 'введите трек')
            path[user_id]='get_tracking_number'  
           
        if curr_message[user_id] == '/Start' :
            bot.send_message(message.chat.id, '''
                                                 вы находитесь в системе отправки отчетов. вам доступны следующие команды:
                                                 /1  - отправить отчет о приеме посылки
                                                 /2  - отправить отчет о доставке посылки                                 
                                                 ''')

    elif path[user_id] == None:
        if curr_message[user_id] == '/Start' :
            bot.send_message(message.chat.id, '''
                                                 вы находитесь в системе отправки отчетов. вам доступны следующие команды:
                                                 /1  - отправить отчет о приеме посылки
                                                 /2  - отправить отчет о доставке посылки                                 
                                                 ''')

            path[user_id]='command'
            
        else:
            bot.send_message(message.chat.id, 'повторите комманду')

    else:
            bot.send_message(message.chat.id, 'повторите комманду')
        
@bot.message_handler(content_types=['photo'])     # хендлер, срабатывающий при отправке фото в сообщении
def handle_docs_photo(message):
    
    try:
        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        user_id = str(message.from_user.id)  # определяем user_id для идентефикации сообщени             
        src=file_info.file_path    # создаем путь куда сохранить файл
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        binary = sqlite3.Binary(downloaded_file) # преобразуем изображение в БЛОБ
        print(binary)
        
        image_from_blob = base64.b64decode(binary)

        
        #files = {'photo': downloaded_file}
        #r = requests.post("http://testflask.space/file", files=files)
        #print(r.text)    
        
        link_photo[user_id] = src   # создаем ссылку на файл      
        report[user_id] = logistic.delivered(user_id, track_number[user_id], link_photo[user_id]) # вызываем функцию, которая записывает в базу дату и время доставки и ссылку на фото 
        bot.send_message(message.chat.id, report[user_id]) #  выводим сообщение о том что фото добавлено
        bot.send_photo(message.chat.id, image_from_blob)
        #bot.reply_to(message, "Фото добавлено и Функция 2 вызвана")
        print(path)
   
    except Exception as e:
        bot.reply_to(message,e )
        print('вызван except')
        
if __name__ == '__main__':
     bot.polling(none_stop=True)
